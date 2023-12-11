import io
import os
import time
from datetime import datetime

import PySimpleGUI as sg
import mss
import mss.tools
from PIL import Image, ImageChops

# messy global state stuff
monitorNumber = 1
homeDir = os.path.expanduser('~')
idstring = (datetime.now()).strftime("%Y_%m_%d_%H%M")

# screengrabber instance
sct = mss.mss()
sct.compression_level = 0

# image data for toggle switch
toggle_btn_off = b'iVBORw0KGgoAAAANSUhEUgAAACgAAAAoCAYAAACM/rhtAAAABmJLR0QA/wD/AP+gvaeTAAAED0lEQVRYCe1WTWwbRRR+M/vnv9hO7BjHpElMKSlpqBp6gRNHxAFVcKM3qgohQSqoqhQ45YAILUUVDRxAor2VAweohMSBG5ciodJUSVqa/iikaePEP4nj2Ovdnd1l3qqJksZGXscVPaylt7Oe/d6bb9/svO8BeD8vA14GvAx4GXiiM0DqsXv3xBcJU5IO+RXpLQvs5yzTijBmhurh3cyLorBGBVokQG9qVe0HgwiXLowdy9aKsY3g8PA5xYiQEUrsk93JTtjd1x3siIZBkSWQudUK4nZO1w3QuOWXV+HuP/fL85klAJuMCUX7zPj4MW1zvC0Ej4yMp/w++K2rM9b70sHBYCjo34x9bPelsgp/XJksZ7KFuwZjr3732YcL64ttEDw6cq5bVuCvgy/sje7rT0sI8PtkSHSEIRIKgCQKOAUGM6G4VoGlwiqoVd2Za9Vl8u87bGJqpqBqZOj86eEHGNch+M7otwHJNq4NDexJD+59RiCEQG8qzslFgN8ibpvZNsBifgXmFvJg459tiOYmOElzYvr2bbmkD509e1ylGEZk1Y+Ssfan18n1p7vgqVh9cuiDxJPxKPT3dfGXcN4Tp3dsg/27hUQs0qMGpRMYjLz38dcxS7Dm3nztlUAb38p0d4JnLozPGrbFfBFm79c8hA3H2AxcXSvDz7/+XtZE1kMN23hjV7LTRnKBh9/cZnAj94mOCOD32gi2EUw4FIRUMm6LGhyiik86nO5NBdGRpxYH14bbjYfJteN/OKR7UiFZVg5T27QHYu0RBxoONV9W8KQ7QVp0iXdE8fANUGZa0QAvfhhXlkQcmjJZbt631oIBnwKmacYoEJvwiuFgWncWnXAtuVBBEAoVVXWCaQZzxmYuut68b631KmoVBEHMUUrJjQLXRAQVSxUcmrKVHfjWWjC3XOT1FW5QrWpc5IJdQhDKVzOigEqS5dKHMVplnNOqrmsXqUSkn+YzWaHE9RW1FeXL7SKZXBFUrXW6jIV6YTEvMAUu0W/G3kcxPXP5ylQZs4fa6marcWvvZfJu36kuHjlc/nMSuXz+/ejxgqPFpuQ/xVude9eu39Jxu27OLvBGoMjrUN04zrNMbgVmOBZ96iPdPZmYntH5Ls76KuxL9NyoLA/brav7n382emDfHqeooXyhQmARVhSnAwNNMx5bu3V1+habun5nWdXhwJZ2C5mirTesyUR738sv7g88UQ0rEkTDlp+1wwe8Pf0klegUenYlgyg7bby75jUTITs2rhCAXXQ2vwxz84vlB0tZ0wL4NEcLX/04OrrltG1s8aOrHhk51SaK0us+n/K2xexBxljcsm1n6x/Fuv1PCWGiKOaoQCY1Vb9gWPov50+fdEqd21ge3suAlwEvA14G/ucM/AuppqNllLGPKwAAAABJRU5ErkJggg=='
toggle_btn_on = b'iVBORw0KGgoAAAANSUhEUgAAACgAAAAoCAYAAACM/rhtAAAABmJLR0QA/wD/AP+gvaeTAAAD+UlEQVRYCe1XzW8bVRCffbvrtbP+2NhOD7GzLm1VoZaPhvwDnKBUKlVyqAQ3/gAkDlWgPeVQEUCtEOIP4AaHSI0CqBWCQyXOdQuRaEFOk3g3IMWO46+tvZ+PeZs6apq4ipON1MNafrvreTPzfvub92bGAOEnZCBkIGQgZOClZoDrh25y5pdjruleEiX+A+rCaQo05bpuvJ/+IHJCSJtwpAHA/e269g8W5RbuzF6o7OVjF8D3Pr4tSSkyjcqfptPDMDKSleW4DKIggIAD5Yf+Oo4DNg6jbUBlvWLUNutAwZu1GnDjzrcXzGcX2AHw/emFUV6Sfk0pqcKpEydkKSo9q3tkz91uF5aWlo1Gs/mYc+i7tz4//19vsW2AU9O381TiioVCQcnlRsWeQhD3bJyH1/MiFLICyBHiuzQsD1arDvypW7DR9nzZmq47q2W95prm+I9fXfqXCX2AF2d+GhI98Y8xVX0lnxvl2UQQg0csb78ag3NjEeD8lXZ7pRTgftmCu4864OGzrq+5ZU0rCa3m+NzXlzvoAoB3+M+SyWQuaHBTEzKMq/3BMbgM+FuFCDBd9kK5XI5PJBKqLSev+POTV29lKB8rT0yMD0WjUSYLZLxzNgZvIHODOHuATP72Vwc6nQ4Uiw8MUeBU4nHS5HA6TYMEl02wPRcZBJuv+ya+UCZOIBaLwfCwQi1Mc4QXhA+PjWRkXyOgC1uIhW5Qd8yG2TK7kSweLcRGKKVnMNExWWBDTQsH9qVmtmzjiThQDs4Qz/OUSGTwcLwIQTLW58i+yOjpXDLqn1tgmDzXzRCk9eDenjo9yhvBmlizrB3V5dDrNTuY0A7opdndStqmaQLPC1WCGfShYRgHdLe32UrV3ntiH9LliuNrsToNlD4kruN8v75eafnSgC6Luo2+B3fGKskilj5muV6pNhk2Qqg5v7lZ51nBZhNBjGrbxfI1+La5t2JCzfD8RF1HTBGJXyDzs1MblONulEqPDVYXgwDIfNx91IUVbAbY837GMur+/k/XZ75UWmJ77ou5mfM1/0x7vP1ls9XQdF2z9uNsPzosXPNFA5m0/EX72TBSiqsWzN8z/GZB08pWq9VeEZ+0bjKb7RTD2i1P4u6r+bwypo5tZUumEcDAmuC3W8ezIqSGfE6g/sTd1W5p5bKjaWubrmWd29Fu9TD0GlYlmTx+8tTJoZeqYe2BZC1/JEU+wQR5TVEUPptJy3Fs+Vkzgf8lemqHumP1AnYoMZSwsVEz6o26i/G9Lgitb+ZmLu/YZtshfn5FZDPBCcJFQRQ+8ih9DctOFvdLIKHH6uUQnq9yhFu0bec7znZ+xpAGmuqef5/wd8hAyEDIQMjAETHwP7nQl2WnYk4yAAAAAElFTkSuQmCC'


