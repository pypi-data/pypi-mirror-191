from setuptools import setup

setup(
   name='pyeasygame',
   version='3.5.2',
   description='A useful game engine for beginners',
   author='Morris El Helou',
   author_email='morriselhelou816@gmail.com',
   include_package_data=True,
   packages=['pyeasygame'], 
   package_data={"pyeasygame": ["*.png"]},
   install_requires=['pygame','keyboard'], #external packages as dependencies
)