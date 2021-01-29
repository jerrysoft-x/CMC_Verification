import os
import shutil

import pytest

from certificate_factory import BaoSteelCertificateFactory, BaoSteelCertificate
from common import CommonUtils, PdfFile, Direction


@pytest.fixture
def baosteel_certificate_pdf_sample_vl_a():
    test_file_vl_a = 'J0E0061697_BGSAJ2009120012700.pdf'
    abs_path = os.path.abspath(test_file_vl_a)
    if os.path.exists(test_file_vl_a):
        os.remove(test_file_vl_a)
    file_source = os.path.abspath(r"../test_data")
    shutil.copy(os.path.join(file_source, test_file_vl_a), test_file_vl_a)
    with CommonUtils.open_file(abs_path) as pdf_file:
        yield pdf_file


@pytest.fixture
def baosteel_certificate_pdf_sample_vl_d36():
    test_file_vl_d36 = 'J9H0001126_BGSAJ2001130008400.pdf'
    abs_path = os.path.abspath(test_file_vl_d36)
    if os.path.exists(test_file_vl_d36):
        os.remove(test_file_vl_d36)
    file_source = os.path.abspath(r"../test_data")
    shutil.copy(os.path.join(file_source, test_file_vl_d36), test_file_vl_d36)
    with CommonUtils.open_file(abs_path) as pdf_file:
        yield pdf_file


@pytest.fixture
def expected_certificate_no_vl_a():
    return ['P610041332']


@pytest.fixture
def expected_serial_numbers_no_vl_a():
    return [
        [(1, 7)]
    ]


@pytest.fixture
def expected_chemical_elements_vl_a():
    return ['C', 'Si', 'Mn', 'P', 'S', 'Ceq', 'Ti', 'Als']


@pytest.fixture
def expected_specification_vl_a():
    return 'VL A'


@pytest.fixture
def expected_thickness_vl_a():
    return 28.0


@pytest.fixture
def expected_delivery_condition_vl_a():
    return [
        [
            'AR'
        ]
    ]


@pytest.fixture
def expected_batch_no_vl_a():
    return [
        [
            '10410241'
        ]
    ]


@pytest.fixture
def expected_plate_no_vl_a():
    return [
        [
            '0909078200'
        ]
    ]


@pytest.fixture
def expected_quantity_vl_a():
    return [
        [
            1
        ]
    ]


@pytest.fixture
def expected_mass_vl_a():
    return [
        [
            3.517
        ]
    ]


@pytest.fixture
def expected_chemical_compositions_vl_a():
    return [
        [
            {'C': 0.14, 'Si': 0.17, 'Mn': 0.82, 'P': 0.018, 'S': 0.007, 'Ceq': 0.28, 'Ti': 0.01, 'Als': 0.023}
        ]
    ]


@pytest.fixture
def expected_yield_strength_vl_a():
    return [
        [
            317
        ]
    ]


@pytest.fixture
def expected_tensile_strength_vl_a():
    return [
        [
            442
        ]
    ]


@pytest.fixture
def expected_elongation_vl_a():
    return [
        [
            33
        ]
    ]


