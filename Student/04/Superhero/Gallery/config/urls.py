from django.urls import path
from photos.views import PhotoListView, PhotoView
urlpatterns = [
    path('chapter-3.jpg', PhotoView.as_view()),
    path('', PhotoListView.as_view()),
]