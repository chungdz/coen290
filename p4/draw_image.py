from utilities import *

# Generate points for two sphere
rp1 = generate_semisphere_3D(r1, sloc1)
rp2 = generate_semisphere_3D(r2, sloc2)

# draw color with light
img = Image.new('RGB', (width, height))
pixels = img.load()
# floor
for x in range(width):
    for z in range(height):
        pixels[x, z] = convert_to_color(cal_intensity(np.array([x, 0, z]), np.array([0, 1, 0]), isFloor=True) * fcolor)
# sphere 1
for point in rp1:
    normal = point - sloc1
    normal = normal / norm(normal, ord=2)
    pixels[point[0], point[2]] = convert_to_color(cal_intensity(point, normal) * scolor1)
# sphere 2
for point in rp2:
    normal = point - sloc2
    normal = normal / norm(normal, ord=2)
    pixels[point[0], point[2]] = convert_to_color(cal_intensity(point, normal, isS2=True) * scolor2)

img.save('shade.jpg')
