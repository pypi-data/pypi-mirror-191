#!/usr/bin/env python
#_*_ coding: utf8 _*_

import shutil
from lxml import html
import requests
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import os
from subprocess import PIPE, run
import platform
from zipfile import ZipFile
import urllib.request

class UpdateChromedriver():

    def __init__(self, ruta_chromedriver):
        sistem_os,chrome_version = self.check_computer_and_google_version()
        self.comparar_chromedriver_version(sistem_os, chrome_version, ruta_chromedriver)

    def check_computer_and_google_version(self,):
        result = ''
        sistem_os = ''
        if platform.system() == 'Darwin':
            command = ['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome','--version']
            result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
            command2 = ['uname', '-m']
            result2 = run(command2, stdout=PIPE, stderr=PIPE, universal_newlines=True)
            if result2 == 'arm64':
                sistem_os = 'mac_arm64'
            else:
                sistem_os = 'mac64'
        elif platform.system() == 'Linux':
            command = ['google-chrome', '--version']
            result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
            sistem_os = 'linux64'
        chrome_version = str(result.stdout).split('Chrome ')[-1].split('.')[0]
        return sistem_os,chrome_version

    def descomprimir_archivo(self, ruta_y_nombre_zip,ruta_y_nombre_archivo):
        ZipFile(ruta_y_nombre_zip).extractall(ruta_y_nombre_archivo)

    def permisos_chromedriver(self, ruta_y_nombre_archivo):
        os.system(f'chmod 775 {ruta_y_nombre_archivo}')

    def descargar_archivo(self, link_descarga, ruta_chromedriver):
        ruta_y_nombre_zip = f'{ruta_chromedriver}chromedriver.zip'
        urllib.request.urlretrieve(link_descarga, ruta_y_nombre_zip)
        ruta_y_nombre_carpeta = f'{ruta_chromedriver}chromedriver_carpeta/'
        self.descomprimir_archivo(ruta_y_nombre_zip,ruta_y_nombre_carpeta)
        ruta_y_nombre_archivo = f'{ruta_chromedriver}chromedriver'
        shutil.move(f'{ruta_y_nombre_carpeta}chromedriver', ruta_y_nombre_archivo)
        os.remove(ruta_y_nombre_zip)
        shutil.rmtree(ruta_y_nombre_carpeta)
        self.permisos_chromedriver(ruta_y_nombre_archivo)
        return ruta_y_nombre_archivo

    def descargar_chromedriver(self, system_os, version, ruta_chromedriver):
        url = 'https://chromedriver.chromium.org/downloads'
        encabezados = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15'}
        session = requests.Session()
        web = session.get(url, headers=encabezados)
        parse = html.fromstring(web.content)
        descargas = parse.xpath('//*[@id="h.e02b498c978340a_87"]/div/div/ul[1]//a/@href')
        for ds in descargas:
            ch_version = ds.split('path=')[-1].split('.')[0]
            if str(version) == ch_version:
                version_extended = ds.split('path=')[-1].replace('/','')
                link_descarga = f'https://chromedriver.storage.googleapis.com/{version_extended}/chromedriver_{system_os}.zip'
                self.descargar_archivo(link_descarga, ruta_chromedriver)

    def comparar_chromedriver_version(self, sistem_os, chrome_version, ruta_chromedriver):
        list = os.listdir(ruta_chromedriver)
        file_info = 'chromedriver_version_info.txt'
        if file_info in list:
            with open(f'{ruta_chromedriver}{file_info}', 'r') as k:
                version_actual = k.read().strip()
            if version_actual != chrome_version:
                os.rename(f'{ruta_chromedriver}chromedriver', f'{ruta_chromedriver}chromedriver_{version_actual}')
                self.descargar_chromedriver(sistem_os, chrome_version, ruta_chromedriver)
                with open(f'{ruta_chromedriver}{file_info}', 'w') as k:
                    k.write(chrome_version)
                print(f'Se ha actualizado la versión {chrome_version} de chromedriver.')
            else:
                print(f'Versión {chrome_version} de chromedriver correcta.')
        else:
            if 'chromedriver' in list:
                os.rename(f'{ruta_chromedriver}chromedriver', f'{ruta_chromedriver}chromedriver_old')
            self.descargar_chromedriver(sistem_os, chrome_version, ruta_chromedriver)
            with open(f'{ruta_chromedriver}{file_info}', 'w') as k:
                k.write(chrome_version)
            print(f'Se ha descargado la versión {chrome_version} de chromedriver.')

