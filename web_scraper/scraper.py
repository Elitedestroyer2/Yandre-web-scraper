import requests
from bs4 import BeautifulSoup
import os
import urllib.request
import cv2
from database import charactermanager
from settings import settings

import concurrent.futures

MAX_PICTURES = 60
MIN_PICTURES = 800
mainURL = "https://yande.re/"
sav_dir = 'CharactersForRec'
page_counter_global =1 


class scraper(object):

    def start_threads(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executer:
            download_characters = {executer.submit(self.grab_pictures): 8}

    def grab_pictures(self):
        self.MAINURL = "https://yande.re/"
        self.sav_dir = settings.read_settings()


        self.pageCounter = 1
        #self.character = []

        #create character from character class
        self.conn = self.connect_to_database()
        self.updateCol = updateCollection()
        while not self.table_empty():
            self.conn.close_connection()
            self.conn = self.connect_to_database()
            self.character = self.grab_added_character_name()
            if self.character == None:
                break
            self.delete_added_charater_from_db()
            if self.character.name == 'ALL':
                self.grab_suggestion_list()
            self.conn.close_connection()
            self.assign_filter_values(self.character)
            self.character = Character(self.character.name, self.fetch_character_url(self.character.name), self.character.amount)
            self.url = f"https://yande.re/tag?name={self.character.name}&order=count&page={self.pageCounter}&type=4"

            #check if directory exsits for current character, if not, create one. Get folderPath
            self.folderPath = self.checkCharacterDir()
            #set fileCount
            self.fileCount = self.get_current_file_count()
            #set amount of pictures to stop at
            self.stopAmount = self.character.amount + self.fileCount
            #start downloading pictures
            self.download_pictures()
            self.conn = self.connect_to_database()
            self.update_database()
            self.conn.close_connection()
            self.updateCol.update()
            self.conn = self.connect_to_database()
        self.conn.close_connection()

    def table_empty(self):
        if self.conn.check_added_characters_table_count() > 0:
            return False
        else:
            return True

    def delete_added_charater_from_db(self):
        self.conn.remove_added_character(self.character.name)

    def grab_suggestion_list(self):
        character_sql = self.conn.grab_suggestion_list()
        self.conn.delete_added_table()
        self.conn.create_added_table()
        amount, max_number, min_number = self.grab_default_values()
        for character in character_sql:
            if character.count < min_number:
                pass
            else:
                self.character.append(addedCharacter(character[0],False,True,False,amount,''))
                self.conn.add_added_character(character)
    
    def grab_default_values(self):
        amount, max_number, min_number = settings.get_default_values()
        return amount, max_number, min_number

    def connect_to_database(self):
        conn = charactermanager.dbConnection()
        conn.connect()
        return conn

    def assign_filter_values(self, character):
        self.lewdFilter = character.lewd
        self.wholesomeFilter = character.wholesome
        self.duplicateFilter = character.duplicate

    def update_database(self):
        amount = self.get_current_file_count() - 1
        character_name = self.character.name
        character_name = character_name.replace('_', ' ')
        self.conn.add_character(character_name, amount)
        pass

    def grab_added_character_name(self):
        return self.conn.grab_added_character()
    
    def delete_added_characters_from_table(self):
        self.conn.delete_added_table()

    def fetch_character_url(self, characterName):
        return f'https://yande.re/post?page={self.pageCounter}&tags={characterName}'
    
    def checkCharacterDir(self):
        folderPath = self.sav_dir + "/" + self.character.name
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
        fileCount = len(next(os.walk(self.folderPath))[2]) + 1
        return fileCount

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
                    pass
            else:
                self.download(download_link)

    def download(self, download_link):

        fullfilename = os.path.join(self.folderPath, str(self.fileCount) + '.jpg')
        urllib.request.urlretrieve(download_link, fullfilename)
        if self.duplicateFilter:
            if not (checkForDuplicate(self.fileCount)):
                self.fileCount = self.get_current_file_count()
        else:
            self.fileCount = self.get_current_file_count()
                

    def unknown(self):
        #Grab character name and urls for the minimum amount of pictures
        while not grabCharacter(url)[0]:
            tempCharacters = grabCharacter(url)[1]
            for char in tempCharacters:
                character.append(char)
            pageCounter += 1
            url = f"https://yande.re/tag?name=&order=count&page={pageCounter}&type=4" 
        for character in character:
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
        folderPath = sav_dir + "/" + character.name
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
    character = []
    numbers = []
    done = False

    resultsForCharacters, numbers = pageResults(url)

    for result, number in zip(resultsForCharacters, numbers):
        #Grabs character names from the list page and puts them in a list
        characterUrl = result.contents[3].attrs['href']
        characterUrl = characterUrl.replace('post?', 'post?page=1&')
        characterName = result.contents[3].contents[0]
        character.append(Character(characterName, mainURL + characterUrl, number))
    return done, character

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

class updateCollection(object):

    def update(self):
        self.conn = self.connect_to_database()
        sav_dir = settings.read_settings()
        list_folders = os.listdir(sav_dir)
        self.conn.delete_table()
        self.conn.create_table()
        for folder in list_folders:
            folder_path = self.get_folder_path(sav_dir, folder)
            amount_of_pics_in_folder = len(next(os.walk(folder_path))[2])
            self.conn.add_character(folder, amount_of_pics_in_folder)
        self.conn.close_connection()
    
    def connect_to_database(self):
        conn = charactermanager.dbConnection()
        conn.connect()
        return conn

    def get_folder_path(self, sav_dir, folder):
        folder_path = sav_dir + '/' + folder
        return folder_path


class suggestionsUpdater(object):

    def __init__(self):
        self.url = f'https://yande.re/tag?commit=Search&name=&order=count&page={page_counter_global}&type=4'

    def startUp(self):
        self.reset_suggestion_table()
        self.grab_character_names_and_counts()
        self.add_characters_to_suggestions()

    def reset_suggestion_table(self):
        self.connect_to_database()
        self.conn.delete_suggestions_table()
        self.conn.create_suggestions_table()
        self.close_database()
    
    def connect_to_database(self):
        self.conn = charactermanager.dbConnection()
        self.conn.connect()
    
    def close_database(self):
        self.conn.close_connection()
    
    def grab_character_names_and_counts(self):
        self.character = []
        done = False
        while not done:
            self.grab_html_data()
            for character_name_outer_html, character_count_outer_html in zip(self.character_names_outer_html, self.character_counts_outer_html):
                if int(character_count_outer_html.contents[0]) > 9:
                    self.character.append(CharacterSuggestion(character_name_outer_html.contents[3].contents[0], character_count_outer_html.contents[0]))
                elif int(character_count_outer_html.contents[0]) < 10:
                    done = True
                    continue

    def grab_html_data(self):
        page = requests.get(self.url)
        soup = BeautifulSoup(page.content, 'html.parser')
        self.character_names_outer_html = soup.findAll('td', class_='tag-type-character')
        self.character_counts_outer_html = soup.findAll('td', align ='right')
        self.increment_page_counter()

    def increment_page_counter(self):
        global page_counter_global
        page_counter_global += 1
        self.url = f'https://yande.re/tag?commit=Search&name=&order=count&page={page_counter_global}&type=4'
    
    def add_characters_to_suggestions(self):
        self.connect_to_database()
        for character in self.character:
            self.conn.added_character_to_suggest_list(character)
        self.close_database()

class CharacterSuggestion:
    def __init__(self, name, count):
        self.name = name
        self.count = count

class addedCharacter:
    def __init__(self, name, lewd, wholesome, duplicate, amount, url=''):
        DEFAULT_AMOUNT = 20
        self.name = name
        self.url = url
        if amount == '':
            self.amount = DEFAULT_AMOUNT
        else:
            self.amount = amount
        self.lewd = lewd
        self.wholesome = wholesome
        self.duplicate = duplicate