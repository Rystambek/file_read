from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_file, name='upload_file'),
    path('files/<int:pk>/', views.file_detail, name='file_detail'),
    path('files/<int:pk>/delete/', views.delete_file, name='delete_file'),
    path('download/<int:pk>/<str:result_type>/', views.download_result, name='download_result'),
]
