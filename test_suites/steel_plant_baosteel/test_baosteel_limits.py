import pytest

from certificate_verification import ChemicalCompositionLimit, LimitType, ThicknessLimit, SpecificationLimit, \
    DeliveryConditionLimit, YieldStrengthLimit, TensileStrengthLimit, ElongationLimit, TemperatureLimit, \
    ImpactEnergyLimit, BaoSteelAlLimit, FineGrainElementLimit, FineGrainElementLimitCombination
from common import SteelPlate, SerialNumber, ChemicalElementValue, Thickness, Specification, DeliveryCondition, \
    YieldStrength, TensileStrength, Elongation, Temperature, ImpactEnergy


@pytest.fixture
def plate():
    plate = SteelPlate(
        serial_number=SerialNumber(
            table_index=None,
            x_coordinate=None,
            y_coordinate=None,
            value=1
        )
    )
    plate.chemical_compositions = {
        'C': ChemicalElementValue(
            table_index=None,
            x_coordinate=None,
            y_coordinate=None,
            value=0,
            precision=0,
            element='C',
            index=None,
            valid_flag=True,
            message=None
        ),
        'Alt': ChemicalElementValue(
            table_index=None,
            x_coordinate=None,
            y_coordinate=None,
            value=0,
            precision=0,
            element='Alt',
            index=None,
            valid_flag=True,
            message=None
        ),
        'Als': ChemicalElementValue(
            table_index=None,
            x_coordinate=None,
            y_coordinate=None,
            value=0,
            precision=0,
            element='Als',
            index=None,
            valid_flag=True,
            message=None
        ),
        'Nb': ChemicalElementValue(
            table_index=None,
            x_coordinate=None,
            y_coordinate=None,
            value=0,
            precision=0,
            element='Nb',
            index=None,
            valid_flag=True,
            message=None
        ),
        'Ti': ChemicalElementValue(
            table_index=None,
            x_coordinate=None,
            y_coordinate=None,
            value=0,
            precision=0,
            element='Ti',
            index=None,
            valid_flag=True,
            message=None
        ),
        'V': ChemicalElementValue(
            table_index=None,
            x_coordinate=None,
            y_coordinate=None,
            value=0,
            precision=0,
            element='V',
            index=None,
            valid_flag=True,
            message=None
        )
    }
    plate.thickness = Thickness(
        table_index=None,
        x_coordinate=None,
        y_coordinate=None,
        value=0,
        index=None,
        valid_flag=True,
        message=None
    )
    plate.specification = Specification(
        table_index=None,
        x_coordinate=None,
        y_coordinate=None,
        value='',
        index=None,
        valid_flag=True,
        message=None
    )
    plate.delivery_condition = DeliveryCondition(
        table_index=None,
        x_coordinate=None,
        y_coordinate=None,
        value='',
        index=None,
        valid_flag=True,
        message=None
    )
    plate.yield_strength = YieldStrength(
        table_index=None,
        x_coordinate=None,
        y_coordinate=None,
        value=0,
        index=None,
        valid_flag=True,
        message=None
    )
    plate.tensile_strength = TensileStrength(
        table_index=None,
        x_coordinate=None,
        y_coordinate=None,
        value=0,
        index=None,
        valid_flag=True,
        message=None
    )
    plate.elongation = Elongation(
        table_index=None,
        x_coordinate=None,
        y_coordinate=None,
        value=0,
        index=None,
        valid_flag=True,
        message=None
    )
    plate.temperature = Temperature(
        table_index=None,
        x_coordinate=None,
        y_coordinate=None,
        value=0,
        index=None,
        valid_flag=True,
        message=None
    )
    plate.impact_energy_list = [
        ImpactEnergy(
            table_index=None,
            x_coordinate=None,
            y_coordinate=None,
            value=0,
            index=None,
            test_number='1',
            valid_flag=True,
            message=None
        ),
        ImpactEnergy(
            table_index=None,
            x_coordinate=None,
            y_coordinate=None,
            value=0,
            index=None,
            test_number='2',
            valid_flag=True,
            message=None
        ),
        ImpactEnergy(
            table_index=None,
            x_coordinate=None,
            y_coordinate=None,
            value=0,
            index=None,
            test_number='3',
            valid_flag=True,
            message=None
        ),
        ImpactEnergy(
            table_index=None,
            x_coordinate=None,
            y_coordinate=None,
            value=0,
            index=None,
            test_number='AVE.',
            valid_flag=True,
            message=None
        )
    ]
    return plate


