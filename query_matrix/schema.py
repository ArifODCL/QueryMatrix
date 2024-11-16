import graphene
from account.query import *
from inventory.query import *


class Query(
    # DesignationQuery, 
    # EmployeeQuery,

    # inventory
    ProductCategoryQuery,
    SupplierQuery,
    ProductQuery,
    WarehouseQuery,





    graphene.ObjectType
):
    pass




class Mutation(graphene.ObjectType):
    # create_designation = CreateDesignation.Field()
    # update_designation = UpdateDesignation.Field()
    # delete_designation = DeleteDesignation.Field()

    # inventory
    create_product_category = CreateProductCategoryMutation.Field()
    update_product_category = UpdateProductCategoryMutation.Field()
    delete_product_category = DeleteProductCategoryMutation.Field()

    create_supplier = CreateSupplierMutation.Field()
    update_supplier = UpdateSupplierMutation.Field()
    delete_supplier = DeleteSupplierMutation.Field()

    create_product = CreateProductMutation.Field()
    update_product = UpdateProductMutation.Field()
    delete_product = DeleteProductMutation.Field()


    create_warehouse = CreateWarehouseMutation.Field()
    update_warehouse = UpdateWarehouseMutation.Field()
    delete_warehouse = DeleteWarehouseMutation.Field()





schema = graphene.Schema(query=Query, mutation=Mutation)



