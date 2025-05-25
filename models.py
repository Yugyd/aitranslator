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

import json

_is_debug = False


class Configuration:

    def __init__(self, config_data):
        self.app_description = config_data["config"].get("appDescription", "")
        self.source_language = config_data["config"].get("sourceLanguage", "")
        self.target_languages = config_data["config"].get("targetLanguages", [])
        self.exclude_translated = config_data["config"].get("excludeTranslated", False)

        self.ai_provider = config_data["config"].get("aiProvider", "")
        self.ai_key = config_data["config"].get("aiKey", "")
        self.ai_folder = config_data["config"].get("aiFolder", "")
        self.ai_model = config_data["config"].get("aiModel", "")

        self.exclude = config_data.get("exclude", [])

        self.validate()

    def validate(self):
        if not self.ai_provider or not self.ai_key:
            raise ValueError("Error: Missing required AI settings in configuration file.")
        elif not self.source_language or not self.target_languages:
            raise ValueError("Error: Missing required config settings in configuration file.")

        if _is_debug:
            print("Configuration file successfully parsed and validated.")

    def to_json(self):
        return json.dumps(self.__dict__, indent=4)


class ModuleConfiguration:

    def __init__(self, module_config):
        self.config_data = module_config.get("config", {})
        self.exclude = module_config.get("exclude", [])

        self.module_description = self.config_data.get("moduleDescription", "")
        self.exclude_translated = self.config_data.get("excludeTranslated", False)

        self.validate()

    def validate(self):
        if not self.module_description:
            raise ValueError("Error: Missing module description in configuration file.")

    def to_json(self):
        return json.dumps(self.config_data, indent=4)
