
from distutils.core import setup

import setuptools
setup(
  name = 'PythonAvroSchemas',         # How you named your package folder (MyLib)
  # packages = ['PythonAvroSchemas'],   # Chose the same as "name"
  version = '1.2.0',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Library containing the python classes that represent avro schemas used in HelpSociety project',   # Give a short description about your library
  author = 'Steven Sopilidis',                   # Type in your name
  author_email = 'stefanossopilidis2003@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/StevenSopilidis/PythonAvroSchemas',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/StevenSopilidis/PythonAvroSchemas/archive/refs/tags/v1.0.0-alpha.tar.gz',    # I explain this later on
  keywords = ['Avro Schemas'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
  ],
  package_dir={"":"src"},
  packages= setuptools.find_packages(where="src")
)
