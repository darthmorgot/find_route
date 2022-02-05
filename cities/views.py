from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from cities.models import City
from cities.forms import HtmlForm, CityForm


def home(request, pk=None):
    # if pk:
    #     city = City.objects.filter(pk=pk).first()
    #     city = City.objects.get(pk=pk)
    #     city = get_object_or_404(City, pk=pk)
    #     context = {'city': city}
    #     return render(request, 'cities/city_detail.html', context=context)

    if request.method == 'POST':
        form = CityForm(request.POST)

        if form.is_valid():
            # print(form.cleaned_data)
            form.save()
    else:
        form = CityForm()

    cities = City.objects.all()
    paginator = Paginator(cities, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'title': 'Travel - Cities',
        'page_obj': page_obj,
        'form': form,
    }
    return render(request, 'cities/home.html', context=context)


class CityDetailView(DetailView):
    queryset = City.objects.all()
    template_name = 'cities/city_detail.html'


class CityCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = City
    form_class = CityForm
    template_name = 'cities/city_create.html'
    success_url = reverse_lazy('cities:home')
    success_message = 'Город успешно создан.'


class CityUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = City
    form_class = CityForm
    template_name = 'cities/city_update.html'
    success_url = reverse_lazy('cities:home')
    success_message = 'Город успешно отредактирован.'


class CityDeleteView(LoginRequiredMixin, DeleteView):
    model = City
    # template_name = 'cities/city_delete.html'
    success_url = reverse_lazy('cities:home')

    def get(self, request, *args, **kwargs):
        messages.success(request, 'Город успешно удален.')
        return self.post(request, *args, **kwargs)


class CityListView(ListView):
    paginate_by = 2
    model = City
    template_name = 'cities/home.html'
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        form = CityForm()
        context['title'] = 'Travel - Города'
        context['form'] = form
        return context
