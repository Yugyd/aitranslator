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

from openai import OpenAI

default_ai_model = "gpt-4.1-mini"
gpt_temperature = 0.7
_is_debug = False


def validate_openai_gpt(ai_key, ai_model):
    if _is_debug:
        print("Initializing OpenAI client!")

    client = OpenAI(api_key=ai_key)

    try:
        if ai_model is None or ai_model == "":
            ai_model = default_ai_model

        response = client.chat.completions.create(
            model=ai_model,
            temperature=gpt_temperature,
            messages=[{"role": "user", "content": "Ping"}]
        )

        # Check if the result is empty or unauthorized
        if not response.choices:
            raise PermissionError("Unauthorized: Invalid API key or access denied.")
        else:
            if _is_debug:
                print("Client initialized successfully!")
    except Exception as e:
        raise ValueError(f"Error: Failed to authenticate with OpenAI API. Exception: {e}")


def translate_openai_gpt(ai_key, ai_model, prompt):
    if _is_debug:
        print("Translating via OpenAI GPT...")

    client = OpenAI(api_key=ai_key)

    try:
        if ai_model is None or ai_model == "":
            ai_model = default_ai_model

        response = client.chat.completions.create(
            model=ai_model,
            temperature=gpt_temperature,
            messages=[
                {"role": "developer",
                 "content": "You are a professional translator specialized in UI/UX localization."},
                {"role": "user", "content": prompt}
            ]
        )

        if not response.choices:
            raise ValueError("No translation response received.")

        return response.choices[0].message.content
    except Exception as e:
        if "401" in str(e) or "unauthorized" in str(e).lower():
            raise PermissionError("Unauthorized: Invalid API key or access denied.")
        else:
            raise RuntimeError(f"Translation failed: {e}")
