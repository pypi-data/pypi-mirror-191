from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Package for debugging Python Code'
LONG_DESCRIPTION = 'A package that makes it easy to debug all python programs and lists helpful and relevant links on the same error on Github & Stackoverflow.'

setup(
    name="Errora",
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author="Lone Walker",
    author_email="lonewalkerns@gmail.com",
    license='MIT',
    packages=find_packages(),
    install_requires=['requests', 'importlib', 'beautifulsoup', 'webbrowser', 'sys'],
    keywords='debug',
    classifiers= [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ]
)