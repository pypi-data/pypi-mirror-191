import django_tables2 as tables

from netbox.tables import (
    NetBoxTable,
    ToggleColumn,
)

from ocp_project_plugin.models import OCPProject


class OCPProjectTable(NetBoxTable):
    """Table for displaying OCP Project objects."""

    pk = ToggleColumn()
    name = tables.Column(
        linkify=True
    )
    description = tables.Column(
        linkify=True
    )
    display_name = tables.Column(
        linkify=True
    )
    project_owner = tables.Column(
        linkify=True
    )
    customer = tables.Column(
        linkify=True
    )

    class Meta(NetBoxTable.Meta):
        model = OCPProject

        fields = ["pk", "name", "description", "display_name", "project_owner", "customer", "docu_url",
                  "workload", "request"]

        default_columns = ["name", "description", "display_name", "project_owner", "customer", "docu_url",
                           "workload", "request"]
