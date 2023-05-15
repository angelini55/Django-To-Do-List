from typing import Any
from django.db import transaction
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic import CreateView, DeleteView, UpdateView, DetailView
from .models import List, Task, SubTask

# Create your views here.

class LoginRequiredMixin(object):
    """Mixing to avoid landing on other users list pages"""

    def dispatch(self, request, *args, **kwargs):
        if request.user.get_username() not in request.path:
            return redirect(reverse_lazy('home'))
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)

class ToDoListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'list/list.html'

    def get_queryset(self):
        user_list = List.objects.filter(title=f"lista de {self.request.user.get_username()}").first()
        return super().get_queryset().filter(list_id=user_list.id)
    
class IndividualTaskView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'list/detail.html'

    def get_success_url(self):
        return reverse_lazy('lista', args=[self.request.user.get_username()])
    
class CreateTaskView(LoginRequiredMixin, CreateView):
    model = Task
    fields = ["title"]
    
    def get_success_url(self):
        return reverse_lazy('lista', args=[self.request.user.get_username()])

    def form_valid(self, form):
        form.instance.list = List.objects.get(title="lista de {}".format(self.request.user.get_username()))
        return super().form_valid(form)
    
class UpdateTaskView(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ["is_completed"]
    template_name_suffix = "_update_form"

    @transaction.atomic
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('lista', args=[self.request.user.get_username()])
    
class DeleteTaskView(LoginRequiredMixin, DeleteView):
    model = Task
    
    def get_success_url(self):
        return reverse_lazy('lista', args=[self.request.user.get_username()])
    
class CreateSubTaskView(LoginRequiredMixin, CreateView):
    model = SubTask
    fields = ["title"]
    
    def get_success_url(self):
        return reverse_lazy('detail', args=[self.request.user.get_username(), self.kwargs['task_pk']])

    def form_valid(self, form):
        form.instance.task = Task.objects.get(id=self.kwargs['task_pk'])
        return super().form_valid(form)
    
class UpdateSubTaskView(LoginRequiredMixin, UpdateView):
    model = SubTask
    fields = ["is_completed"]
    template_name_suffix = "_update_form"

    @transaction.atomic
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('detail', args=[self.request.user.get_username(), self.object.task_id])
    
class DeleteSubTaskView(LoginRequiredMixin, DeleteView):
    model = SubTask
    
    def get_success_url(self):
        return reverse_lazy('detail', args=[self.request.user.get_username(), self.object.task_id])
    
