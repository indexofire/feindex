# -*- coding: utf-8 -*-

from django.views.generic import DetailView
from django.views.generic import TemplateView
from .forms import SignupForm
from .signals import *


class SignupView(TemplateView)
    """
    """
    template_name = 'account/signup_form.html'
    form = SignupForm
    success_url = None

    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()

            # Send the signup complete signal
            signup_complete.send(sender=None, user=user)

            if success_url:
                redirect_to = success_url
            else:
                redirect_to = reverse('account-signup-complete',
                    kwargs={'username': user.username})

            # A new signed user should logout the old one.
            if request.user.is_authenticated(): logout(request)

            return redirect(redirect_to)

    if not extra_context: extra_context = dict()

    def get(self, request, *args, **kwargs):
        context = form
        return self.render_to_response(context)

    #def get_context_data(self, **kwargs):
