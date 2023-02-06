import requests, string, pandas
from bs4 import BeautifulSoup


proxies = {
   'http': '172.177.221.87:80',
   'https': '134.122.22.233:3128',
}

pre_url = 'https://www.mayoclinic.org/diseases-conditions/index?letter='
alphabet = list(string.ascii_uppercase)
alphabet.append('0')

urls_list = []
[urls_list.append(pre_url + letter) for letter in alphabet]


def get_details(*args):
    for url in urls_list:
        response = requests.get(url, proxies=proxies)
        soup = BeautifulSoup(response.text, 'html.parser')
        index_div = soup.find('div', attrs={'id': 'index'})

        for a in index_div.find_all('a', href=True):
            if a['href'] == '#index':
                continue
            else:
                details_url = 'https://www.mayoclinic.org' + a['href']
                response = requests.get(details_url, proxies=proxies)
                soup = BeautifulSoup(response.text, 'html.parser')

                name = soup.find('h1').text
                symptoms = []
                causes = []
                risk_factors = []

                details_div = soup.find('div', attrs={'class': 'content'})
                
                if details_div:
                    ul_set = details_div.find_all('ul')

                    if ul_set[0].attrs == ({'id': 'ul_e6d09fbd-19fe-49ac-9b47-bd857c0d411b'}):
                        [symptoms.append(li.text) for li in ul_set[0]]
                        [causes.append(li.text) for li in ul_set[1]]
                        if ul_set[2]:
                            [risk_factors.append(li.text) for li in ul_set[2]]
                    else:
                        [symptoms.append(li.text) for li in ul_set[1]]
                        if ul_set[2]:
                            [causes.append(li.text) for li in ul_set[2]]
                        if ul_set[3]:
                            [risk_factors.append(li.text) for li in ul_set[3]]

                print(details_url)
                print(name)
                print(symptoms)
                print(causes)
                print(risk_factors)

get_details(urls_list)

# df = pandas.DataFrame(get_details(urls_list))
# df.to_excel('output.xlsx', index=False, header=['Diseas Name'])



