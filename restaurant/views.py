#File: views.py
#Author: Bella WANG (bella918@bu.edu), 5/23/2025
#Description: functions for the "Restaurant" Django app.
#             Includes logic for displaying a order, confirmation,
#             and rendering an about page.

from django.shortcuts import render
from datetime import datetime, timedelta
import random

# MENU
MENU_ITEMS = {
    'Pizza': 10,
    'Burger': 8,
    'Salad': 7,
    'Pasta': 9
}

# Daily rotating specials
DAILY_SPECIALS = {
    'Lobster Roll': 15,
    'Tuna Poke': 13,
    'BBQ Ribs': 20
}


def main(request):
    """
    View to render the main restaurant information page.
    """
    return render(request, 'restaurant/main.html')

def order(request):
    """
    View to render the online order form, including menu and a randomly selected daily special.
    """
    daily_special_item, daily_special_price = random.choice(list(DAILY_SPECIALS.items()))
    context = {
        'daily_special_name': daily_special_item,
        'daily_special_price': daily_special_price,
        'menu': MENU_ITEMS
    }
    return render(request, 'restaurant/order.html', context)


def confirmation(request):
    """
    View to process the submitted order form and display a confirmation page.
    Calculates total cost, shows ordered items, and provides an estimated ready time.
    """
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        special_instructions = request.POST.get("instructions")

        ordered_items = []
        total = 0
        for item, price in MENU_ITEMS.items():
            if request.POST.get(item):
                ordered_items.append(item)
                total += price

        if request.POST.get("daily_special") == "on":
            ds_name = request.POST.get("daily_special_name")
            ds_price = float(request.POST.get("daily_special_price"))
            ordered_items.append(ds_name + " (Daily Special)")
            total += ds_price

        ready_time = datetime.now() + timedelta(minutes=random.randint(30, 60))
        context = {
            'name': name,
            'phone': phone,
            'email': email,
            'instructions': special_instructions,
            'items': ordered_items,
            'total': total,
            'ready_time': ready_time.strftime("%I:%M %p")
        }
        return render(request, 'restaurant/confirmation.html', context)
