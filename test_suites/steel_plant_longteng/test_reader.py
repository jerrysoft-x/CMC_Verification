import os
import shutil

import pytest

# This test file is used to test reader reading data from certificate file of LongTeng in docx format.
from certificate_factory import LongTengCertificateFactory
from common import DocxFile, Direction


@pytest.fixture
def longteng_certificate_docx_sample():
    test_file = 'DNVGL_LONGTENG.docx'
    abs_path = os.path.abspath(test_file)
    if os.path.exists(test_file):
        os.remove(test_file)
    if os.path.exists(f"{test_file}x"):
        os.remove(f"{test_file}x")
    file_source = os.path.abspath(r"../test_data")
    shutil.copy(os.path.join(file_source, test_file), test_file)
    with DocxFile(abs_path) as docx_file:
        yield docx_file


@pytest.fixture
def expected_certificate_no():
    return [
        'LT_DNV GL_2010001',
        'LT_DNV GL_2010002',
        'LT_DNV GL_2010003',
        'LT_DNV GL_2010004',
        'LT_DNV GL_2010005',
        'LT_DNV GL_2010006'
    ]


@pytest.fixture
def expected_serial_numbers():
    return [
        [(1, 6)],
        [(1, 6), (2, 7), (3, 8), (4, 9), (5, 10), (6, 11), (7, 12), (8, 13)],
        [(1, 6), (2, 7), (3, 8), (4, 9), (5, 10), (6, 11), (7, 12), (8, 13), (9, 14), (10, 15), (11, 16), (12, 17)],
        [(1, 6), (2, 7), (3, 8), (4, 9), (5, 10), (6, 11), (7, 12), (8, 13), (9, 14), (10, 15), (11, 16), (12, 17)],
        [(1, 6), (2, 7), (3, 8), (4, 9), (5, 10), (6, 11), (7, 12), (8, 13), (9, 14), (10, 15), (11, 16), (12, 17)],
        [(1, 6), (2, 7), (3, 8), (4, 9), (5, 10), (6, 11), (7, 12)],
    ]


@pytest.fixture
def expected_chemical_elements():
    return ['C', 'Si', 'Mn', 'P', 'S', 'Ni', 'Cr', 'Cu', 'V', 'Al', 'Nb', 'Ceq']


@pytest.fixture
def expected_batch_no():
    return [
        ['D1-1998973'],
        [
            'D2-2000649',
            'D2-2001889',
            'D1-2001877',
            'D1-2001877',
            'D1-2001875',
            'D1-2001875',
            'B1-2008490',
            'B1-2008490'
        ],
        [
            'D2-1903522',
            'D1-2001431',
            'D2-2001896',
            'D2-2001712',
            'D2-2001897',
            'D1-1998415',
            'D2-2001626',
            'D2-2001626',
            'D2-2001625',
            'D1-1998984',
            'D1-1998984',
            'D1-1998983'
        ],
        [
            'D1-1998983',
            'B1-2007395',
            'D1-1999127',
            'D1-1999117',
            'D1-1999115',
            'D1-1999024',
            'D1-1999024',
            'D1-1999025',
            'D1-1999025',
            'D1-1998718',
            'D1-1999165',
            'D1-1998847'
        ],
        [
            'B1-2007649',
            'D1-1999273',
            'D1-1999275',
            'D1-1998860',
            'D1-1998860',
            'D1-1998859',
            'D1-1998859',
            'D1-1998859',
            'D1-1998858',
            'D1-1998627',
            'D1-1998627',
            'D1-1998631'
        ],
        [
            'D1-1998632',
            'D1-1999332',
            'D1-1998631',
            'D1-1998633',
            'D1-1998638',
            'D1-1998638',
            'D1-2001109'
        ]
    ]


