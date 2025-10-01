from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Category, Photo, Package, Booking, Personality, PersonalityImage

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'featured', 'date_added')
    list_filter = ('category', 'featured')
    search_fields = ('title', 'description')

class PersonalityImageInline(admin.TabularInline):
    model = PersonalityImage
    extra = 3

@admin.register(Personality)
class PersonalityAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_added')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [PersonalityImageInline]

@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'date', 'package', 'status', 'created_at')
    list_filter = ('status', 'date', 'package')
    search_fields = ('name', 'email')
