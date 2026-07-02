from django.contrib import admin
from django.urls import path

from core import views

urlpatterns = [

    path(
        'admin/',
        admin.site.urls
    ),

    path(
        '',
        views.index,
        name='index'
    ),

    path(
        'book/<int:id>/',
        views.book_detail,
        name='book_detail'
    ),

    path(
        'section/<str:section_name>/',
        views.section_page,
        name='section_page'
    ),

    path(
        'register/',
        views.register_view,
        name='register'
    ),

    path(
        'login/',
        views.login_view,
        name='login'
    ),

    path(
        'guest-login/',
        views.guest_login_view,
        name='guest_login'
    ),

    path(
        'rate-book/',
        views.rate_book,
        name='rate_book'
    ),

    path(
        'logout/',
        views.logout_view,
        name='logout'
    ),
]