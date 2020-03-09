from urllib.request import urlopen
from bs4 import BeautifulSoup
# import pickle
# import os
import csv
from tqdm import tqdm

with open(r'C:\Users\lp\Desktop\opensar.csv','w', newline='') as csvfile:
    fieldnames = ['dataset name', 'link', 'Public Or Protected', 'Data Name', 'Owner', 'Sensor Platform',
                  'Operation Mode', 'Band', 'Polarization', 'Single Or Multilook', 'Data Domain', 'Cover Area',
                  'Scene', 'Image Acquisition Time', 'Azimuth Pixel Size', 'Slant Range Pixel Size',
                  'Ground Range Pixel Size', 'Cover Area Latlng', 'Data Time Original (UTC)']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for page in tqdm(range(1, 12)):
        if 1 == page:
            init_url = 'http://opensar.sjtu.edu.cn/Data/Search'
        else:
            init_url = f'http://opensar.sjtu.edu.cn/Data/Search?page={page}'
        # create current dict
        my_dict = {}
        content = urlopen(init_url).read()
        soup = BeautifulSoup(content, 'html.parser')
        # a = soup.prettify()
        my_datasets = soup.find_all('a', title=True)  # title is not empty
        for this_dataset in my_datasets:
            this_title = this_dataset['title']
            this_herf = 'http://opensar.sjtu.edu.cn' + this_dataset['href']
            my_dict['dataset name'] = this_title
            my_dict['link'] = this_herf

            this_content = urlopen(this_herf).read()
            this_soup = BeautifulSoup(this_content, 'html.parser')
            # a = soup.prettify()
            my_table = this_soup.find_all('table')[0]  # after the book section
            my_tags = my_table.find_all('b')
            for this_tag in my_tags:
                # a = this_tag.parent.text
                this_tag_name_value = this_tag.parent.text.split("：")
                this_tag_name = this_tag.text.strip()
                if len(this_tag_name_value) == 2:
                    my_dict[this_tag_name] = this_tag_name_value[1].strip()
                elif len(this_tag_name_value) == 3:  # last two tags share one parent, so be name1 : value1\n name2: value2
                    if 'Cover Area Latlng' == this_tag_name:
                        my_dict[this_tag_name] = this_tag_name_value[1].split('\n')[0].strip()
                    else:
                        my_dict[this_tag_name] = this_tag_name_value[2].strip()
            writer.writerow(my_dict)

pass