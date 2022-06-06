from django.urls import URLPattern, path
from . import views
# from django.views.generic import TemplateView

urlpatterns = [
    path('', views.profile, name = 'Profile'),
    path('getMyInfo', views.getMyInfo),
    path('designer_selected_for_commission', views.designer_selected_for_commission),
    path('delete_message',views.delete_message)
]
