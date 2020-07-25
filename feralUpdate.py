#!/usr/bin/python3

import urllib.request
import requests
import shutil
import configparser
import io
import os
import sys
import subprocess


def start_game():
    subprocess.call(["/usr/share/playonlinux/playonlinux", "--run", "Fer.al"])


config = configparser.ConfigParser()
config['version'] = {'latestVersionEndpoint': "none"}
config.read('config.ini')
version_check_url = config['version']['latestVersionEndpoint']

launcher = configparser.ConfigParser()
launcher['version'] = {'currentVersion': 'none'}
launcher.read('game.ini')
current_game_ver = launcher['version']['currentVersion']

if version_check_url == "none":
    print("Missing version endpoint url in the config.ini!!!")
    exit(1)

print("Checking the latest version...")
version_check = urllib.request.urlopen(version_check_url)
version_check_raw = version_check.read()
version_check_data = "[root]\n" + version_check_raw.decode('utf-8')

config = configparser.ConfigParser(allow_no_value = True)
config.read_file(io.StringIO(version_check_data))

latest_game_ver = config["root"]["ApplicationVersion"]

if os.path.isdir("build") and latest_game_ver == current_game_ver:
    print("Game is up to date!")
    start_game()
    exit(0)

print("New version found: %s" % latest_game_ver)
print("-----------------")
print("Downloading an update...")

download_package_url = config["root"]["ApplicationDownloadUrl"]

file_name = "game_build.7z"

if os.path.exists(file_name):
    os.remove(file_name)

with open(file_name, "wb") as f:
    print("Downloading %s" % file_name)
    response = requests.get(download_package_url, stream=True)
    total_length = response.headers.get('content-length')

    if total_length is None:  # no content length header
        f.write(response.content)
    else:
        dl = 0
        total_length = int(total_length)
        for data in response.iter_content(chunk_size=4096):
            dl += len(data)
            f.write(data)
            done = int(50 * dl / total_length)
            sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50 - done)))
            sys.stdout.flush()

if os.path.isdir("build"):
    os.rename("build", "build-old")

print("Extracting...")
os.system('7z x %s' % file_name)

launcher['version']['currentVersion'] = latest_game_ver
with open('game.ini', 'w') as configfile:
    launcher.write(configfile)

print("Removing backups...")
shutil.rmtree('build-old', ignore_errors=True)
if os.path.exists(file_name):
    os.remove(file_name)

print("-----------------")
print("Update complete!")
start_game()

