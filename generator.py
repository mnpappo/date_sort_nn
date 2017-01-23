from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from jinja2 import Environment, FileSystemLoader
from faker import Faker
import glob
import os

file_location = "/home/machine/Documents/kill_bill/generated_html"

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
            my_string = fake.name(),
            text = escape_me(fake.paragraphs(nb=4)),
            date = fake.date(pattern="%Y-%m-%d"),
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


def htmlToImage(image_path):
    index = 1
    # for every html in the direcory
    for html_file in html_file_list:
        # get the name into the right format
        temp_name = "file://" + html_file

        # open in webpage
        driver = webdriver.Chrome(executable_path='./tools/chromedriver')
        # driver = webdriver.Firefox()
        driver.set_window_position(0, 0)
        # driver.set_window_size(1024, 768)
        driver.set_window_size(1366, 768)

        print ("Rendering html {id}".format(id=index))
        driver.get(temp_name)
        image_name = '0' + str(index) + '.png'
        driver.save_screenshot(image_path + image_name)
        print ("Html to image {id} successfully converted".format(id=index))
        driver.quit()
        index += 1
    return True


if __name__ == '__main__':
    bg_type_black = 'black'
    bg_type_white = 'white'
    image_save_path_white = "./converted_images/"
    image_save_path_black = "./converted_images_black/"

    if htmlTemplateGenerator(bg_type_white) is True:
        if htmlToImage(image_save_path_white) is True:
            print("-----------------------")
            print("Successfully all job done. :) ")
            print("-----------------------")
        else:
            print ("Errrroooorrr!!!!!!!!")

    if htmlTemplateGenerator(bg_type_black) is True:
        if htmlToImage(image_save_path_black) is True:
            print("-----------------------")
            print("Successfully all job done. :) ")
            print("-----------------------")
        else:
            print ("Errrroooorrr!!!!!!!!")
