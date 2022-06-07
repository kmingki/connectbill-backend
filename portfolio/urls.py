from . import views

from django.urls import URLPattern, path
# from django.views.generic import TemplateView

urlpatterns = [
    path('portfolio_view/', views.portfolio_view),
    path('create_portfolio', views.create_portfolio),
    path('<int:pk>/portfolio_view_detail/',views.portfolio_view_detail),
    path('projects/create_project',views.create_project),
    path('projects/image_handler',views.image_handler),
    path('projects/project_view_detail/<int:pk>', views.project_view_detail)

]

