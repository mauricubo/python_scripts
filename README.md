## Python Script Project

This repository is a personal use repository when I store my Python Scripts that I'm creating.
* daily_horoscope
* flight_offers_app

### Daily Horoscope
Send an email every morning to my personal email with the horoscope of the day

### Flight Offers App
Send and email with the best flight offers for the list of destinies that I configured.
``` yaml   
    DEFAULT_COFIG = {
        'adults': 2,
        'sort': 'price',
        'curr': 'usd',
        'limit': 15,
        'nights_in_dst_from': 7,
        'nights_in_dst_to': 15,
        'max_stopovers': 0
    }
```
This config apply to all the destinations on the list.
``` yaml
    DESTINATIONS = {
        'LIM': {
            'MVD': {
                'sort': 'price',
                'curr': 'usd',
                'limit': 15,
                'date_from': '19/01/2023',
                'date_to': '18/02/2023',
                'fly_from': 'LIM',
                'fly_to': 'MVD',
                'nights_in_dst_from': 7,
                'nights_in_dst_to': 15,
            },
            'AMS': {
                'sort': 'price',
                'curr': 'usd',
                'limit': 15,
                'date_from': '19/01/2023',
                'date_to': '18/02/2023',
                'fly_from': 'LIM',
                'fly_to': 'AMS',
                'nights_in_dst_from': 15,
                'nights_in_dst_to': 21,
            }
        },
        'MUC': {
            'MVD': {
                'sort': 'price',
                'curr': 'usd',
                'limit': 15,
                'date_from': '19/01/2023',
                'date_to': '18/02/2023',
                'fly_from': 'MUC',
                'fly_to': 'MVD',
                'nights_in_dst_from': 7,
                'nights_in_dst_to': 15,
                'max_stopovers': 2
            },
            'SYD': {
                'sort': 'price',
                'curr': 'usd',
                'limit': 15,
                'date_from': '19/01/2023',
                'date_to': '18/02/2023',
                'fly_from': 'MUC',
                'fly_to': 'SYD',
                'nights_in_dst_from': 7,
                'nights_in_dst_to': 15,
                'max_stopovers': 0
            }
        }
    }
```
This is looking for the cheapest flights from
* LIM -> MVD
* LIM -> AMS
* MUC -> MVD
* MUC -> SYD

### SendEmail
SendEmail is a shared library with the only function to send emails.