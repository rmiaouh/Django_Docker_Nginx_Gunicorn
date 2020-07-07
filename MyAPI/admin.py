from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Task)
admin.site.register(OrangeDB)
admin.site.register(RedDB)
admin.site.register(YellowDB)
admin.site.register(PinkDB)
admin.site.register(BlueDB)
admin.site.register(GreenDB)
