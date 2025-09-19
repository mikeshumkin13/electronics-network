from rest_framework import viewsets

from .models import Product
from .permissions import IsActiveStaff
from .serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """
    CRUD для продуктов.
    Доступ только активным сотрудникам.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsActiveStaff]
