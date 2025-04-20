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

import argparse
import os
import sys

from init import init
from configure import configure
from execute import execute

is_debug = False


def main(project_dir):
    if not os.path.exists(project_dir):
        print(f"❌ Error: Provided project directory does not exist: {project_dir}")
        sys.exit(1)

    configuration, prompt_path = init(project_dir=project_dir)

    execution_graph = configure(project_dir=project_dir)

    execute(prompt_path=prompt_path, configuration=configuration, execution_graph=execution_graph)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="📦 Android Strings Translator - Translate Android string resources into multiple languages."
    )
    parser.add_argument(
        "--project_dir",
        type=str,
        help="Path to the root of the Android project",
        required=False
    )

    args = parser.parse_args()

    main(args.project_dir)
