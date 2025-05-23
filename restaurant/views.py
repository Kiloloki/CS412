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
DAILY_SPECIALS = ['Lobster Roll', 'Tuna Poke', 'BBQ Ribs']

def main(request):
    return render(request, 'restaurant/main.html')

def order(request):
    daily_special = random.choice(DAILY_SPECIALS)
    context = {
        'daily_special': daily_special,
        'menu': MENU_ITEMS
    }
    return render(request, 'restaurant/order.html', context)

def confirmation(request):
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
