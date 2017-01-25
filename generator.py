from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from jinja2 import Environment, FileSystemLoader
from faker import Faker
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
        prize = prize + s
    return prize


def get_date():
    fake = Faker()

    date = date = fake.date(pattern="%Y-%m-%d")
    if random.randint(1, 10) == 1:
        date = fake.date(pattern="%Y-%m-%d")

    if random.randint(1, 10) == 2:
        date = fake.date(pattern="%dth %B %Y")

    if random.randint(1, 10) == 3:
        date = fake.date(pattern="%dth %b %Y")

    if random.randint(1, 10) == 4:
        date = fake.date(pattern="%d-%m-%Y")

    if random.randint(1, 10) == 5:
        date = fake.date(pattern="%d/%m/%Y")

    if random.randint(1, 10) == 6:
        date = fake.date(pattern="%Y/%m/%d")

    if random.randint(1, 10) == 7:
        date = fake.date(pattern="%Y,%m,%d")

    if random.randint(1, 10) == 8:
        date = fake.date(pattern="%d,%m,%Y")

    if random.randint(1, 10) == 9:
        date = fake.date(pattern="%Y-%m-%d")

    if random.randint(1, 10) == 10:
        date = fake.date(pattern="%Y-%m-%d")

    return date

def htmlTemplateGenerator(bg_type):
    fake = Faker()

    for index in range(100000):
        file_name = "{id}.html".format(id=index)
        # check for TemplateDoesnotExist error
        try:
            template = env.get_template(file_name)
        except Exception as e:
            print ("No more template found. Tried to find {id}".format(id=index))
            print ("--------------------")
            break
        # pass params to the jinja2 template
        output_from_parsed_template = template.render(
            bg_color = bg_type,

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
            postcode = fake.postalcode(),
            zipcode = fake.zipcode(),
            street_address = fake.street_address(),
            address = fake.address(),

            phone = fake.phone_number(),
            email = fake.email(),

            date = get_date(),
            date_one = get_date(),
            date_two = get_date(),
            date_three = get_date(),
            date_four = get_date(),
            date_five = get_date(),
            day = fake.day_of_week(),
            time = fake.time(pattern="%H:%M:%S"),

            name = fake.name(),
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
            with open(file_name, "wb") as htmlFIle:
                htmlFIle.write(output_from_parsed_template)
        except IOError as e:
            print ("Error: can\'t find file or read data!!!!!!")
        else:
           print ("Written HTML no {id} in the file successfully".format(id=index))
           htmlFIle.close()
    return True


def htmlToImage(image_path, i):
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
        driver.save_screenshot(image_path + image_name)
        print ("Html to image {id} successfully converted".format(id=index))
        driver.quit()
        index += 1
    return True


if __name__ == '__main__':
    bg_type_black = 'black'
    bg_type_white = ''
    image_save_path_white = "./converted_images/"
    image_save_path_black = "./converted_images_black/"

    for index in range(0,20,10):
        if htmlTemplateGenerator(bg_type_white) is True:
            if htmlToImage(image_save_path_white, index) is True:
                print("-----------------------")
                print("Successfully all white job done. :) ")
                print("-----------------------")
            else:
                print ("Errrroooorrr!!!!!!!!")

        if htmlTemplateGenerator(bg_type_black) is True:
            if htmlToImage(image_save_path_black, index) is True:
                print("-----------------------")
                print("Successfully all black job done. :) ")
                print("-----------------------")
            else:
                print ("Errrroooorrr!!!!!!!!")
