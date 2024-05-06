=================
U.S.News-Scrapper
=================

U.S.News Scrapper is a Python library that collect data from the  usnews_ website and output those data in a file for offline usage. It then collects college data and outputs it in either .xlsx, .csv or .html format.
*Visit github_ page for detailed informations.*

Setup
=====
*Visit github_ page for detailed informations.*

    | $ pip install usnews_scrapper


Usage
=====
usage: python usnews_scrapper.py [-h] outputfilename [-s STARTPAGE] [-e ENDPAGE]  [-f {xlsx,csv,html}] [-p PAUSETIME] 

Collects data from usnews and generates either an excel, a csv or a html file

optional arguments:
-h, --help            		        Show this help message and exit.
-s STARTPAGE, --start STARTPAGE     The page number from which the scrapper starts working.
-e ENDPAGE, --end ENDPAGE     		The page number to which the scrapper works. 
-f FORMAT, --format FORMAT          The format of the output file.  
-p PAUSETIME, --pause PAUSETIME     The pause time between loading pages from usnews.	        


Examples
========

To produce an excel file that ranges between the pages 1 and 2 with a pausetime of 2 seconds, enter this command -

    | $ cd USNews-Scrapper
    | $ python usnews_scrapper.py file_name_ --start 1 --end 2 --format xlsx --pause 2

The output file will be saved in `usnews_scrapper` directory under the name of file_name_*.xlsx

Authors
=======

* *Joy Ghosh* - www.ijoyghosh.com_

.. _usnews: https://www.usnews.com/best-colleges
.. _pip: https://pip.pypa.io/en/stable/
.. _www.ijoyghosh.com : https://www.ijoyghosh.com
.. _github : https://github.com/OvroAbir/USNews-Scrapper
