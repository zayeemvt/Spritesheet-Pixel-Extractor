import struct
from PIL import Image

def sliceSpriteSheet(sheet: Image, frame_width, frame_height):
    pixels = list(sheet.getdata())
    sheet_width, sheet_height = sheet.size
    
    frames = []
    for j in range(0, sheet_height, frame_height):
        for i in range(0, sheet_width, frame_width):
            frame_pixels = []

            for k in range(0, frame_height):
                index = i + j*sheet_height + k*sheet_width

                frame_pixels.append(pixels[index:index+frame_width-1])
            
            frames.append(frame_pixels)
    
    return frames

def exportImageRGBtoBinary(img_filepath, out_filepath):
    # Open the image file and load its pixel data
    img = Image.open(img_filepath)
    pixels = img.getdata()

    # frames = sliceSpriteSheet(img, 16, 16)

    # Get the image dimensions
    width, height = img.size
    num_pixels = width * height

    # Write the pixel data to the binary file
    with open(out_filepath, 'wb') as f:
        for pixel in pixels:
            r, g, b, a = pixel
            f.write(struct.pack('<BBBB', r, g, b, a))
       
    return width, height


def drawImageFromBinary(in_filepath, img_width, img_height):
    # Read the binary file into memory
    with open(in_filepath, 'rb') as f:
        data = f.read()

    print(f'Number of bytes read: {len(data)}')
    # Unpack the binary data into a sequence of RGB pixel values
    num_pixels = img_width * img_height
    pixels = struct.unpack(f'{num_pixels*4}B', data)
    it = iter(pixels)
    pixels = list(zip(it, it, it, it))

    # Create a new image and set its pixel data
    img = Image.new('RGBA', (img_width, img_height))
    img.putdata(pixels)

    # Display the image
    img.show()


if __name__ == "__main__":
    img_filename = "Images/Sine Wave.png"
    out_filename = "output.bin"

    frame_width = 16
    frame_height = 16

    img_width, img_height = exportImageRGBtoBinary(img_filename, out_filename)

    drawImageFromBinary(out_filename, img_width, img_height)