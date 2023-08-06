from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    readme = fh.read()

setup(
    name='pyspedfiscal',
    version='0.2.9',
    url='https://github.com/rodolfoscarp-jr/pyspedfiscal',
    license='MIT License',
    author='Rodolfo Scarp',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='rodolfoscarp@gmail.com',
    keywords='spedfiscal',
    description=u'Serializa um arquivo do tipo SPED Fiscal',
    packages=find_packages(exclude=['test*']),
    install_requires=['pydantic']
)
