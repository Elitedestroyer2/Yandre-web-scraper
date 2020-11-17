import requests
from bs4 import BeautifulSoup
import os
import urllib.request
import cv2
from database import charactermanager
from settings import settings


MAX_PICTURES = 60
MIN_PICTURES = 800
mainURL = "https://yande.re/"
myPath = 'CharactersForRec'


class scraper(object):

    def grab_pictures(self, lewdFilter, wholesomeFilter, duplicateFilter):
        self.MAINURL = "https://yande.re/"
        self.myPath = settings.read_settings()
        self.lewdFilter = self.toggleToBool(lewdFilter)
        self.wholesomeFilter = self.toggleToBool(wholesomeFilter)
        self.duplicateFilter = self.toggleToBool(duplicateFilter)

        #create connection to database
        self.conn = self.connect_to_database()

        self.pageCounter = 1
        self.characters = []

        #create character from character class
        characterName, characterAmount = self.grab_added_character_name()
        self.character = Character(characterName, self.fetch_character_url(characterName), characterAmount)
        self.url = f"https://yande.re/tag?name={self.character.name}&order=count&page={self.pageCounter}&type=4"

        #check if directory exsits for current character, if not, create one. Get folderPath
        self.folderPath = self.checkCharacterDir()
        #set fileCount
        self.get_current_file_count()
        #set amount of pictures to stop at
        self.stopAmount = characterAmount + self.fileCount
        #start downloading pictures
        self.download_pictures()

    def connect_to_database(self):
        conn = charactermanager.dbConnection()
        conn.connect()
        return conn

    def grab_added_character_name(self):
        return self.conn.grab_added_character()
        

    def fetch_character_url(self, characterName):
        return f'https://yande.re/post?page={self.pageCounter}&tags={characterName}'
    
    def checkCharacterDir(self):
        folderPath = self.myPath + "/" + self.character.name
        folderPath = folderPath.replace('_', ' ')
        isdir = os.path.isdir(folderPath)

        if not isdir:
            try:
                os.mkdir(folderPath)
                file_count = 0
            except:
                print("Failed to create directory %s" % folderPath)

        return folderPath
    
    def getPage_thumbnails(self, character):
        page = requests.get(character.url)
        pageContent = BeautifulSoup(page.content, 'html.parser')
        results = pageContent.find(id='post-list-posts')
        thumbnails = results.find_all('a', class_='thumb')
        return thumbnails

    def getpage_download_and_saferating(self, href_element):
        page = requests.get(self.MAINURL + href_element)
        soup = BeautifulSoup(page.content, 'html.parser')
        download_link = soup.find(id='highres').attrs['href']
        safeRating = soup.find(id='stats').contents[3].contents[9].contents[0]
        return download_link, safeRating
    
    def get_current_file_count(self):
        #Grab the number of files and add one to it so that the save does not overwrite the last file in the folder
        self.fileCount = len(next(os.walk(self.folderPath))[2]) + 1

    def ratingCheck(self, safeRating):
        #Will return states of Wholesome, and lewd, respectively 
        safeRating = safeRating.replace('Rating: ', '')
        safeRating = safeRating.replace(' ', '')
        if self.wholesomeFilter:
            if safeRating == 'Safe':
                return True, False
            else:
                return False, True
        if self.lewdFilter:
            if safeRating != 'Safe':
                return False, True
            else:
                return True, False


    def download_pictures(self):
        thumbnail_links = self.getPage_thumbnails(self.character)
        for thumbnail_link in thumbnail_links:
            #if at end amount, stop
            if self.fileCount == self.stopAmount:
                break
            #grab page elements for all thumbnail pictures
            thumbnail_links = self.getPage_thumbnails(self.character)
            for thumbnail_link in thumbnail_links:
                #links to full pictures
                href_element = thumbnail_link['href']
                download_link, safeRating = self.getpage_download_and_saferating(href_element)
                if self.lewdFilter or self.wholesomeFilter:
                    wholesome, lewd = self.ratingCheck(safeRating)
                    if self.wholesomeFilter and wholesome:
                        self.download(download_link)
                    elif self.lewdFilter and lewd:
                        self.download(download_link)
                    else:
                        #go to the next iteration
                        continue
                else:
                    self.download(download_link)

    def download(self, download_link):

        fullfilename = os.path.join(self.folderPath, str(self.fileCount) + '.jpg')
        urllib.request.urlretrieve(download_link, fullfilename)
        if self.duplicateFilter:
            if not (checkForDuplicate(self.file_count)):
                self.get_current_file_count()
        else:
            self.get_current_file_count()


                

    def unknown(self):
        #Grab characters name and urls for the minimum amount of pictures
        while not grabCharacter(url)[0]:
            tempCharacters = grabCharacter(url)[1]
            for char in tempCharacters:
                characters.append(char)
            pageCounter += 1
            url = f"https://yande.re/tag?name=&order=count&page={pageCounter}&type=4" 
        for character in characters:
            previous_page = 1
            url_page = 1
            job_elems, file_count, folderPath = getPage(character)

            while file_count <= MAX_PICTURES:
                previous_page = url_page
                url_page += 1
                character.url = character.url.replace(str(previous_page), str(url_page))
                job_elems = getPage(character)[0]

                for job_elem in job_elems:
                    href_elem = job_elem.attrs['href']
                    temp_url = mainURL + href_elem

                    page = requests.get(temp_url)

                    soup = BeautifulSoup(page.content, 'html.parser')
                    results = soup.find(id='highres')
                    down_link = results.attrs['href']
                    results = soup.find(id='stats')
                    #Grab 'safe' rating
                    safeRating = results.contents[3].contents[9].contents[0]
                    if filtersOn:
                        Islewd, Iswholesome = filterChecks(safeRating)
                        if self.toggleToBool(lewdFilter):
                            if Islewd:
                                pass
                            else:
                                continue
                        elif self.toggleToBool(wholesomeFilter):
                            if Iswholesome:
                                pass
                            else:
                                continue
                    else:
                        pass

                    fullfilename = os.path.join(folderPath, str(file_count) + '.jpg')
                    urllib.request.urlretrieve(down_link, fullfilename)
                    if self.toggleToBool(duplicateFilter):
                        duplicated = checkForDuplicate(file_count)
                    else:
                        duplicated = False
                    if not duplicated:
                        file_count = len(next(os.walk(folderPath))[2]) + 1
                    if file_count > MAX_PICTURES:
                        break

    def toggleToBool(self, toggleString):
        if toggleString == 'down':
            toggle = True
        else:
            toggle = False
        return toggle


    def filterChecks(safeRating):
        isSafe = 'Safe' in safeRating
        if not isSafe:
            Lewd = True
            Wholesome = False
        else:
            Lewd = False
            Wholesome = True
        return Lewd, Wholesome

    def checkForDuplicate(file_count):
        file_check_count = 1
        while file_check_count != file_count:

            original = cv2.imread(folderPath + '/' + str(file_check_count) + '.jpg')
            duplicate = cv2.imread(folderPath + '/' +  str(file_count) + '.jpg')

            if original.shape == duplicate.shape:
                difference = cv2.subtract(original, duplicate)
                b, g, r = cv2.split(difference)
                if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0:
                    os.remove(folderPath + '/' + str(file_count) + '.jpg')
                    return True
            file_check_count += 1

    def getPage1(character):
        page = requests.get(character.url)
        folderPath = myPath + "/" + character.name
        folderPath = folderPath.replace('_', ' ')
        isdir = os.path.isdir(folderPath)

        if not isdir:
            try:
                os.mkdir(folderPath)
                file_count = 0
            except:
                print("Failed to create directory %s" % folderPath)
            else:
                print("Successfully created the directory %s" % folderPath)

        elif isdir:
            #Grab the number of files and add one to it so that the save does not overwrite the last file in the folder
            file_count = len(next(os.walk(folderPath))[2]) + 1

        soup = BeautifulSoup(page.content, 'html.parser')
        results = soup.find(id='post-list-posts')
        elements = results.find_all('a', class_='thumb')
        return elements, file_count, folderPath


