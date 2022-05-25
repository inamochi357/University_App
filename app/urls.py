from django.urls import path
from .views import ClassDetailView, PostNoteView, NoteView, PostReviewView
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.urls import re_path


urlpatterns = [
    path('<slug:pk>/', ClassDetailView.as_view(), name="ClassDetail"),
    path('<slug:pk>/Note/Post/', PostNoteView.as_view(), name="PostNote"),
    path('<slug:pk>/Review/Post/', PostReviewView.as_view(), name="PostReview"),
    path('<slug:pk>/Note/', NoteView.as_view(), name="NoteView"),
    path('<slug:pk>/Review/', views.ReviewListView, name="ReviewView"),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
]
