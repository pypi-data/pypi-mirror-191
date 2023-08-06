from setuptools import setup

with open("README.md", "r") as arquivo:
    readme = arquivo.read()

setup(name='format BRL',
      version = "0.0.1",
      license = "MIT License",
      author = "Icaro Rubem",
      long_description=readme,
      long_description_content_type="text/markdown",
      author_email = "icarorubem63@gmail.com",
      keywords = "BRL_CONVERSOR",
      description = "Oficial",
      packages = ["BRL"],
      install_requires=[""],)