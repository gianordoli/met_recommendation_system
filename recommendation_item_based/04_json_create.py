import urllib
from bs4 import BeautifulSoup
import json
import time
import csv

#--------------------------------------------------------------------------------
# object to load csv file to list in python
def csv_to_list(csv_file, delimiter=','):
    """ 
    Reads in a CSV file and returns the contents as list,
    where every row is stored as a sublist, and each element
    in the sublist represents 1 cell in the table.
    
    """
    with open(csv_file, 'r') as csv_con:
        reader = csv.reader(csv_con, delimiter=delimiter)
        return list(reader)


#--------------------------------------------------------------------------------
# to match gallery numbers and department
gallery_no=csv_to_list("data2/data/gallery_numbers.csv")


# object to load json file
def readConfig(filename) :
    f = open(filename, 'r')
    js = json.loads(f.read())
    f.close()
    return js

obj = readConfig("github/met_recommendation/data/similar_items.json")


#--------------------------------------------------------------------------------
#to see the structure of json file we created
for x in obj[0]['item']:
    print x
    print obj[0]['item'][x]
    print type(obj[0]['item'][x])
    print obj[0]['item'][x][0]
    print type(obj[0]['item'][x][0])
    print obj[0]['item'][x][0][0]
    print obj[0]['item'][x][0][1]


#--------------------------------------------------------------------------------
# object to make a dict for one item
def default_json(item_id, item_title, gallery_number, department, img_url_big, img_url_web, similar_items) :
    dJson = {}
    dJson['item_id']= item_id
    dJson['item_title'] = item_title 
    dJson['gallery_number'] = gallery_number
    dJson['department'] = department 
    dJson['img_url_big'] = img_url_big 
    dJson['img_url_web'] = img_url_web
    dJson['similar_items'] =similar_items
    return dJson

test = default_json(123456,'tree',123,'egypt art', 'http://adfadf', 'http:aaaa' ,[{'t':123456, 's':1.23},{'t':223456, 's':2.23}])
print test


#--------------------------------------------------------------------------------
# use beautiful soup to get final json file
# for each 'item_id', 
# it can get 'item_title', 'gallery_number', 'department', 'img_url_big', and 'img_url_web' from web
# 'similar_items' was in the original json file

final_json =[]

for i in obj:
    #item_id
    item_id = i['item'].keys()[0]
    
    #similar_items
    similar_items =[]
    s_item = {}
    for a in i['item'].values()[0]:
        s_item[a[1]] = a[0]
    similar_items.append(s_item)
    
    #beautiful soup
    url = 'http://www.metmuseum.org/collection/the-collection-online/search/'+str(item_id)
    data = urllib.urlopen(url).read()
    soup = BeautifulSoup(data)
    
    #item_title
    try:
        item_title  = str(soup.find(class_ ='tombstone-container').h2.string)
    except:
        item_title = None
    
    #gallery_number
    try: 
        gallery_number = str(soup.find(class_="gallery").a.text.split(" ")[1])
    except:
        gallery_number = None
    
    #img_url_big
    try: 
        img_url_big = str(soup.find(class_="download").get('href'))
    except:
        img_url_big = None
    
    #img_url_web
    try: 
        img_url_web = str(soup.find(id="inner-image-container").img['src'])
    except:
        img_url_web = None
        
    #department
    for gallery in gallery_no[1:]:
        if gallery_number >= gallery[0] and gallery_number <= gallery[1]:
            department = gallery[2]
        if gallery_number == None:
            department = None
    
    temp = default_json(item_id, item_title, gallery_number, department, img_url_big, img_url_web, similar_items)
    final_json.append(temp)
    print len(final_json)
    
#     print item_id
#     print item_title
#     print gallery_number
#     print department
#     print img_url_big
#     print img_url_web
#     print similar_items

print len(final_json)
print "done"     

#--------------------------------------------------------------------------------
#save in json file in local computer
import io, json

with io.open('final_json.json', 'w', encoding='utf-8') as f:
  f.write(unicode(json.dumps(final_json, ensure_ascii=False)))