@pytest.fixture
def expected_plate_no():
    return [
        [
            '2008F2716'
        ],
        [
            '2006B0537',
            '2008B0095',
            '2008B0516',
            '2008B0516',
            '2008B0522',
            '2008B0522',
            '2009A0156',
            '2009A0157'
        ],
        [
            '2008B0155',
            '2009B0001',
            '2009B0017',
            '2009B0024',
            '2009B0026',
            '2007E0201',
            '2009A0015',
            '2009A0017',
            '2009A0020',
            '2009A0022',
            '2009A0024',
            '2009A0025'
        ],
        [
            '2009A0031',
            '2009A0113',
            '2009A0248',
            '2009A0247',
            '2009A0241',
            '2009A0062',
            '2009A0063',
            '2009A0064',
            '2009A0065',
            '2009A0274',
            '2009A0287',
            '2009A0332'
        ],
        [
            '2009A0413',
            '2009A0458',
            '2009A0464',
            '2009A0439',
            '2009A0440',
            '2009A0441',
            '2009A0442',
            '2009A0443',
            '2009A0446',
            '2007A0407',
            '2007A0408',
            '2007A0449'
        ],
        [
            '2007A0453',
            '2010A0016',
            '2007A0444',
            '2007A0458',
            '2007A0515',
            '2007A0516',
            '2008F0318'
        ]
    ]


@pytest.fixture
def expected_specification():
    return [
        ['VL A36'],
        [
            'VL A36',
            'VL A36',
            'VL A36',
            'VL A36',
            'VL A36',
            'VL A36',
            'VL A36',
            'VL A36',
        ],
        [
            'VL A36',
            'VL A',
            'VL A',
            'VL A36',
            'VL A',
            'VL A36',
            'VL A36',
            'VL A36',
            'VL A36',
            'VL A36',
            'VL A36',
            'VL A36'
        ],
        [
            'VL A36',
            'VL A36',
            'VL A36',
            'VL A',
            'VL A',
            'VL A',
            'VL A',
            'VL A',
            'VL A',
            'VL A',
            'VL A',
            'VL A36'
        ],
        [
            'VL A36',
            'VL A',
            'VL A',
            'VL A36',
            'VL A36',
            'VL A36',
            'VL A36',
            'VL A36',
            'VL A36',
            'VL A36',
            'VL A36',
            'VL A36'
        ],
        [
            'VL A36',
            'VL A',
            'VL A36',
            'VL A36',
            'VL A36',
            'VL A36',
            'VL A'
        ]
    ]


@pytest.fixture
def expected_thickness():
    return [
        [16],
        [9, 9, 9, 9, 9, 9, 11, 11],
        [8, 8, 8, 8, 8, 10, 10, 10, 10, 10, 10, 10],
        [10, 10, 10, 11, 12, 9, 9, 9, 9, 10, 10, 10],
        [10, 10, 10, 11, 11, 11, 11, 11, 11, 10, 10, 10],
        [10, 10, 11, 11, 11, 11, 12]
    ]


@pytest.fixture
def expected_quantity():
    return [
        [19],
        [2, 1, 4, 11, 2, 10, 10, 10],
        [2, 4, 19, 2, 15, 20, 10, 10, 10, 10, 56, 6],
        [20, 40, 10, 18, 4, 10, 30, 10, 40, 2, 19, 4],
        [4, 23, 2, 40, 40, 10, 50, 8, 2, 10, 10, 30],
        [10, 13, 10, 10, 18, 6, 4]
    ]


@pytest.fixture
def expected_mass():
    return [
        [6.207],
        [0.251, 0.143, 0.406, 1.577, 0.191, 1.195, 2.605, 2.605],
        [0.221, 0.442, 2.098, 0.221, 1.656, 4.834, 2.417, 2.417, 2.417, 2.417, 13.534, 1.45],
        [4.834, 9.668, 2.417, 4.689, 1.118, 2.228, 6.684, 2.228, 8.912, 0.546, 5.192, 1.093],
        [1.093, 6.285, 0.546, 11.76, 11.76, 2.94, 14.7, 2.352, 0.588, 3.06, 3.06, 9.18],
        [3.06, 3.978, 3.287, 3.287, 5.916, 1.972, 1.557]
    ]


