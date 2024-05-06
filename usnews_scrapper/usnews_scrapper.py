"""USNews-Scrapper
This script is built to collect informations about the best US universities from 
https://www.usnews.com/best-colleges. 

This script takes the url as input and generates output as either a (.xlsx),
(.csv) or (.html) file.

This file can also be imported as a module and contains the following
functions:
    * usnews_scrapper - returns the path of the output file
    * _main - the main function of the script
"""

import requests
import time
import json
import queue
from argparse import ArgumentParser
from urllib import parse
import os
import sys
import shutil
import datetime

import tablib
from tqdm import tqdm

from college import College


html_start = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    <link rel="stylesheet" href="table_data/styles.css">
    <script src="table_data/main.js" defer></script>
    <title>Document</title>
</head>
<body>
"""
html_end = """
</body>
</html>"""


class USNewsScrapper:
    def __init__(self):    
        self.__args = None
        self.__url = "https://www.usnews.com/best-colleges/rankings/national-universities?_sort=rank&_sortDirection=asc" 
        self.__temp_folder = "./temp"
        self.__data_tablib = None
        self.__called_as_module = False

    def __modifyparser(self, parser):
        default_format = "xlsx"
        default_pause_time = 2
        default_start_page = 1
        default_end_page = 10

        output_help = "The output file name without extension."
        format_help = "The format of the output file"
        pause_help = "The pause time between loading pages from usnews. Minimum pause time is 1 sec."
        from_help = "The page number from which the scrapper starts working."
        to_help = "The page number to which the scrapper works."

        parser.add_argument("outputfilename", help=output_help)
        parser.add_argument("-p", "--pause", help=pause_help, dest="pausetime",  type=int, default=default_pause_time)
        parser.add_argument("-f", "--format", help=format_help, dest="format", choices=["xlsx", "csv", "html"], default=default_format)
        parser.add_argument("-s", "--start", help=from_help, dest="startpage", type=int, default=default_start_page)
        parser.add_argument("-e", "--end", help=to_help, dest="endpage", type=int, default=default_end_page)

    def __get_parser_for_parsing(self):
        parser = ArgumentParser(description="Collects data from usnews and generates excel file")
        self.__modifyparser(parser)
        return parser

    def __parseargs_from_cmd(self):
        parser = self.__get_parser_for_parsing()
        args = parser.parse_args()
        return args

    def __parseargs_from_function_call(self, arguments):
        parser = self.__get_parser_for_parsing()
        args = parser.parse_args(arguments)
        return args

    def __extract_parameters_from_url(self, url):
        location_params = {}
        parse_results = parse.urlsplit(url)

        output_sheet_name = "Ranking"
        
        locations = parse_results.path.split("/")[2:]
        program = locations[0]
        if program != "search":
            location_params["program"] = program
            output_sheet_name = program
        
        try:
            specialty = locations[1][:locations[1].rfind("-")]
            location_params["specialty"] = specialty
            output_sheet_name = specialty
        except:
            pass
        
        location_params["_page"] = "dummy"
        self.__args["output_sheet_name"] = output_sheet_name.replace("-", " ").title()
        querie_params = dict(parse.parse_qsl(parse_results.query))    
        params = {**location_params, **querie_params}

        return params

    def __get_temp_file_name(self, page):
        return self.__temp_folder + "/" + str(page).zfill(3) + ".txt"

    def __create_initial_request_params(self):
        url = "https://www.usnews.com/best-colleges/api/search"
        params = self.__extract_parameters_from_url(self.__url)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        }

        return url, params, headers

    def __cleanup(self, delete_output=False):
        if os.path.isdir(self.__temp_folder):
            shutil.rmtree(self.__temp_folder)
        if delete_output and os.path.isfile(self.__args["outputfilename"]):
            os.remove(self.__args["outputfilename"])

    def __print_request_error(self, response):
        status_code = response.status_code
        url = response.url
        
        if self.__called_as_module == False:
            print("An error occured while processing the url :\n" + url)
            print("Status Code : " + str(status_code) + "\n\n")
        else:
            response.raise_for_status()

    def __get_initial_infos(self, url, params, headers):
        params["_page"] = "1"
        r = requests.get(url=url, params=params, headers=headers)

        if r.status_code != requests.codes.ok:
            self.__print_request_error(r)
            return None

        response_json = r.json()
        time.sleep(1)
        max_page = int(response_json["data"]["total_pages"])

        return max_page, datetime.date.today().year

    def __decide_start_and_end_page(self, max_page, start_page, end_page):
        end_page = min(max(1, end_page), max_page)
        start_page = max(1, start_page)

        if start_page > end_page:
            start_page = end_page = min(start_page, end_page)

        return (start_page, end_page)

    def __scrape_and_save_data(self, req_params):
        url, params, headers = req_params
        
        self.__cleanup(True)
        os.mkdir(self.__temp_folder)
        
        if self.__called_as_module == False:
            print("\nCollecting data from U.S.News...")
        sys.stdout.flush()

        for page in tqdm(range(self.__args["startpage"], self.__args["endpage"] + 1), disable=self.__called_as_module):
            params["_page"] = str(page)
            r = requests.get(url=url, params=params, headers=headers)

            if r.status_code != requests.codes.ok:
                self.__print_request_error(r)
                return
            
            with open(self.__get_temp_file_name(page), "w+") as f:
                response_json = r.json()
                json.dump(response_json, f)
            
            time.sleep(self.__args["pausetime"])

    def __get_column_headers(self):
        output_headers = ["Rank", "Name", "State", "Tuition", "Acc Rate", "SAT Range", "ACT Range", 
                          "Engineering", "Business", "CS", "Nursing"]
        return tuple(output_headers)

    def __append_to_data_tablib(self, school_datas):
        if self.__data_tablib == None:
            headers = self.__get_column_headers()
            self.__data_tablib = tablib.Dataset(title=self.__args["output_sheet_name"])
            self.__data_tablib.headers = headers

        for school_data in school_datas:
            g = tuple(College.getFromJSON(school_data))
            self.__data_tablib.append(g)

    def __print_to_outputfile(self):
        if self.__data_tablib == None:
            print("Data Tablib is None. Some error happened")
            sys.exit()

        filename = self.__args["outputfilename"] + "." + self.__args["format"]

        if self.__args["format"] == "xlsx":
            with open(filename, "wb+") as f:
                f.write(self.__data_tablib.export("xlsx"))
        elif self.__args["format"] == "csv":
            with open(filename, "w", newline="") as f:
                f.write(self.__data_tablib.csv)
        elif self.__args["format"] == "html":
            with open(filename, "w") as f:
                f.write(html_start)
                f.write(self.__data_tablib.html)
                f.write(html_end)

    def __parse_json_from_file(self):
        locked_q = queue.Queue()

        for filename in sorted(os.listdir(self.__temp_folder)):
            filename = os.path.join(self.__temp_folder, filename)
            if os.path.isfile(filename) == False:
                continue

            with open(filename, "r") as f:
                data = json.load(f) 
                school_datas = data["data"]["items"]
                self.__append_to_data_tablib(school_datas)
                if "lockedItems" in data["data"] and data["data"].get("lockedItems") != None: 
                    locked_q.put(data["data"]["lockedItems"])     
            
        while locked_q.empty() == False:
            self.__append_to_data_tablib(locked_q.get())

    def __convert_and_check_args(self, req_params):
        self.__args["startpage"] = int(self.__args["startpage"])
        self.__args["endpage"] = int(self.__args["endpage"])
        self.__args["pausetime"] = int(self.__args["pausetime"])
        
        self.__args["pausetime"] = min(max(self.__args["pausetime"], 1), 10)
        self.__args["startpage"] = max(1, self.__args["startpage"])
        self.__args["endpage"] = max(self.__args["startpage"], self.__args["endpage"])

        url, params, headers = req_params
        max_page, self.__args["year"] = self.__get_initial_infos(url, params, headers)
        self.__args["startpage"], self.__args["endpage"] = self.__decide_start_and_end_page(max_page, 
                                                                                            self.__args["startpage"], 
                                                                                            self.__args["endpage"])

        msg = "Collecting data from \"{}\" \nFrom page {} to page {} with pause time of {} sec."
        if self.__called_as_module == False:
            print(msg.format(self.__url, self.__args["startpage"], self.__args["endpage"], self.__args["pausetime"]))

    def __run_scrapping_and_saving(self):
        req_params = self.__create_initial_request_params()
        self.__convert_and_check_args(req_params)

        self.__scrape_and_save_data(req_params)

        self.__parse_json_from_file()
        self.__print_to_outputfile()

        self.__cleanup()

    def __create_argument_from_values(self, outputfilename, pausetime, format, startpage, endpage):
        arguments = []
        
        arguments.append(str(outputfilename))

        if pausetime is not None:
            arguments.append("-p")
            arguments.append(str(pausetime))

        if format is not None:
            arguments.append("-f")
            arguments.append(str(format))

        if startpage is not None:
            arguments.append("-s")
            arguments.append(str(startpage))

        if endpage is not None:
            arguments.append("-e")
            arguments.append(str(endpage))
        
        return arguments

    def __get_outfile_name_with_working_dir(self):
        return os.path.join(os.getcwd(), self.__args["outputfilename"])

    def usnews_scrapper_for_cmd(self):
        self.__args = vars(self.__parseargs_from_cmd())
        self.__run_scrapping_and_saving()

    def usnews_scrapper_for_function_call(self, outputfilename, pausetime, format, startpage, endpage):    
        arguments = self.__create_argument_from_values(outputfilename, pausetime, format, startpage, endpage)
        self.__called_as_module = True
        
        self.__args = vars(self.__parseargs_from_function_call(arguments))
        self.__run_scrapping_and_saving() 
        
        return self.__get_outfile_name_with_working_dir()
    

def usnews_scrapper(outputfilename:str, pausetime:int=None, format:str=None, startpage:int=None, endpage:int=None) -> str:
    """Collects data from usnews website and outputs a (.xlsx) or (.csv) file.

    Parameters
    ----------
    outputfilename : str
        The expected name of the output file name. The output
        file name will start with this string.
    pause_time : int, optional
        The time between two successive request calls.
    format : options : [xlsx, csv, html]
        The format of the produced file.
    startpage : int, optional
        The page number from which function will start to collect data.
    endpage : int, optional
        The page number upto which function will collect data.

    Returns
    -------
        The absolute path to the output file 
    """
    
    usnews_scrapper_obj = USNewsScrapper()
    return usnews_scrapper_obj.usnews_scrapper_for_function_call(outputfilename, pausetime, format, startpage, endpage)
    

def _main():
    usnews_scrapper_obj = USNewsScrapper()
    usnews_scrapper_obj.usnews_scrapper_for_cmd()

if __name__ == "__main__":
    _main()