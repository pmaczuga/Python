from django.contrib import admin

from .models import Category, Thread, Answer

admin.site.register(Category)
admin.site.register(Thread)
admin.site.register(Answer)

# Register your models here.
