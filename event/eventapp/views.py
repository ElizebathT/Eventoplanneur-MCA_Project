from django.contrib import messages
from django.shortcuts import render, redirect,get_object_or_404
#from .models import User
from .models import CustomUser,Webinar,EventOrganizer,AICTE,Speaker
import re
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User,auth
from .forms import WebinarForm, Organizer
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect
from django.urls import reverse
# import requests
# from django.http import JsonResponse

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        return False
    return True

def is_valid_password(password):
    pattern = r'^(?=.*[0-9])(?=.*[!@#$%^&*])(?=.*[A-Z]).{8,}$'
    if not re.match(pattern, password):
        return False
    return True

def is_valid_name(name):
    pattern = r'^[A-Za-z\s]+$'
    if not re.match(pattern, name):
        return False
    return True

def registration(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_type = request.POST.get('userType') 
        if not is_valid_email(email):
            messages.error(request, 'Invalid email')
            return render(request, 'register.html')   
        if not is_valid_password(password):
            messages.error(request, 'Password must be at least 8 characters long and contain at least one number, one symbol, and one capital letter')
            return render(request, 'register.html')
        
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
        elif email and password and user_type:
            user = CustomUser(email=email)
            user.set_password(password)
            if user_type == 'eventOrganizer':
                user.is_organizer = True
            elif user_type == 'serviceProvider':
                user.is_provider = True
            elif user_type == 'attendee':
                user.is_provider = True
            user.save()
            return redirect('/')
    return render(request, 'register.html')

def reg_organizer(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        if not is_valid_email(email):
            messages.error(request, 'Invalid email')
            return render(request, 'reg_organizer.html') 
        if not is_valid_password(password):
            messages.error(request, 'Password must be at least 8 characters long and contain at least one number, one symbol, and one capital letter')
            return render(request, 'reg_organizer.html')
        
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
        elif email and password:
            user = CustomUser(email=email)
            user.set_password(password)
            user.is_organizer="True"
            user.save()
            return redirect('eventapp:login')
    return render(request, 'reg_organizer.html')

def reg_attendee(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        if not is_valid_email(email):
            messages.error(request, 'Invalid email')
            return render(request, 'reg_attendee.html') 
        if not is_valid_password(password):
            messages.error(request, 'Password must be at least 8 characters long and contain at least one number, one symbol, and one capital letter')
            return render(request, 'reg_attendee.html')
        
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
        elif email and password:
            user = CustomUser(email=email)
            user.set_password(password)
            user.is_attendee="True"
            user.save()
            return redirect('eventapp:login')
    return render(request, 'reg_attendee.html')

def reg_provider(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        if not is_valid_email(email):
            messages.error(request, 'Invalid email')
            return render(request, 'reg_provider.html') 
        if not is_valid_password(password):
            messages.error(request, 'Password must be at least 8 characters long and contain at least one number, one symbol, and one capital letter')
            return render(request, 'reg_provider.html')
        
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
        elif email and password:
            user = CustomUser(email=email)
            user.set_password(password)
            user.is_provider="True"
            user.save()
            return redirect('eventapp:login')
    return render(request, 'reg_provider.html')

def index(request):
    return render(request, 'index.html')

def orghome(request):
    return render(request, 'orghome.html')

def logout(request):
    auth_logout(request)
    return redirect('/')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
                    
        if email and password:
            user = authenticate(request, email=email, password=password)
            if user is not None:
                auth_login(request, user)
                request.session['user_id'] = user.id
                request.session['user_type'] = 'organizer' 
                if user.is_organizer:
                    return redirect('eventapp:orghome')
                else:
                    return redirect('/')
            else:
                try:
                    user = CustomUser.objects.get(email=email)
                    messages.error(request, "Incorrect password")
                except CustomUser.DoesNotExist:
                    messages.error(request, "Email not registered")
        else:
            messages.error(request, "Please provide both email and password")
    
    return render(request, 'login.html')

# @login_required
# def org_profile(request):
#     orgs = request.user
#     TaskFormSet = modelformset_factory(EventOrganizer, form=Organizer, extra=0)
#     formset = None  # Initialize formset to None

#     if request.method == 'POST':
#         try:
#             # Attempt to get the user's existing profile
#             formset = TaskFormSet(request.POST, queryset=EventOrganizer.objects.filter(org_user=orgs))
#         except EventOrganizer.DoesNotExist:
#             # If the profile doesn't exist, create a new one
#             formset = TaskFormSet(request.POST)            
#         if formset.is_valid():
#             formset.save()
#             messages.success(request, "Profile updated successfully")
#             return HttpResponseRedirect(reverse('some_success_view_name'))  # Redirect to a success view
#         else:
#             messages.error(request, "Profile not saved. Please check the form.")
    
#     return render(request, 'org_profile.html', {'formset': formset})

@login_required
def webinar(request):
    # update_webinar = Webinar.objects.all()
    orgs=request.user
    update_webinar=Webinar.objects.filter(org_user=orgs)
    context = {'update_webinar': update_webinar}
    return render(request, 'webinar.html', context)

def view_webinar(request,update_id):
    task=Webinar.objects.get(id=update_id)
    form=WebinarForm(request.POST or None,instance=task)
    speakers = task.speakers.all()
    return render(request,'view_webinar.html',{'form':form,'speakers': speakers})
# def view_webinar(request, update_id):
#     # Retrieve the Webinar instance
#     webinar = get_object_or_404(Webinar, id=update_id)

#     # Retrieve all associated Speaker instances
#     speakers = webinar.speakers.all()

#     if request.method == 'POST':
#         form = WebinarForm(request.POST, instance=webinar)
#         if form.is_valid():
#             form.save()
#             # Handle form submission, e.g., redirect to a success page
#             return redirect('success_url')
#     else:
#         form = WebinarForm(instance=webinar)

#     return render(request, 'view_webinar.html', {'webinar': webinar, 'speakers': speakers, 'form': form})


# def view_webinar(request, update_id):
#     # Get the Webinar instance to view/update
#     webinar = get_object_or_404(Webinar, id=update_id)

#     if request.method == 'POST':
#         form = WebinarForm(request.POST, instance=webinar)
#         if form.is_valid():
#             form.save()
#             # Handle form submission, e.g., redirect to a success page
#             return redirect('success_url')
#     else:
#         form = WebinarForm(instance=webinar)

#     return render(request, 'view_webinar.html', {'webinar': webinar, 'form': form})

def delete_webinar(request,del_id):
    task=Webinar.objects.get(id=del_id)
    task.delete()
    return redirect('eventapp:webinar')

@login_required
def register_webinar(request):
    if request.method == 'POST':
        form = WebinarForm(request.POST)
        if form.is_valid():
            # Save the webinar without committing to the database yet
            webinar = form.save(commit=False)
            # Set the organizer to the currently logged-in user
            webinar.org_user = request.user
            webinar.save()  # Commit the webinar to the database

            # Process speakers
            speakers_designation = request.POST.getlist('speakers_designation[]')
            speakers_name = request.POST.getlist('speakers_name[]')
            for i in range(len(speakers_designation)):
                speaker = Speaker.objects.create(
                    designation=speakers_designation[i],
                    speaker_name=speakers_name[i]
                )
                webinar.speakers.add(speaker)  # Add the speaker to the webinar

            messages.success(request, "Webinar saved successfully")
            return redirect('eventapp:register_webinar')
        else:
            print(form.errors)
            messages.error(request, form.errors)
    else:
        form = WebinarForm()
    return render(request, 'register_webinar.html', {'form': form})
@login_required
def org_profile(request):
    orgs=request.user
    try:
        task=EventOrganizer.objects.get(org_user=orgs)
    except EventOrganizer.DoesNotExist:
        if request.method == "POST":
            form = Organizer(request.POST)
            if form.is_valid():
                event_organizer = form.save(commit=False)
                event_organizer.org_user = orgs  # Set the user association
                event_organizer.save()
                return redirect('eventapp:org_profile')
        else:
            form = Organizer()
    else:
        form=Organizer(request.POST or None,instance=task)
        if form.is_valid():
            form.save()
            return redirect('eventapp:org_profile')
    return render(request, 'org_profile.html', {'form': form})

def update_org_profile(request):
    orgs=request.user
    task=EventOrganizer.objects.get(org_user=orgs)
    form=Organizer(request.POST or None,instance=task)
    if form.is_valid():
        form.save()
        return redirect('eventapp:update_org_profile')
    return render(request,'update_webinar.html',{'form':form})


def update_webinar(request,update_id):
    task=Webinar.objects.get(id=update_id)
    form=WebinarForm(request.POST or None,instance=task)
    if form.is_valid():
        org=form.save(commit=False)
        org.org_user=request.user
        form.save()
        return redirect('eventapp:webinar')
    return render(request,'update_webinar.html',{'form':form})

# def check_aicte(request):
#     if request.method == 'POST':
#         aicte = request.POST.get('aicte')
#         print(aicte)
#         if AICTE.objects.filter(aicte=aicte).exists():
#             messages.error(request, "Email already exists.")
#     return render(request, 'org_profile.html')


# def proxy_to_external_domain(request):
#     url = request.GET.get('url')
#     response = requests.get(url)
#     return JsonResponse({'data': response.text})