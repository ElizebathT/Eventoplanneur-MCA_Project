from django import forms
from .models import Webinar, EventOrganizer, Conference, Attendee, Feedback

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