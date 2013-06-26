#-*- coding: utf-8 -*-
'''
File: filehipporepo.py
Author: Michał "NeoXant" Kolarczyk
License: GNU GPL version 3 (see LICENSE file)

FileHippoRepo class for NXSC.

Code passes PEP8 guidlines (pep8.py agreed with that)
'''

from urllib.parse import urljoin
from functools import partial
import hashlib
from datetime import datetime
import os
import sys
import re
import subprocess
import textwrap
import requests
from bs4 import BeautifulSoup
#import colorama
import yaml
import progressbar
import hurry.filesize  # @UnresolvedImport


class FileHippoRepo(object):
    '''
    Class that provides methods to deal with the filehippo.com.
    '''

    def __init__(self, arch, beta=False):
        '''
        arch: architecure of operating system
        force32: forced installation of 32-bit version on 64-bit OS
        beta: search, upgrade or install beta versions
        '''
        #colorama.init()
        self.downloaded_apps = {}
        self.arch = arch
        self.beta = beta
        self.installed_db = {}
        print('==> Getting info about console window width...')
        try:
            path = os.path.join(os.getenv('windir'), 'system32', 'mode.com')
            proc = subprocess.Popen(path + ' con', stdout=subprocess.PIPE)
            while proc.poll() is None:
                line = proc.stdout.readline()
                if line and line != b'\r\n':
                    if line.split()[0] == b'Columns:':
                        self.con_width = int(line.split()[1])
                        break
        except:
            self.con_width = 80
        print('==> Getting info about installed apps...')
        self.appdata_dir = os.path.join(
            os.getenv('appdata'), 'NeoXant', 'NXSC')
        self.setup_files_dir = os.path.join(self.appdata_dir, 'setup_files')
        self.installed_yaml_file = os.path.join(
            self.appdata_dir, 'installed.yaml')
        if not os.path.exists(self.appdata_dir):
            os.makedirs(self.appdata_dir)
        if not os.path.exists(self.setup_files_dir):
            os.makedirs(self.setup_files_dir)
        try:
            self.installed_db_file = open(self.installed_yaml_file,
                encoding='utf-8')
        except:
            self.installed_db_file = open(self.installed_yaml_file, mode='a',
                encoding='utf-8')
            self.installed_db_file.close()
            self.installed_db_file = open(self.installed_yaml_file,
                encoding='utf-8')
        finally:
            self.installed_db = yaml.load(self.installed_db_file)
            self.installed_db_file.close()
        if self.installed_db == None:
            self.installed_db = {}
        self.base_url = 'http://filehippo.com'
        self.app_url = urljoin(self.base_url, 'download_')
        print('==> Getting status of repositories...')
        r = requests.get(self.base_url)
        if r.status_code == '404':
            print('!!ERROR!! ==> FileHippo in unavailable. Aborting!')
            exit(1)

    def search(self, phrase):
        print('==> Searching...')
        page = 1
        while True:
            r = requests.get(
                '{}/search?q={}&p={}'.format(
                    self.base_url, ' '.join(phrase), page),
                allow_redirects=False,
                cookies={'Filter': 'NOBETA=1'})
            if r.status_code == 302:
                break
            if r.status_code == 200:
                search_page = BeautifulSoup(r.content)
                for finded in search_page.select('.searchmiddle table'):
                    s_name = finded.select('td a')[0]['href'][10:-1]
                    f_name_temp = finded.select(
                        'td h2 a')[0].get_text()
                    to_delete = []
                    to_delete += re.findall('\d*\.\S*', f_name_temp)
                    f_name_list = f_name_temp.split()
                    if 'Build' in f_name_list:
                        del f_name_list[f_name_list.index('Build'):]
                    if 'build' in f_name_list:
                        del f_name_list[f_name_list.index('build'):]
                    for item in to_delete:
                        try:
                            f_name_list.remove(item)
                        except:
                            pass
                    f_name = ' '.join(f_name_list)
                    desc = finded.select('td div')[0].get_text()
                    try:
                        print('\nfilehippo/{} | {}\n    {}'.format(
                            s_name, f_name,
                            textwrap.fill(desc, self.con_width - 5)))
                    except UnicodeEncodeError:
                        desc = desc.encode('utf-8').decode(sys.stdout.encoding)
                        print('\nfilehippo/{} | {}\n    {}'.format(
                            s_name, f_name,
                            textwrap.fill(desc, self.con_width - 5)))
            page = page + 1

    def show(self, app):
        print('==> Getting info... It may take a while. Please be patient\n')
        info = self.get_info(app,
            ['preety_name', 'author', 'license', 'version', 'description'])
        if 'error' in info:
            print("!!ERROR!! ==> Wrong app name! Aborting!")
            return
        print('Name: {}\n\n'
               'Author: {}\n\n'
               'License: {}\n\n'
               'Current version: {}\n\n'
               'Description:\n{}'.format(
             info['preety_name'], info['author'], info['license'],
             info['version'],
             textwrap.fill(info['description'], self.con_width,
                replace_whitespace=False)))

    def download(self, apps, upgrade=False):
        print('==> Downloading...\n')
        for app in apps:
            if upgrade:
                if self.installed_db[app]['beta']:
                    self.beta = True
            if (not upgrade and app in self.installed_db and
                'new verion' in self.installed_db[app]):
                print(
                    '{} - for upgrade this app, use "upgrade" command!'.format(
                    app))
                continue
            info = self.get_info(app,
                ['version', 'publish_date', 'download_link'])
            if 'error' in info:
                print('{}: Error! App not exist!'.format(app))
                continue
            app_setup_f_name = info['download_link'].split('/')[-1]
            if not os.path.exists(os.path.join(
                self.setup_files_dir, app_setup_f_name)):
                dl_r = requests.get(info['download_link'], stream=True)
                size = int(dl_r.headers['Content-Length'].strip())
                b_bytes = 0
                prg_widgets = ['{:20} '.format(app),
                               '{:5} '.format(hurry.filesize.size(size)),
                               progressbar.FileTransferSpeed(),
                               ' ',
                               progressbar.AdaptiveETA(),
                               progressbar.Bar(marker='#',
                                    left=' [', right='] '),
                               progressbar.Percentage()]
                pbar = progressbar.ProgressBar(
                    widgets=prg_widgets, maxval=size).start()
                with open(os.path.join(
                    self.setup_files_dir, app_setup_f_name), 'wb') as f:
                    for chunk in dl_r.iter_content(10240):
                        b_bytes += len(chunk)
                        f.write(chunk)
                        pbar.update(b_bytes)
                pbar.finish()
            self.downloaded_apps[app] = [app_setup_f_name, info['version'],
                info['publish_date']]

    def install(self, upgrade=False):
        if len(self.downloaded_apps) == 0:
            return
        if not upgrade:
            print('\n==> Installing...\n')
        else:
            print('\n==> Upgrading...\n')
        for key in self.downloaded_apps.keys():
            if self.downloaded_apps[key][0].split('.')[-1] in ['exe', 'msi']:
                print('{} {}...'.format(key, self.downloaded_apps[key][1]))
                if self.downloaded_apps[key][0].split('.')[-1] == 'msi':
                    subprocess.call(os.path.join(
                        self.setup_files_dir, self.downloaded_apps[key][0]),
                        shell=True)
                else:
                    subprocess.call(os.path.join(
                        self.setup_files_dir, self.downloaded_apps[key][0]))
            elif self.downloaded_apps[key][0].split('.')[-1] == 'zip':
                print('{} {} - ZIP archive, opening...'.format(
                    key, self.downloaded_apps[key][1]))
                subprocess.call('{} {}'.format('explorer.exe',
                    os.path.join(self.setup_files_dir,
                    self.downloaded_apps[key][0])))
            options = {}
            options['version'] = self.downloaded_apps[key][1]
            if upgrade:
                options['beta'] = self.installed_db[key]['beta']
            else:
                if self.beta:
                    options['beta'] = True
                else:
                    options['beta'] = False
            options['filename'] = self.downloaded_apps[key][0]
            with open(
                os.path.join(self.setup_files_dir, options['filename']),
                    mode='rb') as f:
                md5 = hashlib.md5()
                for buf in iter(partial(f.read, 8192), b''):
                    md5.update(buf)
                options['md5'] = md5.hexdigest()
            if upgrade:
                options['built-in update'] = self.installed_db[key][
                                                'built-in update']
            else:
                options['built-in update'] = False
            options['publish date'] = self.downloaded_apps[key][2]
            self.installed_db[key] = options
            with open(
                self.installed_yaml_file, mode='w', encoding='utf-8') as f:
                yaml.dump(self.installed_db, f, indent=4,
                          default_flow_style=False)
        if not upgrade:
            print(textwrap.fill(
                    'If you know that some apps have built-in update '
                    'function, please edit file installed.yaml.',
                    self.con_width))

    def get_info(self, app, infos):
        response = {}
        fh_cookies = {}
        if self.beta:
            fh_cookies = {'Filter': 'NOBETA=0'}
        else:
            fh_cookies = {'Filter': 'NOBETA=1'}
        r = requests.get(self.app_url + app, cookies=fh_cookies)
        if r.status_code == 404:
            response['error'] = True
            return response
        page = BeautifulSoup(r.content)
        for info in infos:
            if info in ['preety_name', 'version']:
                name_temp = page.select('span[itemprop="name"]')[0].get_text()
                to_delete = []
                to_delete += re.findall('\d*\.\S*', name_temp)
                to_delete += re.findall('[bB]uild \w*', name_temp)
                if info == 'version':
                    response['version'] = ' '.join(to_delete)
                    continue
                else:
                    name_list = name_temp.split()
                    if 'Build' in name_list:
                        del name_list[name_list.index('Build'):]
                    if 'build' in name_list:
                        del name_list[name_list.index('build'):]
                    for item in to_delete:
                        try:
                            name_list.remove(item)
                        except:
                            pass
                    response['preety_name'] = ' '.join(name_list)
            elif info == 'description':
                response['description'] = page.select(
                    'span[itemprop="description]')[0].get_text()
            elif info == 'author':
                response['author'] = page.select(
                    '#progdesc table td em a')[0].get_text()
            elif info == 'license':
                license_temp = page.select(
                    '#progdesc table td em')[0].get_text()
                response['license'] = license_temp[
                    license_temp.index('(') + 1:license_temp.index(')')]
            elif info == 'publish_date':
                response['publish_date'] = datetime.strptime(page.find(
                "meta",
                attrs={'itemprop': 'datePublished'})['content'], '%Y-%m-%d')
            elif info == 'download_link':
                dl_page_link = page.select('#dlbox a')[0]['href']
                dl_page_link_r = requests.get(self.base_url + dl_page_link)
                page_dl = BeautifulSoup(dl_page_link_r.content)
                app_dl_link = page_dl.find(
                    "meta", attrs={
                        'http-equiv': 'Refresh'})['content'].split('; ')[1][4:]
                app_dl_link_r = requests.head(self.base_url + app_dl_link,
                    allow_redirects=False)
                response['download_link'] = app_dl_link_r.headers['location']
        return response

    def update(self):
        print('==> Available updates:')
        for app in self.installed_db.keys():
            if self.installed_db[app]['beta']:
                self.beta = True
            info = self.get_info(app, ['publish_date', 'version'])
            if (info['publish_date'] > self.installed_db[app]['publish date']
                and info['version'] != self.installed_db[app]['version']):
                self.installed_db[app]['new version'] = info['version']
                print('{} {} -> {}'.format(
                    app, self.installed_db[app]['version'],
                    info['version']))
            with open(
            self.installed_yaml_file, mode='w', encoding='utf-8') as f:
                yaml.dump(self.installed_db, f, indent=4,
                      default_flow_style=False)

    def upgrade(self, apps):
        if apps:
            for app in apps:
                if app in self.installed_db:
                    if not 'new version' in self.installed_db[app]:
                        print('{} - this app is not marked to upgrade!'.format(
                            app))
                        apps.remove(app)
                else:
                    print('{} - use "install" command to install this app!')
                    apps.remove(app)
                    continue
            if len(apps) > 0:
                self.download(apps, True)
                self.install(True)
            else:
                return
        else:
            apps_to_install = []
            apps = [[app, 'new version' in self.installed_db[app]]
                    for app in self.installed_db]
            for app in apps:
                if app[1]:
                    apps_to_install.append(app[0])
            self.download(apps_to_install, True)
            self.install(True)
