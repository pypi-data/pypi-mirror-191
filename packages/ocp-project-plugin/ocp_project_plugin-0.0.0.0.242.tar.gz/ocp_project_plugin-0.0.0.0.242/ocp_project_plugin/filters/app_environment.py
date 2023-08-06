import django_filters
from django.db.models import Q

from netbox.filtersets import NetBoxModelFilterSet

from ocp_project_plugin.models import AppEnvironment, OCPProject


class AppEnvironmentFilter(NetBoxModelFilterSet):
    """Filter capabilities for App Environment instances."""
    ocp_project = django_filters.ModelMultipleChoiceFilter(
        field_name='ocp_project__name',
        queryset=OCPProject.objects.all(),
        to_field_name='name',
        label='OCP Projects (name)',
    )

    class Meta:
        model = AppEnvironment
        fields = ["access_token", "cluster_env", "app_env", "mtls", "repo", "branch", "path", "egress_ip",
                  "deployment_kind", "monitoring", "postgres_monitoring", "ocp_project", "requests_cpu",
                  "requests_memory", "limits_cpu", "limits_memory"]

    def search(self, queryset, name, value):
        """Perform the filtered search."""
        if not value.strip():
            return queryset
        qs_filter = (
            Q(app_env__icontains=value)
            | Q(mtls__icontains=value)
            | Q(repo__icontains=value)
            | Q(branch__icontains=value)
            | Q(path__icontains=value)
            | Q(egress_ip__icontains=value)
            | Q(deployment_kind__icontains=value)
            | Q(monitoring__icontains=value)
            | Q(postgres_monitoring__icontains=value)
            | Q(limits_cpu__icontains=value)
            | Q(limits_memory__icontains=value)
            | Q(requests_cpu__icontains=value)
            | Q(requests_memory__icontains=value)
        )
        return queryset.filter(qs_filter)
