from pathlib import Path
from django.shortcuts import render
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView, RedirectView, TemplateView
from .views_reporter import get_reporter
from .views_functions import IsPhotoCreatorMixin

from .models import Photo

def carousel_data(photos):

    def photo_data(id, photo):
        x = dict(image_url=f"/media/{photo.image}", link="/photo/"+str(photo.pk), id=str(id), label=f"{photo.image} {id}")
        if id == 0:
            x.update(active="active", aria='aria-current="true"')
        return x

    return [photo_data(id, photo) for id, photo in enumerate(photos)]

class PhotoListView(ListView):
    template_name = 'photo/list.html'
    model = Photo
    context_object_name = 'photos'

    def get_context_data(self, **kwargs):
        return {
            'object_list': Photo.objects.all()
        }

class PhotoCreateView(LoginRequiredMixin, CreateView):
    template_name = "photo/add.html"
    model = Photo
    fields = '__all__'

    def form_valid(self, form):
        form.instance.reporter = get_reporter(self.request.user)
        return super().form_valid(form)

class PhotoDetailView(DetailView):
    template_name = 'photo/detail.html'
    model = Photo
    context_object_name = 'photo'

class PhotoUpdateView(IsPhotoCreatorMixin, UpdateView):
    template_name = "photo/edit.html"
    model = Photo
    fields = '__all__'
    success_url = reverse_lazy('photo_list')

class PhotoDeleteView(IsPhotoCreatorMixin, DeleteView):
    template_name = 'photo/delete.html'
    model = Photo
    success_url = reverse_lazy('photo_list')

class PhotoCarouselView(TemplateView):
    template_name = 'photo/photocarousel.html'

    def get_context_data(self, **kwargs):
        photos = get_reporter(self.request.user).photos
        carousel = carousel_data(photos)
        return dict(title='Carousel View', carousel=carousel)