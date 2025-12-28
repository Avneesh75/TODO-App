from django.urls import path
from .views import (
    task_api,
    task_detail_api,
    task_list_view,
    task_create_view,
    task_update_api,
    task_delete_api,
)

urlpatterns = [
    # UI pages
    path("", task_list_view, name="task_list"),
    path("add/", task_create_view, name="task_create"),

    # API endpoints
    path("api/tasks/", task_api, name="task_list_create"),
    path("api/tasks/<int:task_id>/", task_detail_api, name="task_detail"),
    path("api/tasks/<int:task_id>/update/", task_update_api, name="task_update"),
    path("api/tasks/<int:task_id>/delete/", task_delete_api, name="task_delete"),
]
