from django import forms
from django.core import validators
from app.models import Customer, Rating
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.core.exceptions import ValidationError
from django.forms import fields, models, widgets
from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from app.models import Contact

class RatingForm(forms.Form):
    rating = forms.ChoiceField(choices=Rating.RATING_CHOICES, widget=forms.RadioSelect)
    
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'locality', 'city', 'zipcode', 'state']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'locality': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'zipcode': forms.NumberInput(attrs={'class': 'form-control'}),
            'state': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        zipcode = self.cleaned_data.get('zipcode')
        if(len(str(zipcode)) != 6):
            raise ValidationError("Zipcode should be length of 6")
        return self.cleaned_data


class CustomerRegistratiopnForm(UserCreationForm):
    password1 = forms.CharField(
        label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control my-2'}))
    password2 = forms.CharField(
        label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control my-2'}))
    email = forms.CharField(label='Email', widget=forms.EmailInput(
        attrs={'class': 'form-control my-2'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {'email': 'Email'}
        widgets = {'username': forms.TextInput(
            attrs={'class': 'form-control my-2'})}

    def clean(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email is already registered")
        return self.cleaned_data


class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(
        attrs={'autofocus': True, 'class': 'form-control'}))
    password = forms.CharField(label="Password", strip=False, widget=forms.PasswordInput(
        attrs={'autocomplete': 'current-password', 'class': 'form-control'}))


class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Old Password", strip=False, widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'current-password', 'autofocus': True}))

    new_password1 = forms.CharField(
        label="New Password", strip=False, widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'new-password'}), help_text=password_validation.password_validators_help_text_html())

    new_password2 = forms.CharField(
        label="Confirm New Password", strip=False, widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'new-password'}))


class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label="Email", max_length=254, widget=forms.EmailInput(attrs={'class': 'form-control', 'autocomplete': 'email'}))


class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label='New Password', strip=False, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'auto-complete': 'new-password'}), help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label='Confirm Password', strip=False, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'auto-complete': 'new-password'}))
    
    

class ContactForm(forms.ModelForm):
    fullname = forms.CharField(required=True, max_length=100)
    email = forms.EmailField(required=True, max_length=254)
    phone_number = forms.CharField(max_length=15, required=True)
    subject = forms.CharField(required=True, max_length=200)
    message = forms.CharField(required=True, widget=forms.Textarea)
    
    class Meta:
        model = Contact
        fields = [
            'fullname',
            'email',
            'subject',
            'message',
            'phone_number',
        ]
        
    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['fullname'].widget.attrs['placeholder'] = 'Your FullName'
        self.fields['fullname'].widget.attrs['class'] = 'form-control form-control-lg'
        self.fields['email'].widget.attrs['class'] = 'form-control form-control-sm'
        self.fields['email'].widget.attrs['placeholder'] = 'Your Email'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Your Contact Number'
        self.fields['phone_number'].widget.attrs['class'] = 'form-control'
        self.fields['subject'].widget.attrs['placeholder'] = 'Your Subject'
        self.fields['subject'].widget.attrs['class'] = 'form-control form-control-sm'
        self.fields['message'].widget.attrs['placeholder'] = 'Your Message'
        self.fields['message'].widget.attrs['cols'] = '30'
        self.fields['message'].widget.attrs['rows'] = '10'


class AdminContactForm(forms.ModelForm):
    fullname = forms.CharField(required=True,max_length=100)
    email = forms.EmailField(required=True,max_length=100)
    subject = forms.CharField(required=True,max_length=300)
    phone = forms.CharField(required=True,max_length=100)
    message = forms.CharField(required=True,widget=forms.Textarea)

    class Meta:
        model = Contact
        fields = [
            'fullname',
            'email',
            'subject',
            'message',
            'phone',
        ]

    def __init__(self, *args, **kwargs):
        super(AdminContactForm, self).__init__(*args, **kwargs)
        self.fields['fullname'].widget.attrs['placeholder'] = 'Full Name'
        self.fields['email'].widget.attrs['placeholder'] = 'E-mail Address'
        self.fields['subject'].widget.attrs['placeholder'] = 'Subject'
        self.fields['phone'].widget.attrs['placeholder'] = 'Contact Number'
        self.fields['message'].widget.attrs['placeholder'] = 'Message'
        self.fields['fullname'].widget.attrs['class'] = 'name half'
        self.fields['phone'].widget.attrs['class'] = 'phone half ml-3'
        self.fields['email'].widget.attrs['class'] = 'email'