@pytest.fixture
def expected_chemical_compositions():
    return [
        [
            {'C': 0.14, 'Si': 0.28, 'Mn': 1.28, 'P': 0.018, 'S': 0.021, 'Ni': 0.03, 'Cr': 0.04, 'Cu': 0.04, 'V': 0.001,
             'Al': 0.035, 'Nb': 0.018, 'Ceq': 0.37}
        ],
        [
            {'C': 0.14, 'Si': 0.28, 'Mn': 1.22, 'P': 0.017, 'S': 0.006, 'Ni': 0.02, 'Cr': 0.05, 'Cu': 0.03, 'V': 0.031,
             'Al': 0.034, 'Nb': 0.005, 'Ceq': 0.36},
            {'C': 0.14, 'Si': 0.33, 'Mn': 1.22, 'P': 0.022, 'S': 0.007, 'Ni': 0.02, 'Cr': 0.05, 'Cu': 0.05, 'V': 0.032,
             'Al': 0.024, 'Nb': 0.004, 'Ceq': 0.36},
            {'C': 0.14, 'Si': 0.3, 'Mn': 1.21, 'P': 0.011, 'S': 0.006, 'Ni': 0.02, 'Cr': 0.05, 'Cu': 0.06, 'V': 0.032,
             'Al': 0.031, 'Nb': 0.004, 'Ceq': 0.36},
            {'C': 0.14, 'Si': 0.3, 'Mn': 1.21, 'P': 0.011, 'S': 0.006, 'Ni': 0.02, 'Cr': 0.05, 'Cu': 0.06, 'V': 0.032,
             'Al': 0.031, 'Nb': 0.004, 'Ceq': 0.36},
            {'C': 0.14, 'Si': 0.31, 'Mn': 1.21, 'P': 0.016, 'S': 0.008, 'Ni': 0.02, 'Cr': 0.07, 'Cu': 0.07, 'V': 0.033,
             'Al': 0.028, 'Nb': 0.004, 'Ceq': 0.37},
            {'C': 0.14, 'Si': 0.31, 'Mn': 1.21, 'P': 0.016, 'S': 0.008, 'Ni': 0.02, 'Cr': 0.07, 'Cu': 0.07, 'V': 0.033,
             'Al': 0.028, 'Nb': 0.004, 'Ceq': 0.37},
            {'C': 0.16, 'Si': 0.25, 'Mn': 1.17, 'P': 0.013, 'S': 0.004, 'Ni': 0.01, 'Cr': 0.06, 'Cu': 0.02, 'V': 0.026,
             'Al': 0.026, 'Nb': 0.002, 'Ceq': 0.38},
            {'C': 0.16, 'Si': 0.25, 'Mn': 1.17, 'P': 0.013, 'S': 0.004, 'Ni': 0.01, 'Cr': 0.06, 'Cu': 0.02, 'V': 0.026,
             'Al': 0.026, 'Nb': 0.002, 'Ceq': 0.38}
        ],
        [
            {'C': 0.14, 'Si': 0.26, 'Mn': 1.19, 'P': 0.021, 'S': 0.007, 'Ni': 0.01, 'Cr': 0.05, 'Cu': 0.03, 'V': 0.027,
             'Al': 0.026, 'Nb': 0.004, 'Ceq': 0.36},
            {'C': 0.14, 'Si': 0.21, 'Mn': 0.65, 'P': 0.008, 'S': 0.01, 'Ni': 0.02, 'Cr': 0.02, 'Cu': 0.02, 'V': 0.02,
             'Al': 0.02, 'Nb': 0.02, 'Ceq': 0.26},
            {'C': 0.14, 'Si': 0.19, 'Mn': 0.63, 'P': 0.021, 'S': 0.006, 'Ni': 0.02, 'Cr': 0.02, 'Cu': 0.02, 'V': 0.02,
             'Al': 0.02, 'Nb': 0.02, 'Ceq': 0.26},
            {'C': 0.14, 'Si': 0.28, 'Mn': 1.21, 'P': 0.01, 'S': 0.008, 'Ni': 0.02, 'Cr': 0.07, 'Cu': 0.03, 'V': 0.034,
             'Al': 0.028, 'Nb': 0.003, 'Ceq': 0.37},
            {'C': 0.15, 'Si': 0.24, 'Mn': 0.65, 'P': 0.02, 'S': 0.01, 'Ni': 0.02, 'Cr': 0.02, 'Cu': 0.02, 'V': 0.02,
             'Al': 0.02, 'Nb': 0.02, 'Ceq': 0.28},
            {'C': 0.14, 'Si': 0.28, 'Mn': 1.23, 'P': 0.011, 'S': 0.005, 'Ni': 0.03, 'Cr': 0.05, 'Cu': 0.07, 'V': 0.001,
             'Al': 0.032, 'Nb': 0.017, 'Ceq': 0.36},
            {'C': 0.14, 'Si': 0.26, 'Mn': 1.22, 'P': 0.018, 'S': 0.015, 'Ni': 0.02, 'Cr': 0.06, 'Cu': 0.03, 'V': 0.027,
             'Al': 0.041, 'Nb': 0.004, 'Ceq': 0.36},
            {'C': 0.14, 'Si': 0.26, 'Mn': 1.22, 'P': 0.018, 'S': 0.015, 'Ni': 0.02, 'Cr': 0.06, 'Cu': 0.03, 'V': 0.027,
             'Al': 0.041, 'Nb': 0.004, 'Ceq': 0.36},
            {'C': 0.14, 'Si': 0.3, 'Mn': 1.19, 'P': 0.014, 'S': 0.006, 'Ni': 0.02, 'Cr': 0.05, 'Cu': 0.03, 'V': 0.026,
             'Al': 0.031, 'Nb': 0.004, 'Ceq': 0.36},
            {'C': 0.15, 'Si': 0.3, 'Mn': 1.27, 'P': 0.015, 'S': 0.002, 'Ni': 0.05, 'Cr': 0.05, 'Cu': 0.08, 'V': 0.001,
             'Al': 0.026, 'Nb': 0.018, 'Ceq': 0.38},
            {'C': 0.15, 'Si': 0.3, 'Mn': 1.27, 'P': 0.015, 'S': 0.002, 'Ni': 0.05, 'Cr': 0.05, 'Cu': 0.08, 'V': 0.001,
             'Al': 0.026, 'Nb': 0.018, 'Ceq': 0.38},
            {'C': 0.15, 'Si': 0.26, 'Mn': 1.24, 'P': 0.016, 'S': 0.006, 'Ni': 0.02, 'Cr': 0.03, 'Cu': 0.05, 'V': 0.001,
             'Al': 0.029, 'Nb': 0.017, 'Ceq': 0.37}
        ],
        [
            {'C': 0.15, 'Si': 0.26, 'Mn': 1.24, 'P': 0.016, 'S': 0.006, 'Ni': 0.02, 'Cr': 0.03, 'Cu': 0.05, 'V': 0.001,
             'Al': 0.029, 'Nb': 0.017, 'Ceq': 0.37},
            {'C': 0.16, 'Si': 0.23, 'Mn': 1.21, 'P': 0.016, 'S': 0.008, 'Ni': 0.01, 'Cr': 0.04, 'Cu': 0.02, 'V': 0.028,
             'Al': 0.023, 'Nb': 0.003, 'Ceq': 0.38},
            {'C': 0.14, 'Si': 0.26, 'Mn': 1.24, 'P': 0.017, 'S': 0.003, 'Ni': 0.06, 'Cr': 0.04, 'Cu': 0.05, 'V': 0.002,
             'Al': 0.029, 'Nb': 0.017, 'Ceq': 0.36},
            {'C': 0.16, 'Si': 0.2, 'Mn': 0.67, 'P': 0.026, 'S': 0.004, 'Ni': 0.02, 'Cr': 0.02, 'Cu': 0.02, 'V': 0.02,
             'Al': 0.02, 'Nb': 0.02, 'Ceq': 0.27},
            {'C': 0.16, 'Si': 0.22, 'Mn': 0.66, 'P': 0.012, 'S': 0.006, 'Ni': 0.02, 'Cr': 0.02, 'Cu': 0.02, 'V': 0.02,
             'Al': 0.02, 'Nb': 0.02, 'Ceq': 0.27},
            {'C': 0.15, 'Si': 0.18, 'Mn': 0.65, 'P': 0.022, 'S': 0.005, 'Ni': 0.02, 'Cr': 0.02, 'Cu': 0.02, 'V': 0.02,
             'Al': 0.02, 'Nb': 0.02, 'Ceq': 0.27},
            {'C': 0.15, 'Si': 0.18, 'Mn': 0.65, 'P': 0.022, 'S': 0.005, 'Ni': 0.02, 'Cr': 0.02, 'Cu': 0.02, 'V': 0.02,
             'Al': 0.02, 'Nb': 0.02, 'Ceq': 0.27},
            {'C': 0.16, 'Si': 0.18, 'Mn': 0.64, 'P': 0.019, 'S': 0.006, 'Ni': 0.02, 'Cr': 0.02, 'Cu': 0.02, 'V': 0.02,
             'Al': 0.02, 'Nb': 0.02, 'Ceq': 0.27},
            {'C': 0.16, 'Si': 0.18, 'Mn': 0.64, 'P': 0.019, 'S': 0.006, 'Ni': 0.02, 'Cr': 0.02, 'Cu': 0.02, 'V': 0.02,
             'Al': 0.02, 'Nb': 0.02, 'Ceq': 0.27},
            {'C': 0.15, 'Si': 0.18, 'Mn': 0.65, 'P': 0.022, 'S': 0.002, 'Ni': 0.02, 'Cr': 0.02, 'Cu': 0.02, 'V': 0.02,
             'Al': 0.02, 'Nb': 0.02, 'Ceq': 0.26},
            {'C': 0.14, 'Si': 0.19, 'Mn': 0.66, 'P': 0.013, 'S': 0.007, 'Ni': 0.02, 'Cr': 0.02, 'Cu': 0.02, 'V': 0.02,
             'Al': 0.02, 'Nb': 0.02, 'Ceq': 0.25},
            {'C': 0.16, 'Si': 0.28, 'Mn': 1.28, 'P': 0.016, 'S': 0.006, 'Ni': 0.01, 'Cr': 0.02, 'Cu': 0.01, 'V': 0.004,
             'Al': 0.033, 'Nb': 0.018, 'Ceq': 0.38}
        ],
        [
            {'C': 0.14, 'Si': 0.25, 'Mn': 1.2, 'P': 0.018, 'S': 0.003, 'Ni': 0.01, 'Cr': 0.05, 'Cu': 0.02, 'V': 0.026,
             'Al': 0.026, 'Nb': 0.002, 'Ceq': 0.35},
            {'C': 0.14, 'Si': 0.21, 'Mn': 0.65, 'P': 0.015, 'S': 0.013, 'Ni': 0.02, 'Cr': 0.02, 'Cu': 0.02, 'V': 0.02,
             'Al': 0.02, 'Nb': 0.02, 'Ceq': 0.25},
            {'C': 0.14, 'Si': 0.22, 'Mn': 0.65, 'P': 0.008, 'S': 0.013, 'Ni': 0.02, 'Cr': 0.02, 'Cu': 0.02, 'V': 0.02,
             'Al': 0.02, 'Nb': 0.02, 'Ceq': 0.25},
            {'C': 0.14, 'Si': 0.29, 'Mn': 1.23, 'P': 0.01, 'S': 0.002, 'Ni': 0.03, 'Cr': 0.04, 'Cu': 0.08, 'V': 0.001,
             'Al': 0.031, 'Nb': 0.017, 'Ceq': 0.36},
            {'C': 0.14, 'Si': 0.29, 'Mn': 1.23, 'P': 0.01, 'S': 0.002, 'Ni': 0.03, 'Cr': 0.04, 'Cu': 0.08, 'V': 0.001,
             'Al': 0.031, 'Nb': 0.017, 'Ceq': 0.36},
            {'C': 0.13, 'Si': 0.3, 'Mn': 1.2, 'P': 0.008, 'S': 0.001, 'Ni': 0.04, 'Cr': 0.04, 'Cu': 0.07, 'V': 0.001,
             'Al': 0.03, 'Nb': 0.017, 'Ceq': 0.35},
            {'C': 0.13, 'Si': 0.3, 'Mn': 1.2, 'P': 0.008, 'S': 0.001, 'Ni': 0.04, 'Cr': 0.04, 'Cu': 0.07, 'V': 0.001,
             'Al': 0.03, 'Nb': 0.017, 'Ceq': 0.35},
            {'C': 0.13, 'Si': 0.3, 'Mn': 1.2, 'P': 0.008, 'S': 0.001, 'Ni': 0.04, 'Cr': 0.04, 'Cu': 0.07, 'V': 0.001,
             'Al': 0.03, 'Nb': 0.017, 'Ceq': 0.35},
            {'C': 0.14, 'Si': 0.28, 'Mn': 1.28, 'P': 0.018, 'S': 0.021, 'Ni': 0.03, 'Cr': 0.04, 'Cu': 0.08, 'V': 0.001,
             'Al': 0.032, 'Nb': 0.019, 'Ceq': 0.37},
            {'C': 0.15, 'Si': 0.27, 'Mn': 1.22, 'P': 0.011, 'S': 0.002, 'Ni': 0.02, 'Cr': 0.04, 'Cu': 0.05, 'V': 0.001,
             'Al': 0.031, 'Nb': 0.015, 'Ceq': 0.37},
            {'C': 0.15, 'Si': 0.27, 'Mn': 1.22, 'P': 0.011, 'S': 0.002, 'Ni': 0.02, 'Cr': 0.04, 'Cu': 0.05, 'V': 0.001,
             'Al': 0.031, 'Nb': 0.015, 'Ceq': 0.37},
            {'C': 0.14, 'Si': 0.26, 'Mn': 1.23, 'P': 0.012, 'S': 0.009, 'Ni': 0.02, 'Cr': 0.04, 'Cu': 0.06, 'V': 0.002,
             'Al': 0.037, 'Nb': 0.017, 'Ceq': 0.36}
        ],
        [
            {'C': 0.15, 'Si': 0.28, 'Mn': 1.24, 'P': 0.013, 'S': 0.01, 'Ni': 0.02, 'Cr': 0.04, 'Cu': 0.04, 'V': 0.002,
             'Al': 0.03, 'Nb': 0.016, 'Ceq': 0.37},
            {'C': 0.16, 'Si': 0.21, 'Mn': 0.67, 'P': 0.022, 'S': 0.008, 'Ni': 0.02, 'Cr': 0.02, 'Cu': 0.02, 'V': 0.02,
             'Al': 0.02, 'Nb': 0.02, 'Ceq': 0.27},
            {'C': 0.14, 'Si': 0.26, 'Mn': 1.23, 'P': 0.012, 'S': 0.009, 'Ni': 0.02, 'Cr': 0.04, 'Cu': 0.06, 'V': 0.002,
             'Al': 0.037, 'Nb': 0.017, 'Ceq': 0.36},
            {'C': 0.14, 'Si': 0.27, 'Mn': 1.24, 'P': 0.017, 'S': 0.004, 'Ni': 0.04, 'Cr': 0.06, 'Cu': 0.07, 'V': 0.003,
             'Al': 0.025, 'Nb': 0.02, 'Ceq': 0.37},
            {'C': 0.13, 'Si': 0.28, 'Mn': 1.26, 'P': 0.012, 'S': 0.004, 'Ni': 0.03, 'Cr': 0.03, 'Cu': 0.04, 'V': 0.002,
             'Al': 0.039, 'Nb': 0.017, 'Ceq': 0.36},
            {'C': 0.13, 'Si': 0.28, 'Mn': 1.26, 'P': 0.012, 'S': 0.004, 'Ni': 0.03, 'Cr': 0.03, 'Cu': 0.04, 'V': 0.002,
             'Al': 0.039, 'Nb': 0.017, 'Ceq': 0.36},
            {'C': 0.15, 'Si': 0.2, 'Mn': 0.64, 'P': 0.016, 'S': 0.013, 'Ni': 0.02, 'Cr': 0.02, 'Cu': 0.02, 'V': 0.02,
             'Al': 0.02, 'Nb': 0.02, 'Ceq': 0.27}
        ]
    ]


