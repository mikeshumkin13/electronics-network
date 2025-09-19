from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter

from .models import NetworkNode, Product
from .permissions import IsActiveStaff
from .serializers import NetworkNodeSerializer, ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """
    CRUD для продуктов.
    Доступ только активным сотрудникам.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsActiveStaff]


class NetworkNodeViewSet(viewsets.ModelViewSet):
    """
    CRUD по звеньям сети (завод/розница/ИП).
    Поле debt недоступно к изменению (см. сериализатор).
    Фильтрация по стране
    """

    queryset = NetworkNode.objects.select_related("supplier").prefetch_related("products").all()
    serializer_class = NetworkNodeSerializer
    permission_classes = [IsActiveStaff]

    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ["country"]
    ordering_fields = ["name", "level", "city", "country", "created_at"]
    search_fields = ["name", "city", "country", "email"]
