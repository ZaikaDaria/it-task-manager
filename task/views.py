from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from .forms import WorkerCreationForm, WorkerSearchForm, TaskNameSearchForm
from .models import Task, Position, Worker, TaskType

from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView, PasswordResetConfirmView
from .forms import RegistrationForm, UserLoginForm, UserPasswordResetForm, UserSetPasswordForm, UserPasswordChangeForm
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
    queryset = Task.objects.all().select_related("task_type")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskNameSearchForm, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = TaskNameSearchForm(initial={
            "name": name}
        )
        return context

    def get_queryset(self):
        queryset = Task.objects.all()
        form = TaskNameSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )
        return queryset


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    fields = ["name", "description", "priority", "deadline", "task_type", "assignees"]
    success_url = reverse_lazy("task:task-list")


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    fields = "__all__"
    success_url = reverse_lazy("manager:task-list")


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("task:task-list")


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(WorkerSearchForm, self).get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["search_form"] = WorkerSearchForm(initial={
            "username": username}
        )
        return context

    def get_queryset(self):
        queryset = Worker.objects.all()
        form = WorkerSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(
                username__icontains=form.cleaned_data["username"]
            )
        return queryset


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker
    queryset = Worker.objects.all().select_related("position")


class WorkerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Worker
    form_class = WorkerCreationForm
    success_url = reverse_lazy("manager:worker-list")


class WorkerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Worker
    fields = ["username", "first_name", "last_name", "position"]
    success_url = reverse_lazy("manager:worker-list")


class WorkerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Worker
    success_url = reverse_lazy("manager:worker-list")


# Authentication

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            print("Account created successfully!")
            return redirect('/accounts/login')
        else:
            print("Registration failed!")
    else:
        form = RegistrationForm()

    context = {'form': form}
    return render(request, 'accounts/sign-up.html', context)


class UserLoginView(LoginView):
    template_name = 'accounts/sign-in.html'
    form_class = UserLoginForm


def logout_view(request):
    logout(request)
    return redirect('/accounts/login')


class UserPasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset.html'
    form_class = UserPasswordResetForm


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    form_class = UserSetPasswordForm


class UserPasswordChangeView(PasswordChangeView):
    template_name = 'accounts/password_change.html'
    form_class = UserPasswordChangeForm


# Sections
def priority(request):
    high_priority_tasks = Task.objects.filter(Q(priority="high") & Q(is_completed=False))
    medium_priority_tasks = Task.objects.filter(Q(priority="medium") & Q(is_completed=False))
    low_priority_tasks = Task.objects.filter(Q(priority="low") & Q(is_completed=False))

    context = {
        "high_priority_tasks": high_priority_tasks,
        "medium_priority_tasks": medium_priority_tasks,
        "low_priority_tasks": low_priority_tasks,
    }

    return render(request, "task/priority.html", context=context)


def page_header(request):
    return render(request, 'sections/page-sections/hero-sections.html')


def features(request):
    return render(request, 'sections/page-sections/features.html')


def navbars(request):
    return render(request, 'sections/navigation/navbars.html')


def nav_tabs(request):
    return render(request, 'sections/navigation/nav-tabs.html')


def pagination(request):
    return render(request, 'sections/navigation/pagination.html')


def inputs(request):
    return render(request, 'sections/input-areas/inputs.html')


def forms(request):
    return render(request, 'sections/input-areas/forms.html')


def avatars(request):
    return render(request, 'sections/elements/avatars.html')


def badges(request):
    return render(request, 'sections/elements/badges.html')


def breadcrumbs(request):
    return render(request, 'sections/elements/breadcrumbs.html')


def buttons(request):
    return render(request, 'sections/elements/buttons.html')


def dropdowns(request):
    return render(request, 'sections/elements/dropdowns.html')


def progress_bars(request):
    return render(request, 'sections/elements/progress-bars.html')


def toggles(request):
    return render(request, 'sections/elements/toggles.html')


def typography(request):
    return render(request, 'sections/elements/typography.html')


def alerts(request):
    return render(request, 'sections/attention-catchers/alerts.html')


def modals(request):
    return render(request, 'sections/attention-catchers/modals.html')


def tooltips(request):
    return render(request, 'sections/attention-catchers/tooltips-popovers.html')
