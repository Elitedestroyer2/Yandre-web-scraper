import os
import urllib

def download_pictures(self, file_count, stop_amount, folder_path):
    self.file_count = file_count
    self.stop_amount = stop_amount
    self.folder_path = folder_path
    thumbnail_links = self.pageManager.getPage_thumbnails(self.character.url)
    for thumbnail_link in thumbnail_links:
        # if at end amount, stop
        if self.file_count == self.stop_amount:
            break
        # grab page elements for all thumbnail pictures
        thumbnail_links = self.pageManager.getPage_thumbnails(self.character.url)
        # links to full pictures
        href_element = thumbnail_link['href']
        download_link, safeRating = self.pageManager.getpage_download_and_saferating(
            href_element)
        if self.character.lewd or self.character.wholesome:
            wholesome, lewd = self.filterManager.ratingCheck(safeRating)
            if self.character.wholesome and wholesome:
                self.download(download_link)
            elif self.character.lewd and lewd:
                self.download(download_link)
            else:
                # go to the next iteration
                pass
        else:
            self.download(download_link)


def download(self, download_link):

    fullfilename = os.path.join(
        self.folder_path, str(self.file_count) + '.jpg')
    urllib.request.urlretrieve(download_link, fullfilename)
    if self.character.duplicate:
        #TODO check for duplicate
            self.file_count += 1
    else:
        self.file_count += 1


def checkForDuplicate():
    pass

    # TODO implament