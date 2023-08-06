from setuptools import setup

readme = open("./README.md", "r", encoding="utf8")

setup(
    name='Dragon-Ball-API',
    packages=['DragonBall', 'DragonBall.Constants', 'DragonBall.Data', 'DragonBall.Soup'],
    # this must be the same as the name above
    version='1.0.0',
    description='Api unofficial de dragon ball inspirado de la fandom de dragon ball',
    long_description=readme.read(),
    long_description_content_type='text/markdown',
    author='Eduardo Lopez',
    author_email='nanguelulpz@gmail.com',
    # use the URL to the GitHub repo
    url='https://github.com/eduardo-nanguelu/Dragon-Ball-API',
    download_url='https://github.com/eduardo-nanguelu/Dragon-Ball-API/tarball/0.1',
    keywords=['Dragon-Ball-Api', 'Dragon Ball', 'Api Dragon Ball'],
    classifiers=[],
    install_requires=['requests~=2.28.2', 'beautifulsoup4~=4.11.2'],
    license='MIT',
    include_package_data=True
)
