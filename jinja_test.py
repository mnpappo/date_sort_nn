#using jinja2 templating
from docxtpl import DocxTemplate
from faker import Faker

doc = DocxTemplate("template/docTemplate-1.docx")
fake = Faker()

def escaper(unicodeList):
    newList = [ s.encode('utf8') for s in unicodeList ]
    finalPara = ""
    for s in newList:
        finalPara = finalPara + s
    return finalPara

for inc in range(3):
    context = {
        'title_h1_bold' : fake.sentence(nb_words=6, variable_nb_words=True),
        'title_h1_normal' : fake.sentence(nb_words=4, variable_nb_words=True),
        'name' : fake.name(),
        'email' : fake.email(),
        'phone' : fake.phone_number(),
        'date' : fake.date(pattern="%Y-%m-%d"),
        'para_one' : escaper(fake.paragraphs(nb=4)),
        'single_sentence_one' : fake.sentence(nb_words=7, variable_nb_words=True),
        'single_sentence_two' : fake.sentence(nb_words=9, variable_nb_words=True),
        'single_sentence_three' : fake.sentence(nb_words=5, variable_nb_words=True),
        'para_two' : escaper(fake.paragraphs(nb=5)),
        }
    doc.render(context)
    doc.save("generated/generated_doc_{id}.docx".format(id=inc))
