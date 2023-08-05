#!/usr/bin/python3
# -*- coding: utf-8 -*-


# from __future__ import unicode_literals
import os
import sys
import time
import pydoc
import locale
import urllib3
import hashlib
import subprocess
from datetime import date
from dialog import Dialog
from sbo_create.templates import (
    SlackBuilds,
    doinst
)

from sbo_create.__metadata__ import __version__

locale.setlocale(locale.LC_ALL, '')


class SBoCreate:
    """ SlackBuild Create Class. """
    def __init__(self):
        # General defines
        self.pwd = None
        self.choices = None
        self.HOME = None
        self.data = None
        self.fields = None
        self.code = None
        self.handy_ruler = None
        self.editor = None
        self.where_you_live = None
        self.email = None
        self.maintainer = None
        self.elements = None
        self.comments = None
        self.width = None
        self.height = None
        self.msg = None
        self.filename = None
        self.editor_options = None
        self.sbo_name = None
        self.sources = None
        self.chk_md5 = None

        # Set colors
        self.colors = {'bold': '\Zb',
                       'reset_bold': '\ZB',
                       'underline': '\Zu',
                       'reset_underline': '\ZU',
                       'reverse': '\Zr',
                       'reset_reverse': 'Zr',
                       'restore': '\Zn',
                       'black': '\Z0',
                       'red': '\Z1',
                       'green': '\Z2',
                       'yellow': '\Z3',
                       'blue': '\Z4',
                       'magenta': '\Z5',
                       'cyan': '\Z6',
                       'white': '\Z7'}

        # Define some configurations
        self.HOME = f'{os.getenv("HOME")}/'
        self.year = date.today().year
        self.d = Dialog(dialog='dialog')
        self.d.add_persistent_args(['--no-nl-expand', '--no-collapse', '--colors'])
        self.title = f'SlackBuild Create Tool {__version__}'
        self.d.set_background_title(self.title)
        self.var_log_packages = '/var/log/packages/'
        self.args = sys.argv
        self.args.pop(0)
        self.arguments()
        self.pwd = f'{os.getcwd()}/'
        self.slack_desc_text = []
        self.slack_desc_data = []
        self.get_the_sboname()

        # aboname.info
        self.info_text = ['PRGNAM=', 'VERSION=', 'HOMEPAGE=', 'DOWNLOAD=',
                          'MD5SUM=', 'DOWNLOAD_x86_64=', 'MD5SUM_x86_64=',
                          'REQUIRES=', 'MAINTAINER=', 'EMAIL=']
        self._version = ''
        self._homepage = ''
        self._download_x86 = ''
        self._md5sum = ''
        self._download_x86_64 = ''
        self._md5sum_x86_64 = ''
        self._requires = ''

        # sboname.desktop
        self._comment = ''
        self._exec = f'/usr/bin/{self.sbo_name}'
        self._icon = f'/usr/share/pixmaps/{self.sbo_name}.png'
        self._terminal = 'false'
        self._type = ''
        self._categories = ''
        self._generic_name = ''

    def arguments(self):
        """ Arguments for the cli. """
        if len(self.args) > 1:
            self.usage()
        elif len(self.args) == 1 and self.args[0] in ['-h', '--help']:
            self.usage()
        elif len(self.args) == 1 and self.args[0] in ['-v', '--version']:
            self.version()
        elif len(self.args) == 1:
            self.sbo_name = self.args[0]

        self.check_for_installed_packages()

    def get_the_sboname(self):
        """ Importing the name from the folder name. """
        sboname = self.pwd.split('/')[-2]
        message = (f"The name '{self.sbo_name}' it\'s different from the folder name.\n"
                   f"\nDo you want to use the name '{sboname}'?")

        if not self.sbo_name:
            self.sbo_name = sboname

        if not self.sbo_name or self.sbo_name != sboname:
            yesno = self.d.yesno(message, height=8, width=(len(self.sbo_name) + 52))

            if yesno == 'ok':
                self.sbo_name = sboname

    def check_for_installed_packages(self):
        """ Check if the package is already installed in your distribution
        or if you have already slpkg installed checks slackbuilds from the
        repository. """
        all_packages = []
        packages = os.listdir(self.var_log_packages)

        for p in packages:
            all_packages.append('-'.join(p.split('-')[:-3]))

        for pkg in all_packages:
            if pkg == self.sbo_name:
                yesno = self.d.yesno(f"{self.colors['red']}WARNING!{self.colors['restore']}"
                                     f" There is a package with the name '{self.sbo_name}'.\n"
                                     '\nDo you want to continue?', height=8, width=55 + len(self.sbo_name))

                if yesno == 'cancel':
                    self.exit()

    def slackbuild_init(self):
        """ Initialization slackbuilds data. """
        self.filename = ''
        self.msg = ''
        self._md5sum = ''
        self._md5sum_x86_64 = ''
        self.data = []
        self.height = 30
        self.width = 80
        self.filename = f'{self.HOME}.sbo-maintainer'
        self.__maintainer_data_read()
        self.choices = [
            ('Info', f'Edit {self.sbo_name}.info file'),
            ('Slack desc', 'Edit slack-desc file'),
            ('SlackBuild', f'Edit {self.sbo_name}.SlackBuild script'),
            ('Doinst.sh', 'Edit doinst.sh script'),
            ('README', 'Edit README file'),
            ('Desktop', f'Edit {self.sbo_name}.desktop file'),
            ('Chmod', f'Permissions -+ {self.sbo_name}.SlackBuild script'),
            ('Download', 'Download the sources'),
            ('MD5SUM', 'Checksum the sources'),
            ('Check', f'Check if the {self.sbo_name} SBo exists.'),
            ('Maintainer', 'Maintainer data'),
            ('Directory', 'Change directory'),
            ('Help', 'Where to get help'),
            ('About', 'About sbo-create'),
            ('Exit', 'Exit the program')
        ]

    def menu(self):
        """ Dialog.menu(text, height=None, width=None, menu_height=None,
        choices=[], **kwargs)
        Display a menu dialog box. """
        self.slackbuild_init()  # reset all data
        width = 53 + len(self.sbo_name)
        code, tag = self.d.menu(f"{' ' * int(width / 3.5)}{self.colors['green']}{self.colors['bold']}"
                                f"SlackBuild Create Tool{self.colors['restore']}\n\n"
                                'Choose an option or press ESC or <Cancel> to Exit.\n',
                                height=27, width=width,
                                menu_height=len(self.choices),
                                choices=self.choices, help_button=True)

        if code == self.d.CANCEL or code == self.d.ESC or tag[0] == '0':
            self.exit()
        elif code == 'help':
            self.get_help()

        case = {
            'Info': self.info_file,
            'Slack desc': self.slack_desc,
            'SlackBuild': self.slackbuild,
            'Doinst.sh': self.doinst_sh,
            'Desktop': self.desktop_file,
            'README': self.readme,
            'Chmod': self.chmod,
            'Download': self.download,
            'MD5SUM': self.md5sum,
            'Check': self.check_sbo,
            'Maintainer': self.maintainer_data,
            'Directory': self.__update_directory,
            'Help': self.get_help,
            'About': self.about,
            'Exit': self.exit
        }
        case[tag]()

    def get_help(self):
        """ Get help from slackbuilds.org. """
        self.msg = ('For additional assistance, visit:\n\n'
                    f"SlackBuild Usage HOWTO: {self.colors['blue']}https://www.slackbuilds.org/howto/"
                    f"{self.colors['restore']}\n"
                    f"Frequently Asked Questions: {self.colors['blue']}https://www.slackbuilds.org/faq/"
                    f"{self.colors['restore']}\n"
                    f"Submission Guidelines: {self.colors['blue']}http://www.slackbuilds.org/guidelines/"
                    f"{self.colors['restore']}\n")

        self.width = 70
        self.height = 10
        self.message_box()
        self.menu()

    def check_sbo(self):
        """ Checks if the SlackBuild exist in the SBo repository. """
        self.d.infobox('Searching please wait...', width=30, height=5)
        self.msg = (f"No SlackBuild found with the name "
                    f"'{self.colors['magenta']}{self.sbo_name}{self.colors['restore']}' in the repository.")
        self.width = len(self.msg) + 3
        self.height = 7

        repo = 'https://slackbuilds.org/slackbuilds/15.0/TAGS.txt'
        http = urllib3.PoolManager()
        repo = http.request('GET', repo)

        for sbo in repo.data.decode().splitlines():
            if self.sbo_name == sbo.split(':')[0]:
                self.width = 50 + len(self.sbo_name)
                self.msg = (f"The SlackBuild '{self.colors['magenta']}{self.sbo_name}{self.colors['restore']}'"
                            f" exists in the repository.")

        self.message_box()
        self.menu()

    def chmod(self):
        """ Change the permissions on the .SlackBuild script. """
        self.height = 7
        self.width = len(self.sbo_name) + 40
        if not os.path.isfile(f'{self.sbo_name}.SlackBuild'):
            self.msg = f'There is no {self.sbo_name}.SlackBuild script.'
            self.message_box()
            self.menu()

        text = 'Change the permissions to the SlackBuild script.'
        height = 10
        width = len(text) + len(self.sbo_name) + 3

        choices = [
            ('chmod +x', f'{self.sbo_name}.SlackBuild', False),
            ('chmod -x', f'{self.sbo_name}.Slackbuild', False),
            ]

        code, tag = self.d.radiolist(text, height,
                                     width, list_height=0, choices=choices)
        if code == 'cancel':
            self.menu()

        if tag == 'chmod +x':
            subprocess.call(f'chmod +x {self.sbo_name}.SlackBuild', shell=True)

        if tag == 'chmod -x':
            subprocess.call(f'chmod -x {self.sbo_name}.SlackBuild', shell=True)

        self.msg = f'The permissions has been changed in the script {self.sbo_name}.SlackBuild.'
        self.message_box()
        self.menu()

    def download(self):
        """ Download the sources. """
        self.filename = f'{self.sbo_name}.info'

        self.__info_file_read()

        if not self._download_x86 and not self._download_x86_64:
            self.height = 7
            self.msg = "There are no DOWNLOAD's in the .info file."
            self.message_box()
            self.menu()

        if self._download_x86:
            for link in self._download_x86.split():
                self.wget(link)

        if self._download_x86_64:
            for link in self._download_x86_64.split():
                self.wget(link)

        self.menu()

    def md5sum(self):
        """ Update the source checksum. """
        self.filename = f'{self.sbo_name}.info'
        text1 = 'Choose which checksum you want to update.'
        text2 = 'Select the type of the architecture.'
        files = {}

        self.__info_file_read()

        sources = self._download_x86
        if not self._download_x86:
            sources = self._download_x86_64

        if not sources:
            self.msg = 'No sources found.'
            self.height = 7
            self.width = len(self.msg) + 7
            self.message_box()
            self.menu()

        height = 20
        width = 80
        choices = []

        # Creating a dictionary with file and checksum
        for src in sources.split():
            file = src.split('/')[-1]
            files[file] = self.source_check_sum(file)

        # Add the items to a list for choosing
        for k, v in files.items():
            choices += [
                (v, k, False)
            ]

        code1, tag1 = self.d.checklist(text1, height,
                                       width, list_height=0, choices=choices)

        if code1 == 'cancel':
            self.menu()

        choices = [
                ('MD5SUM', 'For x86 sources', False),
                ('MD5SUM_x86_64', 'For x86_64 sources', False),
            ]

        code2, tag2 = self.d.radiolist(text2, height,
                                       width, list_height=0, choices=choices)
        if code2 == 'cancel':
            self.menu()

        if tag2 == 'MD5SUM':
            self._md5sum = ' '.join(tag1)
        elif tag2 == 'MD5SUM_x86_64':
            self._md5sum_x86_64 = ' '.join(tag1)

        self.info_file()

    def maintainer_data(self):
        """ Maintainer data handler. """
        self.height = 15
        self.filename = f'{self.HOME}.sbo-maintainer'
        self.comments = ("Enter the details of the maintainer and change "
                         "the editor.\nVim is the default editor.")
        self.width = 75
        field_length = 68
        input_length = 100
        attributes = '0x0'

        text = ['MAINTAINER=', 'EMAIL=', 'WHERE YOU LIVE=', 'EDITOR=', 'OPTIONS FOR EDITOR=']

        self.elements = [
            (text[0], 1, 1, self.maintainer, 1, len(text[0]) + 1, field_length - len(text[0]), input_length,
             attributes),
            (text[1], 2, 1, self.email, 2, len(text[1]) + 1, field_length - len(text[1]), input_length,
             attributes),
            (text[2], 3, 1, self.where_you_live, 3, len(text[2]) + 1, field_length - len(text[2]), input_length,
             attributes),
            (text[3], 4, 1, self.editor, 4, len(text[3]) + 1, field_length - len(text[3]), input_length,
             attributes),
            (text[4], 5, 1, self.editor_options, 5, len(text[4]) + 1, field_length - len(text[4]), input_length,
             attributes)
        ]

        self.mixedform()

        if self.fields:
            self.maintainer = self.fields[0]
            self.email = self.fields[1]
            self.where_you_live = self.fields[2]
            self.editor = self.fields[3]
            self.editor_options = self.fields[4]

        for item, line in zip(text, self.fields):
            self.data.append(f'{item}{line}')

        self.choose()

    def slack_desc(self):
        """ slack-desc file handler. """
        self.height = 29
        self.handy_ruler = 1
        self.__slack_desc_comments()
        self.filename = 'slack-desc'
        self.width = 80 + len(self.sbo_name) + 1
        field_length = 70 + len(self.sbo_name) + 1
        input_length = 70
        attributes = '0x0'
        self.elements = []
        self.__slack_desc_read()
        self.slack_desc_text = []  # Reset slack text after read the file
        start_from = 1  # Set up the line to start

        if not self.slack_desc_data[0]:  # check description
            start_from = 2
            self.elements = [
                (f'{self.sbo_name}:', 1, 1, f' {self.sbo_name} ()', 1,
                 len(self.sbo_name) + 2, field_length - len(self.sbo_name), input_length, attributes)
            ]

        for i, line in zip(range(start_from, 13), self.slack_desc_data):
            self.elements += [(f'{self.sbo_name}:', i, 1, line, i,
                               len(self.sbo_name) + 2, field_length - len(self.sbo_name), input_length,
                               attributes)]

        self.mixedform()

        # Reads the comments second time to align the handy ruler
        self.handy_ruler = 0
        self.__slack_desc_comments()

        self.data = [line for line in self.comments.splitlines()]

        for line in self.fields:
            if not line.startswith(' ') and len(line) < 70:
                line = f' {line}'
            self.data.append(f'{self.sbo_name}:{line}')

        self.choose()

    def info_file(self):
        """ <application>.info file handler. """
        self.filename = f'{self.sbo_name}.info'
        self.comments = f"Creates a '{self.colors['magenta']}{self.filename}{self.colors['restore']}' file."
        self.width = 79
        self.height = 21
        field_length = 72
        input_length = 100
        attributes = '0x0'

        maintainer = self.maintainer
        email = self.email

        self.__info_file_read()

        # Checks for maintainer data
        if maintainer and maintainer != self.maintainer:
            yesno = self.d.yesno('Do you want to replace the maintainer data?',
                                 height=7, width=50)

            if yesno == 'ok':
                self.maintainer = maintainer
                self.email = email

        self.elements = [
            (self.info_text[0], 1, 1, self.sbo_name, 1, len(self.info_text[0]) + 1,
             field_length - len(self.info_text[0]), input_length, attributes),
            (self.info_text[1], 2, 1, self._version, 2, len(self.info_text[1]) + 1,
             field_length - len(self.info_text[1]), input_length, attributes),
            (self.info_text[2], 3, 1, self._homepage, 3, len(self.info_text[2]) + 1,
             field_length - len(self.info_text[2]), input_length * 2, attributes),
            (self.info_text[3], 4, 1, self._download_x86, 4, len(self.info_text[3]) + 1,
             field_length - len(self.info_text[3]), input_length * 10, attributes),
            (self.info_text[4], 5, 1, self._md5sum, 5, len(self.info_text[4]) + 1,
             field_length - len(self.info_text[4]), input_length * 10, attributes),
            (self.info_text[5], 6, 1, self._download_x86_64, 6, len(self.info_text[5]) + 1,
             field_length - len(self.info_text[5]), input_length * 10, attributes),
            (self.info_text[6], 7, 1, self._md5sum_x86_64, 7, len(self.info_text[6]) + 1,
             field_length - len(self.info_text[6]), input_length * 10, attributes),
            (self.info_text[7], 8, 1, self._requires, 8, len(self.info_text[7]) + 1,
             field_length - len(self.info_text[7]), input_length * 4, attributes),
            (self.info_text[8], 9, 1, self.maintainer, 9, len(self.info_text[8]) + 1,
             field_length - len(self.info_text[8]), input_length, attributes),
            (self.info_text[9], 10, 1, self.email, 10, len(self.info_text[9]) + 1,
             field_length - len(self.info_text[9]), input_length, attributes)
        ]

        self.mixedform()

        if self.fields:
            self._version = self.fields[1]
            self._homepage = self.fields[2]
            self._download_x86 = self.fields[3]
            self._md5sum = self.fields[4]
            self.maintainer = self.fields[8]
            self.email = self.fields[9]

            if self._download_x86:
                self.sources = [source.split('/')[-1] for source in self._download_x86.split()]
                self.chk_md5 = self._md5sum
                self.checksum()
            self._download_x86_64 = self.fields[5]
            self._md5sum_x86_64 = self.fields[6]

            if self._download_x86_64:
                self.sources = [source.split('/')[-1] for source in self._download_x86_64.split()]
                self.chk_md5 = self._md5sum_x86_64
                self.checksum()
            self._requires = self.fields[7]

        self.__autocorrect_quotation_mark()

        for item, line in zip(self.info_text, self.fields):
            self.data.append(f'{item}{line}')

        self.choose()

    def desktop_file(self):
        """ <application>.desktop file handler. """
        self.filename = f'{self.sbo_name}.desktop'
        self.width = 79
        self.height = 20
        self.comments = f"Creates a '{self.colors['magenta']}{self.filename}{self.colors['restore']}' file."
        field_length = 72
        input_length = 100
        attributes = '0x0'
        text = ['[Desktop Entry]', 'Name=', 'Comment=', 'Exec=', 'Icon=',
                'Terminal=', 'Type=', 'Categories=', 'GenericName=']

        self.__desktop_file_read()

        self.elements = [
            (text[0], 1, 1, '', 1, 1, field_length - len(text[0]), input_length, 0x1),
            (text[1], 2, 1, self.sbo_name, 2, 6, field_length - len(text[1]),
             input_length, attributes),
            (text[2], 3, 1, self._comment, 3, 9, field_length - len(text[2]), input_length,
             attributes),
            (text[3], 4, 1, self._exec, 4, 6, field_length - len(text[3]), input_length,
             attributes),
            (text[4], 5, 1, self._icon, 5, 6, field_length - len(text[4]), input_length,
             attributes),
            (text[5], 6, 1, self._terminal, 6, 10, field_length - len(text[5]), input_length,
             attributes),
            (text[6], 7, 1, self._type, 7, 6, field_length - len(text[6]), input_length,
             attributes),
            (text[7], 8, 1, self._categories, 8, 12, field_length - len(text[7]),
             input_length, attributes),
            (text[8], 9, 1, self._generic_name, 9, 13, field_length - len(text[8]),
             input_length, attributes),
        ]

        self.mixedform()

        if self.fields:
            self.sbo_name = self.fields[1]
            self._comment = self.fields[2]
            self._exec = self.fields[3]
            self._icon = self.fields[4]
            self._terminal = self.fields[5]
            self._type = self.fields[6]
            self._categories = self.fields[7]
            self._generic_name = self.fields[8]

        for item, line in zip(text, self.fields):
            self.data.append(item + line)
        self.choose()

    def doinst_sh(self):
        """ Doinst.sh handler file. """
        os.system('clear')
        temp = '\n'.join(doinst.splitlines())
        pydoc.pipepager(temp, cmd='less -R')
        self.filename = 'doinst.sh'
        self.edit()
        self.menu()

    def readme(self):
        """ README handler file. """
        self.filename = 'slack-desc'
        self.__slack_desc_read()
        self.filename = 'README'

        if os.path.isfile(f'{self.pwd}slack-desc') and len(self.slack_desc_text[1:]) > 0:
            if os.path.isfile(f'{self.pwd}{self.filename}') and os.path.getsize(f'{self.pwd}{self.filename}') == 0:
                self.__import_to_readme()
            elif not os.path.isfile(f'{self.pwd}{self.filename}'):
                self.__import_to_readme()

        self.slack_desc_text = []  # Reset
        self.edit()
        self.menu()

    def slackbuild(self):
        """ SlackBuild handler file. """
        self.filename = f'{self.sbo_name}.info'

        self.__info_file_read()

        self.filename = f'{self.sbo_name}.SlackBuild'

        if not os.path.isfile(self.pwd + self.filename):
            version = self._version.replace('"', '')
            height = 11
            width = 80
            choices = [
                ('autotools-template', 'autotools-template.SlackBuild', False),
                ('cmake-template', 'cmake-template.SlackBuild', False),
                ('perl-template', 'perl-template.SlackBuild', False),
                ('python-template', 'python-template.SlackBuild', False),
                ('rubygem-template', 'rubygem-template.SlackBuild', False),
                ('haskell-template', 'haskell-template.SlackBuild', False),
                ('meson-template', 'meson-template.SlackBuild', False)
            ]
            display = f'Choose a template for the {self.filename} file.'
            code, tag = self.d.radiolist(f'{display}', height, width, list_height=0, choices=choices)

            if code == 'cancel':
                self.menu()

            self.msg = f'{self.filename} script created.'
            self.height = 7
            self.width = len(self.msg) + 7

            if tag == 'autotools-template':
                self.data = SlackBuilds(
                    self.sbo_name, version, self.year, self.maintainer,
                    self.where_you_live).autotools().splitlines()

            elif tag == 'cmake-template':
                self.data = SlackBuilds(
                    self.sbo_name, version, self.year, self.maintainer,
                    self.where_you_live).cmake().splitlines()

            elif tag == 'perl-template':
                self.data = SlackBuilds(
                    self.sbo_name, version, self.year, self.maintainer,
                    self.where_you_live).perl().splitlines()

            elif tag == 'python-template':
                self.data = SlackBuilds(
                    self.sbo_name, version, self.year, self.maintainer,
                    self.where_you_live).python().splitlines()

            elif tag == 'rubygem-template':
                self.data = SlackBuilds(
                    self.sbo_name, version, self.year, self.maintainer,
                    self.where_you_live).rubygem().splitlines()

            elif tag == 'haskell-template':
                self.data = SlackBuilds(
                    self.sbo_name, version, self.year, self.maintainer,
                    self.where_you_live).haskell().splitlines()

            elif tag == 'meson-template':
                self.data = SlackBuilds(
                    self.sbo_name, version, self.year, self.maintainer,
                    self.where_you_live).meson().splitlines()

            else:
                self.height = 7
                self.msg = 'No SlackBuild template was selected.'
                self.width = len(self.msg) + 10
                self.message_box()
                self.menu()

            self.write()
            self.message_box()

        self.edit()
        self.menu()

    def mixedform(self):
        """ Dialog.mixedform(text, elements, height=0, width=0, form_height=0,
        **kwargs)
        Display a form consisting of labels and fields. """
        self.code, self.fields = self.d.mixedform(self.comments, self.elements,
                                                  self.height, self.width, help_button=True)
        if self.code == 'help':
            self.get_help()

    def edit(self):
        """ Editor handler. """
        if self.editor:
            subprocess.call(f'{self.editor} {self.editor_options} {self.pwd}{self.filename}', shell=True)

    def message_box(self):
        """ View messages. """
        self.d.msgbox(self.msg, self.height, self.width)

    def choose(self):
        """ Choosing if write to file or exit. """
        if self.code == self.d.OK:
            self.file_exist()

            if self.filename.endswith('.info'):
                self.write_info()
            else:
                self.write()
            self.message_box()
            self.menu()

        elif self.code == self.d.CANCEL:
            self.menu()
        elif self.code == self.d.ESC:
            self.menu()

    def __import_to_readme(self):
        """ Import data from slack-desc and write to readme. """
        yesno = self.d.yesno('Import description from the <slack-desc> file?', height=7, width=55)

        if yesno == 'ok':

            for desc in self.slack_desc_data[1:]:
                if desc and not desc.startswith((' Homepage:', ' homepage:')):
                    self.data.append(desc)

            # Removes the space at the beginning
            self.data = map(str.lstrip, self.data)

            self.write()

    def __maintainer_data_read(self):
        """ Initialization maintainer data. """
        self.maintainer = ''
        self.email = ''
        self.where_you_live = ''
        self.editor = 'vim'
        self.editor_options = ''

        if os.path.isfile(self.filename):
            with open(self.filename, 'r') as f:
                mnt = f.read().splitlines()

                if len(mnt) == 5:

                    if '=' in mnt[0]:
                        self.maintainer = mnt[0].split('=')[-1].strip()

                    if '=' in mnt[1]:
                        self.email = mnt[1].split('=')[-1].strip()

                    if '=' in mnt[2]:
                        self.where_you_live = mnt[2].split('=')[-1].strip()

                    if '=' in mnt[3]:
                        self.editor = mnt[3].split('=')[-1].strip()

                    if '=' in mnt[4]:
                        self.editor_options = mnt[4].split('=')[-1].strip()

                else:
                    self.width = 65
                    self.height = 6
                    self.msg = f"The {self.filename} seems it's not correct."
                    self.message_box()

    def __update_directory(self):
        """ Update working directory. """
        self.height = 10
        self.comments = f'Current directory: {self.pwd}'
        field_length = 90
        input_length = 90
        attributes = '0x0'
        self.elements = [
            ('New path=', 1, 1, self.pwd, 1, 10, field_length, input_length,
             attributes),
        ]
        self.mixedform()

        if self.fields:
            if not os.path.isdir(self.fields[0].strip()):
                self.width = 60
                self.height = 6
                self.msg = f"Directory '{self.fields[0].strip()}' is not exist."
                self.message_box()
                self.menu()

            self.pwd = self.fields[0].strip()

            if self.pwd and not self.pwd.endswith('/'):
                self.pwd = f'{self.pwd}/'

            self.width = 60
            self.height = 6
            self.msg = f'Current directory: {self.pwd}'
            self.message_box()

        self.menu()

    def __slack_desc_comments(self):
        """ slack-desc file comments. """
        left = (len(self.sbo_name) + self.handy_ruler)
        self.comments = (
            "# HOW TO EDIT THIS FILE:\n"
            "# The \"handy ruler\" below makes it easier to edit a package description.\n"
            "# Line up the first '|' above the ':' following the base package name, and\n"
            "# the '|' on the right side marks the last column you can put a character in.\n"
            "# You must make exactly 11 lines for the formatting to be correct.  It's also\n"
            "# customary to leave one space after the ':' except on otherwise blank lines.\n\n"
            f"{' ' * left}|-----handy-ruler------------------------------------------------------|")

    def __slack_desc_read(self):
        """ Grab slack-desc text if exist. """
        self.slack_desc_data = []  # Reset data before read

        if os.path.isfile(f'{self.pwd}{self.filename}'):
            with open(f'{self.pwd}{self.filename}', 'r') as info:
                for count, line in enumerate(info):

                    if 7 < count < 19:
                        line = line[len(self.sbo_name) + 1:].rstrip()

                        if line:
                            self.slack_desc_text.append(line)
                        self.slack_desc_data.append(line)
        else:
            self.slack_desc_data = [''] * 10

    def __autocorrect_quotation_mark(self):
        """ Autocorrect the quotation mark "" in the .info file. """
        for i, f in enumerate(self.fields):
            f = f.rstrip()

            if not f.startswith('"'):
                self.fields[i] = f'"{f}'

            if not f.endswith('"'):
                self.fields[i] = f'{self.fields[i]}"'

            if f == '' or f == '"':
                self.fields[i] = '""'

    def __info_file_read(self):
        """ Read data from <application>.info file if exist. """
        if os.path.isfile(f'{self.pwd}{self.filename}'):
            with open(f'{self.pwd}{self.filename}', 'r') as info:

                info_file = info.read().splitlines()

                self._version = self.info_find_element(self.info_text[1], info_file)
                self._homepage = self.info_find_element(self.info_text[2], info_file)

                self._download_x86 = self.info_find_elements_between(self.info_text[3], self.info_text[4], info_file)
                if not self._md5sum:
                    self._md5sum = self.info_find_elements_between(self.info_text[4], self.info_text[5], info_file)

                self._download_x86_64 = self.info_find_elements_between(self.info_text[5], self.info_text[6], info_file)
                if not self._md5sum_x86_64:
                    self._md5sum_x86_64 = self.info_find_elements_between(self.info_text[6], self.info_text[7],
                                                                          info_file)

                self._requires = self.info_find_element(self.info_text[7], info_file)
                self.maintainer = self.info_find_element(self.info_text[8], info_file)
                self.email = self.info_find_element(self.info_text[9], info_file)

    def __desktop_file_read(self):
        """ Read data from <application>.desktop file if exist. """
        if os.path.isfile(self.pwd + self.filename):
            with open(f'{self.pwd}{self.filename}', 'r') as f:
                dsk = f.read().splitlines()

                self._comment = dsk[2].split('=')[1].strip()
                self._exec = dsk[3].split('=')[1].strip()
                self._icon = dsk[4].split('=')[1].strip()
                self._terminal = dsk[5].split('=')[1].strip()
                self._type = dsk[6].split('=')[1].strip()
                self._categories = dsk[7].split('=')[1].strip()
                self._generic_name = dsk[8].split('=')[1].strip()

    @staticmethod
    def info_find_elements_between(start, stop, info_file: list):
        """ Find unknown elements between two elements in a list.
            Example:
                start: DOWNLOAD=a
                                b
                                c
                stop:  MD5SUM=d
                              e
                              f
                return:
                      a b c
        """
        begin, end, = 0, 0
        elements = []

        for i, info in enumerate(info_file):
            if info.startswith(start):
                begin = i
            if info.startswith(stop):
                end = i

        text = info_file[begin:end]

        for txt in text:
            txt = txt.replace('"', '')
            if start in txt:
                txt = txt.replace(start, '')
            elements.append(txt.strip())

        return ' '.join(elements)

    @staticmethod
    def info_find_element(tag, info_file):
        """ Find an element in a list. """
        for info in info_file:
            if info.startswith(tag):
                return info.split('=')[1].replace('"', '').strip()

    def file_exist(self):
        """ Check if file exist. """
        self.width = len(self.filename) + 33
        self.height = 6

        if os.path.isfile(f'{self.pwd}{self.filename}'):
            self.msg = f"The file '{self.filename}' modified."
        else:
            self.msg = f"The file '{self.filename}' is created."

    def checksum(self):
        """ checksum sources. """
        self.height = 7

        for source, md5 in zip(self.sources, self.chk_md5.split()):
            if os.path.isfile(f'{self.pwd}{source}'):
                if md5 != self.source_check_sum(source):
                    self.width = 40 + len(source)
                    self.msg = f"MD5SUM check for {source} {self.colors['red']}FAILED!{self.colors['restore']}"
                    self.message_box()
            else:
                self.msg += f"\nFile '{source}' not found."
                self.message_box()

    def source_check_sum(self, source):
        """ md5sum sources. """
        self.height = 7
        self.width = 30 + len(source)

        if os.path.isfile(f'{self.pwd}{source}'):
            with open(f'{self.pwd}{source}', 'rb') as f:
                data = f.read()
                return hashlib.md5(data).hexdigest()
        else:
            self.msg = f"File '{source}' not found."
            self.message_box()
            self.menu()

    def write_info(self):
        """ Write the info file. """
        with open(f'{self.pwd}{self.filename}', 'w') as f:
            for line in self.data:
                if line.startswith(self.info_text[3]):
                    self.write_the_info_line(f, line, 3)

                elif line.startswith(self.info_text[4]):
                    self.write_the_info_line(f, line, 4)

                elif line.startswith(self.info_text[5]):
                    self.write_the_info_line(f, line, 5)

                elif line.startswith(self.info_text[6]):
                    self.write_the_info_line(f, line, 6)

                else:
                    f.write(f'{line}\n')

    def write_the_info_line(self, f, line, tag):
        """ Do the dirty job for the info file. """
        for i, ln in enumerate(line.split(), start=1):
            if i > 1:
                ln = f'{" " * (len(self.info_text[tag]) + 1)}{ln}'
            f.write(f'{ln}\n')

    def write(self):
        """ Write handler. """
        cache = self.pwd
        if self.filename.endswith('.sbo-maintainer'):
            self.pwd = ''

        with open(f'{self.pwd}{self.filename}', 'w') as f:
            for line in self.data:
                # Remove trailing whitespaces
                line = line.rstrip()
                f.write(f'{line}\n')

            # An empty line on the EOF
            if self.filename == 'README':
                f.write('\n')

        self.pwd = cache

    def wget(self, link):
        """ Wget downloader. """
        file = link.split("/")[-1]

        yesno = self.d.yesno(f"{self.colors['blue']}{file}{self.colors['restore']}\n\n"
                             f"Do you want to download the file?", height=8, width=40 + len(file))

        if yesno == 'ok':
            self.d.infobox('Downloading please wait...', width=35, height=5)
            time.sleep(1)
            output = subprocess.call(f'wget --continue {link}', shell=True,
                                     stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

            if output > 0:
                self.d.msgbox(f"Downloading '{file}' {self.colors['red']}FAILED!{self.colors['restore']}",
                              height=7, width=50 + len(self.sbo_name))
            else:
                self.d.msgbox(f"Downloading file '{file}' finished!", height=7, width=40 + len(file))

    @staticmethod
    def version():
        """ Version info. """
        raise SystemExit(f'Version: {__version__}')

    @staticmethod
    def usage():
        """ Optional arguments. """
        args = (
            "Usage: sbo-create <sbo_name>\n\n"
            "Optional arguments:\n"
            "  -h, --help           Display this message and exit.\n"
            "  -v, --version        Show version and exit."
        )

        raise SystemExit(args)

    def about(self):
        """ About the sbo-create tool. """
        self.width = 70
        self.height = 15

        self.msg = (f"{' ' * int(self.width / 3.5)}{self.colors['green']}{self.colors['bold']} "
                    f"SlackBuild Create Tool{self.colors['restore']}\n\n"
                    "A tool that creates easy, fast and safe SlackBuilds files scripts.\n"
                    f"Version: {__version__}\n\n"
                    f"Homepage: {self.colors['blue']}https://gitlab.com/dslackw/sbo-create{self.colors['restore']}\n"
                    "Copyright © 2022 Dimitris Zlatanidis\n"
                    "Email: dslackw@gmail.com\n\n"
                    "Slackware ® is a Registered Trademark of Patrick Volkerding.\n"
                    "Linux is a Registered Trademark of Linus Torvalds.")

        self.message_box()
        self.menu()

    @staticmethod
    def exit():
        os.system('clear')
        raise SystemExit(0)
