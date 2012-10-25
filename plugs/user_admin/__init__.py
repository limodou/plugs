def _get_portrait_image_filename(id):
    import os
    return os.path.join('portraits', str(id) + '.tmp' + '.jpg')

def _get_portrait_image_thumbnail(id, size=50):
    import os
    return os.path.join('portraits', str(id) + '.%dx%d' % (size, size) + '.jpg')

def get_user_image(user, size=50):
    from uliweb.contrib.staticfiles import url_for_static
    from uliweb import functions
    import os
    
    if user:
        image = functions.get_filename(_get_portrait_image_thumbnail(user.id, size))
        if os.path.exists(image):
            image_url = functions.get_href(_get_portrait_image_thumbnail(user.id, size))
            return image_url

    return functions.url_for_static('images/user%dx%d.jpg' % (size, size))
    
