from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.custom_login, name='login'),
   path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('receipt-list/', views.receipt_list, name='receipt_list'),
    path('add/', views.receipt_add, name='receipt_add'),
    path('edit/<str:pk>/', views.receipt_edit, name='receipt_edit'),
    path('month-report/', views.month_report, name='month_report'),
    path('year-report/', views.year_report, name='year_report'),
    path('receipt/<str:pk>/remove/', views.receipt_remove, name='receipt_remove'),
]