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

from yandex_cloud_ml_sdk import YCloudML

gpt_model = "yandexgpt-lite"
gpt_temperature = 0.5

is_debug = False


def validate_yandex_gpt(ai_key, ai_folder):
    if is_debug:
        print("Initializing YandexGPT client!")

    client = YCloudML(
        auth=ai_key,
        folder_id=ai_folder
    )

    try:
        model = client.models.completions(gpt_model)
        model = model.configure(temperature=gpt_temperature)

        result = model.run("Ping")

        # Check if the result is empty or unauthorized
        if not result:
            raise PermissionError("Unauthorized: Invalid API key or access denied.")
        else:
            if is_debug:
                print("Client initialized successfully!")
    except Exception as e:
        raise ValueError(f"Error: Failed to authenticate with YandexGPT API. Exception: {e}")


def translate_yandex_gpt(ai_key, ai_folder, prompt):
    if is_debug:
        print("Translating via Yandex GPT...")

    client = YCloudML(
        auth=ai_key,
        folder_id=ai_folder
    )

    try:
        model = client.models.completions(gpt_model)
        model = model.configure(temperature=gpt_temperature)

        result = model.run(
            f"You are a professional translator specialized in UI/UX localization.\n{prompt}"
        )

        completions = list(result)
        if not completions:
            raise ValueError("No translation response received.")

        return completions[0].text
    except Exception as e:
        if "401" in str(e) or "unauthorized" in str(e).lower():
            raise PermissionError("Unauthorized: Invalid API key or access denied.")
        else:
            raise RuntimeError(f"Translation failed: {e}")
