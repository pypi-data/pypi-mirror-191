from setuptools import setup, find_packages

setup(
    name='gen_passwrd',
    version='0.1',
    author='Farid Abdi',
    author_email='farid.abdi.cs@gmail.com',
    description='A simple password generator using existing tools',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    py_modules=['password_generator'],
    packages=find_packages()
)
