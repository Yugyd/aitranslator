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

from client import validate
from models import Configuration

is_debug = False


def init(project_dir):
    print("Init!")

    file = find_configuration_file(project_dir)

    prompt_path = find_prompt_file(project_dir)

    config = parse_configuration_file(file)

    init_client(config)

    return config, prompt_path


def find_configuration_file(project_dir):
    if is_debug:
        print("Find configuration file!")

    config_filename = "default-translator-config.yml"
    config_path = os.path.join(project_dir, config_filename)

    if os.path.exists(config_path):
        if is_debug:
            print(f"Configuration file found: {config_path}")

        return config_path
    else:
        raise FileNotFoundError(f"Error: Configuration file '{config_filename}' not found in project root.")


def find_prompt_file(project_dir):
    if is_debug:
        print("Find prompt file!")

    prompt_filename = "default-translator-prompt.txt"
    prompt_path = os.path.join(project_dir, prompt_filename)

    if os.path.exists(prompt_path):
        if is_debug:
            print(f"Prompt file found: {prompt_path}")

        return prompt_path
    else:
        raise FileNotFoundError(f"Error: Prompt file '{prompt_path}' not found in project root.")


def parse_configuration_file(configuration_file):
    if is_debug:
        print("Parse configuration file!")

    if not os.path.exists(configuration_file):
        raise FileNotFoundError(f"Error: Configuration file '{configuration_file}' not found.")

    with open(configuration_file, 'r', encoding='utf-8') as file:
        try:
            config_data = yaml.safe_load(file)
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing YAML file: {e}")

    config = Configuration(config_data)

    if is_debug:
        print(config.to_json())

    return config


def init_client(configuration_config):
    if is_debug:
        print("Init client!")

    validate(configuration_config)
