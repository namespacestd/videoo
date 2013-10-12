from django.db import models
from django import forms
from django.contrib.auth.models import User


class Profile(models.Model):
    """
    User profile, extending the base user class
    """
    email_address = models.CharField(max_length=100)

#class LoginForm(forms.Form):
#    username = forms.CharField(max_length=100)
#    password = forms.CharField(max_length=30,
#        widget=forms.PasswordInput)

#class CreateAccountForm(forms.ModelForm):
#    """
#    Account creation form, including username, password and email address.
#    """
#    username = forms.RegexField(label="Username", max_length=30,
#        regex=r'^[\w.@+-]{6,30}$',
#        help_text="Required. Between 6 and 30 characters. Letters, digits and @/./+/-/_ only.",
#        error_messages={'invalid': "This value may contain only letters, numbers and @/./+/-/_ characters."})
#    password1 = forms.CharField(label="Password",
#        widget=forms.PasswordInput)
#    password2 = forms.CharField(label="Password confirmation",
#        widget=forms.PasswordInput,
#        help_text="Enter the same password as above, for verification.")
#    email_address = forms.CharField(label="Email address")
#
#    class Meta:
#        model = Profile
#        fields = ("username","email_address")
#
#    def clean_username(self):
#        username = self.cleaned_data["username"]
#        try:
#            User._default_manager.get(username=username)
#        except User.DoesNotExist:
#            return username
#        raise forms.ValidationError("A user with that username already exists.")
#
#    def clean_password2(self):
#        password1 = self.cleaned_data.get("password1")
#        password2 = self.cleaned_data.get("password2")
#        if password1 and password2 and password1 != password2:
#            raise forms.ValidationError("The two password fields didn't match.")
#        return password2
#
#    def save(self, commit=True):
#        user = super(CreateAccountForm, self).save(commit=False)
#        user.set_password(self.cleaned_data.get("password1"))
#        user.email_address = self.cleaned_data.get("email_address")
#        if commit:
#            user.save()
#        return user