from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.db.models import Sum
from django.http import HttpResponse
from django.views.generic import TemplateView, View, CreateView, DetailView,FormView
from django.urls import reverse_lazy

from .forms import *
from .models import *
# Create your views here.
def test(request):
    return render(request, 'base.html')
# ===================================================User Log In ===============================
class UserRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            pass
        else:
            return redirect('myapp:UserLoginView')
        return super().dispatch(request, *args, **kwargs)


class UserLoginView(FormView):
    template_name = 'login.html'
    form_class = ULoginForm
    success_url = reverse_lazy('myapp:HomeView')

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data['password']
        usr = authenticate(username=username, password=password)

        if usr is not None:
            login(self.request, usr)

        else:
            return render(self.request, self.template_name, {'form': self.form_class, 'error': 'Invalid user login!'})
        return super().form_valid(form)

class UserLogoutView(View):
    def get(self,request):
        logout(request)
        return redirect('myapp:UserLoginView')


# ================================= end user log in ===========================================
class HomeView(UserRequiredMixin,TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_list'] = Items.objects.all().order_by('-id')
        return context



class AddToCartView(UserRequiredMixin,TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
    #     # prouduct id get from request url
        product_id = self.kwargs['pro_id']

        # get product
        product_obj = Items.objects.get(id=product_id)


        # check it cart exist
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            this_product_in_cart = cart_obj.cartproduct_set.filter(product=product_obj)
            # Product already exists in cart
            if this_product_in_cart.exists():
                cartproduct = this_product_in_cart.last()
                cartproduct.quantity += 1
                cartproduct.subtotal += product_obj.sell_price
                cartproduct.remain_balance -=1

                cartproduct.save()
                cart_obj.total += product_obj.sell_price
                cart_obj.tax = cart_obj.total * 0.05
                cart_obj.super_total = cart_obj.tax + cart_obj.total
                cart_obj.save()
                cartproduct_balance = cartproduct.remain_balance
                item_update = Items.objects.filter(id=product_id).update(balance_qty=cartproduct_balance)
            # New item added in cart
            else:
                item_filter = Items.objects.filter(id=product_id)
                balance_filter = item_filter[0].balance_qty
                cartproduct_balance = balance_filter-1
                cartproduct = CartProduct.objects.create(cart=cart_obj, product=product_obj,
                                                         rate=product_obj.sell_price, quantity=1,
                                                         subtotal=product_obj.sell_price,remain_balance=cartproduct_balance)

                item_update = Items.objects.filter(id=product_id).update(balance_qty=cartproduct_balance)

                cart_obj.total += product_obj.sell_price
                cart_obj.tax = cart_obj.total * 0.05
                cart_obj.super_total = cart_obj.tax + cart_obj.total
                cart_obj.save()
        else:
            cart_obj = Cart.objects.create(total=0)
            self.request.session['cart_id'] = cart_obj.id
            item_filter = Items.objects.filter(id=product_id)
            balance_filter = item_filter[0].balance_qty
            cartproduct_balance = balance_filter - 1
            cartproduct = CartProduct.objects.create(cart=cart_obj, product=product_obj, rate=product_obj.sell_price,
                                                     quantity=1, subtotal=product_obj.sell_price,remain_balance=cartproduct_balance)
            cart_obj.total += product_obj.sell_price
            cart_obj.tax = cart_obj.total * 0.05
            cart_obj.super_total = cart_obj.tax + cart_obj.total
            cart_obj.save()

    #     # if product already exist
        context['product_list'] = Items.objects.all().order_by('-id')
        return context

class MyCartView(UserRequiredMixin,TemplateView):
    template_name = 'mycartview.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get('cart_id', None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
        else:
            cart = None
        context['cart'] = cart
        return context



class ManageCartView(UserRequiredMixin,View):
    def get(self, request, *args, **kwargs):

        cp_id = kwargs['cp_id']
        action = request.GET.get('action')
        cp_obj = CartProduct.objects.get(id=cp_id)
        cart_obj = cp_obj.cart

        if action == "inc":
            cp_obj.quantity +=1
            cp_obj.remain_balance -=1
            cp_obj.subtotal += cp_obj.rate
            cp_obj.save()
            cart_obj.total +=cp_obj.rate
            cart_obj.tax = cart_obj.total * 0.05
            cart_obj.super_total = cart_obj.tax + cart_obj.total
            cart_obj.save()
        elif action == 'dcr':
            cp_obj.quantity -= 1
            cp_obj.remain_balance += 1
            item_balance = cp_obj.remain_balance
            item_update = Items.objects.filter(id=cp_obj.product.id).update(balance_qty=item_balance)
            cp_obj.subtotal -= cp_obj.rate
            cp_obj.save()
            cart_obj.total -= cp_obj.rate
            cart_obj.tax = cart_obj.total * 0.05
            cart_obj.super_total = cart_obj.tax + cart_obj.total
            cart_obj.save()
            if cp_obj.quantity == 0:
                cp_obj.delete()
        elif action == 'rmv':
            cart_obj.total -= cp_obj.subtotal
            # cp_obj.remain_balance += cp_obj.quantity
            item_balance = cp_obj.remain_balance +cp_obj.quantity

            item_update = Items.objects.filter(id=cp_obj.product.id).update(balance_qty=item_balance)
            cart_obj.tax = cart_obj.total * 0.05
            cart_obj.super_total = cart_obj.tax + cart_obj.total
            cart_obj.save()
            cp_obj.delete()
        else:
            pass
        return redirect('myapp:MyCartView')


class EmptyCartView(UserRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        cart_id = request.session.get("cart_id", None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
            cart.cartproduct_set.all().delete()
            cart.total =0
            cart.tax = 0
            cart.super_total=0
            cart.save()
        return redirect('myapp:MyCartView')



class CheckoutView(UserRequiredMixin,CreateView):
    template_name = 'checkout.html'
    form_class = CheckoutForm
    success_url = reverse_lazy('myapp:HomeView')

    # def dispatch(self, request, *args, **kwargs):
    #     if request.user.is_authenticated and request.user.customer:
    #         print('login....')
    #     else:
    #         return redirect('/login/?next=/checkout/')
    #     return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
        else:
            cart_obj = None
        context['cart'] = cart_obj
        return context

    def form_valid(self, form):
        cart_id = self.request.session.get('cart_id')
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            form.instance.cart = cart_obj
            form.instance.subtotal = cart_obj.total
            form.instance.discount = 0
            form.instance.total = cart_obj.total
            # form.instance.ordered_staus = 'Cash'
            form.instance.tax = cart_obj.tax
            form.instance.all_total = cart_obj.super_total

            del self.request.session['cart_id']
        else:
            return redirect('myapp:HomeView')
        return super().form_valid(form)


#Product Edit
class ProductEditView(UserRequiredMixin,View):
    def get(self,request, pk):
        pi = Items.objects.get(id=pk)
        fm = AdminProductEditForm(instance=pi)
        return render(request,'productedit.html', {'form':fm})

    def post(self, request, pk):
        pi = Items.objects.get(id=pk)
        fm = AdminProductEditForm(request.POST,instance=pi)
        if fm.is_valid():
            fm.save()
        return redirect('myapp:HomeView')

class ProductCreate(View):
    def get(self,request):
        category = Category.objects.all()
        item_list = Items.objects.all()
        message = None
        context = {'item_list':item_list,'category':category,'message':message}
        return render(request, 'productcreate.html', context)
    def post(self,request):
        item_name = request.POST.get('item_name')
        category = request.POST.get('category')
        purchase_price = request.POST.get('purchase_price')
        sale_price = request.POST.get('sale_price')
        message = None
        if not item_name:
            message = 'please enter item'
        if not message:
            item = Items(item_name=item_name,category=category,pruchase_price=purchase_price,sell_price=sale_price)
            item.save()
            return redirect(request.META['HTTP_REFERER'])
        else:
            category = Category.objects.all()
            item_list = Items.objects.all()
            context = {'message': message,'category':category,'item_list':item_list}
            return render(request, 'productcreate.html', context)

class CategoryCreate(View):
    def get(self,request):
        category = Category.objects.all()
        item_list = Items.objects.all()
        message = None
        context = {'item_list': item_list, 'category': category, 'message': message}
        return render(request, 'categorycreate.html', context)
    def post(self,request):
        category_name = request.POST.get('category_name')
        message = None
        if not category_name:
            message = 'please enter category name'
        if not message:
            cate = Category(category_name=category_name)
            cate.save()
            return redirect(request.META['HTTP_REFERER'])
        else:
            category = Category.objects.all()
            message = 'please enter category name'
            return render(request, 'categorycreate.html', {'message':message,'category':category})


# ================== report =============
class SaleInvoiceView(UserRequiredMixin,View):
    def get(self,request):
        # form = StockHistorySearchForm()
        queryset = Order.objects.all().order_by('-id')
        order_status = Order.objects.filter(ordered_staus='Ordering')
        sum = queryset.aggregate(Sum('all_total'))
        sum_amt = sum['all_total__sum']
        context = {
            'order_status': order_status,
            'saleinvoice': queryset,
            'sum_amt': sum_amt,
        }
        return render(request, 'invoicelist.html', context)

######## Supplier ##############
class SupplierCreate(View):
    def get(self,request):
        supplier = Supplier.objects.all()
        context = {'supplier':supplier}
        return render(request,'supplier.html', context)
    def post(self,request):
        supplier_name = request.POST.get('supplier_name')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        message = None
        if not supplier_name:
            message = 'Please Enter Supplier Name'
        elif not phone_number:
            message = 'Please Enter Phone Number'
        elif not address:
            message = 'Enter Address'
        if not message:
            supplier_save = Supplier(supplier_name=supplier_name,phone_number=phone_number,address=address)
            supplier_save.save()
            success = 'Supplier Name create successfully'
            supplier = Supplier.objects.all()
            context = {'supplier': supplier,'success':success}
            return render(request, 'supplier.html', context)
        else:
            supplier = Supplier.objects.all()
            context = {'supplier': supplier, 'message': message}
            return render(request, 'supplier.html', context)

class SupplierEdit(UserRequiredMixin,View):
    def get(self,request, pk):
        pi = Supplier.objects.get(id=pk)
        fm = SupplierEditForm(instance=pi)
        return render(request,'supplieredit.html', {'form':fm})

    def post(self, request, pk):
        pi = Supplier.objects.get(id=pk)
        fm = SupplierEditForm(request.POST,instance=pi)
        if fm.is_valid():
            fm.save()
        return redirect('myapp:SupplierCreate')


class PurchaseCreateView(TemplateView):
    template_name = 'purchase_create_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #     # supplier id get from request url
        supplier_id = self.kwargs['id']
        # get car info
        supplier_data = Supplier.objects.get(id=supplier_id)

        context['supplier'] = Supplier.objects.get(id=supplier_id)
        context['item'] = Items.objects.all()
        context['supplier_list'] = PurchaseList.objects.filter(supplier_name=supplier_data.supplier_name)

        return context



class PurchaseData(View):
    def get(self,request):
        supplier = Supplier.objects.all()
        purchasedata = PurchaseList.objects.all()
        sum_purchase_qty = purchasedata.aggregate(Sum('purchase_qty'))['purchase_qty__sum']
        sum_purchase_price = purchasedata.aggregate(Sum('purchase_price'))['purchase_price__sum']
        context = {'supplier': supplier,'purchasedata':purchasedata,'sum_purchase_qty':sum_purchase_qty,'sum_purchase_price':sum_purchase_price}
        return render(request, 'purchasedata.html',context)
    def post(self,request):
        suppliername = request.POST.get('suppliername')
        p_date = request.POST.get('p_date')
        item_name = request.POST.get('item_name')
        purchase_qty = request.POST.get('purchase_qty')
        purchase_price = request.POST.get('purchase_price')
        sale_price = request.POST.get('sale_price')
        message = None
        if not p_date:
            message = 'please select Date'
        elif not item_name:
            message = 'please select Item'
        elif not purchase_qty:
            message = 'please enter quantity'
        elif not purchase_price:
            message = 'please enter purchase price'
        if not message:
            purchase_list = PurchaseList(
                supplier_name=suppliername,
                item_name=item_name,
                purchase_qty=purchase_qty,
                purchase_price=purchase_price,
                sale_price=sale_price,
                p_date=p_date
            )
            purchase_list.save()
            item_balance = Items.objects.filter(item_name=item_name)
            balance_qty = item_balance[0].balance_qty
            total_balance = int(balance_qty)+int(purchase_qty)
            item_update = Items.objects.filter(item_name=item_name).update(pruchase_price=purchase_price,sell_price=sale_price,balance_qty=total_balance)
            return redirect(request.META['HTTP_REFERER'])
        else:
            context = {'message':message}
            # return redirect(request.META['HTTP_REFERER'])
            return render(request,'purchase_create_view.html',context)

class PurchaseReport(View):
    def post(self,request):
        fromdate = request.POST.get('fromdate')
        todate = request.POST.get('todate')
        message = None
        if not fromdate:
            message='select from date'
        elif not todate:
            message = 'select to date'
        if not message:
            supplier = Supplier.objects.all()
            purchasedata = PurchaseList.objects.filter(p_date__range=[fromdate, todate])
            sum_purchase_qty = purchasedata.aggregate(Sum('purchase_qty'))['purchase_qty__sum']
            sum_purchase_price = purchasedata.aggregate(Sum('purchase_price'))['purchase_price__sum']
            context = {'supplier': supplier, 'purchasedata': purchasedata, 'sum_purchase_qty': sum_purchase_qty,
                       'sum_purchase_price': sum_purchase_price}
            return render(request, 'purchasedata.html', context)
        else:
            supplier = Supplier.objects.all()
            context = {'supplier': supplier, 'message':message}
            return render(request, 'purchasedata.html', context)

