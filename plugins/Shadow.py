from PIL import Image

def info():
	print('Information shadow')

def change_brightness(action, extent):

    original_image = Image.open('plugin.png', 'r')
    pixels = original_image.getdata()

    new_image = Image.new('RGB', original_image.size)
    new_image_list = []

    brightness_multiplier = 1.0

    if action == 'lighten':
        brightness_multiplier += (extent/100)
    else:
        brightness_multiplier -= (extent/100)

    for pixel in pixels:
        new_pixel = (int(pixel[0] * brightness_multiplier),
                     int(pixel[1] * brightness_multiplier),
                     int(pixel[2] * brightness_multiplier))

        for pixel in new_pixel:
            if pixel > 255:
                pixel = 255
            elif pixel < 0:
                pixel = 0

        new_image_list.append(new_pixel)

    new_image.putdata(new_image_list)
    new_image.save('plugin.png')

def start_plugin():
	change_brightness('',50)