import datetime
from django.contrib import messages
from django.shortcuts import render, redirect,get_object_or_404
#from .models import User
from .models import Service,CustomUser,Webinar,EventOrganizer,AICTE,Speaker,Conference,WebinarRegistration,Attendee,Package
import re
from django.conf import settings
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User,auth
from .forms import WebinarForm, Organizer,ConferenceForm,AttendeeForm
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
import uuid

 
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
            'eventoplanneur@gmail.com',
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
            'eventoplanneur@gmail.com',
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
        return redirect('eventapp:login')  # Redirect to login page after successful verification
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
            'eventoplanneur@gmail.com',
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
            'eventoplanneur@gmail.com',
            [email],
            fail_silently=False,
        )

        return redirect('eventapp:verify')
    return render(request, 'reg_provider.html')

def index(request):
    return render(request, 'index.html')

def orghome(request):
    return render(request, 'orghome.html')

def admindash(request):
    return render(request, 'admindash.html')

def attendeehome(request):
    return render(request, 'attendeehome.html')

@login_required
def providerhome(request):
    orgs=request.user
    service=Service.objects.filter(org_user=orgs)
    context = {'service': service}
    return render(request, 'providerhome.html', context)

def gallery(request):
    return render(request, 'gallery.html')

def services(request):
    if request.method == 'GET':
        service_input = request.GET.get('serviceInput', '').strip()
        city_input = request.GET.get('cityInput', '').strip()
        search = Service.objects.filter(category__iexact=service_input, locations__contains=city_input)
        view_search = {'search': search}
        services = Service.objects.all()[:6]
        view_service = {'services': services}
        return render(request, 'services.html', {**view_search, **view_service})

    # If the form is not submitted, show all services
    services = Service.objects.all()[:6]
    view_service = {'services': services}
    return render(request, 'services.html', view_service)



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
                if user.is_provider:
                    return redirect('eventapp:providerhome')
                if user.email=="admin@gmail.com":
                    return redirect('eventapp:admindash')
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
    update_webinar=Webinar.objects.filter(org_user=orgs, status=1)
    now = datetime.datetime.now()
    context = {'update_webinar': update_webinar,'today':now}
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
    from_email = 'eventoplanneur@gmail.com'  
    recipient_list = [organizer_email]
    # participants also 
    send_mail(subject, message, from_email, recipient_list)
    webinar.status=0
    webinar.save()

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
                from_email = 'eventoplanneur@gmail.com'  # Replace with your email address
                recipient_list = [recipient_email]  # Use the organizer's email or another recipient
                send_mail(subject, message, from_email, recipient_list)

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
            return redirect('eventapp:orghome')
       
    else:
        form = Organizer(instance=organizer_instance)
    messages.error(request, form.errors)
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
                from_email = 'eventoplanneur@gmail.com'  # Replace with your email address
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
    from_email = 'eventoplanneur@gmail.com'  
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
            from_email = 'eventoplanneur@gmail.com'  # Replace with your email address
            recipient_list = [recipient_email]  # Use the organizer's email or another recipient

            send_mail(subject, message, from_email, recipient_list)

            interested_users = ['elizebaththomasv@gmail.com', 'elizatom9@gmail.com']  # Replace with actual email addresses
            conference_link = 'http://127.0.0.1:8000/'  # Replace with the actual webinar details page URL
            email_subject = f'Upcoming Conference: {conference.title}'
            email_message = f'Hello,\n\nThere is an upcoming conference that you may be interested in: {conference.title} from {conference.start_date} to {conference.end_date}.\n\nYou can find more details and register for the  conference here: {conference_link}.\nRegistration closes by: {conference.deadline}.\n\nPoster Link: {conference.poster}'
            from_email = 'eventoplanneur@gmail.com' 
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
    allwebinars = Webinar.objects.filter(deadline__gt=today, status=1)
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
            from_email = 'eventoplanneur@gmail.com'  
            recipient_list = [recipient_email]  

            send_mail(subject, message, from_email, recipient_list)
            pay_id=webinar_id
            return redirect('payment', pay_id=pay_id) 
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

from django.shortcuts import render
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
 
 
# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
 
def payment(request,pay_id):
    webinar = Webinar.objects.get(pk=pay_id)
    currency = 'INR'
    amount = int(webinar.fee)*100 # Rs. 200
 
    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture='0'))
 
    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = 'eventapp:paymenthandler'
 
    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url
 
    return render(request, 'payment.html', context=context)

@csrf_exempt
def paymenthandler(request):
 
    # only accept POST request.
    if request.method == "POST":
        try:
           
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
 
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result is not None:
                amount = 20000  # Rs. 200
                try:
 
                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)
 
                    # render success page on successful caputre of payment
                    return render(request, 'paymentsuccess.html')
                except:
 
                    # if there is an error while capturing payment.
                    return render(request, 'paymentfail.html')
            else:
 
                # if signature verification fails.
                return render(request, 'paymentfail.html')
        except:
 
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()
    
