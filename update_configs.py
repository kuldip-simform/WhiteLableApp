#!/usr/bin/env python3
import json
import os
import shutil
import logging
import re
import argparse

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def read_json(app_folder):
    src_config_path = os.path.join(app_folder, 'config.json')
    logging.info(f'Reading JSON configuration from {src_config_path}')
    with open(src_config_path, 'r') as file:
        data = json.load(file)
    logging.info(f'Configuration data: {data}')
    return data

def update_ios_config(data):
    logging.info('Updating iOS configuration')
    
    # Update bundle ID
    os.system(f"plutil -replace CFBundleIdentifier -string {data['bundleId']} ios/WhiteLabelApp/Info.plist")
    logging.info('Updated iOS bundle ID')

    # Update app name
    os.system(f"plutil -replace CFBundleDisplayName -string \"{data['appName']}\" ios/WhiteLabelApp/Info.plist")
    logging.info('Updated iOS app name')

def update_android_config(data):
    logging.info('Updating Android configuration')
    
    # Update bundle ID
    os.system(f"sed -i '' 's/applicationId .*/applicationId \"{data['bundleId']}\"/' android/app/build.gradle")
    logging.info('Updated Android bundle ID')

    # Update app name in strings.xml
    strings_xml_path = 'android/app/src/main/res/values/strings.xml'
    with open(strings_xml_path, 'r') as file:
        strings_xml_content = file.read()
    new_app_name = data['appName']
    strings_xml_content = re.sub(r'(<string name="app_name">)[^<]*(</string>)', rf'\1{new_app_name}\2', strings_xml_content)
    with open(strings_xml_path, 'w') as file:
        file.write(strings_xml_content)
    logging.info('Updated app name in strings.xml')

def replace_colors_file(app_folder):
    logging.info('Replacing colors.ts file')
    src_colors_path = os.path.join(app_folder, 'colors.ts')
    dest_colors_path = 'src/config/colors.ts'
    
    shutil.copyfile(src_colors_path, dest_colors_path)
    
    logging.info(f'Replaced colors.ts with the file from {src_colors_path}')

def replace_strings_file(app_folder):
    logging.info('Replacing strings.ts file')
    src_strings_path = os.path.join(app_folder, 'strings.ts')
    dest_strings_path = 'src/config/strings.ts'
    
    shutil.copyfile(src_strings_path, dest_strings_path)
    
    logging.info(f'Replaced strings.ts with the file from {src_strings_path}')


def replace_ios_appicon_set(app_folder):
    logging.info('Replacing AppIcon.appiconset folder')
    src_appicon_path = os.path.join(app_folder, 'icons/ios/AppIcon.appiconset')
    dest_appicon_path = 'ios/WhiteLabelApp/Images.xcassets/AppIcon.appiconset'
    
    if os.path.exists(dest_appicon_path):
        shutil.rmtree(dest_appicon_path)
    
    shutil.copytree(src_appicon_path, dest_appicon_path)
    
    logging.info(f'Replaced AppIcon.appiconset with the folder from {src_appicon_path}')


def replace_android_app_icons(app_folder):
    logging.info('Replacing Android app icon folders')
    mipmap_folders = ['mipmap-hdpi', 'mipmap-mdpi', 'mipmap-xhdpi', 'mipmap-xxhdpi', 'mipmap-xxxhdpi']
    
    for folder in mipmap_folders:
        src_icon_path = os.path.join(app_folder, f'icons/android/{folder}')
        dest_icon_path = f'android/app/src/main/res/{folder}'
        
        if os.path.exists(dest_icon_path):
            shutil.rmtree(dest_icon_path)
        
        shutil.copytree(src_icon_path, dest_icon_path)
        
        logging.info(f'Replaced {folder} with the folder from {src_icon_path}')


def replace_appicon_set(app_folder):
    replace_ios_appicon_set(app_folder)
    replace_android_app_icons(app_folder)

def copy_env_file(app_folder, env):
    env_file = f'.env.{env}'
    src_env_path = os.path.join(app_folder, f'envs/{env_file}')
    dest_env_path = '.env'
    
    if not os.path.exists(src_env_path):
        raise ValueError(f'Environment file {src_env_path} does not exist')

    logging.info(f'Copying {src_env_path} to {dest_env_path}')
    shutil.copyfile(src_env_path, dest_env_path)
    logging.info(f'Copied {env_file} to project root as .env')


def replace_ios_splashscreen(app_folder):
    logging.info('Replacing Splash screen image')
    src_appicon_path = os.path.join(app_folder, 'icons/ios/SplashScreen.png')
    dest_appicon_path = 'ios/WhiteLabelApp/Images.xcassets/SplashScreen.imageset/SplashScreen.png'
    
    shutil.copyfile(src_appicon_path, dest_appicon_path)
    
    logging.info(f'Replaced Splash screen image with the image from {src_appicon_path}')

def main(app, config):
    app_folder = os.path.join('apps',app)
    data = read_json(app_folder)

    update_ios_config(data)
    update_android_config(data)
    replace_colors_file(app_folder)
    replace_strings_file(app_folder)
    replace_appicon_set(app_folder)
    copy_env_file(app_folder, config)
    replace_ios_splashscreen(app_folder)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Update app configurations.')
    parser.add_argument('--app', '-a', type=str, help='App name to update configurations for.')
    parser.add_argument('--config', '-c', type=str, help='Provide Env config name')
    args = parser.parse_args()

    if not args.app:
        args.app = input('Please enter the app name: ').strip()

    if not args.app:
        raise ValueError('App name cannot be empty')

    if not args.config:
        args.config = input('Please enter the enc config: ').strip()

    if not args.config:
        raise ValueError('Env config cannot be empty')

    main(args.app, args.config)

