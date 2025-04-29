from django.contrib import admin
from django.urls import path,include
from . import views
from .views import summary_table
from .views import facebook, display_excel  # ✅ Use the correct function name
from .views import summary_table

urlpatterns = [
    path('facebook/', facebook, name='facebook'),
    path('excel/', display_excel, name='display_excel'),
    path('summary/', summary_table, name='summary_table'),
    path('fb_user_searched/', views.fb_user_searched, name='fb_user_searched'),
    path('messages/', views.log_session_visits, name='fb_messages'),
    path('conversation/', views.conversation, name='fb_conversation'),
    path('download_report/', views.download_report, name='download_report'),
    path('download/<str:filename>/', views.download_file, name='download_file'),
]