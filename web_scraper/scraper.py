import requests
from bs4 import BeautifulSoup
import os
import urllib.request
import cv2
from database import charactermanager


MAX_PICTURES = 60
MIN_PICTURES = 800
mainURL = "https://yande.re/"
myPath = 'CharactersForRec'


class scraper(object):

    def grab_pictures(self, lewdFilter, wholesomeFilter, duplicateFilter, amount):
        self.lewdFilter = toggleToBool(lewdFilter)
        self.wholesomeFilter = toggleToBool(wholesomeFilter)
        self.duplicateFilter = toggleToBool(duplicateFilter)
        self.amount = int(amount)

        self.pageCounter = 1
        self.url = f"https://yande.re/tag?name={self.character.name}&order=count&page={self.pageCounter}&type=4"
        self.characters = []

        #create character from character class
        characterName = grab_added_character_name()
        self.character = Character(characterName, self.fetch_character_url(characterName), self.amount)

        #check if directory exsits for current character, if not, create one. Get folderPath
        self.folderPath = self.checkCharacterDir()
        #grab all picture links are current webpage
        self.getPage()
        self.fileCount = self.get_current_file_count()
        #set amount of pictures to stop at
        self.stopAmount = self.amount + self.fileCount()
        #start downloading pictures

        

    def grab_added_character_name(self):
        return charactermanager.grab_added_character()

    def fetch_character_url(self, characterName):
        return f'https://yande.re/post?page={self.pageCounter}&tags={characterName}'
    
    def checkCharacterDir(self)
        folderPath = myPath + "/" + self.character.name
        folderPath = folderPath.replace('_', ' ')
        isdir = os.path.isdir(folderPath)

        if not isdir:
            try:
                os.mkdir(folderPath)
                file_count = 0
            except:
                print("Failed to create directory %s" % folderPath)

        return folderPath
    
    def getPage(self):
        page = requests.get(self.character.url)
        pageContent = BeautifulSoup(page.content, 'html.parser')
        results = soup.find(id='post-list-posts')
        elements = results.find_all('a', class_='thumb')
    
    def get_current_file_count(self)
        #Grab the number of files and add one to it so that the save does not overwrite the last file in the folder
        return file_count = len(next(os.walk(self.folderPath))[2]) + 1

    def download_pictures(self):
        while self.fileCount < self.stopAmount:
            


        #Grab characters name and urls for the minium amount of pictures
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
                        if toggleToBool(lewdFilter):
                            if Islewd:
                                pass
                            else:
                                continue
                        elif toggleToBool(wholesomeFilter):
                            if Iswholesome:
                                pass
                            else:
                                continue
                    else:
                        pass

                    fullfilename = os.path.join(folderPath, str(file_count) + '.jpg')
                    urllib.request.urlretrieve(down_link, fullfilename)
                    if toggleToBool(duplicateFilter):
                        duplicated = checkForDuplicate(file_count)
                    else:
                        duplicated = False
                    if not duplicated:
                        file_count = len(next(os.walk(folderPath))[2]) + 1
                    if file_count > MAX_PICTURES:
                        break

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

    def toggleToBool(toggleString):
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


