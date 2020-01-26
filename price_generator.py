import random

from datetime import datetime

def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%d-%m-%Y")
    d2 = datetime.strptime(d2, "%d-%m-%Y")
    return abs((d2 - d1).days)

def predict_prices( check_in_date, check_out_date , rating, no_of_people=1, no_of_rooms=1):
    cost = 0
    x=no_of_people/no_of_rooms
    if no_of_people/no_of_rooms > 2:
        
        if rating>4:
            cost += random.randint(1300,2000)*x
        if rating < 5 and rating > 2:
            cost += random.randint(850,1450)*x
        if rating<3:
            cost += random.randint(400,700)*x

    if no_of_rooms > 1:
        
        if rating>4:
            cost += random.randint(2000,3000)*no_of_rooms
        if rating<5 and rating>2:
            cost += random.randint(1600,2300)*no_of_rooms
        if rating<3:
            cost += random.randint(800,1600)*no_of_rooms
        
    days = days_between(check_in_date,check_out_date)
    if days>0:
        if rating>4:
            cost += random.randint(2000,3000)*days
        if rating<5 and rating>2:
            cost += random.randint(1600,2300)*days
        if rating<3:
            cost += random.randint(800,1600)*days
        

    return round(cost,0)

print(predict_prices("1-3-2020","4-3-2020",4,3,1))