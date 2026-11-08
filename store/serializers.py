from rest_framework import serializers

from .models import Artwork, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "slug",
            "description",
        ]


class ArtworkShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artwork
        fields = [
            "id",
            "title",
            "slug",
            "image",
            "price",
        ]


class ArtworkSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source="category",
        write_only=True,
    )

    class Meta:
        model = Artwork
        fields = [
            "id",
            "title",
            "slug",
            "description",
            "image",
            "price",
            "category",
            "category_id",
            "is_active",
            "featured",
            "created_at",
        ]

    def validate_title(self, value):
        value = value.strip()

        if len(value) < 3:
            raise serializers.ValidationError(
                "Название должно содержать минимум 3 символа."
            )

        return value

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Цена должна быть больше нуля."
            )

        return value

    def validate(self, attrs):
        if (
            attrs.get("featured") is True
            and attrs.get("is_active", True) is False
        ):
            raise serializers.ValidationError(
                "Неактивную картину нельзя сделать featured."
            )

        return attrs