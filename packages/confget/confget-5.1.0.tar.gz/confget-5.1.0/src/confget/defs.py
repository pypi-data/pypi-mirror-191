# Copyright (c) 2018 - 2023  Peter Pentchev <roam@ringlet.net>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.

"""Common definitions for the confget configuration parsing library."""

import dataclasses
import enum
import sys

from typing import Dict, List, Optional


class BackendType(str, enum.Enum):
    """The supported confget backends."""

    INI = "ini"
    INI_PYP = "ini-pyp"
    INI_REGEX = "ini-regex"

    def __str__(self) -> str:
        """Return a human-readable representation (the string itself)."""
        return self.value


VERSION_STRING = "5.1.0"
FEATURES = [
    ("BASE", VERSION_STRING),
    ("REGEX", "1.0"),
    (
        "REGEX_IMPL_PYTHON",
        f"{sys.version_info[0]}.{sys.version_info[1]}",
    ),
    ("INI_BACKEND", BackendType.INI_PYP),
    ("INI_PYP", "1.0"),
    ("INI_REGEX", "1.0"),
]

SectionData = Dict[str, str]
ConfigData = Dict[str, SectionData]


@dataclasses.dataclass
class Config:
    """Base class for the internal confget configuration."""

    varnames: List[str]
    filename: Optional[str] = None
    section: str = ""
    section_specified: bool = False
    encoding: str = ""
