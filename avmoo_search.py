import os
import re
import requests
from bs4 import BeautifulSoup

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}




def get_DetailUrlAndMovieName(key):
    url = 'https://avmask.com/cn/search/' + key + '/'
    print(url,end=' ')
    response = requests.get(url)
    print(response.status_code)
    if response.status_code==403:
        exit(-1)
    body = response.text
    detail_url = re.findall('https?://avmask\.com/cn/movie/.{16}', body)
    soup = BeautifulSoup(body, "html.parser")
    info = soup.find('a', class_='movie-box')
    if info!=None:
        info = info.get_text()
    else:
        info = 'null'
    info = re.sub('\n|\s', "", info)
    info_list = re.split('[A-Z]+?-[0-9]{3}\/', info)
    return detail_url, info_list


def get_ImgUrlAndStarUrl(detail_url):
    detail_url=detail_url[0]
    response = requests.get(detail_url+ '/', headers=header)
    body = response.text
    img_url = re.findall('https://jp\.netcdn\.space/digital/video/.*?\.jpg', body)
    star_url = re.findall('https://avmask\.com/cn/star/.{16}', body)
    return star_url, img_url

def get_StarName(star_url):
    response = requests.get(star_url+ '/', headers=header)
    body = response.text
    info = re.findall('<span class="pb-10">.*?</span>', body)[0]
    info = re.sub('<.*?>', "", info)
    return info


def save_img(img_url, save_path, name):
    if img_url == []:
        return
    img = requests.get(img_url[0], headers=header)
    if not os.path.exists(save_path + r'/' + name + '.jpg'):
        with open(save_path + r'/' + name + '.jpg', 'wb') as img_f:
            img_f.write(img.content)
            print(img_url[0])
    if len(img_url) < 2:
        return
    j = 1
    for i in range(2, len(img_url), 2):
        img = requests.get(img_url[i], headers=header)
        if not os.path.exists(save_path + r'/' + str(j) + '.jpg'):
            with open(save_path + r'/' + str(j) + '.jpg', 'wb') as img_f:
                img_f.write(img.content)
                print(img_url[i])
        j += 1


if __name__ == "__main__":
    url = 'https://avmask.com/cn/search/soe-927'

    response = requests.get(url)
    body = response.text
    detail_url = re.findall('https?://avmask\.com/cn/movie/.{16}', body)

    bs4 = BeautifulSoup(body, "html.parser")
    info = bs4.find('a', class_='movie-box').get_text()
    info = re.sub('\n|\s', "", info)
    info_list = re.split('[A-Z]+?-[0-9]{3}\/', info)

    response = requests.get(detail_url[0], headers=header)
    body = response.text
    img_url = re.findall('https://jp\.netcdn\.space/digital/video/.*?\.jpg', body)
    star_url = re.findall('https://avmask\.com/cn/star/.{16}', body)

    response = requests.get(star_url[0], headers=header)
    body = response.text
    info = re.findall('<span class="pb-10">.*?</span>', body)[0]
    info = re.sub('<span class="pb-10">|</span>|\s', "", info)
    print(info)
    detail_url, full_name = get_DetailUrlAndMovieName('soe-927')
    star_url, img_url = get_ImgUrlAndStarUrl(detail_url)
    star = get_StarName(star_url)
    print(star)
