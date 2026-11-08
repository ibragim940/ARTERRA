from rest_framework.routers import DefaultRouter

from .views import ArtworkViewSet, CategoryViewSet


router = DefaultRouter()

router.register(
    "artworks",
    ArtworkViewSet,
    basename="artwork",
)

router.register(
    "categories",
    CategoryViewSet,
    basename="category",
)


urlpatterns = router.urls