from django.contrib import admin
from .models import tasktodo

# Register your models here.
class TodoAdmin(admin.ModelAdmin):
    readonly_fields = ('created', )

admin.site.register(tasktodo, TodoAdmin)