def test_chemical_composition_limit(plate: SteelPlate):
    # if limit type is other than maximum, minimum and range, a value error should be thrown.
    with pytest.raises(ValueError) as e:
        ChemicalCompositionLimit(
            chemical_element='C',
            limit_type=LimitType.UNIQUE
        )
    assert str(e.value) == f"The limit type {LimitType.UNIQUE} is not expected in ChemicalCompositionLimit."
    # if the limit type is maximum, then if the maximum limit value is not specified properly, a value error should be
    # thrown.
    with pytest.raises(ValueError):
        ChemicalCompositionLimit(
            chemical_element='C',
            limit_type=LimitType.MAXIMUM
        )  # if maximum value is not specified, it is None by default, and should trigger an error.
    with pytest.raises(ValueError):
        ChemicalCompositionLimit(
            chemical_element='C',
            limit_type=LimitType.MAXIMUM,
            maximum=20
        )
    # if the limit type is minimum, then if the minimum limit value is not specified properly, a value error should be
    # thrown.
    with pytest.raises(ValueError):
        ChemicalCompositionLimit(
            chemical_element='C',
            limit_type=LimitType.MINIMUM
        )
    with pytest.raises(ValueError):
        ChemicalCompositionLimit(
            chemical_element='C',
            limit_type=LimitType.MINIMUM,
            minimum=10
        )
    # if the limit type is range, then if both maximum and minimum value are not specified properly, a value error
    # should be thrown.
    with pytest.raises(ValueError):
        ChemicalCompositionLimit(
            chemical_element='C',
            limit_type=LimitType.RANGE
        )
    with pytest.raises(ValueError):
        ChemicalCompositionLimit(
            chemical_element='C',
            limit_type=LimitType.RANGE,
            maximum=20.0
        )
    with pytest.raises(ValueError):
        ChemicalCompositionLimit(
            chemical_element='C',
            limit_type=LimitType.RANGE,
            minimum=10.0
        )
    with pytest.raises(ValueError):
        ChemicalCompositionLimit(
            chemical_element='C',
            limit_type=LimitType.RANGE,
            maximum=20,
            minimum=10
        )  # integer type doesn't match float type, and it will raise error too.
    # in case of the maximum type, check the boundary values.
    cl = ChemicalCompositionLimit(
        chemical_element='C',
        limit_type=LimitType.MAXIMUM,
        maximum=0.20
    )
    plate.chemical_compositions['C'].set_value_and_precision(value=19, precision=2)
    cl.verify(plate)
    assert plate.chemical_compositions['C'].valid_flag
    assert '[PASS]' in plate.chemical_compositions['C'].message
    plate.chemical_compositions['C'].set_value_and_precision(value=20, precision=2)
    cl.verify(plate)
    assert plate.chemical_compositions['C'].valid_flag
    assert '[PASS]' in plate.chemical_compositions['C'].message
    plate.chemical_compositions['C'].set_value_and_precision(value=21, precision=2)
    cl.verify(plate)
    assert not plate.chemical_compositions['C'].valid_flag
    assert '[FAIL]' in plate.chemical_compositions['C'].message
    # in case of the minimum type, check the boundary values.
    cl = ChemicalCompositionLimit(
        chemical_element='C',
        limit_type=LimitType.MINIMUM,
        minimum=0.10
    )
    plate.chemical_compositions['C'].set_value_and_precision(value=9, precision=2)
    cl.verify(plate)
    assert not plate.chemical_compositions['C'].valid_flag
    assert '[FAIL]' in plate.chemical_compositions['C'].message
    plate.chemical_compositions['C'].set_value_and_precision(value=10, precision=2)
    cl.verify(plate)
    assert plate.chemical_compositions['C'].valid_flag
    assert '[PASS]' in plate.chemical_compositions['C'].message
    plate.chemical_compositions['C'].set_value_and_precision(value=11, precision=2)
    cl.verify(plate)
    assert plate.chemical_compositions['C'].valid_flag
    assert '[PASS]' in plate.chemical_compositions['C'].message
    # in case of the range type, check the boundary values around maximum and minimum limits.
    cl = ChemicalCompositionLimit(
        chemical_element='C',
        limit_type=LimitType.RANGE,
        minimum=0.10,
        maximum=0.20
    )
    plate.chemical_compositions['C'].set_value_and_precision(value=9, precision=2)
    cl.verify(plate)
    assert not plate.chemical_compositions['C'].valid_flag
    assert '[FAIL]' in plate.chemical_compositions['C'].message
    plate.chemical_compositions['C'].set_value_and_precision(value=10, precision=2)
    cl.verify(plate)
    assert plate.chemical_compositions['C'].valid_flag
    assert '[PASS]' in plate.chemical_compositions['C'].message
    plate.chemical_compositions['C'].set_value_and_precision(value=11, precision=2)
    cl.verify(plate)
    assert plate.chemical_compositions['C'].valid_flag
    assert '[PASS]' in plate.chemical_compositions['C'].message
    plate.chemical_compositions['C'].set_value_and_precision(value=19, precision=2)
    cl.verify(plate)
    assert plate.chemical_compositions['C'].valid_flag
    assert '[PASS]' in plate.chemical_compositions['C'].message
    plate.chemical_compositions['C'].set_value_and_precision(value=20, precision=2)
    cl.verify(plate)
    assert plate.chemical_compositions['C'].valid_flag
    assert '[PASS]' in plate.chemical_compositions['C'].message
    plate.chemical_compositions['C'].set_value_and_precision(value=21, precision=2)
    cl.verify(plate)
    assert not plate.chemical_compositions['C'].valid_flag
    assert '[FAIL]' in plate.chemical_compositions['C'].message


