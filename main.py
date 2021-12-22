import numpy as np
from PIL import Image

def get_color(val):
    if val >= 0.9:
        return (4, 18, 14)
    if val >= 0.8:
        return (4, 38, 4)
    if val >= 0.7:
        return (4, 54, 4)
    if val >= 0.6:
        return (4, 66, 4)
    if val >= 0.5:
        return (4, 94, 4)
    if val >= 0.4:
        return (28, 114, 4)
    if val >= 0.3:
        return (100, 162, 4)
    if val >= 0.2:
        return (142, 182, 20)
    if val >= 0.1:
        return (164, 130, 76)
    if val >= 0:
        return (252, 254, 252)
    if val >= -1:
        return (4, 18, 60)

def get_dots(context):
    coordinates = []
    corners = ['CORNER_UL_LAT_PRODUCT',
               'CORNER_UL_LON_PRODUCT',
               'CORNER_UR_LAT_PRODUCT',
               'CORNER_UR_LON_PRODUCT',
               'CORNER_LL_LAT_PRODUCT',
               'CORNER_LL_LON_PRODUCT',
               'CORNER_LR_LAT_PRODUCT',
               'CORNER_LR_LON_PRODUCT']
    for line in context:
        line = line.strip()
        if line[0:21] in corners:
            coordinates.append(float(line[24:]))
    array_coord = np.array([coordinates[0::2], coordinates[1::2]])
    return {'UL': coordinates[0:2],
            'UR': coordinates[2:4],
            'LL': coordinates[4:6],
            'LR': coordinates[6:8],}

def delta(dots):
    delta_lat = abs(float(dots['UL'][0]) - float(dots['LR'][0]))
    delta_lon = abs(float(dots['LL'][1]) - float(dots['UR'][1]))
    return [delta_lat, delta_lon]

data = open("LE07_L2SP_041036_20021201_20200916_02_T1_MTL.txt", 'r').readlines()

b2 = Image.open("LE07_L2SP_041036_20021201_20200916_02_T1_SR_B2.TIF")

pixwd, pixht = b2.size

lat, lon = delta(get_dots(data))

d_lat = lat/pixht
d_lon = lon/pixwd

y = 34.081249
x = -118.246150


lat_y = int(abs(get_dots(data)['UL'][0] - y)/d_lat)
lon_x = int(abs(get_dots(data)['LL'][1] - x)/d_lon)
print(lon_x, lat_y)
print(d_lat, d_lon)
UL = [(lon_x-800), (lat_y-800)]
LR = [(lon_x+800), (lat_y+800)]
box = (UL[0], UL[1], LR[0], LR[1])
cropped = b2.crop(box)

cropped.save("city.png", "PNG")

b3 = Image.open("LE07_L2SP_041036_20021201_20200916_02_T1_SR_B3.TIF").crop(box)
b4 = Image.open("LE07_L2SP_041036_20021201_20200916_02_T1_SR_B4.TIF").crop(box)

mat_b3 = np.array(b3)
mat_b4 = np.array(b4)
mat_ndvi = (mat_b4 - mat_b3)/ (mat_b4 + mat_b3)

NDVI = Image.new("RGB", b3.size, color=(255, 255, 255))


for x in range(len(mat_ndvi)):
    for y in range(len(mat_ndvi[x])):
        NDVI.putpixel((y, x), get_color(mat_ndvi[x][y]))
NDVI.save("NDVI.png", "PNG")


