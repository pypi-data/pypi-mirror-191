from django.forms import (
    CharField,
    BooleanField, PasswordInput, ModelChoiceField,
)

from ipam.models import Prefix, IPAddress
from netbox.forms import (
    NetBoxModelBulkEditForm,
    NetBoxModelFilterSetForm,
    NetBoxModelImportForm,
    NetBoxModelForm,
)
from ocp_project_plugin.models import AppEnvironment, OCPProject
from utilities.forms import DynamicModelChoiceField, APISelectMultiple, CSVModelChoiceField


class AppEnvironmentAddForm(NetBoxModelForm):
    """Form for creating a new App Environment object."""
    ocp_project = DynamicModelChoiceField(
        queryset=OCPProject.objects.all(),
        label="OCP Project",
        help_text="Choose the ocp project e.g. web shop",
    )
    egress_ip = DynamicModelChoiceField(
        queryset=IPAddress.objects.all(),
        #queryset=Prefix.get_child_ips(Prefix.objects.get(prefix='10.190.1.64/26')),
        #queryset=IPAddress.objects.all(),
        label="Egress IP",
        help_text="Select your egress ip",
        widget=APISelectMultiple(
            api_url='/api/ipam/ip-addresses/?q=&parent=10.190.1.64/26',
        ),
        required=False
    )

    fieldsets = (
        ('OCP Project', ['ocp_project']),
        ('Environment', ('cluster_env', 'app_env')),
        ('Deployment', ('repo', 'branch', 'access_token', 'path', 'deployment_kind')),
        ('Monitoring', ('monitoring', 'postgres_monitoring')),
        ('Resources', ('limits_cpu', 'limits_memory', 'requests_cpu', 'requests_memory')),
        ('Additional Config', ('mtls', 'egress_ip')),
    )

    class Meta:
        model = AppEnvironment

        fields = ["access_token", "cluster_env", "app_env", "mtls", "repo", "branch", "path", "egress_ip", "deployment_kind", "monitoring",
                  "postgres_monitoring", "ocp_project", "requests_cpu", "requests_memory", "limits_cpu",
                  "limits_memory"]

        widgets = {
            'access_token': PasswordInput(),
        }


class AppEnvironmentEditForm(NetBoxModelForm):
    """Form for creating a new App Environment object."""
    ocp_project = DynamicModelChoiceField(
        queryset=OCPProject.objects.all(),
        label="OCP Project",
        help_text="Choose the ocp project e.g. web shop",
        disabled=True
    )
    egress_ip = DynamicModelChoiceField(
        queryset=IPAddress.objects.all(),
        label="Egress IP",
        help_text="Select your egress ip",
        widget=APISelectMultiple(
            api_url='/api/ipam/ip-addresses/?q=&parent=10.190.1.64/26',
        ),
        required = False
    )

    fieldsets = (
        ('OCP Project', ['ocp_project']),
        ('Environment', ('cluster_env', 'app_env')),
        ('Deployment', ('repo', 'branch', 'access_token', 'path', 'deployment_kind')),
        ('Monitoring', ('monitoring', 'postgres_monitoring')),
        ('Resources', ('limits_cpu', 'limits_memory', 'requests_cpu', 'requests_memory')),
        ('Additional Config', ('mtls', 'egress_ip')),
    )

    class Meta:
        model = AppEnvironment

        fields = ["access_token", "cluster_env", "app_env", "mtls", "repo", "branch", "path", "egress_ip", "deployment_kind", "monitoring",
                  "postgres_monitoring", "ocp_project", "requests_cpu", "requests_memory", "limits_cpu",
                  "limits_memory"]

        widgets = {
            'access_token': PasswordInput(),
        }


