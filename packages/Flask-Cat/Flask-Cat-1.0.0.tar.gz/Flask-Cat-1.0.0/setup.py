from setuptools import setup, find_packages

long_description = open('./README.md')

setup(
    name='Flask-Cat',
    version='1.0.0',
    url='https://github.com/ZSendokame/Flask-Cat',
    license='MIT license',
    author='ZSendokame',
    description='Flask-Cat returns a cat for each status code above 399.',
    long_description=long_description.read(),
    long_description_content_type='text/markdown',

    packages=(find_packages(include=['flaskcat']))
)