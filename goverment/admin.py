from django.contrib import admin
from django.utils.html import format_html
from .models import Ministry, Minister, Department, UserProfile


class DepartmentInline(admin.TabularInline):
    model = Department
    extra = 1


class MinisterInline(admin.TabularInline):
    model = Minister
    fields = ('first_name', 'last_name', 'position', 'appointment_date')
    extra = 1


@admin.register(Ministry)
class MinistryAdmin(admin.ModelAdmin):
    list_display = ('name', 'established_date', 'website_link', 'minister_count')
    list_filter = ('established_date',)
    search_fields = ('name', 'description')
    date_hierarchy = 'established_date'
    inlines = [MinisterInline, DepartmentInline]

    def website_link(self, obj):
        if obj.website:
            return format_html('<a href="{}" target="_blank">{}</a>', obj.website, obj.website)
        return '-'

    website_link.short_description = 'Rasmiy veb-sayt'

    def minister_count(self, obj):
        return obj.ministers.count()

    minister_count.short_description = 'Vazirlar soni'


@admin.register(Minister)
class MinisterAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'position', 'ministry', 'appointment_date', 'display_photo')
    list_filter = ('ministry', 'gender', 'appointment_date')
    search_fields = ('first_name', 'last_name', 'position', 'ministry__name')
    date_hierarchy = 'appointment_date'
    fieldsets = (
        ('Shaxsiy ma\'lumotlar', {
            'fields': ('first_name', 'last_name', 'middle_name', 'photo', 'birth_date', 'gender', 'biography')
        }),
        ('Lavozim ma\'lumotlari', {
            'fields': ('ministry', 'position', 'appointment_date')
        }),
        ('Aloqa ma\'lumotlari', {
            'fields': ('email', 'phone'),
            'classes': ('collapse',)
        }),
    )

    def full_name(self, obj):
        return f"{obj.last_name} {obj.first_name}"

    full_name.short_description = 'F.I.O.'

    def display_photo(self, obj):
        if obj.photo:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 50%;" />', obj.photo.url)
        return '-'

    display_photo.short_description = 'Rasm'


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'ministry', 'head')
    list_filter = ('ministry',)
    search_fields = ('name', 'description', 'head', 'ministry__name')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'address', 'display_photo')
    search_fields = ('user__username', 'user__email', 'phone', 'address')

    def display_photo(self, obj):
        if obj.photo:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 50%;" />', obj.photo.url)
        return '-'

    display_photo.short_description = 'Rasm'


# Admin site customization
admin.site.site_header = "O'zbekiston Respublikasi Hukumati - Admin paneli"
admin.site.site_title = "O'zbekiston Respublikasi Hukumati"
admin.site.index_title = "Boshqaruv paneli"