from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
import bs4
import re
import json
import subprocess
from collections import defaultdict
import os
import csv
import datetime


now = datetime.datetime.now()
today=now.strftime("%d.%m.%Y")
#class="pagination-wrapper" - maksymalna ilość stron dnego produktu
#'g-5/c/345-karty-graficzne.html?page=1&per_page=90' -url, 1 podstrona, 90 na strone
#def getMenu(url_restaurant):
baseurl='https://www.x-kom.pl/'
my_url='g-5/c/345-karty-graficzne.html?page=1&per_page=90'#url_restaurant
url=baseurl+my_url
uClient=urlopen(url)
page_html=uClient.read()
uClient.close()
page_soup=BeautifulSoup(page_html, "html.parser")
path_base = os.getcwd()

categoryName=page_soup.h1.text
forbiddenCharacters=['\\','/','?',':','*','<','>','"']
for character in forbiddenCharacters:
    if(character in categoryName):
        categoryName=categoryName.replace(character,"")

listProductNames=[]
listProductPrices=[]
listDates=[]
listDates.append(today)
products=page_soup.findAll("div",{"class":"product-item product-impression"})
for product in products:
    productName=product.findAll("a",{"class":"name"})[0].text.strip()
    if(len(product.findAll("span",{"class":"price text-nowrap"}))):
        productPrice=product.findAll("span",{"class":"price text-nowrap"})[0].text.strip()
    else:
        productPrice=product.findAll("span",{"class":"price text-nowrap new-price"})[0].text.strip()
    productPrice=productPrice.replace(u',',u'.')
    listProductNames.append(productName)
    listProductPrices.append(productPrice)
print(len(listProductPrices), len(listProductPrices))

def list_duplicates(seq):
    tally = defaultdict(list)
    for i,item in enumerate(seq):
        tally[item].append(i)
    return ((key,locs) for key,locs in tally.items() if len(locs)>1)
indexesToRemove=[]
for dup in sorted(list_duplicates(listProductNames)):
    print(dup)
    for i in range(len(dup[1])):
        if(dup[1][i] != dup[1][0]):
            indexesToRemove.append(dup[1][i])
indexesToRemove=sorted(indexesToRemove, reverse=True)
print(indexesToRemove)

for index in indexesToRemove:
    del listProductNames[index]
    del listProductPrices[index]
print(len(listProductPrices), len(listProductPrices))

# make csv if it is not there yes and fill with first dataset
if((os.path.isfile('./'+categoryName+'.csv'))==False):
    listHeader=['Produkt',today]
    csvrow=[]
    with open((categoryName+'.csv'), 'w', newline='') as csvfile:
        csvWriter=csv.writer(csvfile)
        csvWriter.writerow(listHeader)
        all=[]
        for index in range(len(listProductNames)):
            csvrow.append(listProductNames[index])
            csvrow.append(listProductPrices[index])
            all.append(csvrow)
            csvrow=[]
        csvWriter.writerows(all)
        csvfile.close()
else:
    with open((categoryName+'.csv'), 'r') as csvinput:
        reader = csv.reader(csvinput)
        all = []
        products=[]
        prices=[]
        row = next(reader)
        row.append(today)
        all.append(row)
        for row in reader:
            if(row[0] in listProductNames):
                row.append(listProductPrices[listProductNames.index(row[0])])
            else:
                row.append('')
            products.append(row[0])
            prices.append(row[1:])
            all.append(row)
        for product in listProductNames:
            if(product not in products):
                rowlen=len(row)
                products.append(product)
                prices.append(listProductPrices[listProductNames.index(product)])
                row=[]
                row.append(product)
                for i in range(rowlen-2):
                    row.append('')
                row.append(prices[-1])
                all.append(row)
    with open((categoryName+'.csv'),'w') as csvoutput:
        writer = csv.writer(csvoutput, lineterminator='\n')
        writer.writerows(all)
    
os.chdir(path_base)