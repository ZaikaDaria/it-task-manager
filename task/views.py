from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.urls import reverse_lazy
from django.views import generic

from .forms import WorkerCreationForm, WorkerSearchForm, TaskNameSearchForm, WorkerForm
from .models import Task, Worker

from django.shortcuts import render, redirect
from django.contrib.auth.views import (
    LoginView,
    PasswordResetView,
    PasswordChangeView,
    PasswordResetConfirmView,
)
from .forms import (
    RegistrationForm,
    UserLoginForm,
    UserPasswordResetForm,
    UserSetPasswordForm,
    UserPasswordChangeForm,
    TaskForm,
)
from django.contrib.auth import logout


@login_required
def index(request):
    num_workers = get_user_model().objects.count()
    num_tasks = Task.objects.count()

    completed_tasks = Task.objects.filter(is_completed=True)

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_workers": num_workers,
        "num_tasks": num_tasks,
        "completed_tasks": completed_tasks,
        "num_visits": num_visits + 1,
    }

    return render(request, "task/index.html", context=context)


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    paginate_by = 7
    context_object_name = "task_all"
    queryset = Task.objects.all().select_related("task_type")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = TaskNameSearchForm(initial={"name": name})
        return context

    def get_queryset(self):
        queryset = Task.objects.all()
        form = TaskNameSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])
        return queryset


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("task:task-list")


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form = TaskForm
    fields = "__all__"
    success_url = reverse_lazy("task:task-list")


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("task:task-list")


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    paginate_by = 10
    template_name = "task/worker_list.html"
    queryset = Worker.objects.all().select_related("workers")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["search_form"] = WorkerSearchForm(initial={"username": username})
        return context

    def get_queryset(self):
        queryset = Worker.objects.all()
        form = WorkerSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(username__icontains=form.cleaned_data["username"])
        return queryset


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker
    queryset = Worker.objects.all().select_related("position")


class WorkerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Worker
    form_class = WorkerCreationForm
    success_url = reverse_lazy("task:worker-list")


class WorkerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Worker
    form_class = WorkerForm
    success_url = reverse_lazy("task:worker-list")


class WorkerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Worker
    success_url = reverse_lazy("task:worker-list")


class RegisterView(generic.View):
    def get(self, request):
        form = RegistrationForm()
        context = {"form": form}
        return render(request, "accounts/sign-up.html", context)

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            print("Account created successfully!")
            return redirect("/accounts/login")

        context = {"form": form}
        return render(request, "accounts/sign-up.html", context)


class UserLoginView(LoginView):
    template_name = "accounts/sign-in.html"
    form_class = UserLoginForm


class LogoutView(generic.View):
    def get(self, request):
        logout(request)
        return redirect("/accounts/login")


class UserPasswordResetView(PasswordResetView):
    template_name = "accounts/password_reset.html"
    form_class = UserPasswordResetForm


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "accounts/password_reset_confirm.html"
    form_class = UserSetPasswordForm


class UserPasswordChangeView(PasswordChangeView):
    template_name = "accounts/password_change.html"
    form_class = UserPasswordChangeForm


class AssignWorkerView(generic.RedirectView):
    def post(self, request, *args, **kwargs):
        pk = kwargs['pk']
        task = Task.objects.get(pk=pk)
        task.assignees.add(request.user)
        return super().post(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        pk = kwargs['pk']
        return reverse("task:task-detail", kwargs={"pk": pk})


class RemoveWorkerView(generic.View):
    def post(self, request, pk):
        task = Task.objects.get(pk=pk)
        task.assignees.remove(request.user)

        return redirect("task:task-detail", pk=task.pk)

    def get(self, request, pk):
        return redirect("task:task-detail", pk=pk)
