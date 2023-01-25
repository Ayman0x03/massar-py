import requests
from lxml import etree
import pandas as pd 
sep = "(-------------------------------------------------------------)"
ses = requests.session()
CONheaders ={ "Host":'massarservice.men.gov.ma', 
                    "Content-Length":'156', 
                    "Cache-Control": 'max-age=0',
                    "Sec-Ch-Ua": '\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"96\"',
                    "Sec-Ch-Ua-Mobile":'?0',
                    "Sec-Ch-Ua-Platform": '\"Linux\"',
                    "Upgrade-Insecure-Requests": '1',
                    "Origin":'https://massarservice.men.gov.ma',
                    "Content-Type": 'application/x-www-form-urlencoded',
                    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36', 
                    "Accept": 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 
                    "Sec-Fetch-Site": 'same-origin',
                    "Sec-Fetch-Mode": 'navigate', 
                    "Sec-Fetch-User": '?', 
                    "Sec-Fetch-Dest": 'document', 
                    "Referer": 'https://massarservice.men.gov.ma/moutamadris/Account', 
                    "Accept-Encoding": 'gzip, deflate', 
                    "Accept-Language": 'en-US,en;q=0.9', 
                    "Connection": 'close' }

tokenRequest = ses.get('https://massarservice.men.gov.ma/moutamadris/Account')

domain ='https://massarservice.men.gov.ma/moutamadris/Account'
parser = etree.HTMLParser()
csrf = etree.fromstring(tokenRequest.text , parser)
csrftoken = csrf.xpath('//form/input[@name="__RequestVerificationToken"]/@value')[0]
#uid ,Pass = "user@taalim.ma", "password" # for full autonomy fill this line
#       $Ask for creds$
uid=input("Username:")                   #And comment this line
Pass=input("Password:")                  #And this one
#       $Better : read creds from file
#             f=open("Creds.txt","r")
#             lines=f.readlines()
#             uid=lines[0]
#             Pass=lines[1]
#             f.close() 
Creds = {'UserName' : uid ,
         'Password' : Pass,
        '__RequestVerificationToken': csrftoken } 
r1 = ses.post(   
              b'https://massarservice.men.gov.ma/moutamadris/Account' ,  
              headers=CONheaders , 
              data= Creds ,)



print(r1.cookies)
print(sep)
if 'ChangePassword' in r1.text: print('Connected')
else: print('Error , maybe Username or password are invalid'),  exit()
#       $Select instead of plain text$
sess = input("Semestre (01 or 02):")
year = input("Year (for the 2022/2023 write 2022):")
Creds2 = {"Annee":year ,
           "IdSession": sess}
#Creds2 = {"Annee":"2021" , #TBR
#          "IdSession": "02"}
CONheaders2 = {
        "Sec-Ch-Ua":'" Not A;Brand";v="99", "Chromium";v="96"' ,
        "Accept":'*/*',
        "Content-Type": 'application/x-www-form-urlencoded; charset=UTF-8',
        "X-Requested-With": 'XMLHttpRequest' ,
        "Sec-Ch-Ua-Mobile": '?0',
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36',
        "Sec-Ch-Ua-Platform":'"Linux"',
        "Origin":'https://massarservice.men.gov.ma',
        "Sec-Fetch-Site": 'same-origin',
        "Sec-Fetch-Mode": 'cors',
        "Sec-Fetch-Dest": 'empty',
        "Referer": 'https://massarservice.men.gov.ma/moutamadris/TuteurEleves/GetNotesEleve',
        "Accept-Encoding": 'gzip, deflate',
        "Accept-Language": 'en-US,en;q=0.9',
        "Connection": 'close'
}
fr = ses.post( b'https://massarservice.men.gov.ma/moutamadris/General/SetCulture?culture=en',
              headers=CONheaders2)

r2 = ses.post(
        b'https://massarservice.men.gov.ma/moutamadris/TuteurEleves/GetBulletins',
        headers=CONheaders2 ,
        data=Creds2 ,
        cookies=ses.cookies
                ) 


print(sep)
print(sep)
print(sep)
print(sep)
print(sep)
print(sep)
if 'Classe' in r2.text: print('yaaaaaaaaaaaaay')
else: print('Error')
# From here it would start to get really weird but it's fine
# This was still one of the hardest roadblocks in this project
#    "TBD"   $Print which school and class$


notes = pd.read_html(r2.text, decimal=',', thousands='.')
tb0 = notes[0]
tb1 = notes[1]
print('Grades')
print(tb0)
print(sep)
print('Global Grades')
print(tb1)
print(sep)

#DEBUG  print(r2.text ,file=open('regtest.' , 'a'))

f = etree.fromstring(r2.text , parser)
print(''.join(f.xpath('//*[@id="tab_notes_exam"]/div[2]//text()')))

