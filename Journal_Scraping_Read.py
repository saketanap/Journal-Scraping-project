input_path="/content/drive/My Drive"
year=2015
with open(input_path+'/Journal_Scraping_Project/plain_text/Hereditas'+str(year)+'.txt', 'r', encoding="utf8") as infile:
    data=infile.read()
    
articles=data.split('\n-------------------------End of Article--------------------------------\n\n\n') 
articles = articles[:-1]
for k in articles:
    art_ele=k.split('||%%||\n')
    print("Article:")
    print("DOI: ",art_ele[0])
    print("Journal Link: ",art_ele[1])
    print("Title: ",art_ele[2])
    print("Authors: ",art_ele[3])
    print("Author Affiliation: ",art_ele[4])
    print("Corrospondance Author: ",art_ele[5])
    print("Publication Date: ",art_ele[6])
    print("Abstract: ",art_ele[7])
    print("Keywords: ",art_ele[8])
    print("Article Text: ",art_ele[9])
    print("\n--------------End of Article-----------------\n\n")
    
    