@pytest.fixture
def expected_yield_strength():
    return [
        [395],
        [380, 410, 385, 385, 420, 420, 415, 395],
        [410, 320, 300, 400, 305, 395, 380, 390, 380, 385, 385, 385],
        [385, 390, 405, 320, 300, 305, 300, 310, 315, 315, 315, 415],
        [405, 305, 310, 425, 380, 390, 415, 390, 425, 400, 400, 405],
        [425, 325, 405, 420, 400, 395, 300]
    ]


@pytest.fixture
def expected_tensile_strength():
    return [
        [545],
        [520, 530, 550, 550, 545, 545, 525, 545],
        [550, 445, 430, 530, 450, 525, 525, 530, 520, 530, 525, 520],
        [540, 520, 530, 450, 430, 440, 440, 450, 450, 445, 455, 535],
        [525, 430, 440, 540, 520, 530, 545, 530, 540, 535, 525, 545],
        [555, 445, 520, 530, 530, 530, 440]
    ]


@pytest.fixture
def expected_elongation():
    return [
        [31],
        [35, 32, 32, 32, 32, 32, 33, 33],
        [30, 31, 34, 29, 31, 31, 32, 33, 32, 33, 30, 32],
        [34, 31, 32, 36, 35, 31, 31, 35, 34, 32, 31, 34],
        [33, 33, 32, 32, 34, 33, 33, 33, 35, 32, 33, 33],
        [30, 33, 35, 32, 33, 32, 33]
    ]


