import requests
import lxml.html as html
import os
import datetime


HOME_URL = 'https://larepublica.pe'

today_y_m_d = datetime.date.today().strftime('%Y-%m-%d')
today_ymd = datetime.date.today().strftime('%Y/%m/%d')

XPATH_LINK_TO_ARTICLE = str(f'//a[contains(@href,"{today_ymd}")]/@href')
XPATH_TITLE = '//h1[@class="DefaultTitle"]/text()'
XPATH_SUMMARY = '//h2[@class="DefaultSubtitle"]/text()'
XPATH_BODY = '//div[@class="page-internal-content"]//p//text()'

def parse_notice(link, today):
    print('*'*20)
    try:
        if link.startswith('/'):
            link = HOME_URL+ link
        print('link: ', link)

        response = requests.get(link)
        
        if response.status_code != 200:
            raise ValueError(f'Error: {response.status_code}')
            
        notice = response.content.decode('utf-8')
        parsed = html.fromstring(notice)

        try:
            title = parsed.xpath(XPATH_TITLE)[0]
            title = title.replace('\"', '')
            title = title.replace('#', '')
            title = title.replace('|', '')
            title = title.replace(':', ', ')
            summary = parsed.xpath(XPATH_SUMMARY)[0]
            body = parsed.xpath(XPATH_BODY)
        except IndexError:
            return
        print('title: ', title)
        with open(f'{today}/{title}.txt', 'w', encoding='utf-8') as f:
            f.write(title)
            f.write('\n')
            f.write('_'*25)
            f.write('\n\n\n')
            f.write(summary)
            f.write('\n\n\n')
            f.write('*'*25)
            f.write('\n')
            for p in body:
                f.write(p)
                f.write('\n')
            f.write('*'*25)

    except ValueError as ve:
        print(ve)


def parse_home():
    try:
        response = requests.get(HOME_URL)

        if response.status_code != 200:
            raise ValueError(f"Error: {response.status_code}")

        
        home = response.content.decode('utf-8')
        parsed = html.fromstring(home)
        links_to_notices = parsed.xpath(XPATH_LINK_TO_ARTICLE)

        if not os.path.isdir(today_y_m_d):
            os.mkdir(today_y_m_d)

        for link in links_to_notices:
            parse_notice(link, today_y_m_d)

    except ValueError as ve: 
        print(ve)

def main():
    parse_home()

if __name__ == '__main__':
    main()
