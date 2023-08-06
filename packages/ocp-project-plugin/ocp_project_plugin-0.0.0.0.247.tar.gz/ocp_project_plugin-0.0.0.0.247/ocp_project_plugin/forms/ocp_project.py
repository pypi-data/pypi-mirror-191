from django.forms import (
    CharField,
)

from netbox.forms import (
    NetBoxModelBulkEditForm,
    NetBoxModelFilterSetForm,
    NetBoxModelImportForm,
    NetBoxModelForm,
)
from ocp_project_plugin.models import OCPProject
from tenancy.models import Tenant, Contact
from utilities.forms import DynamicModelChoiceField, CSVModelChoiceField


class OCPProjectForm(NetBoxModelForm):
    """Form for creating a new App Environment object."""
    project_owner = DynamicModelChoiceField(
        queryset=Contact.objects.all(),
        label='Project Owner',
        help_text='Choose the Project Owner'
    )
    customer = DynamicModelChoiceField(
        queryset=Tenant.objects.all(),
        label='Customer name',
        help_text='Choose the tenant',
    )

    fieldsets = (
        ('Create OCP Project', ['name', 'description', 'display_name', 'project_owner', 'customer', 'docu_url',
                                'workload', 'request']),
    )

    class Meta:
        model = OCPProject

        fields = ['name', 'description', 'display_name', 'project_owner', 'customer', 'docu_url', 'workload',
                  'request']


class OCPProjectFilterForm(NetBoxModelFilterSetForm):
    """Form for filtering App Environment instances."""

    model = OCPProject

    name = CharField(
        required=False,
        label='OCP Project Name',
        help_text='The ocp project name e.g. web-shop',
    )
    description = CharField(
        required=False,
        label='Description',
        help_text='The description of the project e.g. A web shop software',
    )
    display_name = CharField(
        required=False,
        label='Display name',
        help_text='Display Name of the project e.g. Web Shop Shopify'
    )
    project_owner = DynamicModelChoiceField(
        required=False,
        queryset=Contact.objects.all(),
        label='Project Owner',
        help_text='Choose the Project Owner'
    )
    customer = DynamicModelChoiceField(
        required=False,
        queryset=Tenant.objects.all(),
        label='Customer name',
        help_text='Choose the tenant',
    )
    docu_url = CharField(
        required=False,
        label='URL',
        help_text='The url of the project documentation',
    )
    workload = CharField(
        required=False,
        label='Workload',
        help_text='The workload contents e.g. Postgres DB, nginx',
    )
    request = CharField(
        required=False,
        label='Jira Request',
        help_text='The jira request id e.g. TICKET1234',
    )


class OCPProjectImportForm(NetBoxModelImportForm):
    name = CharField(
        label='OCP Project Name',
        help_text='The ocp project name e.g. web-shop',
    )
    description = CharField(
        label='Description',
        help_text='The description of the project e.g. A web shop software',
    )
    display_name = CharField(
        label='Display name',
        help_text='Display Name of the project e.g. Web Shop Shopify'
    )
    project_owner = CSVModelChoiceField(
        queryset=Contact.objects.all(),
        to_field_name='name',
        help_text='Choose the cutomser'
    )
    customer = CSVModelChoiceField(
        queryset=Tenant.objects.all(),
        to_field_name='name',
        help_text='Choose the tenant'
    )
    docu_url = CharField(
        label='URL',
        help_text='The url of the project documentation',
    )
    workload = CharField(
        label='Workload',
        help_text='The workload contents e.g. Postgres DB, nginx',
    )
    request = CharField(
        label='Jira Request',
        help_text='The jira request id e.g. TICKET1234',
    )

    class Meta:
        model = OCPProject

        fields = ['name', 'description', 'display_name', 'project_owner', 'customer', 'docu_url', 'workload',
                  'request']


class OCPProjectBulkEditForm(NetBoxModelBulkEditForm):
    model = OCPProject

    name = CharField(
        required=False,
        label='OCP Project Name',
        help_text='The ocp project name e.g. web-shop',
    )
    description = CharField(
        required=False,
        label='Description',
        help_text='The description of the project e.g. A web shop software',
    )
    display_name = CharField(
        required=False,
        label='Display name',
        help_text='Display Name of the project e.g. Web Shop Shopify'
    )
    project_owner = CharField(
        required=False,
        label='Owner',
        help_text='Choose the project owner'
    )
    customer = CharField(
        required=False,
        label='Customer name',
        help_text='Choose the tenant'
    )
    docu_url = CharField(
        required=False,
        label='URL',
        help_text='The url of the project documentation',
    )
    workload = CharField(
        required=False,
        label='Workload',
        help_text='The workload contents e.g. Postgres DB, nginx',
    )
    request = CharField(
        required=False,
        label='Jira Request',
        help_text='The jira request id e.g. TICKET1234',
    )
