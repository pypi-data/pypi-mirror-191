# Copyright (c) 2018 - 2022  Peter Pentchev
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

"""The command-line interface to the confget module: specify some parameters
through command-line options, then display variable values or names.
"""

import argparse
import dataclasses
import enum
import sys

from typing import Optional, Tuple

from . import backend
from . import defs
from . import format as fmt
from . import read_ini_file


class QType(str, enum.Enum):
    """The argument to the `-q` command-line option."""

    FEATURE = "feature"
    FEATURES = "features"
    SECTIONS = "sections"

    def __str__(self) -> str:
        """A human-readable representation (the value itself)."""
        return self.value


@dataclasses.dataclass
class MainConfig(fmt.FormatConfig):
    # pylint: disable=too-many-instance-attributes
    """Extend the format config class with some output settings.

    Add the following settings:
    - check_only (boolean): only check whether a variable is defined
    - query_sections (boolean): only display the section names
    """

    check_only: bool = False
    query_sections: bool = False


def version() -> None:
    """Display program version information."""
    print("confget " + defs.VERSION_STRING)


def features(name: Optional[str]) -> None:
    """Display a list of the features supported by the program."""
    if name is None:
        print(" ".join([f"{item[0]}={item[1]}" for item in defs.FEATURES]))
    else:
        ver = dict(defs.FEATURES).get(name, None)
        if ver is None:
            sys.exit(1)
        print(ver)


def output_check_only(cfg: MainConfig, data: defs.ConfigData) -> None:
    """Check whether the variable is present."""
    if cfg.section not in data:
        sys.exit(1)
    elif cfg.varnames[0] not in data[cfg.section]:
        sys.exit(1)
    sys.exit(0)


def output_vars(cfg: MainConfig, data: defs.ConfigData) -> None:
    """Output the variable values."""
    for vitem in fmt.filter_vars(cfg, data):
        print(vitem.output_full)


def output_sections(data: defs.ConfigData) -> None:
    """Output the section names."""
    for name in sorted(data.keys()):
        if name:
            print(name)


def validate_options(args: argparse.Namespace, backend_name: str) -> None:
    """Detect invalid combinations of command-line options."""
    # pylint: disable=confusing-consecutive-elif
    query_sections = args.query == QType.SECTIONS

    if args.list_all or query_sections:
        if args.varnames:
            sys.exit("Only a single query at a time, please!")
    elif args.match_var_names:
        if not args.varnames:
            sys.exit("No patterns to match against")
    elif args.check_only and len(args.varnames) > 1:
        sys.exit("Only a single query at a time, please!")
    elif not args.varnames:
        sys.exit("No variables specified to query")

    if query_sections and not backend_name.startswith("ini"):
        sys.exit("The query for sections is only supported for INI-style backends for the present")


def check_option_conflicts(args: argparse.Namespace) -> None:
    """Make sure that the command-line options do not conflict."""
    total = (
        int(args.query is not None)
        + int(args.match_var_names)
        + int(args.list_all)
        + int(bool(args.varnames) and not (args.match_var_names or args.query == QType.FEATURE))
    )
    if total > 1:
        sys.exit("Only a single query at a time, please!")