def test_thickness_limit(plate: SteelPlate):
    tl = ThicknessLimit(
        maximum=20.0,
        minimum=10.0
    )
    plate.thickness.value = 9.9
    tl.verify(plate)
    assert not plate.thickness.valid_flag
    assert '[FAIL]' in plate.thickness.message
    plate.thickness.value = 10.0
    tl.verify(plate)
    assert not plate.thickness.valid_flag
    assert '[FAIL]' in plate.thickness.message
    plate.thickness.value = 10.1
    tl.verify(plate)
    assert plate.thickness.valid_flag
    assert '[PASS]' in plate.thickness.message
    plate.thickness.value = 19.9
    tl.verify(plate)
    assert plate.thickness.valid_flag
    assert '[PASS]' in plate.thickness.message
    plate.thickness.value = 20.0
    tl.verify(plate)
    assert plate.thickness.valid_flag
    assert '[PASS]' in plate.thickness.message
    plate.thickness.value = 20.1
    tl.verify(plate)
    assert not plate.thickness.valid_flag
    assert '[FAIL]' in plate.thickness.message


def test_specification_limit(plate: SteelPlate):
    sl = SpecificationLimit(
        scope=['VL D', 'VL E']
    )
    plate.specification.value = 'VL D'
    sl.verify(plate)
    assert plate.specification.valid_flag
    assert '[PASS]' in plate.specification.message
    plate.specification.value = 'VL E'
    sl.verify(plate)
    assert plate.specification.valid_flag
    assert '[PASS]' in plate.specification.message
    plate.specification.value = 'VL A'
    sl.verify(plate)
    assert not plate.specification.valid_flag
    assert '[FAIL]' in plate.specification.message


def test_delivery_condition_limit(plate: SteelPlate):
    dcl = DeliveryConditionLimit(
        scope=['TM', 'AR']
    )
    plate.delivery_condition.value = 'TM'
    dcl.verify(plate)
    assert plate.delivery_condition.valid_flag
    assert '[PASS]' in plate.delivery_condition.message
    plate.delivery_condition.value = 'AR'
    dcl.verify(plate)
    assert plate.delivery_condition.valid_flag
    assert '[PASS]' in plate.delivery_condition.message
    plate.delivery_condition.value = 'NR'
    dcl.verify(plate)
    assert not plate.delivery_condition.valid_flag
    assert '[FAIL]' in plate.delivery_condition.message


def test_yield_strength_limit(plate: SteelPlate):
    ysl = YieldStrengthLimit(
        minimum=200
    )
    plate.yield_strength.value = 199
    ysl.verify(plate)
    assert not plate.yield_strength.valid_flag
    assert '[FAIL]' in plate.yield_strength.message
    plate.yield_strength.value = 200
    ysl.verify(plate)
    assert plate.yield_strength.valid_flag
    assert '[PASS]' in plate.yield_strength.message
    plate.yield_strength.value = 201
    ysl.verify(plate)
    assert plate.yield_strength.valid_flag
    assert '[PASS]' in plate.yield_strength.message


