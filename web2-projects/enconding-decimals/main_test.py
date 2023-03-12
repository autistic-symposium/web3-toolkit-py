#!/usr/bin/env python

import unittest
import src.main as m


class EfunTest(unittest.TestCase):
    def setUp(self):
        self.e = m.Efun()
        self.test_data = [
            (-4096, 0x2000, (0x20, 0x00)),
            (-8192, 0x0000, (0x00, 0x00)),
            (0, 0x4000, (0x40, 0x00)),
            (2048, 0x5000, (0x50, 0x00)),
            (8191, 0x7F7F, (0x7F, 0x7F)),
            (6111, 0x6F5F, (0x6F, 0x5F)),
            (340, 0x4254, (0x42, 0x54)),
            (-2628, 0x2B3C, (0x2B, 0x3C)),
            (-255, 0x3E01, (0x3E, 0x01)),
            (-6902, 0x0A0A, (0x0A, 0x0A)),
            (-8151, 0x0029, (0x00, 0x29)),
            (-113, 0x3F0F, (0x3F, 0x0F)),
            (512, 0x4400, (0x44, 0x00)),
            (3967, 0x5E7F, (0x5E, 0x7F)),
        ]

    def test_extract(self):
        for item in self.test_data:
            self.assertEqual(self.e._extract_two_bytes(item[1]), item[2])

    def test_decode(self):
        for item in self.test_data:
            by1, by2 = self.e._extract_two_bytes(item[1])
            self.e._decode(by1, by2)
            self.assertEqual(self.e.dec_byte, item[0])

    def test_encode(self):
        for item in self.test_data:
            self.e._encode(item[0])
            self.assertEqual(self.e.enc_byte, hex(item[1]))

