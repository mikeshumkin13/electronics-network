from rest_framework import serializers

from .models import NetworkNode, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "model", "release_date"]


class NetworkNodeSerializer(serializers.ModelSerializer):
    # products — только читаем красиво (вложенные объекты)
    products = ProductSerializer(many=True, read_only=True)
    # а записывать будем id-шниками (write-only поле)
    product_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        write_only=True,
        required=False,
        queryset=Product.objects.all(),
        source="products",  # пишем в то же m2m-поле
    )

    class Meta:
        model = NetworkNode
        # ВАЖНО: запрет на изменение debt через API
        read_only_fields = ["debt", "level", "created_at"]
        fields = [
            "id",
            "name",
            "email",
            "country",
            "city",
            "street",
            "house",
            "supplier",
            "level",
            "debt",
            "created_at",
            "products",
            "product_ids",
        ]
