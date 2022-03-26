from PIL import Image, ImageDraw, ImageFont


def make_image(photo, name, surname, middle_name, sex, date, county):
    im = Image.new('RGB', (2000, 2000), color=('#FFF'))
    im.paste(photo, (50, 50))
    font = ImageFont.truetype('font/Roboto.ttf', size=64)
    draw_text = ImageDraw.Draw(im)
    k = 0

    for i in [name, surname, middle_name, sex, date, county]:
        draw_text.text(
            (1500, 50 + (k * 200)),
            i,
            font=font,
            fill='#1C0606')
        k += 1
    return im
