from django.db.models import Q

from netbox.filtersets import NetBoxModelFilterSet

from ocp_project_plugin.models import OCPProject


class OCPProjectFilter(NetBoxModelFilterSet):
    class Meta:
        model = OCPProject
        fields = ['name', 'description', 'display_name', 'project_owner', 'customer', 'docu_url', 'workload',
                  'request']

    def search(self, queryset, name, value):
        """Perform the filtered search."""
        if not value.strip():
            return queryset
        qs_filter = (
            Q(name__icontains=value)
            | Q(description__icontains=value)
            | Q(display_name__icontains=value)
            | Q(docu_url__icontains=value)
            | Q(workload__icontains=value)
            | Q(request__icontains=value)
        )
        return queryset.filter(qs_filter)
