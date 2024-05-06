# U.S.News-Scrapper

U.S.News Scrapper is a Python library that collects data from the website of [usnews.com](https://www.usnews.com/best-colleges) and output those data in a file for offline usage. It collects college data and then outputs it in either `.xlsx`, `.csv` or `.html` format.

## Setup
Make sure that [Python 3](https://www.python.org/downloads) is already installed in your system.
### Using pip
```bash
$ pip install usnews-scrapper
```
alternatively you can install by [Using source](#using-source)

### Using source
First clone the repository. Then go to the repository and install the required packages using [pip](https://pip.pypa.io/en/stable/)
```bash
$ git clone https://github.com/OvroAbir/USNews-Scrapper.git
$ cd USNews-Scrapper
$ pip install -r requirements.txt
```
Then it can be used via command line. See [Command line example](command-line-example)

## Usage

### Command line usage
```
python -m usnews_scrapper [-h] outputfilename [-s STARTPAGE] [-e ENDPAGE]  [-f {xlsx,csv,html}] [-p PAUSETIME]
```
Collects data from usnews and generates either an excel, csv or html file.

Necessary Arguments:
```
OUTPUTFILENAME     		                The output file name without extension.
```
Optional Arguments:
```
-h, --help            		            Show this help message and exit.
-s STARTPAGE, --start STARTPAGE         The page number from which the scrapper starts working.  		        
-e ENDPAGE, --end ENDPAGE               The page number to which the scrapper works.
-f FORMAT, --format FORMAT              The format of the output file.
-p PAUSETIME, --pause PAUSETIME         The pause time between loading pages from usnews.	        
```

### Module usage
`usnews_scrapper.unsc()` takes the `filename` as a string. The other arguments are optional. This function will return absolute path to the output file.

```python
from usnews_scrapper import unsc
unsc(outputfilename:str, pausetime:int, format:str, startpage:int, endpage:int) -> str
```
See [Module example](#module-example) for examples.

## Examples

### Command line example
Enter this command -

```bash
$ python -m usnews_scrapper file_name --start 1 --end 2 --format xlsx --pause 2
```

If you want to run from the source, then enter this command instead.

```bash
$ cd USNews-Scrapper/usnews_scrapper/
$ python usnews_scrapper.py file_name --start 1 --end 2 --format xlsx --pause 2
```
In both cases, the output file will be saved in `usnews_scrapper` directory under the name of `file_name_*.xlsx`. 

### Module example

```python
>>> from usnews_scrapper import unsc
>>> output_file = unsc(outputfilename="file_name", startpage=1, endpage=2, format="xlsx", pausetime=2)
```
The output_file will contain the absolute path to the output file.

## Authors

* **Joy Ghosh** - [www.ijoyghosh.com](https://www.ijoyghosh.com)
