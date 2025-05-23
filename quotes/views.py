from django.shortcuts import render
import random

QUOTES = [
    "A person who never made a mistake never tried anything new.",
    "Intellectuals solve problems; geniuses prevent them.",
    "The hardest thing in the world to understand is the income tax.",
    "I am convinced that He (God) does not play dice.",
    "I never think of the future. It comes soon enough.",
    "The value of a man resides in what he gives and not in what he is capable of receiving.",
    "Try not to become a man of success, but rather try to become a man of value."
]

IMAGES = [
    "https://upload.wikimedia.org/wikipedia/commons/a/ad/Albert_Einstein_as_a_child.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/1/14/Albert_Einstein_1947.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/2/26/Einstein_patentoffice_full_%28cropped%29.jpg"
]

def quote(request):
    context = {
        "quote": random.choice(QUOTES),
        "image": random.choice(IMAGES),
    }
    return render(request, "quotes/quote.html", context)

def show_all(request):
    context = {
        "quotes": QUOTES,
        "images": IMAGES
    }
    return render(request, "quotes/show_all.html", context)

def about(request):
    return render(request, "quotes/about.html")
