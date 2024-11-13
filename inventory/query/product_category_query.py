import graphene
from django.db.models import Q
from inventory.models import *
from inventory.types import *
from query_matrix.pagination import *


class ProductCategoryQuery(graphene.ObjectType):
    all_product_categories = graphene.Field(
        create_connection(ProductCategoryType), 
        search=graphene.String(),
        first=graphene.Int(),
        after=graphene.String(),
        last=graphene.Int(),
        before=graphene.String(),
        ordering=graphene.String()
    )
    product_category = graphene.Field(
        ProductCategoryType, 
        id=graphene.ID(required=True)
    )

    def resolve_all_product_categories(self, info, search=None, ordering="id", **kwargs):
        queryset = ProductCategoryModel.objects.all()

        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | 
                Q(description__icontains=search)
            )

        return paginate_queryset(
            queryset=queryset,
            ordering_field=ordering,
            **kwargs
        )
    
    def resolve_product_category(self, info, id):
        product_category_q = ProductCategoryModel.objects.filter(pk=id)
        
        if not product_category_q.exists():
            print("Product Category does not exist")
            return None
        
        return product_category_q.first()


class CreateProductCategoryInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    description = graphene.String()


class CreateProductCategoryMutation(graphene.Mutation):
    class Arguments:
        input = CreateProductCategoryInput(required=True)

    product_category = graphene.Field(ProductCategoryType)

    @classmethod
    def mutate(cls, root, info, input):
        product_category = ProductCategoryModel.objects.create(
            name=input.name,
            description=input.description
        )
        return CreateProductCategoryMutation(product_category=product_category)


class UpdateProductCategoryInput(graphene.InputObjectType):
    id = graphene.ID(required=True)
    name = graphene.String()
    description = graphene.String()


class UpdateProductCategoryMutation(graphene.Mutation):
    class Arguments:
        input = UpdateProductCategoryInput(required=True)

    product_category = graphene.Field(ProductCategoryType)

    @classmethod
    def mutate(cls, root, info, input):
        product_category_q = ProductCategoryModel.objects.filter(pk=input.id)
        
        if not product_category_q.exists():
            print("Product Category does not exist")
            return None
        
        product_category = product_category_q.first()
        if hasattr(input, 'name'):
            product_category.name=input.name
        if hasattr(input, 'description'):
            product_category.description=input.description
        product_category.save()
        return UpdateProductCategoryMutation(product_category=product_category)


class DeleteProductCategoryMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    product_category = graphene.Field(ProductCategoryType)

    @classmethod
    def mutate(cls, root, info, id):
        product_category_q = ProductCategoryModel.objects.filter(pk=id)
        
        if not product_category_q.exists():
            print("Product Category does not exist")
            return None
        
        product_category = product_category_q.first()
        product_category.delete()
        return DeleteProductCategoryMutation(product_category=product_category)

