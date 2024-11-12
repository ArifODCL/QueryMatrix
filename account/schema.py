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

schema = graphene.Schema(query=Query)



