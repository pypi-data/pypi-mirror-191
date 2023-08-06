import logging

# from typing import List, Optional, Dict, Any

import click
import click_log
import pandas as pd

import yaml

from glom import glom, assign
import glom.core as gc

from linkml_runtime.utils.schemaview import SchemaView

logger = logging.getLogger(__name__)
click_log.basic_config(logger)


@click.command()
@click_log.simple_verbosity_option(logger)
@click.option("--yaml_input", type=click.Path(exists=True), required=True)
@click.option("--modifications_config_tsv", type=click.Path(exists=True), required=True)
@click.option("--validation_config_tsv", type=click.Path(exists=True), required=True)
@click.option("--yaml_output", type=click.Path(), required=True)
def modifications_and_validation(yaml_input: str, modifications_config_tsv: str, validation_config_tsv: str,
                                 yaml_output: str):
    """
    :param yaml_input:
    :param config_tsv:
    :param yaml_output:
    :return:
    """

    # todo be defensive
    # parameterize?

    meta_view = SchemaView("https://w3id.org/linkml/meta")

    with open(yaml_input, 'r') as stream:
        try:
            schema_dict = yaml.safe_load(stream)
        except yaml.YAMLError as e:
            logger.warning(e)

    mod_rule_frame = pd.read_csv(modifications_config_tsv, sep="\t")
    mod_rule_frame['class'] = mod_rule_frame['class'].str.split("|")
    mod_rule_frame = mod_rule_frame.explode('class')

    mod_rule_lod = mod_rule_frame.to_dict(orient='records')

    # todo break out overwrites first
    for i in mod_rule_lod:

        pre_base_spec = f"classes.{i['class']}"
        pre_base_dict = glom(schema_dict, pre_base_spec)
        if "slot_usage" not in pre_base_dict:
            assign(obj=pre_base_dict, path="slot_usage", val={})

        with_usage_spec = f"classes.{i['class']}.slot_usage"
        with_usage_dict = glom(schema_dict, with_usage_spec)
        if i['slot'] not in with_usage_dict:
            assign(obj=with_usage_dict, path=i['slot'], val={})

        base_path = f"classes.{i['class']}.slot_usage.{i['slot']}"
        try:
            logger.info(f"{i['slot']} {i['action']} {i['target']} {i['value']}")
            slot_usage_extract = glom(schema_dict, base_path)

            if i['action'] == "add_attribute" and i['target'] != "" and i['target'] is not None:

                # todo abort if slot is not multivalued
                #   alert use that value is being split on pipes

                cv_path = i['target']

                values_list = i['value'].split("|")
                values_list = [x.strip() for x in values_list]

                target_already_present = cv_path in slot_usage_extract
                if target_already_present:
                    current_value = glom(slot_usage_extract, cv_path)
                    target_is_list = type(current_value) == list
                    if target_is_list:
                        augmented_list = current_value + values_list
                        assign(obj=slot_usage_extract, path=i['target'], val=augmented_list)
                    else:
                        augmented_list = [current_value] + values_list
                        assign(obj=slot_usage_extract, path=i['target'], val=augmented_list)
                else:
                    assign(obj=slot_usage_extract, path=i['target'], val=values_list)


            elif i['action'] == "add_example" and i['target'] == "examples":
                cv_path = i['target']

                examples_list = i['value'].split("|")
                examples_list = [x.strip() for x in examples_list]
                assembled_list = []
                for example_item in examples_list:
                    assembled_list.append({'value': example_item})

                target_already_present = cv_path in slot_usage_extract
                if target_already_present:
                    current_value = glom(slot_usage_extract, cv_path)
                    target_is_list = type(current_value) == list
                    if target_is_list:
                        augmented_list = current_value + assembled_list
                        assign(obj=slot_usage_extract, path=i['target'], val=augmented_list)
                    else:
                        augmented_list = [current_value] + assembled_list
                        assign(obj=slot_usage_extract, path=i['target'], val=augmented_list)
                else:
                    assign(obj=slot_usage_extract, path=i['target'], val=assembled_list)


            elif i['action'] == "overwrite_examples" and i['target'] == "examples":
                examples_list = i['value'].split("|")
                examples_list = [x.strip() for x in examples_list]
                assembled_list = []
                for example_item in examples_list:
                    assembled_list.append({'value': example_item})
                assign(obj=slot_usage_extract, path=i['target'], val=assembled_list)

            elif i['action'] == "replace_annotation" and i['target'] != "" and i['target'] is not None:
                if "annotations" in slot_usage_extract:
                    update_path = f"annotations.{i['target']}"
                    assign(obj=slot_usage_extract, path=update_path, val=i['value'])
                else:
                    update_path = f"annotations"
                    assign(obj=slot_usage_extract, path=update_path, val={i['target']: i['value']})

            elif i['action'] == "replace_attribute" and i['target'] != "" and i['target'] is not None:
                update_path = i['target']
                fiddled_value = i['value']
                from_meta = meta_view.get_slot(i['target'])
                fm_range = from_meta.range
                if fm_range == "boolean":
                    fiddled_value = bool(i['value'])
                assign(obj=slot_usage_extract, path=update_path, val=fiddled_value)

            # todo refactor

        except gc.PathAccessError as e:
            logger.warning(e)

    # ============== apply validation rules ============== #
    # ==================================================== #

    # fetch validation_converter sheet as pd df
    validation_rules_df = pd.read_csv(validation_config_tsv, sep="\t", header=0)

    # loop through all induced slots associated with all classes from
    # from the schema_dict and modify slots in place
    for class_name, class_defn in schema_dict["classes"].items():

        # check if the slot_usage key exists in each class definition
        if "slot_usage" in class_defn:

            # loop over slot_usage items from each of the classes
            for _, slot_defn in schema_dict["classes"][class_name][
                "slot_usage"
            ].items():

                # when slot range in filtered list from validation_converter
                if "range" in slot_defn and (
                        slot_defn["range"]
                        in validation_rules_df[
                            validation_rules_df["to_type"] == "DH pattern regex"
                        ]["from_val"].to_list()
                ):
                    slot_defn["pattern"] = validation_rules_df[
                        validation_rules_df["from_val"] == slot_defn["range"]
                        ]["to_val"].to_list()[0]

                # when slot string_serialization in filtered list
                # from validation_converter
                if "string_serialization" in slot_defn and (
                        slot_defn["string_serialization"]
                        in validation_rules_df[
                            validation_rules_df["to_type"] == "DH pattern regex"
                        ]["from_val"].to_list()
                ):
                    slot_defn["pattern"] = validation_rules_df[
                        validation_rules_df["from_val"]
                        == slot_defn["string_serialization"]
                        ]["to_val"].to_list()[0]

    # ==================================================== #

    with open(yaml_output, 'w') as outfile:
        yaml.dump(schema_dict, outfile, default_flow_style=False, sort_keys=False)


if __name__ == '__main__':
    modifications_and_validation()
