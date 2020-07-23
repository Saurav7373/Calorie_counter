from django.contrib import admin

from .models import Food, Diet, Meal

# Register your models here.
admin.site.register(Food)
admin.site.register(Diet)
admin.site.register(Meal)