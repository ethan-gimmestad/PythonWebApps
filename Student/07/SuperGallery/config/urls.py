from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from SuperProfiles.views_hero import HeroDetailView, HeroListView, HeroCreateView, HeroUpdateView, HeroDeleteView
from SuperProfiles.views_reporter import ReporterHomeView, ReporterAddView, ReporterDetailView, ReporterListView, ReporterUpdateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/profile/',  RedirectView.as_view(url='/reporter/home')),

    path('',                     RedirectView.as_view(url='hero/')),
    path('hero/',                HeroListView.as_view(),    name='hero_list'),
    path('hero/<int:pk>',        HeroDetailView.as_view(),  name='hero_detail'),
    path('hero/add',             HeroCreateView.as_view(),  name='hero_add'),
    path('hero/<int:pk>/',       HeroUpdateView.as_view(),  name='hero_edit'),
    path('hero/<int:pk>/delete', HeroDeleteView.as_view(),  name='hero_delete'),

    path('reporter/',                    ReporterListView.as_view(),    name='reporter_list'),
    path('reporter/home',                ReporterHomeView.as_view(),    name='reporter_home'),
    path('reporter/<int:pk>',            ReporterDetailView.as_view(),  name='reporter_detail'),
    path('reporter/add/',                ReporterAddView.as_view(),     name='reporter_add'),
    path('reporter/<int:pk>/',           ReporterUpdateView.as_view(),  name='reporter_edit'),
]