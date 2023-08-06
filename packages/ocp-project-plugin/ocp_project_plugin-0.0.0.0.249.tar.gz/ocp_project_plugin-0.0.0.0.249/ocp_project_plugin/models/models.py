from decimal import Decimal
from django.core.validators import RegexValidator
from django.db.models import CharField, BooleanField, ForeignKey, CASCADE, OneToOneField, SET_NULL, PROTECT, \
    DecimalField
from django.urls import reverse
from django_rq import get_queue

from netbox import settings
from ocp_project_plugin.choices import AppEnvironmentClusterEnvChoices, AppEnvironmentDeploymentKindChoices

from netbox.models import NetBoxModel
from tenancy.models import ContactAssignment, ContactRole

from django.contrib.contenttypes.models import ContentType

PLUGIN_SETTINGS = settings.PLUGINS_CONFIG.get('ocp_project_plugin', dict())
CPU_COST = PLUGIN_SETTINGS.get('cpu_cost', '')
MEMORY_COST = PLUGIN_SETTINGS.get('memory_cost', '')
STORAGE_COST = PLUGIN_SETTINGS.get('storage_cost', '')

memory_validator = RegexValidator(r"[1-9][0-9]*(Mi|Gi)$", "The input should contain only positive Number, which ends "
                                                          "with Mi (Megabyte) or Gi (Gigabyte)")

project_name_validator = RegexValidator(r"^([a-z]|[-]|[0-9]){1,30}$", "The input should contain only small letters,"
                                                                      " Numbers or - sign, it also should no exceed 30 "
                                                                      "Characters")

url_validator = RegexValidator(r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)",
                               "The url validation failed")


