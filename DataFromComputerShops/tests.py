import datetime
import os
import csv

categoryName='Karty Graficzne'

now = datetime.datetime.now()

today=now.strftime("%d.%m.%Y")



if((os.path.isfile('./'+categoryName+'.csv'))==False):
    listHeader=['Produkt',today,'anotherdate']
    with open((categoryName+'.csv'), 'w', newline='') as csvfile:
        csvWriter=csv.writer(csvfile)
        csvWriter.writerow(listHeader)
        csvWriter.writerow(['a']+['1 zł']+['1.5 zł'])
        csvWriter.writerow(['b']+['10 zł']+['9 zł'])
        csvWriter.writerow(['c']+['3 zł']+['3 zł'])
        csvWriter.writerow(['d']+['5 zł']+['4.5 zł'])
        csvWriter.writerow(['e']+['19 zł']+['18 zł'])
        csvfile.close()
newproducts=['a','b','d','e']
newprices=['1 zł','9 zł','3 4.5 zł','18.5 zł']
with open((categoryName+'.csv'), 'r') as csvinput:
    reader = csv.reader(csvinput)
    all = []
    products=[]
    prices=[]
    row = next(reader)
    row.append('boom')
    all.append(row)
    for row in reader:
        if(row[0] in newproducts):
            row.append(newprices[newproducts.index(row[0])])
        else:
            row.append('')
        products.append(row[0])
        prices.append(row[1:])
        all.append(row)
with open((categoryName+'.csv'),'w') as csvoutput:
    writer = csv.writer(csvoutput, lineterminator='\n')
    writer.writerows(all)