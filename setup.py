from setuptools import setup, find_packages

setup(
    name='RESter',  # The name of the package
    version='0.1.0',  # Version of the package
    packages=find_packages(),  # Automatically finds all packages in the current directory
    description='A flexible REST API framework in Python',  # Short description of your module
    long_description=open('README.md').read(),  # Read long description from README.md
    long_description_content_type='text/markdown',  # Specifies markdown for the long description
    author='Calestial Ashley',  # Author's name
    author_email='calestialashley@gmail.com',  # Author's email
    url='https://github.com/CalestialAshley35/RESter.git',  
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[],  # List any dependencies here, e.g. 'requests'
    python_requires='>=3.7',  # Minimum Python version required
)
