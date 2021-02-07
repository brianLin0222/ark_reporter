from jinja2 import Environment, FileSystemLoader
import os


ENV = Environment(loader=FileSystemLoader('%s' % os.path.dirname(__file__)))


def body_render(data):
    template = ENV.get_template(r'./email.html')
    output = template.render(data)
    return output


