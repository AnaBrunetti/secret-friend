from django.views.generic import CreateView
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from accounts.forms import RegisterForm
from django.contrib.auth import views
from django.views.generic import TemplateView


class RegisterView(CreateView):
    template_name = 'accounts/register.html'
    form_class = RegisterForm
    
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('home'))
        return super(RegisterView, self).get(request, *args, **kwargs)
    
    def get_success_url(self):
        return reverse_lazy("home")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.email = user.username
        user.save()
        login(self.request, user)
        return HttpResponseRedirect(self.get_success_url())
     
class PasswordChangeView(views.PasswordChangeView):
    template_name = 'registration/password_change_form1.html'
    
class AboutView(TemplateView):
    template_name = 'general/about.html'
    
class TermsView(TemplateView):
    template_name = 'general/terms.html'
    
class ContactView(TemplateView):
    template_name = 'general/contact.html'