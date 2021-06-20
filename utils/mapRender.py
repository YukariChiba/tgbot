import matplotlib.pyplot as plt
import numpy as np
import math
import requests
from io import BytesIO
from PIL import Image


def deg2num(lat_deg, lon_deg, zoom):
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = (lon_deg + 180.0) / 360.0 * n
    ytile = (1.0 - math.log(math.tan(lat_rad) +
                            (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n
    return (xtile, ytile)


def num2deg(xtile, ytile, zoom):
    n = 2.0 ** zoom
    lon_deg = xtile / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
    lat_deg = math.degrees(lat_rad)
    return (lat_deg, lon_deg)


def getImageCluster(lat_deg, lon_deg, lat_deg2, lon_deg2, zoom):
    smurl = r"https://a.tile.openstreetmap.org/{0}/{1}/{2}.png"
    xmax, ymin = deg2num(lat_deg2, lon_deg2, zoom)
    xmin, ymax = deg2num(lat_deg, lon_deg, zoom)
    xmax = math.ceil(xmax)
    ymax = math.ceil(ymax)
    xmin = math.floor(xmin)
    ymin = math.floor(ymin)
    Cluster = Image.new('RGB', ((xmax-xmin+1)*256-1, (ymax-ymin+1)*256-1))
    for xtile in range(xmin, xmax+1):
        for ytile in range(ymin,  ymax+1):
            try:
                imgurl = smurl.format(zoom, xtile, ytile)
                imgstr = requests.get(imgurl)
                tile = Image.open(BytesIO(imgstr.content))
                Cluster.paste(tile, box=((xtile-xmin)*256,  (ytile-ymin)*255))
            except:
                tile = None
    return Cluster


if __name__ == '__main__':
    a = getImageCluster(38.5, -77.04, 0.02,  0.05, 13)
    fig = plt.figure()
    fig.patch.set_facecolor('white')
    plt.imshow(np.asarray(a))
    plt.show()
