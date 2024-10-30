# -*- codeing = utf-8 -*-
from bs4 import BeautifulSoup
import re 
import urllib.request, urllib.error
import json
from utils import *


def main():
    baseurl = "https://www.quanxue.cn/ct_rujia/zhouyi/zhouyi"
    datalist = getData(baseurl)


def getData(baseurl):
    maps = {
        '■■■■■': 0,
        '■■\u3000■■': 1,
    }
    
    datalist = {}
    for i in range(1, 65):
        cur_data = {}
        if i < 10: url = baseurl + '0' + str(i) + '.html';
        else: url = baseurl + str(i) + '.html';
        html = askURL(url)
        soup = BeautifulSoup(html, "html.parser")

        x = soup.find_all('span', class_='baguatu')[0]
        print(str(x))
        clean_text = re.sub(r'<.*?>', '', str(x))
        clean_text = [maps[i.strip()] for i in clean_text.split('\r\n') if i.strip()]
        num = 计算卦序(clean_text, up=False)
        
        cur_data['卦图'] = clean_text

        x = soup.find_all('div', class_='guaci')[0]
        clean_name = re.sub(r'<.*?>', '', str(x)).strip().split("：")[0].strip()
        clean_text =re.sub(r'<.*?>', '', str(x)).strip().split("：")[1].strip()
        cur_data['卦名'] = clean_name.strip()
        cur_data['卦辞'] = clean_text.strip()

        x = soup.find_all('pre', class_='yaoci')[0]
        clean_text = re.sub(r'<.*?>', '', str(x))
        cur_data['爻辞'] = clean_text
        
        x = soup.find_all('p', class_='tuan')[0]
        clean_text = re.sub(r'<.*?>', '', str(x))
        cur_data['彖'] = clean_text.replace('彖曰', '').strip()
        
        x = soup.find_all('p', class_='xiang')[0]
        clean_text = re.sub(r'<.*?>', '', str(x))
        cur_data['象曰'] = clean_text.replace('象曰', '').strip()
        
        datalist[num] = cur_data

    with open('meta/i_ching.json', 'w', encoding='utf-8') as g:
        json.dump(datalist, g, ensure_ascii=False, indent=2)

    return datalist


def askURL(url):
    head = {
        "User-Agent": "Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 80.0.3987.122  Safari / 537.36"
    }

    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html


if __name__ == "__main__":
    main()
    print("爬取完毕！")