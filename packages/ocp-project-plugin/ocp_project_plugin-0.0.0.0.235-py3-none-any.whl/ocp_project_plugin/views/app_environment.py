from netbox.views.generic import ObjectView, ObjectListView, ObjectEditView, ObjectDeleteView, BulkImportView, \
    BulkEditView, BulkDeleteView

from ocp_project_plugin.filters import AppEnvironmentFilter
from ocp_project_plugin.forms import (
    AppEnvironmentImportForm,
    AppEnvironmentFilterForm,
    AppEnvironmentBulkEditForm, AppEnvironmentAddForm, AppEnvironmentEditForm
)
from ocp_project_plugin.models import AppEnvironment
from ocp_project_plugin.tables import AppEnvironmentTable


class AppEnvironmentListView(ObjectListView):
    queryset = AppEnvironment.objects.all()
    filterset = AppEnvironmentFilter
    filterset_form = AppEnvironmentFilterForm
    table = AppEnvironmentTable


class AppEnvironmentView(ObjectView):
    """Display App Environment details"""
    template_name = 'ocp_project_plugin/app_environment/app_environment.html'
    queryset = AppEnvironment.objects.all()


class AppEnvironmentAddView(ObjectEditView):
    """View for editing App Environment instance."""

    queryset = AppEnvironment.objects.all()
    form = AppEnvironmentAddForm
    default_return_url = "plugins:ocp_project_plugin:appenvironment_list"


class AppEnvironmentEditView(ObjectEditView):
    """View for editing App Environment instance."""

    queryset = AppEnvironment.objects.all()
    form = AppEnvironmentEditForm
    default_return_url = "plugins:ocp_project_plugin:appenvironment_list"


class AppEnvironmentDeleteView(ObjectDeleteView):
    queryset = AppEnvironment.objects.all()
    default_return_url = "plugins:ocp_project_plugin:appenvironment_list"


class AppEnvironmentBulkImportView(BulkImportView):
    queryset = AppEnvironment.objects.all()
    model_form = AppEnvironmentImportForm
    table = AppEnvironmentTable
    default_return_url = "plugins:ocp_project_plugin:appenvironment_list"


class AppEnvironmentBulkEditView(BulkEditView):
    queryset = AppEnvironment.objects.all()
    filterset = AppEnvironmentFilter
    table = AppEnvironmentTable
    form = AppEnvironmentBulkEditForm


class AppEnvironmentBulkDeleteView(BulkDeleteView):
    queryset = AppEnvironment.objects.all()
    table = AppEnvironmentTable
