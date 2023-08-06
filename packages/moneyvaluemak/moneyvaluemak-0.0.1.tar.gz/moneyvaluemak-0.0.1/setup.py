from setuptools import setup, find_packages


VERSION = '0.0.1'
DESCRIPTION = 'For Translate Money Number to Words'


# Setting up
setup(
    name="moneyvaluemak",
    version=VERSION,
    author="SagarMak",
    author_email="sagar.makwana@crestdatasys.com",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'money'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)