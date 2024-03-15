from django.urls import path
from django.contrib.auth import views as auth_views
# from . import views

from .views import upload_document, document_list, add_owner, add_staff, user_login, home, logout, delete_document

urlpatterns = [
    path('',home, name='home'),
    path('upload/', upload_document, name='upload_document'),
    path('documents/', document_list, name='document_list'),
    path('add_owner/', add_owner, name='add_owner'),
    path('add_staff/', add_staff, name='add_staff'),
    path('login/', user_login, name='login'),
    path('accounts/login/', user_login, name='login'),
    path('logout/', logout, name='logout'),
    path('delete_document/<int:document_id>/', delete_document, name='delete_document'),

]
