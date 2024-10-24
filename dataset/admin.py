from django.contrib import admin
from .models import Dataset

@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'price', 'creator', 'is_verified', 'created_at']
    list_filter = ['category', 'is_verified', 'license_type']
    search_fields = ['title', 'description']
    date_hierarchy = 'created_at'