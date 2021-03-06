import os

def get_current_file_count(self):
    # Grab the number of files and add one to it so that the save does not overwrite the last file in the folder
    try:
        return(len(next(os.walk(self.folderPath))[2]) + 1)
    except:
        pass


def checkCharacterDir(self):
    character_name = self.character.name.replace('/', '.')
    self.folderPath = self.sav_dir + "/" + character_name
    isdir = os.path.isdir(self.folderPath)

    if not isdir:
        try:
            os.mkdir(self.folderPath)
            file_count = 0
        except:
            print("Failed to create directory %s" % self.folderPath)

def get_folder_path(self):
    return self.folderPath

