from django.contrib import admin
from .models import WeatherSearch

@admin.register(WeatherSearch)
class WeatherSearchAdmin(admin.ModelAdmin):
    list_display = ['city', 'country', 'temperature', 'description', 'searched_at']
    list_filter = ['country', 'searched_at']
    search_fields = ['city', 'country']
    readonly_fields = ['searched_at']
    
    def has_add_permission(self, request):
        return False  # Disable adding through admin