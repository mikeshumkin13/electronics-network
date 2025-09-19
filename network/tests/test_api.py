import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from network.models import NetworkNode
from network.tests.factories import NetworkNodeFactory, ProductFactory


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def staff_user(db):
    User = get_user_model()
    u = User.objects.create_user(
        username="staff",
        password="pass",
        is_active=True,
        is_staff=True,
    )
    return u


@pytest.fixture
def non_staff_user(db):
    User = get_user_model()
    return User.objects.create_user(
        username="user",
        password="pass",
        is_active=True,
        is_staff=False,
    )


def test_level_computation(db):
    factory = NetworkNodeFactory(supplier=None)
    retail = NetworkNodeFactory(supplier=factory)
    ip = NetworkNodeFactory(supplier=retail)
    assert factory.level == 0
    assert retail.level == 1
    assert ip.level == 2


def test_permissions_active_staff_only(api_client, non_staff_user):
    # залогинились обычным пользователем -> должно запретить
    api_client.login(username="user", password="pass")
    resp = api_client.get("/api/network-nodes/")
    assert resp.status_code == 403  # доступ только для staff


def test_networknode_crud_and_debt_readonly(api_client, staff_user, db):
    api_client.login(username="staff", password="pass")
    p1 = ProductFactory()
    p2 = ProductFactory()

    # create with product_ids
    payload = {
        "name": "Retail",
        "email": "r@ex.com",
        "country": "RU",
        "city": "СПб",
        "street": "Невский",
        "house": "10",
        "product_ids": [p1.id, p2.id],
    }
    resp = api_client.post("/api/network-nodes/", payload, format="json")
    assert resp.status_code == 201
    node_id = resp.json()["id"]

    # попытка изменить debt через API
    resp2 = api_client.patch(f"/api/network-nodes/{node_id}/", {"debt": "999.99"}, format="json")
    assert resp2.status_code in (200, 202)
    # перечитаем объект — debt должен остаться 0.00
    nn = NetworkNode.objects.get(pk=node_id)
    assert str(nn.debt) == "0.00"


def test_filter_by_country(api_client, staff_user, db):
    api_client.login(username="staff", password="pass")
    NetworkNodeFactory(country="RU")
    NetworkNodeFactory(country="US")
    NetworkNodeFactory(country="RU")

    resp_all = api_client.get("/api/network-nodes/")
    assert resp_all.status_code == 200
    assert len(resp_all.json()) >= 3

    resp_ru = api_client.get("/api/network-nodes/?country=RU")
    assert resp_ru.status_code == 200
    data = resp_ru.json()
    # все элементы — из RU
    assert all(item["country"] == "RU" for item in data)
