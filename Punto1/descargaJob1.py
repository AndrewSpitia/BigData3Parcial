import requests
import boto3
import time


def main():
	
	bucket="parcial2headlines"
	
	localtime=time.localtime()
	s3 = boto3.resource('s3')
	revistas("El_tiempo","https://www.eltiempo.com/",localtime,bucket,s3)
	revistas("Publimetro","https://www.publimetro.co/",localtime,bucket,s3)
	
def revistas(nombre, url,localtime,bucket,s3):	
	r = requests.get(url)
	filepath="/tmp/"+nombre+".html"
	f = open(filepath,"w")
	f.write(r.text)
	f.close()
	data={
		'file':filepath,
		'bucket':bucket,
		'path':'raw/newspaper='+nombre+'/year='+str(localtime.tm_year)+'/month='+str(localtime.tm_mon)+'/day='+str(localtime.tm_mday)+'/page.html'
	}
	s3.meta.client.upload_file(data['file'],data['bucket'], data['path'])
	
if __name__ == "__main__":
	main()