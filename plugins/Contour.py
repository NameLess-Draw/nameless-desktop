from PIL import Image, ImageFilter

def info():
	print('Information blur')

def start_plugin():
	im = Image.open('plugin.png')
	im = im.filter(ImageFilter.CONTOUR)
	im.save('plugin.png')
