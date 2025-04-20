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
import xml.etree.ElementTree as ET
from xml.dom import minidom

from client import translate
from models import Configuration
import html

is_debug = False


def execute(prompt_path, configuration, execution_graph):
    print("Execute!")

    languages = get_languages(configuration)

    modules_language_data = []

    for module in execution_graph:
        words = get_words_from_strings_file(module)

        language_with_words = {}

        for language in languages:
            lang_dir_path = make_language_dir_if_not_exists(language, module)
            translated_words = translate_all_words_to_language(
                prompt_path,
                words,
                language,
                configuration,
                module["configuration"]
            )
            language_with_words[language] = translated_words
            write_words_to_strings_file(lang_dir_path, translated_words)

        modules_language_data.append((module, language_with_words))

    make_report(configuration, execution_graph, modules_language_data)


def get_words_from_strings_file(module):
    if is_debug:
        print("Get words from strings file!")

    strings_path = module["strings"]
    configuration = module.get("configuration")
    excluded_keys = set(configuration.exclude) if configuration and configuration.exclude else set()
    words = []

    try:
        tree = ET.parse(strings_path)
        root = tree.getroot()

        for string_element in root.findall("string"):
            key = string_element.attrib.get("name", "")
            if key in excluded_keys:
                continue

            value = string_element.text
            if value:
                cleaned_value = " ".join(value.split())
                words.append({"key": key, "value": cleaned_value})
        if is_debug:
            print(f"Collected {len(words)} string(s) from {strings_path}")
        return words

    except ET.ParseError as e:
        print(f"XML parse error in {strings_path}: {e}")
    except FileNotFoundError:
        print(f"File not found: {strings_path}")
    except Exception as e:
        print(f"Unexpected error reading {strings_path}: {e}")

    return []


def get_languages(global_config: Configuration):
    if is_debug:
        print("Get languages!")

    return global_config.target_languages


def make_language_dir_if_not_exists(language, module):
    if is_debug:
        print("Make language dir!")

    strings_path = module["strings"]
    res_dir = os.path.abspath(os.path.join(strings_path, "..", ".."))  # this gets to the `res` directory
    lang_dir_name = f"values-{language}"
    lang_dir_path = os.path.join(res_dir, lang_dir_name)

    if not os.path.exists(lang_dir_path):
        os.makedirs(lang_dir_path)
        if is_debug:
            print(f"Created directory: {lang_dir_path}")
    else:
        if is_debug:
            print(f"Directory already exists: {lang_dir_path}")

    return lang_dir_path


def translate_all_words_to_language(prompt_path, words, target_language, global_config, module_config):
    if is_debug:
        print("Translate all words to language!")

    module_description = module_config.module_description if module_config else ""

    translated_words = translate(
        prompt_path=prompt_path,
        global_config=global_config,
        module_description=module_description,
        target_language=target_language,
        words=words
    )

    if is_debug:
        print(f"Translated count {len(translated_words)} string(s)")

    for word in translated_words:
        if not word.get("key") or not word.get("value"):
            raise ValueError(f"Invalid translated word: {word}")

    return translated_words


def escape_android_string(value):
    if value is None:
        return ""

    # First, escape &, <, > with XML-safe sequences
    escaped = html.escape(value, quote=False)

    # Then handle Android-specific rules
    escaped = escaped.replace("'", "\\'")
    escaped = escaped.replace('"', '\\"')

    return escaped


def write_words_to_strings_file(lang_dir_path, words):
    if is_debug:
        print("Write words to strings file!")

    # Path to strings.xml
    strings_file_path = os.path.join(lang_dir_path, "strings.xml")

    # Build new XML structure
    resources = ET.Element("resources")
    resources.insert(0, ET.Comment("Generated Translator AI"))

    for word in words:
        string_element = ET.SubElement(resources, "string")
        string_element.set("name", word["key"])
        string_element.text = escape_android_string(word["value"])

    # Convert to pretty XML string
    rough_string = ET.tostring(resources, encoding="utf-8")
    parsed = minidom.parseString(rough_string)
    pretty_xml = parsed.toprettyxml(indent="    ", encoding="utf-8")

    # Write to file (overwrite existing or create new)
    with open(strings_file_path, "wb") as f:
        f.write(pretty_xml)

    # Ensure the file is closed properly
    if is_debug:
        print(f"Wrote {len(words)} translated strings to {strings_file_path}")


def make_report(configuration, execution_graph, modules_language_data):
    print("\n===== TRANSLATION REPORT =====\n")

    print("🔧 Configuration Used:")
    print(f"- App Description     : {configuration.app_description}")
    print(f"- Source Language     : {configuration.source_language}")
    print(f"- Target Languages    : {', '.join(configuration.target_languages)}")
    print(f"- Exclude Translated  : {configuration.exclude_translated}")
    print(f"- AI Provider         : {configuration.ai_provider}")
    print(f"- AI Folder           : {configuration.ai_folder}")
    print(f"- Excluded Keys       : {', '.join(configuration.exclude) if configuration.exclude else 'None'}")

    print()

    print(f"📦 Total Modules Processed: {len(execution_graph)}\n")

    total_translated_lines = 0
    for module, language_with_words in modules_language_data:
        print(f"📁 Module: {module['strings']}")
        for lang, words in language_with_words.items():
            translated_count = len(words)
            total_translated_lines += translated_count
            print(f"  🌐 Language: {lang} → {translated_count} lines translated")
        print()

    print("🧾 Summary:")
    print(f"- Total translated lines: {total_translated_lines}")
    print("\n✅ Translation completed.\n")