def paymentsuccess(request):
    return render(request, 'paymentsuccess.html')

def paymentfail(request):
    return render(request, 'paymentfail.html')

@login_required
def attendee_profile(request):
    org_user = request.user

    try:
        organizer_instance = Attendee.objects.get(org_user=org_user)
    except Attendee.DoesNotExist:
        organizer_instance = None

    if request.method == "POST":
        if organizer_instance:
            form = AttendeeForm(request.POST, instance=organizer_instance)
        else:
            form = AttendeeForm(request.POST)

        if form.is_valid():
            attendee = form.save(commit=False)
            interests = request.POST.get('interests', '')  # Get the interests as a comma-separated string
            attendee.interests = interests
            attendee.org_user = org_user
            attendee.save()
            return redirect('eventapp:attendeehome')

    else:
        initial_data = {}  # Create a dictionary to store initial data for the form
        if organizer_instance and organizer_instance.interests:
            # Split the comma-separated interests string into a list
            initial_data['interests'] = organizer_instance.interests.split(', ')
        form = AttendeeForm(instance=organizer_instance, initial=initial_data)

    return render(request, 'attendee_profile.html', {'form': form})

from django.shortcuts import render
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .models import Webinar, Attendee

def recommendations(request, N=6):
    try:
        attendee_id=request.user.id
        # Get the attendee's interests from the Attendee model
        attendee = Attendee.objects.get(org_user=attendee_id)
        attendee_interests = attendee.interests
        
        # Get all event descriptions and Webinar objects from the Webinar model
        current_date = timezone.now()
        all_events = Webinar.objects.filter(date__gt=current_date)
        
        # Create a dictionary to map event descriptions to Webinar objects
        event_description_to_webinar = {event.description: event for event in all_events}

        # Preprocess the text data (clean and tokenize)
        # You can use NLTK, spaCy, or other libraries for text preprocessing

        # Create TF-IDF vectors for event descriptions and attendee interests
        tfidf_vectorizer = TfidfVectorizer()
        tfidf_matrix_events = tfidf_vectorizer.fit_transform(all_events.values_list('description', flat=True))
        tfidf_matrix_attendee = tfidf_vectorizer.transform([attendee_interests])

        # Calculate cosine similarity between attendee interests and event descriptions
        # Convert tfidf_matrix_attendee to a dense array before calculating similarity
        similarity_scores = cosine_similarity(tfidf_matrix_attendee.toarray(), tfidf_matrix_events)
        
        # Get the indices of events sorted by similarity score
        sorted_event_indices = similarity_scores.argsort()[0][::-1]
        
        sorted_event_indices = sorted_event_indices.tolist()
                
        top_N_events = [event_description_to_webinar[all_events[i].description] for i in sorted_event_indices[:N]]
        return render(request, 'recommendations.html', {'recommended_events': top_N_events})
        

    except Attendee.DoesNotExist:
        # Handle the case where the attendee doesn't exist
        return render(request, 'recommendations.html', {'recommended_events': []})
    
from django.shortcuts import render, redirect
from .forms import ServiceForm

def addservices(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        
        if form.is_valid():
            # Save the service first before working with many-to-many relationships
            service = form.save(commit=False)
            # Set the organizer to the currently logged-in user
            service.org_user = request.user
            service.save()  # Commit the service to the database
            
            # Send confirmation email
            recipient_email = request.user.email
            subject = 'Service Registration Confirmation'
            message = f'Thank you for registering the service: {service.name} that provides {service.category} services.'
            from_email = 'eventoplanneur@gmail.com'
            recipient_list = [recipient_email]
            send_mail(subject, message, from_email, recipient_list)
            
            messages.success(request, "Service saved successfully")
            return redirect('eventapp:addservices')
        else:
            messages.error(request, form.errors)
    else:
        form = ServiceForm()

    return render(request, 'addservices.html', {'form': form})

def viewservices(request, service_id):
    task = get_object_or_404(Service, id=service_id)

    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=task)
        if form.is_valid():
            # Process the form data if it's valid
            form.save()
            # Redirect or render a success page
    else:
        # If it's a GET request, just display the form with the existing data
        form = ServiceForm(instance=task)
    return render(request, 'viewservices.html', {'form': form,'service_id': service_id})

def availability(request, service_id):

    return render(request, 'availability.html')


from .models import Service, BookService
from .forms import ServiceForm, BookServiceForm

def book_services(request, service_id):
    service_task = get_object_or_404(Service, id=service_id)
    service_form = ServiceForm(instance=service_task)
    location_values = service_task.locations.split(',')
    services_required = service_task.services_provided.split(',')

    book_service_form = BookServiceForm(request.POST or None)

    if request.method == 'POST':
        if book_service_form.is_valid():
            # Create a new BookService instance
            book_service = book_service_form.save(commit=False)
            
            # Associate it with the Service instance
            book_service.service = service_task
            book_service.org_user = request.user
            # Save the BookService instance
            book_service.save()
            
            messages.success(request, "Service booked successfully")
            # Redirect or render a success page
        else:
            # Handle the case where the form is not valid
            messages.error(request, book_service_form.errors)

    return render(request, 'book_services.html', {
        'service_form': service_form,
        'book_service_form': book_service_form,
        'location_values': location_values,
        'services_required': services_required,
        'service_id': service_id
    })

