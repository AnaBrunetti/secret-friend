from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
from website.forms import ContactForm
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.urls import reverse

class HomeView(TemplateView):
    template_name = 'home.html'
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(HomeView, self).dispatch(*args, **kwargs)
    
class AboutView(TemplateView):
    template_name = 'general/about.html'
    
class TermsView(TemplateView):
    template_name = 'general/terms.html'
    
class ContactView(TemplateView, FormView, SuccessMessageMixin):
    template_name = 'general/contact.html'
    form_class = ContactForm
    success_message = 'Sua mensagem foi enviada com sucesso!'
    
    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, 'form submission success')
        return reverse('contact:contact')
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.send_email()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

