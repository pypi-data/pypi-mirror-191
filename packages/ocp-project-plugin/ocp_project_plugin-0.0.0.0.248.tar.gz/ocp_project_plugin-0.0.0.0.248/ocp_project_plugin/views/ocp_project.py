from decimal import Decimal

from django.db.models import DecimalField

from netbox import settings
from netbox.views.generic import ObjectView, ObjectListView, ObjectEditView, ObjectDeleteView, BulkImportView, \
    BulkEditView, BulkDeleteView
from ocp_project_plugin.filters import OCPProjectFilter
from ocp_project_plugin.forms import (
    OCPProjectImportForm,
    OCPProjectFilterForm,
    OCPProjectForm,
    OCPProjectBulkEditForm
)
from ocp_project_plugin.models import OCPProject, AppEnvironment
from ocp_project_plugin.tables import OCPProjectTable, AppEnvironmentTable
from utilities.views import register_model_view

PLUGIN_SETTINGS = settings.PLUGINS_CONFIG.get('ocp_project_plugin', dict())
CPU_COST = PLUGIN_SETTINGS.get('cpu_cost', '')
MEMORY_COST = PLUGIN_SETTINGS.get('memory_cost', '')
STORAGE_COST = PLUGIN_SETTINGS.get('storage_cost', '')


class OCPProjectListView(ObjectListView):
    queryset = OCPProject.objects.all()
    filterset = OCPProjectFilter
    filterset_form = OCPProjectFilterForm
    table = OCPProjectTable


class OCPProjectEditView(ObjectEditView):
    """View for editing OCP Project instance."""

    queryset = OCPProject.objects.all()
    form = OCPProjectForm
    default_return_url = "plugins:ocp_project_plugin:ocpproject_list"


class OCPProjectDeleteView(ObjectDeleteView):
    queryset = OCPProject.objects.all()
    default_return_url = "plugins:ocp_project_plugin:ocpproject_list"


class OCPProjectBulkImportView(BulkImportView):
    queryset = OCPProject.objects.all()
    model_form = OCPProjectImportForm
    table = OCPProjectTable
    default_return_url = "plugins:ocp_project_plugin:ocpproject_list"


class OCPProjectBulkEditView(BulkEditView):
    queryset = OCPProject.objects.all()
    filterset = OCPProjectFilter
    table = OCPProjectTable
    form = OCPProjectBulkEditForm


class OCPProjectBulkDeleteView(BulkDeleteView):
    queryset = OCPProject.objects.all()
    table = OCPProjectTable


@register_model_view(OCPProject)
class OCPProjectView(ObjectView):
    template_name = 'ocp_project_plugin/ocp_project/ocp_project.html'
    queryset = OCPProject.objects.all()

    def get_extra_context(self, request, instance):
        app_environment_assignments = AppEnvironment.objects.restrict(request.user, 'view').filter(
            ocp_project=instance
        )
        assignments_table = AppEnvironmentTable(app_environment_assignments, user=request.user)
        assignments_table.configure(request)

        total_cpu = 0
        total_memory = 0
        total_storage = 0
        total_cpu_cost = 0
        total_memory_cost = 0
        total_storage_cost = 0

        for app_env in app_environment_assignments:
            if app_env.limits_cpu is not None:
                total_cpu = + DecimalField().to_python(app_env.limits_cpu)

        for app_env in app_environment_assignments:
            total_memory = + app_env.get_limits_memory_gi()
            # total_cpu_cost = + app_env.calculate_cpu_cost()
            # print(app_env.calculate_memory_cost())

        total_cpu_cost = Decimal(CPU_COST) * Decimal(total_cpu)
        total_memory_cost = Decimal(MEMORY_COST) * Decimal(total_memory)
        total_cost = total_cpu_cost + total_memory_cost + total_storage_cost

        return {
            'assignments_table': assignments_table,
            'assignment_count': AppEnvironment.objects.filter(ocp_project=instance).count(),
            'app_env_list': AppEnvironment.objects.filter(ocp_project=instance),
            'total_cpu': total_cpu,
            'total_memory': total_memory,
            'total_storage': total_storage,
            'total_cpu_cost': total_cpu_cost,
            'total_memory_cost': total_memory_cost,
            'total_storage_cost': total_storage_cost,
            'total_cost': total_cost
        }
