#  Copyright (c)

#
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
import os
import shutil
import tempfile
import time
from sys import stdout

import tomlkit
from selenium.common.exceptions import NoSuchElementException

from selenium import webdriver
from selenium.webdriver.common.by import By


def get_invoices(username, password, destination, timeout):

    with tempfile.TemporaryDirectory() as download_tempdir:
        ...

        options = webdriver.FirefoxOptions()
        options.set_preference("browser.download.folderList", 2)
        # options.set_preference("browser.download.panel.shown", False)
        options.set_preference("browser.download.manager.showWhenStarting", False)
        options.set_preference("browser.download.dir", download_tempdir)
        options.set_preference("browser.preferences.instantApply", True)
        options.set_preference("browser.download.manager.showWhenStarting", False)
        options.set_preference("browser.download.manager.showAlertOnComplete", False)
        # Example:options.set_preference("browser.download.dir", "C:\Tutorial\down")
        options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/download")

        driver = webdriver.Firefox(options=options)

        driver.get('http://magh2:3101/emagh2/')

        # driver.find_element_by_id('xluser').send_keys(username)
        # driver.find_element_by_id('xlpwd').send_keys(password)
        # driver.find_element_by_id('bConfirmer').click()

        time.sleep(1)
        # print(driver.page_source)
        # print(driver.window_handles)

        # Switch to login window
        magh2_window_handle = driver.window_handles[0]
        driver.switch_to.window(magh2_window_handle)
        time.sleep(1)

        driver.find_element(by=By.ID, value='xluser').send_keys(username)
        driver.find_element(by=By.ID, value='xlpwd').send_keys(password)
        time.sleep(1)

        driver.find_element(by=By.ID, value='bConfirmer').click()
        time.sleep(1)

        driver.find_element(by=By.ID, value='bConfirmer').click()
        # print(driver.page_source)
        time.sleep(1)
        command_field = None
        n = 1
        print(f"Connexion MAGH2 avec le login '{username}'", end='')
        while command_field is None:
            try:
                command_field = driver.find_element(by=By.ID, value='XLCOMMAND')
            except NoSuchElementException:
                pass
            time.sleep(1)
            print(".", end='')
            stdout.flush()
            n += 1
            if n > timeout:
                print("\nDélai Connexion MAGH2 dépassé !")
                driver.quit()
                exit(1)

        print("\nConnexion MAGH2 OK.")

        command_field.send_keys('RFAC')
        driver.find_element(by=By.ID, value='bOk').click()

        for i in range(timeout):
            handles: list = driver.window_handles
            handles.remove(magh2_window_handle)
            if handles:
                break
            time.sleep(1)

        driver.switch_to.window(handles[0])
        print("Connexion Prodige OK.")

        for i in range(timeout):
            iframes = driver.find_elements(by=By.CSS_SELECTOR, value='iframe.gwt-Frame.pgih-EK.pgih-DK')
            # print(i, iframes)
            time.sleep(1)
            if iframes:
                break

        driver.switch_to.frame(iframes[0])
        print("Page Prodige affichée.")

        for i in range(timeout):
            export_button = driver.find_elements(by=By.CSS_SELECTOR, value='.EXPORTER > div:nth-child(1) > img:nth-child(1)')
            # print(i, export_button)
            time.sleep(1)
            if export_button:
                break

        export_button[0].click()
        print("Lancement de l'export...", end='')

        done = False
        n = 0
        prev_size = -1
        while not done:
            ld = os.listdir(download_tempdir)
            if ld:
                # print(ld)
                print(".", end='')
                stdout.flush()
                nsize = os.stat(download_tempdir + '/' + ld[0]).st_size
                if nsize > 0 and nsize == prev_size and os.stat(download_tempdir + '/' + ld[0]).st_mtime < time.time() - 2:
                    done = True
                    shutil.copy(download_tempdir + '/' + ld[0], destination)
                prev_size = nsize

            time.sleep(1)
            n += 1
            if n > timeout:
                print("\nDélai attente téléchargement dépassé !")
                driver.quit()
                exit(2)

        # time.sleep(1000)
        # print(driver.page_source)
        driver.quit()
        print("\nTerminé.")


if __name__ == '__main__':
    with open('instance_config.toml') as fp:
        config = tomlkit.load(fp)
    get_invoices(
        config['invoices_grab']['login'],
        config['invoices_grab']['password'],
        config['invoices_grab']['destination'],
        config['invoices_grab'].get('timeout', 500),
    )
