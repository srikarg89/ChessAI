import cv2
import os

folder = "../images/"
filepaths = os.listdir(folder)
filepaths = [os.path.join(folder, filepath) for filepath in filepaths]

for filepath in filepaths:
    img = cv2.imread(filepath, cv2.IMREAD_UNCHANGED)
    print(img.shape)
    resized = cv2.resize(img, (68, 68))
    if "original" in filepath:
        filepath = filepath[:filepath.rindex("/") + 1] + filepath[filepath.rindex("/") + 9:]
    cv2.imwrite(filepath, resized)
