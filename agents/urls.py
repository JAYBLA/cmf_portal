from django.urls import path

from . import views

app_name = "agents"

urlpatterns = [
    # =====================================
    # CLEARING AGENTS
    # =====================================
    path("", views.clearing_agent_list, name="clearing_agent_list"),
    path("create/", views.clearing_agent_create, name="create"),
    path("<int:pk>/update/", views.clearing_agent_update, name="update"),
    path("<int:pk>/delete/", views.clearing_agent_delete, name="delete"),
    path("table/", views.clearing_agent_table, name="clearing_agent_table"),
]
