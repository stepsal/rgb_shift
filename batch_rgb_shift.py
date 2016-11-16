from PIL import Image
from collections import deque
import os
import binascii
import argparse
OUTPUT_FORMAT = ".png"
image_formats = ['.jpg', '.jpeg', '.png', '.tif', '.bmp', 'gif', 'tiff']
SAVE_IMAGE = True


def get_all_images_from_the_input_dir(input_dir):
    images = []
    for file in os.listdir(input_dir):
        filepath = os.path.join(input_dir, file)
        if os.path.isfile(filepath):
            if os.path.splitext(filepath)[1].lower() in image_formats:
                img = Image.open(filepath)
                images.append(img)
    return images


def save_image(image, prefix):
    random_hash = str(binascii.b2a_hex(os.urandom(15)))[2:-1]
    output_image_name = prefix + "_" + random_hash + "_" + OUTPUT_FORMAT
    output_dir = "output"
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir_path = os.path.join(script_dir, output_dir)
    if not os.path.exists(output_dir_path):
        os.makedirs(output_dir_path)
    image_path = os.path.join(output_dir_path, output_image_name)
    print("Image saved to {0}".format(image_path))
    image.save(image_path)


def rgb_shift(image, channel='r', offset=100):
    image = image.convert('RGB')
    image.load()
    r, g, b = image.split()
    eval_getdata = channel + ".getdata()"
    channel_data = eval(eval_getdata)
    channel_deque = deque(channel_data)
    channel_deque.rotate(offset)
    eval_putdata = channel + ".putdata(channel_deque)"
    eval(eval_putdata)
    shifted_image = Image.merge('RGB', (r, g, b))
    return shifted_image


def main():
    images = get_all_images_from_the_input_dir(INPUT_DIR)
    for image in images:
        shifted_image = rgb_shift(image, CHANNEL, OFFSET)
        shifted_image.show()
        save_image(shifted_image, "rgb_shift")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='RGB Shift Script')
    parser.add_argument("-i", "--input", dest="INPUT_DIR",
                        default="/home/stephen.salmon/Pictures/test_input/", help="input directory")
    parser.add_argument("-c", "--channel", dest="CHANNEL",
                        default="r", choices=['r', 'g', 'b'], help="Channel")
    parser.add_argument("-o", "--offset", dest="OFFSET",
                        default=100, type=int, help="Offset")
    try:
        args = parser.parse_args()
    except:
        print("Args Error")
        parser.print_help()
        exit(2)
    OFFSET = args.OFFSET
    CHANNEL = args.CHANNEL
    if args.INPUT_DIR:
        if os.path.isdir(args.INPUT_DIR):
            INPUT_DIR = args.INPUT_DIR
        else:
            print("Not a valid input directory")
            parser.print_help()
            exit(2)
    main()

