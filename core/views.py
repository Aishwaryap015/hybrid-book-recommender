from .recommender import BookRecommender
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import (
    login,
    authenticate,
    logout,
    get_user_model
)
from django.views.decorators.csrf import csrf_exempt

from pymongo import MongoClient

import json
import random

User = get_user_model()

# =========================================================
# MONGODB CONNECTION
# =========================================================

client = MongoClient("mongodb://localhost:27017/")

# Your actual MongoDB database name
db = client["book_recommender_db"]

# Your actual collection name
books_collection = db["core_book"]

ratings_collection = db["ratings"]

recommender = BookRecommender()

# =========================================================
# FILTER HELPER
# =========================================================

def fetch_books_by_keywords(keywords, limit=20):

    regex_pattern = "|".join(keywords)

    return list(

        books_collection.find(

            {
                "$or": [

                    {
                        "title": {
                            "$regex": regex_pattern,
                            "$options": "i"
                        }
                    },

                    {
                        "author": {
                            "$regex": regex_pattern,
                            "$options": "i"
                        }
                    },

                    {
                        "category": {
                            "$regex": regex_pattern,
                            "$options": "i"
                        }
                    }
                ]
            },

            {
                "_id": 0
            }

        ).limit(limit)
    )

# =========================================================
# HOME PAGE
# =========================================================

def index(request):

    mongo_query = {}

    query = request.GET.get(
        "q",
        ""
    ).strip().lower()

    category = request.GET.get(
        "category",
        ""
    ).strip().lower()

    author = request.GET.get(
        "author",
        ""
    ).strip().lower()

    language = request.GET.get(
        "language",
        ""
    ).strip().lower()

    format_type = request.GET.get(
        "format",
        ""
    ).strip().lower()

    subcategory = request.GET.get(
        "subcategory",
        ""
    ).strip().lower()

    section = request.GET.get(
        "section",
        ""
    ).strip().lower()

    # =====================================================
    # SEARCH
    # =====================================================

    if query:

        mongo_query["title"] = {

            "$regex": query,
            "$options": "i"
        }

    # =====================================================
    # CATEGORY
    # =====================================================

    if category:

        mongo_query["category"] = category

    # =====================================================
    # AUTHOR
    # =====================================================

    if author:

        mongo_query["author"] = {

            "$regex": author,
            "$options": "i"
        }

    # =====================================================
    # LANGUAGE
    # =====================================================

    if language:

        mongo_query["language"] = language

    # =====================================================
    # FORMAT
    # =====================================================

    if format_type:

        mongo_query["format"] = format_type

    # =====================================================
    # SUBCATEGORY
    # =====================================================

    if subcategory:

        mongo_query["category"] = {

            "$regex": subcategory,
            "$options": "i"
        }

    # =====================================================
    # FETCH FILTERED BOOKS
    # =====================================================

    filtered_books = list(

        books_collection.find(
            mongo_query,
            {
                "_id": 0
            }
        ).limit(100)
    )

    # =====================================================
    # DISTRIBUTED SECTIONS
    # =====================================================

    sections = {

        "top_local_vibes":

            list(

                books_collection.find(
                    {},
                    {"_id": 0}
                ).limit(20)
            ),

        "youth_bestsellers":

            fetch_books_by_keywords(
                ["young", "youth", "teen", "school"]
            ),

        "spiritual_books":

            fetch_books_by_keywords(
                ["mythology", "god", "legend"]
            ),

        "mystery":

            fetch_books_by_keywords(
                ["mystery", "detective", "secret"]
            ),

        "leadership":

            fetch_books_by_keywords(
                ["leader", "leadership", "management"]
            ),

        "crime":

            fetch_books_by_keywords(
                ["crime", "killer", "murder"]
            ),

        "children_favorites":

            fetch_books_by_keywords(
                ["children", "kids", "child"]
            ),

        "old_age":

            fetch_books_by_keywords(
                [
                    "old",
                    "elder",
                    "grandfather",
                    "grandmother",
                    "aging",
                    "retirement"
                ]
            ),

        "struggle_journey":

            fetch_books_by_keywords(
                [
                    "journey",
                    "struggle",
                    "life",
                    "dream",
                    "survival",
                    "hope",
                    "fight"
                ]
            ),

        "trending":

            list(

                books_collection.find(
                    {},
                    {"_id": 0}
                ).skip(20).limit(20)
            ),

        "top_rated":

            list(

                books_collection.find(
                    {},
                    {"_id": 0}
                ).sort(
                    "rating",
                    -1
                ).limit(50)
            )
    }

    # =====================================================
    # SEE ALL
    # =====================================================

    if section and section in sections:

        filtered_books = sections[section]

    # =====================================================
    # USER PERSONALIZATION
    # =====================================================

    recently_viewed = []

    personalized_books = []

    if request.user.is_authenticated:

        recently_viewed = getattr(
            request.user,
            "recently_viewed",
            []
        ) or []

        preferences = getattr(
            request.user,
            "reading_preferences",
            []
        ) or []

        if preferences:

            personalized_books = list(

                books_collection.find(

                    {
                        "category": {
                            "$in": preferences
                        }
                    },

                    {
                        "_id": 0
                    }

                ).limit(20)
            )

        else:

            personalized_books = list(

                books_collection.find(
                    {},
                    {"_id": 0}
                ).limit(10)
            )

