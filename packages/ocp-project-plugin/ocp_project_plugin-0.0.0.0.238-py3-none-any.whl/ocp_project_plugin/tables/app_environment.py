import django_tables2 as tables

from netbox.tables import (
    NetBoxTable,
    ToggleColumn,
)

from ocp_project_plugin.models import AppEnvironment


class AppEnvironmentTable(NetBoxTable):
    """Table for displaying App Environment objects."""

    pk = ToggleColumn()
    app_env = tables.Column(
        linkify=True
    )
    cluster_env = tables.Column(
        linkify=True
    )
    repo = tables.Column(
        linkify=True
    )
    branch = tables.Column(
        linkify=True
    )
    ocp_project = tables.Column(
        linkify=True
    )

    class Meta(NetBoxTable.Meta):
        model = AppEnvironment

        fields = ["pk", "cluster_env", "app_env", "mtls", "repo", "branch", "path", "egress_ip", "deployment_kind",
                  "monitoring", "postgres_monitoring", "ocp_project", "requests_cpu", "requests_memory", "limits_cpu",
                  "limits_memory"]

        default_columns = ["cluster_env", "app_env", "mtls", "repo", "branch", "path", "deployment_kind",
                           "monitoring", "postgres_monitoring", "ocp_project"]
