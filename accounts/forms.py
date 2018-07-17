from django import forms
#from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from . import models
from datetime import datetime


class ProfileForm(forms.ModelForm):
    """User profile form"""
    birth_date = forms.DateField(
                    input_formats=['%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y'],
                    help_text='YYYY-MM-DD, MM/DD/YYYY, or MM/DD/YY'
                    )
    bio = forms.CharField(widget=forms.Textarea, min_length=10)

    class Meta:
        model = models.Profile
        fields = (
            'first_name',
            'last_name',
            'email',
            'verify_email',
            'birth_date',
            'bio',
            'avatar'
        )
        help_texts = {
            'verify_email':_('Please enter your email again.')
        }

    def clean(self):
        cleaned_data = super(ProfileForm, self).clean()
        email = cleaned_data.get('email')
        verify = cleaned_data.get('verify_email')
        avatar = cleaned_data.get('avatar')

        if email != verify:
            raise forms.ValidationError(
                "You need to enter the same email in both fields")


class ChangePasswordForm(forms.Form):
    """User change password form"""
    old_password = forms.CharField(widget=forms.PasswordInput())
    new_password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean(self):
        user = self.request.user
        cleaned_data = super(ChangePasswordForm, self).clean()
        old_password = cleaned_data.get('old_password')
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        # Check for new password and confirm password match
        if new_password != confirm_password:
            raise forms.ValidationError(
                "New password and confirm password didn't match.")

        # Check for old password and new password are different
        if old_password == new_password:
            raise forms.ValidationError(
                "New password must not be the same as the current password.")

        # Check for min length
        if len(new_password) < 14:
            raise forms.ValidationError(
                "Minimum password length is 14 characters.")

        # Check for uppercase
        if not any(char.isupper() for char in new_password):
            raise forms.ValidationError(
                "Password must contain at least 1 uppercase.")

        # Check for lowercase
        if not any(char.islower() for char in new_password):
            raise forms.ValidationError(
                "Password must contain at least 1 lowercase.")

        # Check for digit
        if sum(char.isdigit() for char in new_password) < 1:
            raise forms.ValidationError(
                "Password must contain at least 1 number.")

        # Check for special characters
        special_caracters = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
        if not any(char in special_caracters for char in new_password):
            raise forms.ValidationError(
                """Password must contain at least 1 special caracter,
                such as  @, #, $""")


        # Check if password contains username, first name or last name
        username = user.username.lower()
        current_user = self.request.user.current_user
        first_name = current_user.first_name.lower()
        last_name = current_user.last_name.lower()

        if username in new_password.lower():
            raise forms.ValidationError("Cannot contain your username" )

        if first_name in new_password.lower():
            raise forms.ValidationError("Cannot contain your first name")

        if last_name in new_password.lower():
            raise forms.ValidationError("Cannot contain your last name")
