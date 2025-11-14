from django.shortcuts import render, reverse
from .models import CustomUser, Uzduotis, UzduotisInstance
from .forms import (BaseUzduotisInstanceForm as base,
                    StaffUzduotisInstanceForm as staff,
                    CustomUserCreateForm)
from django.views.generic import TemplateView
from django.views import generic as g
from django.views.generic.edit import FormMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class IndexView(TemplateView):
    template_name='index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        num_workers = CustomUser.objects.count()
        num_instances = UzduotisInstance.objects.count()
        num_late = UzduotisInstance.objects.filter(status__exact='p').count()

        context.update({
            'num_workers': num_workers,
            'num_instances': num_instances,
            'num_late': num_late,
        })

        return context
    
class CustomUserListView(g.ListView):
    model = CustomUser
    template_name = "workers.html"
    context_object_name = "workers"

class CustomUserDetailView(g.DetailView):
    model = CustomUser
    template_name = "worker.html"
    context_object_name = "worker"

class UzduotisInstanceCreateView(LoginRequiredMixin, g.CreateView):
    model = UzduotisInstance
    template_name = "uzduotis_ins_form.html"
    
    def get_form_class(self):
        if self.request.user.is_staff:
            return staff
        return base           

    def form_valid(self, form):
        name = form.cleaned_data.get('name')
        content = form.cleaned_data.get('content')
        shift = self.request.user.shift if hasattr(self.request.user, 'shift') else '1'
        uzduotis = Uzduotis.objects.create(
            name=name,
            content=content,
            user=self.request.user,
            shift=shift
        )
        form.instance.task = uzduotis
        form.instance.user = self.request.user
        response = super().form_valid(form)
        if not self.request.user.is_staff:
            self.object.worker.add(self.request.user)
            
        return response
    
    def get_success_url(self):
        worker_pk = self.kwargs.get('worker_pk')
        return reverse_lazy("worker", kwargs={"pk": worker_pk})

class SignUp(g.CreateView):
    form_class = CustomUserCreateForm
    template_name = "signup.html"
    success_url = reverse_lazy("login")
