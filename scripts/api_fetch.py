# librairies import
import requests # to do HTTP requests to the API
import csv # to write easily a CSV file 

url = "https://www.fff.fr/api/find-club"

# payload is the dictionnary that contains the corpse of the POST request send to the API
payload = {
    "find_club[age]": "senior F", # this is the key respecting the syntax that we saw in the "inspect" section 
    "find_club[licenceType1][]": "FC",
    "find_club[licenceType2][]": "F11",
    "find_club[position]": "Lille 59000",
    "find_club[latitude]": "50.6311",
    "find_club[longitude]": "3.0468",
    "find_club[radius]": "5"
}

response = requests.post(url, data=payload) # send the HTTP request to the API with the payload
clubs = response.json() # the API send back the data in a JSON form

def is_feminine(profil_list): # verify if the list of profils contains a indication about women football
    for profil in profil_list:
        if 'senior_f' in profil.lower() or 'foot_competition_senior_f' in profil.lower():
            return True
    return False

filtered_clubs = [club for club in clubs if is_feminine(club.get('profil_club_pratiques', []))] # keep only clubs if they're correct about the previous criteria

# writing inside a CSV file
with open('clubs_feminins.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # En-têtes
    writer.writerow(['Nom', 'Adresse', 'Code Postal', 'Ville', 'Latitude', 'Longitude', 'Logo'])

    for club in filtered_clubs:
        adresse = ", ".join(filter(None, [club.get('cl_adr1'), club.get('cl_adr2'), club.get('cl_adr3'), club.get('cl_bdis')]))
        lat = club.get('cl_geo_location', {}).get('lat')
        lon = club.get('cl_geo_location', {}).get('lon')

        writer.writerow([
            club.get('cl_nom', ''),
            adresse,
            club.get('cl_cp', ''),
            club.get('cl_loca', ''),
            lat,
            lon,
            club.get('logo', '')
        ])

print(f"{len(filtered_clubs)} clubs féminins enregistrés dans 'clubs_feminins.csv'")
