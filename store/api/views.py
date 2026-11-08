from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from ..models import Artwork, Category
from ..serializers import (
    ArtworkSerializer,
    ArtworkShortSerializer,
    CategorySerializer,
)
from .pagination import ArtworkPagination
from .permissions import IsAdminOrReadOnly


class ArtworkViewSet(viewsets.ModelViewSet):
    serializer_class = ArtworkSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = ArtworkPagination

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = [
        "category",
        "featured",
        "is_active",
    ]

    search_fields = [
        "title",
        "description",
        "category__name",
    ]

    ordering_fields = [
        "title",
        "price",
        "created_at",
    ]

    ordering = ["-created_at"]

    def get_queryset(self):
        queryset = (
            Artwork.objects
            .select_related("category")
        )

        if self.request.user.is_staff:
            return queryset

        return queryset.filter(is_active=True)


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]

    queryset = Category.objects.all()

    lookup_field = "slug"

    # создаёт дополнительный endpoint, которого нет среди стандартных CRUD-операций.
    @action(
        detail=True,
        methods=["get"],
        url_path="artworks",
    )
    def artworks(self, request, slug=None):
        category = self.get_object()

        artworks = (
            category.artworks
            .filter(is_active=True)
            .select_related("category")
        )

        serializer = ArtworkShortSerializer(
            artworks,
            many=True,
            context={"request": request},
        )

        return Response(serializer.data, status=status.HTTP_200_OK)