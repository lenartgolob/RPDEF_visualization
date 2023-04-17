import json
import mysql.connector
import matplotlib.pyplot as plt
import urllib.request
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from PIL import Image, ImageDraw, ImageOps
import os
import cv2
import numpy as np

def getImage(path, zoom=0.03):
    return OffsetImage(plt.imread(path), zoom=zoom)

def saveImages(player_id_values):
    for i in range(len(player_id_values)):
        if i > 625:
            img_missing = [76993, 2430, 101154, 1890, 101126, 202333, 201175, 101115, 203106, 979, 203544, 101128,
                           200761, 2222, 1905, 2557, 101142, 2203, 203144, 2202, 2742, 201611, 2584, 2229, 1628681,
                           1585]
            if player_id_values[i] not in img_missing:
                url = url = "https://cdn.nba.com/headshots/nba/latest/1040x760/" + str(
                    player_id_values[i]) + ".png?imwidth=1040&imheight=760"
                with urllib.request.urlopen(url) as url_response:
                    with open('./assets/' + str(player_id_values[i]) + '.png', 'wb') as img_file:
                        img_file.write(url_response.read())
                        img_file.close()
                print(i)
                url_response.close()

def crop_images():
    # Set the directory where your PNG files are located
    directory = './assets'

    # Loop through the PNG files in the directory
    for filename in os.listdir(directory):
        if filename.endswith('.png'):
            # Load the image using cv2
            image = cv2.imread(os.path.join(directory, filename), cv2.IMREAD_UNCHANGED)

            # Get the image dimensions
            height, width = image.shape[:2]

            # Define the center and radius of the circle
            center = (int(width / 2), int(height / 2))
            radius = min(center[0], center[1])

            # Create a mask with a white circle on a transparent background
            mask = np.zeros((height, width, 4), dtype=np.uint8)
            cv2.circle(mask, center, radius, (255, 255, 255, 255), -1)

            # Apply the mask to the image to crop it to a circle
            masked_image = cv2.bitwise_and(image, mask)

            # Save the cropped image as a new PNG file
            cropped_filename = os.path.splitext(filename)[0] + '_cropped.png'
            cv2.imwrite(os.path.join(directory, cropped_filename), masked_image)

def rpdef_graph(current_year, position, filename):
    data = json.load(open('db.json'))

    mydb = mysql.connector.connect(
        host="localhost",
        user=data["user"],
        password=data["password"],
        port=data["port"],
        database=data["database"],
    )
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute(
        f"SELECT PDEF FROM player WHERE SeasonYear = %s AND PDEF != 0 AND Position LIKE %s",
        (current_year, position,))
    pdef = mycursor.fetchall()
    pdef_values = [t['PDEF'] for t in pdef]

    mycursor.execute(
        f"SELECT RDEF FROM player WHERE SeasonYear = %s AND RDEF != 0 AND Position LIKE %s",
        (current_year, position,))
    rdef = mycursor.fetchall()
    rdef_values = [t['RDEF'] for t in rdef]

    mycursor.execute(
        f"SELECT NbaPlayerId FROM player WHERE SeasonYear = %s AND RDEF != 0 AND Position LIKE %s",
        (current_year, position,))
    player_id = mycursor.fetchall()
    player_id_values = [t['NbaPlayerId'] for t in player_id]

    x = rdef_values
    y = pdef_values

    paths = []
    for i in range(len(player_id_values)):
        paths.append("assets/" + str(player_id_values[i]) + "_cropped.png")

    fig, ax = plt.subplots(dpi=300)
    ax.scatter(x, y)

    for x0, y0, path in zip(x, y, paths):
        ab = AnnotationBbox(getImage(path), (x0, y0), frameon=False)
        ax.add_artist(ab)

    plt.title('RPDEF ~ Rim Perimeter Defensive Metric', pad=15, fontweight='bold')
    plt.xlabel('RDEF score')
    plt.ylabel('PDEF score')

    plt.show()
    fig.savefig(filename, dpi=300, bbox_inches='tight')

rpdef_graph("22/23", "%", "22-23-all")








