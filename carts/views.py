from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render, get_object_or_404

from products.models import Variation
from .models import Cart, CartItem

# Create your views here.

class ItemCountView(View):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            cart_id = self.request.session.get("cart_id")
            if cart_id == None:
                count = 0
            else:
                cart = Cart.objects.get(id=cart_id)
                count = cart.items.count()
            self.request.session["cart_item_count"] = count
            return JsonResponse({"count": count})
        else:
            return Http404


class CartView(SingleObjectMixin, View):
    model = Cart
    template_name = 'carts/view.html'

    def get_object(self, *args, **kwargs):
        self.request.session.set_expiry(0)  # in seconds..but if 0,session ends when user closes the web browser
        cart_id = self.request.session.get("cart_id")
        if cart_id == None:
            cart = Cart()
            # cart.tax_percentage=0.1
            cart.save()
            cart_id = cart.id
            self.request.session["cart_id"] = cart.id
        cart = Cart.objects.get(id=cart_id)
        if self.request.user.is_authenticated():
            cart.user = self.request.user
            cart.save()
        return cart

    def get(self, request, *args, **kwargs):
        cart = self.get_object()
        item_id = request.GET.get("item")
        delete_item = request.GET.get("delete", False)
        item_added = False
        flash_message = ""
        if item_id:
            item_instance = get_object_or_404(Variation, id=item_id)
            qty = request.GET.get("qty", 1)
            try:
                if int(qty) < 1:
                    delete_item = True
            except:
                raise Http404
            cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item_instance)
            if created:
                item_added = True
                flash_message = cart_item.item.get_title() + " successfully added to the cart."
            if delete_item:
                flash_message = cart_item.item.get_title() + " removed successfully"
                cart_item.delete()
            else:
                if not created:
                    flash_message = "Quantity of " + cart_item.item.get_title() + " has been updated successfully."
                cart_item.quantity = qty
                cart_item.save()
            if not request.is_ajax():
                return HttpResponseRedirect(reverse("cart"))
                # return cart_item.cart.get_absolute_url()

        if request.is_ajax():
            try:
                total = cart_item.line_item_total
            except:
                total = None
            try:
                subtotal = cart_item.cart.subtotal
            except:
                subtotal = None
            try:
                total_items = cart_item.cart.items.count()
            except:
                total_items = 0
            try:
                cart_total = cart_item.cart.total
            except:
                cart_total = None
            try:
                tax_total = cart_item.cart.tax_total
            except:
                tax_total = None
            data = {
            "deleted": delete_item,
            "item_added": item_added,
            "line_total": total,
            "subtotal": subtotal,
            "cart_total": total,
            "tax_total": tax_total,
            "flash_message": flash_message,
            "total_items": total_items,

            }
            return JsonResponse(data)

        context = {
        "object": self.get_object()
        }
        template = self.template_name
        return render(request, template, context)

