from django.shortcuts import render, HttpResponse , redirect, reverse
from app.models import Product, Product_group, Make, MainProductGroup, Product_group
import pandas as pd
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from .models import Model, Product, Product_group, Make, MainProductGroup
from django.db.models import Prefetch

from app.models import Product, Make

from app.models import RefDetails
from django.db.models import Q


from django.http import JsonResponse
from .models import RefDetails
from django.http import JsonResponse
from django.template.loader import render_to_string





def NavSearch(request, toSearch):
    all_products = Product.objects.filter(product_group__desc = toSearch)
    print(all_products)
    return all_products



def products(request):
    all_products = Product.objects.all()
    select_product_groups = Product_group.objects.all()
    make = Make.objects.all()

   

    # Retrieve query parameters
    oem_search = request.GET.get('oem_code')
    ref_search = request.GET.get('ref_no')
    c_code_search = request.GET.get('cross_code')
    selected_make = request.GET.get('make')
    selected_p_group = request.GET.get('model')
    comparison_ids = request.GET.get('comparison_ids')
    inquiry_ids = request.GET.get('inquiry_ids')
    nav_search = request.GET.get('nav_search')

    # Navigation search logic
    if nav_search:
        new_products = NavSearch(request, nav_search)
        context = {
            'all_products': new_products,
            'all_makes': make,
            'all_pro_groups': select_product_groups,
            'main_groups': MainProductGroup.objects.all(),
            'product_groups': Product_group.objects.all(),
        }
        return render(request, 'product.html', context)

    # Apply filters based on query parameters
    if oem_search:
        all_products = all_products.filter(oem_code__contains=oem_search)




    if selected_make:
    # Filter RefDetails by the selected make
       filtered_ref_details = RefDetails.objects.filter(make__name__iexact=selected_make)

    # Retrieve unique product IDs associated with the filtered RefDetails
       product_ids = filtered_ref_details.values_list('product_id', flat=True).distinct()

    # Filter products based on these IDs
       all_products = all_products.filter(id__in=product_ids)

    # Pass the filtered RefDetails to the template
       filtered_ref_details = filtered_ref_details.filter(product__in=all_products)
    else:
    # If no make is selected, retrieve all RefDetails
        filtered_ref_details = RefDetails.objects.all()

    if c_code_search:
        all_products = all_products.filter(cross_code__contains=c_code_search)

    if selected_p_group:
        all_products = all_products.filter(product_group__desc=selected_p_group)

    # Handle POST requests for inquiry or comparison lists
    if request.method == 'POST':
        context = {}
        
        # Clear inquiry list
        if request.POST.get("clear_inquiry_list"):
            inquiry_ids = ''
            context["inquiry_ids"] = ''
            context['all_products'] = []
            return render(request, "inquiry_list.html", context)
        
        # Manage inquiry IDs
        if request.POST.get("inquiry_ids") or request.POST.get("inquiry_ids") == "":
            inquiry_ids = request.POST.get("inquiry_ids").split(",") if request.POST.get("inquiry_ids") else []
            checking_comp_ids_in_inquiry = request.POST.get("checking_comp_ids_in_inquiry", "").split(",")

            # Remove items from inquiry list
            if request.POST.get("to_remove_item"):
                product_id = int(request.POST.get("product_id"))
                inquiry_ids = [str(id) for id in inquiry_ids if int(id) != product_id]

            # Add new references to inquiry list
            if request.POST.get("inquiry_new_ref"):
                inquiry_new_ref = request.POST.get("inquiry_new_ref")
                if Product.objects.filter(ref_no=inquiry_new_ref).exists():
                    product = Product.objects.get(ref_no=inquiry_new_ref)
                    if str(product.id) not in inquiry_ids:
                        inquiry_ids.append(str(product.id))

            # Prepare context for rendering
            inquiry_ids = ",".join(inquiry_ids)
            context["inquiry_ids"] = inquiry_ids
            context['all_products'] = [Product.objects.get(id=id) for id in inquiry_ids] if inquiry_ids else []
            context['main_groups'] = MainProductGroup.objects.all()
            context['product_groups'] = Product_group.objects.all()
            context["checking_comp_ids_in_inquiry"] = checking_comp_ids_in_inquiry

            return render(request, "inquiry_list.html", context)

    # Prepare context for rendering products page
    context = {
    'all_products': all_products,
    'filtered_ref_details': filtered_ref_details,  # Pass only relevant RefDetails
    'search_1': oem_search or '',
    'search_2': ref_search or '',
    'search_3': c_code_search or '',
    'search_4': selected_make or '',
    'search_5': selected_p_group or '',
    'all_makes': make,
    'all_pro_groups': select_product_groups,
    "comparison_ids": comparison_ids or "",
    "inquiry_ids": inquiry_ids or "",
    'main_groups': MainProductGroup.objects.all(),
    'product_groups': Product_group.objects.all(),
}


    return render(request, 'product.html', context)


