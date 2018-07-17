from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from PIL import Image

from . import forms
from . import models

def sign_in(request):
    """Sign in view"""
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            if form.user_cache is not None:
                user = form.user_cache
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(
                        reverse('accounts:profile_detail')  # TODO: go to profile
                    )
                else:
                    messages.error(
                        request,
                        "That user account has been disabled."
                    )
            else:
                messages.error(
                    request,
                    "Username or password is incorrect."
                )
    return render(request, 'accounts/sign_in.html', {'form': form})


def sign_up(request):
    """Sign up view"""
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )
            login(request, user)
            messages.success(
                request,
                "You're now a user! You've been signed in, too."
            )
            return HttpResponseRedirect(reverse('accounts:profile_detail'))  # TODO: go to profile
    return render(request, 'accounts/sign_up.html', {'form': form})


@login_required
def sign_out(request):
    """Sign out view"""
    logout(request)
    messages.success(request, "You've been signed out. Come back soon!")
    return HttpResponseRedirect(reverse('home'))


@login_required
def change_password(request):
    """User's change password view"""
    form = forms.ChangePasswordForm()
    user = request.user
    if request.method == "POST":
            form = forms.ChangePasswordForm(data=request.POST, request=request)
            if form.is_valid():
                request.user.set_password(form.cleaned_data['new_password'])
                request.user.save()
                update_session_auth_hash(request, user)
                messages.success(request, "You've updated your password!")
                return HttpResponseRedirect(reverse('accounts:profile_detail'))
    else:
        form = forms.ChangePasswordForm(request=request)
    return render(request, 'accounts/change_password.html', {'form': form})


@login_required
def create_profile(request):
    """User's create profile view"""
    try:
        profile = models.Profile.objects.get(user=request.user)
    except models.Profile.DoesNotExist:
        profile = None
    form = forms.ProfileForm(instance=profile)
    if request.method == 'POST':
        form = forms.ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.add_message(request, messages.SUCCESS,
                                 "You've created your profile!")
            return HttpResponseRedirect(reverse('home'))
    return render(request, 'accounts/create_profile.html', {'form': form})


@login_required
def profile_detail(request):
    """Show profile detail view"""
    try:
        profile = models.Profile.objects.get(user=request.user)
    except models.Profile.DoesNotExist:
        profile = None
    return render(request, 'accounts/profile_detail.html', {'profile': profile })


@login_required
def edit_profile(request):
    """User's editing profile view"""
    try:
        profile = models.Profile.objects.get(user=request.user)
    except models.Profile.DoesNotExist:
        profile=None
    form = forms.ProfileForm(instance=profile)
    if request.method == 'POST':
        form = forms.ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, "You've updated your profile!")
            return HttpResponseRedirect(reverse('home'))
    return render(request, 'accounts/edit_profile.html', {'form': form})
