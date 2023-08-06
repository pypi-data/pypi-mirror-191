from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.6'
DESCRIPTION = 'Humanize GPT Responses'
LONG_DESCRIPTION = 'A package that enhances ChatGPT\'s ability to produce human-like responses while avoiding ' \
                   'detection from AI detectors '

# Setting up
setup(
    name="gpt-humanizer",
    version=VERSION,
    author="Shaffan",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['openai'],
    keywords=['python', 'openai', 'chatgpt', 'artificial intelligence', 'avoid ai detection', 'chatgpt humanizer', 'gpt3', 'gpt-3', 'gpt 3', 'chat-gpt humanizer', 'gpt humanizer'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows"
    ]
)