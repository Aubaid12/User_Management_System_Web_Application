from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import UserForm
from .models import User
from django.contrib.auth import authenticate, login

@login_required(login_url='login')
def index(request):
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})


@login_required(login_url='login')
def user_detail(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    return render(request, 'user_details.html', {'user': user})


@login_required(login_url='login')
def add_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'User added successfully!')
            send_notification_email(user)
            return redirect('user_list')

    else:
        form = UserForm()
    return render(request, 'add_user.html', {'form': form})


@login_required(login_url='login')
def edit_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User updated successfully!')
            return redirect('index')
    else:
        form = UserForm(instance=user)
    return render(request, 'edit_user.html', { 'user_id': user_id, 'form': form  })


@login_required(login_url='login')
def delete_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.delete()
    messages.success(request, 'User deleted successfully!')
    return redirect('index')


def send_notification_email(user):
    subject = 'New user registered'
    message = f'A new user {user.name} has been registered with email {user.email}.'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [from_email]
    send_mail(subject, message, from_email, recipient_list)


@login_required(login_url='login')
def users_list(request):
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')  # or any other page you want to redirect to after login
        else:
            error_message = "Invalid login credentials. Please try again."
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')