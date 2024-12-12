from django.contrib import admin
from .models import Item, ItemCategory, ItemTag, User, Company


class UserAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        if form.cleaned_data.get('password') and not obj.pk:
            obj.set_password(form.cleaned_data['password'])
        obj.save()


admin.site.register(User, UserAdmin)
admin.site.register(Company)
admin.site.register(ItemCategory)
admin.site.register(ItemTag)
admin.site.register(Item)
