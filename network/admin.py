from decimal import Decimal

from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import NetworkNode, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "model", "release_date")
    search_fields = ("name", "model")


@admin.action(description="Обнулить задолженность у выбранных")
def clear_debt(modeladmin, request, queryset):
    queryset.update(debt=Decimal("0.00"))


@admin.register(NetworkNode)
class NetworkNodeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "level",
        "city",
        "country",
        "supplier_link",
        "debt",
        "created_at",
    )
    list_filter = ("city", "country", "level")
    search_fields = ("name", "city", "country", "email")
    actions = [clear_debt]
    readonly_fields = ("level", "created_at", "supplier_link")
    filter_horizontal = ("products",)  # удобный вид для M2M в админке

    def supplier_link(self, obj: NetworkNode):
        if not obj.supplier_id:
            return "—"
        url = reverse("admin:network_networknode_change", args=[obj.supplier_id])
        return format_html('<a href="{}">{}</a>', url, obj.supplier)

    supplier_link.short_description = "Поставщик"
