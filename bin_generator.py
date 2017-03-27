# -*- coding: utf-8 -*-


from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from jinja2 import Environment, FileSystemLoader
from faker import Factory
import glob
import os
import random
import simplejson

file_location = "/Users/mnpappo/Documents/projects/python/neural_network/date_sort_nn/gen_test"

# get a list of all the files to open
html_file_directory = os.path.join(file_location, '*.html')
html_file_list = glob.glob(html_file_directory)
# jinja2 env
env = Environment(loader=FileSystemLoader('bin_html_template'))


def escape_me(unicodeList):
    """
    Here comes the hero to rescue text from evil format.
    """
    newList = [ s.encode('utf8') for s in unicodeList ]
    prize = ""
    for s in newList:
        prize = prize + s.decode('utf-8')
    return prize


def get_date():
    dates = [
         '১লা এপ্রিল ১৯৯৩' , '২২ শে জানুয়ারী ২০০৩' , '১১ই আগস্ট ১৯৯৯', '৪ঠা জানুয়ারী ১৯৯৫',
         '২৯শে সেপ্টেম্বর ২০০৭', '৫ম ডিসেম্বর ২০১৭', '১০ম জানুয়ারী ২০১৫', '১৫ই নভেম্বর ২০১০',
         '২০১৯ ১৯শে জানুয়ারী', '২০১১ ডিসেম্বর ৭', '২৯শে অক্টোবর ২০০৭', '২১ শে আগস্ট ২০০২' ,
         '১১ই নভেম্বর ১৯৭১' , '২০১৯ ২০শে ফেব্রুয়ারী', '২০০৯ অক্টোবর ৪', '২০৩০ ৬ই ফেব্রুয়ারী',
         '২০১৮ ফেব্রুয়ারী ৩', '১২ই মার্চ ১৯৯৫' , '২০১৯ ২০শে মার্চ', '২০৯০ মার্চ ৪', '১০ম মার্চ ১২' ,
         '১৪ই এপ্রিল ১৯৩১' , '২০১৪ ২২ শে নভেম্বর', '২০৪১ এপ্রিল ৪', '১৬ম এপ্রিল ৩০',
         '২০ শে ফেব্রয়ারি, ২০১৭', '০৭/০৫/২০০৭', '২১-২০০০-১২', '২২.২০১১.০৬',' ২০১৩/২৩/১১',
         '০১ ই জানুয়ারি, ২০০৫',  '০৫/০৯/২০১৫', '২০০৩-০৭-২৫', '২০০১.১১.১২' , '২০১০/১০/২২',
         '০২ রা মার্চ ২০০৭', '১১/১২/২০০১', '২০১০-০৫-০৫', '২০১৩.১২.১৮', '২০১৭/২৫/০৫',
         '১৪ ই আগস্ট ২০০১', '০৫/০৯/২০১০', '২০০৮-১৫-০৭', '২০১৪.১১.১৮', '২০০১/২৬/০৭',
         '২২ শে ডিসেম্বর ২০১৪', '১৫/১২/২০০৬', '২০০১-২৫-০২', '২০০২.১৬.০৪', '২০০৫/২৭/০৯',
         '২৭ শে অক্টোবর ২০১২', '২৭/১১/২০০৯', '২০০৯/২৭/১২', '২০০৮.১৯.০৯', '২০০২-২২-১০',
         '০৩ রা এপ্রিল, ২০০৭', '১২/১২/২০১২', '২০০০/২০/০৫', '২০১০.২৯.০১', '২০০৭-২৭-০৫',
         '০৪ ঠা মে, ২০০৮', '১৩/০৩/২০০২', '২০০৬/৩০/১১', '২০০২.৩১.১১', '২০১০/১৮/০৬',
         '০৫ ই জুন ২০০৯', '২৫/১২/২০০৫', '২০০৭/৩১/০১', '২০১৫.২২.০৩', '২০০৯/২৩/০৪',
         '০৬ ই জুলাই ২০১০', '২৮/০৬/২০০৬', '২০১০/২৪/০৬', '২০১৩.১৪.০৮', '২০০৩/১৭/০৮',
         '০৭ ই সেপ্টেম্বর ২০১১', '২৯/০২/২০০৫', '২০০৬-২৭-০৫', '২০১১.১৯.০৯', '২০০৬/১৯/০৪',
         '০৮ ই নভেম্বর, ২০১২', '৩০/০৫/২০০৯', '২০১০-২৩-০৯', '২০১২.০৮.১৬', '২০০৭/২২/১০',
         '০৯ ই সেপ্টেম্বর, ২০০৬', '২৭/১১/২০১১', '২০১৫-২১-১০', '২০১৪.১০.১০', '২০১২.১২.১৫',
         '১০ ই ফেব্রয়ারি - ২০০১', '০২/০২/২০০২', '২০০৩-০৫-১৯', '২০১৬.০৭.১৭', '২০১৬-১৬-১২',
         '১১ ই আগস্ট,২০১০', '০৫/০৫/২০০১', '২০০৯/০৯/১৯', '২০০৩.১৫.০৩', '২০০৮.১২.০৯',
         '১২ ই ডিসেম্বর - ২০০৮', '১১/১২/২০০৯', '২০১০/১২/০১', '২০০৯.১২.১২', '২০১৫-০৬-১২',
         '১৩ ই মার্চ - ২০০৯', '২৫/০১/২০০৬', '২০১৪/০৬/২৫', '২০১৩.২৭.০৫', '২০১৩-০৯-২৯',
         '১৪ ই ফেব্রয়ারি - ২০০২', '০৩/০৬/২০০৫', '২০১৭/০১/২৩', '২০১৬.১৯.০৪', '২০০৫.১৭.০৬',
         '১৫ ই ডিসেম্বর, ২০১৪', '০৫/০৭/২০১০', '২০১৫/০৫/২৯', '২০১১.২০.০৬', '২০০৮.১৯.০৪',
         '১৬ ই সেপ্টেম্বর, ২০১১', '০৯/১০/২০০৫', '২০১৬/০৮/২৭', '২০০০.১৯.০৫', '২০০৬.২০.০৯'
    ]

    index = random.randint(0, len(dates)-1)
    date = dates[index]

    return date

