# yamdgen(Alpha Version)
A Yaml and Markdown generator, a wrapper built on [dbt Codegen generate_model_yaml](https://hub.getdbt.com/dbt-labs/codegen/latest/). This simple library is for automatically generating the yaml and md files needed for dbt models rather than having to copy from the cli, this package would generate the yaml and markdown in the respective directory of the model provided. See usage below.

# Requirements

- Ensure you have included the codegen package in your packages.yml file as seen [here](https://hub.getdbt.com/dbt-labs/codegen/latest/):

```
packages:
  - package: dbt-labs/codegen
    version: xx.xx.xx
```
- Run dbt deps to install the package.
- Ensure you are in your dbt project folder, as you would when you want to run any dbt command.
- When using **yamlgen** ensure you have ran the dbt model you want to generate the yaml for at least once.

## YAMLGEN 

**Usage for list of models**

```
# run the command below in your cli 

yamlgen "['model_a','model_b','model_c']"

```

**Usage for a directory**

```
# run the command below in your cli (No quotes)

yamlgen fullpath/model_folder

```


## MDGEN 

**Usage for list of models**

```
# run the command below in your cli 

mdgen "['model_a','model_b','model_c']"

```

**Usage for a directory**

```
# run the command below in your cli (No quotes)

mdgen fullpath/model_folder

```





# **Important information !!!!**

1. **As this is work in progress it is advisebale to use this when you dont have a yaml and md file yet as this will  overwrite your yaml and md files in your folder.**


