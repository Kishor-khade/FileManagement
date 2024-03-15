from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Document, UserProfile, Staff
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as django_logout


@login_required
def upload_document(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        is_public = request.POST.get('is_public') == 'on'
        Document.objects.create(owner=request.user.userprofile, title=title, content=content, is_public=is_public)
        return redirect('document_list')
    return render(request, 'upload_document.html')

@login_required
def document_list(request):
    documents = Document.objects.filter(is_public=True)
    staff_member = UserProfile.objects.get(user__username=request.user.username)
    return render(request, 'document_list.html', {'documents': documents})


def add_owner(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        # Check if passwords match
        if password != confirm_password:
            return render(request, 'add_owner.html', {'error_message': 'Passwords do not match'})
        # Check if username already exists
        if User.objects.filter(username=username).exists():
            print('user exist ')
            return render(request, 'add_owner.html', {'error_message': 'Username already exists'})
        print('user not exists already ')

        # Create new user
        user = User.objects.create_user(username=username, password=password)
        
        # Create UserProfile for the owner
        user_profile = UserProfile.objects.create(user=user,is_owner=True)
        print("user created sucessfully")
        return redirect('login')  # Redirect to login page after owner creation
    return render(request, 'add_owner.html')



@login_required
def add_staff(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        # Check if passwords match
        if password != confirm_password:
            print('Passwords do not match')
            return render(request, 'add_staff.html', {'error_message': 'Passwords do not match'})
        
        # Check if username already exists
        if User.objects.filter(username=username).exists():
            print('Username already exists')
            return render(request, 'add_staff.html', {'error_message': 'Username already exists'})

        # Create new user
        
        # Get the owner user profile
        user = User.objects.create_user(username=username, password=password)
        owner_profile = request.user.userprofile  # Assuming the current user is the owner
        user_profile = UserProfile.objects.create(user=user)
        # Create UserProfile for the staff member
        staff_profile = Staff.objects.create(user=user_profile, owner=owner_profile)
        
        return redirect('login')  # Redirect to login page after staff creation
    return render(request, 'add_staff.html')




def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            # Check if the user is an owner or a staff member
            user_profile = UserProfile.objects.get(user=user)
            if user_profile.is_owner:
                print("Owner Found")
                owner_profile = request.user.userprofile
                staff_members = Staff.objects.filter(owner=owner_profile)
                return render(request, 'owner_dashboard.html',{'staffs': staff_members})
            else:
                # Redirect to staff dashboard
                print("Staff Found")
                documents = Document.objects.filter(is_public=True)
                return render(request, 'staff_dashboard.html', {'documents':documents})
        else:
            print("invalid login")
            return render(request, 'login.html', {'error_message': 'Invalid username or password'})
    return render(request, 'login.html')


def home(request):
    return render(request, 'home.html')


def logout(request):
    django_logout(request)
    return redirect('home')


def delete_document(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    owner_profile = request.user.userprofile
    staff_members = Staff.objects.filter(owner=owner_profile)
    # Check if the document belongs to one of the owner's staff members
    if document.owner in staff_members:
        document.delete()
        return redirect('documents_list')
    if document.owner == owner_profile:
        document.delete()
        return redirect('document_list')  # Redirect to the owner dashboard after deletion
    else:
        # Handle unauthorized access or display an error message
        return render(request, 'error.html', {'message': 'You are not authorized to delete this document.'})