def test_tensile_strength_limit(plate: SteelPlate):
    tsl = TensileStrengthLimit(
        maximum=200,
        minimum=100
    )
    plate.tensile_strength.value = 99
    tsl.verify(plate)
    assert not plate.tensile_strength.valid_flag
    assert '[FAIL]' in plate.tensile_strength.message
    plate.tensile_strength.value = 100
    tsl.verify(plate)
    assert plate.tensile_strength.valid_flag
    assert '[PASS]' in plate.tensile_strength.message
    plate.tensile_strength.value = 101
    tsl.verify(plate)
    assert plate.tensile_strength.valid_flag
    assert '[PASS]' in plate.tensile_strength.message
    plate.tensile_strength.value = 199
    tsl.verify(plate)
    assert plate.tensile_strength.valid_flag
    assert '[PASS]' in plate.tensile_strength.message
    plate.tensile_strength.value = 200
    tsl.verify(plate)
    assert plate.tensile_strength.valid_flag
    assert '[PASS]' in plate.tensile_strength.message
    plate.tensile_strength.value = 201
    tsl.verify(plate)
    assert not plate.tensile_strength.valid_flag
    assert '[FAIL]' in plate.tensile_strength.message


def test_elongation_limit(plate: SteelPlate):
    el = ElongationLimit(
        minimum=100
    )
    plate.elongation.value = 99
    el.verify(plate)
    assert not plate.elongation.valid_flag
    assert '[FAIL]' in plate.elongation.message
    plate.elongation.value = 100
    el.verify(plate)
    assert plate.elongation.valid_flag
    assert '[PASS]' in plate.elongation.message
    plate.elongation.value = 101
    el.verify(plate)
    assert plate.elongation.valid_flag
    assert '[PASS]' in plate.elongation.message


def test_temperature_limit(plate: SteelPlate):
    tl = TemperatureLimit(
        maximum=-20
    )
    plate.temperature.value = -21
    tl.verify(plate)
    assert plate.temperature.valid_flag
    assert '[PASS]' in plate.temperature.message
    plate.temperature.value = -20
    tl.verify(plate)
    assert plate.temperature.valid_flag
    assert '[PASS]' in plate.temperature.message
    plate.temperature.value = -19
    tl.verify(plate)
    assert not plate.temperature.valid_flag
    assert '[FAIL]' in plate.temperature.message


def test_impact_energy_limit(plate: SteelPlate):
    iel = ImpactEnergyLimit(
        minimum=100
    )
    plate.impact_energy_list[0].value = 99
    plate.impact_energy_list[1].value = 100
    plate.impact_energy_list[2].value = 101
    plate.impact_energy_list[3].value = 100
    iel.verify(plate)
    assert not plate.impact_energy_list[0].valid_flag
    assert '[FAIL]' in plate.impact_energy_list[0].message
    assert plate.impact_energy_list[1].valid_flag
    assert '[PASS]' in plate.impact_energy_list[1].message
    assert plate.impact_energy_list[2].valid_flag
    assert '[PASS]' in plate.impact_energy_list[2].message
    assert plate.impact_energy_list[3].valid_flag
    assert '[PASS]' in plate.impact_energy_list[3].message


