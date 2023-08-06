from django import template
from django.conf import settings

from ipam.models import Prefix, IPAddress
from ocp_project_plugin.models import AppEnvironment

register = template.Library()

PLUGIN_SETTINGS = settings.PLUGINS_CONFIG.get('ocp_project_plugin', dict())
GITLAB_PROJECT_URL = PLUGIN_SETTINGS.get('gitlab_project_url', '')
JIRA_BROWSE_URL = PLUGIN_SETTINGS.get('jira_browse_url', '')
CPU_COST = PLUGIN_SETTINGS.get('cpu_cost', '')
MEMORY_COST = PLUGIN_SETTINGS.get('memory_cost', '')
STORAGE_COST = PLUGIN_SETTINGS.get('storage_cost', '')
OCP_TST_URL = PLUGIN_SETTINGS.get('ocp_tst_url', '')
OCP_DEV_URL = PLUGIN_SETTINGS.get('ocp_dev_url', '')
OCP_INT_URL = PLUGIN_SETTINGS.get('ocp_int_url', '')
OCP_PRD_URL = PLUGIN_SETTINGS.get('ocp_prd_url', '')
ARGOCD_TST_URL = PLUGIN_SETTINGS.get('argocd_tst_url', '')
ARGOCD_DEV_URL = PLUGIN_SETTINGS.get('argocd_dev_url', '')
ARGOCD_INT_URL = PLUGIN_SETTINGS.get('argocd_int_url', '')
ARGOCD_PRD_URL = PLUGIN_SETTINGS.get('argocd_prd_url', '')
PROMETHEUS_TST_URL = PLUGIN_SETTINGS.get('prometheus_tst_url', '')
PROMETHEUS_DEV_URL = PLUGIN_SETTINGS.get('prometheus_dev_url', '')
PROMETHEUS_INT_URL = PLUGIN_SETTINGS.get('prometheus_int_url', '')
PROMETHEUS_PRD_URL = PLUGIN_SETTINGS.get('prometheus_prd_url', '')
GRAFANA_TST_URL = PLUGIN_SETTINGS.get('grafana_tst_url', '')
GRAFANA_DEV_URL = PLUGIN_SETTINGS.get('grafana_dev_url', '')
GRAFANA_INT_URL = PLUGIN_SETTINGS.get('grafana_int_url', '')
GRAFANA_PRD_URL = PLUGIN_SETTINGS.get('grafana_prd_url', '')
KIBANA_TST_URL = PLUGIN_SETTINGS.get('kibana_tst_url', '')
KIBANA_DEV_URL = PLUGIN_SETTINGS.get('kibana_dev_url', '')
KIBANA_INT_URL = PLUGIN_SETTINGS.get('kibana_int_url', '')
KIBANA_PRD_URL = PLUGIN_SETTINGS.get('kibana_prd_url', '')


# settings value
@register.simple_tag
def jira_browse_url(ticket_id):
    return f"{JIRA_BROWSE_URL}{ticket_id}"


@register.simple_tag
def get_cpu_cost():
    return CPU_COST


@register.simple_tag
def calculate_cpu_cost(amount):
    if amount is '':
        return '-'
    else:
        return int(CPU_COST) * int(amount)


@register.simple_tag
def calculate_memory_cost(amount):
    if amount is '':
        return '-'
    else:
        if amount.endswith('Mi'):
            return int(MEMORY_COST) * float(str(amount)[:-2]) / 1000
        else:
            return int(MEMORY_COST) * float(str(amount)[:-2])


@register.simple_tag
def get_memory_cost():
    return MEMORY_COST


@register.simple_tag
def calculate_storage_cost(amount):
    if amount is '':
        return '0'
    else:
        return int(STORAGE_COST) * int(amount)


@register.simple_tag
def get_storage_cost():
    return STORAGE_COST


@register.simple_tag
def calculate_total_cost(cpu_amount, memory_amount, storage_amount):
    print(cpu_amount)
    print(memory_amount)
    if cpu_amount is '' or memory_amount is '':
        return '0'
    else:
        return calculate_cpu_cost(cpu_amount) + calculate_memory_cost(memory_amount) + 0


@register.simple_tag
def get_ocp_resource_quota_url(cluster_env, app_env, ocp_project_name):
    suffix = '/k8s/ns/' + ocp_project_name + '-' + app_env + '/resourcequotas'
    if cluster_env == 'TST':
        return OCP_TST_URL + suffix
    if cluster_env == 'DEV':
        return OCP_DEV_URL + suffix
    if cluster_env == 'INT':
        return OCP_INT_URL + suffix
    if cluster_env == 'PRD':
        return OCP_PRD_URL + suffix


@register.simple_tag
def get_url(app, cluster_env):
    print("1")
    print(Prefix.objects.get(prefix='10.190.1.64/26'))
    print("2")
    print(Prefix.get_child_ips(Prefix.objects.get(prefix='10.190.1.64/26')))
    print("3")
    print(IPAddress.objects.filter(address__net_host_contained='10.190.1.64/26'))
    print("4")
    if cluster_env == 'TST':
        if app == 'argocd':
            return ARGOCD_TST_URL
        if app == 'grafana':
            return GRAFANA_TST_URL
        if app == 'ocp':
            return OCP_TST_URL
        if app == 'prometheus':
            return PROMETHEUS_TST_URL
        if app == 'kibana':
            return KIBANA_TST_URL
    if cluster_env == 'DEV':
        if app == 'argocd':
            return ARGOCD_DEV_URL
        if app == 'grafana':
            return GRAFANA_DEV_URL
        if app == 'ocp':
            return OCP_DEV_URL
        if app == 'prometheus':
            return PROMETHEUS_DEV_URL
        if app == 'kibana':
            return KIBANA_DEV_URL
    if cluster_env == 'INT':
        if app == 'argocd':
            return ARGOCD_DEV_URL
        if app == 'grafana':
            return GRAFANA_DEV_URL
        if app == 'ocp':
            return OCP_DEV_URL
        if app == 'prometheus':
            return PROMETHEUS_DEV_URL
        if app == 'kibana':
            return KIBANA_DEV_URL
    if cluster_env == 'PRD':
        if app == 'argocd':
            return ARGOCD_DEV_URL
        if app == 'grafana':
            return GRAFANA_DEV_URL
        if app == 'ocp':
            return OCP_DEV_URL
        if app == 'prometheus':
            return PROMETHEUS_DEV_URL
        if app == 'kibana':
            return KIBANA_DEV_URL


@register.simple_tag
def count_app_environments(object_id):
    return AppEnvironment.objects.filter(ocp_project=object_id).count()


@register.simple_tag
def get_all_app_environments(object_id):
    return AppEnvironment.objects.filter(ocp_project=object_id)
