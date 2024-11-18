import pytest 
from inventory.models import ProductCategoryModel


pytestmark = pytest.mark.django_db


class TestProductCategoryModel:
    
    def test_create_product_category(self):

        # Arrange: Set up test data
        category_name = "Test Category"
        category_description = "Test Description"

        # Act: Create product category
        product_category = ProductCategoryModel.objects.create(
            name=category_name,
            description=category_description
        )

        product_count = ProductCategoryModel.objects.count()
        
        # Assert: Check if product category was created
        assert product_category.name == "Test Category"
        assert product_category.description == "Test Description"
        assert product_count == 1

        # Clean up: Delete product category
        product_category.delete()

    
    def test_update_product_category(self, fixture_product_category):

        # Arrange: Set up test data
        category_name = "Updated Category"
        category_description = "Updated Description"

        # Act: Update product category
        fixture_product_category.name = category_name
        fixture_product_category.description = category_description
        fixture_product_category.save()

        # Assert: Check if product category was updated
        assert fixture_product_category.name == "Updated Category"
        assert fixture_product_category.description == "Updated Description"

        # Clean up: Delete product category
        fixture_product_category.delete()

    def test_delete_product_category(self, fixture_product_category):

        # Arrange: Set up test data
        product_count = ProductCategoryModel.objects.count()

        # Act: Delete product category
        fixture_product_category.delete()

        # Assert: Check if product category was deleted
        assert ProductCategoryModel.objects.count() == product_count - 1
        