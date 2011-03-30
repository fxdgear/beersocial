from django.contrib import admin

from beersocial.beers.models import Beer, Brewery, BeerType

class BeerAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

class BreweryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

class BeerTypeAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Beer, BeerAdmin)
admin.site.register(Brewery, BreweryAdmin)
admin.site.register(BeerType, BeerTypeAdmin)