@pytest.fixture
def expected_direction():
    return Direction.LONGITUDINAL


@pytest.fixture
def expected_temperature():
    return 0


@pytest.fixture
def expected_impact_energy_list():
    return [
        [[148, 136, 160, 148]],
        [
            [104, 122, 108, 111],
            [100, 108, 108, 105],
            [124, 106, 122, 117],
            [124, 106, 122, 117],
            [114, 102, 126, 114],
            [114, 102, 126, 114],
            [152, 144, 162, 153],
            [156, 148, 144, 149]
        ],
        [
            [118, 126, 104, 116],
            [],
            [],
            [102, 128, 102, 111],
            [],
            [120, 122, 110, 117],
            [116, 124, 100, 113],
            [118, 106, 102, 109],
            [106, 124, 102, 111],
            [120, 104, 106, 110],
            [118, 102, 112, 111],
            [106, 126, 108, 113]
        ],
        [
            [114, 132, 106, 117],
            [106, 120, 112, 113],
            [116, 102, 116, 111],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [112, 118, 108, 113]
        ],
        [
            [120, 110, 116, 115],
            [],
            [],
            [142, 148, 124, 138],
            [148, 152, 158, 153],
            [140, 154, 152, 149],
            [162, 156, 158, 159],
            [160, 160, 156, 159],
            [158, 128, 152, 146],
            [122, 124, 124, 123],
            [126, 116, 108, 117],
            [108, 114, 122, 115]
        ],
        [
            [112, 118, 112, 114],
            [],
            [162, 144, 136, 147],
            [136, 146, 156, 146],
            [124, 162, 154, 147],
            [162, 160, 142, 155],
            []
        ]
    ]


