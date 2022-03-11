from PIL import Image, ImageDraw, ImageChops
import random
import colorsys

from matplotlib import colors


def random_colour():
    h = random.random()
    s = 1
    v = 1

    floar_rgb = colorsys.hsv_to_rgb(h,s,v)
    rgb = [int(x *255) for x in floar_rgb]
    return tuple(rgb)

def interpolate(start_color, end_color, factor: float):
    recip = 1- factor
    return(
        int(start_color[0] * recip + end_color[0]*factor),
        int(start_color[1] * recip + end_color[1]*factor),
        int(start_color[2] * recip + end_color[2]*factor),

    )

def generate_art(path: str):

    print("here we go!")
    target_size = 256
    
    scale_factor = 2
    image_size_px = target_size * scale_factor
    padding_px = 16 * scale_factor
    image_bg_color= (0,0,0)
    start_color = random_colour()
    end_color = random_colour()

    image = Image.new("RGB", size = (image_size_px,image_size_px), color= image_bg_color)


    #Drawing lines
    draw = ImageDraw.Draw(image)

    points = []

    for _ in range(10):
        random_point = ( 
            random.randint(padding_px, image_size_px-padding_px),
            random.randint(padding_px, image_size_px-padding_px),)

        points.append(random_point)



    #Draw bounding Box
    min_x = min([p[0] for p in points])
    max_x = max([p[0] for p in points])
    min_y = min([p[1] for p in points])
    max_y = max([p[1] for p in points])

    #draw.rectangle((min_x, min_y, max_x, max_y), outline=(230,230,230))

    #Centre the image.
    
    delta_x = min_x - (image_size_px - max_x)
    delta_y = min_y - (image_size_px - max_y)


    for i, point in enumerate(points):
        points[i] = (point[0] - delta_x // 2, point[1] - delta_y // 2)

    
    min_x = min([p[0] for p in points])
    max_x = max([p[0] for p in points])
    min_y = min([p[1] for p in points])
    max_y = max([p[1] for p in points])

    #draw.rectangle((min_x, min_y, max_x, max_y), outline=(230,0,0))
    


    #Dawing Lines   
    thickness = 0
    n_points = len(points) - 1
    for i, point in enumerate(points):

        overlay_image = Image.new("RGB", size = (image_size_px,image_size_px), color= image_bg_color)
        overlay_draw = ImageDraw.Draw(overlay_image)


        p1 = point

        if i == n_points:
            p2 = points[0]
        else:
            p2 = points[i+1]


        line_xy = (p1,p2)
        color_factor = i / n_points
        line_color = interpolate(start_color, end_color, color_factor)
        thickness += scale_factor
        overlay_draw.line(line_xy, fill=line_color, width = thickness)
        image = ImageChops.add(image, overlay_image) #can we use this fo rhte layering?


    image = image.resize((target_size, target_size), resample=Image.ANTIALIAS)
    image.save(path)


if __name__ == "__main__":
    for i in range(10):
        generate_art(f"test_image_{i}.png")