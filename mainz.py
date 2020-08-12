from urllib.request import urlopen
from bs4 import BeautifulSoup as parse
from xml.etree import ElementTree
import re
import datetime


price_regex = re.compile('(?P<price>\d+[,.]\d{2}) ?€')
remove_notes_regex = re.compile('\((\w+,?)+\w+\)')
extract_notes_regex = re.compile('((?<=,)|(?<=\())\w{1,2}')

url = 'https://www.studierendenwerk-mainz.de/speiseplan/frontend/index.php'

canteenLegend = {
  # API Extraction: https://github.com/kreativmonkey/jgu-mainz-openmensa/issues/1
  '0' : 'Alle Mensas',
  '1' : 'Zentralmensa',
  '2' : 'Mensa Georg Foster',
  '3' : 'Café Rewi',
  '4' : 'Mensa Bingen',
  '5' : 'Mensa K3',
  '6' : 'Mensa Holzstraße',
  '7' : 'Mens@rium',
  '8' : 'Café Bingen Rochusberg',
  '9' : 'Mensablitz'
}

display = {
  '0' : 'Today',
  '1' : 'Aktuelle Woche',
  '2' : 'Nächste Woche'
}

roles = ('student', 'other', 'employee')

extraLegend = {
    # Source: https://www.studierendenwerk-mainz.de/essentrinken/speiseplan/
    '1': 'mit Farbstoff',
    '2': 'mit Konservierungsstoff',
    '3': 'mit Antioxidationsmittel',
    '4': 'mit Geschmacksverstärker',
    '5': 'geschwefelt',
    '6': 'geschwärzt',
    '7': 'gewachst',
    '8': 'Phosphat',
    '9': 'mit Süßungsmitteln',
    '10': 'enthält eine Phenylalaninquelle',
    'S' : 'Schweinefleisch',
    'G' : 'Geflügelfleisch',
    'R' : 'Rindfleisch',
    'Gl' : 'Gluten',
    'We' : 'Weizen (inkl. Dinkel)',
    'Ro' : 'Roggen',
    'Ge' : 'Gerste',
    'Haf': 'Hafer',
    'Kr' : 'Krebstiere und Krebstiererzeugnisse',
    'Ei' : 'Eier und Eiererzeugnisse',
    'Fi' : 'Fisch und Fischerzeugnisse',
    'En' : 'Erdnüsse und Erdnusserzeugnisse',
    'So' : 'Soja und Sojaerzeugnisse',
    'La' : 'Milch und Milcherzeugnisse',
    'Sl' : 'Sellerie und Sellerieerzeugnisse',
    'Sf' : 'Senf und Senferzeugnisse',
    'Se' : 'Sesamsamen und Sesamsamenerzeugnisse',
    'Sw' : 'Schwefeldioxid und Sulfite > 10mg/kg',
    'Lu' : 'Lupine und Lupinerzeugnisse',
    'Wt' : 'Weichtiere und Weichtiererzeugnisse',
    'Nu' : 'Schalenfrüchte',
    'Man': 'Mandel',
    'Has': 'Haselnüsse',
    'Wa' : 'Walnüsse',
    'Ka' : 'Kaschunüsse',
    'Pe' : 'Pecanüsse',
    'Pa' : 'Paranüsse',
    'Pi' : 'Pistatien',
    'Mac':'Macadamianüsse',
	'icon:vegan.png' : 'Vegan',
	'icon:La.png' : 'Lammfleisch'
}


def parse_meals(canteen, url, display):
	content = urlopen(url + '?building_id=' + canteen + '&display_type=' + display).read().decode('utf-8', errors='ignore')
	document = parse(content, features='lxml')
	speiseplan = document.find('div', class_='speiseplan')
	
	if speiseplan == 'none':
		return 0
	
	speisen = ""
	
	# Extrahiere Speiseplandaten
	# <div class="counter count2">
	#		<div class="counter_box">
	#			<div class="speiseplancounter"> Ausgabe 2 </div>
	#				<div class="menuspeise">
	#					<div class="speiseplanname">Quinoa Bratling (Gl) mit Reis und veganem Joghurt-Kräuter-Dip (3,Gl,So,Sf,Ge)</div>
	#					<div class="vegan_icon"> <img src="/fileadmin/templates/images/speiseplan/Vegan.png" style="margin:0 10px 0 0"/> </div>
	#					<div class="food_icon"> <img src="/fileadmin/templates/images/speiseplan/La.png"/> </div>
	#					<div class="hinweis"> </div>
	#					3,40 € / 5,65 €
	#				</div>
	#			</div>
	for v in speiseplan.find_all('div'):
	  if not v.has_attr('class'):
		  continue

	  if v['class'][0] == 'speiseplan_date':
		  # Print the String of Date
		  # Format: Montag, 12. August 2020
		  speisen += "<day date='"+ str(v.string).strip() +"'> \n"
		  		  
	  if v['class'][0] == 'speiseplan_bldngall_name':
		  # Get Mensa Name
		  speisen += "\t<mensa name='" + str(v.string).strip() +"'> \n"
		  
	  if v['class'][0] == 'speiseplancounter':
		  # Print the Counter
		  # It is the category in the elements
		  # Format: Ausgabe X (X = Number)
		  # str(v.string).strip()
		  speisen += "\t<category>" + str(v.string).strip() + "</category> \n"
		  
	  if v['class'][0] == 'menuspeise':
		  # Name des Gerichts
		  name = str(v.find('div', class_="speiseplanname").string).strip()
		  		  
		  
		  # Remove the notes from Mealname and delete unnecessary spaces
		  name = ' '.join(re.sub(r'\((\w+,?)+\w+\)', '', name).split())
		  if len(name) > 250:
                    name = name[:245] + '...' 
		  		
		  notes = [span['title'] for span in meal_data.find_all('span', 'tooltip')]  	
		  notes += [img['title'] for img in meal_data.find_all('img')]
		  prices = price_regex.findall(meal_data.find('span', 'price').text)
		  # Preis aus v extrahieren
		  # 3,40 € / 5,65 €
		  
	return speisen

	# Find and convert Legend

speisen = parse_meals('0', url, '2')

print(speisen)
