import pytest
from inventory.models import ProductCategoryModel

@pytest.fixture(scope="module")
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        pass


@pytest.fixture
def fixture_product_category():
    return ProductCategoryModel.objects.create(name="Prototype Category", description="Prototype Category Description")