from distutils.core import setup
setup(
  name = 'pyvectorguidance',         # How you named your package folder (MyLib)
  packages = ['pyvectorguidance'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='Apache Software License',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Vector Guidance method implemented in Python.',   # Give a short description about your library
  author = 'Iftach Naftaly',                   # Type in your name
  author_email = 'iftahnaf@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/iftahnaf/pyvectorguidance',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['Python', 'Vector Guidance'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'numpy==1.21.5',
          'rich==13.3.1',
          'scipy==1.10.0'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: Apache Software License',   # Again, pick a license
    'Programming Language :: Python :: 3.10'
  ],
)