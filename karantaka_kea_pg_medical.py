from mechanize import Browser
from bs4 import BeautifulSoup
import urllib2
import numpy as np
import csv

csv_file = "resources/medical_final.csv"

with open(csv_file,"r") as f:
    reader = csv.reader(f)
    reader = list(reader)

rno = np.asarray(reader)
print rno[2:,1]

for r in rno[2:,1]:

    br = Browser()
    br.set_handle_robots( False )
    br.addheaders = [('User-agent', 'Firefox')]
    # br.open("http://keapu-webugpp01-in.cloudapp.net:81/pgetresults/main/results.php")
    br.open("http://keapu-webugpp01-in.cloudapp.net:81/pgetresults-r2/main/results.php")
    br.select_form("form1")
    #now enter the dates according to your choice
    # print r
    br.form["txtrollno"] = r
    response = br.submit()

    soup = BeautifulSoup(response,'html.parser')
    html = soup.find_all('td')

    if len(html)>36:
        print r,html[21].span.text,html[27].span.text,html[33].text,html[36].text
        print "                Claimed Category :", html[24].text.strip(' \t\n\r')
        print "                Category Alotted :", html[39].text.strip(' \t\n\r'), "\n"
    else:
        print r,"Not alotted any seat\n"