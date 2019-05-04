from time import localtime as lt
import PIL, PIL.Image, PIL.ImageDraw, PIL.ImageFont, os, ctypes, time, math

def localtime() -> dict: #returns the details about the local time in a dict
    ENDTIMEDICT = {}
    LOCALTIME = lt()
    for partition in range(len(LOCALTIME)):
        if (partition == 0):
            ENDTIMEDICT['year'] = LOCALTIME[partition]
        elif (partition == 1):
            ENDTIMEDICT['month'] = LOCALTIME[partition]
        elif (partition == 2):
            ENDTIMEDICT['day'] = LOCALTIME[partition]
        elif (partition == 3):
            ENDTIMEDICT['hour_24HR'] = LOCALTIME[partition]
            ENDTIMEDICT['hour_12HR'] = int(LOCALTIME[partition])
            if (int(ENDTIMEDICT['hour_24HR'] > 12)):
                ENDTIMEDICT['hour_12HR'] = int(LOCALTIME[partition]) - 12
                ENDTIMEDICT['pm/am'] = 'pm'
            else:
                ENDTIMEDICT['pm/am'] = 'am'
        elif (partition == 4):
            ENDTIMEDICT['minute'] = LOCALTIME[partition]
        elif (partition == 5):
            ENDTIMEDICT['second'] = LOCALTIME[partition]
        elif (partition == 6):
            ENDTIMEDICT['weekday'] = LOCALTIME[partition]
        elif (partition == 7):
            ENDTIMEDICT['yearday'] = LOCALTIME[partition]
        elif (partition == 8):
            ENDTIMEDICT['daylightsavingtime'] = bool(int(LOCALTIME[partition]))
    return ENDTIMEDICT
def getPresetData() -> dict:
    data = {}
    presetFileData = str(open('./presets.txt').read())
    for each in range(len(presetFileData.split('\n'))):
        each = presetFileData.split('\n')[each]
        data[each.split(':')[0]] = each.split(':')[1]
    return data

#this is code I got from https://stackoverflow.com/questions/32504246/draw-ellipse-in-python-pil-with-line-thickness and its not mine.
def draw_ellipse(image, bounds, width=1, outline='white', antialias=4):
    """Improved ellipse drawing function, based on PIL.ImageDraw."""

    # Use a single channel image (mode='L') as mask.
    # The size of the mask can be increased relative to the imput image
    # to get smoother looking results. 

    Image = PIL.Image
    ImageDraw = PIL.ImageDraw

    mask = Image.new(
        size=[int(dim * antialias) for dim in image.size],
        mode='L', color='black')
    draw = ImageDraw.Draw(mask)

    # draw outer shape in white (color) and inner shape in black (transparent)
    for offset, fill in (width/-2.0, 'white'), (width/2.0, 'black'):
        left, top = [(value + offset) * antialias for value in bounds[:2]]
        right, bottom = [(value - offset) * antialias for value in bounds[2:]]
        draw.ellipse([left, top, right, bottom], fill=fill)

    # downsample the mask using PIL.Image.LANCZOS 
    # (a high-quality downsampling filter).
    mask = mask.resize(image.size, Image.LANCZOS)
    # paste outline color to input image through the mask
    image.paste(outline, mask=mask)

def findCoordsOfHandEdges(centerX, centerY, radius, angle) -> int: #yes this is my code, yes im proud of it, yes it almost gave me a heart attack making it
    coords = [0, 0] #the top of the screen is 0 degrees/north = 0deg
    a = radius * math.sin(math.radians(angle + 90)) #opposite side to the angle
    b = radius * math.cos(math.radians(angle + 90)) #adjacent side to the angle
    b = centerX - b
    a = centerY - a
    coords = [b, a]
    return coords
def main() -> None:
    presetData = getPresetData()
    image = PIL.Image.open(presetData['localWallpaperPath'])
    outputPath = os.path.normpath(os.getcwd() + '/output.png')
    drawSurface = PIL.ImageDraw.Draw(image)
    font = PIL.ImageFont.truetype(presetData['fontPath'], int(image.size[1] / 12))

    lineColor = 'white'
    clockSize = int(image.size[1] / 2)
    ellipseCoords = [int((image.size[0] - clockSize) / 2), int((image.size[1] - clockSize) / 2), int((image.size[0] - clockSize) / 2) + clockSize, int((image.size[1] - clockSize) / 2) + clockSize]
    draw_ellipse(image, (ellipseCoords[0], ellipseCoords[1], ellipseCoords[2], ellipseCoords[3]), outline = lineColor, width = int(clockSize / 20))
    lineSize = int(clockSize / 20)
    lineHeight = int(clockSize / 10)
    drawSurface.line([int(image.size[0] / 2), int(ellipseCoords[1]), int(image.size[0] / 2), int(ellipseCoords[1] + lineHeight)], fill = lineColor, width = lineSize) #top middle hour line (12:00)
    drawSurface.line([int(image.size[0] / 2), int(ellipseCoords[1] + clockSize), int(image.size[0] / 2), int(ellipseCoords[1] - lineHeight + clockSize)], fill = lineColor, width = lineSize) #bottom middle hour line (6:00)
    drawSurface.line([int(ellipseCoords[0]), int(image.size[1] / 2), int(ellipseCoords[0] + lineHeight), int(image.size[1] / 2)], fill = lineColor, width = lineSize) #left center hour line (9:00)
    drawSurface.line([int(ellipseCoords[0] + clockSize), int(image.size[1] / 2), int(ellipseCoords[0] - lineHeight + clockSize), int(image.size[1] / 2)], fill = lineColor, width = lineSize) #right center hour line (3:00)

    timeNow = localtime()
    clockHandCenterCoords = [int(image.size[0] / 2), int(image.size[1] / 2)]
    minuteHandAngle, hourHandAngle = int((timeNow['minute'] / 60) * 360), int((timeNow['hour_12HR'] / 12) * 360)
    tmpvar1 = findCoordsOfHandEdges(clockHandCenterCoords[0], clockHandCenterCoords[1], int(clockSize / 3), hourHandAngle) #just a temporary variablle used to store the coordinates of the edge of the hour hand
    hourHandCoords = [clockHandCenterCoords[0], clockHandCenterCoords[1], tmpvar1[0], tmpvar1[1]]
    tmpvar2 = findCoordsOfHandEdges(clockHandCenterCoords[0], clockHandCenterCoords[1], int(clockSize / 2), minuteHandAngle) #just a temporary variablle used to store the coordinates of the edge of the minute hand
    minuteHandCoords = [clockHandCenterCoords[0], clockHandCenterCoords[1], tmpvar2[0], tmpvar2[1]]
    drawSurface.line([*hourHandCoords], fill = lineColor, width = lineSize) #hour hand
    drawSurface.line([*minuteHandCoords], fill = lineColor, width = lineSize) #hour hand

    image.save(outputPath)
    ctypes.windll.user32.SystemParametersInfoW(20, 0, outputPath, 0)

while (1):
    main()
    time.sleep(30)