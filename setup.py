from setuptools import setup, find_packages

setup(
    name='emailme',
    version='0.0.1',    
    description='A simple emailer',
    url='https://github.com/benschulman/emailme',
    author='Ben Schulman',
    author_email='bgschulman31@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['Jinja2>=3.0.2',
    ],

    classifiers=[
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.9',
    ],
)
