import boto3
import csv
from bs4 import BeautifulSoup
bucketInicial= "parcial2headlines"
bucketFinal= "parcial3headlines"

def main():
    
    localtime=time.localtime()
    for nombre in ['El_tiempo','Publimetro']:
        if nombre == 'El_tiempo':
            revista='raw/newspaper=El_tiempo/year='+str(localtime.tm_year)+'/month='+str(localtime.tm_mon)+'/day='+str(localtime.tm_mday)+'/page.html'
        else:
            revista='raw/newspaper=Publimetro/year='+str(localtime.tm_year)+'/month='+str(localtime.tm_mon)+'/day='+str(localtime.tm_mday)+'/page.html'
        archivo=nombre
        s3 = boto3.resource('s3')
        s3.meta.client.download_file(bucketInicial, page.html, revista)
        f = open('/tmp/'+revista,'r',encoding='utf-8')
        txt=f.read()
        soup = BeautifulSoup(txt,'html.parser')
        if nombre == 'El_tiempo':
            scrapping(archivo,"El_tiempo",soup,s3)
        else:
            scrapping(archivo,"Publimetro",soup,s3)

def scrapping(archivo,revista,soup,s3):
    csvFile = open('/tmp/'+archivo+'.csv', 'w',encoding='utf-8')
    writer = csv.writer(csvFile,dialect='unix')
    row=['title','section','url']
    writer.writerow(row)

    if(revista=="El_tiempo"):
        articles=soup.find_all('article')
        for article in articles:
            categories=article.find("a",{'class':'category'})
            titles= article.find("a",{'class':'title'})
            if(categories and titles):
                category=categories.getText()
                title=titles.getText()
                url='https://www.eltiempo.com'+titles.get('href')
                row=[title,category,url]
                writer.writerow(row)
    elif(revista=='Publimetro'):
        mainDiv=soup.find(id='main')
        divNews=mainDiv.find_all('div',{'class':'container layout-section'})
        usefulDivNews=divNews[1]
        for row in usefulDivNews:
            headers=row.find_all('h4')
            if(len(headers)!=0):  
                for header in headers:
                    section = header.text
                    nextElement=header.nextSibling
                    if nextElement:
                        if(header.parent.name=='main'):
                            items = nextElement.find_all('div',{'class':'list-item'})
                            for news in items:
                                anchor=news.find_all('a')[0]
                                url = "https://www.publimetro.co"+anchor.get('href')
                                title= anchor.get('title')
                                if("," in title):
                                    title=title.replace(",","")
                                row=[title,section,url]
                                writer.writerow(row)
                        else:
                            articles=nextElement.find_all('article')
                            if articles:
                                for article in articles:
                                    headlines = article.find_all('h2')
                                    for line in headlines:
                                        anchor=line.find('a')
                                        if(anchor):
                                            ref = anchor.get('href')
                                            url=""
                                            if (not ref.startswith('https://')):
                                                url = "https://www.publimetro.co"+anchor.get('href')
                                            else:
                                                url = anchor.get('href')
                                            title = anchor.getText()
                                            if("," in title):
                                                title=title.replace(",","")
                                            row=[title,section,url]
                                            writer.writerow(row)
    csvFile.close()
    s3.meta.client.upload_file('/tmp/'+archivo+'.csv', bucketFinal,'final/newspaper='+archivo+'/year='+str(localtime.tm_year)+'/month='+str(localtime.tm_mon)+'/day='+str(localtime.tm_mday)+'/'+archivo+'.csv')
    
        
if __name__ == "__main__":
	main()