def validInt(text):
    if len(text) == 1 and text in '+-':
        return True
    else:
        try:
            number = int(text)
            return True
        except:
            return False


def validFloat(text):
    if len(text) == 1 and text in '+-':
        return True
    else:
        try:
            number = float(text)
            return True
        except:
            return False


def imagesEqual(imga,imgb):
    if len(set(ImageChops.difference(imga, imgb).getdata())) > 1:
        return False
    else:
        return True


def millis():
    return round(time.time() * 1000)


def convert_from_bytes(im):
    return Image.frombytes('RGB', im.size, im.bgra, 'raw', 'BGRX')


def main():
    # setup initial state
    start = millis()
    now = start
    then = start
    recording = False
    recordDeltas = False
    recInterval = 1000

    xmin = sct.monitors[0]['left']
    ymin = sct.monitors[0]['top']
    wmax = sct.monitors[0]['width']
    hmax = sct.monitors[0]['height']

    mon = sct.monitors[monitorNumber]
    x0 = mon['left']
    y0 = mon['top']
    w = mon['width']
    h = mon['height']
    displaySize = (400, 440)
    print(displaySize)
    exportDir = homeDir

    sg.theme("DarkBlue2")
    layout = [
        [
            sg.Text('left', auto_size_text=False, size=3),
            sg.In(key='-X0-', size=(10, 1), default_text=x0, enable_events=True),
            sg.Text('width', auto_size_text=False, size=5),
            sg.In(key='-W-', size=(10, 1), default_text=w, enable_events=True)
        ],
        [
            sg.Text('top', auto_size_text=False, size=3),
            sg.In(key='-Y0-', size=(10, 1), default_text=y0, enable_events=True),
            sg.Text('height', auto_size_text=False, size=5),
            sg.In(key='-H-', size=(10, 1), default_text=h, enable_events=True)
        ],
        [
            sg.HorizontalSeparator(color='gray')
        ],
        [
            sg.Text('recording interval (ms)', auto_size_text=False, size=18),
            sg.In(key='-dT-', size=(14, 1), default_text=recInterval, enable_events=True)
        ],
        [
            sg.Text('output file directory', auto_size_text=False, size=(18, 1)),
            sg.Input(key='-DIR-', enable_events=True, visible=False),
            sg.FolderBrowse(target='-DIR-', size=(12, 1), button_color='gray', initial_folder=homeDir)
        ],
        [
            sg.HorizontalSeparator(color='gray')
        ],
        [
            sg.Text('save deltas', size=(10, 1)),
            sg.Button(
                image_data=toggle_btn_off, key='-DELTA-', size=(12, 1),
                button_color=(sg.theme_background_color(), sg.theme_background_color()), border_width=0,
                metadata=False
            ),
            sg.Button('start', key='-START-', size=(4, 1), button_color='green'),
            sg.Button('stop', key='-STOP-', size=(4, 1), button_color='red')
        ],
        [
            sg.Image(key="-IMAGE-", background_color=sg.theme_background_color(), expand_x=True, expand_y=True)
        ],
        [
            sg.Text('ready...', key='-STATUS-', expand_x=True, auto_size_text=True)
        ]
    ]

    # create window
    # TODO: find a better way to calculate the initial window size tuple
    window = sg.Window("Pyclops Screencapture", layout, resizable=True, finalize=True, size=(400,440))
    window.bind('<Configure>', '-CONFIG-')

    # initialize captures
    capture = sct.grab({'left': x0, 'top': y0, 'width': w, 'height': h})
    capimage = convert_from_bytes(capture)
    oldcapimg = capimage

    # enter the sole event loop
    while True:
        # check for user events
        event, values = window.read(timeout=1)
        updateBounds = False
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        elif event == '-START-':
            # reset zero-time to when user clicks start
            idstring = (datetime.now()).strftime("%Y_%m_%d_%H%M")
            start = millis()
            now = start
            then = start

            # update state
            window['-STATUS-'].update('recording started')
            recording = True

            # minimize cap window?
            # window.minimize()

        elif event == '-STOP-':
            window['-STATUS-'].update('recording stopped')
            recording = False

        elif event == '-CONFIG-':
            displaySize = window['-IMAGE-'].get_size()

        elif event == '-DELTA-':
            recordDeltas = not recordDeltas
            window['-DELTA-'].metadata = not window['-DELTA-'].metadata
            window['-DELTA-'].update(image_data=toggle_btn_on if window['-DELTA-'].metadata else toggle_btn_off)
            if recordDeltas:
                window['-STATUS-'].update('recording only frames with changes')
            else:
                window['-STATUS-'].update('recording all frames')

        elif event == '-DIR-':
            exportDir = values['-DIR-']
            window['-STATUS-'].update('saving captures to ' + exportDir)

        elif event == '-dT-':
            text = values['-dT-']
            if validFloat(text):
                recInterval = float(text)
                window['-STATUS-'].update('recording interval set to ' + str(recInterval) + ' milliseconds')

        elif event == '-X0-':
            text = values['-X0-']
            if validInt(text):
                x0 = int(text)
                updateBounds = True
        elif event == '-Y0-':
            text = values['-Y0-']
            if validInt(text):
                y0 = int(text)
                updateBounds = True
        elif event == '-W-':
            text = values['-W-']
            if validInt(text):
                w = int(text)
                updateBounds = True
        elif event == '-H-':
            text = values['-H-']
            if validInt(text):
                h = int(text)
                updateBounds = True

        if updateBounds:
            x0 = max(x0, xmin)
            y0 = max(y0, ymin)
            x0 = min(x0, wmax - 1)
            y0 = min(y0, hmax - 1)

            w = max(w, 1)
            h = max(h, 1)
            w = min(w, wmax)
            h = min(h, hmax)

            if (x0 + w > wmax):
                w = wmax - x0
            if (y0 + h > hmax):
                h = hmax - y0

            window['-STATUS-'].update('updated capture area bounds')

        now = millis()

        # grab capture
        capture = sct.grab({'left': x0, 'top': y0, 'width': w, 'height': h})
        capimage = convert_from_bytes(capture)

        # decide to save or not - keep track of time and the diff to check future capture changes against
        save = False
        if recording and ((now - then) > recInterval):
            if recordDeltas and not imagesEqual(capimage, oldcapimg):
                oldcapimg = capimage
                save = True
            elif not recordDeltas:
                save = True
            then = now

        # save file if necessary
        if save:
            window['-STATUS-'].update('captured screen at t = ' + str(now - start) + 'ms')
            fname = os.path.join(exportDir, idstring + "_" + str(now - start) + '.png')
            print(fname)
            mss.tools.to_png(capture.rgb, capture.size, output=fname)

        # update preview graphic
        dispImage = capimage.copy()
        dispImage.thumbnail(displaySize, resample=Image.Resampling.BICUBIC)
        dispBytes = io.BytesIO()
        dispImage.save(dispBytes, format="PNG", compress_level=0)
        window["-IMAGE-"].update(data=dispBytes.getvalue())

    window.close()


main()
