from PIL import Image, ImageFont, ImageDraw

outfile = "Reeds Weekly Logo - 2022-12-19.jpg"

# Image for the background
my_image = Image.open("/images/Reeds Weekly Logo.jpg")

# Font used.
title_font = ImageFont.truetype('Roboto_Condensed/RobotoCondensed-Bold.ttf', 84)



first_text = "New Project"
second_text = "Worship for December 12, 2022"
image_editable = ImageDraw.Draw(my_image)

image_editable.text((960, 920), first_text, font=title_font, align='center', fill="white", anchor='ms')
image_editable.text((960, 1020), second_text, font=title_font, align='center', fill="white", anchor='ms')

# (237, 230, 211), ,anchor='mb'

my_image.save(outfile, "JPEG")

my_image.show()