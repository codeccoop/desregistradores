# BUILT-INS
import os
import re

# VENDOR
import cv2
import numpy as np
import pytesseract
import pdf2image
from matplotlib  import pyplot as plt


def increase_contrast (img):
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l,a,b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    cl = clahe.apply(l)
    limg = cv2.merge((cl, a, b))
    return cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)


def get_grayscale (img):
    return cv2.cvtColor(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), cv2.COLOR_LAB2BGR)


def binarize (img):
    return cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)


def remove_noise (img):
    return cv2.medianBlur(img, 7)


def thresholding (img):
    return cv2.threshold(img, .0, 255., cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]


def dilate (img):
    kernel = np.ones((3, 3), np.uint8)
    return cv2.dilate(img, kernel, iterations=1)


def erode (img):
    kernel = np.ones((1, 1), np.uint8)
    return cv2.erode(img, kernel, iterations=1)


def opening (img):
    kernel = np.ones((3, 3), np.uint8)
    return cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)


def canny (img):
    return cv2.Canny(img, 100, 200)


def deskew (img):
    coords = np.column_stack(np.where(img > 0))
    angle = cv2.minAreaRect(coords)[1]
    if angle < 45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = img.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.)
    rotated = cv2.wrapAffine(img, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated


def match_template (img, template):
    return cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)


def get_rotation (img):
    osd = pytesseract.image_to_osd(img)
    angle = re.search(r"(?<=Rotate: )\d+", osd)
    return angle


def pdf_to_images (file_path):
    doc_name = os.path.basename(os.path.splitext(file_path)[0])
    directory = re.sub(r"\/pdfs.*$", "/images", file_path)
    # directory = os.path.relpath(os.path.join(os.path.abspath(os.path.dirname(__file__)), "../images"))
    subdirectory = os.path.join(directory, doc_name)
    if os.path.isdir(subdirectory):
        for file_name in os.listdir(subdirectory):
            os.remove(os.path.join(subdirectory, file_name))
        os.rmdir(subdirectory)

    os.mkdir(subdirectory)

    imgs = pdf2image.convert_from_path(file_path, dpi=300)
    img_paths = list()
    for i, img in enumerate(imgs):
        img_path = os.path.join(subdirectory, f"{i}.png")
        img.save(img_path)
        img_paths.append(img_path)

    return img_paths


class ImageParser (object):

    def __init__(self, file_path):
        if not file_path or type(file_path) != str:
            raise ValueError("file_path arguments is not a valid type")
        elif not os.path.isfile(file_path):
            raise FileExistsError("Can't find nothing at the end of the path")

        self.file_path = file_path
        self.file_name = os.path.basename(file_path)
        self.images = [cv2.imread(img_path) for img_path in pdf_to_images(file_path)]
        self.preprocess()

    @property
    def text (self):
        text = ""
        for img in self.images:
            text += "\n" + re.sub(r"(\n+|  +)", "  ", pytesseract.image_to_string(img, lang="spa"))

        return text

    def preprocess (self):
        preprocessed = []
        for img in self.images:
            img = increase_contrast(img)
            img = get_grayscale(img)
            # img = remove_noise(img)
            # img = thresholding(img)
            # img = binarize(img)
            # img = opening(img)
            # img = erode(img)
            # img = dilate(img)
            self.show_image("Test", img)

            preprocessed.append(img)

        self.images = preprocessed

        return
        # print(get_rotation(img))
        deskewed = deskew(img)
        self.show_image("Deskewed", deskewed)
        self.show_image("Gray Scale", grayscale)
        denoised = remove_noise(img)
        self.show_image("Denoised", denoised)
        # threshold = thresholding(img)
        # self.show_image("Threshold", threshold)
        dilated = dilate(img)
        self.show_image("Dilated", dilated)
        eroded = erode(img)
        self.show_image("Eroded", eroded)
        # cv2img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        # cv2.imshow("Image", get_grayscale(cv2img))

    def show_image (self, name, img):
        plt.subplot(121), plt.imshow(img), plt.title(name)
        plt.xticks([]), plt.yticks([])
        plt.show()
        # cv2.imshow(name, img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()


if __name__ == "__main__":
    file_path = os.path.join("../pdfs/T1/Verdi 106.pdf")
    parser = ImageParser(file_path)
    print(parser.text)
    i = 1
    out_path = os.path.join("../images")
    for img in parser.images:
        cv2.imwrite(os.path.join(out_path, "test-%s.png" % i), img)
