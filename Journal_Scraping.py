from bs4 import BeautifulSoup
import requests
import re 
import urllib
import pandas as pd
year=2015
def extract_data(year):
    input_path="/content/drive/My Drive"
    Volyear = {2015: '152', 2016: '153', 2017: '154', 2018:'155', 2019:'156'}
    if year not in Volyear.keys():
        #print("No articles for given year")
        return "No articles for given year"
    else:
        file_path=input_path+"/Journal_Scraping_Project/plain_text/Hereditas"+str(year)+".txt"
    myfile = open(file_path, 'w',encoding="utf-8")
    print("Available")
    res = pd.DataFrame(columns=('DOI','Journal Link', 'Title', 'Authors','Author Affiliations','Corresponding Author','Publication Date','Abstract','Keywords','Full Text'))
    volume=Volyear.get(year)
    #print(volume)
    link="https://hereditasjournal.biomedcentral.com/articles?tab=keyword&volume="+volume+"&sort=PubDate"
    #print(link)
    r = requests.get(link)
    soup = BeautifulSoup(r.content, 'html.parser')
    html_page = urllib.request.urlopen(link)
    soup = BeautifulSoup(html_page)
    links = []
    for link in soup.findAll('a'):
        links.append(link.get('href'))
    kk="https://hereditasjournal.biomedcentral.com"
    mm=[]
    for ll in links:
        if 'articles/' in ll:
            mm.append(kk+ll)

    mm=set(mm)
    print(len(mm))
    for url in mm:
        response = requests.get(url)
        soup = BeautifulSoup(response.text)
        metas = soup.find_all('meta')
        abstract=[ meta.attrs['content'] for meta in metas if 'name' in meta.attrs and meta.attrs['name'] == 'citation_abstract' ]
        abstract = ''.join(abstract)
        #title = soup.find('title')
        #title=title.renderContents().decode("utf-8")
        title=[ meta.attrs['content'] for meta in metas if 'name' in meta.attrs and meta.attrs['name'] == 'dc.title' ]
        #published_date = soup.find_all("p",  {"class" : "c-bibliographic-information__value"})
        #pub_date=published_date[2].find('time').contents[0]
        pub_date=[ meta.attrs['content'] for meta in metas if 'name' in meta.attrs and meta.attrs['name'] == 'dc.date' ]
        keyword=soup.find_all("ul",  {"class" : "c-article-subject-list"})
        keywords=[]
        if (len(keyword)!=0):
           for k in keyword:
               pp=k.find_all('span',  {"itemprop" : "about"})
               for p in pp:
                   keywords.append(p.text)
        authors=[ meta.attrs['content'] for meta in metas if 'name' in meta.attrs and meta.attrs['name'] == 'dc.creator' ]
        aff=soup.find_all("ol",  {"class" : "c-article-author-affiliation__list"})
        affs=[]
        aff_loc=[]
        aff_aut=[]
        if (len(aff)!=0):
            for af in aff:
                aa=af.find_all('h4',  {"class" : "c-article-author-affiliation__address u-h3"})
                bb=af.find_all('ul',  {"class" : "c-article-author-affiliation__authors-list"})
                for a in aa:
                    aff_loc.append(a.text)
                for b in bb:
                    aff_aut.append(b.text)
            affiliation=[m+" "+n for m,n in zip(aff_loc,aff_aut)]  
        cor=soup.find_all('a',id='corresp-c1')
        corrospondance=[]
        if(len(cor)!=0):
            for c in cor:
                corrospondance.append(c.text)
        doio = soup.find_all("li",  {"class" : "c-bibliographic-information__list-item c-bibliographic-information__list-item--doi"})
        doi=[]
        if(len(doio)!=0):
            for d in doio:
                doii=d.find_all("p", {"class" : "c-bibliographic-information__value"})
                for ddd in doii:
                    doi.append(ddd.text)
        #article_text=html2text.html2text(str(soup))
        article_text = ''.join(BeautifulSoup(response.content, "html.parser").stripped_strings)
        file_name=doi[0]+".html"
        file_name=file_name[16:]
        file_name=file_name.replace('/','_')
        file_path=input_path+"/Journal_Scraping_Project/html_text_files/"
        file_name=file_path+file_name
        Html_file= open(file_name,"w",encoding='utf-8')
        Html_file.write(str(soup))
        Html_file.close()
        keywords = list(map(lambda s: s.strip(), keywords))
        #print(keywords)
        #print(type(article_text))
        #print(type(doi))
        #print(type(corrospondance))
        #print(type(affiliation))
        #print(type(authors))
        #print(type(abstract))
        #print(type(title))
        #print(type(pub_date))
        #print(type(keywords))
        #article_text=myString = ",".join(article_text)
        doi=myString = ",".join(doi)
        corrospondance= ",".join(corrospondance)
        affiliation=",".join(affiliation)
        authors=",".join(authors)
        #abstract=",".join(abstract)
        title= ",".join(title)
        pub_date=",".join(pub_date)
        keywords=",".join(keywords)
        #print(article_text)
        article_text=article_text.replace('\n', ' ') 
        article_text=article_text.replace('\t', ' ') 
        abstract=abstract.replace('\n', ' ')
        #print(doi)
        #print(corrospondance)
        #print(affiliation)
        #print(authors)
        #print(abstract)
        #print(title)
        #print(pub_date)
        #print(keywords)
        res = res.append({'DOI':doi, 'Journal Link':url, 'Title':title, 'Authors':authors,'Author Affiliations':affiliation,'Corresponding Author':corrospondance,'Publication Date':pub_date,'Abstract':abstract,'Keywords':keywords,'Full Text':article_text},ignore_index=True)
        final_list=[doi,url,title,authors,affiliation,corrospondance,pub_date,abstract,keywords,article_text]
        final_str="||%%||\n".join(final_list)
        myfile.writelines(final_str)
        myfile.write("\n-------------------------End of Article--------------------------------\n\n\n")
    myfile.close()
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 100)
    pd.set_option('display.max_colwidth', 300)
    print(res)
    res.to_csv(input_path+"/Journal_Scraping_Project/plain_text/data"+str(year)+".csv",header=True)
    print(res.shape)
    
extract_data(year)  
    
    

  
    