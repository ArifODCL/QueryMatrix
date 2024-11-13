import graphene
from django.db.models import Q
from inventory.models import *
from inventory.types import *
from query_matrix.pagination import *
from django.core.exceptions import ValidationError
from graphql import GraphQLError


class SupplierQuery(graphene.ObjectType):
    all_suppliers = graphene.Field(
        create_connection(SupplierType), 
        search=graphene.String(),
        first=graphene.Int(),
        after=graphene.String(),
        last=graphene.Int(),
        before=graphene.String(),
        ordering=graphene.String()
    )
    supplier = graphene.Field(
        SupplierType, 
        id=graphene.ID(required=True)
    )

    def resolve_all_suppliers(self, info, search=None, ordering="id", **kwargs):
        queryset = SupplierModel.objects.all()

        if search:
            queryset = queryset.filter(
                name__icontains=search,
                contact_email__icontains=search,
                contact_phone__icontains=search,
                address__icontains=search,
                website__icontains=search,
            )

        return paginate_queryset(
            queryset=queryset,
            ordering_field=ordering,
            **kwargs
        )

    def resolve_supplier(self, info, id):
        queryset = SupplierModel.objects.filter(pk=id)

        if queryset.exists():
            return queryset.first()
        else:
            return None


class CreateSupplierInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    contact_email = graphene.String(required=True)
    contact_phone = graphene.String(required=True)
    address = graphene.String(required=True)
    website = graphene.String(required=True)


class CreateSupplierMutation(graphene.Mutation):
    class Arguments:
        input = CreateSupplierInput(required=True)

    supplier = graphene.Field(SupplierType)

    @classmethod
    def mutate(cls, root, info, input):
        supplier = SupplierModel(
            name=input.name,
            contact_email=input.contact_email,
            contact_phone=input.contact_phone,
            address=input.address,
            website=input.website
        )
        try:
            supplier.full_clean()
            supplier.save()
        except ValidationError as e:
            raise GraphQLError(f"{e.message_dict}")

        return CreateSupplierMutation(supplier=supplier)


class UpdateSupplierInput(graphene.InputObjectType):
    id = graphene.ID(required=True)
    name = graphene.String()
    contact_email = graphene.String()
    contact_phone = graphene.String()
    address = graphene.String()
    website = graphene.String()


class UpdateSupplierMutation(graphene.Mutation):
    class Arguments:
        input = UpdateSupplierInput(required=True)

    supplier = graphene.Field(SupplierType)

    @classmethod
    def mutate(cls, root, info, input):
        supplier_q = SupplierModel.objects.filter(pk=input.id)
        
        if not supplier_q.exists():
            print("Supplier does not exist")
            return None
        
        supplier = supplier_q.first()
        supplier.name = input.name
        supplier.contact_email = input.contact_email
        supplier.contact_phone = input.contact_phone
        supplier.address = input.address
        supplier.website = input.website
        supplier.save()
        return UpdateSupplierMutation(supplier=supplier)
    

class DeleteSupplierMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    supplier = graphene.Field(SupplierType)

    @classmethod
    def mutate(cls, root, info, id):
        supplier_q = SupplierModel.objects.filter(pk=id)
        
        if not supplier_q.exists():
            print("Supplier does not exist")
            return None
        
        supplier = supplier_q.first()
        supplier.delete()
        return DeleteSupplierMutation(supplier=supplier)