def test_reading_baosteel_certificate_vl_a(
    baosteel_certificate_pdf_sample_vl_a,
    expected_certificate_no_vl_a,
    expected_serial_numbers_no_vl_a,
    expected_chemical_elements_vl_a,
    expected_specification_vl_a,
    expected_thickness_vl_a,
    expected_delivery_condition_vl_a,
    expected_batch_no_vl_a,
    expected_plate_no_vl_a,
    expected_quantity_vl_a,
    expected_mass_vl_a,
    expected_chemical_compositions_vl_a,
    expected_yield_strength_vl_a,
    expected_tensile_strength_vl_a,
    expected_elongation_vl_a
):
    factory = BaoSteelCertificateFactory()
    certificates = factory.read(baosteel_certificate_pdf_sample_vl_a)
    for cert_index, certificate in enumerate(certificates):
        assert isinstance(certificate, BaoSteelCertificate)
        # the file_path attribute should be the abstract path of the certificate file.
        assert certificate.file_path == baosteel_certificate_pdf_sample_vl_a.file_path
        assert 'J0E0061697_BGSAJ2009120012700.pdf' in certificate.file_path
        # the steel_plant attribute should be the full name of bao steel.
        assert certificate.steel_plant == 'BAOSHAN IRON & STEEL CO., LTD.'
        # the certificate no. attribute should match the expected value.
        assert certificate.certificate_no == expected_certificate_no_vl_a[cert_index]
        # the serial numbers attribute should match the expected value.
        converted_serial_numbers = [(serial_number.value, serial_number.x_coordinate) for serial_number in
                                    certificate.serial_numbers]
        assert converted_serial_numbers == expected_serial_numbers_no_vl_a[cert_index]
        # check serial number attribute of each element in steel plates attribute
        converted_list_serial_number = [(plate.serial_number.value, plate.serial_number.x_coordinate) for plate in
                                        certificate.steel_plates]
        assert converted_list_serial_number == expected_serial_numbers_no_vl_a[cert_index]
        # the chemical elements attribute should be a dictionary contains all the expected chemical elements
        # print(certificate.chemical_elements.keys())
        assert len(certificate.chemical_elements) == len(expected_chemical_elements_vl_a)
        for element in expected_chemical_elements_vl_a:
            assert element in certificate.chemical_elements
            assert element == certificate.chemical_elements[element].value
        # the specification value is extracted from certificate level, and then cascade to each steel plate.
        assert certificate.specification.value == expected_specification_vl_a
        # the thickness value is extracted from certificate level, and then cascade to each steel plate.
        assert certificate.thickness.value == expected_thickness_vl_a
        for plate_index, plate in enumerate(certificate.steel_plates):
            # check delivery condition attribute of each element in steel plates attribute
            assert plate.delivery_condition.value == expected_delivery_condition_vl_a[cert_index][plate_index]
            # check if the batch no. attribute of each steel plate matches the expected value. (炉号)
            assert plate.batch_no.value == expected_batch_no_vl_a[cert_index][plate_index]
            # check if the plate no. attribute of each steel plate matches the expected value. (钢板号)
            assert plate.plate_no.value == expected_plate_no_vl_a[cert_index][plate_index]
            # check if the specification attribute of each steel plate matches the expected value. (标准)
            assert plate.specification.value == expected_specification_vl_a
            # check if the thickness attribute of each steel plate matches the expected value.（厚度）
            assert plate.thickness.value == expected_thickness_vl_a
            # check if the quantity attribute of each steel plate matches the expected value. (数量)
            assert plate.quantity.value == expected_quantity_vl_a[cert_index][plate_index]
            # check if the mass attribute of each steel plate matches the expected value. (重量)
            assert plate.mass.value == expected_mass_vl_a[cert_index][plate_index]
            # check if each element value of each steel plate matches the expected value.
            for element in certificate.chemical_elements:
                assert plate.chemical_compositions[element].calculated_value == \
                       expected_chemical_compositions_vl_a[cert_index][plate_index][element]
            # check if the yield strength value of each steel plate matches the expected value. (屈服)
            assert plate.yield_strength.value == expected_yield_strength_vl_a[cert_index][plate_index]
            # check if the tensile strength value of each steel plate matches the expected value. (抗拉)
            assert plate.tensile_strength.value == expected_tensile_strength_vl_a[cert_index][plate_index]
            # check if the elongation value of each steel plate matches the expected value. (伸长)
            assert plate.elongation.value == expected_elongation_vl_a[cert_index][plate_index]
            # check if the direction value of each steel plate matches the expected value.
            # assert plate.position_direction_impact.value == expected_direction
            assert plate.position_direction_impact is None  # no impact test in the VL A sample
            # check if the temperature value of each steel plate matches the expected value.
        #     assert plate.temperature.value == expected_temperature
            assert plate.temperature is None  # no impact test in the VL A sample
            # check if the impact energy values of eact steel plate match the expected values.
        #     current_imapct_energy_list = expected_impact_energy_list[cert_index][plate_index]
        #     assert len(plate.impact_energy_list) == len(current_imapct_energy_list)
        #     if len(current_imapct_energy_list) > 0:
        #         for impact_energy_index, impact_energy_value in enumerate(current_imapct_energy_list):
        #             assert plate.impact_energy_list[impact_energy_index].value == impact_energy_value
            assert len(plate.impact_energy_list) == 0  # no impact test in the VL A sample


@pytest.fixture
def expected_certificate_no_vl_d36():
    return ['P630001347']


@pytest.fixture
def expected_serial_numbers_no_vl_d36():
    return [
        [
            (1, 7),
            (2, 7),
            (3, 7),
            (4, 7)
        ]
    ]


@pytest.fixture
def expected_chemical_elements_vl_d36():
    return ['C', 'Si', 'Mn', 'P', 'S', 'Alt', 'Ceq', 'Cu', 'Ni', 'Cr', 'Nb', 'V', 'Ti', 'Mo', 'Als']


@pytest.fixture
def expected_specification_vl_d36():
    return 'VL D36'


@pytest.fixture
def expected_thickness_vl_d36():
    return 50.0


@pytest.fixture
def expected_delivery_condition_vl_d36():
    return [
        [
            'TM',
            'TM',
            'TM',
            'TM'
        ]
    ]


