from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse

# Create your views here.
class HomeView(View):
    template_name = 'home/main.html'

    def get(self, request):
        return render(request, self.template_name)
