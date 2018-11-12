from django import forms
from django.contrib.admin import widgets
from .models import orders_list
from datetime import datetime
class WorkFlowForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['client'].widget.attrs.update({'class':'form-control','id':'focusedInput'})
        self.fields['order_quantity'].widget.attrs.update({'class':'form-control','id':'focusedInput'})
        self.fields['spec'].widget.attrs.update({'class':'form-control','id':'focusedInput'})
        self.fields['unit'].widget.attrs.update({'class':'form-control','id':'focusedInput'})
        self.fields['person_incharge'].widget.attrs.update({'class':'form-control','id':'focusedInput'})
        self.fields['requirement'].widget.attrs.update({'class':'form-control','id':'focusedInput'})
        self.fields['remark'].widget.attrs.update({'class':'form-control','id':'focusedInput'})

    class Meta:
        model=orders_list
        fields = ('client','order_quantity','spec','unit','person_incharge','requirement','remark')

    order_time = forms.DateField()
    sub_time = forms.DateField(widget=widgets.AdminDateWidget())
    order_time.widget.attrs.update({'value':datetime.now().strftime('%Y-%m-%d'),'class':'form-control'})
    sub_time.widget.attrs.update({'class':'form-control'})

class WorkFlowDetailForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['client'].widget.attrs.update({'class':'form-control','id':'focusedInput'})
        self.fields['order_quantity'].widget.attrs.update({'class':'form-control','id':'focusedInput'})
        self.fields['spec'].widget.attrs.update({'class':'form-control','id':'focusedInput'})
        self.fields['unit'].widget.attrs.update({'class':'form-control','id':'focusedInput'})
        self.fields['person_incharge'].widget.attrs.update({'class':'form-control','id':'focusedInput'})
        self.fields['requirement'].widget.attrs.update({'class':'form-control','id':'focusedInput'})
        self.fields['remark'].widget.attrs.update({'class':'form-control','id':'focusedInput'})

    class Meta:
        model=orders_list
        fields = ('client','order_quantity','spec','unit','person_incharge','requirement','remark')

    order_time = forms.DateField()
    sub_time = forms.DateField(widget=widgets.AdminDateWidget())
    order_time.widget.attrs.update({'value':datetime.now().strftime('%Y-%m-%d'),'class':'form-control'})
    sub_time.widget.attrs.update({'class':'form-control'})

