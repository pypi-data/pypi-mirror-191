import io
import os
import re
from setuptools import setup

scriptFolder = os.path.dirname(os.path.realpath(__file__))
os.chdir(scriptFolder)

# Find version info from module (without importing the module):
with open('autoguix/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

# Use the README.md content for the long description:
with io.open("README.md", encoding="utf-8") as fileObj:
    long_description = fileObj.read()

setup(
    name='AutoGUIX',
    version=version,
    url='https://github.com/4akhilkumar/autoguix',
    author='Sai Akhil Kumar Reddy N',
    author_email='4akhilkumar@gmail.com',
    description=('AutoGUIX is the extended version of PyAutoGUI. Few features are added with the help of PyGetWindow and PyAutoGUI.'),
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='BSD',
    packages=['AutoGUIX'],
    keywords="gui automation test testing keyboard click press keystroke control",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    zip_safe=True
)