def view_bookings(request):
    current_user = request.user
    
    # Filter BookService instances where the org_user of the associated service is the current user
    booked_services = BookService.objects.filter(service__org_user=current_user)

    # Get a list of unique org_users from booked_services
    unique_org_users = booked_services.values_list('org_user', flat=True).distinct()

    # Filter EventOrganizer objects for the unique org_users
    organizer = EventOrganizer.objects.filter(org_user__in=unique_org_users)

    return render(request, 'view_bookings.html', {'booked_services': booked_services, 'organizer': organizer})


from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import BookService  # Import your BookService model here

def bookings(request):
    current_user = request.user
    booking_instances = BookService.objects.filter(org_user=current_user)
    return render(request, 'bookings.html', {'booking_instances': booking_instances})


from .models import BookService, Review

def review_service(request):
    current_user = request.user
    booking_instances = BookService.objects.filter(org_user=current_user, status='completed')

    return render(request, 'review_service.html', {'booking_instances': booking_instances})

def submit_review(request):
    if request.method == 'POST':
        service_id = request.POST.get('service')
        rating = request.POST.get('rating')
        comments = request.POST.get('comments')

        # Assuming you have a Review model with a foreign key to the Service model
        service = Service.objects.get(id=service_id)
        review = Review.objects.create(service=service, rating=rating, comments=comments)

        return redirect('review_service')
    else:
        # Handle other HTTP methods if needed
        return redirect('review_service')

def approve_booking(request, booking_id):
    booking_instance = get_object_or_404(BookService, pk=booking_id)
    booking_instance.status = "approved"
    booking_instance.save()
    return redirect('eventapp:view_bookings')
def reject_booking(request, booking_id):
    booking_instance = get_object_or_404(BookService, pk=booking_id)
    booking_instance.status = "rejected"
    booking_instance.save()
    return redirect('eventapp:view_bookings')

from django.http import JsonResponse

def check_availability(request):
    if request.method == 'POST':
        service_id = request.POST.get('service_id')
        date = request.POST.get('date')
        location = request.POST.get('location')

        # Check if there is any service booked on the selected date for the given location
        is_available = not BookService.objects.filter(service_id=service_id, date=date, location=location).exists()
        
        return JsonResponse({'available': is_available})

def bookings(request):
    currency = 'INR'
    amount = 200000  # Rs. 200
 
    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture='0'))
 
    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = 'eventapp:bookings'
    current_user = request.user
    booking_instances = BookService.objects.filter(org_user=current_user)

    # Create a context dictionary for booking instances
    context = {
        'booking_instances': booking_instances,
    }
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url
 
    return render(request, 'bookings.html', context=context)
 
 
# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
@csrf_exempt
def service_paymenthandler(request):
 
    # only accept POST request.
    if request.method == "POST":
        try:
           
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
 
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result is not None:
                amount = 200000  # Rs. 200
                try:
 
                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)
 
                    # render success page on successful caputre of payment
                    return render(request, 'service_paymentsuccess.html')
                except:
 
                    # if there is an error while capturing payment.
                    return render(request, 'service_paymentfail.html')
            else:
 
                # if signature verification fails.
                return render(request, 'service_paymentfail.html')
        except:
 
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()
def service_paymentsuccess(request):
    return render(request, 'service_paymentsuccess.html')

def service_paymentfail(request):
    return render(request, 'service_paymentfail.html')

# def services_required(request, webinar_id):
#     service_options = ['catering', 'venue', 'transportation', 'sound and lighting', 'entertainment', 'decoration', 'accommodation', 'event staffing', 'promotion', 'photography and videography']

#     # Fetch the webinar information from the database
#     webinar = get_object_or_404(Webinar, id=webinar_id)

#     if request.method == 'POST':
#         selected_services = request.POST.getlist('service_categories[]')
#         # Process the selected services

#     return render(request, 'services_required.html', {
#         'service_options': service_options,
#         'webinar_location': webinar.location,
#         'webinar_date': webinar.date,
#     })

def services_required(request, webinar_id):
    # Assuming you also want to fetch webinar information
    webinar = get_object_or_404(Webinar, id=webinar_id)
    service_options = ['catering', 'venue', 'transportation', 'sound and lighting', 'entertainment', 'decoration', 'accomodation', 'event staffing', 'promotion', 'photography and videography']

    # Fetch all packages for the current user (adjust the filter condition based on your needs)
    packages = Package.objects.all()

    if request.method == 'POST':
        selected_services = request.POST.getlist('service_categories[]')
        # Process the selected services

    return render(request, 'services_required.html', {
        'webinar_location': webinar.location.lower(),
        'service_options': service_options,
        'webinar_date': webinar.date,
        'participants': webinar.max_participants,
        'packages': packages,
    })