from django.urls import path
from .views import *
from . import views
app_name = 'myapp'
urlpatterns = [
    path('test',views.test, name='test'),
    path('HomeView', HomeView.as_view(), name='HomeView'),
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
    path('SaleInvoiceReportFilter/', SaleInvoiceReportFilter.as_view(), name='SaleInvoiceReportFilter'),
    path('InvoiceDetailView/<int:pk>/', InvoiceDetailView.as_view(), name='InvoiceDetailView'),
    path('InvoiceStatusChange/<int:pk>/', InvoiceStatusChange.as_view(), name='InvoiceStatusChange'),
    path('SaleItemReportView', SaleItemReportView.as_view(), name='SaleItemReportView'),
    path('GPView', GPView.as_view(), name='GPView'),

    path('DamageItemView/', DamageItemView.as_view(), name='DamageItemView'),
    path('DamageInvoiceView/<int:id>/', DamageInvoiceView.as_view(), name='DamageInvoiceView'),
    path('DamageProductView/<int:id>/', DamageProductView.as_view(), name='DamageProductView'),
    path('DamageReportView/', DamageReportView.as_view(), name='DamageReportView'),

    path('ExpenseLedgerView/<int:id>', ExpenseLedgerView.as_view(), name='ExpenseLedgerView'),
    path('LedgerImport/', LedgerImport.as_view(), name='LedgerImport'),
    path('ExpenseReportView/', ExpenseReportView.as_view(), name='ExpenseReportView'),
    path('ExpenseReportFilter/', ExpenseReportFilter.as_view(), name='ExpenseReportFilter'),
    path('LedgerCreateView/', LedgerCreateView.as_view(), name='LedgerCreateView'),

    path('', DashboardView.as_view(), name='DashboardView'),
    path('testbarcode/', testbarcode.as_view(), name='testbarcode'),


]
