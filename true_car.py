from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import numpy as np
from datetime import datetime
import pandas as pd
import seaborn as sns
import matplotlib.pylab as plt

def create_naked_df():
	df = pd.DataFrame(columns=['date','trim','truecar','inventory'])
	df.to_csv('prices&inventory.csv',index=False)


try: df = pd.read_csv('prices_inventory.csv')
except: create_naked_df()

sport = 'https://www.truecar.com/prices-new/honda/ridgeline-summary/2021/?postalCode=19118&section=review&styleId=72032'
rtl = 'https://www.truecar.com/prices-new/honda/ridgeline-summary/2021/?postalCode=19118&section=review&styleId=72033'
rtl_e = 'https://www.truecar.com/prices-new/honda/ridgeline-summary/2021/?postalCode=19118&section=review&styleId=72035'
black = 'https://www.truecar.com/prices-new/honda/ridgeline-summary/2021/?postalCode=19118&section=review&styleId=72037'
sport20 = 'https://www.truecar.com/prices-new/honda/ridgeline-summary/2020/?postalCode=19118&section=review&styleId=67796'

prices = []
for name,url in zip(['sport','rtl','rtl_e','black','2020'],[sport,rtl,rtl_e,black,sport20]):
	browser = webdriver.Safari()
	browser.get(url)
	time.sleep(2)
	main = browser.find_element_by_id("main")
	time.sleep(2)
	price = main.find_element_by_class_name("col-md-6").text.split('$')
	if len(price) == 3:
		try:price = np.mean([int(price[1].split(' ')[0].replace(',', '')),int(price[2].split(' ')[0].replace(',', ''))])
		except:price = price[1].split(' ')[0].replace(',', '')
	elif len(price) ==2:
		price = price[1].split(' ')[0].replace(',', '')
	print (price)
	prices.append(price)
	browser.close()

black = "https://www.autotrader.com/cars-for-sale/new-cars/truck/honda/ridgeline/philadelphia-pa-19118?incremental=ALL&dma=&driveGroup=AWD4WD&searchRadius=100&location=&startYear=2021&trimCodeList=RIDGELINE%7CBlack%20Edition&isNewSearch=true&marketExtension=include&showAccelerateBanner=false&sortBy=relevance&numRecords=25"
rtl = 'https://www.autotrader.com/cars-for-sale/new-cars/truck/honda/ridgeline/philadelphia-pa-19118?incremental=ALL&dma=&driveGroup=AWD4WD&searchRadius=100&location=&startYear=2021&trimCodeList=RIDGELINE%7CRTL&isNewSearch=true&marketExtension=include&showAccelerateBanner=false&sortBy=relevance&numRecords=25'
rtl_e = 'https://www.autotrader.com/cars-for-sale/new-cars/truck/honda/ridgeline/philadelphia-pa-19118?incremental=ALL&dma=&driveGroup=AWD4WD&searchRadius=100&location=&startYear=2021&marketExtension=include&trimCodeList=RIDGELINE%7CRTL-E&isNewSearch=true&showAccelerateBanner=false&sortBy=relevance&numRecords=25'
sport = 'https://www.autotrader.com/cars-for-sale/new-cars/truck/honda/ridgeline/philadelphia-pa-19118?incremental=ALL&dma=&driveGroup=AWD4WD&searchRadius=100&location=&startYear=2021&marketExtension=include&trimCodeList=RIDGELINE%7CSport&isNewSearch=true&showAccelerateBanner=false&sortBy=relevance&numRecords=25'
all_2020 = 'https://www.autotrader.com/cars-for-sale/new-cars/truck/2020/honda/ridgeline/philadelphia-pa-19118?incremental=ALL&dma=&driveGroup=AWD4WD&searchRadius=100&location=&marketExtension=include&isNewSearch=true&showAccelerateBanner=false&sortBy=relevance&numRecords=25'
inventories = []
for name,url in zip(['sport','rtl','rtl_e','black','2020'],[sport,rtl,rtl_e,black,all_2020]):
	browser = webdriver.Safari()
	browser.get(url)
	inventory = browser.find_element_by_xpath('//*[@id="mountNode"]/div[1]/div[3]/div/div[2]/div[2]/div[1]/div[1]/div[1]').text.split(' ')[-2]
	print (inventory)
	inventories.append(inventory)
	browser.close()

trims = ['sport','rtl','rtl_e','black','2020']
date = [datetime.now(),datetime.now(),datetime.now(),datetime.now(),datetime.now()]

this_df = pd.DataFrame(columns=['date','trim','truecar','inventory'])
this_df['date'] = date
this_df['truecar'] = prices
this_df['inventory'] = inventories
this_df['trim'] = trims

df = df.append(this_df,ignore_index=True)
df.to_csv('prices_inventory.csv',index=False)

plt.close()
sns.set_style('whitegrid')
fig,axes = plt.subplots(1,2,figsize=(8,5))
df = pd.read_csv('prices_inventory.csv')
df.date = pd.DatetimeIndex(df.date)
df = df.set_index('date')
plt.sca(axes[0])
ax1 = sns.lineplot(x="date", y="truecar",hue="trim",data=df)
plt.xticks(rotation=90)

ax2 = ax1.twinx()
plt.sca(axes[1])
sns.lineplot(x="date", y="inventory",hue="trim",data=df)
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig('ridgeline.png')
plt.close()
