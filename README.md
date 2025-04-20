AI Translator
=============

Translates string resources in Android applications. Uses AI API to translate string resources into selected languages
of the world.

> 🛠️ **The project is in active development.**
> At the moment only Android projects.

# Applications using AI Translator

[Quiz-Platform](https://github.com/Yugyd/quiz-platform/)

# Stack

Coming soon

# Debug

- Make a replacement in the files `is_debug = True` [Temporary solution]

# Run

### Step 1: Add Configuration File to Android Project

- Add the `default-translator-config.yml` file to the root of your Android project.
- Configure the values in the configuration file. [Configuration example](assets/default-translator-config.yml)
    - `{config}` - basic configuration
        - `{appDescription}` - application description
        - `{sourceLanguage}` - source language
        - `{targetLanguages}` - target language
        - `{aiProvider}` - AI provider
        - `{aiKey}` - API key for AI
        - `{aiFolder}` - project ID in the cloud for AI
        - `{excludeTranslated}` - exclude already translated strings
    - `{exclude}` - exclude from translation

### Step 2: Add file with prompt (optional)

- Add the file `default-translator-prompt.txt` to the root of your Android project.
- Required arguments in the prompt:
    - `{source_lang_full}` - original language
    - `{target_lang_full}` - translation language
    - `{app_description}` - application description
    - `{module_description}` - module or screen description
    - `{words_json}` - Example of JSON response with translated words

### Step 3: Add configuration file to modules (optional)

- Add the `translator-config.yml` file to the root of the module.
- Configure the values in the configuration file. [Configuration example](assets/translator-config.yml)
    - `{config}` - base configuration
        - `{moduleDescription}` - module or screen description
        - `{excludeTranslated}` - exclude already translated strings
    - `{exclude}` - exclude from translation

### Step 4: Run script

- `python3 aitranslator.py --project_dir=<path_to_project>`

# License

```
   Copyright 2025 Roman Likhachev

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
```