def get_date_en():
    fake = Faker()
    n = 11
    #ymd
    date = date = fake.date(pattern="%Y-%m-%d")
    if random.randint(1, n) == 1:
        date = fake.date(pattern="%Y-%m-%d")
    #dmy th
    if random.randint(1, n) == 2:
        date = fake.date(pattern="%dth %B %Y")
    #dmy th
    if random.randint(1, n) == 3:
        date = fake.date(pattern="%dth %b %Y")
    #dmy
    if random.randint(1, n) == 4:
        date = fake.date(pattern="%d-%m-%Y")
    # dmy
    if random.randint(1, n) == 5:
        date = fake.date(pattern="%d/%m/%Y")
    # dmy
    if random.randint(1, n) == 11:
        date = fake.date(pattern="%d.%m.%Y")
    #ymd
    if random.randint(1, n) == 6:
        date = fake.date(pattern="%Y/%m/%d")
    #ymd
    if random.randint(1, n) == 7:
        date = fake.date(pattern="%Y,%m,%d")
    #dmy
    if random.randint(1, n) == 8:
        date = fake.date(pattern="%d,%m,%Y")
    #ymd
    if random.randint(1, n) == 9:
        date = fake.date(pattern="%m-%Y-%d")
    #ymd
    if random.randint(1, n) == 10:
        date = fake.date(pattern="%m,%Y,%d")

    return date




def get_phone():
    phone = [
         '+৩৩-০১৭১৪৩৫৯৬৬৬',
         '+৬৬০১৬৮৯৩৮৫০২১',
         '+০২-০১৯৫৩৮৭৬৩৯৭',
         '০১৬৭৮৭০৭৮৩৪',
         '০১৬৭৯৫৮২৯৩৫',
         '০২২৫২৬',
         '৮৮৭৩৪৯২০৮৭৫৭২২',
         '+৮৮১৬৪৯২০৮৭৫৭২২',
         '+৮৭১৬৪৯২০৮৭৫৭২২',
         '+৮৮১৬৪-৯২০৮৭৫৭২২',
         '২২২০১৯৮৮৫৪৭৬৮৪',
         '০১৭১৩৯৭৩৯৭৫',
         '০০০৮৭৩৮৪৫৬৭৫',
         '৫৫৭৮৭৬৮৯৩৪',
         '৪৩৫৭৬৮৮০৯৬৬৬',
         '০১১৯৯৭৫৮৪৯৩',
         '৯৮৪৩৭',
         '০১৬৭৮৮৮২২৯৯১০',
         '০১৯১৪৮৫৯৪৭৭',
         '০১৬৭৮৯০৯২৩৪',
         '০১৭৫১২৩৪৫৬৭',
         '০১১৯১৪৭৫৯৩৭',
         '০১৭৩৭৮৯৪৫৬৭',
         '০১৭৯৭৬৫৪৩২৮',
         '০০৪৪৭৮৪৫৪৭',
    ]

    index = random.randint(0, len(phone)-1)
    p = phone[index]

    return p



