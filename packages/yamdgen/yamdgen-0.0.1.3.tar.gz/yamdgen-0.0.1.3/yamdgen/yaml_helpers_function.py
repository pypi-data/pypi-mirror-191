import os
import yaml
import re
import subprocess
import os
from collections.abc import Iterable
import sys


def get_dbt_project_status():
    """
    This function uses the dbt debug command and returns the status of the dbt project and its location.
    
    :return: A tuple with the first element being either 'passed' the current directory has dbt_project.yml, 
            'failed' or 'unknown', and the second element being the path to the dbt project.
    """
    result = subprocess.run(['dbt', 'debug'], capture_output=True, text=True)
    output = result.stdout
    if 'ERROR not found' in output:
        return ('failed', None)
    elif 'All checks passed' in output:
        lines = output.split("\n")
        for line in lines:
            if "Using dbt_project.yml file at" in line:
                path = line.split("dbt_project.yml file at")[1].strip()
                path = os.path.dirname(path)
                if os.path.exists(path):
                    return ('passed', path)
        return ('passed', None)
    else:
        return ('unknown', None)


def find_file_path(model_name,path):
    """
    This function returns the path to the directory where a model with the provided name in the argument is stored.
    
    :param model_name: The name of the model to search for.
    :param path: The root directory to start the search from.
    :return: The path to the directory where the model is stored or None if the model is not found.
    """
    models_dir = os.path.join(path, "models")
    for root, dirs, files in os.walk(models_dir):
        for file in files:
            if file == f"{model_name}.sql" or file == model_name:
                return root
    return None


def check_sql_config(file_path):
    """
    This function checks if the dbt model configuration of a given model is set to materialize as ephemeral.
    
    :param file_path: The path to the dbt model to check.
    :return: True if the configuration specifies an ephemeral materialization, False otherwise.
    """
    with open(file_path, 'r') as sql_file:
        file_content = sql_file.read()
        match = re.search(r"config\s*\((.*)\)", file_content)
        if match:
            config_args = match.group(1)
            match = re.search(r"materialized\s*=\s*'(.*?)'", config_args)
            if match:
                materialized_arg = match.group(1)
                if materialized_arg == "ephemeral":
                    return True
    return False


def find_file(model_name,path):
    """
    This function searches for a model with a given name in the models directory of a specified path.
    
    :param model_name: The name of the model to search for.
    :param path: The path to search in.
    :return: The path to the model if it is found, or None if it is not found.
    """
    models_dir = os.path.join(path, "models")
    for root, dirs, files in os.walk(models_dir):
        for file in files:
            if file == f"{model_name}.sql" or file == model_name:
                return os.path.join(root, file)
    return None



def yamlgen(model_name, path, version=2):
    """
    This function generates a YAML file for the provided model name, and stores it in the specified path.

    :param model_name (str): Name of the model for which YAML file is to be generated.
    :param path (str): Path where the YAML file will be stored.
    :param version (int, optional): Version of the YAML file. Default is 2.

    Returns:
    None: The function only generates the YAML file and stores it in the specified path, no return value.
    """
    model_name = model_name.split('.', 1)[0]
    model_path = find_file(model_name,path)
    file_path = find_file_path(model_name,path)
    mod_name = {"model_names": [model_name]}
    if not check_sql_config(model_path):
        cmd = "dbt run-operation generate_model_yaml --args '{}'".format(mod_name)
        output = subprocess.check_output(cmd, cwd='.', shell=True)
        output = output.decode("utf-8")
        ver_details = 'version: {}\n'.format(version)
        mod_details = output.split('version: 2')[1]
        data = yaml.load(mod_details, Loader=yaml.FullLoader)
        if not data['models'][0]['columns']:
            print(f"Whoops! {model_name} wasn't created.....try running the model using dbt run and then retry yamlgen \n")
        else:
            file_path = '{}/{}.yml'.format(file_path, model_name)
            with open(file_path, "w") as text_file:
                text_file.write(ver_details + mod_details)
            print("{}.yml has been created in {} \n".format(model_name, file_path))
    else:
        print("{} is ephemeral, skipping...".format(model_name))
        pass






def generate_yaml_for_models(model_names,path, version=2):
    """
    This function generates yaml files for a list of models provided. Using the yamlgen function.

    :param model_names (list): A list of strings that contain the name of each model.
    :param path (str): The path of the directory where the models and their yaml files will be stored.
    :param version (int, optional): The version of the yaml file, by default 2.

    Returns:
    None: This function generates yaml files and doesn't return anything.
    """
    for model_name in model_names:
        yamlgen(model_name,path, version)


def get_sql_list(path):
    """
    Get a list of all .sql files in the provided path.

    :param path: (str) Path to where SQL files are stored.
    :return: (list) List of all .sql files in the path.
    """
    list_sql = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".sql"):
                list_sql.append(file)
                
    return list_sql
                                  