def test_baosteel_al_limit(plate: SteelPlate):
    bal = BaoSteelAlLimit()
    # in case both alt and als pass the test
    plate.chemical_compositions['Alt'].set_value_and_precision(value=15, precision=3)
    plate.chemical_compositions['Als'].set_value_and_precision(value=10, precision=3)
    bal.verify(plate)
    assert plate.chemical_compositions['Alt'].valid_flag
    assert '[PASS]' in plate.chemical_compositions['Alt'].message
    assert '[FAIL]' not in plate.chemical_compositions['Alt'].message
    assert plate.chemical_compositions['Als'].valid_flag
    assert '[PASS]' in plate.chemical_compositions['Als'].message
    assert '[FAIL]' not in plate.chemical_compositions['Als'].message
    # in case alt pass but als not
    plate.chemical_compositions['Alt'].set_value_and_precision(value=15, precision=3)
    plate.chemical_compositions['Als'].set_value_and_precision(value=9, precision=3)
    bal.verify(plate)
    assert plate.chemical_compositions['Alt'].valid_flag
    assert '[PASS]' in plate.chemical_compositions['Alt'].message
    assert '[FAIL]' in plate.chemical_compositions['Alt'].message
    assert plate.chemical_compositions['Als'].valid_flag
    assert '[PASS]' in plate.chemical_compositions['Als'].message
    assert '[FAIL]' in plate.chemical_compositions['Als'].message
    # in case alt fail but als pass
    plate.chemical_compositions['Alt'].set_value_and_precision(value=14, precision=3)
    plate.chemical_compositions['Als'].set_value_and_precision(value=10, precision=3)
    bal.verify(plate)
    assert plate.chemical_compositions['Alt'].valid_flag
    assert '[PASS]' in plate.chemical_compositions['Alt'].message
    assert '[FAIL]' in plate.chemical_compositions['Alt'].message
    assert plate.chemical_compositions['Als'].valid_flag
    assert '[PASS]' in plate.chemical_compositions['Als'].message
    assert '[FAIL]' in plate.chemical_compositions['Als'].message
    # in case both alt and als fail
    plate.chemical_compositions['Alt'].set_value_and_precision(value=14, precision=3)
    plate.chemical_compositions['Als'].set_value_and_precision(value=9, precision=3)
    bal.verify(plate)
    assert not plate.chemical_compositions['Alt'].valid_flag
    assert '[FAIL]' in plate.chemical_compositions['Alt'].message
    assert '[PASS]' not in plate.chemical_compositions['Alt'].message
    assert not plate.chemical_compositions['Als'].valid_flag
    assert '[FAIL]' in plate.chemical_compositions['Als'].message
    assert '[PASS]' not in plate.chemical_compositions['Als'].message


