#!/usr/bin/env python
# coding: utf-8


# automated version with user prompt
import os
import argparse
import yaml
import re
import subprocess
import os
from collections.abc import Iterable
import sys
from yamdgen.yaml_helpers_function import *
from yamdgen.md_helpers_function import *
                  
                            
def main_yaml():
    result,path = get_dbt_project_status()
    if result == "passed":
        print("running yaml generator using dbt_project.yml in {}/dbt_project.yml...........\n".format(path))
        parser = argparse.ArgumentParser(description='Check if the argument is a path or a list \n')
        parser.add_argument('input', type=str, help='Path or list of values \n')

        args = parser.parse_args()

        if os.path.exists(args.input):
            list_sql = get_sql_list(args.input)
            generate_yaml_for_models(list_sql,path)
          
        elif isinstance(eval(args.input), list):
            values = eval(args.input)
            generate_yaml_for_models(values,path)
                
        else:
            print(f"Check the argument is the expected format \n")

    else:
        print("Error: Please go into a dbt project as a dbt_project.yml file could not be found in the current directory. \n")


def main_md():
    result,path = get_dbt_project_status()
    if result == "passed":
        print("running md generator using this dbt project in {}...........\n".format(path))
        parser = argparse.ArgumentParser(description='Check if the argument is a path or a list \n')
        parser.add_argument('input', type=str, help='Path or list of values \n')

        args = parser.parse_args()

        if os.path.exists(args.input):
            list_sql = get_sql_list(args.input)
            generate_md_for_models(list_sql,path)
          
        elif isinstance(eval(args.input), list):
            values = eval(args.input)
            generate_md_for_models(values,path)
                
        else:
            print(f"Check the argument is the expected format \n")

    else:
        print("Error: Please go into a dbt project as a dbt_project.yml file could not be found in the current directory. \n")





if __name__ == "__main__":
    main_yaml()
    main_md()
                