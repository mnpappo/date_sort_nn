#using jinja2 templating 
from docxtpl import DocxTemplate

doc = DocxTemplate("template/docTemplate-1.docx")
context = { 'company_name' : "World company", }
doc.render(context)
doc.save("generated/generated_doc.docx")