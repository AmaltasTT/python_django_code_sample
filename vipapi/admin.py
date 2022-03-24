from django.contrib import admin
from .models import VipWinner, RegisterVIP, PersonalInfo, PhotoPortfolio, DescribeYourself, ApplicantStatus, Messages, PhotoStory
from .forms import RegisterVIPForm
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _

# Register your models here.
admin.site.register(PhotoStory)
admin.site.register(VipWinner)
admin.site.register(PersonalInfo)
admin.site.register(PhotoPortfolio)
admin.site.register(DescribeYourself)
admin.site.register(ApplicantStatus)
admin.site.register(Messages)

@admin.register(RegisterVIP)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

#Customising the admin site - look and feel:
admin.site.site_header = 'VIPNAMES Administration'
admin.site.index_template = 'admin/vipindex.html'
admin.autodiscover()        
