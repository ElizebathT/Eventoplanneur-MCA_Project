from django.contrib import messages
from django.shortcuts import render, redirect,get_object_or_404
from numpy import mean
from .models import Service,CustomUser,Webinar,EventOrganizer,AICTE,Speaker,Conference,WebinarRegistration,Attendee,Package,ServiceProvider,ParticipationCertificate
import re
from django.conf import settings
from django.contrib.auth import authenticate, login as auth_login
from .forms import WebinarForm, Organizer,ConferenceForm,AttendeeForm,Provider
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.http import HttpResponse
from django.core.mail import send_mail
from django.utils import timezone
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
        return redirect('eventapp:login')   
    else:
        return render(request, 'invalid_token.html')  
    
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
    return render(request, 'reg_provider.html')

def index(request):
    return render(request, 'index.html')

def orghome(request):
    notifications = Notification.objects.filter(is_read=False).order_by('-timestamp')[:5]
    return render(request, 'orghome.html',{'notifications':notifications})

def admindash(request):
    return render(request, 'admindash.html')

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

from django.db.models import Q
@login_required
def webinar(request):
    org_user = request.user
    search_query = request.GET.get('search', '')
    current_date = timezone.now().date()
    if search_query:
        update_webinar = Webinar.objects.filter(
            Q(org_user=org_user, status=1),
            Q(title__icontains=search_query),Q(date__gte=current_date) 
        ).order_by('date')
    else:
        update_webinar = Webinar.objects.filter(org_user=org_user, status=1,date__gte=current_date).order_by('date')
    context = {'update_webinar': update_webinar, 'search_query': search_query}
    return render(request, 'webinar.html', context)

from django.db.models import Q
@login_required
def completed_webinar(request):
    org_user = request.user
    search_query = request.GET.get('search', '')
    current_date = timezone.now().date()
    if search_query:
        update_webinar = Webinar.objects.filter(
            Q(org_user=org_user, status=1),
            Q(title__icontains=search_query),Q(date__lt=current_date) 
        ).order_by('date')
    else:
        update_webinar = Webinar.objects.filter(org_user=org_user, status=1,date__lt=current_date).order_by('date')
    context = {'update_webinar': update_webinar, 'search_query': search_query}
    return render(request, 'completed_webinar.html', context)

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
                messages.error(request, "A webinar with the same name and date already exists.")
            else:
                webinar = form.save(commit=False)
                webinar.org_user = request.user
                webinar.save()  
                speakers_designation = request.POST.getlist('speakers_designation[]')
                speakers_name = request.POST.getlist('speakers_name[]')
                for i in range(len(speakers_designation)):
                    speaker = Speaker.objects.create(
                        designation=speakers_designation[i],
                        speaker_name=speakers_name[i]
                    )
                    webinar.speakers.add(speaker) 
                recipient_email = request.user.email
                subject = 'Webinar Registration Confirmation'
                message = f'Thank you for registering the webinar: {webinar.title} on {webinar.date} from {webinar.start_time} to {webinar.end_time}.'
                from_email = 'eventoplanneur@gmail.com'  
                recipient_list = [recipient_email]
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
                subject = 'Webinar Date and Time Update'
                message = f'The date and time for the webinar "{webinar.title}" have been updated.\n\nNew Date: {new_date}\nNew Time: {new_time}'
                from_email = 'eventoplanneur@gmail.com'  
                recipient_email = ['elizebaththomasv@gmail.com']  
                send_mail(subject, message, from_email, recipient_email)
            web = form.save(commit=False)
            web.org_user = request.user
            web.save()
            for speaker in speakers:
                designation_field = f"speakers-{speaker.id}-designation"
                name_field = f"speakers-{speaker.id}-speaker_name"
                speaker.designation = request.POST.get(designation_field)
                speaker.speaker_name = request.POST.get(name_field)
                speaker.save()
            messages.success(request, "Webinar updated successfully")
            return redirect('update_webinar', update_id=update_id)
        else:
            messages.error(request, form.errors)
    else:
        form = WebinarForm(instance=webinar)  
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

