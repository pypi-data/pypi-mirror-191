from django.db import migrations, models
import utilities.json


class Migration(migrations.Migration):
    initial = True

    operations = [
        migrations.CreateModel(
            name="OCPProject",
            fields=[
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                (
                    "custom_field_data",
                    models.JSONField(
                        blank=True,
                        default=dict,
                        encoder=utilities.json.CustomFieldJSONEncoder
                    ),
                ),
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=30)),
                ("description", models.CharField(max_length=150)),
                ("display_name", models.CharField(max_length=50)),
                ("project_owner", models.ForeignKey(on_delete=models.deletion.PROTECT, related_name="ocp_project_owner",
                                                    to="tenancy.Contact")),
                ("customer",
                 models.ForeignKey(on_delete=models.deletion.PROTECT, related_name="ocp_project_tenant",
                                   to="tenancy.Tenant")),
                ("docu_url", models.CharField(max_length=255)),
                ("workload", models.CharField(max_length=255)),
                ("request", models.CharField(max_length=255))
            ],
            options={
                "ordering": ("name", "description", "display_name", "project_owner", "customer", "url", "workload",
                             "request"),
            },
        ),
        migrations.CreateModel(
            name="AppEnvironment",
            fields=[
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                (
                    "custom_field_data",
                    models.JSONField(
                        blank=True,
                        default=dict,
                        encoder=utilities.json.CustomFieldJSONEncoder
                    ),
                ),
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("cluster_env", models.CharField(max_length=3)),
                ("app_env", models.CharField(max_length=20)),
                ("mtls", models.BooleanField()),
                ("repo", models.CharField(max_length=255)),
                ("branch", models.CharField(max_length=20)),
                ("access_token", models.CharField(max_length=100)),
                ("path", models.CharField(max_length=20)),
                ("egress_ip",
                 models.OneToOneField(blank=True, null=True, on_delete=models.deletion.SET_NULL,
                                      related_name='app_env_egress_ip', to='ipam.ipaddress')),
                ("deployment_kind", models.CharField(max_length=20)),
                ("monitoring", models.BooleanField()),
                ("postgres_monitoring", models.BooleanField()),
                ("ocp_project",
                 models.ForeignKey(on_delete=models.deletion.CASCADE, related_name="app_env_ocp_project",
                                   to="ocp_project_plugin.OCPProject")),
                ("requests_cpu", models.DecimalField(max_digits=4, decimal_places=2, null=True)),
                ("requests_memory", models.CharField(max_length=5, null=True)),
                ("limits_cpu", models.DecimalField(max_digits=4, decimal_places=2, null=True)),
                ("limits_memory", models.CharField(max_length=5, null=True)),
            ],
            options={
                "ordering": ["cluster_env", "app_env", "mtls", "repo", "branch", "path", "egress_ip", "deployment_kind",
                             "monitoring", "postgres_monitoring", "ocp_project", "requests_cpu",
                             "requests_memory", "limits_cpu", "limits_memory"],
            },
        ),
    ]
