from bs4 import BeautifulSoup as b_;
import requests as r_
def decode_url(url):
    if not url:url=input("url:")
    rs=r_.get(url);del url
    if rs.status_code==200:soup = b_(rs.text,'html.parser');co=soup.get_text(separator='\n');co=co.strip();del rs 
    start,nco=False,""
    for l in co.splitlines():
        if start:nco+=l+"\n"
        if l.strip()=="y-coordinate":start=True
    co=nco;del nco,start;ls=co.split("\n");result=[]
    for i in range(0,len(ls),3):result.append(ls[i:i+3])
    co=result;del result;x=0;y=0
    for n in co:
        if len(n)!=3:continue
        if int(n[0])>x:x=int(n[0])
        if int(n[2])>y:y=int(n[2])
    x,y=x+1,y+1;array=[[" "for _ in range(x)]for _ in range(y)];del x,y
    for l in co:
        if len(l)!=3:continue
        xt=int(l[0]);char=l[1];yt=int(l[2]);array[yt][xt]=char
    del co,xt,yt
    for row in array:
        print("".join(row))
    del array
url = 'https://docs.google.com/document/d/e/2PACX-1vSHesOf9hv2sPOntssYrEdubmMQm8lwjfwv6NPjjmIRYs_FOYXtqrYgjh85jBUebK9swPXh_a5TJ5Kl/pub'
decode_url(url)