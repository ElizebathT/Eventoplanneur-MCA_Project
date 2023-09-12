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
from django.core.mail import send_mail
# import requests
from django.http import JsonResponse

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


@login_required
def webinar(request):
    try:
        user_profile = EventOrganizer.objects.get(org_user=request.user)
    except EventOrganizer.DoesNotExist:
        # If the user does not have a profile, redirect them to the profile creation page
        return redirect('eventapp:org_profile') 
    orgs=request.user
    update_webinar=Webinar.objects.filter(org_user=orgs)
    context = {'update_webinar': update_webinar}
    return render(request, 'webinar.html', context)

def view_webinar(request,update_id):
    task=Webinar.objects.get(id=update_id)
    form=WebinarForm(request.POST or None,instance=task)
    speakers = task.speakers.all()
    return render(request,'view_webinar.html',{'form':form,'speakers': speakers})

# def delete_webinar(request,del_id):
#     task=Webinar.objects.get(id=del_id)
#     task.delete()
#     return redirect('eventapp:webinar')

@login_required
def delete_webinar(request, del_id):
    webinar = Webinar.objects.get(id=del_id)
    organizer_email = webinar.org_user.email  
    subject = 'Webinar Deleted'
    message = f'The webinar "{webinar.title}" on {webinar.date} at {webinar.time} has been deleted.'
    from_email = 'mailtoshowvalidationok@gmail.com'  
    recipient_list = [organizer_email]

    send_mail(subject, message, from_email, recipient_list)
    webinar.delete()

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
            recipient_email = request.user.email
            subject = 'Webinar Registration Confirmation'
            message = f'Thank you for registering the webinar: {webinar.title} on {webinar.date} at {webinar.time}.'
            from_email = 'mailtoshowvalidationok@gmail.com'  # Replace with your email address
            recipient_list = [recipient_email]  # Use the organizer's email or another recipient

            send_mail(subject, message, from_email, recipient_list)

            interested_users = ['elizebaththomasv@gmail.com', 'elizatom9@gmail.com']  # Replace with actual email addresses
            webinar_link = 'http://127.0.0.1:8000/'  # Replace with the actual webinar details page URL
            email_subject = f'Upcoming Webinar: {webinar.title}'
            email_message = f'Hello,\n\nThere is an upcoming webinar that you may be interested in: {webinar.title} on {webinar.date} at {webinar.time}.\n\nYou can find more details and register for the webinar here: {webinar_link}.\n\nPoster Link: {webinar.poster}'
            from_email = 'elizatom9@gmail.com' 
            send_mail(email_subject, email_message, from_email, interested_users)

            # hosting_department = webinar.department  # Assuming this is the hosting department
            # matching_colleges = AICTE.objects.filter(departments=hosting_department)

            # # Find matching colleges based on specified programs
            # specified_programs = webinar.programs_offered.all()
            # matching_colleges |= AICTE.objects.filter(programs_offered__in=specified_programs)

            # # Send emails to matching colleges
            # for college in matching_colleges:
            #     subject = 'Webinar Notification'
            #     message = f'There is an upcoming webinar: {webinar.title} on {webinar.date} at {webinar.time} that may be of interest to your college. You can find more details and register for the webinar here: {webinar_link}'
            #     from_email = 'your@email.com'  # Replace with your email address
            #     recipient_list = [college.email]  # Use the college's email or another recipient

            #     send_mail(subject, message, from_email, recipient_list)

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
    org_user = request.user

    try:
        organizer_instance = EventOrganizer.objects.get(org_user=org_user)
    except EventOrganizer.DoesNotExist:
        organizer_instance = None

    if request.method == "POST":
        if organizer_instance:
            form = Organizer(request.POST, instance=organizer_instance)
        else:
            form = Organizer(request.POST)

        if form.is_valid():
            event_organizer = form.save(commit=False)
            event_organizer.org_user = org_user
            event_organizer.save()
            return redirect('eventapp:org_profile')

    else:
        form = Organizer(instance=organizer_instance)

    return render(request, 'org_profile.html', {'form': form})

def update_org_profile(request):
    orgs=request.user
    task=EventOrganizer.objects.get(org_user=orgs)
    form=Organizer(request.POST or None,instance=task)
    if form.is_valid():
        form.save()
        return redirect('eventapp:update_org_profile')
    return render(request,'update_webinar.html',{'form':form})


def update_webinar(request, update_id):
    webinar = Webinar.objects.get(id=update_id)
    if request.method == 'POST':
        form = WebinarForm(request.POST, instance=webinar)
        if form.is_valid():
            form.save()

            # Update speakers
            for speaker in webinar.speakers.all():
                designation_field = f"speakers-{speaker.id}-designation"
                name_field = f"speakers-{speaker.id}-speaker_name"
                speaker.designation = request.POST.get(designation_field)
                speaker.speaker_name = request.POST.get(name_field)
                speaker.save()

            messages.success(request, "Webinar and speakers updated successfully")
            return redirect('eventapp:update_webinar', update_id=update_id)
        else:
            messages.error(request, form.errors)
    else:
        form = WebinarForm(instance=webinar)

    speakers = webinar.speakers.all()
    return render(request, 'update_webinar.html', {'form': form, 'speakers': speakers})


def check_aicte_id(request):
    aicte_id = request.GET.get('aicte_id')
    
    try:
        aicte = AICTE.objects.get(aicte_id=aicte_id)
        return JsonResponse({'valid': True, 'name': aicte.name, 'location': aicte.location,'address': aicte.address})
    except AICTE.DoesNotExist:
        return JsonResponse({'valid': False, 'name': None, 'location': None,'address': None})
