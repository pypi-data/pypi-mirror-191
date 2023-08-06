from utilities.choices import ChoiceSet


class AppEnvironmentClusterEnvChoices(ChoiceSet):
    key = 'AppEnvironment.cluster_env'

    CHOICE_PRD = 'PRD'
    CHOICE_INT = 'INT'
    CHOICE_TST = 'TST'
    CHOICE_DEV = 'DEV'

    CHOICES = [
        (CHOICE_PRD, 'PRD', 'red'),
        (CHOICE_INT, 'INT', 'yellow'),
        (CHOICE_TST, 'TST', 'cyan'),
        (CHOICE_DEV, 'DEV', 'green'),
    ]


class AppEnvironmentDeploymentKindChoices(ChoiceSet):
    key = 'AppEnvironment.deployment_kind'

    DEPLOYMENT_KIND_HELM = 'HELM'
    DEPLOYMENT_KIND_KUSTOMIZE = 'KUSTOMIZE'
    DEPLOYMENT_KIND_NORMAL = 'NORMAL'

    CHOICES = [
        (DEPLOYMENT_KIND_HELM, 'HELM', 'gray'),
        (DEPLOYMENT_KIND_KUSTOMIZE, 'KUSTOMIZE', 'green'),
        (DEPLOYMENT_KIND_NORMAL, 'NORMAL', 'cyan'),
    ]
