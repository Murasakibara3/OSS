# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import sys
from PIL import Image
import random
import hashlib
import os

DIST = 8

def keyInput():
    secretKey=raw_input("Secret Key : ")
    print ("You have inputed "+"\""+secretKey+"\""+" as a Secret Key")
    encryptedKey=hashlib.sha256()
    encryptedKey.update(secretKey)
    return encryptedKey.hexdigest()


def normalize_pixel(r, g, b):
    """
    pixel color normalize
    :param r: int
    :param g: int
    :param b: int
    :return: (int, int, int)
    """
    if is_modify_pixel(r, g, b):
        seed = random.randint(1, 3)
        if seed == 1:
            r = _normalize(r)
        if seed == 2:
            g = _normalize(g)
        if seed == 3:
            b = _normalize(b)
    return r, g, b


def modify_pixel(r, g, b):
    """
    pixel color modify
    :param r: int
    :param g: int
    :param b: int
    :return: (int, int, int)
    """
    return map(_modify, [r, g, b])


def is_modify_pixel(r, g, b):
    """
    :param r: int
    :param g: int
    :param b: int
    :return: bool
    """
    return r % DIST == g % DIST == b % DIST == 1


def _modify(i):
    if i >= 128:
        for x in xrange(DIST + 1):
            if i % DIST == 1:
                return i
            i -= 1
    else:
        for x in xrange(DIST + 1):
            if i % DIST == 1:
                return i
            i += 1
    raise ValueError


def _normalize(i):
    if i >= 128:
        i -= 1
    else:
        i += 1
    return i


def normalize(path, output):
    """
    normalize image
    :param path: str
    :param output: str
    """
    img = Image.open(path)
    img = img.convert('RGB')
    size = img.size
    new_img = Image.new('RGB', size)

    for y in range(img.size[1]):
        for x in range(img.size[0]):
            r, g, b = img.getpixel((x, y))
            _r, _g, _b = normalize_pixel(r, g, b)
            new_img.putpixel((x, y), (_r, _g, _b))
    new_img.save(output, "PNG", optimize=True)


def hide_text(path, text):
    """
    hide text to image
    :param path: str
    :param text: str
    """
    text = str(text)

    # convert text to hex for write
    write_param = []
    _base = 0
    for _ in to_hex(text):
        write_param.append(int(_, 16) + _base)
        _base += 16

    # hide hex-text to image
    img = Image.open(path)
    counter = 0
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            if counter in write_param:
                r, g, b = img.getpixel((x, y))
                r, g, b = modify_pixel(r, g, b)
                img.putpixel((x, y), (r, g, b))
            counter += 1

    # save
    img.save(path, "PNG", optimize=True)


def to_hex(s):
    return s.encode("hex")


def to_str(s):
    return s.decode("hex")


def read_text(path):
    """
    read secret text from image
    :param path: str
    :return: str
    """
    img = Image.open(path)
    counter = 0
    result = []
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            r, g, b = img.getpixel((x, y))
            if is_modify_pixel(r, g, b):
                result.append(counter)
            counter += 1
            if counter == 16:
                counter = 0
    return to_str(''.join([hex(_)[-1:] for _ in result]))


class Steganography(object):
    @classmethod
    def encode(cls, input_image_path, output_image_path, encode_text):
        """
        hide text to image
        :param input_image_path: str
        :param output_image_path: str
        :param encode_text: str
        """
        normalize(input_image_path, output_image_path)
        hide_text(output_image_path, encode_text)
        assert read_text(output_image_path) == encode_text, read_text(output_image_path)

    @classmethod
    def decode(cls, image_path):
        """
        read secret text from image
        :param image_path: str
        :return: str
        """
        return read_text(image_path)


# Main program
def main():
    available_list = ['jpg', 'gif', 'png', 'bmp', 'ico']
    
    #handle exception with no extension
    try:
        signature = sys.argv[2].split('.')[1]
    except :
        print "There is no extension!!"
        return

    if not  signature.lower() in available_list:
        print signature + " is not supported extension!!"
        return
    
    secretCode = keyInput()
    secretCodeLength = len(secretCode)

    checkSum = "0"
    checkSumLength = len(checkSum)

    if len(sys.argv) == 5 and sys.argv[1] == '-e':
        # encode
        input_image_path = sys.argv[2]
        output_image_path = sys.argv[3]
        text = secretCode+sys.argv[4]#+checkSum
        """
        checkStr = Steganography.decode(input_image_path)
        
        if(checkSum == checkStr[-checkSumLength:]):
            print "Already encoded!!"
            return
        else:
        """
        print("Start Encode : {}".format(input_image_path))
        Steganography.encode(input_image_path, output_image_path, text)
        print("Finish Encode : {}".format(output_image_path))
        print("Input Image Size : %d" % os.path.getsize(input_image_path))
        print("Output Image size : %d" % os.path.getsize(output_image_path))
        #the end of else(Line 215)
        return
    if len(sys.argv) == 3 and sys.argv[1] == '-d':
        # decode
        input_image_path = sys.argv[2]
        result=Steganography.decode(input_image_path)
        leakSecretCode=result[0:secretCodeLength]
        if(secretCode==leakSecretCode):
            print "Your secret message was \"%s\"" % result[secretCodeLength:]#-checkSumLength]
        else:
            print "You are not permited!!"
        return
    print_help_text()

def print_help_text():
    print("ERROR: not SteganographyApp command")
    print("--------------------------------")
    print("# encode example: hide text to image")
    print("SteganographyApp -e /tmp/image/input.jpg /tmp/image/output.jpg 'The quick brown fox jumps over the lazy dog.'")
    print("")
    print("# decode example: read secret text from image")
    print("SteganographyApp -d /tmp/image/output.jpg")
    print("")

if __name__ == "__main__":
    main()
