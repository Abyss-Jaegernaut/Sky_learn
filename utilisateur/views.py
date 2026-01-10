from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .forms import UtilisateurCreationForm

@login_required
def profile(request):
    return render(request, 'accounts/profile.html', {'title': 'Profil'})

@login_required
def edit_profile(request):
    return render(request, 'setting/profile_info_change.html')

@login_required
def change_password(request):
    return render(request, 'setting/password_change.html')

@login_required
def admin_panel(request):
    return render(request, 'setting/admin_panel.html')

def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = UtilisateurCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'registration/login.html', {'form': form, 'mode': 'sign-up'})
    else:
        form = UtilisateurCreationForm()
    
    return render(request, 'registration/login.html', {'form': form, 'mode': 'sign-up'})
