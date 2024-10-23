from .models import FAQ
from datetime import timezone
from django.contrib import admin
from .models import *
from .models import IDVerification

# Register your models here.

from .models import Product, Garden, Service, Blog, Banner, Vote, Notification, Order, OrderItem, FAQ, FAQMainPage
# admin.site.register(AppUser)
admin.site.register(Product)


class ProductModelAdmin(admin.ModelAdmin):
    fields = ['name', 'desc', 'price', 'image', 'category', 'created_at']


admin.site.register(Category)
admin.site.register(Review)
admin.site.register(Farmer)

admin.site.register(Garden)


class GardenModelAdmin(admin.ModelAdmin):
    fields = ['name', 'location', 'size', 'description']


admin.site.register(Service)


class ServiceModelAdmin(admin.ModelAdmin):
    fields = ['type', 'description', 'price']


admin.site.register(Blog)


class BlogModelAdmin(admin.ModelAdmin):
    fields = ['id', 'title', 'content', 'slug',
              'image', 'created_at', 'updated_at']


admin.site.register(Poll)
admin.site.register(Vote)


class PollModelAdmin(admin.ModelAdmin):
    fields = ['id', 'title', 'description', 'votes']


admin.site.register(IDVerification)


class IDVerificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'id_document_type', 'id_document_number',
                    'is_verified', 'submitted_at', 'verified_at')
    list_filter = ('is_verified', 'id_document_type')
    search_fields = ('user__username', 'id_document_number')
    readonly_fields = ('submitted_at', 'verified_at', 'is_verified')
    fieldsets = (
        (None, {
            'fields': ('user', 'id_document_type', 'id_document_number', 'document_image', 'photo_image')
        }),
        ('Verification Info', {
            'fields': ('is_verified', 'submitted_at', 'verified_at')
        }),
    )

    def has_add_permission(self, request):
        # Prevents adding new verification records through the admin interface
        return False

    def has_delete_permission(self, request, obj=None):
        # Prevents deletion of verification records through the admin interface
        return False


# Banner for Marketplace

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'active', 'created_at')
    list_filter = ('active', 'created_at')
    search_fields = ('title',)


admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Notification)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1  # Allows you to add one extra item by default when creating an Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'customer_name', 'customer_email',
                    'total_price', 'payment_method', 'created_at')
    search_fields = ('order_id', 'customer_name', 'customer_email')
    list_filter = ('payment_method', 'created_at')
    # Allows adding/editing order items directly in the order admin page
    inlines = [OrderItemInline]
    # Make these fields read-only
    readonly_fields = ('order_id', 'created_at', 'updated_at')


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'product_price',
                    'product_quantity', 'order')
    search_fields = ('product_name',)


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question',)


# admin.py

@admin.register(FAQMainPage)
class FAQMainPageAdmin(admin.ModelAdmin):
    list_display = ['question']
    search_fields = ['question']


admin.site.register(Profile)
