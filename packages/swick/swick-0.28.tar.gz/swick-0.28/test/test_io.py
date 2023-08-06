import unittest
import swick


class TestReadSWC(unittest.TestCase):

    def test_too_few_fields(self):
        with self.assertRaises(swick.SWCFormatError):
            swick.read_swc('test/data/too_few_fields.swc')

    def test_too_many_fields(self):
        with self.assertRaises(swick.SWCFormatError):
            swick.read_swc('test/data/too_many_fields.swc')

    def test_read_write(self):
        swick.read_swc('test/data/valid_neuromorpho.swc')
        # TODO: ensure that reading and writing an SWC file results in the same
        #       file
        # TODO: preserve comments in SWC files to make this work


if __name__ == '__main__':
    unittest.main()
