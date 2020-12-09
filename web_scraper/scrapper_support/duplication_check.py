import cv2
import os

def checkForDuplicate(file_count, folder_path):
    file_check_count = 1
    while file_check_count != file_count:

        original = cv2.imread(
            folder_path + '/' + str(file_check_count) + '.jpg')
        duplicate = cv2.imread(folder_path + '/' + str(file_count) + '.jpg')

        if original.shape == duplicate.shape:
            difference = cv2.subtract(original, duplicate)
            b, g, r = cv2.split(difference)
            if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0:
                os.remove(folder_path + '/' + str(file_count) + '.jpg')
                return True
        file_check_count += 1