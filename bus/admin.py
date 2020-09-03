from django.contrib import admin
from .models import Bus_info, From_to, Cord,Station, Restaurant
# Register your models here.

class From_toAdmin(admin.ModelAdmin):
    list_display = ('From', 'To')


class Bus_infoAdmin(admin.ModelAdmin):
    list_display = ('bus_name', 'stoppage')


class CordAdmin(admin.ModelAdmin):
    list_display = ('From_to_id', 'From_to', 'coordinates')



class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('restaurant_location','restaurant_name', 'restaurant_link')
    list_filter = ['restaurant_location']
    

admin.site.register(From_to, From_toAdmin)
admin.site.register(Bus_info, Bus_infoAdmin)
admin.site.register(Cord, CordAdmin)
admin.site.register(Station)
admin.site.register(Restaurant, RestaurantAdmin)