# ==================================
# HOMEPAGE RECOMMENDATIONS
# ==================================

    recommended_books = []

    visited_book = request.session.get(
        "last_visited_book"
    )

    if visited_book:

        recommendations = (
            recommender.get_recommendations(
                book_title=visited_book,
                num_books=8
            )
        )

        for title in recommendations:

            rec_book = (
                books_collection.find_one(
                    {
                        "title": title
                    },
                    {
                        "_id": 0
                    }
                )
            )

            if rec_book:

                rec_book["image_url_l"] = (
                    rec_book.get(
                        "image_url",
                        ""
                    )
                )

                recommended_books.append(
                    rec_book
                )

    return render(

        request,

        "index.html",

        {

            "all_books":
                filtered_books,

            "recommended_books":
                recommended_books,

            "visited_book":
                visited_book,

            "query":
                query,

            "category":
                category,

            "author":
                author,

            "language":
                language,

            "format":
                format_type,

            "subcategory":
                subcategory,

            "section":
                section,
        }
    )


# =========================================================
# REGISTER
# =========================================================

@csrf_exempt
def register_view(request):

    if request.method == "POST":

        try:

            payload = json.loads(
                request.body
            )

            email = payload.get(
                "email"
            )

            password = payload.get(
                "pass"
            )

            first_name = payload.get(
                "first",
                ""
            )

            last_name = payload.get(
                "last",
                ""
            )

            if not email or not password:

                return JsonResponse({

                    "status":
                        "error",

                    "message":
                        "Email and password are required"

                }, status=400)

            if User.objects.filter(
                email=email
            ).exists():

                return JsonResponse({

                    "status":
                        "error",

                    "message":
                        "Email already exists"

                }, status=400)

            user = User.objects.create_user(

                username=email,

                email=email,

                password=password,

                first_name=first_name,

                last_name=last_name
            )

            login(
                request,
                user
            )

            return JsonResponse({

                "status":
                    "success",

                "initials":
                    user.username[:2].upper()
            })

        except Exception as e:

            return JsonResponse({

                "status":
                    "error",

                "message":
                    str(e)

            }, status=400)

    return JsonResponse({

        "status":
            "error"

    }, status=400)
# =========================================================
# LOGIN
# =========================================================

@csrf_exempt
def login_view(request):

    if request.method == "POST":

        try:

            payload = json.loads(request.body)

            username = payload.get("username")

            password = payload.get("password")

            user = authenticate(

                username=username,

                password=password
            )

            if user is not None:

                login(request, user)

                return JsonResponse({

                    "status": "success",

                    "initials":
                        user.username[:2].upper()
                })

            return JsonResponse({

                "status": "error",

                "message": "Invalid credentials"

            }, status=401)

        except Exception as e:

            return JsonResponse({

                "status": "error",

                "message": str(e)

            }, status=400)

    return JsonResponse({

        "status": "error"

    }, status=400)

# =========================================================
# GUEST LOGIN
# =========================================================

@csrf_exempt
def guest_login_view(request):

    try:

        user, created = User.objects.get_or_create(

            username="guest_user@example.com",

            defaults={

                "email":
                    "guest_user@example.com",

                "first_name":
                    "Guest",

                "is_guest":
                    True
            }
        )

        if created:

            user.set_password("Guest@123")

            user.save()

        login(request, user)

        return JsonResponse({

            "status": "success",

            "initials": "G"
        })

    except Exception as e:

        return JsonResponse({

            "status": "error",

            "message": str(e)

        }, status=400)

# =========================================================
# LOGOUT
# =========================================================

