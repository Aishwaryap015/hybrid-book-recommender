from django.db import models
from django.contrib.auth.models import AbstractUser


# =========================================================
# CUSTOM USER MODEL
# =========================================================

class DoodleUser(AbstractUser):

    # =========================
    # USER TYPES
    # =========================

    is_guest = models.BooleanField(
        default=False
    )

    # =========================
    # USER INTERESTS
    # =========================

    interests = models.JSONField(
        default=list,
        blank=True
    )

    # =========================
    # PROFILE STATS
    # =========================

    coins = models.IntegerField(
        default=50
    )

    books_read = models.IntegerField(
        default=0
    )

    # =========================
    # READING HISTORY
    # =========================

    recently_viewed = models.JSONField(
        default=list,
        blank=True
    )

    # =========================
    # USER ACTIVITY TRACKING
    # =========================

    most_visited_books = models.JSONField(
        default=dict,
        blank=True
    )

    most_visited_categories = models.JSONField(
        default=dict,
        blank=True
    )

    # =========================
    # PERSONALIZATION
    # =========================

    reading_preferences = models.JSONField(
        default=list,
        blank=True
    )

    favorite_sections = models.JSONField(
        default=list,
        blank=True
    )

    wishlist = models.JSONField(
        default=list,
        blank=True
    )

    reading_list = models.JSONField(
        default=list,
        blank=True
    )

    # =========================
    # LIBRARY SETTINGS
    # =========================

    preferred_theme = models.CharField(
        max_length=50,
        default="dark"
    )

    auto_sync_enabled = models.BooleanField(
        default=True
    )

    # =========================
    # USER METADATA
    # =========================

    last_active_section = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    profile_picture = models.URLField(
        max_length=1000,
        blank=True,
        null=True
    )

    # =========================
    # STRING REPRESENTATION
    # =========================

    def __str__(self):

        return (
            f"{self.username} "
            f"({'Guest' if self.is_guest else 'Member'})"
        )


# =========================================================
# BOOK MODEL
# =========================================================

class Book(models.Model):

    # =========================
    # BASIC DETAILS
    # =========================

    title = models.CharField(
        max_length=500
    )

    author = models.CharField(
        max_length=500
    )

    isbn = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    # =========================
    # CATEGORY & CLASSIFICATION
    # =========================

    category = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    subcategory = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    language = models.CharField(
        max_length=100,
        default="english"
    )

    format_type = models.CharField(
        max_length=100,
        default="book"
    )

    # =========================
    # MEDIA
    # =========================

    image_url = models.URLField(
        max_length=1000,
        blank=True,
        null=True
    )

    # =========================
    # BOOK METADATA
    # =========================

    description = models.TextField(
        blank=True,
        null=True
    )

    publisher = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    published_year = models.IntegerField(
        blank=True,
        null=True
    )

    rating = models.FloatField(
        default=0
    )

    pages = models.IntegerField(
        default=0
    )

    # =========================
    # LIBRARY STATS
    # =========================

    total_views = models.IntegerField(
        default=0
    )

    wishlist_count = models.IntegerField(
        default=0
    )

    reading_list_count = models.IntegerField(
        default=0
    )

    trending_score = models.IntegerField(
        default=0
    )

    # =========================
    # FEATURE FLAGS
    # =========================

    is_featured = models.BooleanField(
        default=False
    )

    is_top_rated = models.BooleanField(
        default=False
    )

    is_recommended = models.BooleanField(
        default=False
    )

    # =========================
    # TIMESTAMPS
    # =========================

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    # =========================
    # STRING REPRESENTATION
    # =========================

    def __str__(self):

        return self.title


# =========================================================
# BOOK RATINGS MODEL
# =========================================================

class BookRating(models.Model):

    user_id = models.CharField(
        max_length=255
    )

    book_id = models.CharField(
        max_length=255
    )

    rating = models.IntegerField()

    review = models.TextField(

        blank=True,

        null=True
    )

    created_at = models.DateTimeField(

        auto_now_add=True
    )

    def __str__(self):

        return f"{self.user_id} - {self.book_id}"