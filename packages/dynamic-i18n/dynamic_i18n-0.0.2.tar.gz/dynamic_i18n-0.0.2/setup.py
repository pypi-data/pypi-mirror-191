from setuptools import setup, find_packages

VERSION = '0.0.2'
DESCRIPTION = 'A basic dynamic class to support I18N translation'
LONG_DESCRIPTION = 'A basic dynamic class that can be used for several things, but the main purpose is to support I18N translation'

# Setting up
setup(
    name="dynamic_i18n",
    version=VERSION,
    author="Jeferson-Peter (Jeferson Peter)",
    author_email="jeferson.peter@pm.me",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['Python', 'I18N', 'Translation', 'Dynamic Class', 'Flatten Json'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)