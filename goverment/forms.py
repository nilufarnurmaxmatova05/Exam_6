from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Ministry, Minister, Department, UserProfile


class MinistryForm(forms.ModelForm):
    class Meta:
        model = Ministry
        fields = ['name', 'description', 'established_date', 'website']
        widgets = {
            'established_date': forms.DateInput(attrs={'type': 'date'}),
        }


class MinisterForm(forms.ModelForm):
    class Meta:
        model = Minister
        fields = ['first_name', 'last_name', 'middle_name', 'photo', 'birth_date',
                  'gender', 'biography', 'ministry', 'position', 'appointment_date',
                  'email', 'phone']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'appointment_date': forms.DateInput(attrs={'type': 'date'}),
            'biography': forms.Textarea(attrs={'rows': 5}),
        }


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'ministry', 'description', 'head']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone', 'address', 'photo']