def parse_args() -> Tuple[MainConfig, str]:
    """Parse the command-line arguments."""
    parser = argparse.ArgumentParser(
        prog="confget",
        usage="""
    confget [-t ini] -f filename [-s section] varname...
    confget -V | -h | --help | --version
    confget -q features""",
    )
    parser.add_argument(
        "-c",
        action="store_true",
        dest="check_only",
        help="check whether the variables are defined in the file",
    )
    parser.add_argument(
        "-f",
        type=str,
        dest="filename",
        help="specify the configuration file name",
    )
    parser.add_argument(
        "-L",
        action="store_true",
        dest="match_var_names",
        help="specify which variables to display",
    )
    parser.add_argument(
        "-l",
        action="store_true",
        dest="list_all",
        help="list all variables in the specified section",
    )
    parser.add_argument(
        "-m",
        type=str,
        dest="match_var_values",
        help="only display variables with values that match the specified pattern",
    )
    parser.add_argument(
        "-N",
        action="store_true",
        dest="show_var_name",
        help="always display the variable name",
    )
    parser.add_argument(
        "-n",
        action="store_true",
        dest="hide_var_name",
        help="never display the variable name",
    )
    parser.add_argument(
        "-O",
        action="store_true",
        dest="section_override",
        help="allow variables in the specified section to "
        "override those placed before any "
        "section definitions",
    )
    parser.add_argument(
        "-P",
        type=str,
        dest="name_suffix",
        help="display this string after the variable name",
    )
    parser.add_argument(
        "-p",
        type=str,
        dest="name_prefix",
        help="display this string before the variable name",
    )
    parser.add_argument(
        "-q",
        type=QType,
        dest="query",
        choices=[QType.FEATURE, QType.FEATURES, QType.SECTIONS],
        help="query for a specific type of information, e.g. the list of "
        "sections defined in "
        "the configuration file",
    )
    parser.add_argument(
        "-S",
        action="store_true",
        dest="shell_quote",
        help="quote the values suitably for the Bourne shell",
    )
    parser.add_argument(
        "-s",
        type=str,
        dest="section",
        help="specify the configuration file section",
    )
    parser.add_argument(
        "-t",
        type=str,
        default=defs.BackendType.INI,
        dest="backend",
        help="specify the configuration file type",
    )
    parser.add_argument(
        "-V",
        "--version",
        action="store_true",
        help="display program version information and exit",
    )
    parser.add_argument(
        "-x",
        action="store_true",
        dest="match_regex",
        help="treat the match patterns as regular expressions",
    )
    parser.add_argument("varnames", nargs="*", help="the variable names to query")

    args = parser.parse_args()
    if args.version:
        version()
        sys.exit(0)

    check_option_conflicts(args)

    if args.query == QType.FEATURES:
        if args.varnames:
            sys.exit("No arguments to -q features")
        features(None)
        sys.exit(0)
    if args.query == QType.FEATURE:
        if len(args.varnames) != 1:
            sys.exit("Only a single feature name expected")
        features(args.varnames[0])
        sys.exit(0)

    query_sections = args.query == QType.SECTIONS

    cfg = MainConfig(
        check_only=args.check_only,
        filename=args.filename,
        list_all=args.list_all,
        match_regex=args.match_regex,
        match_var_names=args.match_var_names,
        match_var_values=args.match_var_values,
        name_prefix=args.name_prefix,
        name_suffix=args.name_suffix,
        query_sections=query_sections,
        section=args.section if args.section is not None else "",
        section_override=args.section_override,
        section_specified=args.section is not None,
        shell_escape=args.shell_quote,
        show_var_name=args.show_var_name
        or (
            (args.match_var_names or args.list_all or len(args.varnames) > 1)
            and not args.hide_var_name
        ),
        varnames=args.varnames,
    )

    matched_backends = (
        [args.backend]
        if args.backend in backend.BACKENDS
        else [name for name in sorted(backend.BACKENDS.keys()) if name.startswith(args.backend)]
    )
    if not matched_backends:
        sys.exit(f'Unknown backend "{args.backend}", use "list" for a list')
    elif len(matched_backends) > 1:
        sys.exit(f'Ambiguous backend "{args.backend}": {" ".join(matched_backends)}')
    backend_name = matched_backends[0]
    assert backend_name.startswith("ini")

    validate_options(args, backend_name)

    return cfg, backend_name


def main() -> None:
    """The main program: parse arguments, do things."""
    cfg, backend_name = parse_args()

    try:
        data = read_ini_file(cfg, backend_name=backend_name)
    except Exception as exc:  # pylint: disable=broad-except
        sys.exit(str(exc))

    if cfg.check_only:
        output_check_only(cfg, data)
    elif cfg.query_sections:
        output_sections(data)
    else:
        output_vars(cfg, data)


if __name__ == "__main__":
    main()
