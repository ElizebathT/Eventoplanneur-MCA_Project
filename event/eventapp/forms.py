from django import forms
from .models import Webinar, EventOrganizer, Conference, Attendee, Feedback, BookService

class WebinarForm(forms.ModelForm):
    class Meta:
        model = Webinar
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(WebinarForm, self).__init__(*args, **kwargs)
        self.fields['speakers'].widget = forms.SelectMultiple(attrs={'class': 'form-control'})

class Organizer(forms.ModelForm):
    class Meta:
        model = EventOrganizer
        fields = '__all__'

class ConferenceForm(forms.ModelForm):
    class Meta:
        model = Conference
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(ConferenceForm, self).__init__(*args, **kwargs)
        self.fields['speakers'].widget = forms.SelectMultiple(attrs={'class': 'form-control'})

class AttendeeForm(forms.ModelForm):
    class Meta:
        model = Attendee
        fields = '__all__'

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'email', 'content']

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        email = cleaned_data.get('email')
        content = cleaned_data.get('content')
        # add your custom validation logic here
        return cleaned_data
    
from .models import Service
class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'category', 'image', 'locations', 'services_provided', 'capacity','description','booked_dates']
    
    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        category = cleaned_data.get('category')

        existing_service = Service.objects.filter(
            name__iexact=name,
            category__iexact=category
        )

        if existing_service:
            raise forms.ValidationError("This service already exists.")


class BookServiceForm(forms.ModelForm):
    class Meta:
        model = BookService
        fields = ['location', 'services_required', 'budget', 'date', 'participants']