class OCPProject(NetBoxModel):
    name = CharField(
        max_length=30,
        verbose_name="OCP Project Name",
        help_text="The ocp project name e.g. web-shop",
        validators=[project_name_validator],
    )
    description = CharField(
        max_length=150,
        verbose_name="Description",
        help_text="The description of the project e.g. A web shop software",
    )
    display_name = CharField(
        max_length=50,
        verbose_name="Display name",
        help_text="Display Name of the project e.g. Web Shop Shopify"
    )
    project_owner = ForeignKey(
        to='tenancy.Contact',
        on_delete=PROTECT,
        related_name='ocp_project_owner',
    )
    customer = ForeignKey(
        to='tenancy.Tenant',
        on_delete=PROTECT,
        related_name='ocp_project_tenant',
    )
    docu_url = CharField(
        max_length=255,
        verbose_name="URL",
        help_text="The url of the project documentation e.g. https://confluence.com/space/project",
        validators=[url_validator],
    )
    workload = CharField(
        max_length=255,
        verbose_name="Workload",
        help_text="The workload contents e.g. Postgres DB, nginx",
    )
    request = CharField(
        max_length=255,
        verbose_name="Jira Request",
        help_text="The jira request id e.g. TICKET1234",
    )

    clone_fields = ["name", "description", "display_name", "project_owner", "customer", "docu_url", "workload",
                    "request"]

    class Meta:
        verbose_name = "OCP Project"
        ordering = ["name", "description", "display_name", "project_owner", "customer", "docu_url", "workload",
                    "request"]

    def __str__(self):
        return f"{self.name} ({self.display_name}-{self.customer})"

    def get_absolute_url(self):
        return reverse("plugins:ocp_project_plugin:ocpproject", kwargs={"pk": self.pk})

    @property
    def docs_url(self):
        return f'https://confluence.ti8m.ch/docs/models/OCPProject/'

    def save(self, *args, **kwargs):
        super(OCPProject, self).save(*args, **kwargs)
        project_owner_pk = ContactRole.objects.get(name='Project Owner').pk
        ocp_project_type_pk = ContentType.objects.get(app_label='ocp_project_plugin', model='ocpproject').pk

        count_assignment = ContactAssignment.objects.filter(object_id=self.pk).count()
        if count_assignment == 0:
            ContactAssignment.objects.create(object_id=self.pk,
                                             contact_id=self.project_owner.pk,
                                             content_type_id=ocp_project_type_pk,
                                             role_id=project_owner_pk)
        else:
            current_assignment = ContactAssignment.objects.get(object_id=self.pk, content_type_id=ocp_project_type_pk)
            print(current_assignment.contact)
            print(self.project_owner)
            print(*args)
            print(**kwargs)
            if current_assignment.contact == self.project_owner:
                print("Nothing changed in assignment")
            else:
                print("something changed in assignment")
                current_assignment.contact = self.project_owner
                current_assignment.save()

    def export_yaml_dict(self):
        yaml_object = {
            'name': self.name,
            'description': self.description,
            'displayName': self.display_name,
            'customer': self.customer.name,
            'owner': self.project_owner.name,
            'contact': self.project_owner.email,
            'workloads': self.workload,
            'request': self.request,
            'url': self.docu_url,
            'environments': {

            }
        }
        if len(self.get_app_env(AppEnvironmentClusterEnvChoices.CHOICE_DEV)) > 0:
            yaml_object['environments']['DEV'] = self.get_app_env(AppEnvironmentClusterEnvChoices.CHOICE_DEV)
        if len(self.get_app_env(AppEnvironmentClusterEnvChoices.CHOICE_TST)) > 0:
            yaml_object['environments']['TST'] = self.get_app_env(AppEnvironmentClusterEnvChoices.CHOICE_TST)
        if len(self.get_app_env(AppEnvironmentClusterEnvChoices.CHOICE_INT)) > 0:
            yaml_object['environments']['INT'] = self.get_app_env(AppEnvironmentClusterEnvChoices.CHOICE_INT)
        if len(self.get_app_env(AppEnvironmentClusterEnvChoices.CHOICE_PRD)) > 0:
            yaml_object['environments']['PRD'] = self.get_app_env(AppEnvironmentClusterEnvChoices.CHOICE_PRD)

        print(yaml_object)
        return yaml_object

    def get_app_env(self, app_env_choice):
        app_env_queryset = AppEnvironment.objects.filter(cluster_env=app_env_choice, ocp_project=self)

        app_env_list = []
        for app_env in app_env_queryset:
            # @TODO deployment kind
            app_env_list.append({
                'appEnv': app_env.app_env,
                'monitoring': app_env.monitoring,
                'postgresMonitoring': app_env.postgres_monitoring,
                'deployment': {
                    'repo': app_env.repo,
                    'branch': app_env.branch,
                    'path': app_env.path
                },
                'resourceQuota': {
                    'requests': {
                        'cpu': str(app_env.requests_cpu or ''),
                        'memory': app_env.requests_memory
                    },
                    'limits': {
                        'cpu': str(app_env.limits_cpu or ''),
                        'memory': app_env.limits_memory
                    }
                }
            })
        return app_env_list

    def count_app_environments(self):
        return AppEnvironment.objects.filter(OCPProject=self).count()

    def get_all_app_environments(self):
        return AppEnvironment.objects.filter(OCPProject=self)