from django.http import JsonResponse

def get_models(request, make_id):
    models = Model.objects.filter(refdetails__make_id=make_id).distinct()
    model_data = [{"id": model.id, "name": model.name} for model in models]
    return JsonResponse({"models": model_data})

def get_years(request, model_id):
    years = RefDetails.objects.filter(model_id=model_id).values_list('year_body_type', flat=True).distinct()
    return JsonResponse({"years": list(years)})


# def fetch_models(request):
#     make_name = request.GET.get('make')
#     if not make_name:
#         return JsonResponse({'error': 'Make not provided'}, status=400)
    
#     models = RefDetails.objects.filter(make__name=make_name).values_list('model__name', flat=True).distinct()
#     if not models:
#         return JsonResponse({'models': []})
#     return JsonResponse({'models': list(models)})


# def fetch_year_body_types(request):
#     make_name = request.GET.get('make')
#     model_name = request.GET.get('model')
#     if not make_name or not model_name:
#         return JsonResponse({'error': 'Make or Model not provided'}, status=400)

#     year_body_types = RefDetails.objects.filter(make__name=make_name, model__name=model_name).values_list('year_body_type', flat=True).distinct()
#     return JsonResponse({'year_body_types': list(year_body_types)})


# from django.template.loader import render_to_string
# from django.http import JsonResponse
# import logging
# logger = logging.getLogger(__name__)

# from django.http import JsonResponse
# from django.template.loader import render_to_string

# def filter_products(request):
#     make = request.GET.get('make')
#     model = request.GET.get('model')
#     year_body_type = request.GET.get('year_body_type')

#     # Query the products based on filters
#     products = Product.objects.filter(make=make, model=model, year_body_type=year_body_type)

#     # Render table rows as HTML
#     html = render_to_string('product_table_body.html', {'products': products})

#     return JsonResponse({'html': html})



def product_details(request, ref_no):
    
    product_getted = Product.objects.get(ref_no = ref_no)
    context = {
        'product_getted' : product_getted,
        'ref_details': product_getted.ref_details.all(),
    }
        
    return render(request, 'product_details.html', context)



def check_or_unchecked(compare_ids):
    for x in Product.objects.all():
        if not str(x.id) in compare_ids:
            x.checked_box = False
        else:
            x.checked_box = True

def inquiry_check(inquiry_ids):
    for x in Product.objects.all():
        if not str(x.id) in inquiry_ids:
            x.inquiry_box = False    
        else:
            x.inquiry_box = True

def index(request):
    all_products = Product.objects.all()
    select_product_groups = Product_group.objects.all()
    make = Make.objects.all()
    nav_search = request.GET.get('nav_search')
    if nav_search:
        new_products = NavSearch(request, nav_search)
        context = {
            'all_products' : new_products,
            'all_makes' : make,
            'all_pro_groups' : select_product_groups,
            'main_groups' : MainProductGroup.objects.all(),
            'product_groups' : Product_group.objects.all(),
        }
        return render(request, 'product.html',context)
    
    context = {
        'all_products' : all_products,
        'all_makes' : make,
        'all_pro_groups' : select_product_groups,
        'main_groups' : MainProductGroup.objects.all(),
        'product_groups' : Product_group.objects.all(),
        
        
    }
    return render(request, 'index.html', context)





