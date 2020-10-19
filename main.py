from tkinter import *
from tkinter import filedialog as fd
from tkinter.colorchooser import askcolor
from PIL import Image, ImageTk, ImageFilter, ImageDraw
import random
from datetime import date
import os
from re import findall
import sys
from sys import platform
import os
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
sys.path.append('plugins')


class Paint(object):
	DEFAULT_COLOR = 'black'
	screen_width = 1280
	screen_height = 720
	type_draw = 0

	text = ''

	objects = None

	def __init__(self):

		self.root = Tk()
		self.menu_plugins = Menu(self.root)

		self.root.title("Графический редактор")

		self.plug = []
		self.plug_in_dir = []
		self.img = []

		self.indeter = self.upd()
		for row in range(self.indeter):
			self.plug.append(self.plug_in_dir[row])

		self.variable = StringVar(self.root)
		self.variable.set(self.plug[0])

		menu = Menu(self.root)
		menu_file = Menu(menu)
		menu_file.add_command(label='Загрузить',
							  command=self.insertImg)
		menu_file.add_command(label='Сохранить',
							  command=self.extractImg)
		menu_file.add_command(labe='Отправить на почту',
							  command=self.send_on_email)
		menu_file.add_command(labe='Шифровка',
							  command=self.dlg_shifr)
		menu_file.add_command(labe='Плагины',
							  command=self.dlg_plugins)
		menu_file.add_command(labe='Новый лист',
							  command=self.dlg_new_list)
		menu.add_cascade(label='Файл', menu=menu_file)

		menu_paint = Menu(self.root)
		menu_paint.add_command(label='Карандаш',
							   command=self.use_pen)
		menu_paint.add_command(label='Эллипс',
							   command=self.use_oval)
		menu_paint.add_command(labe='Прямоугольник',
							   command=self.use_rect)
		menu_paint.add_command(labe='Линия',
							   command=self.use_line)
		menu_paint.add_command(labe='Ластик',
							   command=self.use_eraser)
		menu_paint.add_command(labe='Очистить',
							   command=self.use_clear)
		menu_paint.add_command(labe='Назад',
							   command=self.back)
		menu.add_cascade(label='Инструменты', menu=menu_paint)

		menu_style = Menu(self.root)
		menu_style.add_command(label='Цвет контура',
							   command=self.choose_color)
		menu_style.add_command(label='Цвет заливки',
							   command=self.choose_color_2)
		menu_style.add_command(label='Размер кисти',
							   command=self.choose_size)
		menu.add_cascade(label='Стиль', menu=menu_style)

		self.root.config(menu=menu)

		self.c = Canvas(self.root, bg='white', width=self.screen_width,
						height=self.screen_height, scrollregion=(0, 0, self.screen_width, self.screen_height), cursor='pencil')

		hbar=Scrollbar(self.root,orient=HORIZONTAL)
		hbar.pack(side=BOTTOM,fill=X)
		hbar.config(command=self.c.xview)
		vbar=Scrollbar(self.root,orient=VERTICAL)
		vbar.pack(side=RIGHT,fill=Y)
		vbar.config(command=self.c.yview)

		self.c.config(width=self.screen_width, height=self.screen_height)
		self.c.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
		self.c.pack(side=LEFT, expand=TRUE)
		# self.c.grid(row=3, columnspan=6)

		self.setup()
		self.root.mainloop()

	def encrypted(self):
		file_name = fd.asksaveasfilename(filetypes=(
			("PNG files", "*.png"), ("ALL files", "*.*")))
		try:
			keys = []
			self.save_plugin(file_name)
			img = Image.open(file_name)
			draw = ImageDraw.Draw(img)
			width = img.size[0]
			height = img.size[1]
			pix = img.load()

			today = str(date.today())
			day = today[-2:]
			month = today[-5:-3]
			year = today[2:4]
			day = int(day)
			month = int(month)
			year = int(year)

			msg = self.entry_recieve_mail.get('1.0', 'end-1c')
			msg += '~'

			g, b = pix[0,0][1:3]
			draw.point((0,0), (day, month, year))

			seed = day + month + year
			random.seed(seed)

			for elem in ([ord(elem) for elem in msg]):
				key = (random.randint(1,width-1),random.randint(1,height-1))
				g, b = pix[key][1:3]
				draw.point(key, (elem,g , b))

			img.save(file_name, "PNG")
		except:
			pass

	def decrypted(self):
		file_name = fd.askopenfilename(filetypes=(
			("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("ALL files", "*.*")))
		try:
			a = []
			keys = []
			img = Image.open(file_name)
			pix = img.load()
			width = img.size[0]
			height = img.size[1]

			r = pix[0,0][0]

			seed = pix[0,0][0] + pix[0,0][1] + pix[0,0][2]
			random.seed(seed)

			key = (random.randint(1,width-1),random.randint(1,height-1))
			a.append(pix[tuple(key)][0])

			while chr(pix[tuple(key)][0]) != '~':
				key = (random.randint(1,width-1),random.randint(1,height-1))
				a.append(pix[tuple(key)][0])

			msg = ''.join([chr(elem) for elem in a])
			msg = msg[:-1]
			self.entry_recieve_mail.delete(1.0, END)
			self.entry_recieve_mail.insert(END, msg)
		except:
			pass

	def save_plugin(self, file_name):
		self.c.postscript(file=file_name[: len(file_name)-4] + '.eps')
		img = Image.open(file_name[: len(file_name)-4] + '.eps')
		img.save(file_name, 'png')
		os.remove(file_name[: len(file_name)-4] + '.eps')

	def ok(self):
		for row in range(self.indeter+1):
			if row == 0 and self.variable.get() == 'Плагины':
				pass
			elif self.variable.get() == self.plug[row]:
				self.save_plugin('plugin.png')
				exec('import plugins.'+self.plug_in_dir[row-1])
				exec('plugins.'+self.plug_in_dir[row-1]+'.start_plugin()')
				self.load('plugin.png')
				os.remove('plugin.png')

	def choose_size(self):
		self.dlg_email = Tk()
		self.dlg_email.title(
			"Размер кисти")
		self.choose_size_button = Scale(
			self.dlg_email, from_=1, to=30, width=30, length=190, orient=HORIZONTAL)
		self.choose_size_button.grid(row=0, column=0)
		self.choose_size_button.bind('<ButtonRelease-1>', self.change_line)
		self.dlg_email.call('wm', 'attributes', '.', '-topmost', '1')

		self.dlg_email.mainloop()

	def effect_shadow(self):
		self.c.create_rectangle(0, 0, self.screen_width,
								self.screen_height, fill='white', outline='white')

	def effect_sobel(self):
		self.c.create_rectangle(0, 0, self.screen_width,
								self.screen_height, fill='white', outline='white')

	def dlg_new_list(self):
		self.form_plugins = Tk()
		self.form_plugins.title(
			"Новый лист")

		dlg_menu_plugin = Menu(self.form_plugins)

		self.height_label = Label(self.form_plugins, width=10, text="Высота")
		self.height_text = Entry(self.form_plugins, width=10)

		self.width_label = Label(self.form_plugins, width=10, text="Ширина")
		self.width_text = Entry(self.form_plugins, width=10)

		self.plug_ok = Button(self.form_plugins, text="Создать",
							  command=self.ok_new_canvas, width=20)

		self.height_label.grid(row=0, column=0)
		self.height_text.grid(row=0, column=1)

		self.width_label.grid(row=1, column=0)
		self.width_text.grid(row=1, column=1)

		# self.height_text.grid(row=1, column=1)
		self.plug_ok.grid(row=2,  columnspan=2)

		self.form_plugins.config(menu=dlg_menu_plugin)
		self.form_plugins.call('wm', 'attributes', '.', '-topmost', '1')
		self.form_plugins.mainloop()

	def dlg_new_list(self):
		self.form_plugins = Tk()
		self.form_plugins.title(
			"Новый лист")

		dlg_menu_plugin = Menu(self.form_plugins)

		self.height_label = Label(self.form_plugins, width=10, text="Высота")
		self.height_text = Entry(self.form_plugins, width=10)

		self.width_label = Label(self.form_plugins, width=10, text="Ширина")
		self.width_text = Entry(self.form_plugins, width=10)

		self.plug_ok = Button(self.form_plugins, text="Создать",
							  command=self.ok_new_canvas, width=20)

		self.height_label.grid(row=0, column=0)
		self.height_text.grid(row=0, column=1)

		self.width_label.grid(row=1, column=0)
		self.width_text.grid(row=1, column=1)

		# self.height_text.grid(row=1, column=1)
		self.plug_ok.grid(row=2,  columnspan=2)

		self.form_plugins.config(menu=dlg_menu_plugin)
		self.form_plugins.call('wm', 'attributes', '.', '-topmost', '1')
		self.form_plugins.mainloop()

	def ok_new_canvas(self):
		self.screen_width = self.width_text.get()
		self.screen_height = self.height_text.get()
		self.use_clear()
		self.c.config(width=self.screen_width, height=self.screen_height, scrollregion=(0, 0, self.screen_width, self.screen_height), cursor='pencil')

	def dlg_plugins(self):
		self.form_plugins = Tk()
		self.form_plugins.title(
			"Плагины")

		dlg_menu_plugin = Menu(self.form_plugins)

		self.plug = ['Плагины']
		self.plug_in_dir = []

		self.indeter = self.upd()
		for row in range(self.indeter):
			self.plug.append(self.plug_in_dir[row])

		self.variable = StringVar(self.form_plugins)
		self.variable.set(self.plug[0])

		self.w = OptionMenu(self.form_plugins,
							self.variable, *self.plug)
		self.w.grid(row=0, column=0)
		self.plug_ok = Button(self.form_plugins, text="OK",
							  command=self.ok, width=10)
		self.plug_ok.grid(row=0, column=1)

		self.form_plugins.config(menu=dlg_menu_plugin)
		self.form_plugins.call('wm', 'attributes', '.', '-topmost', '1')
		self.form_plugins.mainloop()

	def dlg_shifr(self):
		self.form_shifr = Tk()
		self.form_shifr.title(
			"Шифровка и расшифровка сообщения")

		dlg_menu_shifr = Menu(self.form_shifr)

		self.entry_recieve_mail = Text(self.form_shifr, height=1, width=100)
		self.entry_recieve_mail.grid(column=0, row=0)

		menu_shifr = Menu(self.form_shifr)
		menu_shifr.add_command(label='Зашифровать',
							   command=self.encrypted)
		menu_shifr.add_command(label='Расшифровать',
							   command=self.decrypted)
		dlg_menu_shifr.add_cascade(label='Шифровка', menu=menu_shifr)

		self.form_shifr.config(menu=dlg_menu_shifr)
		self.form_shifr.call('wm', 'attributes', '.', '-topmost', '1')
		self.form_shifr.mainloop()

	def send_on_email(self):
		self.dlg_email = Tk()
		self.dlg_email.title(
			"Введите ящик того, кому вы хотите прислать изображение")

		self.entry_recieve_mail = Entry(self.dlg_email, width=100)
		self.entry_recieve_mail.grid(column=0, row=0)

		self.btn_close = Button(self.dlg_email, text="Ввел",
								command=self.on_dlg_email_close)
		self.btn_close.grid(column=0, row=1)
		self.dlg_email.mainloop()

	def on_dlg_email_close(self):
		ImgFileName = fd.askopenfilename(filetypes=(
			("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("ALL files", "*.*")))
		try:
			self.load(file_name)
		except:
			pass

		smtp_server = "smtp.gmail.com"
		port = 587
		sender_email = "nameless.team.001@gmail.com"
		# receiver_email = "nameless.team.001@gmail.com"
		receiver_email = self.entry_recieve_mail.get()
		password = "2019created_by_nameless"
		img_data = open(ImgFileName, 'rb').read()
		msg = MIMEMultipart()
		msg['Subject'] = 'Вам пришла картинка'
		text = MIMEText(
			"Благодарим, что используете наш редактор изображений!")
		msg.attach(text)
		image = MIMEImage(img_data, name=os.path.basename(ImgFileName))
		msg.attach(image)
		send_process = smtplib.SMTP(smtp_server, port)
		send_process.ehlo()
		send_process.starttls()
		send_process.ehlo()
		send_process.login(sender_email, password)
		send_process.sendmail(sender_email, receiver_email, msg.as_string())
		send_process.quit()

		self.dlg_email.destroy()

	def setup(self):
		self.obj = []
		self.file_name = None
		self.img = []
		self.obj_pen = []
		self.old_x = None
		self.old_y = None
		self.line_width = 1
		self.color = self.DEFAULT_COLOR
		self.color_2 = 'white'
		self.eraser_on = False
		# self.active_button = self.pen_button
		self.c.bind('<B1-Motion>', self.paint)
		self.c.bind('<ButtonRelease-1>', self.reset)
		self.c.bind('<ButtonPress-1>', self.press)
		self.root.bind('<Control-z>', self.back)
		self.root.bind('<Control-Z>', self.back)
		# self.activate_button(self.pen_button)

	def change_line(self, key = None):
		self.line_width = self.choose_size_button.get()

	def insertImg(self):
		self.type_draw = 4
		self.file_name = fd.askopenfilename(filetypes=(
			("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("ALL files", "*.*")))

	def load(self, file_name):
		self.img.append(Image.open(file_name))
		self.img[-1] = self.img[-1].resize(
			(self.screen_width, self.screen_height))
		self.img[-1] = ImageTk.PhotoImage(self.img[-1])
		self.objects = self.c.create_image(0, 0, anchor=NW, image=self.img[-1])
		a = []
		a.append(self.objects)
		self.obj.append(a)

	def extractImg(self):
		file_name = fd.asksaveasfilename(filetypes=(
			("PNG files", "*.png"), ("ALL files", "*.*")))
		try:
			self.save(file_name)
		except:
			pass

	def save(self, file_name):
		self.c.postscript(file='/'+file_name[1: len(file_name)-4] + '.eps')
		img = Image.open('/'+file_name[1: len(file_name)-4] + '.eps')
		img.save('/'+file_name, 'png')
		os.remove('/'+file_name[1: len(file_name)-4] + '.eps')

	def back(self, key = None):
		if self.obj != []:
			for row in self.obj[-1]:
				self.c.delete(row)
			self.obj = self.obj[:-1]
		else:
			self.img = []

	def use_clear(self):
		self.c.create_rectangle(
			0, 0, self.screen_width, self.screen_height, fill='white', outline='white')
		self.obj = []
		self.img = []

	def show_extension(self):
		self.color_save = Place(
			self.root, text='Ghbv', command=self.extractImg)
		# self.color_save.grid(row=1, column=4)

		self.c.create_rectangle(
			0, 0, self.screen_width, self.screen_height, fill='white', outline='white')

	def use_pen(self):
		# self.eraser_on = False
		self.color = self.DEFAULT_COLOR
		self.type_draw = 0

	def use_rect(self):
		self.type_draw = 2

	def use_oval(self):
		self.type_draw = 1

	def use_line(self):
		self.type_draw = 3

	def choose_color(self):
		self.eraser_on = False
		self.color = askcolor(color=self.color, title='Изменить цвет')[1]

	def choose_color_2(self):
		self.eraser_on = False
		self.color_2 = askcolor(color=self.color_2, title='Изменить цвет')[1]

	def use_eraser(self):
		self.check_size()
		self.type_draw = 0
		self.color = 'white'
		# self.eraser_on = True

	def activate_button(self, some_button, eraser_mode=False):
		some_button.config(relief=SUNKEN)
		self.active_button = some_button
		self.eraser_on = eraser_mode

	def paint(self, event):
		self.check_size()

		if self.type_draw == 0:
			self.pencil(event)
		elif self.type_draw == 1:
			self.oval(event)
		elif self.type_draw == 2:
			self.rectangle(event)
		elif self.type_draw == 3:
			self.line(event)
		elif self.type_draw == 4:
			self.draw_image(event)

	def draw_image(self, event):
		self.c.delete(self.objects)
		self.img.append(Image.open(self.file_name))
		w = abs(event.x-self.old_x)
		h = abs(event.y-self.old_y)
		if w == 0:
			w += 1
		if h == 0:
			h += 1
		self.img[-1] = self.img[-1].resize((w, h))
		self.img[-1] = ImageTk.PhotoImage(self.img[-1])
		self.objects = self.c.create_image(
			self.old_x, self.old_y, anchor=NW, image=self.img[-1])

	def pencil(self, event):
		try:
			self.check_size()
			paint_color = 'white' if self.eraser_on else self.color
			if self.old_x and self.old_y:
				a = self.c.create_line(self.old_x, self.old_y, event.x, event.y, width=self.line_width,
									   fill=paint_color, capstyle=ROUND, smooth=TRUE, splinesteps=36)
			self.old_x = event.x
			self.old_y = event.y
			self.obj_pen.append(a)
		except:
			pass

	def press(self, event):
		self.check_size()
		self.old_x = event.x
		self.old_y = event.y
		if self.type_draw == 1:
			self.objects = self.c.create_oval(
				self.old_x, self.old_y, event.x, event.y, fill=self.color_2, width=self.line_width, outline=self.color)
		elif self.type_draw == 2:
			self.objects = self.c.create_oval(
				self.old_x, self.old_y, event.x, event.y, fill=self.color_2, width=self.line_width, outline=self.color)
		elif self.type_draw == 3:
			self.objects = self.c.create_line(self.old_x, self.old_y, event.x, event.y,
											  width=self.line_width, capstyle=ROUND, smooth=TRUE, fill=self.color, splinesteps=36)
		elif self.type_draw == 0:
			self.obj_pen = []
			a = self.c.create_line(self.old_x, self.old_y, event.x, event.y, width=self.line_width,
								   capstyle=ROUND, smooth=TRUE, fill=self.color, splinesteps=36)
			self.obj_pen.append(a)
		elif self.type_draw == 4:
			try:
				w = abs(event.x-self.old_x)
				h = abs(event.y-self.old_y)
				if w == 0:
					w += 1
				if h == 0:
					h += 1
				self.img.append(Image.open(self.file_name))
				self.img[-1] = self.img[-1].resize((w, h))
				self.img[-1] = ImageTk.PhotoImage(self.img[-1])
				self.objects = self.c.create_image(
					self.old_x, self.old_y, anchor=NW, image=self.img[-1])
			finally:
				pass

	def oval(self, event):
		self.check_size()
		self.c.delete(self.objects)
		self.objects = self.c.create_oval(
			self.old_x, self.old_y, event.x, event.y, fill=self.color_2, width=self.line_width, outline=self.color)

	def rectangle(self, event):
		self.check_size()
		self.c.delete(self.objects)
		self.objects = self.c.create_rectangle(
			self.old_x, self.old_y, event.x, event.y, fill=self.color_2, width=self.line_width, outline=self.color)

	def line(self, event):
		self.check_size()
		self.c.delete(self.objects)
		self.objects = self.c.create_line(self.old_x, self.old_y, event.x, event.y,
										  width=self.line_width, capstyle=ROUND, smooth=TRUE, fill=self.color)

	def reset(self, event):
		a = []
		a.append(self.objects)
		if self.type_draw == 0:
			self.obj.append(self.obj_pen)
		else:
			self.obj.append(a)
		self.old_x, self.old_y = None, None

	def check_size(self):
		try:
			self.line_width = self.choose_size_button.get()
		except:
			pass

	def upd(self):
		self.plug_in_dir = []
		for root, dirs, files in os.walk("plugins"):
			for file in files:
				if file.endswith(".py"):
					a = os.path.join(root, file)
					a = a[8:-3]
					self.plug_in_dir.append(a)
		return len(self.plug_in_dir)


if __name__ == '__main__':
	Paint()
