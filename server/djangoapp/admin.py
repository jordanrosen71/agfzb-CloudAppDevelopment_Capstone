from django.contrib import admin
from .models import CarMake, CarModel

# CarModelInline class
class CarModelInline(admin.TabularInline):
    model = CarModel
    extra = 1  # Number of empty forms to display

# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'dealer_id', 'car_type', 'year')  # Columns to display in admin view
    list_filter = ['car_type']  # Filtering options in the sidebar
    search_fields = ['name', 'dealer_id']  # Search fields

# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]  # This will let you add/edit CarModel entries directly from the CarMake page.
    list_display = ('name', 'description')
    search_fields = ['name']

# Register models here
admin.site.register(CarModel, CarModelAdmin)
admin.site.register(CarMake, CarMakeAdmin)
