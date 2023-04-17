import json
import mysql.connector
import matplotlib.pyplot as plt
import numpy as np
import urllib.request
import matplotlib.image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from PIL import Image

def getImage(path, zoom=0.05):
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

data = json.load(open('db.json'))

mydb = mysql.connector.connect(
    host="localhost",
    user=data["user"],
    password=data["password"],
    port=data["port"],
    database=data["database"],
)
current_year = "22/23"
mycursor = mydb.cursor(dictionary=True)
mycursor.execute(
    f"SELECT PDEF FROM player WHERE SeasonYear = %s AND PDEF != 0",
    (current_year,))
pdef = mycursor.fetchall()
pdef_values = [t['PDEF'] for t in pdef]

mycursor.execute(
    f"SELECT RDEF FROM player WHERE SeasonYear = %s AND RDEF != 0",
    (current_year,))
rdef = mycursor.fetchall()
rdef_values = [t['RDEF'] for t in rdef]

mycursor.execute(
    f"SELECT NbaPlayerId FROM player WHERE SeasonYear = %s AND RDEF != 0",
    (current_year,))
player_id = mycursor.fetchall()
player_id_values = [t['NbaPlayerId'] for t in player_id]

url = "https://cdn.nba.com/headshots/nba/latest/1040x760/" + str(player_id_values[0]) + ".png?imwidth=1040&imheight=760"

x = rdef_values
y = pdef_values

paths = []
for i in range(len(player_id_values)):
    paths.append("assets/" + str(player_id_values[i]) + ".png")

fig, ax = plt.subplots()
ax.scatter(x, y)

for x0, y0, path in zip(x, y, paths):
    ab = AnnotationBbox(getImage(path), (x0, y0), frameon=False)
    ax.add_artist(ab)

plt.show()
