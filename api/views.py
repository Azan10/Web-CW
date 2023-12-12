from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_http_methods
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm
from django.shortcuts import render




def main_spa(request: HttpRequest) -> HttpResponse:
    return render(request, 'api/spa/index.html', {})



def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user and get the user instance
            login(request, user)  # Log the user in
            return JsonResponse({"success": True, "message": "Account created successfully!"}, status=200)
    else:
        form = CustomUserCreationForm()

    return render(request, 'signup.html', {'form': form})





# Login page using the default AuthenticationForm
@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)  # Use the default AuthenticationForm
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')  # Redirect to the home page after successful login
    else:
        form = AuthenticationForm()  # Use the default AuthenticationForm
    return render(request, 'login.html', {'form': form})


@login_required
def profile_update(request):
    if request.method == 'POST':
        user = request.user
        data = request.POST
        user.email = data.get('email', user.email)
        user.date_of_birth = data.get('date_of_birth', user.date_of_birth)
        if 'profile_image' in request.FILES:
            user.profile_image = request.FILES['profile_image']
        user.save()
        return JsonResponse({'status': 'success', 'message': 'Profile updated successfully'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

# Logout page
def user_logout(request):
    logout(request)
    return redirect('login')  # Redirect to the login page after logout
