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
from ai_client import validate_ai, translate_ai
from models import Configuration
import json
import pycountry
import os

_is_debug = False


def validate(config: Configuration):
    if _is_debug:
        print("Validate!")

    validate_ai(
        ai_provider=config.ai_provider,
        ai_key=config.ai_key,
        ai_folder=config.ai_folder,
        ai_model=config.ai_model
    )


def translate(prompt_path, global_config, module_description, target_language, words):
    if _is_debug:
        print("Translate!")

    prompt = __generate_prompt__(
        prompt_path=prompt_path,
        app_description=global_config.app_description,
        module_description=module_description,
        source_language=global_config.source_language,
        target_language=target_language,
        words=words
    )

    result = translate_ai(
        ai_provider=global_config.ai_provider,
        ai_key=global_config.ai_key,
        ai_folder=global_config.ai_folder,
        ai_model=global_config.ai_model,
        prompt=prompt
    )

    return parse_(result)


def parse_(response_text):
    if _is_debug:
        print(f"Parsing GPT response: {response_text}")

    try:
        json_start = response_text.find('[')
        json_end = response_text.rfind(']') + 1
        json_str = response_text[json_start:json_end]

        return json.loads(json_str)
    except Exception as e:
        raise ValueError(f"Failed to parse response: {e}\nOriginal response: {response_text}")


DEFAULT_PROMPT_TEMPLATE = """
You are an assistant that translates Android string resources from one language to another. 
Translate the following list of UI strings from {source_lang_full} to {target_lang_full}.

Project description: {app_description}
Module (screen) description: {module_description}

Each string is a key-value pair. Return a JSON array where each item contains:
- "key": the original key
- "value": the translated text

Example response:
[
  {{ "key": "title_hello", "value": "Hola" }},
  ...
]

Here is the list to translate:
{words_json}
"""


def load_prompt_template(prompt_path):
    if os.path.exists(prompt_path):
        with open(prompt_path, "r", encoding="utf-8") as f:
            return f.read()

    return DEFAULT_PROMPT_TEMPLATE


def __generate_prompt__(prompt_path, app_description, module_description, source_language, target_language, words):
    def get_language_name(code):
        try:
            return pycountry.languages.get(alpha_2=code).name
        except:
            return code

    source_lang_full = get_language_name(source_language)
    target_lang_full = get_language_name(target_language)

    template = load_prompt_template(prompt_path=prompt_path)
    prompt = template.format(
        app_description=app_description,
        module_description=module_description,
        source_lang_full=source_lang_full,
        target_lang_full=target_lang_full,
        words_json=json.dumps(words, indent=2)
    )
    return prompt.strip()
