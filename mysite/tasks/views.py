from django.shortcuts import render, redirect, reverse, get_object_or_404
from .models import CustomUser, Uzduotis, UzduotisInstance
from .models import PAMAINA
from .forms import (BaseUzduotisInstanceForm as base,
                    StaffUzduotisInstanceForm as staff,
                    CustomUserCreateForm,
                    CustomUserUpdateForm,
                    StaffUserUpdateForm)
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
    
class UzduotisListView(LoginRequiredMixin, UserPassesTestMixin, g.ListView):
    model = Uzduotis
    template_name = "visos_uzduotys.html"
    context_object_name = "task_list"

    def test_func(self):
        return self.request.user.is_staff   

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('query', '')
        if query:
            filters = Q() 
            shift_keys = []
            filters |= Q(name__icontains=query)
            try:
                shift_keys = [
                    key for key, label in PAMAINA if query.lower() in label.lower()
                ]    
                filters |= Q(shift__in=shift_keys)
                filters |= Q(shift__icontains=query)
            except NameError:
                pass                
            filters |= Q(instances__worker__first_name__icontains=query)
            filters |= Q(instances__worker__last_name__icontains=query)
            if shift_keys: 
                filters |= Q(instances__worker__shift__in=shift_keys)
            queryset = queryset.filter(filters).distinct()
        return queryset
    
class UzduotisInstanceListView(LoginRequiredMixin, UserPassesTestMixin, g.ListView):
    model = UzduotisInstance
    template_name = "task_instances.html" 
    context_object_name = "task_inst_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        uzduotis_pk = self.kwargs.get('pk')
        context['uzduotis_definition'] = get_object_or_404(Uzduotis, pk=uzduotis_pk)
        return context
    
    def get_queryset(self):
        uzduotis_pk = self.kwargs.get('pk')
        queryset = UzduotisInstance.objects.filter(task__pk=uzduotis_pk)
        return queryset

    def test_func(self):
        return self.request.user.is_staff 
    
class CustomUserListView(LoginRequiredMixin, UserPassesTestMixin, g.ListView):
    model = CustomUser
    template_name = "workers.html"
    context_object_name = "workers"

    def test_func(self):
        return self.request.user.is_staff

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('query', '')
        if query:
            shift_keys = [
                key for key, label in PAMAINA if query.lower() in label.lower()
            ]
            queryset = queryset.filter(
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(shift__icontains=query) |
                Q(shift__in=shift_keys)
            )                                    
        return queryset

class CustomUserUpdateView(LoginRequiredMixin, UserPassesTestMixin, g.UpdateView):
    model = CustomUser
    template_name = "worker.html"
    context_object_name = "worker"
    form_class = StaffUserUpdateForm

    def get_success_url(self):
        return reverse('worker', kwargs={'pk': self.object.pk})
    
    def test_func(self):
        return self.request.user == self.get_object() or self.request.user.is_staff

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)
    

class UzduotisInstanceCreateView(LoginRequiredMixin, g.CreateView):
    model = UzduotisInstance
    template_name = "uzduotis_form.html"
    
    def get_form_class(self):
        if self.request.user.is_staff:
            return staff
        return base           

    def form_valid(self, form):
        if not self.request.user.is_staff:
            selected_task = form.cleaned_data.get('task_default')
            form.instance.task = selected_task
            form.instance.user = self.request.user
            response = super().form_valid(form)
            self.object.worker.add(self.request.user)
        else:
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
                
        return response

    
    def get_success_url(self):
        return reverse_lazy("worker", kwargs={"pk": self.kwargs.get('worker_pk')})
    
class UzduotisInstanceUpdateView(LoginRequiredMixin, UserPassesTestMixin, g.UpdateView):
    model = UzduotisInstance
    template_name = "uzduotis_form.html"

    def get_form_class(self):
        if self.request.user.is_staff:
            return staff
        return base    
    
    def get_success_url(self):
        return reverse_lazy("worker", kwargs={"pk": self.kwargs.get('worker_pk')})

    def test_func(self):
        return self.get_object().user == self.request.user or self.request.user.is_staff
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.method == 'GET':
            instance = self.get_object()
            kwargs['initial'] = {
                'name': instance.task.name,
                'content': instance.task.content
            }
        return kwargs
    
    def form_valid(self, form):
        instance = self.object
        if 'name' in form.cleaned_data:
            related_task = instance.task
            related_task.name = form.cleaned_data['name']
            related_task.content = form.cleaned_data['content']
            related_task.save()
        return super().form_valid(form)

class SignUp(g.CreateView):
    form_class = CustomUserCreateForm
    template_name = "signup.html"
    success_url = reverse_lazy("index")

class ProfileUpdateView(LoginRequiredMixin, g.UpdateView):
    model = CustomUser
    form_class = CustomUserUpdateForm
    template_name = "profile.html"
    success_url = reverse_lazy("profile")
    
    def get_object(self, queryset=...):
        return self.request.user
    
    def form_invalid(self, form):
        self.request.user.refresh_from_db()
        return self.render_to_response(self.get_context_data(form=form))
