from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Invisible
from dal import autocomplete
from django import forms

from LottoWebCore.models import MiddleMan, Ticket, StudentDirectory, University, Raffle, City, RegistrationRequest


class TicketForm(forms.ModelForm):
    method = forms.CharField(widget=forms.HiddenInput(), initial='ADD')
    model = forms.CharField(widget=forms.HiddenInput(), initial='TCK')

    Vendedor = forms.ModelChoiceField(
        queryset=MiddleMan.objects.all(),
        widget=autocomplete.ModelSelect2(url='seller-autocomplete')
    )

    class Meta:
        model = Ticket
        fields = ('raffle', 'directory')


class StudentDirectoryForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(StudentDirectoryForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.id:
            self.fields['id'].required = False
            self.fields['id'].widget.attrs['readonly'] = 'readonly'

    method = forms.CharField(widget=forms.HiddenInput(), initial='ADD')
    model = forms.CharField(widget=forms.HiddenInput(), initial='DIR')

    class Meta:
        model = StudentDirectory
        fields = '__all__'


class UniversityForm(forms.ModelForm):
    method = forms.CharField(widget=forms.HiddenInput(), initial='ADD')
    model = forms.CharField(widget=forms.HiddenInput(), initial='UNI')

    class Meta:
        model = University
        fields = '__all__'


class CityForm(forms.ModelForm):
    method = forms.CharField(widget=forms.HiddenInput(), initial='ADD')
    model = forms.CharField(widget=forms.HiddenInput(), initial='CTY')

    class Meta:
        model = City
        fields = '__all__'


class RaffleForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(RaffleForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.id:
            self.fields['id'].required = False
            self.fields['id'].widget.attrs['readonly'] = 'readonly'
            self.fields['lottery'].widget.attrs['id'] = 'datepicker'

    # widgets = {
    #     'lottery': forms.DateTimeInput(attrs={'class': 'datetime-input'})
    # }

    method = forms.CharField(widget=forms.HiddenInput(), initial='ADD')
    model = forms.CharField(widget=forms.HiddenInput(), initial='RAF')

    class Meta:
        model = Raffle
        fields = '__all__'
        widgets = {
            'completed': forms.HiddenInput(),
        }


class TicketEditForm(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super(TicketEditForm, self).__init__(*args, **kwargs)
    #     instance = getattr(self, 'instance', None)
    #     if instance and instance.id:
    #         self.fields['id'].required = False
    #         self.fields['id'].widget.attrs['readonly'] = 'readonly'

    id = forms.ModelChoiceField(
        queryset=Ticket.objects.all(),
        widget=autocomplete.ModelSelect2(url='ticket-autocomplete', forward=['ticket_status'])
    )

    ticket_status = forms.CharField(widget=forms.HiddenInput(), initial='True')
    method = forms.CharField(widget=forms.HiddenInput(), initial='EDT')
    model = forms.CharField(widget=forms.HiddenInput(), initial='TCK_E')

    class Meta:
        model = Ticket
        fields = ('name', 'email', 'phone', 'raffle')
        widgets = {
            'notified': forms.HiddenInput(),
            'activated': forms.HiddenInput(),
            'raffle': forms.HiddenInput(),
        }


class TicketActivationForm(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super(TicketEditForm, self).__init__(*args, **kwargs)
    #     instance = getattr(self, 'instance', None)
    #     if instance and instance.id:
    #         self.fields['id'].required = False
    #         self.fields['id'].widget.attrs['readonly'] = 'readonly'

    id = forms.ModelChoiceField(
        queryset=Ticket.objects.all(),
        widget=autocomplete.ModelSelect2(url='ticket-autocomplete', forward=['ticket_status'])
    )

    ticket_status = forms.CharField(widget=forms.HiddenInput(), initial='False')
    method = forms.CharField(widget=forms.HiddenInput(), initial='ATV')
    model = forms.CharField(widget=forms.HiddenInput(), initial='TCK_A')

    class Meta:
        model = Ticket
        fields = ('name', 'seller', 'phone', 'email')
        widgets = {
            'completed': forms.HiddenInput(),
        }


class SignUpForm(forms.ModelForm):
    method = forms.CharField(widget=forms.HiddenInput(), initial='ADD')
    model = forms.CharField(widget=forms.HiddenInput(), initial='REG')
    captcha = ReCaptchaField(widget=ReCaptchaV2Invisible(), label='')

    class Meta:
        model = RegistrationRequest
        fields = '__all__'


class TicketCheckForm(forms.ModelForm):
    method = forms.CharField(widget=forms.HiddenInput(), initial='ATV')
    model = forms.CharField(widget=forms.HiddenInput(), initial='CHK')
    captcha = ReCaptchaField(widget=ReCaptchaV2Invisible(), label='')

    id = forms.CharField(max_length=10, required=True, label="Número do Bilhete")
    # email = forms.EmailField()

    class Meta:
        model = Ticket
        fields = ('raffle', 'seller')
