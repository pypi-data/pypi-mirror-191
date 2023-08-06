# BSD 3-Clause License
# 
# Copyright (c) 2023, LuxProvide S.A.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# 
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

__email__      = 'jean-philippe.clipffel@lxp.lu'
__author__     = 'Jean-Philippe Clipffel <jean-philippe.clipffel@lxp.lu>'
__license__    = 'BSD-3-Clause'
__copyright__  = 'Copyright (c) 2023 LuxProvide S.A.'
__maintainer__ = 'Jean-Philippe Clipffel'


import importlib
import pkgutil
import argparse

# Disable Pydantic warnings
import warnings
warnings.filterwarnings('ignore')

# MelCtl plugins packages
import melctl_client_plugins

from .hints import Hinter


def load_commands(commands, subparser):
    """Loads and initializes MelCtl commands.

    :param subparser: Argparse's subparser
    """
    # Commands parsers, subparsers and instances
    commands_parsers = []
    commands_subparsers = []
    commands_instances = []
    # Commands parsers, subparsers and instances initialization
    for command_name, commands_actions in commands.items():
        # For command in form 'melctl <command> <action> ...':
        if isinstance(commands_actions, (list, tuple, set)):
            commands_parsers.append(subparser.add_parser(command_name))
            commands_subparsers.append(
                commands_parsers[-1].add_subparsers(dest='action')
            )
            for command_action in commands_actions:
                commands_instances.append(command_action(commands_subparsers[-1]))
                commands_subparsers[-1].required = True
        # For command in form 'melctl <command> ...':
        else:
            commands_instances.append(commands_actions(subparser))
    # Done
    return commands_parsers, commands_subparsers, commands_instances


def load_plugins(subparser, pkgs: list = [melctl_client_plugins,]):
    """Load MelCtl client plugins.

    :param subparser: Argparse's subparser
    :param pkgs: Packages to load plugins from
    """
    for pkg in pkgs:
        for _, name, _ in pkgutil.iter_modules(pkg.__path__, pkg.__name__ + '.'):
            # Import plugin
            plugin = importlib.import_module(name)
            # Load plugin commands
            if hasattr(plugin, 'commands'):
                load_commands(plugin.commands, subparser)


def main():
    """MelCtl entry point.
    """
    # Root parser and subparser
    parser = argparse.ArgumentParser('melctl')
    subparser = parser.add_subparsers(dest='command')
    subparser.required = True
    # Load and init plugins & commands
    load_plugins(subparser)
    # Parse arguments, run hints and invoke command
    args = parser.parse_args()
    Hinter()(args)
    args.func(args)


if __name__ == '__main__':
    main()
