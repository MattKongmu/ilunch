import requests
import smtplib
from email.mime.text import MIMEText


#function to find restaurants with specific params, such as location and cost level.
def get_restaurants(api_key, latitude, longitude, radius):
    headers = {
        'Authorization': f'Bearer {api_key}',
    }

    params = {
        'latitude': latitude,
        'longitude': longitude,
        'radius': radius,
        'categories': 'restaurants',
        'limit': 50,
        'price': '1,2'
    }
    #yelp request
    response = requests.get('https://api.yelp.com/v3/businesses/search', headers=headers, params=params)
    response.raise_for_status()
    data = response.json()

    return data['businesses']

#select a random place based off of the 50 results or less generated.
def select_random_restaurant(restaurants):
    import random
    return random.choice(restaurants)

#Send the email!
def send_email(sender_email, recipient_emails, subject, message):
    for recipient_email in recipient_emails:
        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = recipient_email
        server = smtplib.SMTP('OMITTED SERVER DNS')
        server.login(#omitted creds)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()

def main():
    # create the API URL
    api_key = 'OMMITTED KEY'
    latitude = #latitude goes here
    longitude = #Longitude goes here
    radius = 12 * 1609  # Convert miles to meters

    # Sender and recipient emails
    sender_email = 'iLunch@OmmittedDoman.com'
    recipient_emails = ["OMMITTED@Emails.com"]

    restaurants = get_restaurants(api_key, latitude, longitude, radius)
    if not restaurants:
        print('No restaurants found in the specified radius.')
        return
    #put the selected restaurant in
    selected_restaurant = select_random_restaurant(restaurants)
    result = f"Selected restaurant: {selected_restaurant['name']} ({selected_restaurant['location']['address1']})<br><a href=\"{selected_restaurant['url']}\">Yelp Review</a>"
    print(result)

    #make the email
    html_message = f"""\
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
    </head>
    <body>
        {result},
    </body>
    </html>
    """

    # Send it
    subject = 'Selected Restaurant'
    send_email(sender_email,recipient_emails, subject, html_message)

#dundermain
if __name__ == '__main__':
    main()