@login_required
def register_conference(request):
    if request.method == 'POST':
        form = ConferenceForm(request.POST)
        if form.is_valid():
            conference = form.save(commit=False)
            conference.org_user = request.user
            conference.save()            
            speakers_designation = request.POST.getlist('speakers_designation[]')
            speakers_name = request.POST.getlist('speakers_name[]')
            for i in range(len(speakers_designation)):
                speaker = Speaker.objects.create(
                    designation=speakers_designation[i],
                    speaker_name=speakers_name[i]
                )
                conference.speakers.add(speaker)
            recipient_email = request.user.email
            subject = 'Conference Registration Confirmation'
            message = f'Thank you for registering the conference: {conference.title} from {conference.start_date} to {conference.end_date}.'
            from_email = 'eventoplanneur@gmail.com'  
            recipient_list = [recipient_email]  
            send_mail(subject, message, from_email, recipient_list)
            interested_users = ['elizebaththomasv@gmail.com', 'elizatom9@gmail.com'] 
            conference_link = 'http://127.0.0.1:8000/'  
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
    today = timezone.now().date()
    allwebinars = Webinar.objects.filter(deadline__gt=today, status=1)
    context = {'allwebinars': allwebinars}
    return render(request, 'listwebinars.html', context)

def events(request):
    query = request.GET.get('search')
    if query:
        webinars = Webinar.objects.filter(Q(title__icontains=query) | Q(description__icontains=query)).order_by('-date')[:8]
    else:
        webinars = Webinar.objects.all().order_by('-date')[:9]
    return render(request, 'events.html', {'webinars': webinars})

from twilio.rest import Client
def register_for_webinar(request, webinar_id):
    attendee = request.user
    webinar = Webinar.objects.get(pk=webinar_id)
    user = Attendee.objects.get(email=attendee.email)
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
            message_body = f"Webinar Registration Confirmed for {webinar.title} on {webinar.date} hosted by {webinar.organizer_name}."
            client = Client("AC5649992a1008a1d4e8455e183b97072d", "11aac5884cccdfd8869d78de65606fb5")
            message = client.messages.create(
                from_='whatsapp:+14155238886',
                body=message_body,
                to='whatsapp:+919061849932'  
            )
            return redirect('payment', pay_id=pay_id) 
        else:
            messages.success(request, "You are already registered for this webinar.")
            return redirect('eventapp:events')
    else:
        messages.error(request, "Webinar reached maximum number of participants")
        return redirect('eventapp:events')

from django.utils import timezone
@login_required
def registered_webinar(request):
    attendee = request.user
    current_date = timezone.now().date()
    user = Attendee.objects.get(email=attendee.email)
    upcoming_webinars = WebinarRegistration.objects.filter(user=user, webinar__date__gte=current_date)    
    context = {
        'upcoming_webinars': upcoming_webinars
    }
    return render(request, 'registered_webinar.html', context)

@login_required
def past_webinars(request):
    attendee = request.user
    current_date = timezone.now().date()
    user = Attendee.objects.get(email=attendee.email)
    upcoming_webinars = WebinarRegistration.objects.filter(user=user, webinar__date__lt=current_date)    
    context = {
        'upcoming_webinars': upcoming_webinars
    }
    return render(request, 'past_webinars.html', context)

from django.shortcuts import render
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
 
def payment(request,pay_id):
    webinar = Webinar.objects.get(pk=pay_id)
    currency = 'INR'
    amount = int(webinar.fee)*100 
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture='0'))
    razorpay_order_id = razorpay_order['id']
    callback_url = 'eventapp:paymenthandler'
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url
 
    return render(request, 'payment.html', context=context)

@csrf_exempt
def paymenthandler(request):
    if request.method == "POST":
        try:
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }            
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result is not None:
                amount = 20000 
                try:
                    razorpay_client.payment.capture(payment_id, amount)
                    return render(request, 'paymentsuccess.html')
                except:
                    return render(request, 'paymentfail.html')
            else:
                return render(request, 'paymentfail.html')
        except:
            return HttpResponseBadRequest()
    else:
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
            interests = request.POST.get('interests', '') 
            attendee.interests = interests
            attendee.org_user = org_user
            attendee.save()
            return redirect('eventapp:attendeehome')
    else:
        initial_data = {}  
        if organizer_instance and organizer_instance.interests:
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
        attendee = Attendee.objects.get(org_user=attendee_id)
        attendee_interests = attendee.interests
        current_date = timezone.now()
        all_events = Webinar.objects.filter(date__gt=current_date)
        event_description_to_webinar = {event.description: event for event in all_events}
        tfidf_vectorizer = TfidfVectorizer()
        tfidf_matrix_events = tfidf_vectorizer.fit_transform(all_events.values_list('description', flat=True))
        tfidf_matrix_attendee = tfidf_vectorizer.transform([attendee_interests])
        similarity_scores = cosine_similarity(tfidf_matrix_attendee.toarray(), tfidf_matrix_events)
        sorted_event_indices = similarity_scores.argsort()[0][::-1]        
        sorted_event_indices = sorted_event_indices.tolist()                
        top_N_events = [event_description_to_webinar[all_events[i].description] for i in sorted_event_indices[:N]]
        return render(request, 'recommendations.html', {'recommended_events': top_N_events})        

    except Attendee.DoesNotExist:
        return render(request, 'recommendations.html', {'recommended_events': []})
    
