import graphene
from account.query import *
from account.models import *
from account.types import *


class Query(
    DesignationQuery, 
    EmployeeQuery,





    graphene.ObjectType
):
    pass




class Mutation(graphene.ObjectType):
    create_designation = CreateDesignation.Field()
    update_designation = UpdateDesignation.Field()
    delete_designation = DeleteDesignation.Field()





schema = graphene.Schema(query=Query, mutation=Mutation)