def grabCharacter(url):
    characters = []
    numbers = []
    done = False

    resultsForCharacters, numbers = pageResults(url)

    for result, number in zip(resultsForCharacters, numbers):
        #Grabs characters names from the list page and puts them in a list
        if int(number) < MIN_PICTURES:
            done = True
            return done, characters
        else:
            characterUrl = result.contents[3].attrs['href']
            characterUrl = characterUrl.replace('post?', 'post?page=1&')
            characterName = result.contents[3].contents[0]
            characters.append(Character(characterName, mainURL + characterUrl, number))
    return done, characters

def pageResults(url):
    numbers = []
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    resultsForCharacters = soup.findAll('td', class_='tag-type-character')
    resultsForNumbers = soup.findAll('td', align ='right')
    for result in resultsForNumbers:
        numbers.append(result.contents[0])
    return resultsForCharacters, numbers
    

class Character:
    def __init__(self, name, url = '', amount = 20):
        self.name = name
        self.url = url
        self.amount = amount



def searchSuggest(input):
    suggested_characters = []
    searchUrl = f'https://yande.re/tag?name={input}&type=4&order=count'
    grabed_characters = grabCharacter(searchUrl)[1]
    for character in grabed_characters:
        suggested_characters.append(character.name)
        if len(suggested_characters) == 10:
            break
    grabed_characters.clear()
    return suggested_characters