def attendeehome(request):
        return render(request, 'attendeehome.html')
    
from django.shortcuts import render, redirect
from .forms import ServiceForm

def addservices(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)        
        if form.is_valid():
            service = form.save(commit=False)
            service.org_user = request.user
            service.save() 
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
    service = get_object_or_404(Service, id=service_id)
    reviews = Review.objects.filter(service__id=service_id)
    average_rating = mean([review.rating for review in reviews]) if reviews else None
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
    else:
        form = ServiceForm(instance=service)
    return render(request, 'viewservices.html', {
        'form': form,
        'service': service,
        'reviews': reviews,
        'average_rating': average_rating,
        'service_id':service_id
    })

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
            book_service = book_service_form.save(commit=False)
            book_service.service = service_task
            book_service.org_user = request.user
            book_service.save()            
            messages.success(request, "Service booked successfully")
        else:
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
    booked_services = BookService.objects.filter(service__org_user=current_user)
    unique_org_users = booked_services.values_list('org_user', flat=True).distinct()
    organizer = EventOrganizer.objects.filter(org_user__in=unique_org_users)
    return render(request, 'view_bookings.html', {'booked_services': booked_services, 'organizer': organizer})

from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import BookService  

def bookings(request):
    current_user = request.user
    booking_instances = BookService.objects.filter(org_user=current_user)
    return render(request, 'bookings.html', {'booking_instances': booking_instances})

def approve_booking(request, booking_id):
    booking_instance = get_object_or_404(BookService, pk=booking_id)
    booking_instance.status = "approved"
    booking_instance.save()
    return redirect('eventapp:view_bookings')

def service_complete(request, booking_id):
    booking_instance = get_object_or_404(BookService, pk=booking_id)
    booking_instance.status = "service completed"
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
        is_available = not BookService.objects.filter(service_id=service_id, date=date, location=location).exists()        
        return JsonResponse({'available': is_available})

def bookings(request):
    currency = 'INR'
    amount = 200000  
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture='0'))
    razorpay_order_id = razorpay_order['id']
    callback_url = 'eventapp:bookings'
    current_user = request.user
    booking_instances = BookService.objects.filter(org_user=current_user)
    context = {
        'booking_instances': booking_instances,
        
    }
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url
 
    return render(request, 'bookings.html', context=context)
 
def pay_advance(request, booking_id):
    booking_instance = BookService.objects.get(id=booking_id)
    if booking_instance and booking_instance.status == 'pending':
        booking_instance.status = 'advance_paid'
        booking_instance.save()
        messages.success(request, 'Advance payment successful.')
    return redirect('eventapp:bookings')

@csrf_exempt
def service_paymenthandler(request):
    if request.method == "POST":
        try:
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result is not None:
                amount = 200000 
                try:
                    razorpay_client.payment.capture(payment_id, amount)
                    return render(request, 'service_paymentsuccess.html')
                except:
                    return render(request, 'service_paymentfail.html')
            else:
                return render(request, 'service_paymentfail.html')
        except:
            return HttpResponseBadRequest()
    else:
        return HttpResponseBadRequest()
    
def service_paymentsuccess(request):
    return render(request, 'service_paymentsuccess.html')

def service_paymentfail(request):
    return render(request, 'service_paymentfail.html')

def services_required(request, webinar_id):
    webinar = get_object_or_404(Webinar, id=webinar_id)
    service_options = ['catering', 'venue', 'transportation', 'sound and lighting', 'entertainment', 'decoration', 'accomodation', 'event staffing', 'promotion', 'photography and videography']
    packages = Package.objects.all()
    if request.method == 'POST':
        selected_services = request.POST.getlist('service_categories[]')
    webinar_location=None
    if webinar.location:
        webinar_location=webinar.location.lower()
    return render(request, 'services_required.html', {
        'webinar_location': webinar_location,
        'service_options': service_options,
        'webinar_date': webinar.date,
        'participants': webinar.max_participants,
        'packages': packages,
    })

