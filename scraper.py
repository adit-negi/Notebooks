from bs4 import BeautifulSoup
import requests
import csv
import time
List_of_cities = ['belfast', 'liverpool', 'nottingham', 'leicester', 'cardiff',
                  'coventry', 'brighton', 'bournemouth', 'harrow', 'bradford', 'southampton', 'aberdeen']

for city in List_of_cities:
    csv_file = open('UKlistings' + city + '.csv', 'w')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Name', 'address', 'phone',
                         'website', 'description'])
    for i in range(1, 26):
        time.sleep(7)
        url = "https://www.cylex-uk.co.uk/s?q=&c=" + city + \
            "&z=&" + "p=" + str(i) + "&dst=&sUrl=&cUrl=" + city
        fetchHtml = requests.get(url).text
        soup = BeautifulSoup(fetchHtml, 'lxml')

        block = soup.find('ul', class_='lm-results list-unstyled')
        for listing in block.find_all('li'):
            company_data = listing.find(
                'div', class_='lm-result-companyData ab-test')
            try:
                company_name = company_data.find(
                    'span', class_='block bold h4').a.text
                print(company_name)

            except:
                company_name = None
            try:
                addressPhoneBlock = company_data.find(
                    'address', class_='col-md-8 col-xs-8')
                address = addressPhoneBlock.text
                phone = addressPhoneBlock.text[-13:]
                phone = phone.replace(" ", "")
                if len(phone) == 11:
                    pass
                else:
                    phone = phone[1:]
                print(address)
                print(phone)
            except:
                address = None
                phone = None
            if address == None:
                try:
                    addressPhoneBlock = company_data.find(
                        'address', class_='col-xs-12')
                    address = addressPhoneBlock.text
                    phone = addressPhoneBlock.text[-13:]
                    phone = phone.replace(" ", "")
                    if len(phone) == 11:
                        pass
                    else:
                        phone = phone[1:]
                    print(address)
                    print(phone)
                except:
                    address = None
                    phone = None

            try:
                AdditionalInfo = company_data.find(
                    'ul', class_='lm-features list-group list-inline pull-left')
                web = AdditionalInfo.findAll('li')[1]
                website = web.find('a', href=True)
                website_link = website['href']
                print(website_link)
            except:
                website_link = None

            try:
                description = company_data.find('div', class_='lm-desc').text
                print(description)
            except:
                description = None
            csv_writer.writerow(
                [company_name, address, phone, website_link, description])

    csv_file.close()
