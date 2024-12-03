from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import Group
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Add the user to the 'Property Owners' group
            property_owners_group = Group.objects.get(name='Property Owners')
            property_owners_group.user_set.add(user)

            login(request, user)  # Automatically log in the user after signing up
            return redirect('/admin')  # Redirect to the home page or any other page after signup
    else:
        form = CustomUserCreationForm()

    return render(request, 'inventory/signup.html', {'form': form})
