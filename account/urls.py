from django.urls import path
from graphene_django.views import GraphQLView
from account.schema import *

urlpatterns = [
    path("graphql/", GraphQLView.as_view(graphiql=True, schema=designation_schema)),
]