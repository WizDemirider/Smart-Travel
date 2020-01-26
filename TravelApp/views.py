from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils.html import escape

from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

import calendar
from .models import *
from . import extract, itinerary

def index(request):
    return redirect('login')

def signupUser(request):
    if request.method == 'POST':
        username = escape(request.POST['username'])
        raw_password = escape(request.POST['password1'])
        raw_password2 = escape(request.POST['password2'])
        try:
            if raw_password == raw_password2 and len(raw_password) >= 6:
                user = User.objects.create(username=username, password=raw_password)
                user.set_password(raw_password)
                user.save()
                login(request, user) # logs User in
                return redirect('home')
            elif len(raw_password) >= 6:
                return render(request, 'Authentication/signup.html', {'error': "Passwords do not match!"})
            else:
                return render(request, 'Authentication/signup.html', {'error': "Password must be 6 characters or more"})
        except Exception as e:
            return render(request, 'Authentication/signup.html', {'error': str(e)})
    return render(request, 'Authentication/signup.html', {'error': None})

def loginUser(request):
    if request.method == 'POST':
        username = escape(request.POST['username'])
        raw_password = escape(request.POST['password'])
        user = authenticate(username=username, password=raw_password)
        if user is not None:
            login(request, user) # logs User in
            return redirect('home')
        else:
            return render(request, 'Authentication/signup.html', {'error': "Unable to Log you in!"})
    return render(request, 'Authentication/login.html', {'error': None})

def logoutUser(request):
    logout(request)
    return redirect('index')

@login_required
def suggestCity(request):
    if request.method == 'POST':
        cities = [(review.city.name, review.score) for review in MonthlyCityReview.objects.filter(month=request.POST['Month']).order_by('-score')]
        return render(request, 'suggestCity.html', {
            'months': [{'val':str(i), 'name':calendar.month_name[i]} for i in range(1,13)],
            'cities': cities[:5],
            'selected_month': request.POST['Month'],
            'No_days': request.POST['No_days']
        })
    return render(request, 'suggestCity.html', {'months': [{'val':str(i), 'name':calendar.month_name[i]} for i in range(1,13)]})

@login_required
def places(request, city, No_days):
    hotels = extract.get_list_of_hotels(city)
    iti = itinerary.get_places(city.lower(), No_days)
    return render(request, 'places.html', {
        'city': city,
        'graph_data': [review.score for review in MonthlyCityReview.objects.filter(city_id=city).order_by('month')],
        'calendar_months': calendar.month_name,
        'hotels': hotels['list_of_hotels'][:5],
        'city_img': hotels['city_image'],
        'No_days': No_days,
        'iti': iti
        })

@login_required
def home(request):
    return redirect('suggest-city')