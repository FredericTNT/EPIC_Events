from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render


class PresentationView(LoginRequiredMixin, View):
    template_name = 'events/home.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
