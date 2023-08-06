# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ocp_project_plugin',
 'ocp_project_plugin.api',
 'ocp_project_plugin.fields',
 'ocp_project_plugin.filters',
 'ocp_project_plugin.forms',
 'ocp_project_plugin.migrations',
 'ocp_project_plugin.models',
 'ocp_project_plugin.tables',
 'ocp_project_plugin.templatetags',
 'ocp_project_plugin.views']

package_data = \
{'': ['*'],
 'ocp_project_plugin': ['docs/*',
                        'docs/models/ocp_project_plugin/*',
                        'site/*',
                        'site/css/*',
                        'site/fonts/*',
                        'site/img/*',
                        'site/js/*',
                        'site/models/ocp_project_plugin/appenvironment/*',
                        'site/search/*',
                        'static/models/ocpproject/*',
                        'templates/ocp_project_plugin/*',
                        'templates/ocp_project_plugin/app_environment/*',
                        'templates/ocp_project_plugin/ocp_project/*']}

setup_kwargs = {
    'name': 'ocp-project-plugin',
    'version': '0.0.0.0.248',
    'description': 'Netbox OCP Project Plugin',
    'long_description': '# General\n## Build Project\nTo build the project go to login in the pypi web ui and get your token. Add your token to the local pypi config.\n```\npoetry config pypi-token.pypi pypi-\n```\nAfter you made changes, change the version in the files pyproject.toml and netbox_storage/__init__.py\n\nNow you can build and publish the project.\n```\npoetry publish --build\n```\n\n## Use Project\nLink: https://github.com/netbox-community/netbox-docker/wiki/Using-Netbox-Plugins\n\ndocker-compose build --no-cache && docker-compose build --no-cache && docker-compose up -d\n\n\n## Directory structure\n\n```\n+- api - The API Classes, consitsts of Serializer, URL Mapper and Views\n+- filters - Filters of the models, the implementation of the method search, for searching\n+- forms - The ModelForm, ModelFilterForm, ModelImportForm, ModelBulkEditForm, the forms which will be displayed\n+- migrations - DB Django Migration steps\n+- tables - The ModelTable, which has the configuration on how the table looks like\n+- templates\n  +- netbox_storage - The detail view of each model\n    +- drive - The template content of drive, with base and partition model\n    +- inc - The template content box in the Virtual Machine Model\n    +- partition - The template content of partition, with base and physicalvolume model\n    +- physicalvolume - The template content of physicalvolume with base and linuxvolume model\n    +- volumegroup - The template content of volumegroup with base, logicalvolume and physicalvolume\n+- views - PhysicalvolumeListView, PhysicalvolumeView, PhysicalvolumeEditView, PhysicalvolumeDeleteView, \n           PhysicalvolumeBulkImportView, PhysicalvolumeBulkEditView, PhysicalvolumeBulkDeleteView\n```\n## ERM\n\n![The ERM of the Project](documents/erm.jpg?raw=true "ERM Diagram")\n\n## Queues / Worker\n\n### 1. Job - add_project\n1. Git Repo pullen\n2. Überprüfen ob es einen Branch mit dem Ticket Namen schon gibt\n3. Neuer Branch erstellen mit dem Ticket Namen\n4. Secrets entschlüsseln\n5. OCPPRoject/AppEnvironment Model Daten in yaml konvertieren\n6. YAML Daten dem values.yaml anfügen\n7. Secrets der Secrets Datei anfügen\n8. Secret verschlüsseln\n9. Mergen\n\n',
    'author': 'Tim Rhomberg',
    'author_email': 'timrhomberg@hotmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
