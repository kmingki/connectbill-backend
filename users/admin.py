from django.contrib import admin
from .models import *


admin.site.register(User)
admin.site.register(Designer)

admin.site.register(Client)

admin.site.register(Message)


