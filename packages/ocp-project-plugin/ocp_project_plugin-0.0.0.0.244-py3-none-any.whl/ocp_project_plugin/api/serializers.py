from rest_framework.serializers import HyperlinkedIdentityField

from netbox.api.serializers import NetBoxModelSerializer
from ocp_project_plugin.api.nested_serializers import NestedOCPProjectSerializer
from ocp_project_plugin.models import AppEnvironment, OCPProject
from tenancy.api.nested_serializers import NestedTenantSerializer, NestedContactSerializer


class AppEnvironmentSerializer(NetBoxModelSerializer):
    url = HyperlinkedIdentityField(view_name="plugins-api:ocp_project_plugin-api:appenvironment-detail")
    ocp_project = NestedOCPProjectSerializer()

    class Meta:
        model = AppEnvironment
        fields = ["url", "id", "cluster_env", "app_env", "mtls", "repo", "branch", "access_token", "path", "egress_ip", "deployment_kind",
                  "monitoring", "postgres_monitoring", "ocp_project", "requests_cpu", "requests_memory",
                  "limits_cpu", "limits_memory", "created", "last_updated", "custom_fields"]


class OCPProjectSerializer(NetBoxModelSerializer):
    url = HyperlinkedIdentityField(view_name="plugins-api:ocp_project_plugin-api:ocpproject-detail")
    customer = NestedTenantSerializer()
    project_owner = NestedContactSerializer()

    class Meta:
        model = OCPProject
        fields = ["url", "id", "name", "description", "display_name", "project_owner", "customer", "docu_url",
                  "workload", "request", "created", "last_updated", "custom_fields"]
