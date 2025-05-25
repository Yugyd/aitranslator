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

from enum import Enum
from chat_gpt import validate_openai_gpt, translate_openai_gpt
from yandex_gpt import validate_yandex_gpt, translate_yandex_gpt


class AIService(Enum):
    YANDEX = "yandex"
    OPENAI = "openai"


_is_debug = False


def validate_ai(ai_provider, ai_key, ai_folder, ai_model):
    service = get_ai_service(ai_provider)

    if service == AIService.YANDEX:
        validate_yandex_gpt(ai_key, ai_folder, ai_model)
    elif service == AIService.OPENAI:
        validate_openai_gpt(ai_key, ai_model)
    else:
        raise ValueError(f"Unknown AI service: {service}")


def translate_ai(ai_provider, ai_key, ai_folder, ai_model, prompt):
    service = get_ai_service(ai_provider)

    if service == AIService.YANDEX:
        if not ai_folder:
            raise ValueError("Folder ID is required for YandexGPT")
        return translate_yandex_gpt(ai_key, ai_folder, ai_model, prompt)
    elif service == AIService.OPENAI:
        return translate_openai_gpt(ai_key, ai_model, prompt)
    else:
        raise ValueError(f"Unknown AI service: {service}")


def get_ai_service(ai_provider):
    ai_provider = ai_provider.lower()

    if ai_provider == "yandex":
        return AIService.YANDEX
    elif ai_provider == "openai":
        return AIService.OPENAI
    else:
        raise ValueError("Error: Unsupported AI provider.")
