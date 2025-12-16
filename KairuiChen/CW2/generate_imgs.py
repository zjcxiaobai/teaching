from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import datetime
import animal

FONT_CONST = '/usr/share/fonts/truetype/ubuntu/UbuntuMono-R.ttf'

def generate_adoption_form(output_filename: str, adoption_animal: animal.Animal, adopter_name: str, adopter_address: str,
                           template_filename: str):
    # load template image
    img = Image.open(template_filename)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT_CONST, 60)
    # add adopter name and address to form
    draw.text((700, 600), adopter_name, (0, 0, 0), font=font)
    draw.text((700, 800), adopter_address, (0, 0, 0), font=font)
    # add date to signature lines
    current_date =  datetime.datetime.now().strftime('%d/%m/%Y')
    draw.text((400, 1850), current_date, (0, 0, 0), font=font)
    draw.text((400, 2330), current_date, (0, 0, 0), font=font)

    # add name and date of birth
    draw.text((700, 1200), adoption_animal.name, (0, 0, 0), font=font)
    draw.text((750, 1330), adoption_animal.dob.strftime('%d/%m/%Y'), (0, 0, 0), font=font)

    # save copy of image
    img.save(output_filename)

def generate_adoption_poster(filename: str, animals: list[animal.Animal], template_filename: str):
    img = Image.open(template_filename)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT_CONST, 60)

    for i in range(len(animals)):
        a = animals[i]
        x_pos = 600 + (i % 2) * 900
        y_pos = 1000 + (i // 2) * 900
        draw.text((x_pos, y_pos), f'{a.name} ({a.species})', (0, 0, 0), font=font)
        draw.text((x_pos, y_pos+60), f'Age: {a.get_age()}', (0, 0, 0), font=font)

    img.save(filename)
