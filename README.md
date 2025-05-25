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

- Make a replacement in the files `_is_debug = True` [Temporary solution]

# Configure for Android

### Step 1: Add Configuration File to Android Project

- Add the `default-translator-config.yml` file to the root of your Android project.
- Configure the values in the configuration file. [Configuration example](assets/default-translator-config.yml)
    - `{config}` - basic configuration
        - `{appDescription}` - application description. String with the application description.
            - Example: `Quiz Platform is a platform for creating and playing quizzes.`
        - `{sourceLanguage}` - source language. String with the language code.
            - Example: `en` for English, etc.
        - `{targetLanguages}` - target language. Array of languages to translate into.
            - Example: `["en", "ru", "fr"]`
        - `{aiProvider}` - AI provider. Available options:
            - `openai` - OpenAI
            - `yandex` - Yandex GPT
        - `{aiKey}` - API key for AI. String with the API key.
            - Example: `sk-...` for OpenAI, `AQAAAA...` for Yandex GPT.
        - `{aiFolder}` - project ID in the cloud for AI. Only for Yandex GPT. String with the project ID.
            - Example: `b1g2...` for Yandex GPT.
        - `{aiModel}` - AI model. Available options:
            - `gpt-4.1-mini` - OpenAI GPT-4.1-Mini, etc. Default is `gpt-4.1-mini`.
            - `yandexgpt-lite` - Latest Yandex GPT, etc. Default is `yandexgpt-lite`.
        - `{excludeTranslated}` - exclude already translated strings. Boolean value.
    - `{exclude}` - exclude from translation. Array of strings to exclude from translation.
        - Example: `["app_name", "app_description"]`

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
    - `{config}` - base configuration for the module
        - `{moduleDescription}` - module or screen description. String with the module description.
            - Example: `Correct screen for the quiz platform.`
        - `{excludeTranslated}` - exclude already translated strings. Boolean value.
    - `{exclude}` - exclude from translation. Array of strings to exclude from translation.
        - Example: `["app_name", "app_description"]`

### Step 4: Run script

- `python3 aitranslator.py --project_dir=<path_to_project>`

# Configure for iOS

Coming soon

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
