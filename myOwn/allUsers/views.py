from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegisForm

def register(request):
    if request.method == 'POST':
        regisForm = RegisForm(request.POST)
        # RegisForm is a class inherets from the UserCreationForm
        # but with customizations
        if regisForm.is_valid():
            regisForm.save()
            # if not save, there isn't data in admin
            username = regisForm.cleaned_data.get('username')
            # .cleaned_data is a dictionary
            messages.success(request, f'{username}, your account has been created. Please feel free to log in!')
            return redirect('login')
    else:
        # this is to create a form to be passed to the template for the view
        regisForm = RegisForm()
        # this UserCreationForm gives user space to type in username and password
    return render(request, 'allUsers/register.html', {'regisForm': regisForm})

@login_required
def profile(request):
    return render(request, 'allUsers/profile.html')