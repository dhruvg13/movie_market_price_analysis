import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

opt=Options()
opt.add_experimental_option('detach',True)
opt.add_argument('--incognito')
path="/Users/abhijeetkashyap/Desktop/chromedriver"
service=Service(executable_path=path)
# opening chrome
driver=webdriver.Chrome(service=service,options=opt)
# Acessing link
driver.get("https://www.boxofficemojo.com/showdown/?ref_=bo_nb_cso_tab")
time.sleep(2)
height=driver.execute_script("return document.body.scrollHeight")

# Managing whole content
while True:
    driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
    time.sleep(2)

    new_height = driver.execute_script('return document.body.scrollHeight')
    if new_height==height:
        break
    height=new_height
page=driver.page_source
# saving html file
with open('imdb.html','w') as f:
    f.write(page)
# opening html file
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests

with open('imdb.html', 'r') as f:
    html = f.read()

Showdown = []
link = []
soup = BeautifulSoup(html, 'lxml')

# showdown
show_down = soup.find_all('a', {'class': 'a-link-normal'})
for sh in show_down:
    if sh['href'].startswith('/showdown/'):
        Showdown.append(sh.text.replace('\n', '').strip())
        link.append(sh['href'])

Showdown = Showdown[1:]
link = link[1:]

Url_link = []
for i in link:
    base_url = "https://www.boxofficemojo.com"
    link = urljoin(base_url, i)
    Url_link.append(link)


nested_dict = {}
key = 0
for full_url in Url_link:
    p = requests.get(full_url)
    time.sleep(1)
    soup1 = BeautifulSoup(p.text, 'lxml')
    # name
    movie_name = []
    m_name = soup1.find_all('h2', {'class': "a-size-base"})
    nested_dict[key] = {}
    for i in m_name:
        movie_name.append(i.text.strip())
    nested_dict[key]['movie_name'] = movie_name
    # Genre
    genre = []
    td_tags = soup1.find_all(name='td', class_=False)
    text_content = [td.get_text(strip=True).replace("\n", '') for td in td_tags if
                    len(td.contents) == 1 and not td.contents[0].name]
    for i in text_content:
        st = str(i).replace(" ", '')
        genre.append(st)
    nested_dict[key]['Genre'] = genre
    # production_budget
    p_b = []
    tr_class = None
    td_class = soup1.find_all('td', {'class': 'a-text-left'})
    for td in td_class:
        if td.text == 'Production Budget':
            tr_class = td.find_parent('tr')
            break
    prod_budget = tr_class.find_all('span', {'class': 'money'})
    for budget in prod_budget:
        p_b.append(budget.text)
    nested_dict[key]['Production_budget'] = p_b
    # Rating
    r = []
    tr_class1 = None
    for td in td_class:
        if td.text == 'MPAA Rating':
            tr_class1 = td.find_parent('tr')
            break
    rating = tr_class1.find_all('td', {'class': 'a-align-center'})
    for rate in rating:
        r.append(rate.text)
    nested_dict[key]['Rating'] = r
    # running_time
    r_t = []
    tr_class2 = None
    for td in td_class:
        if td.text == 'Running Time':
            tr_class2 = td.find_parent('tr')
            break
    running_time = tr_class2.find_all('td', {'class': 'a-align-center'})
    for rt in running_time:
        r_t.append(rt.text)
    nested_dict[key]['Running_time'] = r_t
    # foreign_gross value
    f_gv = []
    tr_class3 = None
    for td in td_class:
        if td.text == 'Foreign Gross':
            tr_class3 = td.find_parent('tr')
            break
    froign_gross = tr_class3.find_all('span', {'class': 'money'})
    for fg in froign_gross:
        f_gv.append(fg.text)
    nested_dict[key]['Foreign_gross'] = f_gv
    # Domestic_gross
    d_g = []
    tr_class4 = None
    for td in td_class:
        if td.text == ' Domestic Gross':
            tr_class3 = td.find_parent('tr')
            break
    domestic_gross = tr_class3.find_all('span', {'class': 'money'})
    for dg in domestic_gross:
        d_g.append(dg.text)
    nested_dict[key]['Domestic_gross'] = d_g
    # release_date
    r_d = []
    tr_class5 = None
    for td in td_class:
        if td.text == 'Release Date':
            tr_class5 = td.find_parent('tr')
            break
    relase_date = tr_class5.find_all('a', {'class': 'a-link-normal'})
    for rd in relase_date:
        r_d.append(rd.text)
    nested_dict[key]['Relase_date'] = r_d
    # closing_date
    c_d = []
    tr_class6 = None
    for td in td_class:
        if td.text == 'Close Date':
            tr_class6 = td.find_parent('tr')
            break
    close_date = tr_class6.find_all('a', {'class': 'a-link-normal'})
    for cd in close_date:
        c_d.append(cd.text)
    nested_dict[key]['Closing_date'] = c_d
    # Distributors
    dist = []
    tr_class7 = None
    td_class7 = soup1.find_all('td', {'class': 'a-text-left a-align-center'})
    for td in td_class7:
        if td.text == 'Distributor':
            tr_class7 = td.find_parent('tr')
            break
    Distributor = tr_class7.find_all('a', {'class': 'a-link-normal'})
    for d in Distributor:
        dist.append(d.text)

    key = key + 1