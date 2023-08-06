from rest_framework import serializers

from netbox.api.serializers import WritableNestedSerializer
from ocp_project_plugin.models import AppEnvironment, OCPProject


#
# App Environment
#

class NestedAppEnvironmentSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:ocp_project_plugin-api:appenvironment-detail"
    )

    class Meta:
        model = AppEnvironment
        fields = ["id", "url", "display", "app_env"]


#
# OCP Project
#
class NestedOCPProjectSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:ocp_project_plugin-api:ocpproject-detail"
    )

    class Meta:
        model = OCPProject
        fields = ["id", "url", "display", "name"]
