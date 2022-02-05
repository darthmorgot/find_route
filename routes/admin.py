from django.contrib import admin

from routes.models import Route


class RouteAdmin(admin.ModelAdmin):
    class Meta:
        model = Route

    list_display = ['name', 'from_city', 'to_city', 'travel_times']


admin.site.register(Route, RouteAdmin)
