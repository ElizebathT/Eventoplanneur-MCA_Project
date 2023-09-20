from django.contrib import messages
from django.shortcuts import render, redirect,get_object_or_404
#from .models import User
from .models import CustomUser,Webinar,EventOrganizer,AICTE,Speaker,Conference,WebinarRegistration
import re
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User,auth
from .forms import WebinarForm, Organizer,ConferenceForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.forms import modelformset_factory
from django.http import HttpResponse
from django.urls import reverse
from django.core.mail import send_mail
from django.utils import timezone
# import requests
from django.http import JsonResponse
from django.utils.crypto import get_random_string

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
        user = CustomUser.objects.create_user(email=email, password=password)
        token = get_random_string(length=32)
        user.verification_token = token
        user.is_verified = False
        if user_type == 'eventOrganizer':
            user.is_organizer = True
        elif user_type == 'serviceProvider':
            user.is_provider = True
        elif user_type == 'attendee':
            user.is_provider = True
        user.save()
        send_mail(
            'Email Verification',
            f'Click the following link to verify your email: {request.build_absolute_uri("/verify/")}?token={token}',
            'mailtoshowvalidationok@gmail.com',
            [email],
            fail_silently=False,
        )
        return redirect('eventapp:verify')
    return render(request, 'register.html')

