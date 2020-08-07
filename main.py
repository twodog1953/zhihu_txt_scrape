from urllib.request import urlopen as uReq
import urllib.request
from bs4 import BeautifulSoup as soup
from time import sleep
import json
import os

q_num = '295342639'
rest_t = 0.5

headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36',
}

# building urls
my_url = 'https://www.zhihu.com/api/v4/questions/' + q_num + '/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%2Cis_recognized%2Cpaid_info%2Cpaid_info_content%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics&limit=5&offset=0&platform=desktop&sort_by=default'
temp_url = 'https://www.zhihu.com/question/' + q_num

uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()

uClient2 = uReq(temp_url)
temp_html = uClient2.read()
uClient2.close()
temp_soup = soup(temp_html, "html.parser")
temp_header = temp_soup.h1

folder_name = temp_header.get_text()

if folder_name[-1] == '?':
    folder_name = folder_name[0:-1]

folder_name = folder_name + ' (text version)'


is_end = False

n = 1

while is_end == False:
    sleep(rest_t)
    print('Next page ...')
    aa = json.loads(page_html)
    # three big catagory: ad_info, data, paging
    paging = aa["paging"]
    data = aa['data']
    for i in data:
        # find all img
        content = i['content']
        author_tot = i['author']
        author_name = author_tot['name']
        page_soup = soup(content, "html.parser")

        containers = page_soup.get_text()

        # # all kinds of replacement to fit in txt files
        # containers1 = str(page_soup).replace('<p class="ztext-empty-paragraph"><br/></p>', ' \n')
        # containers2 = containers1.replace('<p>', '    ')
        #
        # containers = containers2.replace('</p>', '\n').replace('<br>', '    ').replace('</br>', ' \n').replace('<br/>', '     ')
        #
        # # remove <figure>
        # start_lst = []
        # end_lst = []
        # for ij in range(len(containers)):
        #     if containers[ij:ij + 7] == '<figure':
        #         start_lst.append(ij)
        #     if containers[ij:ij + 9] == '</figure>':
        #         end_lst.append(ij)
        # for ji in range(len(start_lst)):
        #     containers = containers.replace(containers[start_lst[ji]:end_lst[ji]],
        #                                     ' ' * len(containers[start_lst[ji]:end_lst[ji]]))
        #
        # # remove <a>
        # start_lst = []
        # end_lst = []
        # for ij in range(len(containers)):
        #     if containers[ij:ij + 2] == '<a':
        #         start_lst.append(ij)
        #     if containers[ij:ij + 4] == '</a>':
        #         end_lst.append(ij)
        # for ji in range(len(start_lst)):
        #     containers = containers.replace(containers[start_lst[ji]:end_lst[ji]],
        #                                     ' ' * len(containers[start_lst[ji]:end_lst[ji]]))
        #
        # containers = containers.replace('</figure>', ' ' * len('</figure>')).replace('<hr/>',
        #                                                                              ' ' * len('<hr/>')).replace(
        #     '<blockquote>', ' ' * len('<blockquote>')).replace('</blockquote>', ' ' * len('</blockquote>')).replace(
        #     '</b>', ' ').replace('<b>', '   ')
        # print(containers)

        # img_links = []
        # for j in containers:
        #     img_links.append(j['src'])
        # print(img_links)

        # save 2 dir
        current_directory = os.getcwd()
        final_directory = os.path.join(current_directory, folder_name)
        if not os.path.exists(final_directory):
            os.makedirs(final_directory)

        os.chdir(final_directory)

        f = open('Answer No. ' + str(n) + '.txt', 'w', encoding='utf-8')
        f.write('Author name: ' + author_name + '\n')
        f.write('Answer content: \n')
        f.write(containers)
        f.close()
        n += 1

        os.chdir(current_directory)

    is_end = paging['is_end']
    my_url = paging['next']

    uClient = uReq(my_url)
    page_html = uClient.read()
    uClient.close()

print('Everything finished lol')

# page_soup = soup(page_html, "html.parser")
# # j = json.loads(uClient.read())
# print(page_soup.h1)
# containers = page_soup.findAll('img',{"class": "origin_image zh-lightbox-thumb"})
# print(containers)
#
# img_links = []
# for j in containers:
#     img_links.append(j['src'])
# print(img_links)
