from django.db.models.fields.files import ImageField, ImageFieldFile
from PIL import Image
import os


def _add_thumb(s): # 3
    parts = s.split(".")
    parts.insert(-1, "thumb")
    if parts[-1].lower() not in ['jpeg', 'jpg']: # 4
        parts[-1] = 'jpg'
    return ".".join(parts)


class ThumbnailImageFieldFile(ImageFieldFile): # 5
    def _get_thumb_path(self): # 6
        return _add_thumb(self.path)
    thumb_path = property(_get_thumb_path)

    def _get_thumb_url(self): # 7
        return _add_thumb(self.url)
    thumb_url = property(_get_thumb_url)

    def save(self, name, content, save=True): # 8
        super(ThumbnailImageFieldFile, self).save(name, content, save) # 9
        img = Image.open(self.path)
        #img = img.convert('RGB')

        size = (128, 128)
        img.thumbnail(size, Image.ANTIALIAS) # 10
        background = Image.new('RGBA', size, (255, 255, 255, 0)) # 11
        background.paste(img, (int((size[0] - img.size[0]) / 2), int((size[1] - img.size[1]) / 2))) # 12
        background = background.convert('RGB')
        background.save(self.thumb_path, 'JPEG') # 13

    def delete(self, save=True): # 14
        if os.path.exists(self.thumb_path):
            os.remove(self.thumb_path)
        super(ThumbnailImageFieldFile, self).delete(save)


class ThumbnailImageField(ImageField): # 15
    attr_class = ThumbnailImageFieldFile # 16

    def __init__(self, thumb_width=128, thumb_height=128, *args, **kwargs): # 17
        self.thumb_width = thumb_width
        self.thumb_height = thumb_height
        super(ThumbnailImageField, self).__init__(*args, **kwargs) # 18
