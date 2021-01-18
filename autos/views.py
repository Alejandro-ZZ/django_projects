from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from autos.models import Auto, Make

# Create your views here.
#-----------------------------------------------------------------------------

class MainView(LoginRequiredMixin, View):
    def get(self, request):
        mc = Make.objects.all().count()
        al = Auto.objects.all()

        ctx = {'make_count': mc, 'auto_list': al}
        return render(request, 'autos/auto_list.html', ctx)


class MakeView(LoginRequiredMixin, View):
    def get(self, request):
        ml = Make.objects.all()
        ctx = {'make_list': ml}
        return render(request, 'autos/make_list.html', ctx)

#------------------------------------------------------------------------------

class MakeCreate(LoginRequiredMixin, CreateView):
    model = Make
    fields = ['name']
    success_url = reverse_lazy('autos:all')

    # Valid Form
    def form_valid(self, form):
        posts = Make.objects.filter(owner__username=self.request.user)
        post_num = posts.count()

        # User has 3 or less makes
        if post_num < 3:
            # Add owner to the model before saving
            make = form.save(commit=False)
            make.owner = self.request.user
            make.save()
            return redirect(self.success_url)
        # User has more than 3 makes
        else:
            return render(self.request, 'autos/make_form.html', {'form': form, 'error': 'Limit exceeded'})


class MakeUpdate(LoginRequiredMixin, UpdateView):
    model = Make
    #Shows all fields of Make table
    fields = '__all__'
    success_url = reverse_lazy('autos:all')


class MakeDelete(LoginRequiredMixin, DeleteView):
    model = Make
    #Shows all fields of Make table
    fields = '__all__'
    success_url = reverse_lazy('autos:all')

#------------------------------------------------------------------------------

class AutoCreate(LoginRequiredMixin, CreateView):
    model = Auto
    #fields = '__all__'
    fields = ['nickname', 'mileage', 'comments', 'make']
    success_url = reverse_lazy('autos:all')

    # Valid Form
    def form_valid(self, form):
        posts = Auto.objects.filter(owner__username=self.request.user)
        post_num = posts.count()

        # User has 3 or less autos
        if post_num < 3:
            # Add owner to the model before saving
            auto = form.save(commit=False)
            auto.owner = self.request.user
            auto.save()
            return redirect(self.success_url)
        # User has more than 3 makes
        else:
            return render(self.request, 'autos/auto_form.html', {'form': form, 'error': 'Limit exceeded'})

class AutoUpdate(LoginRequiredMixin, UpdateView):
    model = Auto
    fields = '__all__'
    success_url = reverse_lazy('autos:all')


class AutoDelete(LoginRequiredMixin, DeleteView):
    model = Auto
    fields = '__all__'
    success_url = reverse_lazy('autos:all')
