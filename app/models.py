from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
import pandas as pd
import threading

from django.db import models


class Make(models.Model):
    name = models.CharField(max_length=600)

    def __str__(self):
        return self.name


class Model(models.Model):
    name = models.CharField(max_length=600)

    def __str__(self):
        return self.name

    
class Product(models.Model):
    ref_no = models.CharField(max_length=600)
    product_group = models.ForeignKey("Product_group", on_delete=models.CASCADE)
    material = models.ForeignKey("Material", on_delete=models.CASCADE)
    bar_code_id = models.CharField(max_length=600, blank=True, null=True)
    position = models.CharField(max_length=600, blank=True, null=True)
    oem_code = models.CharField(max_length=600, blank=True, null=True)
    quantity_per_vehicle = models.CharField(max_length=600, blank=True, null=True)
    product_img = models.URLField(max_length=1500, blank=True, null=True)
    weight = models.CharField(max_length=600, blank=True, null=True)
    total_length = models.CharField(max_length=600, blank=True, null=True)
    width = models.CharField(max_length=600, blank=True, null=True)
    height = models.CharField(max_length=600, blank=True, null=True)
    bolt_matric = models.CharField(max_length=600, blank=True, null=True)
    log_metric = models.CharField(max_length=255, null=True, blank=True)
    region = models.ForeignKey("Region", on_delete=models.CASCADE)
    pairs_handed = models.CharField(max_length=600, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    cross_code = models.CharField(max_length=600, blank=True, null=True)
    checked_box = models.BooleanField(default=False)
    inquiry_box = models.BooleanField(default=False)

    def __str__(self):
        return self.ref_no


class RefDetails(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="ref_details")
    make = models.ForeignKey("Make", on_delete=models.CASCADE)
    model = models.ForeignKey("Model", on_delete=models.CASCADE)
    year_body_type = models.CharField(max_length=600)

    def __str__(self):
        return f"{self.product.ref_no} - {self.make.name} - {self.model.name} - {self.year_body_type}"

    

class Region(models.Model):
    region = models.CharField(max_length=600, blank=True, null=True)

    def __str__(self):
        return self.region


class MainProductGroup(models.Model):
    main_group_name = models.CharField(max_length=600, blank=True, null=True)

    def __str__(self):
        return self.main_group_name


class Product_group(models.Model):
    main_pg = models.ForeignKey("MainProductGroup", on_delete=models.CASCADE, blank=True, null=True)
    desc = models.CharField(max_length=600)

    def __str__(self):
        return self.desc







class Material(models.Model):
    material_type = models.CharField(max_length=600)

    def __str__(self):
        return self.material_type


class BulkUpload(models.Model):
    file = models.FileField(upload_to='file')

    def __str__(self):
        return self.file.name


# def uploadData(instance):
#     # Read the Excel file into a pandas DataFrame
#     try:
#         p = pd.read_excel(instance.file.path).values
#     except Exception as e:
#         print(f"Error reading file: {e}")
#         return

#     # Loop through the rows in the Excel file
#     for x in p:
#         try:
#             ref_no = x[2]  # TECHNOMOTIV Code (column 3)
#             if not Product.objects.filter(ref_no=ref_no).exists():
#                 # Create or get MainProductGroup and Product_group
#                 main_group_name = x[3]  # PRODUCT CATEGORY (column 4)
#                 main_group, created = MainProductGroup.objects.get_or_create(main_group_name=main_group_name)
#                 product_group_desc = x[4]  # PRODUCT GROUP (column 5)
#                 product_group, created = Product_group.objects.get_or_create(desc=product_group_desc, main_pg=main_group)

#                 # Create the product
#                 pr = Product(
#                     product_img=x[1],  # Image of the product (column 2)
#                     ref_no=ref_no,
#                     product_group=product_group,
#                     make=Make.objects.get_or_create(name=x[5])[0],  # Car Make (column 6)
#                     model=Model.objects.get_or_create(name=x[6])[0],  # Model (column 7)
#                     year_body_type=x[7],  # Year & Body Type (column 8)
#                     position=x[8],  # Position (column 9)
#                     oem_code=x[9],  # OEM Code (column 10)
#                     cross_code=x[10],  # Cross Code (column 11)
#                     quantity_per_vehicle=x[11],  # Quantity per vehicle (column 12)
#                     weight=x[12],  # Weight kg (column 13)
#                     width=x[13],  # Width mm (column 14)
#                     bolt_matric=x[14],  # Bolt Metric (column 15)
#                     total_length=x[15],  # Centre Length mm (column 16)
#                     height=x[16],  # Height mm (column 17)
#                     material=Material.objects.get_or_create(material_type=x[17])[0],  # Material (column 18)
#                     region=Region.objects.get_or_create(region=x[18])[0],  # Region (column 19)
#                     pairs_handed=x[19],  # Quantity per box (column 20)
#                     notes=x[20],  # Notes (column 21)
#                     bar_code_id=x[21],  # Bar Code ID (column 22)
#                     log_metric=x[22],  # Log Metric (column 24)
                    
#                 )
#                 pr.save()

               
            

#         except Exception as e:
#             print(f"Error processing row {x}: {e}")


# def uploadData(instance):
#     # Read the Excel file into a pandas DataFrame
#     try:
#         data = pd.read_excel(instance.file.path).values
#     except Exception as e:
#         print(f"Error reading file: {e}")
#         return

#     # Loop through the rows in the Excel file
#     for row in data:
#         try:
#             ref_no = row[2]  # TECHNOMOTIVE Code (column 3)

#             # Create or get MainProductGroup and Product_group
#             main_group_name = row[3]  # PRODUCT CATEGORY (column 4)
#             main_group, _ = MainProductGroup.objects.get_or_create(main_group_name=main_group_name)
            
#             product_group_desc = row[4]  # PRODUCT GROUP (column 5)
#             product_group, _ = Product_group.objects.get_or_create(desc=product_group_desc, main_pg=main_group)

#             # Create or get Product
#             product, _ = Product.objects.get_or_create(
#                 ref_no=ref_no,
#                 product_group=product_group,
#                 defaults={  # Populate other fields only if the product is new
#                     'product_img': row[1],  # Image of the product (column 2)
#                     'position': row[8],  # Position (column 9)
#                     'oem_code': row[9],  # OEM Code (column 10)
#                     'cross_code': row[10],  # Cross Code (column 11)
#                     'quantity_per_vehicle': row[11],  # Quantity per vehicle (column 12)
#                     'weight': row[12],  # Weight kg (column 13)
#                     'width': row[13],  # Width mm (column 14)
#                     'bolt_matric': row[14],  # Bolt Metric (column 15)
#                     'total_length': row[15],  # Centre Length mm (column 16)
#                     'height': row[16],  # Height mm (column 17)
#                     'material': Material.objects.get_or_create(material_type=row[17])[0],  # Material (column 18)
#                     'region': Region.objects.get_or_create(region=row[18])[0],  # Region (column 19)
#                     'pairs_handed': row[19],  # Quantity per box (column 20)
#                     'notes': row[20],  # Notes (column 21)
#                     'bar_code_id': row[21],  # Bar Code ID (column 22)
#                     'log_metric': row[22],  # Log Metric (column 24)
#                 }
#             )

#             # Create RefDetails for each unique combination of make, model, and year_body_type
#             make_name = row[5]  # Car Make (column 6)
#             model_name = row[6]  # Model (column 7)
#             year_body_type = row[7]  # Year & Body Type (column 8)

#             make, _ = Make.objects.get_or_create(name=make_name)
#             model, _ = Model.objects.get_or_create(name=model_name)

#             RefDetails.objects.get_or_create(
#                 product=product,
#                 make=make,
#                 model=model,
#                 year_body_type=year_body_type
#             )

           

#         except Exception as e:
#             print(f"Error processing row {row}: {e}")


def uploadData(instance):
    # Read the Excel file into a pandas DataFrame
    try:
        data = pd.read_excel(instance.file.path).values
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    # Loop through the rows in the Excel file
    for row in data:
        try:
            ref_no = row[2]  # TECHNOMOTIVE Code (column 3)

            # Create or get MainProductGroup and Product_group
            main_group_name = row[3]  # PRODUCT CATEGORY (column 4)
            main_group, _ = MainProductGroup.objects.get_or_create(main_group_name=main_group_name)
            
            product_group_desc = row[4]  # PRODUCT GROUP (column 5)
            product_group, _ = Product_group.objects.get_or_create(desc=product_group_desc, main_pg=main_group)

            # Create or get Product
            product, _ = Product.objects.get_or_create(
                ref_no=ref_no,
                product_group=product_group,
                defaults={  # Populate other fields only if the product is new
                    'product_img': row[1],  # Image of the product (column 2)
                    'position': row[8],  # Position (column 9)
                    'oem_code': row[9],  # OEM Code (column 10)
                    'cross_code': row[10],  # Cross Code (column 11)
                    'quantity_per_vehicle': row[11],  # Quantity per vehicle (column 12)
                    'weight': row[12],  # Weight kg (column 13)
                    'width': row[13],  # Width mm (column 14)
                    'bolt_matric': row[14],  # Bolt Metric (column 15)
                    'total_length': row[15],  # Centre Length mm (column 16)
                    'height': row[16],  # Height mm (column 17)
                    'material': Material.objects.get_or_create(material_type=row[17])[0],  # Material (column 18)
                    'region': Region.objects.get_or_create(region=row[18])[0],  # Region (column 19)
                    'pairs_handed': row[19],  # Quantity per box (column 20)
                    'notes': row[20],  # Notes (column 21)
                    'bar_code_id': row[21],  # Bar Code ID (column 22)
                    'log_metric': row[22],  # Log Metric (column 24)
                }
            )

            # Create RefDetails for each unique combination of make, model, and year_body_type
            make_name = row[5]  # Car Make (column 6)
            model_name = row[6]  # Model (column 7)
            year_body_type = row[7]  # Year & Body Type (column 8)

            make, _ = Make.objects.get_or_create(name=make_name)
            model, _ = Model.objects.get_or_create(name=model_name)

            # Create RefDetails
            RefDetails.objects.get_or_create(
                product=product,
                make=make,
                model=model,
                year_body_type=year_body_type
            )

        except Exception as e:
            print(f"Error processing row {row}: {e}")


         
@receiver(post_save, sender=BulkUpload)
def update_stock(sender, instance, *args, **kwargs):
    # Running the data upload in a separate thread to avoid blocking the main thread
    t = threading.Thread(target=uploadData, args=(instance,))
    t.daemon = True
    t.start()