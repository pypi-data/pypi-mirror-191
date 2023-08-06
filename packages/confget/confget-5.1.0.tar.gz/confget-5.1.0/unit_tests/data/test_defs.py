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

"""Class definitions for the confget test suite."""

# This is a test suite. We know what we are checking for.
# pylint: disable=magic-value-comparison

import abc
import dataclasses
import os
import shlex

from typing import Any, Dict, Iterable, List, NamedTuple, Optional, Type

from confget import backend as cbackend
from confget import defs as cdefs
from confget import format as cformat


class CmdOpt(NamedTuple):
    """Does a command-line option require an argument?"""

    option: str
    has_argument: bool


CMDLINE_OPTIONS = {
    "check_only": CmdOpt("-c", False),
    "filename": CmdOpt("-f", True),
    "hide_var_name": CmdOpt("-n", False),
    "list_all": CmdOpt("-l", False),
    "match_var_names": CmdOpt("-L", False),
    "match_var_values": CmdOpt("-m", True),
    "section": CmdOpt("-s", True),
    "section_override": CmdOpt("-O", False),
    "section_specified": CmdOpt("", False),
    "show_var_name": CmdOpt("-N", False),
}


def get_test_path(relpath: Optional[str]) -> str:
    """Get the path to a test definition file."""
    return os.environ.get("TESTDIR", "test_data") + ("/" + relpath if relpath is not None else "")


@dataclasses.dataclass(frozen=True)
class XFormType(metaclass=abc.ABCMeta):
    """Transform something to something else with great prejudice."""

    @property
    @abc.abstractmethod
    def command(self) -> str:
        """Get the shell command to transform the confget output."""
        raise NotImplementedError(f"{type(self).__name__}.command")

    @abc.abstractmethod
    def do_xform(self, res: Iterable[cformat.FormatOutput]) -> str:
        """Transform the Python representation of the result."""
        raise NotImplementedError(f"{type(self).__name__}.do_xform()")


@dataclasses.dataclass(frozen=True)
class XFormNone(XFormType):
    """No transformation, newlines preserved."""

    @property
    def command(self) -> str:
        return ""

    def do_xform(self, res: Iterable[cformat.FormatOutput]) -> str:
        xform = "\n".join([line.output_full for line in res])
        return xform


@dataclasses.dataclass(frozen=True)
class XFormNewlineToSpace(XFormType):
    """Translate newlines to spaces."""

    @property
    def command(self) -> str:
        return '| tr "\\n" " "'

    def do_xform(self, res: Iterable[cformat.FormatOutput]) -> str:
        xform = "".join(line.output_full + " " for line in res)
        return xform


@dataclasses.dataclass(frozen=True)
class XFormCountLines(XFormType):
    """Count the lines output by confget."""

    sought: Optional[str] = None
    sought_in: bool = True

    @property
    def command(self) -> str:
        prefix = (
            # pylint: disable-next=consider-using-f-string
            "| fgrep -{inv}e {sought} ".format(
                inv="" if self.sought_in else "v",
                sought=shlex.quote(self.sought),
            )
            if self.sought is not None
            else ""
        )
        return prefix + "| wc -l | tr -d ' '"

    def do_xform(self, res: Iterable[cformat.FormatOutput]) -> str:
        if self.sought is None:
            return str(len(list(res)))

        lines = [line for line in res if self.sought_in == (self.sought in line.output_full)]
        return str(len(lines))


XFORM = {
    "": XFormNone(),
    "count-lines": XFormCountLines(),
    "count-lines-eq": XFormCountLines(sought="="),
    "count-lines-non-eq": XFormCountLines(sought="=", sought_in=False),
    "newline-to-space": XFormNewlineToSpace(),
}


class OutputDef(metaclass=abc.ABCMeta):
    """A definition for a single test's output."""

    def __init__(self) -> None:
        """No initialization at all for the base class."""

    @abc.abstractmethod
    def get_check(self) -> str:
        """Get the check string as a shell command."""
        raise NotImplementedError(f"{type(self).__name__}.get_check()")

    @property
    @abc.abstractmethod
    def var_name(self) -> str:
        """Get the variable name to display."""
        raise NotImplementedError(f"{type(self).__name__}.var_name")

    @abc.abstractmethod
    def check_result(self, _res: str) -> None:
        """Check whether the processed confget result is correct."""
        raise NotImplementedError(f"{type(self).__name__}.check_result()")


class ExactOutputDef(OutputDef):
    """Check that the program output this exact string."""

    def __init__(self, exact: str) -> None:
        """Initialize an exact test output object."""
        super().__init__()
        self.exact = exact

    def get_check(self) -> str:
        return '[ "$v" = ' + shlex.quote(self.exact) + " ]"

    @property
    def var_name(self) -> str:
        return "v"

    def check_result(self, res: str) -> None:
        assert res == self.exact


class ExitOKOutputDef(OutputDef):
    """Check that the program succeeded or failed as expected."""

    def __init__(self, success: bool) -> None:
        """Initialize an "finished successfully" test output object."""
        super().__init__()
        self.success = success

    def get_check(self) -> str:
        # pylint: disable-next=consider-using-f-string
        return '[ "$res" {compare} 0 ]'.format(compare="=" if self.success else "!=")

    @property
    def var_name(self) -> str:
        return "res"

    def check_result(self, res: str) -> None:
        # pylint: disable=useless-super-delegation
        super().check_result(res)


@dataclasses.dataclass(frozen=True)
class SingleTestDef:
    """A definition for a single test."""

    args: Dict[str, str]
    keys: List[str]
    output: OutputDef
    xform: str = ""
    backend: str = cdefs.BackendType.INI
    stdin: Optional[str] = None

    def get_backend(self) -> Type[cbackend.abstract.Backend]:
        """Get the appropriate confget backend type."""
        return cbackend.BACKENDS[self.backend]

    def get_config(self) -> cformat.FormatConfig:
        """Convert the test's data to a config object."""
        data: Dict[str, Any] = {}
        for name, value in self.args.items():
            if name == "hide_var_name":
                continue

            opt = CMDLINE_OPTIONS[name]
            if opt.has_argument:
                data[name] = value
            else:
                data[name] = True

        if "filename" in data:
            data["filename"] = get_test_path(data["filename"])
        elif self.stdin:
            data["filename"] = "-"

        data["show_var_name"] = "show_var_name" in self.args or (
            ("match_var_names" in self.args or "list_all" in self.args or len(self.keys) > 1)
            and "hide_var_name" not in self.args
        )

        return cformat.FormatConfig(self.keys, **data)

    def do_xform(self, res: Iterable[cformat.FormatOutput]) -> str:
        """Return the output delimiter depending on the xform property."""
        return XFORM[self.xform].do_xform(res)


@dataclasses.dataclass(frozen=True)
class FileDef:
    """A definition for a file defining related tests."""

    tests: List[SingleTestDef]
