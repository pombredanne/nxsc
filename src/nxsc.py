#-*- coding: utf-8 -*-

'''
File: nxsc.py
Author: Michał "NeoXant" Kolarczyk
License: GNU GPL version 3 (see LICENSE file)

Main NXSC script

Code passes PEP8 guidlines (pep8.py agreed with that)
'''

import platform
import argparse
from filehipporepo import FileHippoRepo
#print(platform.architecture()[0])

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                prog='nxsc',
                description='Python script for easy download, '
                    'install and update software on Microsoft Windows',
                epilog='More information at http://github.com/NeoXant/nxsc',
                formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('--version', help='show version', action='version',
         version='''NXSC 0.1.0
Copyright (c) 2013 Michal "NeoXant" Kolarczyk
This software is under GNU GPL version 3 license''')

    subparsers = parser.add_subparsers(
        title='commands',
        description='commands to execute:',
        dest='command')

    parser_install = subparsers.add_parser(
        'install',
        help='install application(s)')
    parser_install.add_argument(
        'app_name',
        help='application name',
        nargs='+')
    parser_install.add_argument(
        '--beta', '-b',
        help='install beta version if is newer than stable',
        default=False,
        action='store_true')

    parser_search = subparsers.add_parser(
        'search',
        help='search for application(s)')
    parser_search.add_argument(
        'app_name',
        help='application name',
        nargs='+')

    parser_update = subparsers.add_parser(
        'update',
        help='update information about installed applications')

    parser_upgrade = subparsers.add_parser(
        'upgrade',
        help='install updates')
    parser_upgrade.add_argument(
        'app_name',
        help='application name',
        nargs='*')

    parser_show = subparsers.add_parser(
        'show',
        help='displays detailed information about one or more applications')
    parser_show.add_argument(
        'app_name',
        help='application name')
    parser_show.add_argument(
        '--beta', '-b',
        help='show beta version if is newer than stable',
        default=False,
        action='store_true')

    parser_download = subparsers.add_parser(
        'download',
        help='only download application(s) without installing')
    parser_download.add_argument(
        'app_name',
        help='application name',
        nargs='+')
    parser_download.add_argument(
        '--beta', '-b',
        help='show beta version if is newer than stable',
        default=False,
        action='store_true')

    args = parser.parse_args()
    print('''NXSC 0.1.0
Copyright (c) 2013 Michał "NeoXant" Kolarczyk
This software is under GNU GPL version 3 license
''')
    arch = platform.architecture()[0]
    if args.command:
        print("==> Detected OS architecture: " + arch)
        if hasattr(args, 'beta'):
            fh = FileHippoRepo(arch, args.beta)
        else:
            fh = FileHippoRepo(arch)
        if args.command == 'search':
            fh.search(args.app_name)
        elif args.command == 'show':
            fh.show(args.app_name)
        elif args.command == 'install':
            fh.download(args.app_name)
            fh.install()
        elif args.command == 'download':
            fh.download(args.app_name)
        elif args.command == 'update':
            fh.update()
        elif args.command == 'upgrade':
            fh.upgrade(args.app_name)
    else:
        parser.print_help()
