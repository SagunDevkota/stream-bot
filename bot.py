import requests
import bs4
from config import BASE_URL
def all_matches_name():
    try: 
        res = requests.get(BASE_URL)
        soup = bs4.BeautifulSoup(res.text,'html.parser').find_all('div',{'class':'col-md-12 border rounded'})
        all_match_link = []
        all_match_name = []
        for league in soup:
            links = league.findChildren("a" , recursive=False)
            for link in links:
                temp = link.find_all("img")[0]['alt']+"VS"+link.find_all("img")[1]['alt']
                matchName = ""
                for chars in temp.upper():
                    if(ord(chars)>=65 and ord(chars)<=90):
                        matchName+=chars
                    if(ord(chars) == ord(' ')):
                        matchName+='_'
                all_match_name.append((f'/{matchName}'))
                all_match_link.append(link['href'])
        all_matches = dict(zip(all_match_name,all_match_link))
        return all_matches
    except Exception as e: return e

def selected_match(all_matches,user_match_name):
    try:
        all_links = 0
        users_match = requests.get(all_matches[user_match_name])

        all_contents = bs4.BeautifulSoup(users_match.text,'html.parser').find_all("div",attrs={"class":"data-row"})
        print(all_contents[0]['onclick'].split("'")[1])
        all_individual_match_link = []
        for content in all_contents:
            link_content = content['onclick'].split("'")[1]
            if(len(link_content) == 0):
                continue
            all_links = all_links+1
            all_individual_match_link.append(link_content)
            if(all_links>=15):
                break
        return all_individual_match_link
    except:
        return None