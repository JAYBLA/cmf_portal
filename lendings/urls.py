from django.urls import path

from . import views

app_name = "lendings"

urlpatterns = [
    path("", views.lending_list, name="lending_list"),
    path("table/", views.lending_table, name="lending_table"),
    path("create/", views.lending_create, name="lending_create"),
    path("<int:pk>/update/", views.lending_update, name="lending_update"),
    path("<int:pk>/delete/", views.lending_delete, name="lending_delete"),
    path("<int:lending_id>/items/", views.item_list, name="item_list"),
    path("<int:lending_id>/items/table/", views.item_table, name="item_table"),
    path("<int:lending_id>/items/create/", views.item_create, name="item_create"),
    path("items/<int:pk>/update/", views.item_update, name="item_update"),
    path("items/<int:pk>/delete/", views.item_delete, name="item_delete"),
]
