from django.contrib import admin
from django.urls import path, include
from app.views import product_list, index, products, product_details,inquiry_list,pdf,inquiry_checkbox,compare_checkbox, ImgNotFound, compare_items
from . import views

app_name = "products"

urlpatterns = [
    path('', index, name='index'),
    # path('products', products, name='products'),
    path('inquiry_list', inquiry_list, name='inquiry_list'),
    path('compare_items', compare_items, name='compare_items'),
    path('product_details/<str:ref_no>', product_details, name = 'product_details'),
    path('product-list/', views.product_list, name='product_list'),
    # path('product-details/<slug:ref_no>/', views.product_details, name='product_details'),

    path('pdf', pdf, name = 'pdf'),
    path('compare_checkbox', compare_checkbox, name='compare_checkbox'),
    path('inquiry_checkbox', inquiry_checkbox, name='inquiry_checkbox'),


    path("""media/ImgNotFound""", ImgNotFound, name='ImgNotFound'),

    # path('fetch_models/', views.fetch_models, name='fetch_models'),
    # path('fetch_year_body_types/', views.fetch_year_body_types, name='fetch_year_body_types'),

    # path('filter_products/', views.filter_products, name='filter_products'),

    # path('get-models/<int:make_id>/', views.get_models, name='get_models'),
    # path('get-years/<int:model_id>/', views.get_years, name='get_years'),


    path('products/', views.products, name='products'),
    path('get-models/<int:make_id>/', views.get_models, name='get_models'),
    path('get-years/<int:model_id>/', views.get_years, name='get_years'),
    path('search-products/', views.search_products, name='search_products'),
    path('search-products-by-oem/', views.search_products_by_oem, name='search_products_by_oem'),

]