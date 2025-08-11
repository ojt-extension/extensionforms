

# accounts/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required


from .forms import OJTCoordinatorCreationForm, OJTCoordinatorLoginForm



def coordinator_auth(request):
    # Determine if a signup form or login form was submitted
    if request.method == 'POST':
        # Check if it's the signup form submission
        if 'username' in request.POST and 'email' in request.POST:
            signup_form = OJTCoordinatorCreationForm(request.POST)
            if signup_form.is_valid():
                user = signup_form.save(commit=False)
                user.is_coordinator = True
                user.save()
                messages.success(request, 'Account created successfully! You can now log in.')
                return redirect('coordinator_auth')
            else:
                login_form = OJTCoordinatorLoginForm()
                return render(request, 'accounts/login_signup.html', {'login_form': login_form, 'signup_form': signup_form, 'show_signup': True})

        # Assume it's a login form submission otherwise
        else:
            login_form = OJTCoordinatorLoginForm(request, data=request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                if user.is_superuser:
                    return redirect('admin_dashboard')
                else:
                    return redirect('coordinator_dashboard')
            else:
                messages.error(request, 'Invalid email/username or password.')
                signup_form = OJTCoordinatorCreationForm()
                return render(request, 'accounts/login_signup.html', {'login_form': login_form, 'signup_form': signup_form, 'show_signup': False})
    
    # If it's a GET request, initialize the forms
    else:
        login_form = OJTCoordinatorLoginForm()
        signup_form = OJTCoordinatorCreationForm()

    context = {
        'login_form': login_form,
        'signup_form': signup_form,
        'show_signup': False  # Default to showing the login tab
    }
    return render(request, 'accounts/login_signup.html', context)

def coordinator_logout(request):
    logout(request)
    return redirect('coordinator_auth')

@login_required
def admin_dashboard(request):
    """
    The custom dashboard for the superuser.
    This will eventually show all submitted reports.
    """
    # You can add logic here to fetch all reports from the database
    # and pass them to the template's context.
    
    return render(request, 'accounts/admin_dashboard.html')


@login_required
def coordinator_dashboard(request):
    """
    The main dashboard for OJT coordinators.
    This view now passes a list of forms to the template.
    """
    forms = [
        {'name': 'Table 10: Media Features', 'url_name': 'table_10_form'},
        {'name': 'Table 11: Technologies Commercialized', 'url_name': 'table_11_form'},
        # Add other forms here as needed
    ]
    
    context = {
        'forms': forms,
    }
    return render(request, 'media_features/dashboard.html', context)