from django.urls import path

from netbox.views.generic import ObjectChangeLogView

from ocp_project_plugin.models import AppEnvironment, OCPProject
from ocp_project_plugin.views import (
    # App Environment Views
    AppEnvironmentListView,
    AppEnvironmentView,
    AppEnvironmentEditView,
    AppEnvironmentDeleteView,
    AppEnvironmentBulkImportView,
    AppEnvironmentBulkEditView,
    AppEnvironmentBulkDeleteView,
    # OCP Project Views
    OCPProjectListView,
    OCPProjectView,
    OCPProjectEditView,
    OCPProjectDeleteView,
    OCPProjectBulkImportView,
    OCPProjectBulkEditView,
    OCPProjectBulkDeleteView, AppEnvironmentAddView,
)

app_name = "ocp_project_plugin"

urlpatterns = [
    #
    # App Environment urls
    #
    path("appenvironment/", AppEnvironmentListView.as_view(), name="appenvironment_list"),
    path("appenvironment/add/", AppEnvironmentAddView.as_view(), name="appenvironment_add"),
    path("appenvironment/import/", AppEnvironmentBulkImportView.as_view(), name="appenvironment_import"),
    path("appenvironment/edit/", AppEnvironmentBulkEditView.as_view(), name="appenvironment_bulk_edit"),
    path("appenvironment/delete/", AppEnvironmentBulkDeleteView.as_view(), name="appenvironment_bulk_delete"),
    path("appenvironment/<int:pk>/", AppEnvironmentView.as_view(), name="appenvironment"),
    path("appenvironment/<int:pk>/edit/", AppEnvironmentEditView.as_view(), name="appenvironment_edit"),
    path("appenvironment/<int:pk>/delete/", AppEnvironmentDeleteView.as_view(), name="appenvironment_delete"),
    path(
        "appenvironment/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="appenvironment_changelog",
        kwargs={"model": AppEnvironment},
    ),
    #
    # OCP Project urls
    #
    path("ocpproject/", OCPProjectListView.as_view(), name="ocpproject_list"),
    path("ocpproject/add/", OCPProjectEditView.as_view(), name="ocpproject_add"),
    path("ocpproject/import/", OCPProjectBulkImportView.as_view(), name="ocpproject_import"),
    path("ocpproject/edit/", OCPProjectBulkEditView.as_view(), name="ocpproject_bulk_edit"),
    path("ocpproject/delete/", OCPProjectBulkDeleteView.as_view(), name="ocpproject_bulk_delete"),
    path("ocpproject/<int:pk>/", OCPProjectView.as_view(), name="ocpproject"),
    path("ocpproject/<int:pk>/edit/", OCPProjectEditView.as_view(), name="ocpproject_edit"),
    path("ocpproject/<int:pk>/delete/", OCPProjectDeleteView.as_view(), name="ocpproject_delete"),
    path(
        "ocpproject/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="ocpproject_changelog",
        kwargs={"model": OCPProject},
    ),
]