def test_fine_grain_element_limit(plate: SteelPlate):
    # sample as Al+Nb+Ti+V
    fgel = FineGrainElementLimit(
        concurrent_limits=[
            BaoSteelAlLimit(),
            ChemicalCompositionLimit(
                chemical_element='Nb',
                limit_type=LimitType.RANGE,
                minimum=0.010,
                maximum=0.050
            ),
            ChemicalCompositionLimit(
                chemical_element='Ti',
                limit_type=LimitType.RANGE,
                minimum=0.007,
                maximum=0.020
            ),
            ChemicalCompositionLimit(
                chemical_element='V',
                limit_type=LimitType.RANGE,
                minimum=0.03,
                maximum=0.10
            ),
            ChemicalCompositionLimit(
                chemical_element='Nb + V + Ti',
                limit_type=LimitType.MAXIMUM,
                maximum=0.12
            )
        ]
    )
    element_scope = ['Alt', 'Als', 'Nb', 'Ti', 'V']
    # in case everything pass the check
    plate.chemical_compositions['Alt'].set_value_and_precision(value=15, precision=3)
    plate.chemical_compositions['Als'].set_value_and_precision(value=10, precision=3)
    plate.chemical_compositions['Nb'].set_value_and_precision(value=10, precision=3)
    plate.chemical_compositions['Ti'].set_value_and_precision(value=7, precision=3)
    plate.chemical_compositions['V'].set_value_and_precision(value=30, precision=3)
    assert fgel.verify(plate)
    for element in element_scope:
        assert plate.chemical_compositions[element].valid_flag
        assert '[PASS]' in plate.chemical_compositions[element].message
        assert '[FAIL]' not in plate.chemical_compositions[element].message
    # in case only alt fail
    for element in element_scope:
        plate.chemical_compositions[element].valid_flag = True
        plate.chemical_compositions[element].message = None
    plate.chemical_compositions['Alt'].set_value_and_precision(value=14, precision=3)
    assert fgel.verify(plate)
    for element in element_scope:
        assert plate.chemical_compositions[element].valid_flag
        assert '[PASS]' in plate.chemical_compositions[element].message
        if element in ['Alt', 'Als']:
            assert '[FAIL]' in plate.chemical_compositions[element].message
    # in case only als fail
    for element in element_scope:
        plate.chemical_compositions[element].valid_flag = True
        plate.chemical_compositions[element].message = None
    plate.chemical_compositions['Alt'].set_value_and_precision(value=15, precision=3)
    plate.chemical_compositions['Als'].set_value_and_precision(value=9, precision=3)
    assert fgel.verify(plate)
    for element in element_scope:
        assert plate.chemical_compositions[element].valid_flag
        assert '[PASS]' in plate.chemical_compositions[element].message
        if element in ['Alt', 'Als']:
            assert '[FAIL]' in plate.chemical_compositions[element].message
    # in case both alt and als fail
    # when and only when all pass the valid_flag and message will be set
    for element in element_scope:
        plate.chemical_compositions[element].valid_flag = True
        plate.chemical_compositions[element].message = None
    plate.chemical_compositions['Alt'].set_value_and_precision(value=14, precision=3)
    plate.chemical_compositions['Als'].set_value_and_precision(value=9, precision=3)
    assert not fgel.verify(plate)
    for element in element_scope:
        assert plate.chemical_compositions[element].valid_flag
        assert plate.chemical_compositions[element].message is None
    # in case only Nb fail
    for element in element_scope:
        plate.chemical_compositions[element].valid_flag = True
        plate.chemical_compositions[element].message = None
    plate.chemical_compositions['Alt'].set_value_and_precision(value=15, precision=3)
    plate.chemical_compositions['Als'].set_value_and_precision(value=10, precision=3)
    plate.chemical_compositions['Nb'].set_value_and_precision(value=9, precision=3)
    assert not fgel.verify(plate)
    for element in element_scope:
        assert plate.chemical_compositions[element].valid_flag
        assert plate.chemical_compositions[element].message is None
    # in case only Ti fail
    for element in element_scope:
        plate.chemical_compositions[element].valid_flag = True
        plate.chemical_compositions[element].message = None
    plate.chemical_compositions['Nb'].set_value_and_precision(value=10, precision=3)
    plate.chemical_compositions['Ti'].set_value_and_precision(value=6, precision=3)
    assert not fgel.verify(plate)
    for element in element_scope:
        assert plate.chemical_compositions[element].valid_flag
        assert plate.chemical_compositions[element].message is None
    # in case only V fail
    for element in element_scope:
        plate.chemical_compositions[element].valid_flag = True
        plate.chemical_compositions[element].message = None
    plate.chemical_compositions['Ti'].set_value_and_precision(value=7, precision=3)
    plate.chemical_compositions['V'].set_value_and_precision(value=20, precision=3)
    assert not fgel.verify(plate)
    for element in element_scope:
        assert plate.chemical_compositions[element].valid_flag
        assert plate.chemical_compositions[element].message is None
    # in case Nb + V + Ti fail
    for element in element_scope:
        plate.chemical_compositions[element].valid_flag = True
        plate.chemical_compositions[element].message = None
    plate.chemical_compositions['Nb'].set_value_and_precision(value=50, precision=3)
    plate.chemical_compositions['Ti'].set_value_and_precision(value=20, precision=3)
    plate.chemical_compositions['V'].set_value_and_precision(value=10, precision=2)
    assert not fgel.verify(plate)
    for element in element_scope:
        assert plate.chemical_compositions[element].valid_flag
        assert plate.chemical_compositions[element].message is None