from .models import Review
from .forms import ReviewForm
@login_required
def review_service(request):
    review_submitted = False
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            service_id = request.POST.get('service_id')
            
            service = Service.objects.get(id=service_id)
            review = form.save(commit=False)
            review.user = request.user
            review.service = service
            review.save()
            review_submitted = True
    else:
        form = ReviewForm()
    completed_services = BookService.objects.filter(org_user=request.user, status='service completed')
    service_id = request.GET.get('q')
    services = Service.objects.all()
    reviews = Review.objects.all()
    query = request.GET.get('q')    
    if query:
        reviews = reviews.filter(service=query)    
    context = {'form': form, 'completed_services': completed_services, 'review_submitted': review_submitted,'reviews': reviews, 'services': services, 'query': query}
    return render(request, 'review_service.html', context)

def display_registrations(request, webinar_id):
    webinar = Webinar.objects.get(pk=webinar_id)
    registrations = webinar.get_registrations()
    return render(request, 'registration_list.html', {'webinar': webinar, 'registrations': registrations})

def edit_services(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            form.save()
            return redirect('eventapp:edit_services', service_id=service.id)
    else:
        form = ServiceForm(instance=service)
    return render(request, 'edit_services.html', {'form': form, 'service': service})

def user_services(request):
    user_services = Service.objects.filter(org_user=request.user)  
    return render(request, 'user_services.html', {'user_services': user_services})

@login_required
def provider_profile(request):
    service_user = request.user
    try:
        organizer_instance = ServiceProvider.objects.get(service_user=service_user)
    except ServiceProvider.DoesNotExist:
        organizer_instance = None
    if request.method == "POST":
        if organizer_instance:
            form = Provider(request.POST, instance=organizer_instance)
        else:
            form = Provider(request.POST)
        if form.is_valid():
            event_organizer = form.save(commit=False)
            event_organizer.service_user = service_user
            event_organizer.save()
            return redirect('eventapp:providerhome')
    else:
        form = Provider(instance=organizer_instance)
    messages.error(request, form.errors)
    return render(request, 'provider_profile.html', {'form': form})

from .models import Notification
from django.db.models import F

def generate_certificate(request, webinar_id):
    webinar = get_object_or_404(Webinar, pk=webinar_id)
    current_user = request.user
    attendee = Attendee.objects.get(org_user=current_user)
    certificate = ParticipationCertificate.objects.create(
        attendee_name=attendee.name,
        webinar_title=webinar.title,
        organization=webinar.organizer_name,
        date=webinar.date
    )
    return redirect('certificate_download', certificate_id=certificate.id)

from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas


def certificate_download(request, certificate_id):
    certificate = get_object_or_404(ParticipationCertificate, id=certificate_id)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="certificate.pdf"'
    template_image_path = 'D:\Project\Eventoplanneur\event\static\images\certificate.png'
    template_image = Image.open(template_image_path)
    width, height = template_image.size
    doc = SimpleDocTemplate(response, pagesize=(width, height))
    c = canvas.Canvas(response, pagesize=(width, height))
    c.drawImage(template_image_path, 0, 0, width, height)
    custom_body_style = ParagraphStyle(
    name='CustomBodyText',
    fontName='Helvetica',
    fontSize=40
    )
    custom_body_style_large = ParagraphStyle(
        name='CustomBodyTextLarge',
        fontName='Helvetica',
        fontSize=80
    )
    custom_body_style_small = ParagraphStyle(
        name='CustomBodyTextSmall',
        fontName='Helvetica',
        fontSize=20
    )
    elements = [
        Paragraph(f"{certificate.attendee_name}", custom_body_style_large),
        Paragraph(f"{certificate.webinar_title}", custom_body_style),
        Paragraph(f"{certificate.organization}", custom_body_style),
        Paragraph(f"{certificate.date}", custom_body_style),
        Paragraph(f"{certificate.certificate_issued_date}", custom_body_style_small),
    ]    
    positions = [
        (650, height - 600), 
        (700, height - 840),  
        (550, height - 965), 
        (1550, height - 840),
        (1000, height - 1200), 
    ]
    for i, element in enumerate(elements):
        x, y = positions[i]
        element.wrapOn(c, width, height)
        element.drawOn(c, x, y)
    c.save()
    return response

from django.shortcuts import render, redirect
from .models import Response, Question

def questionnaire(request, webinar_id):
    existing_questions = Question.objects.filter(webinar_id=webinar_id)            
    if request.method == 'POST':
        questions_text = request.POST.getlist('questions[]') 
        for question_text in questions_text:
            if question_text:
                question = Question.objects.create(
                    question=question_text,
                    webinar_id=webinar_id
                )
                question.save()
        return redirect('eventapp:webinar') 
    return render(request, 'questionnaire.html', {'existing_questions': existing_questions, 'webinar_id': webinar_id})

def response(request, webinar_id):
    webinar = Webinar.objects.get(pk=webinar_id)
    questions = Question.objects.filter(webinar=webinar)  
    current_user = request.user
    attendee = Attendee.objects.get(org_user=current_user)
    certify = WebinarRegistration.objects.get(user=attendee, webinar=webinar)    
    if request.method == 'POST':
        for question in questions:
            response_text = request.POST.get('response_{}'.format(question.id))
            response = Response.objects.create(
                user=attendee,
                response=response_text,
                question=question 
            )
        certify.certificate_status = 1
        certify.save()
        return redirect('eventapp:past_webinars')
    return render(request, 'response.html', {'questions': questions})

def view_responses(request,webinar_id):
    questions = Question.objects.filter(webinar_id=webinar_id)
    question_responses = {}
    for question in questions:
        responses = Response.objects.filter(question_id=question.id)
        question_responses[question] = responses
    return render(request, 'view_responses.html', {'question_responses': question_responses})

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from django.http import HttpResponse
import matplotlib.pyplot as plt
from datetime import datetime
from .models import Webinar, ParticipationCertificate, WebinarRegistration

def generate_webinar_report(request, webinar_id):
    webinar = Webinar.objects.get(id=webinar_id)
    num_participants = ParticipationCertificate.objects.filter(webinar_title=webinar.title)
    start_datetime = datetime.combine(datetime.today(), webinar.start_time)
    end_datetime = datetime.combine(datetime.today(), webinar.end_time)
    duration = end_datetime - start_datetime
    speakers_list = ', '.join(str(speaker) for speaker in webinar.speakers.all())
    registrations = WebinarRegistration.objects.filter(webinar=webinar)
    organizations = registrations.values_list('user__organization', flat=True).distinct()

    # Table data for main details
    main_table_data = [
        ['Title', webinar.title],
        ['Date', str(webinar.date)],
        ['Start Time', str(webinar.start_time) if webinar.start_time else "N/A"],
        ['End Time', str(webinar.end_time) if webinar.end_time else "N/A"],
        ['Duration', str(duration) if duration else "N/A"],
        ['Online/Offline', webinar.event_type],
        ['Organizer', webinar.organizer_name],
        ['Speakers', speakers_list],
        ['Participants', str(num_participants.count())],
        ['Registrations', str(webinar.get_registrations().count())]
    ]

    # Table data for organization-wise participants
    organization_table_data = [['Organization', 'Number of Registrations']]
    participants_by_organization = {}
    for organization in organizations:
        num_participants = registrations.filter(user__organization=organization).count()
        participants_by_organization[organization] = num_participants
        organization_table_data.append([organization, num_participants])

    # # Plotting the graph
    plt.figure(figsize=(10, 6))
    plt.bar(participants_by_organization.keys(), participants_by_organization.values())
    plt.xlabel('Organization')
    plt.ylabel('Number of Participants')
    plt.title('Number of Participants from Each Organization')
    plt.yticks(range(0, max(participants_by_organization.values()) + 1))  # Set y-ticks to whole numbers
    plt.tight_layout()  # Adjust layout to prevent clipping of labels
    plt.show()

    # Generating PDF
    pdf_filename = f"webinar_report_{webinar_id}.pdf"
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{pdf_filename}"'
    doc = SimpleDocTemplate(response, pagesize=letter)

    # Main heading style
    main_heading_style = ParagraphStyle(
        name='MainHeading',
        fontSize=20,
        textColor=colors.black,
        alignment=TA_CENTER,  
        spaceAfter=20 
    )
    main_heading = Paragraph("Webinar Report", main_heading_style)
    report_content = [main_heading]

    # Main details table
    main_table = Table(main_table_data, colWidths=[150, 300])
    main_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))    

    # Organization-wise participants table
    organization_table = Table(organization_table_data, colWidths=[200, 150])
    organization_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    # Building PDF content
    doc.build([main_heading, Spacer(1, 20), main_table, Spacer(1, 20), organization_table])    
    return response
