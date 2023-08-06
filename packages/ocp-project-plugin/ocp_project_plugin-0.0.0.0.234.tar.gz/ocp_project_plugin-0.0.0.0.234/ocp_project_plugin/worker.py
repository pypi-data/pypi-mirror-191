import yaml
from django.conf import settings
from django_rq import job
from git import Repo

PLUGIN_SETTINGS = settings.PLUGINS_CONFIG.get('ocp_project_plugin', dict())
GITLAB_PROJECT_URL = PLUGIN_SETTINGS.get('gitlab_project_url', '')
VALUES_PATH = PLUGIN_SETTINGS.get('jira_browse_url', '')

"""
1. Git Repo pullen
2. Überprüfen ob es einen Branch mit dem Ticket Namen schon gibt
3. Neuer Branch erstellen mit dem Ticket Namen
4. Secrets entschlüsseln
5. OCP PRoject/App Environment Model Daten in yaml konvertieren
6. Überprüfen ob OCP Project & App Environment schon existiern in values.yaml
7. YAML Daten dem values.yaml anfügen oder updaten
8. Secrets der Secrets Datei anfügen oder updaten
9. Secret verschlüsseln
10. Mergen
"""


@job("default")
def sync_project(yaml_object):
    print("Step 1: Print new yaml Object")
    print(yaml_object)
    try:
        print("Step 2: Start cloning git repository")
        repo_instance = Repo.clone_from(GITLAB_PROJECT_URL, '/repo/project-repo')
        print(f"Step 2.1: Cloning finished, {repo_instance}")
    except:
        print("Step: 2: Cloning failed")

    request = yaml_object['request']
    print(f"Step 3: Check if int this repository a branch with the name {request} already exists.")
    repo = Repo('/repo/project-repo')
    remote_refs = repo.remote().refs

    found = False
    for refs in remote_refs:
        if refs.name == 'origin/' + request:
            found = True
        # print(refs.name)

    if found:
        print("Step 4: Branch already exists")
    else:
        print("Step 4: Branch doesn't exists")
        branch_name = request
        current = repo.create_head(branch_name)
        current.checkout()

        print(f"Step 4.1: Create branch {branch_name}")

        repo.git.push('--set-upstream', 'origin', current)

        print(f"Step 4.2: Branch {branch_name} pushed")

    print("Step 5: Read project values file")
    with open('/repo/project-repo/cluster/projects/values.yaml', 'r') as file:
        cur_yaml = yaml.safe_load(file)  # Note the safe_load

    index = -1
    for idx, project in enumerate(cur_yaml['projects']):
        if project['name'] == yaml_object['name']:
            print(f"Step 5.1: Project already exists, Index Key: {idx}")
            index = idx

    print("Step 6: Sync project values")
    if index > -1:
        cur_yaml['projects'][index] = yaml_object
    else:
        cur_yaml['projects'].append(yaml_object)

    print("Step 7: Save project values")
    if cur_yaml:
        with open('/repo/project-repo/cluster/projects/values.yaml', 'w') as file:
            yaml.safe_dump(cur_yaml, file, sort_keys=False)

    changedFiles = [item.a_path for item in repo.index.diff(None)]
    if len(changedFiles) > 0:
        repo.config_writer().set_value("user", "name", "myusername").release()
        repo.config_writer().set_value("user", "email", "myemail").release()
        repo.git.add('*')
        repo.git.commit(m="Sync OCP Project")
        repo.git.push()

    print("Step 8: Changes pushed in the repository")

    repo = Repo('/repo/project-repo')
    repo.git.checkout('main')
    repo.git.merge(request)
    repo.git.push()
    print("Step 9: Changes merged in the main branch")

    remote = repo.remote(name='origin')
    remote.push(refspec=f":{request}")
    print("Step 10: branch deleted remote")
    repo.delete_head(request)
    print("Step 11: branch deleted local")