def test_fine_grain_element_limit_combination(plate: SteelPlate):
    error_message: str = '[FAIL] Fine Grain Element failed test: '

    # simulate this situation: specification = VL E36, delivery condition = TM, thickness <= 50.
    # both Al+Ti and Al+Nb+Ti apply
    plate.specification.value = 'VL E36'
    plate.delivery_condition.value = 'TM'
    plate.thickness.value = 40

    # define fine grain element limit for Al+Ti
    al_plus_ti_limit = FineGrainElementLimit(
        concurrent_limits=[
            BaoSteelAlLimit(),
            ChemicalCompositionLimit(
                chemical_element='Ti',
                limit_type=LimitType.RANGE,
                minimum=0.007,
                maximum=0.020
            )
        ]
    )
    error_message += '[Al+Ti] Alt expect minimum 0.015 or Als expect minimum 0.010, Ti expect range [0.007, 0.02] '

    # define fine grain element limit for Al+Nb_Ti
    al_plus_nb_plus_ti_limit = FineGrainElementLimit(
        concurrent_limits=[
            BaoSteelAlLimit(),
            ChemicalCompositionLimit(
                chemical_element='Nb',
                limit_type=LimitType.RANGE,
                minimum=0.010,
                maximum=0.050
            ),
            ChemicalCompositionLimit(
                chemical_element='Ti',
                limit_type=LimitType.RANGE,
                minimum=0.007,
                maximum=0.020
            )
        ]
    )
    error_message += (
        '[Al+Nb+Ti] Alt expect minimum 0.015 or Als expect minimum 0.010, Nb expect range [0.01, 0.05], '
        'Ti expect range [0.007, 0.02] '
    )

    combination = FineGrainElementLimitCombination(
        fine_grain_element_limits=[al_plus_ti_limit, al_plus_nb_plus_ti_limit],
        error_message=error_message
    )

    # in fine grain element limit combination, as long as one of the limits pass, the combination pass.

    # Al+Ti pass, Al+Nb+Ti pass
    plate.chemical_compositions['Alt'].set_value_and_precision(value=15, precision=3)
    plate.chemical_compositions['Als'].set_value_and_precision(value=10, precision=3)
    plate.chemical_compositions['Ti'].set_value_and_precision(value=7, precision=3)
    plate.chemical_compositions['Nb'].set_value_and_precision(value=10, precision=3)
    assert combination.verify(plate)
    # in this case only Al+Ti is actually checked, and ignored Al+Nb+Ti
    assert plate.chemical_compositions['Alt'].valid_flag
    assert plate.chemical_compositions['Als'].valid_flag
    assert plate.chemical_compositions['Ti'].valid_flag
    assert plate.chemical_compositions['Nb'].valid_flag
    assert '[PASS]' in plate.chemical_compositions['Alt'].message
    assert '[PASS]' in plate.chemical_compositions['Als'].message
    assert '[PASS]' in plate.chemical_compositions['Ti'].message
    assert plate.chemical_compositions['Nb'].message is None

    # reset
    for element in ['Alt', 'Als', 'Ti', 'Nb']:
        plate.chemical_compositions[element].valid_flag = True
        plate.chemical_compositions[element].message = None

    # Al+Ti fail, Al+Nb+Ti pass NOT APPLICABLE because Al+Ti condition is actually a super set of Al+Nb+Ti
    # if Al+Ti fail, Al+Nb+Ti must fail too

    # Al+Ti pass, Al+Nb+Ti fail
    plate.chemical_compositions['Alt'].set_value_and_precision(value=15, precision=3)
    plate.chemical_compositions['Als'].set_value_and_precision(value=10, precision=3)
    plate.chemical_compositions['Ti'].set_value_and_precision(value=7, precision=3)
    plate.chemical_compositions['Nb'].set_value_and_precision(value=9, precision=3)
    assert combination.verify(plate)
    # in this case only Al+Ti is actually checked, and ignored Al+Nb+Ti
    assert plate.chemical_compositions['Alt'].valid_flag
    assert plate.chemical_compositions['Als'].valid_flag
    assert plate.chemical_compositions['Ti'].valid_flag
    assert plate.chemical_compositions['Nb'].valid_flag
    assert '[PASS]' in plate.chemical_compositions['Alt'].message
    assert '[PASS]' in plate.chemical_compositions['Als'].message
    assert '[PASS]' in plate.chemical_compositions['Ti'].message
    assert plate.chemical_compositions['Nb'].message is None

    # reset
    for element in ['Alt', 'Als', 'Ti', 'Nb']:
        plate.chemical_compositions[element].valid_flag = True
        plate.chemical_compositions[element].message = None

    # Al+Ti fail, Al+Nb+Ti fail
    plate.chemical_compositions['Alt'].set_value_and_precision(value=15, precision=3)
    plate.chemical_compositions['Als'].set_value_and_precision(value=10, precision=3)
    plate.chemical_compositions['Ti'].set_value_and_precision(value=6, precision=3)
    plate.chemical_compositions['Nb'].set_value_and_precision(value=10, precision=3)
    assert not combination.verify(plate)
    # in this case only Al+Ti is actually checked, and ignored Al+Nb+Ti
    assert not plate.chemical_compositions['Alt'].valid_flag
    assert not plate.chemical_compositions['Als'].valid_flag
    assert not plate.chemical_compositions['Ti'].valid_flag
    assert not plate.chemical_compositions['Nb'].valid_flag
    assert '[FAIL]' in plate.chemical_compositions['Alt'].message
    assert '[FAIL]' in plate.chemical_compositions['Als'].message
    assert '[FAIL]' in plate.chemical_compositions['Ti'].message
    assert '[FAIL]' in plate.chemical_compositions['Nb'].message
