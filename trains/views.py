from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from trains.models import Train
from trains.forms import TrainForm


def home(request, pk=None):
    trains = Train.objects.all()
    paginator = Paginator(trains, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'title': 'Travel - Trains',
        'page_obj': page_obj,
    }
    return render(request, 'trains/home.html', context=context)


class TrainListView(ListView):
    paginate_by = 5
    model = Train
    template_name = 'trains/home.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        form = TrainForm()
        context['form'] = form
        context['title'] = 'Travel - Поезда'
        return context


class TrainDetailView(DetailView):
    queryset = Train.objects.all()
    template_name = 'trains/train_detail.html'


class TrainCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Train
    form_class = TrainForm
    template_name = 'trains/train_create.html'
    success_url = reverse_lazy('trains:home')
    success_message = 'Поезд успешно создан.'


class TrainUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Train
    form_class = TrainForm
    template_name = 'trains/train_update.html'
    success_url = reverse_lazy('trains:home')
    success_message = 'Поезд успешно отредактирован.'


class TrainDeleteView(LoginRequiredMixin, DeleteView):
    model = Train
    # template_name = 'trains/train_delete.html'
    success_url = reverse_lazy('trains:home')

    def get(self, request, *args, **kwargs):
        messages.success(request, 'Поезд успешно удален.')
        return self.post(request, *args, **kwargs)
