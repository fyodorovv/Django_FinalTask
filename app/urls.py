from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('addproduct/', views.AddProduct.as_view(), name='addproduct'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('product/<slug:product_slug>/',
         views.ShowProduct.as_view(), name='product'),
    path('category/<slug:category_slug>/',
         views.ProductCategory.as_view(), name='category'),
    path('logout/', views.LoginUser.logout_user, name='logout'),
    path('basket/', views.BasketView.as_view(), name='basket'),
    path('add/<int:product_id>/',
         views.BasketView.add_to_basket, name='add_to_basket'),
    path('basket/add/<int:product_id>/',
         views.BasketView.add_product, name='add_product'),
    path('basket/remove/<int:product_id>/',
         views.BasketView.remove_product, name='remove_product'),
    path('basket/delete/<int:product_id>/',
         views.BasketView.remove_from_basket, name='remove_from_basket'),

    path('register/', views.RegisterUser.as_view(), name='register'),

]
