from PIL import Image
import unittest

from sirius.coding import image_encoding


class ImageCase(unittest.TestCase):

    def test_normal_text(self):
        data = image_encoding.html_to_png('')
        image = Image.open(data)
        self.assertEquals(image.size[0], 384)

    def test_normal_height(self):
        data = image_encoding.html_to_png(
            '<html><body style="margin: 0px; height: 100px;"></body></html>')
        image = Image.open(data)
        self.assertEquals(image.size[0], 384)
        self.assertEquals(image.size[1], 100)

    def test_probably_beyond_viewport_height(self):
        data = image_encoding.html_to_png(
            '<html><body style="margin: 0px; height: 10000px;"></body></html>')
        image = Image.open(data)
        self.assertEquals(image.size[0], 384)
        self.assertEquals(image.size[1], 10000)

    def test_rle(self):
        data = image_encoding.html_to_png('')
        image = Image.open(data)
        n_bytes, _ = image_encoding.rle_from_bw(image)
        self.assertEquals(n_bytes, 3072)


class PipeTestCase(unittest.TestCase):

    def test_full(self):
        data = image_encoding.html_to_png('')

        image = Image.open(data)
        image = image_encoding.crop_384(image)
        image = image_encoding.convert_to_1bit(image)

        n_bytes, _ = image_encoding.rle_from_bw(image)
        self.assertEquals(n_bytes, 3072)

    def test_default_pipeline(self):
        n_bytes, _ = image_encoding.rle_from_bw(
            image_encoding.default_pipeline('')
        )
        self.assertEquals(n_bytes, 3072)