@pytest.fixture
def expected_batch_no_vl_d36():
    return [
        [
            '19403832',
            '19403832',
            '19403832',
            '19403832'
        ]
    ]


@pytest.fixture
def expected_plate_no_vl_d36():
    return [
        [
            '0103107100',
            '0103107200',
            '0103108100',
            '0103108200'
        ]
    ]


@pytest.fixture
def expected_quantity_vl_d36():
    return [
        [
            1,
            1,
            1,
            1
        ]
    ]


@pytest.fixture
def expected_mass_vl_d36():
    return [
        [
            8.855,
            8.855,
            8.855,
            8.855
        ]
    ]


@pytest.fixture
def expected_chemical_compositions_vl_d36():
    return [
        [
            {
                'C': 0.09,
                'Si': 0.30,
                'Mn': 1.46,
                'P': 0.012,
                'S': 0.002,
                'Alt': 0.035,
                'Ceq': 0.34,
                'Cu': 0.01,
                'Ni': 0.00,
                'Cr': 0.02,
                'Nb': 0.017,
                'V': 0.001,
                'Ti': 0.014,
                'Mo': 0.003,
                'Als': 0.03
            },
            {
                'C': 0.09,
                'Si': 0.30,
                'Mn': 1.46,
                'P': 0.012,
                'S': 0.002,
                'Alt': 0.035,
                'Ceq': 0.34,
                'Cu': 0.01,
                'Ni': 0.00,
                'Cr': 0.02,
                'Nb': 0.017,
                'V': 0.001,
                'Ti': 0.014,
                'Mo': 0.003,
                'Als': 0.03
            },
            {
                'C': 0.09,
                'Si': 0.30,
                'Mn': 1.46,
                'P': 0.012,
                'S': 0.002,
                'Alt': 0.035,
                'Ceq': 0.34,
                'Cu': 0.01,
                'Ni': 0.00,
                'Cr': 0.02,
                'Nb': 0.017,
                'V': 0.001,
                'Ti': 0.014,
                'Mo': 0.003,
                'Als': 0.03
            },
            {
                'C': 0.09,
                'Si': 0.30,
                'Mn': 1.46,
                'P': 0.012,
                'S': 0.002,
                'Alt': 0.035,
                'Ceq': 0.34,
                'Cu': 0.01,
                'Ni': 0.00,
                'Cr': 0.02,
                'Nb': 0.017,
                'V': 0.001,
                'Ti': 0.014,
                'Mo': 0.003,
                'Als': 0.03
            }
        ]
    ]


@pytest.fixture
def expected_yield_strength_vl_d36():
    return [
        [
            461,
            461,
            458,
            458
        ]
    ]


@pytest.fixture
def expected_tensile_strength_vl_d36():
    return [
        [
            574,
            574,
            553,
            553
        ]
    ]


@pytest.fixture
def expected_elongation_vl_d36():
    return [
        [
            27,
            27,
            29,
            29
        ]
    ]


@pytest.fixture
def expected_position_direction_impact_vl_36():
    return [
        [
            Direction.LONGITUDINAL,
            Direction.LONGITUDINAL,
            Direction.LONGITUDINAL,
            Direction.LONGITUDINAL
        ]
    ]


@pytest.fixture
def expected_temperature_vl_d36():
    return [
        [
            -20,
            -20,
            -20,
            -20
        ]
    ]


@pytest.fixture
def expected_impact_energy_list_vl_d36():
    return [
        [
            [360, 356, 350, 355],
            [360, 356, 350, 355],
            [344, 344, 342, 343],
            [344, 344, 342, 343]
        ]
    ]


