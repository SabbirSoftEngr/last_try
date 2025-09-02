from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponseForbidden, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .forms import RegistrationForm, ProfileForm, BloodRequestForm, BloodFilterForm
from .models import Profile, BloodRequest, Donation
from .tokens import email_verification_token
from django.views.generic import TemplateView

class AboutView(TemplateView):
    template_name = "pages/about.html"

class PrivacyView(TemplateView):
    template_name = "pages/privacy.html"

class TermsView(TemplateView):
    template_name = "pages/terms.html"

class ContactView(TemplateView):
    template_name = "pages/contact.html"

def home(request):
    form = BloodFilterForm(request.GET or None)
    donors = Profile.objects.filter(available=True).select_related('user').order_by('full_name')
    if form.is_valid():
        bg = form.cleaned_data.get('blood_group')
        if bg:
            donors = donors.filter(blood_group=bg)
    return render(request, 'home.html', {'donors': donors, 'form': form})

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = email_verification_token.make_token(user)
            verify_url = request.build_absolute_uri(reverse('verify_email', args=[uid, token]))
            subject = 'Verify your Blood Bank account'
            message = render_to_string('emails/verify_email.txt', {'user': user, 'verify_url': verify_url})
            send_mail(subject, message, None, [user.email])
            return redirect('verification_sent')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def verification_sent(request):
    return render(request, 'registration/verification_sent.html')

def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception:
        user = None
    if user is not None and email_verification_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Email verified! You can now log in.')
        return redirect('login')
    else:
        messages.error(request, 'Invalid or expired verification link.')
        return redirect('register')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Please verify your email before logging in.')
        else:
            messages.error(request, 'Invalid credentials.')
    return render(request, 'registration/login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def dashboard_index(request):
    return render(request, 'dashboard/index.html')

@login_required
def edit_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated.')
            return redirect('dashboard')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'dashboard/profile_form.html', {'form': form})

@login_required
def create_request(request):
    if request.method == 'POST':
        form = BloodRequestForm(request.POST)
        if form.is_valid():
            br = form.save(commit=False)
            br.requester = request.user
            br.save()
            messages.success(request, 'Blood request created.')
            return redirect('recipient_requests')
    else:
        form = BloodRequestForm()
    return render(request, 'dashboard/request_form.html', {'form': form})

@login_required
def list_recipient_requests(request):
    requests_qs = BloodRequest.objects.filter(status='OPEN').exclude(requester=request.user).select_related('requester').order_by('-created_at')
    return render(request, 'dashboard/requests.html', {'requests': requests_qs})

@login_required
def accept_request(request, pk):
    br = get_object_or_404(BloodRequest, pk=pk)
    if br.requester_id == request.user.id:
        return HttpResponseForbidden('You cannot accept your own request.')
    if br.status != 'OPEN':
        messages.error(request, 'This request is not open.')
        return redirect('recipient_requests')
    Donation.objects.create(donor=request.user, request=br, status='PLEDGED')
    br.status = 'ACCEPTED'
    br.save()
    messages.success(request, 'You accepted this request. It\'s now in your history.')
    return redirect('donation_history')

@login_required
def cancel_request(request, pk):
    br = get_object_or_404(BloodRequest, pk=pk)
    if br.requester_id != request.user.id:
        if hasattr(br, 'donation') and br.donation.donor_id == request.user.id:
            br.donation.status = 'CANCELED'
            br.donation.save()
            br.status = 'CANCELED'
            br.save()
            messages.success(request, 'You canceled your donation.')
            return redirect('donation_history')
        raise Http404()
    br.status = 'CANCELED'
    if hasattr(br, 'donation'):
        br.donation.status = 'CANCELED'
        br.donation.save()
    br.save()
    messages.success(request, 'Request canceled.')
    return redirect('donation_history')

@login_required
def mark_donated(request, pk):
    br = get_object_or_404(BloodRequest, pk=pk)
    if not hasattr(br, 'donation'):
        messages.error(request, 'No donor yet.')
        return redirect('donation_history')
    if request.user.id not in [br.donation.donor_id, br.requester_id]:
        raise Http404()
    br.donation.status = 'DONATED'
    br.donation.save()
    br.status = 'COMPLETED'
    br.save()
    messages.success(request, 'Marked as donated.')
    return redirect('donation_history')

@login_required
def donation_history(request):
    as_donor = Donation.objects.filter(donor=request.user).select_related('request').order_by('-created_at')
    as_recipient = BloodRequest.objects.filter(requester=request.user).order_by('-created_at')
    return render(request, 'dashboard/history.html', {'as_donor': as_donor, 'as_recipient': as_recipient})


@login_required
def resend_verification(request):
    user = request.user
    if user.is_active:
        messages.info(request, 'Your account is already verified.')
        return redirect('home')

    from .tokens import email_verification_token  # ensure import at top if not present
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = email_verification_token.make_token(user)
    verify_url = request.build_absolute_uri(reverse('verify_email', args=[uid, token]))

    subject = 'Verify your Blood Bank account'
    message = render_to_string('emails/verify_email.txt', {
        'user': user,
        'verify_url': verify_url,
    })

    # from_email=None -> uses DEFAULT_FROM_EMAIL
    send_mail(subject, message, None, [user.email])

    messages.success(request, 'Verification email sent again. Please check your inbox.')
    return redirect('verification_sent')
