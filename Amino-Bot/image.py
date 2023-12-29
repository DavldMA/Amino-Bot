import imgbbpy
import numpy as np
from PIL import Image
from PIL import ImageDraw
import urllib.request
import io

client = imgbbpy.SyncClient('key')

def convertImageToLink(url):
    try:
        image = client.upload(url=url)
        return image.url
    except:
        return None

def processGayImage(input_image_link):
    try:
        output_image_path = "output_image.png"

        with urllib.request.urlopen(input_image_link) as response:
            image_data = response.read()
        image = Image.open(io.BytesIO(image_data))
        image = image.convert("RGBA")

        lgbt_colors = [(255, 0, 0), (255, 165, 0), (255, 255, 0), (0, 128, 0), (0, 0, 255), (101, 3, 143)]

        gradient_height = image.size[1]
        gradient_width = image.size[0]
        gradient = Image.new('RGBA', (gradient_width, gradient_height))
        draw = ImageDraw.Draw(gradient)

        for i in range(len(lgbt_colors) - 1):
            start_y = i * gradient_height // (len(lgbt_colors) - 1)
            end_y = (i + 1) * gradient_height // (len(lgbt_colors) - 1)
            for y in range(start_y, end_y):
                r = int(lgbt_colors[i][0] + (lgbt_colors[i+1][0] - lgbt_colors[i][0]) * (y - start_y) / (end_y - start_y))
                g = int(lgbt_colors[i][1] + (lgbt_colors[i+1][1] - lgbt_colors[i][1]) * (y - start_y) / (end_y - start_y))
                b = int(lgbt_colors[i][2] + (lgbt_colors[i+1][2] - lgbt_colors[i][2]) * (y - start_y) / (end_y - start_y))
                for x in range(gradient_width):
                    draw.point((x, y), fill=(r, g, b, 255))

        # Resize the gradient image to match the input image dimensions
        gradient = gradient.resize((image.size[0], image.size[1]))

        # Blend the input image and gradient
        alpha = 0.45  # Adjust the alpha value to control the blending intensity
        result = Image.blend(image, gradient, alpha)

        # Save the resulting image
        result.save(output_image_path)

        return output_image_path
    except Exception as e:
        print("Error:", e)
        return None
