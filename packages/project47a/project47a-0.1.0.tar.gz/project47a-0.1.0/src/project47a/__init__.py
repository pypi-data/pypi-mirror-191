# Copyright 2023 Henryk Plötz
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import random
from typing import Literal, Optional, Callable, Protocol

from . import data

__version__ = "0.1.0"


class Generator(Protocol):
    def __call__(self, rng: Optional[random.Random] = None) -> str:
        ...


def get_generator(lang: Literal["de"]) -> Generator:
    if lang == "de":
        return data.de.generate_random
    raise KeyError("Language not supported")
