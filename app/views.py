import cStringIO
import urllib
from PIL import Image
from django.shortcuts import render_to_response
from django.http import HttpResponse


def home(request):
    return render_to_response('app/base.html')

def tracking(request):
    return render_to_response('app/tracking.html')


def webcat(request, image_url=None, max_length=100.0, color=True, font_size=7):
    """
    Based on http://github.com/hit9/img2txt.git
    """
    color_webcat = None
    webcat = None

    if image_url is None:
        image_url = "http://loremflickr.com/100/75/kitten"

    img = Image.open(cStringIO.StringIO(urllib.urlopen(image_url).read()))

    width, height = img.size
    rate = max_length / max(width, height)
    width = int(rate * width)
    height = int(rate * height)
    img = img.resize((width, height))

    pixels = img.load()

    # grayscale
    char_set = "MNHQ$OC?7>!:-;. "

    if color:
        color_webcat = [[('\xe2\x96\x87', str(pixels[w, h]))
                         for w in xrange(width)]
                        for h in xrange(height)]
    else:
        webcat = '\n'.join(
            [''.join(map(str, [char_set[int(sum(pixels[w, h]) / 3.0 / 256.0 * 16)]
                               for w in xrange(width)]))
             for h in xrange(height)])


    return render_to_response('app/webcat.html', context={"font_size": font_size,
                                                          "webcat": webcat,
                                                          "color_webcat": color_webcat,
                                                          'color': color,
                                                          })


def verify(request):
    return HttpResponse("loaderio-f45938ab864b663eaacfcb8eb41ca3e5")