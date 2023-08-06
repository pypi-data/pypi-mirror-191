# -*- coding: utf-8 -*-
# This file is part of the cashbook-module from m-ds for Tryton.
# The COPYRIGHT file at the top level of this repository contains the
# full copyright notices and license terms.

from io import BytesIO
from PIL import Image
from trytond.tests.test_tryton import ModuleTestCase, with_transaction
from trytond.pool import Pool
from trytond.transaction import Transaction
from trytond.exceptions import UserError
from trytond.modules.cashbook.tests import CashbookTestCase
from datetime import date
from decimal import Decimal
from .img_data import img_data_png, dok_data_pdf, text_data


class LineTestCase(CashbookTestCase):
    'Test cashbook line module'
    module = 'cashbook_media'

    @with_transaction()
    def test_media_add_image(self):
        """ create cook/line, add png-file
        """
        pool = Pool()
        Book = pool.get('cashbook.book')
        Lines = pool.get('cashbook.line')

        types = self.prep_type()
        category = self.prep_category(cattype='in')
        company = self.prep_company()
        party = self.prep_party()
        book, = Book.create([{
            'name': 'Book 1',
            'btype': types.id,
            'company': company.id,
            'currency': company.currency.id,
            'number_sequ': self.prep_sequence().id,
            'start_date': date(2022, 5, 1),
            'lines': [('create', [{
                    'date': date(2022, 5, 1),
                    'description': 'Text 1',
                    'category': category.id,
                    'bookingtype': 'in',
                    'amount': Decimal('1.0'),
                    'party': party.id,
                },])],
            }])
        self.assertEqual(book.name, 'Book 1')
        self.assertEqual(len(book.lines), 1)
        self.assertEqual(book.state, 'open')

        # add image to line-1
        Lines.write(*[
            [book.lines[0]],
            {
                'media': img_data_png,
                'media_name': 'image.png',
            }])
        self.assertEqual(book.lines[0].media_size, 18428)
        self.assertEqual(book.lines[0].media_mime, 'image/png')
        self.assertEqual(book.lines[0].media_name, 'image.png')

        # replace image at line-1 by pdf
        Lines.write(*[
            [book.lines[0]],
            {
                'media': dok_data_pdf,
            }])
        self.assertEqual(book.lines[0].media_size, 8724)
        self.assertEqual(book.lines[0].media_mime, 'application/pdf')
        self.assertEqual(book.lines[0].media_name, 'image.png')

        # create line with pdf
        Book.write(*[
            [book],
            {
                'lines': [('create', [{
                    'date': date(2022, 5, 2),
                    'description': 'Text 2',
                    'category': category.id,
                    'bookingtype': 'in',
                    'amount': Decimal('1.0'),
                    'party': party.id,
                    'media': dok_data_pdf,
                    'media_name': 'data.pdf',
                    }])],
                }
            ])
        self.assertEqual(len(book.lines), 2)
        self.assertEqual(book.lines[1].media_size, 8724)
        self.assertEqual(book.lines[1].media_mime, 'application/pdf')
        self.assertEqual(book.lines[1].media_name, 'data.pdf')

    @with_transaction()
    def test_media_add_invalid_file(self):
        """ create cook/line, add txt-file
        """
        pool = Pool()
        Book = pool.get('cashbook.book')
        Lines = pool.get('cashbook.line')

        types = self.prep_type()
        category = self.prep_category(cattype='in')
        company = self.prep_company()
        party = self.prep_party()
        book, = Book.create([{
            'name': 'Book 1',
            'btype': types.id,
            'company': company.id,
            'currency': company.currency.id,
            'number_sequ': self.prep_sequence().id,
            'start_date': date(2022, 5, 1),
            'lines': [('create', [{
                    'date': date(2022, 5, 1),
                    'description': 'Text 1',
                    'category': category.id,
                    'bookingtype': 'in',
                    'amount': Decimal('1.0'),
                    'party': party.id,
                },])],
            }])
        self.assertEqual(book.name, 'Book 1')
        self.assertEqual(len(book.lines), 1)
        self.assertEqual(book.state, 'open')

        # add invalid file
        self.assertRaisesRegex(UserError,
            "The file type 'text/plain' of the record '05/02/2022|Rev|1.00 usd|Text 2 [Cat1]' is not allowed. (allowed: PNG, JPG, PDF)",
            Book.write,
            *[
                [book],
                {
                    'lines': [('create', [{
                        'date': date(2022, 5, 2),
                        'description': 'Text 2',
                        'category': category.id,
                        'bookingtype': 'in',
                        'amount': Decimal('1.0'),
                        'party': party.id,
                        'media': text_data,
                        'media_name': 'text.txt',
                        }])],
                }
            ])

        # replace image at line-1 by invalid file
        self.assertRaisesRegex(UserError,
            "The file type 'text/plain' of the record '05/02/2022|Rev|1.00 usd|Text 2 [Cat1]' is not allowed. (allowed: PNG, JPG, PDF)",
            Lines.write,
            *[
                [book.lines[0]],
                {
                    'media': text_data,
                    'media_name': 'text.txt',
                },
            ])

    @with_transaction()
    def test_media_add_big_file(self):
        """ create cook/line, add big png-file
        """
        pool = Pool()
        Book = pool.get('cashbook.book')
        Lines = pool.get('cashbook.line')

        types = self.prep_type()
        category = self.prep_category(cattype='in')
        company = self.prep_company()
        party = self.prep_party()

        book, = Book.create([{
            'name': 'Book 1',
            'btype': types.id,
            'company': company.id,
            'currency': company.currency.id,
            'number_sequ': self.prep_sequence().id,
            'start_date': date(2022, 5, 1),
            'lines': [('create', [{
                    'date': date(2022, 5, 1),
                    'description': 'Text 1',
                    'category': category.id,
                    'bookingtype': 'in',
                    'amount': Decimal('1.0'),
                    'party': party.id,
                },])],
            }])
        self.assertEqual(book.name, 'Book 1')
        self.assertEqual(len(book.lines), 1)
        self.assertEqual(book.state, 'open')

        # construct image
        with BytesIO() as fhdl:
            img1 = Image.new('RGB', (3200, 1340))
            img1.save(fhdl, 'PNG', optimize=True)
            del img1

            fhdl.seek(0)
            img_big_data = fhdl.read()

        # create line with png, should be resized
        Book.write(*[
            [book],
            {
                'lines': [('create', [{
                    'date': date(2022, 5, 2),
                    'description': 'Text 2',
                    'category': category.id,
                    'bookingtype': 'in',
                    'amount': Decimal('1.0'),
                    'party': party.id,
                    'media': img_big_data,
                    'media_name': 'big.png',
                    }])],
                }
            ])
        self.assertEqual(len(book.lines), 2)
        self.assertEqual(book.lines[1].media_mime, 'image/jpeg')
        self.assertEqual(book.lines[1].media_size, 10221)
        self.assertEqual(book.lines[1].media_name, 'big.jpg')

        # check image size
        with BytesIO(book.lines[1].media) as fhdl:
            img2 = Image.open(fhdl, 'r')
            self.assertEqual(img2.size, (2000, 837))

# end LineTestCase
