from extras.plugins import PluginMenuButton, PluginMenuItem
from extras.plugins import PluginMenu
from utilities.choices import ButtonColorChoices

app_environment_menu_item = PluginMenuItem(
    link="plugins:ocp_project_plugin:appenvironment_list",
    link_text="App Environment",
    permissions=["ocp_project_plugin.appenvironment_view"],
    buttons=(
        PluginMenuButton(
            "plugins:ocp_project_plugin:appenvironment_add",
            "Add",
            "mdi mdi-plus-thick",
            ButtonColorChoices.GREEN,
            permissions=["ocp_project_plugin.add_appenvironment"],
        ),
        PluginMenuButton(
            "plugins:ocp_project_plugin:appenvironment_import",
            "Import",
            "mdi mdi-upload",
            ButtonColorChoices.CYAN,
            permissions=["ocp_project_plugin.add_appenvironment"],
        ),
    ),
)

ocp_project_menu_item = PluginMenuItem(
    link="plugins:ocp_project_plugin:ocpproject_list",
    link_text="OCP Project",
    permissions=["ocp_project_plugin.ocpproject_view"],
    buttons=(
        PluginMenuButton(
            "plugins:ocp_project_plugin:ocpproject_add",
            "Add",
            "mdi mdi-plus-thick",
            ButtonColorChoices.GREEN,
            permissions=["ocp_project_plugin.add_ocpproject"],
        ),
        PluginMenuButton(
            "plugins:ocp_project_plugin:ocpproject_import",
            "Import",
            "mdi mdi-upload",
            ButtonColorChoices.CYAN,
            permissions=["ocp_project_plugin.add_ocpproject"],
        ),
    ),
)

menu = PluginMenu(
    label="OCP Projects",
    groups=(
        (
            "General Configuration",
            (
                app_environment_menu_item,
                ocp_project_menu_item,
            ),
        ),
    ),
    icon_class="mdi mdi-apps",
)