class AppEnvironment(NetBoxModel):
    cluster_env = CharField(
        max_length=3,
        choices=AppEnvironmentClusterEnvChoices,
        default=AppEnvironmentClusterEnvChoices.CHOICE_TST,
        verbose_name="Cluster ENV",
        help_text="The Cluster Environment",
    )
    app_env = CharField(
        max_length=20,
        verbose_name="App ENV",
        help_text="The app Env String used for creating the namespace e.g. tst",
    )
    deployment_kind = CharField(
        max_length=20,
        choices=AppEnvironmentDeploymentKindChoices,
        default=AppEnvironmentDeploymentKindChoices.DEPLOYMENT_KIND_NORMAL,
        verbose_name="Deployment Kind",
        help_text="Choose the way how the deployment should work",
    )
    mtls = BooleanField(
        default=False,
        blank=False,
        verbose_name="MTLS",
        help_text="Enable if mtls should be used",
    )
    repo = CharField(
        max_length=255,
        verbose_name="Git Repository",
        help_text="Path of git Repository, don't forget the .git at the end e.g. "
                  "https://gitlab.com/example/example-deployment-manifests.git",
    )
    branch = CharField(
        max_length=20,
        verbose_name="Git Branch",
        help_text="The git Branch of the Repository e.g. main"
    )
    access_token = CharField(
        blank=True,
        max_length=100,
        verbose_name="Git Access Token",
        help_text="The access token of the tst git repo, int & prd are automatically provided"
    )
    path = CharField(
        max_length=100,
        verbose_name="Git Path",
        help_text="Path of the deployment files e.g. overlays/tst"
    )
    egress_ip = OneToOneField(
        to='ipam.IPAddress',
        on_delete=SET_NULL,
        related_name='app_env_egress_ip',
        blank=True,
        null=True,
        verbose_name='Egress IP'
    )
    monitoring = BooleanField(
        default=True,
        verbose_name="Monitoring",
        help_text="Enable if monitoring should be used",
    )
    postgres_monitoring = BooleanField(
        default=False,
        verbose_name="Postgres Monitoring",
        help_text="Enable if postgres monitoring should be used",
    )
    requests_cpu = DecimalField(
        max_digits=4,
        decimal_places=2,
        blank=True,
        verbose_name="CPU request",
        help_text="The CPU request value e.g. 1",
    )
    requests_memory = CharField(
        max_length=5,
        blank=True,
        verbose_name="Memory request",
        help_text="The memory value e.g. 200Mi or 1Gi",
        validators=[memory_validator],
    )
    limits_cpu = DecimalField(
        max_digits=4,
        decimal_places=2,
        blank=True,
        verbose_name="CPU Limit",
        help_text="The CPU request value e.g. 2",
    )
    limits_memory = CharField(
        max_length=5,
        blank=True,
        verbose_name="Memory Limit",
        help_text="The CPU memory value e.g. 400Mi or 2Gi",
        validators=[memory_validator],
    )
    ocp_project = ForeignKey(OCPProject, on_delete=CASCADE, related_name="app_env_ocp_project")

    clone_fields = ["access_token", "cluster_env", "app_env", "mtls", "repo", "branch", "path", "egress_ip",
                    "deployment_kind", "monitoring", "postgres_monitoring", "ocp_project", "requests_cpu",
                    "requests_memory", "limits_cpu", "limits_memory"]

    class Meta:
        ordering = ["access_token", "cluster_env", "app_env", "mtls", "repo", "branch", "path", "egress_ip",
                    "deployment_kind", "monitoring", "postgres_monitoring", "ocp_project", "requests_cpu",
                    "requests_memory", "limits_cpu", "limits_memory"]

    def __str__(self):
        return f"{self.cluster_env}-{self.app_env} ({self.repo}-{self.branch})"

    def get_absolute_url(self):
        return reverse("plugins:ocp_project_plugin:appenvironment", kwargs={"pk": self.pk})

    #@property
    #def docs_url(self):
    #    return f'https://confluence.ti8m.ch/docs/models/AppEnvironment/'

    def save(self, *args, **kwargs):
        yaml_object = self.ocp_project.export_yaml_dict()
        get_queue("default").enqueue("ocp_project_plugin.worker.sync_project", yaml_object)
        super(AppEnvironment, self).save(*args, **kwargs)

    def get_cluster_color(self):
        return AppEnvironmentClusterEnvChoices.colors.get(self.cluster_env)

    def get_limits_memory_gi(self):
        if self.limits_memory is '':
            return 0
        else:
            if str(self.limits_memory).endswith('Mi'):
                return float(str(self.limits_memory)[:-2]) / 1000
            else:
                return float(str(self.limits_memory)[:-2])

    def calculate_cpu_cost(self):
        return Decimal(CPU_COST) * DecimalField().to_python(self.limits_cpu)

    def calculate_memory_cost(self):
        if self.limits_memory is '':
            return '0'
        else:
            return int(MEMORY_COST) * float(str(self.limits_memory)[:-2])
