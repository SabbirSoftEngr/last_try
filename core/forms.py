from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, BloodRequest, BLOOD_GROUPS

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.is_active = False  # require email verification
        if commit:
            user.save()
        return user

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('full_name', 'age', 'address', 'blood_group', 'last_donation_date', 'available', 'phone')
        widgets = {'last_donation_date': forms.DateInput(attrs={'type': 'date'})}

class BloodRequestForm(forms.ModelForm):
    class Meta:
        model = BloodRequest
        fields = ('blood_group', 'units', 'hospital', 'location', 'needed_date', 'details')
        widgets = {'needed_date': forms.DateInput(attrs={'type': 'date'})}

class BloodFilterForm(forms.Form):
    blood_group = forms.ChoiceField(choices=[('', 'All')] + BLOOD_GROUPS, required=False)
