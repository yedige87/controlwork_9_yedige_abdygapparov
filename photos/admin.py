from django.contrib import admin

# Register your models here.
from .models import Photo


# Register your models here.
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'description', 'image', 'date_publish')
    list_filter = ('id', 'author', 'description', 'image', 'date_publish')
    search_fields = ('author', 'description')
    fields = ('author', 'description', 'image', 'date_publish')
    readonly_fields = ('id', 'date_publish', 'date_update')


admin.site.register(Photo, PhotoAdmin)