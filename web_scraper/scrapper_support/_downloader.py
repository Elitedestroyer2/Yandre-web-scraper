import os
import urllib


def download_pictures(self):
    thumbnail_links = self.getPage_thumbnails(self.character)
    for thumbnail_link in thumbnail_links:
        # if at end amount, stop
        if self.fileCount == self.stopAmount:
            break
        # grab page elements for all thumbnail pictures
        thumbnail_links = self.getPage_thumbnails(self.character)
        # links to full pictures
        href_element = thumbnail_link['href']
        download_link, safeRating = self.getpage_download_and_saferating(
            href_element)
        if self.lewdFilter or self.wholesomeFilter:
            wholesome, lewd = self.ratingCheck(safeRating)
            if self.wholesomeFilter and wholesome:
                self.download(download_link)
            elif self.lewdFilter and lewd:
                self.download(download_link)
            else:
                # go to the next iteration
                pass
        else:
            self.download(download_link)


def download(self, download_link):

    fullfilename = os.path.join(
        self.folderPath, str(self.fileCount) + '.jpg')
    urllib.request.urlretrieve(download_link, fullfilename)
    if self.duplicateFilter:
        if not (checkForDuplicate(self.fileCount)):
            self.fileCount = self.get_current_file_count()
    else:
        self.fileCount = self.get_current_file_count()
