import requests
import bs4
def all_matches_name():
    try:    
        res = requests.get("https://buffersports.com/homer16.php")
        soup = bs4.BeautifulSoup(res.text,'lxml').find_all('ul',attrs={"class":"country-sales list-group list-group-flush container"})[0]

        all_match_name=[]
        all_match_link=[]

        for list_group_item in soup.find_all('li',attrs={"class":"country-sales-content list-group-item"}):
            link_counter = 0
            for match_name in list_group_item.find_all('span',attrs={"class":"ml-3 mt-4 col text-center"}):
                match = match_name.find_all('a')[0].find_all('h6')[0]
                accepted_str=""
                for char in match.text:
                    if((ord(char)>=65 and ord(char)<=90) or (ord(char)>=92 and ord(char)<=122)):
                        accepted_str = accepted_str+char
                all_match_name.append("/"+(accepted_str).replace(" ",""))
            for match_link in list_group_item.find_all('span',attrs={"class":"text-dark col text-center"}):
                link = match_link.find_all("a")
                all_match_link.append(link[0]['href'])
                link_counter+=1
        all_matches = dict(zip(all_match_name,all_match_link))
        return all_matches
    except:
        return None

def selected_match(all_matches,user_match_name):
    try:
        users_match = requests.get(all_matches[user_match_name])
        streaming_website = bs4.BeautifulSoup(users_match.text,'lxml').find_all('iframe')[0]['src']


        streaming_document = requests.get(streaming_website)
        streaming_link_list = bs4.BeautifulSoup(streaming_document.text,'lxml').find('table')
        all_individual_match_link=[]

        for links in streaming_link_list.find_all('tr'):
            links_data = links.find_all('td')
            for link in links_data:
                x = link.find('a')
                if(x!=None):
                    all_individual_match_link.append(x['href'])

        return all_individual_match_link
    except:
        return None
