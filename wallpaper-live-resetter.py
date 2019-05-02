from time import localtime as lt
import PIL, PIL.Image, PIL.ImageDraw, PIL.ImageFont, os, ctypes, time

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
def formatTimeString(string) -> str: #returns a formatted string
    timeNow = localtime()
    if (len(str(timeNow['second'])) == 1):
        timeNow['second'] = '0' + str(timeNow['second'])
    if (len(str(timeNow['minute'])) == 1):
        timeNow['minute'] = '0' + str(timeNow['minute'])
    replaceWith = [ #I bet there is a better way to iterate through this but, whatever, its not like this is big 1000 client prod server code
        ['%year%', timeNow['year']],
        ['%month%', timeNow['month']],
        ['%day%', timeNow['day']],
        ['%hour%', timeNow['hour_12HR']],
        ['%hour24%', timeNow['hour_24HR']],
        ['%pm/am%', timeNow['pm/am']],
        ['%minute%', timeNow['minute']],
        ['%second%', timeNow['second']],
        ['%weekday%', timeNow['weekday']],
        ['%yearday%', timeNow['yearday']],
        ['%dst%', timeNow['daylightsavingtime']],
    ]
    for each in range(len(replaceWith)):
        string = string.replace(str(replaceWith[each][0]), str(replaceWith[each][1]))
    return string
def getPresetData() -> dict:
    data = {}
    presetFileData = str(open('./presets.txt').read())
    for each in range(len(presetFileData.split('\n'))):
        each = presetFileData.split('\n')[each]
        data[each.split(':')[0]] = each.split(':')[1]
    return data
def main() -> None:
    presetData = getPresetData()
    image = PIL.Image.open(presetData['localWallpaperPath'])
    outputPath = os.path.normpath(os.getcwd() + '/output.png')
    textFormat = str(open('./format.txt').read())
    textFormat = formatTimeString(textFormat)
    drawSurface = PIL.ImageDraw.Draw(image)
    font = PIL.ImageFont.truetype(presetData['fontPath'], int(image.size[1] / 12))
    for each in range(len(textFormat.split('\n'))):
        text = textFormat.split('\n')[each]
        textSize = drawSurface.textsize(text, font = font)
        textCoords = [image.size[0] - textSize[0] - 10, (each * textSize[1]) - 10]
        drawSurface.text(textCoords, text, (255, 255, 255), font = font)
    image.save(outputPath)
    ctypes.windll.user32.SystemParametersInfoW(20, 0, outputPath, 0)

while (1):
    main()
    time.sleep(30)