def reg_organizer(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
        user = CustomUser.objects.create_user(email=email, password=password)
        token = get_random_string(length=32)
        user.verification_token = token
        user.is_verified = False
        user.is_organizer=True
        user.save()
        send_mail(
            'Email Verification',
            f'Click the following link to verify your email: {request.build_absolute_uri("/verify/")}?token={token}',
            'mailtoshowvalidationok@gmail.com',
            [email],
            fail_silently=False,
        )

        return redirect('eventapp:verify')

    return render(request, 'reg_organizer.html')

def verify(request):
    token = request.GET.get('token')
    user = CustomUser.objects.filter(verification_token=token).first()
    if user:
        user.is_verified = True
        user.verification_token = None
        user.save()
        return redirect('/')  # Redirect to login page after successful verification
    else:
        return render(request, 'invalid_token.html')  # Handle invalid token
    
def reg_attendee(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
        user = CustomUser.objects.create_user(email=email, password=password)
        token = get_random_string(length=32)
        user.verification_token = token
        user.is_verified = False
        user.is_attendee=True
        user.save()
        send_mail(
            'Email Verification',
            f'Click the following link to verify your email: {request.build_absolute_uri("/verify/")}?token={token}',
            'mailtoshowvalidationok@gmail.com',
            [email],
            fail_silently=False,
        )

        return redirect('eventapp:verify')
    return render(request, 'reg_attendee.html')

def reg_provider(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
        user = CustomUser.objects.create_user(email=email, password=password)
        token = get_random_string(length=32)
        user.verification_token = token
        user.is_verified = False
        user.is_provider=True
        user.save()
        send_mail(
            'Email Verification',
            f'Click the following link to verify your email: {request.build_absolute_uri("/verify/")}?token={token}',
            'mailtoshowvalidationok@gmail.com',
            [email],
            fail_silently=False,
        )

        return redirect('eventapp:verify')
    return render(request, 'reg_provider.html')

def index(request):
    return render(request, 'index.html')

def orghome(request):
    return render(request, 'orghome.html')

def attendeehome(request):
    return render(request, 'attendeehome.html')

def gallery(request):
    return render(request, 'gallery.html')

def logout(request):
    auth_logout(request)
    return redirect('/')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
                    
        if email and password:
            user = authenticate(request, email=email, password=password)
            if user is not None and user.is_verified:
                auth_login(request, user)
                request.session['user_id'] = user.id
                # request.session['user_type'] = 'organizer' 
                if user.is_organizer:
                    return redirect('eventapp:orghome')
                if user.is_attendee:
                    return redirect('eventapp:attendeehome')
                else:
                    return redirect('/')
            else:
                try:
                    user = CustomUser.objects.get(email=email)
                    messages.error(request, "Email not verified or Incorrect password")
                except CustomUser.DoesNotExist:
                    messages.error(request, "Email not registered")
        else:
            messages.error(request, "Please provide both email and password")
    
    return render(request, 'login.html')


@login_required
def webinar(request):
    orgs=request.user
    update_webinar=Webinar.objects.filter(org_user=orgs)
    context = {'update_webinar': update_webinar}
    return render(request, 'webinar.html', context)

def view_webinar(request,update_id):
    task=Webinar.objects.get(id=update_id)
    form=WebinarForm(request.POST or None,instance=task)
    speakers = task.speakers.all()
    return render(request,'view_webinar.html',{'form':form,'speakers': speakers})

@login_required
def delete_webinar(request, del_id):
    webinar = Webinar.objects.get(id=del_id)
    organizer_email = webinar.org_user.email  
    subject = 'Webinar Deleted'
    message = f'The webinar "{webinar.title}" on {webinar.date} at {webinar.start_time} has been deleted.'
    from_email = 'mailtoshowvalidationok@gmail.com'  
    recipient_list = [organizer_email]
    # participants also 
    send_mail(subject, message, from_email, recipient_list)
    webinar.delete()

    return redirect('eventapp:webinar')


@login_required
def register_webinar(request):
    if request.method == 'POST':
        form = WebinarForm(request.POST)
        if form.is_valid():
            title=request.POST.get('title')
            date=request.POST.get('date')
            existing_webinar = Webinar.objects.filter(title=title, date=date)
            if existing_webinar:
                # If a webinar with the same name and date exists, show an error message
                messages.error(request, "A webinar with the same name and date already exists.")
            else:# Save the webinar without committing to the database yet
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
                message = f'Thank you for registering the webinar: {webinar.title} on {webinar.date} from {webinar.start_time} to {webinar.end_time}.'
                from_email = 'mailtoshowvalidationok@gmail.com'  # Replace with your email address
                recipient_list = [recipient_email]  # Use the organizer's email or another recipient

                send_mail(subject, message, from_email, recipient_list)

            
                # webinar_link = 'http://127.0.0.1:8000/'
                # matching_colleges = AICTE.objects.filter(departments='5')
                
                # for i in matching_colleges:
                #     college = EventOrganizer.objects.filter(aicte=i.aicte_id)
                #     for j in college:
                #         subject = f'Upcoming Webinar: {webinar.title}'
                #         message = f'Hello,\n\nThere is an upcoming webinar that you may be interested in: {webinar.title} on {webinar.date} at {webinar.time}.\n\nYou can find more details and register for the webinar here: {webinar_link}.\nRegister before:{webinar.deadline}\n\nPoster Link: {webinar.poster}'
                #         from_email = 'elizatom9@gmail.com'  # Replace with your email address
                #         recipient_list = [j.email]  # Use the college's email or another recipient

                # send_mail(subject, message, from_email, recipient_list)



                # interested_users = ['elizebaththomasv@gmail.com', 'elizatom9@gmail.com']  # Replace with actual email addresses
                # webinar_link = 'http://127.0.0.1:8000/'  # Replace with the actual webinar details page URL
                # email_subject = f'Upcoming Webinar: {webinar.title}'
                # email_message = f'Hello,\n\nThere is an upcoming webinar that you may be interested in: {webinar.title} on {webinar.date} at {webinar.time}.\n\nYou can find more details and register for the webinar here: {webinar_link}.\nRegister before:{webinar.deadline}\n\nPoster Link: {webinar.poster}'
                # from_email = 'elizatom9@gmail.com' 
                # send_mail(email_subject, email_message, from_email, interested_users)

                # Assuming this is the hosting department
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
    speakers = webinar.speakers.all()

    if request.method == 'POST':
        form = WebinarForm(request.POST, instance=webinar)
        if 'event_type' in request.POST and request.POST['event_type'] == 'Offline':
            form.fields['livestream'].initial = 'None'
        if form.is_valid():
            # Save the updated webinar
            new_date=request.POST.get('date')
            new_time=request.POST.get('start_time')
            if webinar.date != new_date or webinar.time != new_time:
                # Send an email notification
                subject = 'Webinar Date and Time Update'
                message = f'The date and time for the webinar "{webinar.title}" have been updated.\n\nNew Date: {new_date}\nNew Time: {new_time}'
                from_email = 'mailtoshowvalidationok@gmail.com'  # Replace with your email address
                recipient_email = ['elizebaththomasv@gmail.com']  # Replace with the recipient's email address

                # Send the email
                send_mail(subject, message, from_email, recipient_email)
            # max=request.POST.get('max_participants')
            web = form.save(commit=False)
            # web.max_participants=max
            web.org_user = request.user
            web.save()

            # Update speakers
            for speaker in speakers:
                designation_field = f"speakers-{speaker.id}-designation"
                name_field = f"speakers-{speaker.id}-speaker_name"
                speaker.designation = request.POST.get(designation_field)
                speaker.speaker_name = request.POST.get(name_field)
                speaker.save()

            messages.success(request, "Webinar updated successfully")

            # Redirect to the same page to refresh the form
            return redirect('update_webinar', update_id=update_id)
        else:
            messages.error(request, form.errors)
    else:
        form = WebinarForm(instance=webinar)  # Initialize form with webinar data

    return render(request, 'update_webinar.html', {'form': form, 'speakers': speakers, 'webinar': webinar})

def check_aicte_id(request):
    aicte_id = request.GET.get('aicte_id')
    
    try:
        aicte = AICTE.objects.get(aicte_id=aicte_id)
        return JsonResponse({'valid': True, 'name': aicte.name, 'location': aicte.location,'address': aicte.address})
    except AICTE.DoesNotExist:
        return JsonResponse({'valid': False, 'name': None, 'location': None,'address': None})

@login_required
def conference(request):
    # try:
    #     user_profile = EventOrganizer.objects.get(org_user=request.user)
    # except EventOrganizer.DoesNotExist:
    #     return redirect('eventapp:org_profile') 
    orgs=request.user
    con=Conference.objects.filter(org_user=orgs)
    context = {'con': con}
    return render(request, 'conference.html', context)

def view_conference(request,view_id):
    task=Conference.objects.get(id=view_id)
    form=ConferenceForm(request.POST or None,instance=task)
    speakers = task.speakers.all()
    return render(request,'view_conference.html',{'form':form,'speakers': speakers})

@login_required
def delete_conference(request, del_id):
    conference = Conference.objects.get(id=del_id)
    organizer_email = conference.org_user.email  
    subject = 'Conference Deleted'
    message = f'The conference "{ conference.title}" planned from { conference.start_date} to { conference.end_date} has been deleted.'
    from_email = 'mailtoshowvalidationok@gmail.com'  
    recipient_list = [organizer_email]

    send_mail(subject, message, from_email, recipient_list)
    conference.delete()

    return redirect('eventapp:conference')


# @login_required
# def register_conference(request):
#     if request.method == 'POST':
#         form = ConferenceForm(request.POST)
#         if form.is_valid():
#             conference = form.save(commit=False)
#             conference.org_user = request.user
#             speakers_designation = request.POST.getlist('speakers_designation[]')
#             speakers_name = request.POST.getlist('speakers_name[]')
#             for i in range(len(speakers_designation)):
#                 speaker = Speaker.objects.create(
#                     designation=speakers_designation[i],
#                     speaker_name=speakers_name[i]
#                 )
#                 conference.speakers.add(speaker)  
#             recipient_email = request.user.email
#             subject = 'Conference Registration Confirmation'
#             message = f'Thank you for registering the conference: {conference.title} from {conference.start_date} at {conference.end_date}.'
#             from_email = 'mailtoshowvalidationok@gmail.com'  # Replace with your email address
#             recipient_list = [recipient_email]  # Use the organizer's email or another recipient

#             send_mail(subject, message, from_email, recipient_list)

#             interested_users = ['elizebaththomasv@gmail.com', 'elizatom9@gmail.com']  # Replace with actual email addresses
#             conference_link = 'http://127.0.0.1:8000/'  # Replace with the actual webinar details page URL
#             email_subject = f'Upcoming Conference: {conference.title}'
#             email_message = f'Hello,\n\nThere is an upcoming conference that you may be interested in: {conference.title} from {conference.start_date} at {conference.end_time}.\n\nYou can find more details and register for the  conference here: {conference_link}.\n\nPoster Link: {conference.poster}'
#             from_email = 'mailtoshowvalidationok@gmail.com' 
#             send_mail(email_subject, email_message, from_email, interested_users)
#             messages.success(request, "Conference saved successfully")
#             return redirect('eventapp:register_conference')
#         else:
#             print(form.errors)
#             messages.error(request, form.errors)
#     else:
#         form = ConferenceForm()
#     return render(request, 'register_conference.html', {'form': form})
@login_required
def register_conference(request):
    if request.method == 'POST':
        form = ConferenceForm(request.POST)
        if form.is_valid():
            conference = form.save(commit=False)
            conference.org_user = request.user
            # Save the conference object to the database first
            conference.save()
            
            speakers_designation = request.POST.getlist('speakers_designation[]')
            speakers_name = request.POST.getlist('speakers_name[]')
            for i in range(len(speakers_designation)):
                speaker = Speaker.objects.create(
                    designation=speakers_designation[i],
                    speaker_name=speakers_name[i]
                )
                # Now that the conference is saved, you can add speakers to it
                conference.speakers.add(speaker)

            recipient_email = request.user.email
            subject = 'Conference Registration Confirmation'
            message = f'Thank you for registering the conference: {conference.title} from {conference.start_date} to {conference.end_date}.'
            from_email = 'mailtoshowvalidationok@gmail.com'  # Replace with your email address
            recipient_list = [recipient_email]  # Use the organizer's email or another recipient

            send_mail(subject, message, from_email, recipient_list)

            interested_users = ['elizebaththomasv@gmail.com', 'elizatom9@gmail.com']  # Replace with actual email addresses
            conference_link = 'http://127.0.0.1:8000/'  # Replace with the actual webinar details page URL
            email_subject = f'Upcoming Conference: {conference.title}'
            email_message = f'Hello,\n\nThere is an upcoming conference that you may be interested in: {conference.title} from {conference.start_date} to {conference.end_date}.\n\nYou can find more details and register for the  conference here: {conference_link}.\nRegistration closes by: {conference.deadline}.\n\nPoster Link: {conference.poster}'
            from_email = 'mailtoshowvalidationok@gmail.com' 
            send_mail(email_subject, email_message, from_email, interested_users)

            messages.success(request, "Conference saved successfully")
            return redirect('eventapp:register_conference')
        else:
            print(form.errors)
            messages.error(request, form.errors)
    else:
        form = ConferenceForm()
    return render(request, 'register_conference.html', {'form': form})


def update_conference(request, update_id):
    conference = Conference.objects.get(id=update_id)
    if request.method == 'POST':
        form = ConferenceForm(request.POST, instance=conference)
        if form.is_valid():
            form.save()

            # Update speakers
            for speaker in conference.speakers.all():
                designation_field = f"speakers-{speaker.id}-designation"
                name_field = f"speakers-{speaker.id}-speaker_name"
                speaker.designation = request.POST.get(designation_field)
                speaker.speaker_name = request.POST.get(name_field)
                speaker.save()

            messages.success(request, "Conference and speakers updated successfully")
            return redirect('eventapp:update_conference', update_id=update_id)
        else:
            messages.error(request, form.errors)
    else:
        form = ConferenceForm(instance=conference)

    speakers = conference.speakers.all()
    return render(request, 'update_conference.html', {'form': form, 'speakers': speakers})

def listwebinars(request):
    # Filter webinars whose date is greater than today
    today = timezone.now().date()
    allwebinars = Webinar.objects.filter(deadline__gt=today)
    context = {'allwebinars': allwebinars}
    return render(request, 'listwebinars.html', context)



def events(request):
    webinars=Webinar.objects.all().order_by('-date')[:8]
    return render(request, 'events.html', {'webinars': webinars})

def register_for_webinar(request, webinar_id):
    user = request.user
    webinar = Webinar.objects.get(pk=webinar_id)
    registration_count = WebinarRegistration.objects.filter(webinar=webinar).count()
    if registration_count < webinar.max_participants:
        if not WebinarRegistration.objects.filter(user=user, webinar=webinar).exists():
            WebinarRegistration.objects.create(user=user, webinar=webinar)
            messages.success(request, "Webinar registered successfully")
            recipient_email = request.user.email
            subject = 'Webinar Registration Confirmation'
            message = f'Thank you for registering the webinar: {webinar.title} on {webinar.date} '
            from_email = 'mailtoshowvalidationok@gmail.com'  
            recipient_list = [recipient_email]  

            send_mail(subject, message, from_email, recipient_list)
            return redirect('eventapp:events') 
        else:
            messages.success(request, "You are already registered for this webinar.")
            return redirect('eventapp:events')
    else:
        messages.error(request, "Webinar reached maximum number of participants")
        return redirect('eventapp:events')
@login_required
def registered_webinar(request):
    user = request.user
    webinar_registrations = WebinarRegistration.objects.filter(user=user)
    context = {'webinar': webinar_registrations}
    return render(request, 'registered_webinar.html', context)