def htmlTemplateGenerator(bg_type, txt_type, date_bg, date_txt):
    fake = Factory.create('bn_BD')

    date = get_date()
    date_one = get_date()
    date_two = get_date()
    date_three = get_date()
    date_four = get_date()
    date_five = get_date()

    date_x = get_date()
    date_one_x = get_date()
    date_two_x = get_date()
    date_three_x = get_date()
    date_four_x = get_date()
    date_five_x = get_date()

    date_y = get_date_en()
    date_one_y = get_date_en()
    date_two_y = get_date_en()
    date_three_y = get_date_en()
    date_four_y = get_date_en()
    date_five_y = get_date_en()

    date_z = get_date_en()
    date_one_z = get_date_en()
    date_two_z = get_date_en()
    date_three_z = get_date_en()
    date_four_z = get_date_en()
    date_five_z = get_date_en()

    

    for index in range(1000000):
        file_name = "{id}.html".format(id=index)
        # check for TemplateDoesnotExist error
        try:
            template = env.get_template(file_name)
        except Exception as e:
            print ("No more template found. Tried to find {id}".format(id=index))
            print (e)
            break

        # pass params to the jinja2 template
        output_from_parsed_template = template.render(
            bg_color = bg_type,
            txt_color = txt_type,
            date_bg = date_bg,
            date_txt = date_txt,

            date = date,
            date_one = date_one,
            date_two = date_two,
            date_three = date_three,
            date_four = date_four,
            date_five = date_five,

            date_x = date_x,
            date_one_x = date_one_x,
            date_two_x = date_two_x,
            date_three_x = date_three_x,
            date_four_x = date_four_x,
            date_five_x = date_five_x,

            date_y = date_y,
            date_one_y = date_one_y,
            date_two_y = date_two_y,
            date_three_y = date_three_y,
            date_four_y = date_four_y,
            date_five_y = date_five_y,

            date_z = date_z,
            date_one_z = date_one_z,
            date_two_z = date_two_z,
            date_three_z = date_three_z,
            date_four_z = date_four_z,
            date_five_z = date_five_z,
            )

        # to save the results
        file_name = "generated_html/{id}.html".format(id=index)
        try:
            with open(file_name, "w") as htmlFIle:
                htmlFIle.write(output_from_parsed_template)
        except IOError as e:
            print ("Error: can\'t find file or read data!!!!!!")
        else:
           print ("Written HTML no {id} in the file successfully".format(id=index))
           htmlFIle.close()
    return True


def htmlToImage(path, i):
    index = i
    # for every html in the direcory
    for html_file in html_file_list:
        # get the name into the right format
        temp_name = "file://" + html_file

        # open in webpage
        # driver = webdriver.Chrome(executable_path='./tools/chromedriver')
        driver = webdriver.Firefox(executable_path='./tools/geckodriver')
        driver.set_window_position(0, 0)
        driver.maximize_window()

        print ("Rendering html {id}".format(id=index))
        driver.get(temp_name)
        image_name = str(index) + '.png'
        driver.save_screenshot(path + image_name)
        print ("Html to image {id} successfully converted".format(id=index))
        driver.quit()
        index += 1
    return True


