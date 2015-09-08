"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from django.shortcuts import render_to_response
from datetime import datetime

YOUR_INFO = {
    'name' : 'Your name',
    'bio' : 'What\'s your deal? What do you do?',
    'email' : '', # Leave blank if you'd prefer not to share your email with other conference attendees
    'twitter_username' : 'tweettweet', # No @ symbol, just the handle.
    'github_username' : "fetchpush", 
    'headshot_url' : '', # Link to your GitHub, Twitter, or Gravatar profile image.
}
    
def home(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/base.html',
        context_instance = RequestContext(request,
            {
                'attendee' : YOUR_INFO,    
                'year': datetime.now().year,
            })
    )

def webcat(request, imgname=None, maxLen=100.0, clr=True, fontSize=7):
    """
    Based on http://github.com/hit9/img2txt.git
    """

    import sys

    from PIL import Image
    import cStringIO
    import urllib

    if imgname is None:
        # imgname = "/Users/ajna/Code/YourDjangoSiteResume/cats-animals-kittens-background.jpg"
        imgname = "http://loremflickr.com/320/240/kitten"

    # img = Image.open(imgname)
    img = Image.open(cStringIO.StringIO(urllib.urlopen(imgname).read()))
    color_webcat = None
    webcat = None


    # resize to: the max of the img is maxLen

    width, height = img.size
    rate = maxLen / max(width, height)
    width = int(rate * width)  # cast to int

    height = int(rate * height)

    img = img.resize((width, height))


    # get pixels
    pixel = img.load()

    # grayscale
    color = "MNHQ$OC?7>!:-;. "

    webcat = ""

    # for h in xrange(height):  # first go through the height,  otherwise will roate
    #     for w in xrange(width):
    #         rgb = pixel[w, h]
    #         if clr:
    #             color_webcat += "<span style=\"color:rgb" + str(rgb) + \
    #                 ";\">▇</span>"
    #         else:
    #             webcat += color[int(sum(rgb) / 3.0 / 256.0 * 16)]
    #     webcat += "\n"
    #

    if clr:
        color_webcat = [[('\xe2\x96\x87', str(pixel[w, h])) for w in xrange(width)] for h in xrange(height)]
        # color_webcat = [[(color[int(sum(pixel[w, h]) / 3.0 / 256.0 * 16)], str(pixel[w, h])) for w in xrange(width)] for h in xrange(height)]
    # wrappe with html
    else:
        webcat = '\n'.join(
            [''.join(map(str,[color[int(sum(pixel[w, h]) / 3.0 / 256.0 * 16)]
                              for w in xrange(width)]))
             for h in xrange(height)])



    return render_to_response('app/webcat.html', context={"font_size": fontSize,
                                                          "webcat": webcat,
                                                          "color_webcat": color_webcat,
                                                          'color': clr,
                                                          })