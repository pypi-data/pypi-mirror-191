from ocp_project_plugin.models import AppEnvironment, OCPProject
from netbox.search import SearchIndex, register_search


@register_search
class OCPProjectIndex(SearchIndex):
    model = OCPProject
    fields = (
        ('name', 100),
        ('description', 100),
        ('display_name', 100),
        ('project_owner', 100),
        ('customer', 100),
        ('docu_url', 100),
        ('workload', 100),
        ('request', 100),
    )


@register_search
class AppEnvironmentIndex(SearchIndex):
    model = AppEnvironment
    fields = (
        ('cluster_env', 100),
        ('app_env', 100),
        ('mtls', 100),
        ('repo', 100),
        ('branch', 100),
        ('path', 100),
        ('egress_ip', 100),
        ('deployment_kind', 100),
        ('monitoring', 100),
        ('postgres_monitoring', 100),
        ('ocp_project', 100),
        ('requests_cpu', 100),
        ('requests_memory', 100),
        ('limits_cpu', 100),
        ('limits_memory', 100),
    )
