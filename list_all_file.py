import csv
import json
import os
import re
import avmoo_search


def multi_star_formate(movie_dict):
    multi_list = []
    temp_dict = {}
    print(len(movie_dict))
    for key, val in movie_dict.items():
        if int(val[-1]) == 5:
            multi_list.append(key)
            temp_dict[key]=val
    for key in multi_list:
        del movie_dict[key]
    print(len(movie_dict))
    with open(r'./movie_dict.txt', 'w', encoding='utf8') as f1:
        for key, val in movie_dict.items():
            f1.write(key + ',' + val[0] + ',' + val[1] + ',' + val[2] + ',' + val[3] + ',' + str(val[4]) + '\n')
    for file_keycode in multi_list:
        print(file_keycode)
        starlist = []
        detail_url, full_name = avmoo_search.get_DetailUrlAndMovieName(file_keycode)
        if not detail_url:
            full_name = 'null'
            starlist.append('unknown')
            star_urls = []
        else:
            full_name = re.sub('\/|\*|,', "", full_name[0])
            star_urls, img_url = avmoo_search.get_ImgUrlAndStarUrl(detail_url)
            if not star_urls:
                starlist.append('unknown')
            elif len(star_urls) > 1:
                for star_url in star_urls:
                    starlist.append(avmoo_search.get_StarName(star_url))
            else:
                starlist.append(avmoo_search.get_StarName(star_urls[0]))
        movie_dict[file_keycode] = [temp_dict[file_keycode][0]] + [starlist] + temp_dict[file_keycode][2:]
        with open(r'./movie_dict.txt', 'a', encoding='utf8') as f1:
            for star in starlist:
                # f1.write(file_keycode + ',' + full_name + ',' + star + ',' + file_dir + ',' + 'y' + ',' + star_len
                # + '\n')
                f1.write(file_keycode + ',' + full_name + ',' + star + ',' + temp_dict[file_keycode][
                    2] + ',' + 'y' + ',' + str(len(star_urls)) + '\n')
                print(file_keycode + ',' + full_name + ',' + star + ',' + temp_dict[file_keycode][
                    2] + ',' + 'y' + ',' + str(len(star_urls)) + '\n', end='')


def list_file(filepath, movie_dict, code_front):
    files = os.listdir(filepath)
    for file in files:
        file_dir = os.path.join(filepath, file)
        if os.path.isfile(file_dir):
            file_name, ext = os.path.splitext(file)
        else:
            file_name = file
            ext = ''
        file_keycode = re.findall('[A-Za-z]+?-[0-9]{3,4}', file_name)
        if not file_keycode:
            for front in code_front:
                file_keycode = re.findall(front + '[0-9]{3,4}', file_name)
                if file_keycode:
                    file_keycode = file_keycode[0]
                    file_keycode = front + '-' + file_keycode[-3:]
                    break
            if os.path.isdir(file_dir) and file_keycode == []:
                list_file(file_dir, movie_dict, code_front)
            continue
        else:
            file_keycode = file_keycode[0]
            print(file_keycode)
        if file_keycode in movie_dict.keys():
            continue
        if (not os.path.isdir(os.path.join(filepath, file_keycode))) and (
        not os.path.isdir(os.path.join(filepath, file_keycode + ext))):
            print('mkdir')
            if os.path.isfile(file_dir):
                os.rename(file_dir, os.path.join(filepath, file_keycode + ext))
                file_dir = os.path.join(filepath, file_keycode + ext)
            else:
                os.rename(file_dir, os.path.join(filepath, file_keycode))
                file_dir = os.path.join(filepath, file_keycode)
        starlist = []
        detail_url, full_name = avmoo_search.get_DetailUrlAndMovieName(file_keycode)
        if not detail_url:
            full_name = 'null'
            starlist.append('unknown')
            star_urls = []
        else:
            full_name = re.sub('\/|\*|,', "", full_name[0])
            star_urls, img_url = avmoo_search.get_ImgUrlAndStarUrl(detail_url)

            if not star_urls:
                starlist.append('unknown')
            elif len(star_urls) > 1:
                for star_url in star_urls:
                    starlist.append(avmoo_search.get_StarName(star_url))
                movie_dict[file_keycode] = [full_name, starlist, file_dir, 'y', str(len(star_urls))]
            else:
                starlist.append(avmoo_search.get_StarName(star_urls[0]))
                movie_dict[file_keycode] = [full_name, starlist[0], file_dir, 'y', str(len(star_urls))]
        for star in starlist:
            with open(r'./movie_dict.txt', 'a', encoding='utf8') as f1:
                # f1.write(file_keycode + ',' + full_name + ',' + star + ',' + file_dir + ',' + 'y' + ',' + star_len + '\n')
                f1.write(file_keycode + ',' + full_name + ',' + star + ',' + file_dir + ',' + 'y' + ',' + str(
                    len(star_urls)) + '\n')
                print(file_keycode + ',' + full_name + ',' + star + ',' + file_dir + ',' + 'y' + ',' + str(
                    len(star_urls)) + '\n', end='')
def movie_txt2csv():
    movie_dict = []
    with open(r'./movie_dict.txt', 'r', encoding='utf8') as f1:
        j=0
        for line in f1:
            line = re.sub('\n', '', line)
            list1 = re.split(',', line)
            movie_dict.append(list1)

    with open(r'./movie.csv', 'w', encoding='GB18030',newline='') as csv1:
        writer = csv.writer(csv1)
        writer.writerows(movie_dict)

if __name__ == "__main__":
    movie_dict = {}
    code_front = []

    # 电影的字典结构{电影编号：[电影名，演员名，存储地址，是否下载，是否单体]}
    # 番号前缀表为list
    # with open(r'./movie_dict.txt', 'r', encoding='utf8') as f1:
    #     for line in f1:
    #         line = re.sub('\n', '', line)
    #         list1 = re.split(',', line)
    #         if (list1[0] in movie_dict.keys()) and os.path.exists(movie_dict[list1[0]][2]):
    #             print(list1[0])
    #             continue
    #         movie_dict[list1[0]] = list1[1:]

    with open(r'./影片字典.json', 'r', encoding='utf8') as f1:
        movie_dict=json.load(f1)
        movie_dict = dict(movie_dict)

    with open(r'./前缀列表.json', 'r', encoding='utf8') as f1:
        code_front=json.load(f1)
        code_front = list(code_front)

    movie_txt2csv()

    # for key , val in movie_dict.items():
    #     front = re.sub('-[0-9]{3}', '', key)
    #     if val[0]!='null' and (not front in code_front):
    #         code_front.append(front)
    #     if int(val[-1])==4:
    #         movie_dict[key][-1] = 1

    # with open(r'./movie_dict.txt', 'w',encoding='utf8') as f1:
    #     f1.write('')

    # file_dirs = [r'x:\大文件', r'y:\item', r'z:\system\item']
    # for file_d in file_dirs:
    #     files = os.listdir(file_d)
    #     for file in files:  # file是star对应的目录
    #         file_d = os.path.join(file_d, file)
    #         print(file_d)
    #         #list_file(file_d,movie_dict,code_front)
    print(len(movie_dict))
    #multi_star_formate(movie_dict)

    print(len(movie_dict))
    print(code_front)

    with open(r'./影片字典.json', 'w', encoding='utf8') as jfile:
        json.dump(movie_dict, jfile)

    with open(r'./前缀列表.json', 'w', encoding='utf8') as f1:
        json.dump(code_front, f1)

    # with open(r'./前缀列表.json', 'r', encoding='utf8') as f1:
    #     movie=json.load(f1)
    #     movie = dict(movie)
    #
    # print(s)
