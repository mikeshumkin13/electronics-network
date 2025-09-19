from rest_framework.routers import DefaultRouter

from .views import NetworkNodeViewSet, ProductViewSet

router = DefaultRouter()
router.register(r"products", ProductViewSet, basename="product")
router.register(r"network-nodes", NetworkNodeViewSet, basename="networknode")

urlpatterns = router.urls
