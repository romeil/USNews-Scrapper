=================
U.S.News-Scrapper
=================

U.S.News Scrapper is a Python library that collect data from the website of usnews_ and output those data in a file for offline usage. Till now, it is only capable of collecting graduate schools data and output it in .xls format. After generating the .xls file, it will be opened by default excel file opener.

Setup
=====

First clone the repository. Then go to the repository and install the required packages using pip_

    | $ git clone https://github.com/OvroAbir/USNews-Scrapper.git
    | $ cd USNews-Scrapper
    | $ pip install -r requirements.txt


Usage
=====
usage: python main.py [-h] -u URL [-o OUTPUTFILENAME] [-p PAUSETIME] [--from STARTPAGE] [--to ENDPAGE]

Collects data from usnews and generates excel file

optional arguments:
-h, --help            		        Show this help message and exit
-u URL, --url URL     		        The usnews address to collect data from. Put the URL within qoutes i.e. " or ' .
-o OUTPUTFILENAME     		        The output file name without extension.
-p PAUSETIME, --pause PAUSETIME             The pause time between loading pages from usnews.
--from STARTPAGE      		        The page number from which the scrapper starts working.
--to ENDPAGE          		        The page number to which the scrapper works.


Examples
========

Copy the address of the page from usnews website and in the Command Prompt and enter this command -

    | $ cd USNews-Scrapper
    | $ python main.py --url="https://www.usnews.com/best-graduate-schools/top-science-schools/computer-science-rankings" -o file_name -p 2 --from=2 --to=5 

The output file will be saved in current directory under the name of file_name_*.xls 

Authors
=======

* *Joy Ghosh* - www.ijoyghosh.com_

.. _usnews: https://www.usnews.com/best-graduate-schools
.. _pip: https://pip.pypa.io/en/stable/
.. _www.ijoyghosh.com : https://www.ijoyghosh.com