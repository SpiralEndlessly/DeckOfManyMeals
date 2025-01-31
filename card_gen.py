# Create an enhanced SVG recipe card design with a collectible card game style
from svgwrite import Drawing, image
import qrcode
from PIL import Image
import tomllib
import random

card_width_px = 1240 #4.1 * 300 # 1230
card_height_px = 1748 #5.8 * 300 # 1740

def read_toml(index):
    with open(f"def\\{index}.toml", "rb") as f:
        data = tomllib.load(f)
    return data

def kind_to_category(kind):
    if kind == 0:
        return "Frucht & Gemüse"
    elif kind == 1:
        return "Fleisch"
    elif kind == 2:
        return "Milchprodukte"
    elif kind == 3:
        return "Trockenes"
    elif kind == 4:
        return "Dosen & Gläser"
    elif kind == 5:
        return "Backwaren"
    elif kind == 6:
        return "Gewürze & Saucen"
    else:
        return "Gekühltes"

def create_qr(index, size):
    # URL to encode in the QR code
    url = f"https://spiralendlessly.github.io/DeckOfManyMeals/meal/{index}.html"
    
    # Set the desired width and height for the QR code image
    width = size
    height = size

    # Generate the QR code
    qr = qrcode.QRCode(
        version=1,  # Controls the size of the QR code
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # Error correction level
        box_size=10,  # Size of each individual box in the QR code
        border=0,  # Border thickness (minimum 4)
    )
    qr.add_data(url)
    qr.make(fit=True)

    # Create an image from the QR code
    img = qr.make_image(fill='black', back_color='white')

    img = img.convert("RGBA")
    pixdata = img.load()

    width, height = img.size
    for y in range(height):
        for x in range(width):
            if pixdata[x, y] == (255, 255, 255, 255):
                pixdata[x, y] = (255, 255, 255, 0)

    # Resize the image to the desired width and height
    img = img.resize((width, height), Image.BICUBIC)

    # Save the image as a PNG file
    img.save(f"qr/{index}qr.png")

