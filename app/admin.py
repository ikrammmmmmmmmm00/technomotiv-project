from django.contrib import admin
from app.models import Product, Product_group, Make, Model, Material, Region, BulkUpload, MainProductGroup, RefDetails

admin.site.register(Product)
admin.site.register(Product_group)
admin.site.register(Make)
admin.site.register(Model)
admin.site.register(Material)
admin.site.register(Region)
admin.site.register(BulkUpload)
admin.site.register(MainProductGroup)



admin.site.register(RefDetails)
