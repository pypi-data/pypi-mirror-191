# -*- coding: utf-8 -*-
# This file is part of the cashbook-module from m-ds for Tryton.
# The COPYRIGHT file at the top level of this repository contains the
# full copyright notices and license terms.

import mimetypes, magic
from io import BytesIO
from PIL import Image, UnidentifiedImageError
from trytond.model import fields
from trytond.pool import Pool, PoolMeta
from trytond.config import config
from trytond.transaction import Transaction
from trytond.exceptions import UserError
from trytond.i18n import gettext
from trytond.pyson import Eval, Bool
from trytond.modules.cashbook.line import STATES, DEPENDS


store_prefix = config.get('cashbook', 'store_prefix', default='cashbook')
image_limit = config.get('cashbook', 'image_max_pixel', default='2000')
try :
    image_limit = int(image_limit)
    if image_limit < 100:
        image_limit = 100
    if image_limit > 10000:
        image_limit = 10000
except :
    image_limit = 2000


STATES2 = {}
STATES2.update(STATES)
DEPENDS2 = []
DEPENDS2.extend(DEPENDS)


class Line(metaclass=PoolMeta):
    __name__ = 'cashbook.line'

    media = fields.Binary(string='Image of PDF', filename='media_name',
        file_id='media_id', store_prefix=store_prefix,
        states=STATES2, depends=DEPENDS2)
    media_name = fields.Char(string='File name',
        states={
            'required': Bool(Eval('media')),
            'readonly': STATES2['readonly'],
        }, depends=DEPENDS2)
    media_id = fields.Char(string='File ID', readonly=True)
    media_mime = fields.Char(string='MIME', readonly=True)
    media_size = fields.Integer(string='File size', readonly=True)
    media_image = fields.Function(fields.Binary(string='Image', readonly=True,
        states={
            'invisible': ~Eval('media_mime', '').in_(['image/png', 'image/jpg', 'image/jpeg']),
        }, depends=['media_mime']),
        'on_change_with_media_image')

    @fields.depends('media', 'media_mime')
    def on_change_with_media_image(self, name=True):
        """ return binary if its a image
        """
        if (self.media_mime or '-').startswith('image/'):
            return self.media

    @classmethod
    def _identify_file(cls, data, mime=True):
        """ get file-type
        """
        return magic.from_buffer(data, mime=mime)

    @classmethod
    def _hr_file_size(cls, num, suffix="B"):
        """
        """
        for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
            if abs(num) < 1024.0:
                return f"{num:3.1f}{unit}{suffix}"
            num /= 1024.0
        return f"{num:.1f}Yi{suffix}"

    @classmethod
    def resize_image_file(cls, image_data):
        """ shrink image 'image_limit' pixel if its bigger
        """
        image_data2 = None
        with BytesIO(image_data) as fhdl:
            try :
                image = Image.open(fhdl, 'r')
            except UnidentifiedImageError:
                raise UserError(gettext('cashbook_media.msg_file_unknown_type'))

            (width, height) = image.size
            if (width > image_limit) or (height > image_limit):

                if width > height:
                    new_size = (image_limit, int(height * image_limit / width))
                else :
                    new_size = (int(width * image_limit / height), image_limit)

                # resize - fit in (image_limit x image_limit)
                img2 = image.resize(new_size, Image.LANCZOS)
                with BytesIO() as fhdl2:
                    img2.save(fhdl2, 'JPEG', optimize=True, quality=80)
                    fhdl2.seek(0)
                    image_data2 = fhdl2.read()
                del img2
            del image

        return image_data2

    @classmethod
    def get_media_info(cls, values):
        """ get mime-type, update file-name
        """
        if len(values['media'] or '') < 100:
            values['media'] = None
            values['media_mime'] = None
            values['media_size'] = None
            values['media_name'] = None
        else :
            values['media_mime'] = cls._identify_file(values['media'][:1024])

            # if its a image, resize it to fit in (image_limit x image_limit) pixel
            if values['media_mime'].startswith('image'):
                new_image = cls.resize_image_file(values['media'])
                if new_image is not None:
                    values['media'] = new_image
                    values['media_mime'] = cls._identify_file(values['media'][:1024])

            values['media_size'] = len(values['media'])
            file_ext = mimetypes.guess_extension(values['media_mime'])
            if 'media_name' in values.keys():
                if not values['media_name'].endswith(file_ext):
                    # cut extension
                    if values['media_name'][-4] == '.':
                        values['media_name'] = values['media_name'][:-4]
                    values['media_name'] = values['media_name'] + file_ext
        return values

    @classmethod
    def validate(cls, lines):
        """ deny invalid mime-types, file-sizes etc.
        """
        super(Line, cls).validate(lines)

        for line in lines:
            if line.media is not None:
                if line.media_size > 1024*1024*5:
                    raise UserError(gettext(
                        'cashbook_media.msg_file_too_big',
                        recname = line.rec_name,
                        ))
                if not line.media_mime in ['application/pdf',
                    'image/png', 'image/jpg', 'image/jpeg']:
                    raise UserError(gettext(
                        'cashbook_media.msg_file_invalid_mime',
                        recname = line.rec_name,
                        fmime = line.media_mime,
                        ))

    @classmethod
    def create(cls, vlist):
        """ add media-info
        """
        vlist = [x.copy() for x in vlist]
        for values in vlist:
            if 'media' in values.keys():
                values.update(cls.get_media_info(values))
        return super(Line, cls).create(vlist)

    @classmethod
    def write(cls, *args):
        """ update media-info
        """
        actions = iter(args)
        to_write = []
        for records, values in zip(actions, actions):
            if 'media' in values.keys():
                values.update(cls.get_media_info(values))

            to_write.extend([
                records,
                values,
                ])
        super(Line, cls).write(*to_write)

# end Line
