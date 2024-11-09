# Stolen from https://gist.github.com/XOYZ69/1cbda896d780d38146de0b6637f661c3
# modified to fix some things

# Imports
import requests
import json
import subprocess
import time
import sys
import zipfile
import shutil
import os

start_time = time.time()

# Variables
zig_version_json_url    = 'https://ziglang.org/download/index.json'
zig_version_json        = {}
zig_install_dir         = 'D:\\Software\\Zig\\'
zig_version_current     = ''
zig_version_master      = ''
zig_file_master         = ''
zig_build_version       = 'x86_64-windows'
zig_updater_log_file    = 'zig_updater.log'
zig_new_version_found   = False

# Getting the Version Json File
zig_version_json = json.loads(
    requests.get(zig_version_json_url).text
)

def log(content, end = '\n', progress_bar = False):
    message = time.ctime() + ': ' + str(content)
    print(message, end = end if not progress_bar else '\r')
    return message + end

with open(zig_install_dir + 'zig_updater.log', 'a', encoding = 'utf-8') as log_file:
    log_file.write(log('--------------------------------------------------------------------------------------'))
    log_file.write(log('Launching zig_updater....'))

    # Version Checking
    zig_version_master = zig_version_json['master']['version']
    log_file.write(log('Checking Master Version: ' + zig_version_master))
    zig_version_current = str(subprocess.run(['zig', 'version'], stdout = subprocess.PIPE).stdout.decode('UTF-8'))
    log_file.write(log('Checking System Version: ' + zig_version_current, ''))
    zig_new_version_found = zig_version_current < zig_version_master
    log_file.write(log('New Version Available?: ' + str(zig_new_version_found)))

    if not zig_new_version_found:
        if '-f' in sys.argv:
            log_file.write(log('Zig is up to date! Forcing re-install...'))
        else:
            sys.exit()
    
    zig_file_master = zig_version_json['master'][zig_build_version]['tarball']
    log_file.write(log('Master Link: ' + zig_file_master))
    zig_file_master = zig_file_master.split('/')[-1]

    log_file.write(log('Downloading new Zig version'))
    zig_response = requests.get(zig_version_json['master'][zig_build_version]['tarball'], stream=True)
    total_length = zig_response.headers.get('content-length')

    last_update = 0

    with open(zig_install_dir + zig_file_master, 'wb') as zig_master_zip:
        if total_length is None: # no content length header
            log_file.write(log(zig_response.content))
        else:
            dl = 0
            total_length = int(total_length)
            for data in zig_response.iter_content(chunk_size=4096):
                dl += len(data)
                zig_master_zip.write(data)
                done = int(100 * dl / total_length)
                # log_file.write(log("\r[%s%s]" % ('=' * done, ' ' * (50-done)) ))
                if done % 5 == 0 and done != last_update:
                    message = log('Downloading [' + zig_version_master + ']: ' + '{:>3}'.format(done) + ' %', progress_bar = True)
                    log_file.write(message)
                    last_update = done
    
    print('\n', end = '')
    if '-do' in sys.argv:
        log_file.write(log('Download Complete. Exiting...'))
        sys.exit()
    
    # Extract Zip
    log_file.write(log('Extracting zip [' + zig_install_dir + zig_file_master + '] to [' + zig_install_dir + ']'))
    with zipfile.ZipFile(zig_install_dir + zig_file_master, 'r') as zip_ref:
        zip_ref.extractall(zig_install_dir)
    
    log_file.write(log('Removing [' + zig_install_dir + zig_file_master + ']'))
    os.remove(zig_install_dir + zig_file_master)

    log_file.write(log('Removing bin dir [' + zig_install_dir + 'bin]'))
    shutil.rmtree(zig_install_dir + 'bin', ignore_errors=True)

    log_file.write(log('Copy new installation files to fresh bin folder'))
    log_file.write(log('   From: ' + zig_install_dir + zig_file_master.replace('.zip', '')))
    log_file.write(log('   To:   ' + zig_install_dir + 'bin'))
    shutil.copytree(
        zig_install_dir + zig_file_master.replace('.zip', ''),
        zig_install_dir + 'bin'
        )

    log_file.write(log('Removing downloaded folder [' + zig_install_dir + zig_file_master.replace('.zip', '')))
    shutil.rmtree(
        zig_install_dir + zig_file_master.replace('.zip', '')
    )

    log_file.write(log('Finished zig_updater in: ' + str(round(time.time() - start_time, 2)) + 's'))