def logout_view(request):

    logout(request)

    return redirect("index")

# =========================================================
# BOOK DETAIL PAGE
# =========================================================

def book_detail(request, id):

    global recommender

    if recommender is None:
        recommender = BookRecommender()

    book = books_collection.find_one(
        {
            "id": int(id)
        },
        {
            "_id": 0
        }
    )

    if not book:
        return redirect("/")

    # ==================================
    # GET BOOK TITLE + ISBN
    # ==================================

    book_title = book.get("title", "")
    # Save last visited book
    request.session[
    "last_visited_book"
] = book_title

    
    book_isbn = book.get("isbn", "")
    print("\nBOOK TITLE:", book_title)
    print("BOOK ISBN:", book_isbn)

    # ==================================
    # GET RECOMMENDATIONS
    # ==================================

    recommended_titles = (
    recommender.get_recommendations(
        book_title=book_title,
        book_isbn=book_isbn,
        num_books=8
    )
)

    # ==================================
    # FETCH FULL BOOK DATA
    # ==================================

    recommended_books = []

    for title in recommended_titles:

        recommended_book = (
            books_collection.find_one(
                {
    "title": title
},
                {
                    "_id": 0
                }
            )
        )

        if recommended_book:

            # Fix image key for Django template
            recommended_book["image_url_l"] = (
    recommended_book.get(
        "image_url",
        ""
    )
)

            recommended_books.append(
                recommended_book
            )
        
    return render(
        request,
        "book_detail.html",
        {
            "book": book,
            "recommended_books": recommended_books,
            "user": request.user
            
        }
    )
# =========================================================
# SECTION PAGE
# =========================================================

def section_page(request, section_name):

    sections = {

        "top-local-vibes":

            list(
                books_collection.find(
                    {},
                    {"_id": 0}
                ).limit(20)
            ),

        "youth-bestsellers":

            fetch_books_by_keywords(
                ["young", "youth", "teen"]
            ),

        "mystery-vault":

            fetch_books_by_keywords(
                ["mystery", "detective"]
            ),

        "leadership":

            fetch_books_by_keywords(
                ["leader", "management"]
            ),

        "mythology":

            fetch_books_by_keywords(
                ["mythology", "god"]
            ),

        "crime-chronicles":

            fetch_books_by_keywords(
                ["crime", "killer"]
            ),

        "top-rated":

            list(

                books_collection.find(
                    {},
                    {"_id": 0}
                ).sort(
                    "rating",
                    -1
                ).limit(50)
            )
    }

    books = sections.get(section_name, [])

    return render(

        request,

        "section_page.html",

        {
            "books": books,

            "section_name":
                section_name.replace("-", " ").title()
        }
    )

# =========================================================
# RATE BOOK API
# =========================================================

from bson import ObjectId

@csrf_exempt
def rate_book(request):

    if request.method != "POST":
        return JsonResponse({
            "status": "error",
            "message": "POST request required"
        })

    try:
        data = json.loads(request.body)

        book_id = str(data.get("book_id"))
        rating = int(data.get("rating"))
        review = data.get("review", "")

        if not request.user.is_authenticated:
            return JsonResponse({
                "status": "error",
                "message": "Please login first"
            })

        user_id = str(request.user.id)

        ratings_collection.update_one(

            {
                "user_id": user_id,
                "book_id": book_id
            },

            {
                "$set": {
                    "user_id": user_id,
                    "book_id": book_id,
                    "rating": rating,
                    "review": review
                },

                "$setOnInsert": {
                    "_id": str(ObjectId())
                }
            },

            upsert=True
        )

        return JsonResponse({
            "status": "success",
            "message": "Rating submitted successfully"
        })

    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": str(e)
        })

        # =====================================
        # CALCULATE AVG RATING
        # =====================================

        ratings = list(

            ratings_collection.find({

                "book_id": book_id

            })
        )

        avg_rating = sum(

            r["rating"]

            for r in ratings

        ) / len(ratings)

        avg_rating = round(avg_rating, 1)

        # =====================================
        # UPDATE BOOK AVG RATING
        # =====================================

        books_collection.update_one(

            {
                "id": int(book_id)
            },

            {
                "$set": {

                    "rating": avg_rating
                }
            }
        )

        return JsonResponse({

            "status": "success",

            "message": "Rating submitted successfully!",

            "average_rating": avg_rating
        })

    except Exception as e:

        return JsonResponse({

            "status": "error",

            "message": str(e)
        })