def compare_items(request):

    comparison_ids = request.POST.get('comparison_ids')
    compare_ids = request.POST.get('comparison_ids')
    nav_search = request.GET.get('nav_search')
    if nav_search:
        new_products = NavSearch(request, nav_search)
        context = {
            'all_products' : new_products,
            'main_groups' : MainProductGroup.objects.all(),
            'product_groups' : Product_group.objects.all(),
        }
        return render(request, 'product.html',context)

    
    if not comparison_ids == "" and not comparison_ids == None:
        comparison_ids = comparison_ids.split(",")
        comparison_ids = ",".join(comparison_ids)
    else:
        comparison_ids = ",".join([str(a) for a in Product.objects.filter(checked_box=True).values_list("id", flat=True)])

    context = {}

    if request.POST.get("clear_lists"):
        compare_ids = []
        context["compare_ids"] = ''
        context['all_products'] = []

    # Check if the "comparison_ids" key is present in the request data before trying to split
    if request.POST.get("comparison_ids") is not None and request.POST.get("comparison_ids") != "":
        compare_ids = request.POST.get("comparison_ids").split(",")
    else:
        compare_ids = []

    all_products = []
    if compare_ids:
        for id in compare_ids:
            z = Product.objects.get(id=id)
            all_products.append(z)

    if request.POST.get("comparison_new_ref"):
        print(request.POST.get("comparison_new_ref"))
        comparison_new_ref = request.POST.get("comparison_new_ref")
        if Product.objects.filter(ref_no=comparison_new_ref).exists():
            p = Product.objects.get(ref_no=comparison_new_ref)
            if not str(p.id) in compare_ids:
                all_products.append(p)
                compare_ids.append(str(p.id))

    compare_ids = ",".join(compare_ids)

    context['all_products'] = all_products

    context = {
        'all_products': all_products,
        "compare_ids": compare_ids,
        "comparison_ids": comparison_ids if comparison_ids else "",
        'main_groups' : MainProductGroup.objects.all(),
        'product_groups' : Product_group.objects.all(),
    }
    return render(request, 'compare_items.html',context)



from django.shortcuts import render
from app.models import Product  # Import Product model

def product_list(request):
    # Fetch all products
    product_list = Product.objects.all()  # This fetches all products from the Product model
    
    # Debugging: Check if product_list contains any data
    print("Product List: ", product_list)  # This will print the list of products in the console/log

    # Check if product_list is empty and print a message in the console
    if not product_list:
        print("No products found")

    context = {
        'product_list': product_list,
    }
    return render(request, 'product_list.html', context)


# def products(request):
#     all_products = Product.objects.all()
#     makes = Make.objects.all()
#     select_product_groups = Product_group.objects.all()

#     # Filters
#     oem_search = request.GET.get('oem_code')
#     ref_search = request.GET.get('ref_no')
#     c_code_search = request.GET.get('cross_code')
#     selected_make = request.GET.get('make')
#     selected_p_group = request.GET.get('model')

#     # Apply filters
#     if oem_search:
#         all_products = all_products.filter(oem_code__icontains=oem_search)
#     if ref_search:
#         all_products = all_products.filter(ref_no__icontains=ref_search)
#     if c_code_search:
#         all_products = all_products.filter(cross_code__icontains=c_code_search)
#     if selected_make:
#         all_products = all_products.filter(ref_details__make__name__iexact=selected_make).distinct()
#     if selected_p_group:
#         all_products = all_products.filter(product_group__desc=selected_p_group)

#     context = {
#         'all_products': all_products,
#         'all_makes': makes,
#         'all_pro_groups': select_product_groups,
#     }
#     return render(request, 'product.html', context)






# def product_list(request):
#     search_4 = request.GET.get('make', None)  # Get the selected 'Make' from the GET request

#     if search_4:
#         # Filter products based on the selected 'Make' by checking the related 'ref_details'
#         all_products = Product.objects.filter(ref_details__make__name=search_4).distinct()
#     else:
#         # If no filter, display all products
#         all_products = Product.objects.all()

#     all_makes = Make.objects.all()  # Assuming you have a model called 'Make'

#     context = {
#         'all_products': all_products,
#         'all_makes': all_makes,
#         'search_4': search_4,
#     }
#     return render(request, 'product_list.html', context)



def inquiry_list(request):
    return render(request, 'inquiry_list.html')


def pdf(request):
    return render(request, 'inquiry_pdf.html')

@csrf_exempt
def compare_checkbox(request):
    if request.method == "POST":
        product_id = request.POST.get('product_id')
        checkbox_val = request.POST.get('checkbox_val')
        getted_item = Product.objects.get(id = product_id)
        
        if getted_item.checked_box == True:
            getted_item.checked_box = False
            getted_item.save()
        else:
            getted_item.checked_box = True
            getted_item.save()

        return JsonResponse({"success":"saved"})
        
    return JsonResponse({"success":"error"})

def inquiry_checkbox(request):
    return render(request, 'inquiry_pdf.html')

def ImgNotFound(request):
    return render(request, 'ImgNotFound.html')




