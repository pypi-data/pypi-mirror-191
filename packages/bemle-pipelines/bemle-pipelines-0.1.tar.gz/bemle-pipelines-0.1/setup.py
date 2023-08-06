from distutils.core import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setup(
  name = 'bemle-pipelines',         # How you named your package folder (MyLib)
  packages = ['src'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = "Automation for Machine Learning Tasks",
  long_description=long_description,
  long_description_content_type="text/markdown",   # Give a short description about your library
  author = 'Vicky',                   # Type in your name
  author_email = 'waqasbilal02@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/IamVicky90/bemle-pipelines',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/IamVicky90/bemle-pipelines/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['automation', 'automl', 'bemle','mlpipelines'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'numpy==1.23.1',
          'pandas==1.4.3',
          'scikit-learn==1.1.2',

      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
  ],
  python_requires=">=3.8",
)