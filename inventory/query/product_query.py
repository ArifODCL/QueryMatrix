import graphene
from django.db.models import Q
from inventory.models import *
from inventory.types import *
from query_matrix.pagination import *
from django.core.exceptions import ValidationError
from graphql import GraphQLError
from inventory.serializers import ProductSerializer


class ProductQuery(graphene.ObjectType):
    all_products = graphene.Field(
        create_connection(ProductType), 
        search=graphene.String(),
        first=graphene.Int(),
        after=graphene.String(),
        last=graphene.Int(),
        before=graphene.String(),
        ordering=graphene.String()
    )
    product = graphene.Field(
        ProductType, 
        id=graphene.ID(required=True)
    )

    def resolve_all_products(self, info, search=None, ordering="id", **kwargs):
        queryset = ProductModel.objects.all().order_by(ordering)

        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | 
                Q(sku__icontains=search) |
                Q(category__name__icontains=search) |
                Q(category__description__icontains=search) |
                Q(supplier__name__icontains=search) |
                Q(description__icontains=search)
            )

        return paginate_queryset(
            queryset=queryset,
            ordering_field=ordering,
            **kwargs
        )
    
    def resolve_product(self, info, id):
        queryset = ProductModel.objects.filter(pk=id)

        if queryset.exists():
            return queryset.first()
        else:
            return None
        

class CreateProductInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    sku = graphene.String(required=True)
    category = graphene.ID(required=True)
    description = graphene.String(required=True)
    unit_price = graphene.Float(required=True)
    supplier = graphene.ID(required=True)


class CreateProductMutation(graphene.Mutation):
    class Arguments:
        input = CreateProductInput(required=True)

    product = graphene.Field(ProductType)

    @classmethod
    def mutate(cls, root, info, input):
        product_data = input.__dict__

        product_serializer = ProductSerializer(data=product_data)

        if not product_serializer.is_valid():
            raise GraphQLError(f"{product_serializer.errors}")
        
        product = product_serializer.save()

        # try:
        #     product.full_clean()
        #     product.save()
        # except ValidationError as e:
        #     raise GraphQLError(f"{e.message_dict}")
        
        return CreateProductMutation(product=product)
    

class UpdateProductInput(graphene.InputObjectType):
    id = graphene.ID(required=True)
    name = graphene.String()
    sku = graphene.String()
    category = graphene.ID()
    description = graphene.String()
    unit_price = graphene.Float()
    supplier = graphene.ID()


class UpdateProductMutation(graphene.Mutation):
    class Arguments:
        input = UpdateProductInput(required=True)

    product = graphene.Field(ProductType)

    @classmethod
    def mutate(cls, root, info, input):
        product_q = ProductModel.objects.filter(pk=input.id)
        
        if not product_q.exists():
            print("Product does not exist")
            return None
        
        product = product_q.first()
        product.name = input.name or product.name
        product.sku = input.sku or product.sku
        product.category = input.category or product.category
        product.description = input.description or product.description
        product.unit_price = input.unit_price or product.unit_price
        product.supplier = input.supplier or product.supplier
        product.save()

        return UpdateProductMutation(product=product)
    

class DeleteProductMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    product = graphene.Field(ProductType)

    @classmethod
    def mutate(cls, root, info, id):
        product_q = ProductModel.objects.filter(pk=id)
        
        if not product_q.exists():
            print("Product does not exist")
            return None
        
        product = product_q.first()
        product.delete()
        return DeleteProductMutation(product=product)
