import urequests
import os
import gc
import json
#import micropython

VERSION = "1.0"

class OTAUpdater:
    """ This class handles OTA updates. It connects to the Wi-Fi, checks for updates, downloads and installs them."""
    def __init__(self, repo_url, filename):
        self.filename = filename
        self.repo_url = repo_url
        self.version_file = filename + '_' + 'ver.json'

        # self.version_url = repo_url + 'main/version.json'                 # Replacement of the version mechanism by Github's oid
        self.version_url = self.process_version_url(repo_url, filename)     # Process the new version url
        self.firmware_url = repo_url + filename                             # Removal of the 'main' branch to allow different sources

        print("Version URL is ", self.version_url)
        print("Firmware URL is ", self.firmware_url)

        # get the current version (stored in version.json)
        if self.version_file in os.listdir():
            with open(self.version_file) as f:
                self.current_version = json.load(f)['version']
            version_message = "Current " + self.filename + " is " + self.current_version
            print("version message ", version_message)

        else:
            print("No version file")
            self.current_version = "0"
            # save the current version
            with open(self.version_file, 'w') as f:
                json.dump({'version': self.current_version}, f)
            
    def process_version_url(self, repo_url, filename):
        """ Convert the file's url to its assoicatied version based on Github's oid management."""

        # Necessary URL manipulations
        version_url = repo_url.replace("raw.githubusercontent.com", "github.com")  # Change the domain
        version_url = version_url.replace("/", "§", 4)                             # Temporary change for upcoming replace
        version_url = version_url.replace("/", "/latest-commit/", 1)                # Replacing for latest commit
        version_url = version_url.replace("§", "/", 4)                             # Rollback Temporary change
        version_url = version_url + filename                                       # Add the targeted filename
        
        return version_url
        
    def fetch_latest_code(self)->bool:
        """ Fetch the latest code from the repo, returns False if not found."""
        
        # Fetch the latest code from the repo.
        response = urequests.get(self.firmware_url, timeout=20)
        if response.status_code == 200:
            gc.collect()
            try:
                # Save the fetched code to memory
                self.latest_code = response.text
                return True
            except Exception as e:
                print('Failed to fetch latest code:', e)
                return False
        
        elif response.status_code == 404:
            print('Firmware not found.')
            return False

    def update_no_reset(self):
        """ Update the code without resetting the device."""

        # Save the fetched code and update the version file to latest version.
        with open('latest_code.py', 'w') as f:
            f.write(self.latest_code)
        
        # update the version in memory
        self.current_version = self.latest_version

        # save the current version
        with open(self.version_file, 'w') as f:
            json.dump({'version': self.current_version}, f)
        
        # free up some memory
        self.latest_code = None

        # Overwrite the old code.
        os.rename('latest_code.py', self.filename)
        
    def check_for_updates(self):
        """ Check if updates are available."""
        
        # Connect to Wi-Fi
        # self.connect_wifi()

        print('Checking for latest version...')
        gc.collect()
        headers = {"accept": "application/json"} 
#        micropython.mem_info(True)
#        print('send request')
        
        response = urequests.get(self.version_url, headers=headers, timeout=5)
        
#        print('load response')
        data = json.loads(response.text)
       
        self.latest_version = data['oid']                   # Access directly the id managed by GitHub
#        latest_version_message = "Latest " + self.filename + " version is: " + self.latest_version
#        print(latest_version_message)
        
        # compare versions
        newer_version_available = True if self.current_version != self.latest_version else False
        newer_version_message = "New ver: " + str(newer_version_available)
        print(newer_version_message)    
        return newer_version_available
    
    def download_and_install_update_if_available(self):
        """ Check for updates, download and install them."""
        
        if self.check_for_updates():
            return self.download_and_install_update()
        else:
            print('No new updates available.')
            return True

    def download_and_install_update(self):
        """ Check for updates, download and install them."""
        if self.fetch_latest_code():
            self.update_no_reset()
        else:
            return False
        return True
