from __future__ import annotations

from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    release_date = models.DateTimeField()

    class Meta:
        ordering = ["name", "model"]
        unique_together = ("name", "model")

    def __str__(self) -> str:
        return f"{self.name} ({self.model})"


class NetworkNode(models.Model):
    """
    Универсальное звено сети (завод/розничная сеть/ИП).
    Уровень (level) определяется положением в иерархии:
      supplier=None -> level=0 (завод), далее +1 на каждый шаг.
    """

    name = models.CharField(max_length=255)

    email = models.EmailField()
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    house = models.CharField(max_length=50)

    supplier = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="clients",
        help_text="Поставщик (родительское звено)",
    )

    products = models.ManyToManyField(Product, blank=True, related_name="nodes")

    debt = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[MinValueValidator(Decimal("0.00"))],
        help_text="Задолженность перед поставщиком",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    level = models.PositiveSmallIntegerField(editable=False, default=0)

    class Meta:
        ordering = ["level", "name"]

    def __str__(self) -> str:
        return f"[L{self.level}] {self.name}"

    def compute_level(self) -> int:
        lvl = 0
        parent = self.supplier
        seen = {self.pk}
        while parent:
            lvl += 1
            if parent.pk in seen:  # защита от циклов
                break
            seen.add(parent.pk)
            parent = parent.supplier
        return lvl

    def save(self, *args, **kwargs):
        self.level = self.compute_level()
        super().save(*args, **kwargs)

        for child in self.clients.all():
            child.save()
