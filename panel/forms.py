from django.forms import ModelForm
from .models import Submit_Information_Model
from jalali_date.fields import JalaliDateField, SplitJalaliDateTimeField
from jalali_date.widgets import AdminJalaliDateWidget, AdminSplitJalaliDateTime
from django import forms

class Submit_Information_Form(forms.ModelForm):
    description_letter = forms.CharField(widget=forms.Textarea(attrs={"rows":8}), required=False)
    description = forms.CharField(widget=forms.Textarea(attrs={"rows":8}), required=False)
    class Meta:
        model = Submit_Information_Model
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(Submit_Information_Form, self).__init__(*args, **kwargs)
        self.fields['date_letter'] = JalaliDateField(label=('date_letter'),
            widget=AdminJalaliDateWidget
        )
        self.fields['date_deposit'] = JalaliDateField(label=('date_deposit'), 
            widget=AdminJalaliDateWidget
        )
        self.fields['date_letter'].required=False
        self.fields['date_deposit'].required=False
        # self.fields['description_letter', 'description', 'date_letter', 'date_deposit'].required = False