from . import views

from django.urls import URLPattern, path
# from django.views.generic import TemplateView

urlpatterns = [
    path('create_review', views.create_review),
    path('review_view/', views.review_view),
    path('<int:pk>/review_view_detail/', views.review_view_detail)
   
]

