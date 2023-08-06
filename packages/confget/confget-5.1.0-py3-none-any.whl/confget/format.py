# Copyright (c) 2018 - 2020, 2022  Peter Pentchev <roam@ringlet.net>
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

"""Filter and format a subset of the configuration variables."""

import dataclasses
import fnmatch
import re
import shlex

from typing import Callable, Dict, Iterable, NamedTuple, List, Optional

from . import defs


class FormatOutput(NamedTuple):
    """A single formatted variable, value, etc."""

    name: str
    value: str
    output_name: str
    output_value: str
    output_full: str


@dataclasses.dataclass
class FormatConfig(defs.Config):
    # pylint: disable=too-many-instance-attributes
    """Extend the config class with some output settings.

    Add the following settings:
    - list_all (boolean): list all variables, not just a subset
    - match_regex (boolean): for match_var_names and match_var_values,
      perform regular expression matches instead of filename pattern ones
    - match_var_names (boolean): treat the variable names specified as
      patterns and display all variables that match those
    - match_var_values (string): display only the variables with values
      that match this pattern
    - name_prefix (string): when displaying variable names, prepend this string
    - name_suffix (string): when displaying variable names, append this string
    - show_var_name (boolean): display the variable names, not just
      the values
    - shell_escape (boolean): format the values in a manner suitable for
      the Bourne shell
    """

    list_all: bool = False
    match_regex: bool = False
    match_var_names: bool = False
    match_var_values: Optional[str] = None
    name_prefix: Optional[str] = None
    name_suffix: Optional[str] = None
    section_override: bool = False
    show_var_name: bool = False
    shell_escape: bool = False


def get_check_function(cfg: FormatConfig, patterns: List[str]) -> Callable[[str], bool]:
    """Get a predicate for displayed variables.

    Get a function that determines whether a variable name should be
    included in the displayed subset.
    """
    if cfg.match_regex:
        re_vars = [re.compile(name) for name in patterns]

        def check_re_vars(key: str) -> bool:
            """Check that the key matches any of the specified regexes."""
            return any(rex.search(key) for rex in re_vars)

        return check_re_vars

    def check_fn_vars(key: str) -> bool:
        """Check that the key matches any of the specified patterns."""
        return any(fnmatch.fnmatch(key, pattern) for pattern in patterns)

    return check_fn_vars


def get_varnames(cfg: FormatConfig, sect_data: Dict[str, str]) -> Iterable[str]:
    """Get the variable names that match the configuration requirements."""
    if cfg.list_all:
        varnames: Iterable[str] = sect_data.keys()
    elif cfg.match_var_names:
        check_var = get_check_function(cfg, cfg.varnames)
        varnames = [name for name in sect_data.keys() if check_var(name)]
    else:
        varnames = [name for name in cfg.varnames if name in sect_data]

    if not cfg.match_var_values:
        return varnames

    check_value = get_check_function(cfg, [cfg.match_var_values])
    return [name for name in varnames if check_value(sect_data[name])]


def filter_vars(cfg: FormatConfig, data: defs.ConfigData) -> Iterable[FormatOutput]:
    """Filter the variables according to the specified criteria.

    Return an iterable of FormatOutput structures allowing the caller to
    process the variable names and values in various ways.
    """
    sect_data = data[""] if cfg.section_override else {}
    if cfg.section in data:
        sect_data.update(data[cfg.section])

    varnames = get_varnames(cfg, sect_data)
    res: List[FormatOutput] = []
    for name in sorted(varnames):
        output_name = "".join(
            [
                "" if cfg.name_prefix is None else cfg.name_prefix,
                name,
                "" if cfg.name_suffix is None else cfg.name_suffix,
            ]
        )

        value = sect_data[name]
        output_value = shlex.quote(value) if cfg.shell_escape else value
        output_full = f"{output_name}={output_value}" if cfg.show_var_name else output_value

        res.append(
            FormatOutput(
                name=name,
                value=value,
                output_name=output_name,
                output_value=output_value,
                output_full=output_full,
            )
        )

    return res
