from django import forms
from django.contrib.admin import widgets
from .models import orders_list
from datetime import datetime
class WorkFlowForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['client'].widget.attrs.update({'class':'form-control','id':'client'})
        self.fields['order_quantity'].widget.attrs.update({'class':'form-control','id':'quantity'})
        self.fields['spec'].widget.attrs.update({'class':'form-control','id':'spec'})
        #self.fields['unit'].widget.attrs.update({'class':'form-control','id':'focusedInput','value':'支'})
        self.fields['person_incharge'].widget.attrs.update({'class':'form-control','id':'person_incharge'})
        self.fields['requirement'].widget.attrs.update({'class':'form-control','id':'requirement','placeholder':'暂无'})
        self.fields['remark'].widget.attrs.update({'class':'form-control','id':'remark','placeholder':'暂无'})

    class Meta:
        model=orders_list
        fields = ('client','order_quantity','spec','person_incharge','requirement','remark')

    order_time = forms.DateField()
    sub_time = forms.DateField(widget=forms.SelectDateWidget(), label=u'时间')
    order_time.widget.attrs.update({'value':datetime.now().strftime('%Y-%m-%d'),'class':'form-control','id':'order_time'})
    sub_time.widget.attrs.update({'id':'sub_time'})
    #sub_time.widget.attrs.update({'value':datetime.now().strftime('%Y-%m-%d'),'class':'form-control'})

class WorkFlowDetailForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['client'].widget.attrs.update({'class':'form-control','id':'focusedInput','disabled':'disabled'})
        self.fields['order_quantity'].widget.attrs.update({'class':'form-control','id':'focusedInput','disabled':'disabled'})
        self.fields['spec'].widget.attrs.update({'class':'form-control','id':'focusedInput','disabled':'disabled'})
        self.fields['unit'].widget.attrs.update({'class':'form-control','id':'focusedInput','disabled':'disabled'})
        self.fields['person_incharge'].widget.attrs.update({'class':'form-control','id':'focusedInput','disabled':'disabled'})
        self.fields['requirement'].widget.attrs.update({'class':'form-control','id':'focusedInput'})
        self.fields['remark'].widget.attrs.update({'class':'form-control','id':'focusedInput'})
        self.fields['sub_time'].widget.attrs.update({'class':'form-control','id':'focusedInput'})
        self.fields['order_time'].widget.attrs.update({'class':'form-control','id':'focusedInput','disabled':'disabled'})
        self.fields['next_node'].widget.attrs.update({'class':'form-control','id':'focusedInput'})
    class Meta:
        model=orders_list
        fields = ('client','order_quantity','spec','unit','person_incharge','requirement','remark','order_time','sub_time','next_node')