class AppEnvironmentFilterForm(NetBoxModelFilterSetForm):
    """Form for filtering App Environment instances."""

    model = AppEnvironment

    app_env = CharField(
        required=False,
        label="App Env",
        help_text="The app Env String used for creating the namespace e.g. tst",
    )
    mtls = BooleanField(
        required=False,
        label="MTLS",
        help_text="Enable if mtls should be used",
    )
    repo = CharField(
        required=False,
        label="Git Repository",
        help_text="Path of git Repository, don't forget the .git at the end e.g. "
                  "https://gitlab.com/example/example-deployment-manifests.git",
    )
    branch = CharField(
        required=False,
        label="Git Branch",
        help_text="The git Branch of the Repository e.g. main"
    )
    path = CharField(
        required=False,
        label="Git Path",
        help_text="Path of the deployment files e.g. overlays/tst"
    )
    egress_ip = CharField(
        required=False,
        label="Egress IP",
        help_text="The egress IP e.g. 10.10.10.10"
    )
    monitoring = BooleanField(
        required=False,
        label="Monitoring",
        help_text="Enable if monitoring should be used",
    )
    postgres_monitoring = BooleanField(
        required=False,
        label="Postgres Monitoring",
        help_text="Enable if postgres monitoring should be used",
    )


class AppEnvironmentImportForm(NetBoxModelImportForm):
    cluster_env = CharField(
        label="App Env",
        help_text="The app Env String used for creating the namespace e.g. tst",
    )
    app_env = CharField(
        label="App Env",
        help_text="The app Env String used for creating the namespace e.g. tst",
    )
    mtls = BooleanField(
        required=False,
        label="MTLS",
        help_text="Enable if mtls should be used",
    )
    repo = CharField(
        label="Git Repository",
        help_text="Path of git Repository, don't forget the .git at the end e.g. "
                  "https://gitlab.com/example/example-deployment-manifests.git",
    )
    branch = CharField(
        label="Git Branch",
        help_text="The git Branch of the Repository e.g. main"
    )
    path = CharField(
        label="Git Path",
        help_text="Path of the deployment files e.g. overlays/tst"
    )
    egress_ip = CharField(
        required=False,
        label="Egress IP",
        help_text="The egress IP e.g. 10.10.10.10"
    )
    monitoring = BooleanField(
        required=False,
        label="Monitoring",
        help_text="Enable if monitoring should be used",
    )
    postgres_monitoring = BooleanField(
        required=False,
        label="Postgres Monitoring",
        help_text="Enable if postgres monitoring should be used",
    )
    ocp_project = CSVModelChoiceField(
        queryset=OCPProject.objects.all(),
        to_field_name='name',
        help_text='Choose the ocpproject'
    )

    class Meta:
        model = AppEnvironment

        fields = ["cluster_env", "app_env", "mtls", "repo", "branch", "path", "egress_ip", "deployment_kind", "monitoring", "postgres_monitoring",
                  "ocp_project"]


class AppEnvironmentBulkEditForm(NetBoxModelBulkEditForm):
    model = AppEnvironment

    app_env = CharField(
        required=False,
        label="App Env",
        help_text="The app Env String used for creating the namespace e.g. tst",
    )
    mtls = BooleanField(
        required=False,
        label="MTLS",
        help_text="Enable if mtls should be used",
    )
    repo = CharField(
        required=False,
        label="Git Repository",
        help_text="Path of git Repository, don't forget the .git at the end e.g. "
                  "https://gitlab.com/example/example-deployment-manifests.git",
    )
    branch = CharField(
        required=False,
        label="Git Branch",
        help_text="The git Branch of the Repository e.g. main"
    )
    path = CharField(
        required=False,
        label="Git Path",
        help_text="Path of the deployment files e.g. overlays/tst"
    )
    egress_ip = CharField(
        required=False,
        label="Egress IP",
        help_text="The egress IP e.g. 10.10.10.10"
    )
    monitoring = BooleanField(
        required=False,
        label="Monitoring",
        help_text="Enable if monitoring should be used",
    )
    postgres_monitoring = BooleanField(
        required=False,
        label="Postgres Monitoring",
        help_text="Enable if postgres monitoring should be used",
    )
