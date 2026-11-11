from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

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

urlpatterns += [
    path(
        "auth/token/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "auth/token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
]