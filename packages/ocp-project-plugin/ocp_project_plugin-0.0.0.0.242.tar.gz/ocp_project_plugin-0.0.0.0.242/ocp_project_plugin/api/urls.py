from netbox.api.routers import NetBoxRouter
from ocp_project_plugin.api.views import OCPProjectPluginRootView, AppEnvironmentViewSet, OCPProjectViewSet

router = NetBoxRouter()
router.APIRootView = OCPProjectPluginRootView

router.register("appenvironment", AppEnvironmentViewSet)
router.register("ocpproject", OCPProjectViewSet)

urlpatterns = router.urls
