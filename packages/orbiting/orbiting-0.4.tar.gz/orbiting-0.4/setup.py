from setuptools import setup

setup(name='orbiting',
      version='0.004',
      description='Combines Celestrak.org with a reverse-gecoder',
      url='https://github.com/la-reine-c/Orbital',
      author='Lawrence Carter',
      author_email='lawrence.tn.carter@gmail.com',
      liscence='MIT',
      include_package_data=True,
      long_description=open('README.md').read(),
      install_requires=[
          'requests',
          'pandas',
 	  'ephem',
          'country_converter',
      ]
)
