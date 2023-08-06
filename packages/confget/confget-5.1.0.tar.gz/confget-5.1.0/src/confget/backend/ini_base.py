# Copyright (c) 2018 - 2022  Peter Pentchev <roam@ringlet.net>
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

"""A base class for confget backends for reading INI-style files."""

import abc
import locale
import sys

from typing import IO

from .. import defs

from . import abstract


class INIBackendBase(abstract.Backend, metaclass=abc.ABCMeta):
    """Parse INI-style configuration files."""

    STDIN_NAME = "-"

    encoding: str
    parsed: defs.ConfigData

    def __init__(self, cfg: defs.Config) -> None:
        super().__init__(cfg)

        if self._cfg.filename is None:
            raise ValueError("No config filename specified")

        encoding = self._cfg.encoding if self._cfg.encoding else locale.nl_langinfo(locale.CODESET)
        assert encoding

        self.encoding = encoding
        self.parsed = {}

    def open_file(self) -> IO[str]:
        """Open the requested file or input stream."""
        assert self._cfg.filename is not None
        if self._cfg.filename == self.STDIN_NAME:
            return open(sys.stdin.fileno(), encoding=self.encoding, closefd=False)

        return open(self._cfg.filename, encoding=self.encoding, closefd=True)

    def get_dict(self) -> defs.ConfigData:
        return {item[0]: dict(item[1]) for item in self.parsed.items()}
