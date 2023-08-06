import setuptools    

setuptools.setup(
    name='excel_to_dataframe',
    version='0.2.54',
    author='Nelson Rossi Bittencourt',
    author_email='nbittencourt@hotmail.com',
    description='C++ library (dll or so) to converts Excel worksheets to Pandas dataframes',
    long_description="""
## excel_to_dataframe
C++ Library to convert Excel worksheets to Pandas (folder python) or Microsoft (folder csharp) dataframes (Windows only).

This software is in testing phase.

Feel free to test it out. If you want to share your experience, send me an email (nbittencourt@hotmail.com).

## Performance (python test only):
On an old processor (Intel Core i7-4510U 2.60 GHz, 4 cores) and with 8Gb RAM, the dll was between 12 and 25 times faster than Pandas.

## How it works:
Under construction.

## Installation (Python version only. Microsoft version comming soon):

### PyPI:
```Python
pip install excel-to-dataframe==0.2.54
```

### Anaconda/Miniconda:
#### Python 3.9
```Python
conda install -c nbittencourt excel_to_dataframe=0.2.54=py39_0
```

#### Python 3.10
```Python
conda install -c nbittencourt excel_to_dataframe=0.2.54=py310_0
```

#### Python 3.11
```Python
conda install -c nbittencourt excel_to_dataframe=0.2.54=py311_0
```


## Personal site:
http://www.nrbenergia.somee.com/  

or

https://nrbenergia.azurewebsites.net/

## More info:
https://www.linkedin.com/in/nelsonrossibittencourt/""",
    long_description_content_type="text/markdown",
    url='https://github.com/nelsonbittencourt/excel_to_dataframe',
    license='MIT',
    packages=['excel_to_dataframe'],
	include_package_data=True,
	package_data={'':['excel_to_df.dll','excel_to_df.so']},
    install_requires=['pandas','openpyxl'],
    classifiers=[
    # How mature is this project? Common values are
    #   3 - Alpha
    #   4 - Beta
    #   5 - Production/Stable
    'Development Status :: 4 - Beta',

    # Indicate who your project is intended for
    'Intended Audience :: Developers',
    'Intended Audience :: Education',
    'Intended Audience :: End Users/Desktop',
    
    # Pick your license as you wish (should match "license" above)
    'License :: OSI Approved :: MIT License',

    # Specify the Python versions you support here. In particular, ensure
    # that you indicate whether you support Python 2, Python 3 or both.
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
    
    # OS
    'Operating System :: Microsoft :: Windows',
    'Operating System :: Unix'
],
)