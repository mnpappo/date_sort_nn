# -*- coding: utf-8 -*-


from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from jinja2 import Environment, FileSystemLoader
from faker import Factory
import glob
import os
import random

file_location = "/Users/mnpappo/Documents/projects/python/neural_network/date_sort_nn/generated_html"

# get a list of all the files to open
html_file_directory = os.path.join(file_location, '*.html')
html_file_list = glob.glob(html_file_directory)
# jinja2 env
env = Environment(loader=FileSystemLoader('html_template'))


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
         '১লা জানুয়ারী ১৯৯৩' , '২২ শে জানুয়ারী ২০০৩' , '১১ই জানুয়ারী ১৯৯৯', '৪ঠা জানুয়ারী ১৯৯৫',
         '২৯শে জানুয়ারী ২০০৭', '৫ম জানুয়ারী ২০১৭', '১০ম জানুয়ারী ২০১৫', '১৫ই জানুয়ারী ২০১০',
         '২০১৯ ১৯শে জানুয়ারী', '২০১১ জানুয়ারী ৭', '২৯শে ফেব্রুয়ারী ২০০৭', '২১ শে ফেব্রুয়ারী ২০০২' ,
         '১১ই ফেব্রুয়ারী ১৯৭১' , '২০১৯ ২০শে ফেব্রুয়ারী', '২০০৯ ফেব্রুয়ারী ৪', '২০৩০ ৬ই ফেব্রুয়ারী',
         '২০১৮ ফেব্রুয়ারী ৩', '১২ই মার্চ ১৯৯৫' , '২০১৯ ২০শে মার্চ', '২০৯০ মার্চ ৪', '১০ম মার্চ ১২' ,
         '১৪ই এপ্রিল ১৯৩১' , '৩০০০ ২২ শে এপ্রিল', '২০৪১ এপ্রিল ৪', '১৬ম এপ্রিল ৩০',
         '২০ শে ফেব্রয়ারি, ২০১৭', '০৭/০৫/২০০৭', '২১-২০০০-১২', '২২.২০১১.০৬',' ২০১৩/২৩/১১',
         '০১ ই জানুয়ারি, ২০০৫',  '০৫/০৯/২০১৫', '২০০৩-০৭-২৫', '২০০১.১১.১২' , '২০১০/১০/২২',
         '০২ রা মার্চ' , '২০০৭,১১/১২/২০০১', '২০১০-০৫-০৫', '২০১৩.১২.১৮', '২০১৭/২৫/০৫', '১৪ ই আগস্ট',
         '২০০১,০৫/০৯/২০১০', '২০০৮-১৫-০৭', '২০১৪.১১.১৮', '২০০১/২৬/০৭', '২২ শে ডিসেম্বর',
         '২০১৪,১৫/১২/২০০৬', '২০০১-২৫-০২', '২০০২.১৬.০৪', '২০০৫/২৭/০৯', '২৭ শে অক্টোবর',
         '২০১২,২৭/১১/২০০৯', '২০০৯/২৭/১২', '২০০৮.১৯.০৯', '২০০২-২২-১০', '০৩ রা এপ্রিল',
         '২০০৭,১২/১২/২০১২', '২০০০/২০/০৫', '২০১০.২৯.০১', '২০০৭-২৭-০৫', '০৪ ঠা মে, ২০০৮',
         '১৩/০৩/২০০২', '২০০৬/৩০/১১', '২০০২.৩১.১১', '২০১০/১৮/০৬', '০৫ ই জুন২০০৯',
         '২৫/১২/২০০৫', '২০০৭/৩১/০১', '২০১৫.২২.০৩', '২০০৯/২৩/০৪', '০৬ ই জুলাই২০১০',
         '২৮/০৬/২০০৬', '২০১০/২৪/০৬', '২০১৩.১৪.০৮', '২০০৩/১৭/০৮', '০৭ ই সেপ্টেম্বর ২০১১',
         '২৯/০২/২০০৫', '২০০৬-২৭-০৫', '২০১১.১৯.০৯', '২০০৬/১৯/০৪', '০৮ ই নভেম্বর, ২০১২',
         '৩০/০৫/২০০৯', '২০১০-২৩-০৯', '২০১২.০৮.১৬', '২০০৭/২২/১০', '০৯ ই জানুয়ারি, ২০০৬',
         '২৭/১১/২০১১', '২০১৫-২১-১০', '২০১৪.১০.১০', '২০১২.১২.১৫', '১০ ই ফেব্রয়ারি - ২০০১',
         '০২/০২/২০০২', '২০০৩-০৫-১৯', '২০১৬.০৭.১৭', '২০১৬-১৬-১২', '১১ ই আগস্ট,২০১০',
         '০৫/০৫/২০০১', '২০০৯/০৯/১৯', '২০০৩.১৫.০৩', '২০০৮.১২.০৯', '১২ ই ডিসেম্বর - ২০০৮',
         '১১/১২/২০০৯', '২০১০/১২/০১', '২০০৯.১২.১২', '২০১৫-০৬-১২', '১৩ ই মার্চ - ২০০৯',
         '২৫/০১/২০০৬', '২০১৪/০৬/২৫', '২০১৩.২৭.০৫', '২০১৩-০৯-২৯', '১৪ ই ফেব্রয়ারি - ২০০২',
         '০৩/০৬/২০০৫', '২০১৭/০১/২৩', '২০১৬.১৯.০৪', '২০০৫.১৭.০৬', '১৫ ই ডিসেম্বর, ২০১৪',
         '০৫/০৭/২০১০', '২০১৫/০৫/২৯', '২০১১.২০.০৬', '২০০৮.১৯.০৪', '১৬ ই সেপ্টেম্বর, ২০১১',
         '০৯/১০/২০০৫', '২০১৬/০৮/২৭', '২০০০.১৯.০৫', '২০০৬.২০.০৯'
    ]

    index = random.randint(0, len(dates)-1)
    date = dates[index]

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

            company_name = fake.company(),
            company = fake.company(),
            company_one = fake.company(),
            company_two = fake.company(),
            company_three = fake.company(),
            job = fake.job(),
            job_one = fake.job(),
            job_two = fake.job(),
            job_three = fake.job(),

            building_number = fake.building_number(),
            street_name = fake.street_name(),
            city = fake.city(),
            postcode = fake.postcode(),
            zipcode = fake.postcode(),
            street_address = fake.street_address(),
            address = fake.address(),

            phone = get_date(),
            email = fake.email(),

            date = get_date(),
            date_one = get_date(),
            date_two = get_date(),
            date_three = get_date(),
            date_four = get_date(),
            date_five = get_date(),
            day = fake.day_of_week(),
            time = fake.time(pattern="%H:%M:%S"),


            name = escape_me(fake.name()),
            name_two = fake.name(),
            name_three = fake.name(),

            paragraph_one = escape_me(fake.paragraphs(nb=1)),
            paragraph_two = escape_me(fake.paragraphs(nb=1)),
            paragraph_three = escape_me(fake.paragraphs(nb=1)),
            paragraph_four = escape_me(fake.paragraphs(nb=1)),
            paragraph_five = escape_me(fake.paragraphs(nb=1)),
            paragraph_six = escape_me(fake.paragraphs(nb=1)),
            paragraph_seven = escape_me(fake.paragraphs(nb=1)),
            paragraph_eight = escape_me(fake.paragraphs(nb=1)),

            sentence_one = fake.sentence(nb_words=12, variable_nb_words=True),
            sentence_two = fake.sentence(nb_words=9, variable_nb_words=True),
            sentence_three = fake.sentence(nb_words=4, variable_nb_words=True),
            sentence_four = fake.sentence(nb_words=9, variable_nb_words=True),
            sentence_five = fake.sentence(nb_words=5, variable_nb_words=True),
            sentence_six = fake.sentence(nb_words=6, variable_nb_words=True),
            sentence_seven = fake.sentence(nb_words=4, variable_nb_words=True),
            sentence_eight = fake.sentence(nb_words=9, variable_nb_words=True),
            sentence_nine = fake.sentence(nb_words=8, variable_nb_words=True),
            sentence_ten = fake.sentence(nb_words=6, variable_nb_words=True),
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

    for index in range(0,30000,10):
        #white txt
        if htmlTemplateGenerator(bg_type_black, txt_type_white, date_bg_black, date_txt_white) is True:
            if htmlToImage(image_save_path_white, index) is True:
                print("-----------------------")
                print("Successfully all black job done. :) ")
                print("-----------------------")
            else:
                print ("Errrroooorrr!!!!!!!!")

        #black txt
        if htmlTemplateGenerator(bg_type_black, txt_type_black, date_bg_white, date_txt_white) is True:
            if htmlToImage(image_save_path_black, index) is True:
                print("-----------------------")
                print("Successfully all white job done. :) ")
                print("-----------------------")
            else:
                print ("Errrroooorrr!!!!!!!!")