@pytest.fixture
def expected_steel_making_type():
    return [
        ['EAF, CC'],
        [
            'EAF, CC',
            'EAF, CC',
            'EAF, CC',
            'EAF, CC',
            'EAF, CC',
            'EAF, CC',
            'BOC, CC',
            'BOC, CC'
        ],
        [
            'EAF, CC',
            'EAF, CC',
            'EAF, CC',
            'EAF, CC',
            'EAF, CC',
            'EAF, CC',
            'EAF, CC',
            'EAF, CC',
            'EAF, CC',
            'EAF, CC',
            'EAF, CC',
            'EAF, CC'
        ],
        [
            'EAF, CC',
            'BOC, CC',
            'EAF, CC',
            'EAF, CC',
            'EAF, CC',
            'EAF, CC',
            'EAF, CC',
            'EAF, CC',
            'EAF, CC',
            'EAF, CC',
            'EAF, CC',
            'EAF, CC'
        ],
        [
            'BOC, CC',
            'EAF, CC',
            'EAF, CC',
            'EAF, CC',
            'EAF, CC',
            'EAF, CC',
            'EAF, CC',
            'EAF, CC',
            'EAF, CC',
            'EAF, CC',
            'EAF, CC',
            'EAF, CC'
        ],
        [
            'EAF, CC',
            'EAF, CC',
            'EAF, CC',
            'EAF, CC',
            'EAF, CC',
            'EAF, CC',
            'EAF, CC'
        ]
    ]


