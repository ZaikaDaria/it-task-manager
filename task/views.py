from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from .forms import WorkerCreationForm, WorkerSearchForm
from .models import Task, Position, Worker, TaskType


def index(request):
    pass