def test_reading_baosteel_certificate_vl_d36(
    baosteel_certificate_pdf_sample_vl_d36,
    expected_certificate_no_vl_d36,
    expected_serial_numbers_no_vl_d36,
    expected_chemical_elements_vl_d36,
    expected_specification_vl_d36,
    expected_thickness_vl_d36,
    expected_delivery_condition_vl_d36,
    expected_batch_no_vl_d36,
    expected_plate_no_vl_d36,
    expected_quantity_vl_d36,
    expected_mass_vl_d36,
    expected_chemical_compositions_vl_d36,
    expected_yield_strength_vl_d36,
    expected_tensile_strength_vl_d36,
    expected_elongation_vl_d36,
    expected_position_direction_impact_vl_36,
    expected_temperature_vl_d36,
    expected_impact_energy_list_vl_d36
):
    factory = BaoSteelCertificateFactory()
    certificates = factory.read(baosteel_certificate_pdf_sample_vl_d36)
    for cert_index, certificate in enumerate(certificates):
        assert isinstance(certificate, BaoSteelCertificate)
        # the file_path attribute should be the abstract path of the certificate file.
        assert certificate.file_path == baosteel_certificate_pdf_sample_vl_d36.file_path
        assert 'J9H0001126_BGSAJ2001130008400.pdf' in certificate.file_path
        # the steel_plant attribute should be the full name of bao steel.
        assert certificate.steel_plant == 'BAOSHAN IRON & STEEL CO., LTD.'
        # the certificate no. attribute should match the expected value.
        assert certificate.certificate_no == expected_certificate_no_vl_d36[cert_index]
        # the serial numbers attribute should match the expected value.
        converted_serial_numbers = [(serial_number.value, serial_number.x_coordinate) for serial_number in
                                    certificate.serial_numbers]
        assert converted_serial_numbers == expected_serial_numbers_no_vl_d36[cert_index]
        # check serial number attribute of each element in steel plates attribute
        converted_list_serial_number = [(plate.serial_number.value, plate.serial_number.x_coordinate) for plate in
                                        certificate.steel_plates]
        assert converted_list_serial_number == expected_serial_numbers_no_vl_d36[cert_index]
        # the chemical elements attribute should be a dictionary contains all the expected chemical elements
        # print(certificate.chemical_elements.keys())
        assert len(certificate.chemical_elements) == len(expected_chemical_elements_vl_d36)
        for element in expected_chemical_elements_vl_d36:
            assert element in certificate.chemical_elements
            assert element == certificate.chemical_elements[element].value
        # the specification value is extracted from certificate level, and then cascade to each steel plate.
        assert certificate.specification.value == expected_specification_vl_d36
        # the thickness value is extracted from certificate level, and then cascade to each steel plate.
        assert certificate.thickness.value == expected_thickness_vl_d36
        for plate_index, plate in enumerate(certificate.steel_plates):
            # check delivery condition attribute of each element in steel plates attribute
            assert plate.delivery_condition.value == expected_delivery_condition_vl_d36[cert_index][plate_index]
            # check if the batch no. attribute of each steel plate matches the expected value. (炉号)
            assert plate.batch_no.value == expected_batch_no_vl_d36[cert_index][plate_index]
            # check if the plate no. attribute of each steel plate matches the expected value. (钢板号)
            assert plate.plate_no.value == expected_plate_no_vl_d36[cert_index][plate_index]
            # check if the specification attribute of each steel plate matches the expected value. (标准)
            assert plate.specification.value == expected_specification_vl_d36
            # check if the thickness attribute of each steel plate matches the expected value.（厚度）
            assert plate.thickness.value == expected_thickness_vl_d36
            # check if the quantity attribute of each steel plate matches the expected value. (数量)
            assert plate.quantity.value == expected_quantity_vl_d36[cert_index][plate_index]
            # check if the mass attribute of each steel plate matches the expected value. (重量)
            assert plate.mass.value == expected_mass_vl_d36[cert_index][plate_index]
            # check if each element value of each steel plate matches the expected value.
            for element in certificate.chemical_elements:
                assert plate.chemical_compositions[element].calculated_value == \
                       expected_chemical_compositions_vl_d36[cert_index][plate_index][element]
            # check if the yield strength value of each steel plate matches the expected value. (屈服)
            assert plate.yield_strength.value == expected_yield_strength_vl_d36[cert_index][plate_index]
            # check if the tensile strength value of each steel plate matches the expected value. (抗拉)
            assert plate.tensile_strength.value == expected_tensile_strength_vl_d36[cert_index][plate_index]
            # check if the elongation value of each steel plate matches the expected value. (伸长)
            assert plate.elongation.value == expected_elongation_vl_d36[cert_index][plate_index]
            # check if the direction value of each steel plate matches the expected value.
            assert plate.position_direction_impact.value == expected_position_direction_impact_vl_36[cert_index][
                plate_index]
            # check if the temperature value of each steel plate matches the expected value.
            assert plate.temperature.value == expected_temperature_vl_d36[cert_index][plate_index]
            # check if the impact energy values of eact steel plate match the expected values.
            current_imapct_energy_list = expected_impact_energy_list_vl_d36[cert_index][plate_index]
            assert len(plate.impact_energy_list) == len(current_imapct_energy_list)
            if len(current_imapct_energy_list) > 0:
                for impact_energy_index, impact_energy_value in enumerate(current_imapct_energy_list):
                    assert plate.impact_energy_list[impact_energy_index].value == impact_energy_value


if __name__ == '__main__':
    test_file_vl_a = 'J0E0061697_BGSAJ2009120012700.pdf'
    abs_path = os.path.abspath(test_file_vl_a)
    with CommonUtils.open_file(abs_path) as pdf_file:
        cert_file: PdfFile = pdf_file
        print(cert_file.tables[1])
