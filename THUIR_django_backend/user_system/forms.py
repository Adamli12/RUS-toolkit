#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'defaultstr'

from django import forms

search_frequency_choices = (
    ('', u''),
    ('frequently', u'multiple times a day'),
    ('usually', u'one time a day'),
    ('sometimes', u'twice or three times a week'),
    ('rarely', u'no more than one time a week'),
)
search_history_choices = (
    ('', u''),
    ('very long', u'more than 5 years'),
    ('long', u'3~5 years'),
    ('short', u'1~3 year'),
    ('very short', u'less than 1 year'),
)


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control login-field',
                'placeholder': u'username',
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control login-field',
                'placeholder': u'password',
            }
        )
    )


class SignupForm(forms.Form):
    username = forms.CharField(
        required=True,
        min_length=6,
        label=u'username',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control login-field',
                'placeholder': u'username',
            }
        )
    )
    password = forms.CharField(
        required=True,
        min_length=6,
        label=u'password',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control login-field',
                'placeholder': u'password',
            }
        )
    )
    password_retype = forms.CharField(
        required=True,
        min_length=6,
        label=u'please input password again',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control login-field',
                'placeholder': u'please input password again',
            }
        )
    )
    name = forms.CharField(
        required=True,
        label=u'real name',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control login-field',
                'placeholder': u'real name',
            }
        )
    )
    sex = forms.CharField(
        required=True,
        label=u'gender',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control login-field',
                'placeholder': u'gender',
            }
        )
    )
    age = forms.IntegerField(
        required=True,
        label=u'age',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control login-field',
                'placeholder': u'age',
            }
        )
    )
    phone = forms.CharField(
        required=True,
        label=u'phone number',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control login-field',
                'placeholder': u'phone number',
            }
        )
    )
    email = forms.EmailField(
        required=True,
        label=u'email',
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control login-field',
                'placeholder': u'email',
            }
        )
    )
    field = forms.CharField(
        required=True,
        label=u'career or major',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control login-field',
                'placeholder': u'career or major',
            }
        )
    )
    search_frequency = forms.ChoiceField(
        required=True,
        choices=search_frequency_choices,
        label=u'frequency of using search engine',
        widget=forms.Select(
            attrs={
                'class': 'select2-container form-control select select-primary',
            }
        )
    )
    search_history = forms.ChoiceField(
        required=True,
        choices=search_history_choices,
        label=u'history of using search engine',
        widget=forms.Select(
            attrs={
                'class': 'select2-container form-control select select-primary',
            }
        )
    )

    def clean(self):
        cleaned_data = super(SignupForm, self).clean()
        password = cleaned_data.get('password')
        password_retype = cleaned_data.get('password_retype')

        if password != password_retype:
            raise forms.ValidationError(
                u'different passwords are given'
            )

        return cleaned_data


class EditInfoForm(forms.Form):
    name = forms.CharField(
        required=True,
        label=u'real name',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control login-field',
                'placeholder': u'real name',
            }
        )
    )
    sex = forms.CharField(
        required=True,
        label=u'gender',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control login-field',
                'placeholder': u'gender',
            }
        )
    )
    age = forms.IntegerField(
        required=True,
        label=u'age',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control login-field',
                'placeholder': u'age',
            }
        )
    )
    phone = forms.CharField(
        required=True,
        label=u'phone number',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control login-field',
                'placeholder': u'phone number',
            }
        )
    )
    email = forms.EmailField(
        required=True,
        label=u'email',
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control login-field',
                'placeholder': u'email',
            }
        )
    )
    field = forms.CharField(
        required=True,
        label=u'career or major',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control login-field',
                'placeholder': u'career or major',
            }
        )
    )
    search_frequency = forms.ChoiceField(
        required=True,
        choices=search_frequency_choices,
        label=u'frequency of using search engine',
        widget=forms.Select(
            attrs={
                'class': 'select2-container form-control select select-primary',
            }
        )
    )
    search_history = forms.ChoiceField(
        required=True,
        choices=search_history_choices,
        label=u'history of using search engine',
        widget=forms.Select(
            attrs={
                'class': 'select2-container form-control select select-primary',
            }
        )
    )


class EditPasswordForm(forms.Form):

    cur_password = forms.CharField(
        required=True,
        min_length=6,
        label=u'current password',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control login-field',
                'placeholder': u'password',
            }
        )
    )
    new_password = forms.CharField(
        required=True,
        min_length=6,
        label=u'new password',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control login-field',
                'placeholder': u'password',
            }
        )
    )
    new_password_retype = forms.CharField(
        required=True,
        min_length=6,
        label=u'please input password again',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control login-field',
                'placeholder': u'please input password again',
            }
        )
    )

    def clean(self):
        cleaned_data = super(EditPasswordForm, self).clean()
        password = cleaned_data.get('new_password')
        password_retype = cleaned_data.get('new_password_retype')

        if password != password_retype:
            raise forms.ValidationError(
                u'different passwords are given'
            )

        return cleaned_data


class ForgetPasswordForm(forms.Form):
    email = forms.EmailField(
        required=True,
        label=u'email',
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control login-field',
                'placeholder': u'email',
            }
        )
    )


class ResetPasswordForm(forms.Form):

    new_password = forms.CharField(
        required=True,
        min_length=6,
        label=u'new password',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control login-field',
                'placeholder': u'password',
            }
        )
    )
    new_password_retype = forms.CharField(
        required=True,
        min_length=6,
        label=u'please input password again',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control login-field',
                'placeholder': u'please input password again',
            }
        )
    )

    def clean(self):
        cleaned_data = super(ResetPasswordForm, self).clean()
        password = cleaned_data.get('new_password')
        password_retype = cleaned_data.get('new_password_retype')

        if password != password_retype:
            raise forms.ValidationError(
                u'different passwords are given'
            )

        return cleaned_data