from django.urls import path
from .views import *
from . import views
app_name = 'myapp'
urlpatterns = [
    path('test',views.test, name='test'),
    path('', HomeView.as_view(), name='HomeView'),
    path('ProductCreate', ProductCreate.as_view(), name='ProductCreate'),
    path('ProductEditView/<int:pk>/', ProductEditView.as_view(), name='ProductEditView'),
    path('CategoryCreate',CategoryCreate.as_view(), name='CategoryCreate'),
    path('login', UserLoginView.as_view(), name = 'UserLoginView'),
    path('logout/', UserLogoutView.as_view(), name='UserLogoutView'),
    path('AddToCartView/<int:pro_id>', AddToCartView.as_view(), name='AddToCartView'),
    path('mycart/', MyCartView.as_view(), name='MyCartView'),
    path('manage/<int:cp_id>/', ManageCartView.as_view(), name='ManageCartView'),
    path('checkout/', CheckoutView.as_view(), name='CheckoutView'),
    path('empty/', EmptyCartView.as_view(), name='EmptyCartView'),

    path('SupplierCreate/', SupplierCreate.as_view(), name='SupplierCreate'),
    path('SupplierEdit/<int:pk>/', SupplierEdit.as_view(), name='SupplierEdit'),
    path('PurchaseCreateView/<int:id>/', PurchaseCreateView.as_view(), name='PurchaseCreateView'),
    path('PurchaseData/', PurchaseData.as_view(), name='PurchaseData'),
    path('PurchaseReport/', PurchaseReport.as_view(), name='PurchaseReport'),

    path('SaleInvoiceView/', SaleInvoiceView.as_view(), name='SaleInvoiceView'),

]
