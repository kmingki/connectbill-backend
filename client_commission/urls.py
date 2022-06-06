from . import views

from django.urls import URLPattern, path
# from django.views.generic import TemplateView

urlpatterns = [
    path('commission_view/', views.commission_view),
    path('create_commission', views.create_commission),
    path('<int:pk>/commission_view_detail/',views.commission_view_detail),
    # path('commission_designer_selected_by_client',views.commission_designer_selected_by_client),
    path('<int:pk>/commission_select_for_designer',views.commission_select_for_designer),
    path('<int:pk>/end_commission',views.end_commission)
]

