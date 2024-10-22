from django.urls import path
from . import views

app_name = 'clients'
urlpatterns = [
    path('',views.clients_list,name='list'),
    path('<int:pk>/',views.clients_detail,name='detail'),
    path('add/',views.clients_add,name='add'),
    path('<int:pk>/delete_client/',views.clients_delete,name='delete'),
    path('<int:pk>/edit_client/',views.clients_edit,name='edit'),
    path('<int:pk>/add-comment/',views.clients_detail,name='add_comment'),
    path('export/',views.client_export,name='export'),
]