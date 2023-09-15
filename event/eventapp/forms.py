from django import forms
from .models import Webinar, EventOrganizer, Conference

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