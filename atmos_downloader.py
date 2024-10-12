import requests
import zipfile
import os
from tqdm import tqdm
import shutil
from bs4 import BeautifulSoup

directory = "copy_to_sd"

def get_latest_firmware_version():
    url = 'https://yls8.mtheall.com/ninupdates/reports.php'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the table
    table = soup.find('table')

    # Get all rows in the table
    rows = table.find_all('tr')

    # Reverse the list of rows
    rows.reverse()

    # Iterate over the rows
    for row in rows:
        # Get all cells in the row
        cells = row.find_all('td')

        # Iterate over the cells
        for i, cell in enumerate(cells):
            # If the cell contains the text "Switch"
            if 'Switch' in cell.text:
                # Get the previous cell
                previous_cell = cells[i - 1]

                # Return the text in the previous cell
                return previous_cell.text


if os.path.exists(directory):
    # Delete the folder and its contents
    
    shutil.rmtree(directory)
    os.makedirs(directory)

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
            zipfile.ZipFile(asset['name']).extractall(directory)

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
            zipfile.ZipFile(asset['name']).extractall(directory)
            # If payload.bin exists, delete it
            if os.path.exists(f"{directory}/payload.bin"):
                os.remove(f"{directory}/payload.bin")
            # Rename all binary files to payload.bin
            for file in os.listdir(directory):
                if file.endswith(".bin"):
                    os.rename(f"{directory}/{file}", f"{directory}/payload.bin")

            # Delete the zip file
            os.remove(asset['name'])
            print()
            break

print("Downloading Patches...")
isDlPatches = True
if isDlPatches:
    # Patches downloader
    url = 'https://sigmapatches.coomer.party/sigpatches.zip'
    
    response = requests.get(url)
    dl_file('sigpatches.zip', url)
    print(url)
    zipfile.ZipFile('sigpatches.zip').extractall(directory)
    # Delete the zip file
    os.remove("sigpatches.zip")
    print()



print("Download firmware? (y/n)")
isDlFirmware = input()

if isDlFirmware == "y":
    # Firmware downloader
    print("What version? (e.g. 1.0.0) Leave blank if latest")
    version = input()
    # if version is empty, use the latest version
    if version == "":
        version = get_latest_firmware_version()
    print("Downloading firmware " + version)
    url = f'https://api.github.com/repos/THZoria/NX_Firmware/releases/tags/{version}'
    response = requests.get(url)

    # Raise an exception if the API call fails.
    response.raise_for_status()

    data = response.json()
    for asset in data['assets']:
        if asset['name'].endswith('.zip'):
            if os.path.exists(f'{directory}/firmware'):
                # Delete the firmware folder
                os.rmdir(f'{directory}/firmware')
                os.makedirs(f'{directory}/firmware')
            dl_file(asset['name'], asset['browser_download_url'])
            zipfile.ZipFile(asset['name']).extractall(f"{directory}/firmware")
            print()
            break



    