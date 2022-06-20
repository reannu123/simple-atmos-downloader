import requests
import zipfile
import os
from tqdm import tqdm
import shutil

if os.path.exists('download'):
    # Delete the folder and its contents
    
    shutil.rmtree('download')
    os.makedirs('download')

def dl_file(filename:str, url:str="")->bool:
    r = requests.get(url, stream=True, allow_redirects=True)
    total_size = int(r.headers.get('content-length'))
    initial_pos = 0
    with open(filename,'wb') as f: 
        with tqdm(total=total_size, unit="B",unit_scale=True,desc=filename,initial=initial_pos, ascii=True) as pbar:
            for ch in r.iter_content(chunk_size=1024):                            
                    if ch:
                        f.write(ch) 
                        pbar.update(len(ch))                                # Return False if the file was not downloaded successfully                                       # Return False if the file was not downloaded successfully




print("Downloading Atmosphere...")
isDlAtmos = True
if isDlAtmos:
    # Atmosphere Downloader
    url = 'https://api.github.com/repos/Atmosphere-NX/Atmosphere/releases/latest'
    response = requests.get(url)

    # Raise an exception if the API call fails.
    response.raise_for_status()

    data = response.json()
    for asset in data['assets']:
        if asset['name'].endswith('.zip'):
            dl_file(asset['name'], asset['browser_download_url'])
            print(asset['browser_download_url'])
            zipfile.ZipFile(asset['name']).extractall("download")

            # Delete the zip file
            os.remove(asset['name'])
            print()
            break

print("Downloading Hekate...")
isDlHekate = True
if isDlHekate:
    # hekate downloader
    url = 'https://api.github.com/repos/CTCaer/hekate/releases/latest'
    response = requests.get(url)

    # Raise an exception if the API call fails.
    response.raise_for_status()

    data = response.json()
    for asset in data['assets']:
        if asset['name'].endswith('.zip'):
            dl_file(asset['name'], asset['browser_download_url'])
            print(asset['browser_download_url'])
            zipfile.ZipFile(asset['name']).extractall("download")
            # If payload.bin exists, delete it
            if os.path.exists("download/payload.bin"):
                os.remove("download/payload.bin")
            # Rename all binary files to payload.bin
            for file in os.listdir("download"):
                if file.endswith(".bin"):
                    os.rename(f"download/{file}", f"download/payload.bin")

            # Delete the zip file
            os.remove(asset['name'])
            print()
            break

print("Downloading Patches...")
isDlPatches = True
if isDlPatches:
    # Patches downloader
    url = 'https://api.github.com/repos/ITotalJustice/patches/releases/latest'
    response = requests.get(url)

    # Raise an exception if the API call fails.
    response.raise_for_status()

    data = response.json()
    for asset in data['assets']:
        if asset['name'].endswith('.zip'):
            dl_file(asset['name'], asset['browser_download_url'])
            print(asset['browser_download_url'])
            zipfile.ZipFile(asset['name']).extractall("download")

            # Delete the zip file
            os.remove(asset['name'])
            print()
            break



print("Download firmware? (y/n)")
isDlFirmware = input()

if isDlFirmware == "y":
    # Firmware downloader
    print("What version? (e.g. 1.0.0) Leave blank if latest")
    version = input()
    # if version is empty, use the latest version
    if version == "":
        version = "14.1.2"
    print("Downloading firmware " + version)
    url = f"https://archive.org/download/nintendo-switch-global-firmwares/Firmware%20{version}.zip"
    file = "firmware.zip"
    if os.path.exists('download/firmware'):
        # Delete the firmware folder
        os.rmdir('download/firmware')
        os.makedirs('download/firmware')
    dl_file(file, url)
    
    zipfile.ZipFile(file).extractall("download/firmware")
