from django.contrib import admin
from django.utils.html import format_html
from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):

    list_display = (
        'cover_image',
        'title',
        'author',
    )

    search_fields = (
        'title',
        'author',
    )

    list_per_page = 20

    show_full_result_count = False


    def cover_image(self, obj):

        if obj.image_url:

            return format_html(
                '<img src="{}" style="width:45px;height:auto;border-radius:6px;" />',
                obj.image_url
            )

        return "No Image"

    cover_image.short_description = 'Cover'