def create_svg(index, name, ingredients, cook_time, prep_time, portions, kind, store_time, **kwargs):
    # Initialize the enhanced card design
    dwg = Drawing(f'svg/{index}.svg', size=(card_width_px, card_height_px), profile='tiny')
    
    color ="#1c192f"

    # Add background image at random offset
    x_margin = int(1652 - card_width_px)
    y_margin = int(2065 - card_height_px)
    x_shift = -random.randrange(0, x_margin)
    y_shift = -random.randrange(0, y_margin)
    dwg.add(image.Image("file:///D:\\repos\\DeckOfManyMeals\\img\\texture6.png", insert=(x_shift, y_shift)))

    # Ornate border
    stroke_width = 30
    dwg.add(dwg.rect(insert=(stroke_width / 2, stroke_width / 2), 
                    size=(card_width_px - stroke_width, card_height_px - stroke_width), 
                    fill="none", stroke=color, stroke_width=stroke_width))

    # Recipe Name Banner
    title_height = 180
    parts = name.upper().split("|")
    part_offset = 0
    if len(parts) == 1:
        title_height += 80
    for p in parts:
        dwg.add(dwg.text(f"{p}", insert=(card_width_px / 2, 20 + title_height / 2 + 8 + part_offset), 
                        font_size=74, font_family="Georgia", fill="black", text_anchor="middle"))
        part_offset += 80

    # Cooking Time Banner
    banner_width = 300
    banner_height = 50
    banner_x = card_width_px * 0.75 - banner_width / 2 + 80
    banner_y = 270
    banner_dist = 60
    dwg.add(dwg.rect(insert=(banner_x, banner_y + 0*banner_dist), size=(banner_width, banner_height), fill=color, rx=10, ry=10))
    dwg.add(dwg.rect(insert=(banner_x, banner_y + 1*banner_dist), size=(banner_width, banner_height), fill=color, rx=10, ry=10))
    dwg.add(dwg.rect(insert=(banner_x, banner_y + 2*banner_dist), size=(banner_width, banner_height), fill=color, rx=10, ry=10))
    dwg.add(dwg.rect(insert=(banner_x, banner_y + 3*banner_dist), size=(banner_width, banner_height), fill=color, rx=10, ry=10))
    dwg.add(dwg.rect(insert=(banner_x, banner_y + 4*banner_dist), size=(banner_width, banner_height), fill=color, rx=10, ry=10))

    if kind == 0:
        tag = "🥑\tVegan"
    elif kind == 1:
        tag = "🧀\tVegetarisch"
    elif kind == 2:
        tag = "🥩\tFleisch"
    else:
        tag = "🐟\tFisch"

    info_x = banner_x + 20
    info_y = banner_y + banner_height / 2 + 12
    dwg.add(dwg.text(tag, insert=(info_x, info_y + 0*banner_dist), 
                   font_size=32, font_family="Georgia", fill="white", text_anchor="start"))
    dwg.add(dwg.text(f"🕑\tVor: {prep_time}", insert=(info_x, info_y + 1*banner_dist), 
                   font_size=32, font_family="Georgia", fill="white", text_anchor="start"))
    dwg.add(dwg.text(f"🕑\tZub: {cook_time}", insert=(info_x, info_y + 2*banner_dist), 
                   font_size=32, font_family="Georgia", fill="white", text_anchor="start"))
    dwg.add(dwg.text(f"🍽️\t{portions} Portionen", insert=(info_x, info_y + 3*banner_dist), 
                   font_size=32, font_family="Georgia", fill="white", text_anchor="start"))
    dwg.add(dwg.text(f"❄️\t{store_time}", insert=(info_x, info_y + 4*banner_dist), 
                   font_size=32, font_family="Georgia", fill="white", text_anchor="start"))

    # Image
    image_size = 300
    image_x = card_width_px * 0.25 - image_size / 2 - 80
    image_y = 270
    dwg.add(image.Image(f"file:///D://repos//DeckOfManyMeals//img//{index}.png", insert=(image_x, image_y), 
                        size=(image_size, image_size)))

    ingredient_dist = 54
    category_dist = 90

    # Assemble categories
    # 0="Frucht & Gemüse", 1="Fleisch", 2="Milchprodukte", "3=Trockenes"
    # 4="Dosen & Gläser", 5="Backwaren", 6="Gewürze & Saucen"
    categories = dict()
    for ing, data in ingredients.items():
        # consolidate
        if isinstance(data, list):
            if "amount" in data[0]:
                unit = data[0]["unit"]
                amount = 0
                for x in data:
                    amount += x["amount"]
                data = dict(amount=amount, unit=unit, kind=data[0]["kind"])
            else:
                data = dict(kind=data[0]["kind"])
        else:
            if "amount" in data:
                amount = data["amount"]
            else:
                amount = 0

        category = kind_to_category(data["kind"])
        if not category in categories:
            categories[category] = list()
        
        if data["kind"] != 6 and amount != 0:
            insert = str(amount) + data["unit"] + " "
            y = ing.replace("#", insert)
        else: 
            y = ing.replace("#", "")
        categories[category].append(y)

    # Calculate category size
    sizes = dict()
    for category, items in categories.items():
        size = ingredient_dist
        for ingredient in items:
            sub = ingredient.split("|")
            size += ingredient_dist * len(sub)
        sizes[category] = size

    # Find balanced split
    assignment = dict()
    cost = 9999999
    for i in range(2 ** len(sizes.values())):
        indices = dict()
        a = 0
        b = 0
        for j, category in enumerate(sizes.keys()):
            if (i >> j) & 1 == 0:
                if a > 0:
                    a += category_dist
                a += sizes[category]
                indices[category] = 0
            else:
                if b > 0:
                    b += category_dist
                b += sizes[category]
                indices[category] = 1
        if abs(a-b) < cost:
            cost = abs(a-b)
            assignment = indices
            if b > a:
                for key in assignment.keys():
                    assignment[key] ^= 1

    # Ingredients list with icons
    ingredients_x = [80, 675]
    ingredients_y = 720
    category_offset = [0, 0]
    for category, items in categories.items():
        c = assignment[category]
        dwg.add(dwg.text(f"{category}:", insert=(ingredients_x[c], ingredients_y + category_offset[c]), font_size=42, font_family="Georgia", fill="black", font_weight="bold"))
        icon_size = 14
        for i, ingredient in enumerate(items):
            sub = ingredient.split("|")
            y_offset = ingredients_y + ingredient_dist + i * ingredient_dist
            dwg.add(dwg.circle(center=(ingredients_x[c] + 20, y_offset + category_offset[c] - 12), r=icon_size / 2, fill=color))
            dwg.add(dwg.text(sub[0], insert=(ingredients_x[c] + 40, y_offset + category_offset[c]), font_size=42, font_family="Georgia", fill="black"))
            for j in range(1, len(sub)):
                category_offset[c] += ingredient_dist
                dwg.add(dwg.text("\t"+sub[j], insert=(ingredients_x[c] + 40, y_offset + category_offset[c]), font_size=42, font_family="Georgia", fill="black"))
        category_offset[c] += category_dist + ingredient_dist * len(items)

    # QR Code decorative placement
    qr_size = 300
    create_qr(index, qr_size)
    qr_x = 0.5 * card_width_px
    qr_y = 270
    dwg.add(image.Image(f"file:///D:\\repos\\DeckOfManyMeals\\qr\\{index}qr.png", insert=(qr_x - qr_size / 2, qr_y), 
                        size=(qr_size, qr_size)))

    # Save enhanced SVG
    dwg.save()

def add_ingredient(lines, ingredient, data):
    if "amount" in data:
        insert = str(data["amount"]) + data["unit"] + " "
    else:
        insert = ""
    line = ingredient.replace("#", insert) + "\n"
    line = line.replace("-", "")
    line = line.replace("|", "")
    lines.append("- " + line)

def create_page(index, name, ingredients, instructions, subheaders, **kwargs):
    lines = []

    name = name.replace("|", "")
    lines.append(f"# {name}\n")
    lines.append("## Zutaten\n")

    if len(subheaders) > 0:
        for i, sub in enumerate(subheaders):
            lines.append(f"### {sub}\n")
            for ing, data in ingredients.items():
                if isinstance(data, list):
                    for subdata in data:
                        if subdata["sub"] == i:
                            add_ingredient(lines, ing, subdata)
                else:
                    if data["sub"] == i:
                        add_ingredient(lines, ing, data)
            lines.append("\n")
    else:
        for ing, data in ingredients.items():
            add_ingredient(lines, ing, data)
        lines.append("\n")

    lines.append("## Anleitung\n")
    for i, step in enumerate(instructions):
        lines.append(f"{i+1}. {step}\n")

    with open(f"meal/{index}.md", "w", encoding="utf-8") as f:
        f.writelines(lines)

for i in range(26):
    data = read_toml(i+1)
    create_svg(**data)
    create_page(**data)