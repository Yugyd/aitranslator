# Copyright 2025 Roman Likhachev
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import yaml
from models import ModuleConfiguration

_is_debug = False


def configure(project_dir):
    print("Configure!")

    all_strings, all_configurations = find_all_modules(project_dir)

    execution_graph = build_execution_graph(all_strings, all_configurations)

    return execution_graph


def find_all_modules(project_dir):
    if _is_debug:
        print("Find all modules!")

    all_strings = find_all_strings_files(project_dir)
    all_configurations = find_all_configuration_files(project_dir)

    return all_strings, all_configurations


def find_all_strings_files(project_dir):
    if _is_debug:
        print("Find all strings files!")

    strings_files = []
    for root, _, files in os.walk(project_dir):
        for file in files:
            if file == "strings.xml":
                values_dir = os.path.basename(root)

                # Only include 'values' directory (exclude 'values-xx' folders)
                if values_dir == "values":
                    strings_files.append(os.path.join(root, file))

    if _is_debug:
        print(f"Found {len(strings_files)} strings.xml files.")

    return strings_files


def find_all_configuration_files(project_dir):
    if _is_debug:
        print("Find all configuration files!")

    config_files = []
    for root, _, files in os.walk(project_dir):
        for file in files:
            if file == "translator-config.yml":
                config_files.append(os.path.join(root, file))

    if _is_debug:
        print(f"Found {len(config_files)} translator-config.yml files.")

    return config_files


def find_module_root(strings_file: str) -> str:
    current_dir = os.path.dirname(strings_file)

    while current_dir and not os.path.exists(os.path.join(current_dir, 'src')):
        current_dir = os.path.dirname(current_dir)

    return current_dir


def build_execution_graph(all_strings_files, all_configurations_files):
    if _is_debug:
        print("Building execution graph!")

    execution_graph = []

    for strings_file in all_strings_files:
        module_root = find_module_root(strings_file)

        matching_config_files = [
            config_file for config_file in all_configurations_files
            if os.path.dirname(config_file) == module_root
        ]

        if matching_config_files:
            config_file = matching_config_files[0]
            module_config_data = load_yaml(config_file)
            module_config = ModuleConfiguration(module_config_data)
        else:
            module_config = None

        execution_graph.append(
            {
                "module_path": module_root,
                "strings": strings_file,
                "configuration": module_config
            }
        )

    for entry in execution_graph:
        if _is_debug:
            print(f"Module: {entry['strings']}, Configuration: {entry['configuration']}, Path: {entry['module_path']}")

    return execution_graph


def load_yaml(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        try:
            return yaml.safe_load(file)
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing YAML file: {e}")
