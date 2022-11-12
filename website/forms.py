from django import forms
from django.core.mail import send_mail
from django.http import JsonResponse

class ContactForm(forms.Form):
    contact_subject = forms.CharField()
    contact_message = forms.CharField(widget=forms.Textarea)
    
    def send_email(self):
        try:
            send_mail('[Amigo Secreto] - Novo contato: ' + self.cleaned_data.get('contact_subject'),
				self.cleaned_data.get('contact_message'),
				'carol-brunetti@hotmail.com',
				['eduardomonita1@gmail.com'],
				fail_silently=False,)
            return JsonResponse({ 'success' : True, 'message' : 'seu email foi enviado com sucesso.' }, safe = False, status=200)
        except Exception as e:
            return JsonResponse({ 'success' : False, "message": str(e) }, status=500)
