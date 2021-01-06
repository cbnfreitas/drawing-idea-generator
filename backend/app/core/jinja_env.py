import pathlib

from jinja2 import Environment, PackageLoader, select_autoescape

from ..core import s

dir_name = 'app'  # TODO

jinja_env = Environment(
    loader=PackageLoader(dir_name, s.EMAIL_TEMPLATES_DIR),
    autoescape=select_autoescape(['html', 'xml'])
)
