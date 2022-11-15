import requests
import json
from random import randint
from django.views.generic import CreateView
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import views
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from accounts.forms import RegisterForm, ProfissionalRegisterForm
from accounts.models import User
from accounts.selenium import get_recaptcha_token

COLORS = ['vermelho', 'verde', 'azul', 'preto', 'branco', 'marrom', 'laranja', 'amarelo', 'cinza']
ANIMALS = ['peixe', 'passaro', 'gato', 'cachorro', 'leao', 'rapossa', 'urso', 'sapo', 'morcego', 'tubarao']
NUMBERS_RANGE = [0, 999]


class RegisterView(CreateView):
    template_name = 'accounts/register.html'
    form_class = RegisterForm
    
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('chat'))
        return super(RegisterView, self).get(request, *args, **kwargs)
    
    def get_success_url(self):
        return reverse_lazy("chat")

    def get_initial(self, **kwargs):
        initial = super(RegisterView, self).get_initial()
        initial["username"] = f'{COLORS[randint(0,len(COLORS)-1)]}.{ANIMALS[randint(0,len(ANIMALS)-1)]}.' \
            f'{randint(*NUMBERS_RANGE):03d}'
        while User.objects.filter(username=initial["username"]).exists():
            initial["username"] = f'{COLORS[randint(0, len(COLORS)-1)]}.{ANIMALS[randint(0, len(ANIMALS)-1)]}.' \
                f'{randint(*NUMBERS_RANGE)}'
        initial["role"] = User.ROLE_PATIENT
        return initial
    
    def get_context_data(self, **kwargs):
        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()
        
        kwargs.setdefault('view', self)
        if self.extra_context is not None:
            kwargs.update(self.extra_context)
        return kwargs

    def form_invalid(self, form, **kwargs):
        raw_data = form.data.copy()
        raw_data.update(form.cleaned_data)
        raw_data.update(form.initial)
        form.data = raw_data
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.username = form.initial["username"]
        self.object.save()
        login(self.request, self.object)
        return HttpResponseRedirect(self.get_success_url())


class ProfissionaRegisterView(CreateView):
    template_name = 'accounts/profissional-register.html'
    form_class = ProfissionalRegisterForm
    
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('chat'))
        return super(ProfissionaRegisterView, self).get(request, *args, **kwargs)
    
    def get_success_url(self):
        return reverse_lazy("chat")

    def get_initial(self, **kwargs):
        initial = super(ProfissionaRegisterView, self).get_initial()
        initial["role"] = User.ROLE_PROFESSIONAL
        return initial
    
    def get_context_data(self, **kwargs):
        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()
        
        kwargs.setdefault('view', self)
        if self.extra_context is not None:
            kwargs.update(self.extra_context)
        return kwargs

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            
            cpf = form.cleaned_data["cpf"].replace(".", "").replace("-", "")
            token = get_recaptcha_token()
            url = f'https://cn-api.cfp.org.br/psi/busca?nome=&regiao=&registro=&tipo=PF&recaptchaToken={token}&cpf={cpf}'
            
            response = requests.get(url)
            response_dict = json.loads(response.text)
            
            is_approved = False
            if len(response_dict) > 0 and response_dict[0].get("situacao") == "ATIVO":
                is_approved = True
            return self.form_valid(form, is_approved=is_approved)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form, **kwargs):
        raw_data = form.data.copy()
        raw_data.update(form.cleaned_data)
        raw_data.update(form.initial)
        form.data = raw_data
        return self.render_to_response(self.get_context_data(form=form))
    
    def form_valid(self, form, is_approved=False):
        profissional = form.save(is_approved=is_approved)
        if not profissional.is_approved:
            messages.add_message(
                self.request,
                messages.INFO,
                'Sua conta foi criada! Estamos verificando seus dados para aprová-lo como profissional e logo terá permissão para logar.'
            )
            return HttpResponseRedirect(reverse_lazy("profissiona_register"))
        login(self.request, profissional.user)
        return HttpResponseRedirect(self.get_success_url())


class PasswordChangeView(views.PasswordChangeView):
    template_name = 'registration/password_change.html'
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PasswordChangeView, self).dispatch(*args, **kwargs)


class ProfileEditView(views.PasswordChangeView):
    template_name = 'accounts/edit-profile.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProfileEditView, self).dispatch(*args, **kwargs)