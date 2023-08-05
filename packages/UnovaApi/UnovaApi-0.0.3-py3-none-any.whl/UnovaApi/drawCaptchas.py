import PIL
import PIL.Image


def draw_image(image_path, height, width, threshold=165):
    image = PIL.Image.open(image_path)
    image = image.resize((width, height), PIL.Image.ANTIALIAS)
    image = image.convert("L")
    pixels = list(image.getdata())
    pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]
    characters = " `^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
    characters = characters[::-1]
    for row in pixels:
        if any(isinstance(e, int) and e < threshold for e in row):
            for pixel in row:
                if pixel > threshold:
                    pixel = 255
                char = characters[int(pixel / 255 * (len(characters) - 1))]
                print(char, end="")
            print()