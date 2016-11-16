from django.contrib import admin


from . import models


class ItemAdmin(admin.ModelAdmin):
    # fields = ( 'image_tag', )
    readonly_fields = ('image_tag', )

admin.site.register(models.Receipt)
admin.site.register(models.Item, ItemAdmin)