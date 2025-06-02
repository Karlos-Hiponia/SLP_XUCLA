from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Activity, ULASActivity
from django.contrib.auth.forms import SetPasswordForm


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', 'Passwords do not match.')

        return cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'nickname', 'year_admitted', 'office_name', 'law_school',
            'work_cell', 'roll_number', 'sector', 'office_address', 'profile_picture'
        ]


class ActivityForm(forms.ModelForm):
    other_activity_type = forms.CharField(
        max_length=100, required=False, label='Please specify activity type')

    declaration = forms.BooleanField(
        required=True,
        label="I attest that all the information provided in this form is true and correct. I understand that any false declaration may subject me to accountability under ULAS policies and protocols.",
        error_messages={'required': 'You must agree to the declaration to submit this form.'}
    )

    class Meta:
        model = Activity
        exclude = ['user', 'status']  
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
        help_texts = {
            'description': 'Please provide a brief but clear narrative of the legal activity conducted. Avoid including confidential or sensitive client information. Focus on the nature of the service rendered, legal issues addressed, and the type of assistance provided (e.g., legal counseling, document drafting, representation, etc.).',
            'number_of_students': 'Indicate how many law student interns or externs were supervised during the activity.',
            'number_of_clients': 'State the number of distinct clients who received legal services during this activity.',
            'hours_rendered': 'Provide the total number of hours spent in rendering the legal service, including preparation, meetings, and follow-up work (if any).',
            'proof': 'Kindly upload here a general picture showing your work rendered. Please be mindful of sensitive and confidential materials.',
        }

    def clean(self):
        cleaned_data = super().clean()
        activity_type = cleaned_data.get('activity_type')
        other_activity_type = cleaned_data.get('other_activity_type')
        if activity_type == 'Other (Please specify)':
            if not other_activity_type:
                self.add_error('other_activity_type', 'This field is required when selecting Other.')
            else:
                cleaned_data['activity_type'] = other_activity_type
        return cleaned_data

    def clean_clients_served(self):
        value = self.cleaned_data.get('clients_served')
        try:
            return int(value)
        except (ValueError, TypeError):
            raise forms.ValidationError("Please enter a valid number.")


class ULASActivityForm(forms.ModelForm):
    class Meta:
        model = ULASActivity
        exclude = ['user', 'status']
        fields = [
            'activity_type', 'description', 'students_supervised',
            'clients_served', 'date_of_activity', 'hours_rendered', 'proof_image'
        ]
        widgets = {
            'activity_type': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'students_supervised': forms.NumberInput(attrs={'class': 'form-control'}),
            'clients_served': forms.NumberInput(attrs={'class': 'form-control'}),
            'date_of_activity': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hours_rendered': forms.NumberInput(attrs={'class': 'form-control'}),
            'proof_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean_clients_served(self):
        value = self.cleaned_data.get('clients_served')
        try:
            return int(value)
        except (ValueError, TypeError):
            raise forms.ValidationError("Please enter a valid number.")


class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your email',
        'autocomplete': 'email',
    }))


class PasswordResetCodeForm(forms.Form):
    code = forms.CharField(label="Reset Code", max_length=6, widget=forms.TextInput(attrs={
        'class': 'form-control code-input',
        'placeholder': 'Enter the 6-digit code',
        'autocomplete': 'one-time-code',
    }))


class PasswordResetSetForm(SetPasswordForm):
    new_password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your new password',
        'autocomplete': 'new-password',
    }))
    new_password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Confirm your new password',
        'autocomplete': 'new-password',
    }))
