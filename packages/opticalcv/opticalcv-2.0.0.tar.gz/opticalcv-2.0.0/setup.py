from setuptools import setup

setup(
    name="opticalcv",
    version="2.0.0",
    description="optical character verification",
    author="anas.ali",
    author_email="anas.ali@pekatvision.com",
    packages=["opticalcv"],
    package_data={
        'opticalcv': ['train.py'],
    },
    
)