# Test reading data from long teng docx file
def test_reading_longteng_certificate(
        longteng_certificate_docx_sample,
        expected_certificate_no,
        expected_serial_numbers,
        expected_chemical_elements,
        expected_batch_no,
        expected_plate_no,
        expected_specification,
        expected_thickness,
        expected_quantity,
        expected_mass,
        expected_chemical_compositions,
        expected_yield_strength,
        expected_tensile_strength,
        expected_elongation,
        expected_direction,
        expected_temperature,
        expected_impact_energy_list,
        expected_steel_making_type
):
    factory = LongTengCertificateFactory()
    certificates = factory.read(longteng_certificate_docx_sample)
    for cert_index, certificate in enumerate(certificates):
        # the file_path attribute should be the abstract path of the docx file.
        assert certificate.file_path == longteng_certificate_docx_sample.file_path
        # the steel_plant attribute should be the full name of long teng.
        assert certificate.steel_plant == 'CHANGSHU LONGTENG SPECIAL STEEL CO., LTD.'
        # the certificate no. attribute should match the expected value.
        assert certificate.certificate_no == expected_certificate_no[cert_index]
        # the delivery condition attribute should be hardcoded as AR, as all plates produced in LongTeng is As Rolled.
        assert certificate.delivery_condition.value == 'AR'
        # the serial numbers attribute should match the expected value.
        converted_serial_numbers = [(serial_number.value, serial_number.x_coordinate) for serial_number in
                                    certificate.serial_numbers]
        assert converted_serial_numbers == expected_serial_numbers[cert_index]
        # the chemical elements attribute should be a dictionary contains all the expected chemical elements
        # print(certificate.chemical_elements.keys())
        assert len(certificate.chemical_elements) == len(expected_chemical_elements)
        for element in expected_chemical_elements:
            assert element in certificate.chemical_elements
            assert element == certificate.chemical_elements[element].value
        # check serial number attribute of each element in steel plates attribute
        converted_list_serial_number = [(plate.serial_number.value, plate.serial_number.x_coordinate) for plate in
                                        certificate.steel_plates]
        assert converted_list_serial_number == expected_serial_numbers[cert_index]
        for plate_index, plate in enumerate(certificate.steel_plates):
            # check delivery condition attribute of each element in steel plates attribute
            # (hardcoded value AR, broadcast, Condition of Supply: As Rolled)
            assert plate.delivery_condition.value == 'AR'
            # check if the batch no. attribute of each steel plate matches the expected value. (冶炼炉号Batch No.)
            assert plate.batch_no.value == expected_batch_no[cert_index][plate_index]
            # check if the steel making type attribute of each steel plate matches the expected value.
            assert plate.steel_making_type.value == expected_steel_making_type[cert_index][plate_index]
            # check if the plate no. attribute of each steel plate matches the expected value. (轧制批号Roll No.)
            assert plate.plate_no.value == expected_plate_no[cert_index][plate_index]
            # check if the specification attribute of each steel plate matches the expected value. (钢级Grade)
            assert plate.specification.value == expected_specification[cert_index][plate_index]
            # check if the thickness attribute of each steel plate matches the expected value.
            # (The last dimension in 产品规格  Dimensions)
            assert plate.thickness.value == float(expected_thickness[cert_index][plate_index])
            # check if the quantity attribute of each steel plate matches the expected value. (支数PCS)
            assert plate.quantity.value == expected_quantity[cert_index][plate_index]
            # check if the mass attribute of each steel plate matches the expected value. (重量Weight(t))
            assert plate.mass.value == expected_mass[cert_index][plate_index]
            # check if each element value of each steel plate matches the expected value.
            for element in certificate.chemical_elements:
                assert plate.chemical_compositions[element].calculated_value == \
                       expected_chemical_compositions[cert_index][plate_index][element]
            # check if the yield strength value of each steel plate matches the expected value. (屈服强度ReH(MPa))
            assert plate.yield_strength.value == expected_yield_strength[cert_index][plate_index]
            # check if the tensile strength value of each steel plate matches the expected value. (抗拉强度Rm (Mpa))
            assert plate.tensile_strength.value == expected_tensile_strength[cert_index][plate_index]
            # check if the elongation value of each steel plate matches the expected value. (伸长率 A5 (%))
            assert plate.elongation.value == expected_elongation[cert_index][plate_index]
            # check if the direction value of each steel plate matches the expected value. (Longitudinal by default)
            assert plate.position_direction_impact.value == expected_direction
            # check if the temperature value of each steel plate matches the expected value.
            assert plate.temperature.value == expected_temperature
            # check if the impact energy values of eact steel plate match the expected values.
            current_imapct_energy_list = expected_impact_energy_list[cert_index][plate_index]
            assert len(plate.impact_energy_list) == len(current_imapct_energy_list)
            if len(current_imapct_energy_list) > 0:
                for impact_energy_index, impact_energy_value in enumerate(current_imapct_energy_list):
                    assert plate.impact_energy_list[impact_energy_index].value == impact_energy_value
