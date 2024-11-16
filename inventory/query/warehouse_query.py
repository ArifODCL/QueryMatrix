import graphene
from django.db.models import Q
from inventory.models import *
from inventory.types import *
from query_matrix.pagination import *


class WarehouseQuery(graphene.ObjectType):
    all_warehouses = graphene.Field(
        create_connection(WarehouseType), 
        search=graphene.String(),
        first=graphene.Int(),
        after=graphene.String(),
        last=graphene.Int(),
        before=graphene.String(),
        ordering=graphene.String()
    )

    def resolve_all_warehouses(self, info, search=None, ordering="id", **kwargs):
        queryset = WarehouseModel.objects.all().order_by(ordering)

        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(location__icontains=search) |
                Q(description__icontains=search)
            )

        # return queryset
        return paginate_queryset(
            queryset=queryset,
            ordering_field=ordering,
            **kwargs
        )

    warehouse = graphene.Field(
        WarehouseType, 
        id=graphene.ID(required=True)
    )

    def resolve_warehouse(self, info, id):
        queryset = WarehouseModel.objects.filter(pk=id)

        if queryset.exists():
            return queryset.first()
        else:
            return None


class CreateWarehouseInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    location = graphene.String(required=True)
    capacity = graphene.Int(required=True)
    description = graphene.String(required=True)


class CreateWarehouseMutation(graphene.Mutation):
    class Arguments:
        input = CreateWarehouseInput(required=True)

    warehouse = graphene.Field(WarehouseType)

    @classmethod
    def mutate(cls, root, info, input):
        warehouse = WarehouseModel.objects.create(
            name=input.name,
            location=input.location,
            capacity=input.capacity,
            description=input.description
        )
        return CreateWarehouseMutation(warehouse=warehouse)


class UpdateWarehouseInput(graphene.InputObjectType):
    id = graphene.ID(required=True)
    name = graphene.String()
    location = graphene.String()
    capacity = graphene.Int()
    description = graphene.String()


class UpdateWarehouseMutation(graphene.Mutation):
    class Arguments:
        input = UpdateWarehouseInput(required=True)

    warehouse = graphene.Field(WarehouseType)

    @classmethod
    def mutate(cls, root, info, input):
        warehouse = WarehouseModel.objects.get(pk=input.id)
        warehouse.name = input.name
        warehouse.location = input.location
        warehouse.capacity = input.capacity
        warehouse.description = input.description
        warehouse.save()
        return UpdateWarehouseMutation(warehouse=warehouse)


class DeleteWarehouseMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    warehouse = graphene.Field(WarehouseType)

    @classmethod
    def mutate(cls, root, info, id):
        warehouse = WarehouseModel.objects.get(pk=id)
        warehouse.delete()
        return DeleteWarehouseMutation(warehouse=warehouse)
