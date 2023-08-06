from setuptools import setup, find_packages

setup(name="DOMOTICARO",
      version="0.1",
      description="Paquete de instalacion de DOMOTICARO",
      author="Valentin Basel",
      author_email='valentinbasel@gmail.com',
      license="GPL3",
      url="http://roboticaro.org",
      packages=find_packages(),
      #install_requires=[i.strip() for i in
      #                  open("requirements.txt").readlines()],
      #packages=['bot','voz','domoticaro','domoticaro.hardware'],
      install_requires=["requests", "lxml", "pyserial","numpy"]
      )