if __name__ == '__main__':
    bg_type_black = 'black'
    bg_type_white = 'black'


    date_bg_white = 'white'
    date_bg_black = 'black'

    date_txt_white = 'white'
    date_txt_black = 'black'

    txt_type_black = 'black'
    txt_type_white = 'white'

    image_save_path_white = "./txt_white_bn/"
    image_save_path_black = "./txt_black_bn/"

    # for index in range(9300,30000,10):
    #     #white txt
    #     if htmlTemplateGenerator(bg_type_black, txt_type_white, date_bg_black, date_txt_white) is True:
    #         if htmlToImage(image_save_path_white, index) is True:
    #             print("-----------------------")
    #             print("Successfully all black job done. :) ")
    #             print("-----------------------")
    #         else:
    #             print ("Errrroooorrr!!!!!!!!")
    #
    #     #black txt
    #     if htmlTemplateGenerator(bg_type_black, txt_type_black, date_bg_white, date_txt_white) is True:
    #         if htmlToImage(image_save_path_black, index) is True:
    #             print("-----------------------")
    #             print("Successfully all white job done. :) ")
    #             print("-----------------------")
    #         else:
    #             print ("Errrroooorrr!!!!!!!!")




try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

import io
from selenium import webdriver
from PIL import Image
import json

data = {}

for i in range(10000):
    print("Data - " , i)
    fake = Factory.create('bn_BD')

    date = get_date()
    date_one = get_date()
    date_two = get_date()
    date_three = get_date()
    date_four = get_date()
    date_five = get_date()
    date_x = get_date()
    date_one_x = get_date()
    date_two_x = get_date()
    date_three_x = get_date()
    date_four_x = get_date()
    date_five_x = get_date()
    date_y = get_date()
    date_one_y = get_date()
    date_two_y = get_date()
    date_three_y = get_date()
    date_four_y = get_date()
    date_five_y = get_date()

    file_location = "/Users/mnpappo/Documents/projects/python/neural_network/date_sort_nn/gen_test/"
    # get a list of all the files to open
    html_file_directory = os.path.join(file_location, '*.html')
    html_file_list = glob.glob(html_file_directory)
    # jinja2 env
    env = Environment(loader=FileSystemLoader('bin_html_template'))

    for index in range(1000):
        file_name = "{id}.html".format(id=index)
        # check for TemplateDoesnotExist error
        try:
            template = env.get_template(file_name)
        except Exception as e:
            print ("No more template found. Tried to find {id}".format(id=index))
            print (e)
            break

        # pass params to the jinja2 template
        output_from_parsed_template = template.render(
            bg_color = bg_type,
            txt_color = txt_type,
            date_bg = date_bg,
            date_txt = date_txt,

            date = date,
            date_one = date_one,
            date_two = date_two,
            date_three = date_three,
            date_four = date_four,
            date_five = date_five,

            date_x = date_x,
            date_one_x = date_one_x,
            date_two_x = date_two_x,
            date_three_x = date_three_x,
            date_four_x = date_four_x,
            date_five_x = date_five_x,

            date_y = date_y,
            date_one_y = date_one_y,
            date_two_y = date_two_y,
            date_three_y = date_three_y,
            date_four_y = date_four_y,
            date_five_y = date_five_y,
            )

        # to save the results
        file_name = "gen_test/{id}.html".format(id=index)
        try:
            with open(file_name, "w") as htmlFIle:
                htmlFIle.write(output_from_parsed_template)
        except IOError as e:
            print ("Error: can\'t find file or read data!!!!!!")
        else:
           print ("Written HTML no {id} in the file successfully".format(id=index))
           htmlFIle.close()


    driver = webdriver.Firefox(executable_path='./tools/geckodriver')
    html_file = '/Users/mnpappo/Documents/projects/python/neural_network/date_sort_nn/gen_test/0.html'
    temp_name = "file://" + html_file

    driver.get(temp_name)

    # get the logo element
    elements = driver.find_elements_by_class_name('border')

    file_location = './test/'
    image_file_directory = os.path.join(file_location, '*.png')
    image_file_list = glob.glob(image_file_directory)
    i = 0
    index = len(image_file_list)

    for element in elements:

        date_list = [0,3,10,11,14]
        if i in date_list:
            data_type = 1
        else:
            data_type = 0

        data[index] = data_type
        rect = element.rect
        points = [rect['x'], rect['y'], rect['x'] + rect['width'], rect['y'] + rect['height']]
        with Image.open(io.BytesIO(driver.get_screenshot_as_png())) as img :
            with img.crop(points) as imgsub :
                imgsub.save("test/{}.png".format(index), 'PNG')
        index += 1
        i += 1
        print("saving imgae - ", index)

    driver.quit()

print(data)
print(len(data))

f = open('labels2.json', 'w')
simplejson.dump(data, f)
f.close()
