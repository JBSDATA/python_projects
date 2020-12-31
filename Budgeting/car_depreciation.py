import os
import pandas as pd
import numpy as np

''' in order to do this properly we should see the original msrp for each car type
 and then compare that to its actual sale price to calculate change

Consider looking into:
- Kelly Blue Book
- True Car
- Carvana

Need to get a current snapshot listing of cars for subaru impreza

Also look at a similar car of another make/model: Toyota Corolla

Analyze based on similarities across years
'''

import requests
import json
import nltk
import re

init_query_str_1 = 'https://www.kbb.com/cars-for-sale/all'

make = 'Toyota'
model = 'Corolla'
city = 'Norfolk'
state = 'VA'
zip_code = 23501

city_state_zip = '-'.join([city, state, str(zip_code)])

query_list = [init_query_str_1, make.lower(), model.lower(), city_state_zip.lower()]
init_query_str_2 = '/'.join(query_list)

param_key_list = ['dma', 'searchRadius', 'marketExtension', 'showAccelerateBanner', 'sortBy', 'numRecords']
radius = 150
num_recs = 100
param_val_list = ['', str(radius), 'include', 'false', 'relevance', str(num_recs)]
param_val_list
param_dict = dict(zip(param_key_list, param_val_list))

param_str = '&'.join([k+'='+v for k, v in param_dict.items()])

init_query_str_2
final_query_subaru_impreza = init_query_str_2+'?'+param_str

########### read in kelley blue book

os.chdir('Kelley Bluebook Queries')
from bs4 import BeautifulSoup



mode='new_query'

########################### retrieve the HTML document

if mode=='new_query':
	r = requests.get(final_query_subaru_impreza)
	soup = BeautifulSoup(r.text)

else:
	subaru_html_file = 'Subaru Impreza for Sale in Norfolk, VA (Test Drive at Home) - Kelley Blue Book.html'
	with open(subaru_html_file, 'r', encoding='utf-8') as sub_file:
		html_doc_basic_read = sub_file.read()
		# convert document into JSON string
		html_dict_str = json.dumps(html_doc_basic_read)
		# convert JSON string into dictionary
		html_dict = json.loads(html_dict_str)

	soup = BeautifulSoup(html_doc_basic_read)

########################### Parse the HTML
every_listing = soup.findAll("div",{"class":"inventory-listing"})
len(every_listing)

try:
	assert len(every_listing) < num_recs
except:
	print('Number of results is more than was queried. Potential issue in extracting data')

# import re
# html_text_pat = re.compile('^>.*<$')

def extract_listing_data(listing):
	description = listing.find("h2", {"data-cmp":"subheading"}).text
	price = listing.find("div", {"data-cmp":"pricing"}).text
	detail_list_init = listing.find("ul", {"data-cmp":"list"}).findAll('li')
	detail_list_raw = [d.text for d in detail_list_init]
	detail_keys = [d.split(':')[0] for d in detail_list_raw]
	detail_vals = [':'.join(d.split(':')[1:]).strip() for d in detail_list_raw]
	detail_dict = dict(zip(detail_keys, detail_vals))
	init_dict = {'Description':description, 'Price':price}
	init_dict.update(detail_dict)
	return init_dict

listing_data = [extract_listing_data(listing) for listing in every_listing]
current_listings_df = pd.DataFrame(listing_data)

# extract year of make
current_listings_df['Year']= current_listings_df['Description'].str.findall('([0-9]{4})')
get_year = lambda d: int(d[0]) if type(d)==type([1]) and d!=[] else None
current_listings_df['Year'] = current_listings_df['Year'].apply(get_year)

from datetime import datetime
current_year = datetime.now().year
current_listings_df = current_listings_df[current_listings_df['Year']>current_year-6]

### sedan or hatchback
current_listings_df['Car Type'] = None
hatchback_inds = current_listings_df['Description'].str.lower().str.contains('hatchback')
sedan_inds = current_listings_df['Description'].str.lower().str.contains('sedan')
current_listings_df.loc[hatchback_inds,'Car Type']='Hatchback'
current_listings_df.loc[sedan_inds,'Car Type']='Sedan'

# Export
import json
'{} {} | {}-{}-{}.xlsx'.format(datetime.today)
file_name = '{} {} | {}-{}-{}'.format(make, model, datetime.today().year, datetime.today().month, datetime.today().day)
current_listings_df.to_excel(file_name+'.xlsx')
help(json.dump)
with open(file_name+'.html','w') as fp:
	json.dump(soup.text, fp)
