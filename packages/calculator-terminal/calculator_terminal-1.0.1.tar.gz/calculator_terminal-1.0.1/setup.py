import os
from distutils.command.register import register as register_orig
from distutils.command.upload import upload as upload_orig

from setuptools import setup


class register(register_orig):

    def _get_rc_file(self):
        return os.path.join('.', '.pypirc')

class upload(upload_orig):

    def _get_rc_file(self):
        return os.path.join('.', '.pypirc')

setup(
    
    name="calculator_terminal",
    version="1.0.1",
    description="La mejor calculadora que veras, puedes utilizarla en la terminal de tu interprete e incluso puedes utilizarla para distintas APIs que vayas a crear con sus multifunciones y todos los errores entendibles que se invocan cuando algo falla.",
    author="Developer Anonymous#8593",
    author_email="developeranonymous_buss@hotmail.com",
    url="https://github.com/Developer-Anony/calculator",
    packages= [],
    cmdclass={
        'register': register,
        'upload': upload,
    }
)