import requests as r
import csv
import datetime as dt
from PIL import Image
from IPython.display import display

url = 'https://api.covid19api.com/dayone/country/brazil'
resp = r.get(url)
rawData = resp.json()
finalData = []
for data in rawData:
    finalData.append([data['Confirmed'], data['Deaths'], data['Recovered'], data['Active'], data['Date']])
finalData.insert(0,['Confirmados', 'Obitos', 'Recuperados', 'Ativos', 'Data'])


# Remoção do relógio, mantendo apenas a data
CONFIRMADOS = 0
OBITOS = 1
RECUPERADOS = 2
ATIVOS = 3
DATA = 4

for i in range(len(finalData)):
    finalData[i][DATA] = finalData[i][DATA][:10]

finalData[i][DATA] = dt.datetime.strptime(finalData[i][DATA], '%Y-%m-%d')

with open('brasil-covid.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(finalData)

def getDatasets(y, labels):
    if type(y[0]) == list:
        datasets = []
        for i in range(len(y)):
            datasets.append({
                'label': labels[i],
                'data': y[i]
            })
        return datasets
    else:
        return [
            {
                'label': labels[0],
                'data': y
            }
        ]
 
def setTitle(title = ''):
    if title != '':
        display = 'true'
    else:
        display = 'false'
    return {
        'title':title,
        'display': display
    }

def createChart(x,y,labels, kind='bar', title=''):
    datasets = getDatasets(y,labels)
    options = setTitle(title)
    chart = {
        'type': kind,
        'data': {
            'labels':x,
            'datasets': datasets
        },
        'options': options
    }
    return chart

def getApiChart(chart):
    urlBase = 'https://quickchart.io/chart'
    resp = r.get(f'{urlBase}?c={str(chart)}')
    return resp.content

def saveImage(path, content):
    with open(path,'wb') as image:
        image.write(content)

def displayImage(path):
    img_pil = Image.open(path)
    display(img_pil)

yData1 = []
for obs in finalData[1::15]: #a cada 15 dias
    yData1.append(obs[OBITOS])
    
labels = ['Confirmados', "Obitos"]
x = []
for obs in finalData[1::15]:
    data = dt.datetime.strptime(obs[DATA], '%Y-%m-%d')
    x.append(data.strftime("%d/%m/%Y"))

chart = createChart(x, yData1, labels, title= 'Gráfico confirmados vs obitos')
chartContent = getApiChart(chart)
saveImage('meu-primeiro-grafico.png', chartContent)
displayImage('meu-primeiro-grafico.png')