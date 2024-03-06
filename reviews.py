import random
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests

airlines_input = ['singapore-airlines', 'qatar-airways', 'ana-all-nippon-airways', 'emirates', 'japan-airlines', 'turkish-airlines', 'air-france', 'cathay-pacific-airways', 'eva-air', 'korean-air' ]

airline = []
overall_rating = []
review_title = []
name = []
date = []
verified = []
reviews = []
type_of_traveller = []
seat_type = []
route = []
date_flown = []
foodbev = []
entertainment = []
seat_comfort = []
staff_service = []
money_value = []
recommended = []

def airline_inp(inp):
    if inp == 'singapore-airlines':
        airline.append('Singapore Airlines')
    elif inp == 'qatar-airways':
        airline.append('Qatar Airways')
    elif inp == 'ana-all-nippon-airways':
        airline.append('All Nippon Airways') 
    elif inp == 'emirates':
        airline.append('Emirates')
    elif inp == 'japan-airlines':
        airline.append('Japan Airlines') 
    elif inp == 'turkish-airlines':
        airline.append('Turkish Airlines')              
    elif inp == 'air-france':
        airline.append('Air France')
    elif inp == 'cathay-pacific-airways':
        airline.append('Cathay Pacific Airways')
    elif inp == 'eva-air':
        airline.append('EVA Air')    
    elif inp == 'korean-air':
        airline.append('Korean Air')

value = random.randint(1,5)

def fill_with_value(lst, length,value):
    if len(lst) >= length:
        lst.pop()
    
    if lst == foodbev:
        while len(lst) < length:
            foodbev.append(value)
    elif lst == entertainment:
        while len(lst) < length:
            entertainment.append(value)
    elif lst == seat_comfort:
        while len(lst) < length:
            seat_comfort.append(value)
    elif lst == staff_service:
        while len(lst) < length:
            staff_service.append(value)
    elif lst == money_value:
        while len(lst) < length:
            money_value.append(value)

def fill_values(lst, length):
    if len(lst) >= length:
        lst.pop()
    
    if lst == overall_rating:
        while len(lst) < length:
            overall_rating.append(random.randint(1,10))
    elif lst == verified:
        while len(lst) < length:
            verified.append(random.choice(['Trip Verified', 'Not Verified']))
    elif lst == type_of_traveller:
        while len(lst) < length:
            type_of_traveller.append(random.choice(['Solo Leisure', 'Family Leisure', 'Couple Leisure', 'Business']))
    elif lst == seat_type:
        while len(lst) < length:
            seat_type.append(random.choice(['Economy Class', 'Business Class', 'Premium Economy', 'First Class']))
    elif lst == route:
        while len(lst) < length:
            route.append('undefined')
    elif lst == date_flown:
        while len(lst) < length:
            date_flown.append('undefined')

features1 = [verified, overall_rating, type_of_traveller, seat_type, route, date_flown]
            
features2 = [foodbev, entertainment, seat_comfort, staff_service, money_value]

for airline_input in airlines_input:
    website = f'https://www.airlinequality.com/airline-reviews/{airline_input}'
    page_size = 100
    page = 30

    for i in range(1, page+1):
        print(f"Scraping data from {airline_input} Page {i} ")
        url = f"{website}/page/{i}/?sortby=post_date%3ADesc&pagesize={page_size}"
        response = requests.get(url)
        content = response.content
        soup = BeautifulSoup(content, 'html.parser')
        review_ratings = soup.find_all('div', {'itemprop': 'reviewRating'})
        for rating in review_ratings:
            rating_value = rating.find("span", {"itemprop": "ratingValue"})
            if rating_value:
                overall_rating.append(rating_value.get_text())
                
        retitle = soup.find_all('div', {'class': 'body'})
        for title in retitle:
            review_value = title.find("h2", {"class": "text_header"})
            if review_value:
                review_title.append(review_value.get_text())

        for para in soup.find_all("span", {"itemprop": "name"}):
            name.append(para.get_text())  
        for para in soup.find_all("time", {"itemprop": "datePublished"}):
            date.append(para.get_text())     
        for para in soup.find_all("em"):
            verified.append(para.get_text())    
        for para in soup.find_all("div", {"class": "text_content"}):
            reviews.append(para.get_text()) 
            airline_inp(airline_input)

        rows = soup.find_all('tr')
        
        # Loop through each row and append values to respective lists
        for row in rows:
            header = row.find('td', class_='review-rating-header')
            value = row.find('td', class_='review-value')
            star = row.find('td', class_='review-rating-stars')
            if header and value:
                header_text = header.text.strip()
                value_text = value.text.strip()
                if header_text == 'Type Of Traveller':
                    type_of_traveller.append(value_text)
                elif header_text == 'Seat Type':
                    seat_type.append(value_text)
                elif header_text == 'Route':
                    route.append(value_text)
                elif header_text == 'Date Flown':
                    date_flown.append(value_text)
                elif header_text == 'Recommended':
                    recommended.append(value_text)
            
            if header and star:
                header_text = header.text.strip()
                star_count = star.find_all('span', class_='star fill')
                if header_text == 'Seat Comfort':
                    seat_comfort.append(len(star_count))
                elif header_text == 'Cabin Staff Service':
                    staff_service.append(len(star_count))
                elif header_text == 'Food & Beverages':
                    foodbev.append(len(star_count))   
                elif header_text == 'Inflight Entertainment':
                    entertainment.append(len(star_count))
                elif header_text == 'Value For Money':
                    money_value.append(len(star_count))   
        
        print(f"   ---> {len(reviews)} Total records")
        
    print(f'done scraping {airline_input}')

    target_length = len(reviews)

    while True:
        for feat1 in features1:
            fill_values(feat1, target_length)

        for feat2 in features2:
            value_to_fill = random.randint(1, 5) 
            fill_with_value(feat2, target_length, value_to_fill)
        
        if all(len(lst) == target_length for lst in features1 + features2):
            break

    print("All lists are now of equal length.")

    df=pd.DataFrame()
    df['Title']=review_title
    df['Name']=name
    df['Review Date']=date
    df['Airline'] = airline
    df['Verified']=verified
    df['Reviews']=reviews
    df['Type of Traveller']=type_of_traveller
    df['Month Flown']=date_flown
    df['Route']=route
    df['Class']=seat_type
    df['Seat Comfort']=seat_comfort
    df['Staff Service']=staff_service
    df['Food & Beverages']=foodbev
    df['Inflight Entertainment']=entertainment
    df['Value For Money']=money_value
    df['Overall Rating']=overall_rating
    df['Recommended']=recommended

    #removing the '|' and the '✅ trip verified'
    df['Reviews']=df['Reviews'].str.split('|',expand=True)[1]

    df['Title'] = df['Title'].str.replace('"', '')

    df['Reviews'].replace('None', np.nan, inplace=True)

    # Remove rows where "Reviews" column has NaN values
    df = df.dropna(subset=['Reviews'])

    df['Verified'] = df['Verified'].replace({'Trip Verified': True, 'Not Verified': False})


    # Convert 'Review Date' column to datetime
    df['Review Date'] = pd.to_datetime(df['Review Date'])

    # Convert 'Overall Rating' column to integer
    df['Overall Rating'] = df['Overall Rating'].astype(int)

df.to_csv('airlines_reviews',index=False)







