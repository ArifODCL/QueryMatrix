import graphene
from django.db.models import Q
from account.models import *
from account.types import *
from account.pagination import *


class DesignationQuery(graphene.ObjectType):
    all_designations = graphene.Field(
        create_connection(DesignationType), 
        search=graphene.String(),
        first=graphene.Int(),
        after=graphene.String(),
        last=graphene.Int(),
        before=graphene.String(),
        ordering=graphene.String()
    )
    designation = graphene.Field(
        DesignationType, 
        id=graphene.ID(required=True)
    )

    def resolve_all_designations(self, info, search=None, ordering="id", **kwargs):
        queryset = DesignationModel.objects.all()

        if search:
            queryset = queryset.filter(
                Q(name__icontains=search)
            )

        return paginate_queryset(
            queryset=queryset,
            ordering_field=ordering,
            **kwargs
        )

    def resolve_designation(self, info, id):
        designation_q = DesignationModel.objects.filter(pk=id)
        
        if not designation_q.exists():
            print("Designation does not exist")
            return None
        
        return designation_q.first()


class CreateDesignationInput(graphene.InputObjectType):
    name = graphene.String(required=True)


class UpdateDesignationInput(graphene.InputObjectType):
    id = graphene.ID(required=True)
    name = graphene.String()


class CreateDesignation(graphene.Mutation):
    class Arguments:
        input = CreateDesignationInput(required=True)

    designation = graphene.Field(DesignationType)
    
    @classmethod
    def mutate(cls, root, info, input):
        designation = DesignationModel.objects.create(
            name=input.name,
        )
        return CreateDesignation(designation=designation)

class UpdateDesignation(graphene.Mutation):
    class Arguments:
        input = UpdateDesignationInput(required=True)

    designation = graphene.Field(DesignationType)

    @classmethod
    def mutate(cls, root, info, input):
        designation_q = DesignationModel.objects.filter(pk=input.id)
        
        if not designation_q.exists():
            print("Designation does not exist")
            return UpdateDesignation(designation=None)
        
        designation = designation_q.first()
        if hasattr(input, 'name'):
            designation.name=input.name
            designation.save()
            return UpdateDesignation(designation=designation)


class DeleteDesignation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, id):
        try:
            designation = DesignationModel.objects.get(pk=id)
            designation.delete()
            return DeleteDesignation(success=True)
        except DesignationModel.DoesNotExist:
            return DeleteDesignation(success=False)





class EmployeeQuery(graphene.ObjectType):
    all_employees = graphene.List(EmployeeType)
    
    def resolve_all_employees(self, info):
        return EmployeeModel.objects.all()




