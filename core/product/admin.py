from django.contrib import admin

# Register your models here.
from .models import Brand, Category, Product, ProductLine


class ProductLineInline(admin.TabularInline):
    model = ProductLine


""" registering Products with the below decorator and the
 above TabularInline class will allow for the display and
 edit of the productline fields from the product admin page
 see product page on admin site.  This essentially displays 
 all the models that has a relationshop with products + allows
 for creation and edit of a product instance in one place """


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductLineInline]


admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(ProductLine)
# admin.site.register(Product)
