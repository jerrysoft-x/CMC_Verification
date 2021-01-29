import pytest

from certificate_verification import LongTengRuleMaker, LimitType, ChemicalCompositionLimit, \
    FineGrainElementLimitCombination, FineGrainElementLimit
from common import SteelPlate, SerialNumber, Specification, DeliveryCondition, Thickness, ChemicalElementValue, \
    ImpactEnergy, PositionDirectionImpact, Direction, YieldStrength, TensileStrength, Elongation, Temperature, \
    SteelMakingType
from test_suites.common.conftest import BaseTester


@pytest.fixture(scope='module')
def rule_maker():
    return LongTengRuleMaker()


@pytest.fixture
def blank_steel_plate():
    plate = SteelPlate(
        serial_number=SerialNumber(
            table_index=None,
            x_coordinate=None,
            y_coordinate=None,
            value=1
        )
    )
    plate.specification = Specification(
        table_index=None,
        x_coordinate=None,
        y_coordinate=None,
        value='N/A',
        index=None,
        valid_flag=True,
        message=None
    )
    plate.delivery_condition = DeliveryCondition(
        table_index=None,
        x_coordinate=None,
        y_coordinate=None,
        value='N/A',
        index=None,
        valid_flag=True,
        message=None
    )
    plate.thickness = Thickness(
        table_index=None,
        x_coordinate=None,
        y_coordinate=None,
        value=10,
        index=None,
        valid_flag=True,
        message=None
    )
    plate.chemical_compositions['C'] = ChemicalElementValue(
        table_index=None,
        x_coordinate=None,
        y_coordinate=None,
        value=0,
        index=0,
        element='C',
        precision=0,
        valid_flag=True,
        message=None
    )
    plate.chemical_compositions['Si'] = ChemicalElementValue(
        table_index=None,
        x_coordinate=None,
        y_coordinate=None,
        value=0,
        index=0,
        element='Si',
        precision=0,
        valid_flag=True,
        message=None
    )
    plate.chemical_compositions['Mn'] = ChemicalElementValue(
        table_index=None,
        x_coordinate=None,
        y_coordinate=None,
        value=0,
        index=0,
        element='Mn',
        precision=0,
        valid_flag=True,
        message=None
    )
    plate.chemical_compositions['P'] = ChemicalElementValue(
        table_index=None,
        x_coordinate=None,
        y_coordinate=None,
        value=0,
        index=0,
        element='P',
        precision=0,
        valid_flag=True,
        message=None
    )
    plate.chemical_compositions['S'] = ChemicalElementValue(
        table_index=None,
        x_coordinate=None,
        y_coordinate=None,
        value=0,
        index=0,
        element='S',
        precision=0,
        valid_flag=True,
        message=None
    )
    plate.chemical_compositions['Cu'] = ChemicalElementValue(
        table_index=None,
        x_coordinate=None,
        y_coordinate=None,
        value=0,
        index=0,
        element='Cu',
        precision=0,
        valid_flag=True,
        message=None
    )
    plate.chemical_compositions['Cr'] = ChemicalElementValue(
        table_index=None,
        x_coordinate=None,
        y_coordinate=None,
        value=0,
        index=0,
        element='Cr',
        precision=0,
        valid_flag=True,
        message=None
    )
    plate.chemical_compositions['Ni'] = ChemicalElementValue(
        table_index=None,
        x_coordinate=None,
        y_coordinate=None,
        value=0,
        index=0,
        element='Ni',
        precision=0,
        valid_flag=True,
        message=None
    )
    plate.chemical_compositions['Mo'] = ChemicalElementValue(
        table_index=None,
        x_coordinate=None,
        y_coordinate=None,
        value=0,
        index=0,
        element='Mo',
        precision=0,
        valid_flag=True,
        message=None
    )
    plate.chemical_compositions['Al'] = ChemicalElementValue(
        table_index=None,
        x_coordinate=None,
        y_coordinate=None,
        value=0,
        index=0,
        element='Al',
        precision=0,
        valid_flag=True,
        message=None
    )
    plate.chemical_compositions['Nb'] = ChemicalElementValue(
        table_index=None,
        x_coordinate=None,
        y_coordinate=None,
        value=0,
        index=0,
        element='Nb',
        precision=0,
        valid_flag=True,
        message=None
    )
    plate.chemical_compositions['V'] = ChemicalElementValue(
        table_index=None,
        x_coordinate=None,
        y_coordinate=None,
        value=0,
        index=0,
        element='V',
        precision=0,
        valid_flag=True,
        message=None
    )
    plate.chemical_compositions['Ti'] = ChemicalElementValue(
        table_index=None,
        x_coordinate=None,
        y_coordinate=None,
        value=0,
        index=0,
        element='Ti',
        precision=0,
        valid_flag=True,
        message=None
    )
    plate.position_direction_impact = PositionDirectionImpact(
        table_index=None,
        x_coordinate=None,
        y_coordinate=None,
        value=Direction.LONGITUDINAL,
        index=None
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
    plate.steel_making_type = SteelMakingType(
        table_index=None,
        x_coordinate=None,
        y_coordinate=None,
        value='BOC, CC',
        index=None
    )
    return plate


# Normal Strength Steel
class TestVLA(BaseTester):

    def setup_class(self):
        self.specification = 'VL A'

    # Special Rules
    # Specification
    def test_specification(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='SpecificationLimit',
            limit_type=LimitType.SCOPE,
            scope=['VL A', 'VL B', 'VL D', 'VL A32', 'VL A36', 'VL D32', 'VL D36']
        )
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.specification.valid_flag
        assert '[PASS]' in blank_steel_plate.specification.message
        blank_steel_plate.specification.value = 'VL E'
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.specification.valid_flag
        assert '[FAIL]' in blank_steel_plate.specification.message

    # Delivery Condition
    def test_delivery_condition(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='DeliveryConditionLimit',
            limit_type=LimitType.SCOPE,
            scope=['AR']
        )
        blank_steel_plate.delivery_condition.value = 'AR'
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.delivery_condition.valid_flag
        assert '[PASS]' in blank_steel_plate.delivery_condition.message
        blank_steel_plate.delivery_condition.value = 'TM'
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.delivery_condition.valid_flag
        assert '[FAIL]' in blank_steel_plate.delivery_condition.message

    # Thickness
    def test_thickness(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        # steel making type is None
        blank_steel_plate.steel_making_type.value = None
        with pytest.raises(ValueError) as e:
            rule_maker.get_rules(blank_steel_plate)
        assert str(
            e.value) == f"The steel making type value {blank_steel_plate.steel_making_type.value} is not expected."
        # steel making type is BOC, CC
        blank_steel_plate.steel_making_type.value = 'BOC, CC'
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ThicknessLimit',
            limit_type=LimitType.RANGE,
            maximum=15,
            minimum=0
        )
        blank_steel_plate.thickness.value = 14
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.thickness.valid_flag
        assert '[PASS]' in blank_steel_plate.thickness.message
        blank_steel_plate.thickness.value = 15
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.thickness.valid_flag
        assert '[PASS]' in blank_steel_plate.thickness.message
        blank_steel_plate.thickness.value = 16
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.thickness.valid_flag
        assert '[FAIL]' in blank_steel_plate.thickness.message
        # steel making type is EAF, CC
        blank_steel_plate.steel_making_type.value = 'EAF, CC'
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ThicknessLimit',
            limit_type=LimitType.RANGE,
            maximum=20,
            minimum=0
        )
        blank_steel_plate.thickness.value = 19
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.thickness.valid_flag
        assert '[PASS]' in blank_steel_plate.thickness.message
        blank_steel_plate.thickness.value = 20
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.thickness.valid_flag
        assert '[PASS]' in blank_steel_plate.thickness.message
        blank_steel_plate.thickness.value = 21
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.thickness.valid_flag
        assert '[FAIL]' in blank_steel_plate.thickness.message

    # Chemical Composition
    # C
    def test_element_c(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ChemicalCompositionLimit',
            chemical_element='C',
            limit_type=LimitType.MAXIMUM,
            maximum=0.21,
            minimum=None
        )
        blank_steel_plate.chemical_compositions['C'].set_value(0.20)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['C'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['C'].message
        blank_steel_plate.chemical_compositions['C'].set_value(0.21)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['C'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['C'].message
        blank_steel_plate.chemical_compositions['C'].set_value(0.22)
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.chemical_compositions['C'].valid_flag
        assert '[FAIL]' in blank_steel_plate.chemical_compositions['C'].message

    # Si
    def test_element_si(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ChemicalCompositionLimit',
            chemical_element='Si',
            limit_type=LimitType.MAXIMUM,
            maximum=0.50,
            minimum=None
        )
        blank_steel_plate.chemical_compositions['Si'].set_value(0.49)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Si'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Si'].message
        blank_steel_plate.chemical_compositions['Si'].set_value(0.50)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Si'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Si'].message
        blank_steel_plate.chemical_compositions['Si'].set_value(0.51)
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.chemical_compositions['Si'].valid_flag
        assert '[FAIL]' in blank_steel_plate.chemical_compositions['Si'].message

    # Mn
    def test_element_mn(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ChemicalCompositionLimit',
            chemical_element='Mn',
            limit_type=LimitType.MINIMUM,
            maximum=None,
            minimum=0.525
        )
        blank_steel_plate.chemical_compositions['Mn'].set_value(0.524)
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.chemical_compositions['Mn'].valid_flag
        assert '[FAIL]' in blank_steel_plate.chemical_compositions['Mn'].message
        blank_steel_plate.chemical_compositions['Mn'].set_value(0.525)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Mn'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Mn'].message
        blank_steel_plate.chemical_compositions['Mn'].set_value(0.526)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Mn'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Mn'].message

    # P
    def test_element_p(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ChemicalCompositionLimit',
            chemical_element='P',
            limit_type=LimitType.MAXIMUM,
            maximum=0.035,
            minimum=None
        )
        blank_steel_plate.chemical_compositions['P'].set_value(0.034)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['P'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['P'].message
        blank_steel_plate.chemical_compositions['P'].set_value(0.035)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['P'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['P'].message
        blank_steel_plate.chemical_compositions['P'].set_value(0.036)
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.chemical_compositions['P'].valid_flag
        assert '[FAIL]' in blank_steel_plate.chemical_compositions['P'].message

    # S
    def test_element_s(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ChemicalCompositionLimit',
            chemical_element='S',
            limit_type=LimitType.MAXIMUM,
            maximum=0.035,
            minimum=None
        )
        blank_steel_plate.chemical_compositions['S'].set_value(0.034)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['S'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['S'].message
        blank_steel_plate.chemical_compositions['S'].set_value(0.035)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['S'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['S'].message
        blank_steel_plate.chemical_compositions['S'].set_value(0.036)
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.chemical_compositions['S'].valid_flag
        assert '[FAIL]' in blank_steel_plate.chemical_compositions['S'].message

    # Cu
    def test_element_cu(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ChemicalCompositionLimit',
            chemical_element='Cu',
            limit_type=LimitType.MAXIMUM,
            maximum=0.35,
            minimum=None
        )
        blank_steel_plate.chemical_compositions['Cu'].set_value(0.34)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Cu'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Cu'].message
        blank_steel_plate.chemical_compositions['Cu'].set_value(0.35)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Cu'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Cu'].message
        blank_steel_plate.chemical_compositions['Cu'].set_value(0.36)
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.chemical_compositions['Cu'].valid_flag
        assert '[FAIL]' in blank_steel_plate.chemical_compositions['Cu'].message

    # Cr
    def test_element_cr(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ChemicalCompositionLimit',
            chemical_element='Cr',
            limit_type=LimitType.MAXIMUM,
            maximum=0.20,
            minimum=None
        )
        blank_steel_plate.chemical_compositions['Cr'].set_value(0.19)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Cr'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Cr'].message
        blank_steel_plate.chemical_compositions['Cr'].set_value(0.20)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Cr'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Cr'].message
        blank_steel_plate.chemical_compositions['Cr'].set_value(0.21)
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.chemical_compositions['Cr'].valid_flag
        assert '[FAIL]' in blank_steel_plate.chemical_compositions['Cr'].message

    # Ni
    def test_element_ni(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ChemicalCompositionLimit',
            chemical_element='Ni',
            limit_type=LimitType.MAXIMUM,
            maximum=0.40,
            minimum=None
        )
        blank_steel_plate.chemical_compositions['Ni'].set_value(0.39)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Ni'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Ni'].message
        blank_steel_plate.chemical_compositions['Ni'].set_value(0.40)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Ni'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Ni'].message
        blank_steel_plate.chemical_compositions['Ni'].set_value(0.41)
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.chemical_compositions['Ni'].valid_flag
        assert '[FAIL]' in blank_steel_plate.chemical_compositions['Ni'].message

    # Mo
    def test_element_mo(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ChemicalCompositionLimit',
            chemical_element='Mo',
            limit_type=LimitType.MAXIMUM,
            maximum=0.08,
            minimum=None
        )
        blank_steel_plate.chemical_compositions['Mo'].set_value(0.07)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Mo'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Mo'].message
        blank_steel_plate.chemical_compositions['Mo'].set_value(0.08)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Mo'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Mo'].message
        blank_steel_plate.chemical_compositions['Mo'].set_value(0.09)
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.chemical_compositions['Mo'].valid_flag
        assert '[FAIL]' in blank_steel_plate.chemical_compositions['Mo'].message

    # C + 1/6 Mn
    def test_element_c_plus_one_sixth_mn(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ChemicalCompositionLimit',
            chemical_element='C + 1/6 Mn',
            limit_type=LimitType.MAXIMUM,
            maximum=0.40,
            minimum=None
        )
        blank_steel_plate.chemical_compositions['C'].set_value(0.20)
        blank_steel_plate.chemical_compositions['Mn'].set_value(1.19)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['C'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['C'].message
        assert blank_steel_plate.chemical_compositions['Mn'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Mn'].message
        blank_steel_plate.chemical_compositions['C'].set_value(0.20)
        blank_steel_plate.chemical_compositions['Mn'].set_value(1.20)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['C'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['C'].message
        assert blank_steel_plate.chemical_compositions['Mn'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Mn'].message
        blank_steel_plate.chemical_compositions['C'].set_value(0.20)
        blank_steel_plate.chemical_compositions['Mn'].set_value(1.21)
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.chemical_compositions['C'].valid_flag
        assert '[FAIL]' in blank_steel_plate.chemical_compositions['C'].message
        assert not blank_steel_plate.chemical_compositions['Mn'].valid_flag
        assert '[FAIL]' in blank_steel_plate.chemical_compositions['Mn'].message

    # Mechanical Properties
    # Yield Strength
    def test_yield_strength(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='YieldStrengthLimit',
            limit_type=LimitType.MINIMUM,
            minimum=235
        )
        blank_steel_plate.yield_strength.value = 234
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.yield_strength.valid_flag
        assert '[FAIL]' in blank_steel_plate.yield_strength.message
        blank_steel_plate.yield_strength.value = 235
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.yield_strength.valid_flag
        assert '[PASS]' in blank_steel_plate.yield_strength.message
        blank_steel_plate.yield_strength.value = 236
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.yield_strength.valid_flag
        assert '[PASS]' in blank_steel_plate.yield_strength.message

    # Tensile Strength
    def test_tensile_strength(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='TensileStrengthLimit',
            limit_type=LimitType.RANGE,
            maximum=520,
            minimum=400
        )
        blank_steel_plate.tensile_strength.value = 399
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.tensile_strength.valid_flag
        assert '[FAIL]' in blank_steel_plate.tensile_strength.message
        blank_steel_plate.tensile_strength.value = 400
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.tensile_strength.valid_flag
        assert '[PASS]' in blank_steel_plate.tensile_strength.message
        blank_steel_plate.tensile_strength.value = 401
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.tensile_strength.valid_flag
        assert '[PASS]' in blank_steel_plate.tensile_strength.message
        blank_steel_plate.tensile_strength.value = 519
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.tensile_strength.valid_flag
        assert '[PASS]' in blank_steel_plate.tensile_strength.message
        blank_steel_plate.tensile_strength.value = 520
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.tensile_strength.valid_flag
        assert '[PASS]' in blank_steel_plate.tensile_strength.message
        blank_steel_plate.tensile_strength.value = 521
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.tensile_strength.valid_flag
        assert '[FAIL]' in blank_steel_plate.tensile_strength.message

    # Elongation
    def test_elongation(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ElongationLimit',
            limit_type=LimitType.MINIMUM,
            minimum=22
        )
        blank_steel_plate.elongation.value = 21
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.elongation.valid_flag
        assert '[FAIL]' in blank_steel_plate.elongation.message
        blank_steel_plate.elongation.value = 22
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.elongation.valid_flag
        assert '[PASS]' in blank_steel_plate.elongation.message
        blank_steel_plate.elongation.value = 23
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.elongation.valid_flag
        assert '[PASS]' in blank_steel_plate.elongation.message

    # Temperature
    def test_temperature(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        # For VL A, in the LongTeng agreement document, the possible maximum thickness is 20
        blank_steel_plate.thickness.value = 20
        limit_list = rule_maker.get_rules(blank_steel_plate)
        # For VL A, maximum thickness 20, the impact test is not required. So TemperatureLimit should not be included.
        assert not any([limit.__class__.__name__ == 'TemperatureLimit' for limit in limit_list])

    # Impact Energy
    def test_impact_energy(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        # For VL A, in the LongTeng agreement document, the possible maximum thickness is 20
        blank_steel_plate.thickness.value = 20
        limit_list = rule_maker.get_rules(blank_steel_plate)
        # For VL A, maximum thickness 20, the impact test is not required.
        # So Impact Energy Limit should not be included.
        assert not any([limit.__class__.__name__ == 'ImpactEnergyLimit' for limit in limit_list])

    # Fine Grain Element
    def test_fine_grain_elements(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        # 5 kinds of situations for steel making types: BOC, CC; EAF, CC; value is None; invalid value; None
        # value is None
        blank_steel_plate.steel_making_type.value = None
        with pytest.raises(ValueError) as e:
            rule_maker.get_rules(blank_steel_plate)
        assert str(e.value) == (
            f"The steel making type value {blank_steel_plate.steel_making_type.value} is not expected."
        )
        # BOC, CC
        blank_steel_plate.steel_making_type.value = 'BOC, CC'
        limit_list = rule_maker.get_rules(blank_steel_plate)
        hit_limits = [limit for limit in limit_list if isinstance(limit, FineGrainElementLimitCombination)]
        assert len(hit_limits) == 1
        fine_grain_element_limit_combination = hit_limits[0]
        assert len(fine_grain_element_limit_combination.fine_grain_element_limits) == 1
        fine_grain_element_limit = fine_grain_element_limit_combination.fine_grain_element_limits[0]
        assert isinstance(fine_grain_element_limit, FineGrainElementLimit)
        assert len(fine_grain_element_limit.concurrent_limits) == 1
        chemical_composition_limit = fine_grain_element_limit.concurrent_limits[0]
        assert isinstance(chemical_composition_limit, ChemicalCompositionLimit)
        assert chemical_composition_limit.chemical_element == 'Al'
        assert chemical_composition_limit.limit_type == LimitType.MINIMUM
        assert chemical_composition_limit.minimum == 0.020
        # EAF, CC
        blank_steel_plate.steel_making_type.value = 'EAF, CC'
        limit_list = rule_maker.get_rules(blank_steel_plate)
        hit_limits = [limit for limit in limit_list if isinstance(limit, FineGrainElementLimitCombination)]
        assert len(hit_limits) == 0
        # invalid value
        blank_steel_plate.steel_making_type.value = 'N/A'
        with pytest.raises(ValueError) as excinfo:
            rule_maker.get_rules(blank_steel_plate)
        assert str(excinfo.value) == (
            f"The steel making type value {blank_steel_plate.steel_making_type.value} is not expected."
        )
        # None
        blank_steel_plate.steel_making_type = None
        with pytest.raises(ValueError) as e:
            rule_maker.get_rules(blank_steel_plate)
        assert str(e.value) == "The steel making type is not instantiated in the steel plate."


class TestVLB(BaseTester):

    def setup_class(self):
        self.specification = 'VL B'

    # Special Rules
    # Specification
    def test_specification(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='SpecificationLimit',
            limit_type=LimitType.SCOPE,
            scope=['VL A', 'VL B', 'VL D', 'VL A32', 'VL A36', 'VL D32', 'VL D36']
        )
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.specification.valid_flag
        assert '[PASS]' in blank_steel_plate.specification.message
        blank_steel_plate.specification.value = 'VL E'
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.specification.valid_flag
        assert '[FAIL]' in blank_steel_plate.specification.message

    # Delivery Condition
    def test_delivery_condition(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='DeliveryConditionLimit',
            limit_type=LimitType.SCOPE,
            scope=['AR']
        )
        blank_steel_plate.delivery_condition.value = 'AR'
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.delivery_condition.valid_flag
        assert '[PASS]' in blank_steel_plate.delivery_condition.message
        blank_steel_plate.delivery_condition.value = 'TM'
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.delivery_condition.valid_flag
        assert '[FAIL]' in blank_steel_plate.delivery_condition.message

    # Thickness
    def test_thickness(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        # steel making type is None
        blank_steel_plate.steel_making_type.value = None
        with pytest.raises(ValueError) as e:
            rule_maker.get_rules(blank_steel_plate)
        assert str(
            e.value) == f"The steel making type value {blank_steel_plate.steel_making_type.value} is not expected."
        # steel making type is BOC, CC
        blank_steel_plate.steel_making_type.value = 'BOC, CC'
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ThicknessLimit',
            limit_type=LimitType.RANGE,
            maximum=15,
            minimum=0
        )
        blank_steel_plate.thickness.value = 14
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.thickness.valid_flag
        assert '[PASS]' in blank_steel_plate.thickness.message
        blank_steel_plate.thickness.value = 15
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.thickness.valid_flag
        assert '[PASS]' in blank_steel_plate.thickness.message
        blank_steel_plate.thickness.value = 16
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.thickness.valid_flag
        assert '[FAIL]' in blank_steel_plate.thickness.message
        # steel making type is EAF, CC
        blank_steel_plate.steel_making_type.value = 'EAF, CC'
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ThicknessLimit',
            limit_type=LimitType.RANGE,
            maximum=20,
            minimum=0
        )
        blank_steel_plate.thickness.value = 19
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.thickness.valid_flag
        assert '[PASS]' in blank_steel_plate.thickness.message
        blank_steel_plate.thickness.value = 20
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.thickness.valid_flag
        assert '[PASS]' in blank_steel_plate.thickness.message
        blank_steel_plate.thickness.value = 21
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.thickness.valid_flag
        assert '[FAIL]' in blank_steel_plate.thickness.message

    # Chemical Composition
    # C
    def test_element_c(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ChemicalCompositionLimit',
            chemical_element='C',
            limit_type=LimitType.MAXIMUM,
            maximum=0.21,
            minimum=None
        )
        blank_steel_plate.chemical_compositions['C'].set_value(0.20)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['C'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['C'].message
        blank_steel_plate.chemical_compositions['C'].set_value(0.21)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['C'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['C'].message
        blank_steel_plate.chemical_compositions['C'].set_value(0.22)
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.chemical_compositions['C'].valid_flag
        assert '[FAIL]' in blank_steel_plate.chemical_compositions['C'].message

    # Si
    def test_element_si(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ChemicalCompositionLimit',
            chemical_element='Si',
            limit_type=LimitType.MAXIMUM,
            maximum=0.35,
            minimum=None
        )
        blank_steel_plate.chemical_compositions['Si'].set_value(0.34)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Si'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Si'].message
        blank_steel_plate.chemical_compositions['Si'].set_value(0.35)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Si'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Si'].message
        blank_steel_plate.chemical_compositions['Si'].set_value(0.36)
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.chemical_compositions['Si'].valid_flag
        assert '[FAIL]' in blank_steel_plate.chemical_compositions['Si'].message

    # Mn
    def test_element_mn_no_impact_test(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        blank_steel_plate.impact_energy_list = []
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ChemicalCompositionLimit',
            chemical_element='Mn',
            limit_type=LimitType.MINIMUM,
            maximum=None,
            minimum=0.80
        )
        blank_steel_plate.chemical_compositions['Mn'].set_value(0.79)
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.chemical_compositions['Mn'].valid_flag
        assert '[FAIL]' in blank_steel_plate.chemical_compositions['Mn'].message
        blank_steel_plate.chemical_compositions['Mn'].set_value(0.80)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Mn'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Mn'].message
        blank_steel_plate.chemical_compositions['Mn'].set_value(0.81)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Mn'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Mn'].message

    def test_element_mn_has_impact_test(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        blank_steel_plate.impact_energy_list = [
            ImpactEnergy(
                table_index=None,
                x_coordinate=None,
                y_coordinate=None,
                value=0,
                index=None,
                valid_flag=True,
                message=None,
                test_number='1'
            ),
            ImpactEnergy(
                table_index=None,
                x_coordinate=None,
                y_coordinate=None,
                value=0,
                index=None,
                valid_flag=True,
                message=None,
                test_number='2'
            ),
            ImpactEnergy(
                table_index=None,
                x_coordinate=None,
                y_coordinate=None,
                value=0,
                index=None,
                valid_flag=True,
                message=None,
                test_number='3'
            ),
            ImpactEnergy(
                table_index=None,
                x_coordinate=None,
                y_coordinate=None,
                value=0,
                index=None,
                valid_flag=True,
                message=None,
                test_number='4'
            )
        ]
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ChemicalCompositionLimit',
            chemical_element='Mn',
            limit_type=LimitType.MINIMUM,
            maximum=None,
            minimum=0.60
        )
        blank_steel_plate.chemical_compositions['Mn'].set_value(0.59)
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.chemical_compositions['Mn'].valid_flag
        assert '[FAIL]' in blank_steel_plate.chemical_compositions['Mn'].message
        blank_steel_plate.chemical_compositions['Mn'].set_value(0.60)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Mn'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Mn'].message
        blank_steel_plate.chemical_compositions['Mn'].set_value(0.61)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Mn'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Mn'].message

    # P
    def test_element_p(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ChemicalCompositionLimit',
            chemical_element='P',
            limit_type=LimitType.MAXIMUM,
            maximum=0.035,
            minimum=None
        )
        blank_steel_plate.chemical_compositions['P'].set_value(0.034)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['P'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['P'].message
        blank_steel_plate.chemical_compositions['P'].set_value(0.035)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['P'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['P'].message
        blank_steel_plate.chemical_compositions['P'].set_value(0.036)
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.chemical_compositions['P'].valid_flag
        assert '[FAIL]' in blank_steel_plate.chemical_compositions['P'].message

    # S
    def test_element_s(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ChemicalCompositionLimit',
            chemical_element='S',
            limit_type=LimitType.MAXIMUM,
            maximum=0.035,
            minimum=None
        )
        blank_steel_plate.chemical_compositions['S'].set_value(0.034)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['S'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['S'].message
        blank_steel_plate.chemical_compositions['S'].set_value(0.035)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['S'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['S'].message
        blank_steel_plate.chemical_compositions['S'].set_value(0.036)
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.chemical_compositions['S'].valid_flag
        assert '[FAIL]' in blank_steel_plate.chemical_compositions['S'].message

    # Cu
    def test_element_cu(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ChemicalCompositionLimit',
            chemical_element='Cu',
            limit_type=LimitType.MAXIMUM,
            maximum=0.35,
            minimum=None
        )
        blank_steel_plate.chemical_compositions['Cu'].set_value(0.34)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Cu'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Cu'].message
        blank_steel_plate.chemical_compositions['Cu'].set_value(0.35)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Cu'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Cu'].message
        blank_steel_plate.chemical_compositions['Cu'].set_value(0.36)
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.chemical_compositions['Cu'].valid_flag
        assert '[FAIL]' in blank_steel_plate.chemical_compositions['Cu'].message

    # Cr
    def test_element_cr(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ChemicalCompositionLimit',
            chemical_element='Cr',
            limit_type=LimitType.MAXIMUM,
            maximum=0.20,
            minimum=None
        )
        blank_steel_plate.chemical_compositions['Cr'].set_value(0.19)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Cr'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Cr'].message
        blank_steel_plate.chemical_compositions['Cr'].set_value(0.20)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Cr'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Cr'].message
        blank_steel_plate.chemical_compositions['Cr'].set_value(0.21)
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.chemical_compositions['Cr'].valid_flag
        assert '[FAIL]' in blank_steel_plate.chemical_compositions['Cr'].message

    # Ni
    def test_element_ni(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ChemicalCompositionLimit',
            chemical_element='Ni',
            limit_type=LimitType.MAXIMUM,
            maximum=0.40,
            minimum=None
        )
        blank_steel_plate.chemical_compositions['Ni'].set_value(0.39)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Ni'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Ni'].message
        blank_steel_plate.chemical_compositions['Ni'].set_value(0.40)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Ni'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Ni'].message
        blank_steel_plate.chemical_compositions['Ni'].set_value(0.41)
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.chemical_compositions['Ni'].valid_flag
        assert '[FAIL]' in blank_steel_plate.chemical_compositions['Ni'].message

    # Mo
    def test_element_mo(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ChemicalCompositionLimit',
            chemical_element='Mo',
            limit_type=LimitType.MAXIMUM,
            maximum=0.08,
            minimum=None
        )
        blank_steel_plate.chemical_compositions['Mo'].set_value(0.07)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Mo'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Mo'].message
        blank_steel_plate.chemical_compositions['Mo'].set_value(0.08)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Mo'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Mo'].message
        blank_steel_plate.chemical_compositions['Mo'].set_value(0.09)
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.chemical_compositions['Mo'].valid_flag
        assert '[FAIL]' in blank_steel_plate.chemical_compositions['Mo'].message

    # C + 1/6 Mn
    def test_element_c_plus_one_sixth_mn(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ChemicalCompositionLimit',
            chemical_element='C + 1/6 Mn',
            limit_type=LimitType.MAXIMUM,
            maximum=0.40,
            minimum=None
        )
        blank_steel_plate.chemical_compositions['C'].set_value(0.20)
        blank_steel_plate.chemical_compositions['Mn'].set_value(1.19)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['C'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['C'].message
        assert blank_steel_plate.chemical_compositions['Mn'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Mn'].message
        blank_steel_plate.chemical_compositions['C'].set_value(0.20)
        blank_steel_plate.chemical_compositions['Mn'].set_value(1.20)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['C'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['C'].message
        assert blank_steel_plate.chemical_compositions['Mn'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Mn'].message
        blank_steel_plate.chemical_compositions['C'].set_value(0.20)
        blank_steel_plate.chemical_compositions['Mn'].set_value(1.21)
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.chemical_compositions['C'].valid_flag
        assert '[FAIL]' in blank_steel_plate.chemical_compositions['C'].message
        assert not blank_steel_plate.chemical_compositions['Mn'].valid_flag
        assert '[FAIL]' in blank_steel_plate.chemical_compositions['Mn'].message

    # Temperature
    def test_temperature(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        # For VL B, in the LongTeng agreement document, the possible maximum thickness is 20
        blank_steel_plate.thickness.value = 20
        limit_list = rule_maker.get_rules(blank_steel_plate)
        # For VL B, maximum thickness 20, the impact test is not required. So TemperatureLimit should not be included.
        assert not any([limit.__class__.__name__ == 'TemperatureLimit' for limit in limit_list])

    # Impact Energy
    def test_impact_energy(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        # For VL B, in the LongTeng agreement document, the possible maximum thickness is 20
        blank_steel_plate.thickness.value = 20
        limit_list = rule_maker.get_rules(blank_steel_plate)
        # For VL B, maximum thickness 20, the impact test is not required. So ImpactEnergyLimit should not be included.
        assert not any([limit.__class__.__name__ == 'ImpactEnergyLimit' for limit in limit_list])

    # Fine Grain Element
    def test_fine_grain_elements(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        # 5 kinds of situations for steel making types: BOC, CC; EAF, CC; value is None; invalid value; None
        # value is None
        blank_steel_plate.steel_making_type.value = None
        with pytest.raises(ValueError) as e:
            rule_maker.get_rules(blank_steel_plate)
        assert str(
            e.value) == f"The steel making type value {blank_steel_plate.steel_making_type.value} is not expected."
        # BOC, CC
        blank_steel_plate.steel_making_type.value = 'BOC, CC'
        limit_list = rule_maker.get_rules(blank_steel_plate)
        hit_limits = [limit for limit in limit_list if isinstance(limit, FineGrainElementLimitCombination)]
        assert len(hit_limits) == 1
        fine_grain_element_limit_combination = hit_limits[0]
        assert len(fine_grain_element_limit_combination.fine_grain_element_limits) == 1
        fine_grain_element_limit = fine_grain_element_limit_combination.fine_grain_element_limits[0]
        assert isinstance(fine_grain_element_limit, FineGrainElementLimit)
        assert len(fine_grain_element_limit.concurrent_limits) == 1
        chemical_composition_limit = fine_grain_element_limit.concurrent_limits[0]
        assert chemical_composition_limit.chemical_element == 'Al'
        assert chemical_composition_limit.limit_type == LimitType.MINIMUM
        assert chemical_composition_limit.minimum == 0.020
        # EAF, CC
        blank_steel_plate.steel_making_type.value = 'EAF, CC'
        limit_list = rule_maker.get_rules(blank_steel_plate)
        hit_limits = [limit for limit in limit_list if isinstance(limit, FineGrainElementLimitCombination)]
        assert len(hit_limits) == 0
        # invalid value
        blank_steel_plate.steel_making_type.value = 'N/A'
        with pytest.raises(ValueError) as excinfo:
            rule_maker.get_rules(blank_steel_plate)
        assert str(excinfo.value) == (
            f"The steel making type value {blank_steel_plate.steel_making_type.value} is not expected."
        )
        # None
        blank_steel_plate.steel_making_type = None
        with pytest.raises(ValueError) as e:
            rule_maker.get_rules(blank_steel_plate)
        assert str(e.value) == "The steel making type is not instantiated in the steel plate."


class TestVLD(BaseTester):

    def setup_class(self):
        self.specification = 'VL D'

    # Special Rules
    # Specification
    def test_specification(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='SpecificationLimit',
            limit_type=LimitType.SCOPE,
            scope=['VL A', 'VL B', 'VL D', 'VL A32', 'VL A36', 'VL D32', 'VL D36']
        )
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.specification.valid_flag
        assert '[PASS]' in blank_steel_plate.specification.message
        blank_steel_plate.specification.value = 'VL E'
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.specification.valid_flag
        assert '[FAIL]' in blank_steel_plate.specification.message

    # Delivery Condition
    def test_delivery_condition(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='DeliveryConditionLimit',
            limit_type=LimitType.SCOPE,
            scope=['AR']
        )
        blank_steel_plate.delivery_condition.value = 'AR'
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.delivery_condition.valid_flag
        assert '[PASS]' in blank_steel_plate.delivery_condition.message
        blank_steel_plate.delivery_condition.value = 'TM'
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.delivery_condition.valid_flag
        assert '[FAIL]' in blank_steel_plate.delivery_condition.message

    # Thickness
    def test_thickness(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        # steel making type is None
        blank_steel_plate.steel_making_type.value = None
        with pytest.raises(ValueError) as e:
            rule_maker.get_rules(blank_steel_plate)
        assert str(
            e.value) == f"The steel making type value {blank_steel_plate.steel_making_type.value} is not expected."
        # steel making type is BOC, CC
        blank_steel_plate.steel_making_type.value = 'BOC, CC'
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ThicknessLimit',
            limit_type=LimitType.RANGE,
            maximum=19,
            minimum=0
        )
        blank_steel_plate.thickness.value = 18
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.thickness.valid_flag
        assert '[PASS]' in blank_steel_plate.thickness.message
        blank_steel_plate.thickness.value = 19
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.thickness.valid_flag
        assert '[PASS]' in blank_steel_plate.thickness.message
        blank_steel_plate.thickness.value = 20
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.thickness.valid_flag
        assert '[FAIL]' in blank_steel_plate.thickness.message
        # steel making type is EAF, CC
        blank_steel_plate.steel_making_type.value = 'EAF, CC'
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ThicknessLimit',
            limit_type=LimitType.RANGE,
            maximum=15,
            minimum=0
        )
        blank_steel_plate.thickness.value = 14
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.thickness.valid_flag
        assert '[PASS]' in blank_steel_plate.thickness.message
        blank_steel_plate.thickness.value = 15
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.thickness.valid_flag
        assert '[PASS]' in blank_steel_plate.thickness.message
        blank_steel_plate.thickness.value = 16
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.thickness.valid_flag
        assert '[FAIL]' in blank_steel_plate.thickness.message

    # Chemical Composition
    # C
    def test_element_c(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ChemicalCompositionLimit',
            chemical_element='C',
            limit_type=LimitType.MAXIMUM,
            maximum=0.21,
            minimum=None
        )
        blank_steel_plate.chemical_compositions['C'].set_value(0.20)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['C'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['C'].message
        blank_steel_plate.chemical_compositions['C'].set_value(0.21)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['C'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['C'].message
        blank_steel_plate.chemical_compositions['C'].set_value(0.22)
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.chemical_compositions['C'].valid_flag
        assert '[FAIL]' in blank_steel_plate.chemical_compositions['C'].message

    # Si
    def test_element_si(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ChemicalCompositionLimit',
            chemical_element='Si',
            limit_type=LimitType.RANGE,
            maximum=0.35,
            minimum=0.10
        )
        blank_steel_plate.chemical_compositions['Si'].set_value(0.09)
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.chemical_compositions['Si'].valid_flag
        assert '[FAIL]' in blank_steel_plate.chemical_compositions['Si'].message
        blank_steel_plate.chemical_compositions['Si'].set_value(0.10)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Si'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Si'].message
        blank_steel_plate.chemical_compositions['Si'].set_value(0.11)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Si'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Si'].message
        blank_steel_plate.chemical_compositions['Si'].set_value(0.34)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Si'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Si'].message
        blank_steel_plate.chemical_compositions['Si'].set_value(0.35)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Si'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Si'].message
        blank_steel_plate.chemical_compositions['Si'].set_value(0.36)
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.chemical_compositions['Si'].valid_flag
        assert '[FAIL]' in blank_steel_plate.chemical_compositions['Si'].message

    # Mn
    def test_element_mn(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ChemicalCompositionLimit',
            chemical_element='Mn',
            limit_type=LimitType.MINIMUM,
            maximum=None,
            minimum=0.60
        )
        blank_steel_plate.chemical_compositions['Mn'].set_value(0.59)
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.chemical_compositions['Mn'].valid_flag
        assert '[FAIL]' in blank_steel_plate.chemical_compositions['Mn'].message
        blank_steel_plate.chemical_compositions['Mn'].set_value(0.60)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Mn'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Mn'].message
        blank_steel_plate.chemical_compositions['Mn'].set_value(0.61)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Mn'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Mn'].message

    # P
    def test_element_p(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ChemicalCompositionLimit',
            chemical_element='P',
            limit_type=LimitType.MAXIMUM,
            maximum=0.035,
            minimum=None
        )
        blank_steel_plate.chemical_compositions['P'].set_value(0.034)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['P'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['P'].message
        blank_steel_plate.chemical_compositions['P'].set_value(0.035)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['P'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['P'].message
        blank_steel_plate.chemical_compositions['P'].set_value(0.036)
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.chemical_compositions['P'].valid_flag
        assert '[FAIL]' in blank_steel_plate.chemical_compositions['P'].message

    # S
    def test_element_s(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ChemicalCompositionLimit',
            chemical_element='S',
            limit_type=LimitType.MAXIMUM,
            maximum=0.035,
            minimum=None
        )
        blank_steel_plate.chemical_compositions['S'].set_value(0.034)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['S'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['S'].message
        blank_steel_plate.chemical_compositions['S'].set_value(0.035)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['S'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['S'].message
        blank_steel_plate.chemical_compositions['S'].set_value(0.036)
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.chemical_compositions['S'].valid_flag
        assert '[FAIL]' in blank_steel_plate.chemical_compositions['S'].message

    # Cu
    def test_element_cu(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ChemicalCompositionLimit',
            chemical_element='Cu',
            limit_type=LimitType.MAXIMUM,
            maximum=0.35,
            minimum=None
        )
        blank_steel_plate.chemical_compositions['Cu'].set_value(0.34)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Cu'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Cu'].message
        blank_steel_plate.chemical_compositions['Cu'].set_value(0.35)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Cu'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Cu'].message
        blank_steel_plate.chemical_compositions['Cu'].set_value(0.36)
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.chemical_compositions['Cu'].valid_flag
        assert '[FAIL]' in blank_steel_plate.chemical_compositions['Cu'].message

    # Cr
    def test_element_cr(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ChemicalCompositionLimit',
            chemical_element='Cr',
            limit_type=LimitType.MAXIMUM,
            maximum=0.20,
            minimum=None
        )
        blank_steel_plate.chemical_compositions['Cr'].set_value(0.19)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Cr'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Cr'].message
        blank_steel_plate.chemical_compositions['Cr'].set_value(0.20)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Cr'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Cr'].message
        blank_steel_plate.chemical_compositions['Cr'].set_value(0.21)
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.chemical_compositions['Cr'].valid_flag
        assert '[FAIL]' in blank_steel_plate.chemical_compositions['Cr'].message

    # Ni
    def test_element_ni(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ChemicalCompositionLimit',
            chemical_element='Ni',
            limit_type=LimitType.MAXIMUM,
            maximum=0.40,
            minimum=None
        )
        blank_steel_plate.chemical_compositions['Ni'].set_value(0.39)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Ni'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Ni'].message
        blank_steel_plate.chemical_compositions['Ni'].set_value(0.40)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Ni'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Ni'].message
        blank_steel_plate.chemical_compositions['Ni'].set_value(0.41)
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.chemical_compositions['Ni'].valid_flag
        assert '[FAIL]' in blank_steel_plate.chemical_compositions['Ni'].message

    # Mo
    def test_element_mo(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ChemicalCompositionLimit',
            chemical_element='Mo',
            limit_type=LimitType.MAXIMUM,
            maximum=0.08,
            minimum=None
        )
        blank_steel_plate.chemical_compositions['Mo'].set_value(0.07)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Mo'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Mo'].message
        blank_steel_plate.chemical_compositions['Mo'].set_value(0.08)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Mo'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Mo'].message
        blank_steel_plate.chemical_compositions['Mo'].set_value(0.09)
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.chemical_compositions['Mo'].valid_flag
        assert '[FAIL]' in blank_steel_plate.chemical_compositions['Mo'].message

    # C + 1/6 Mn
    def test_element_c_plus_one_sixth_mn(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ChemicalCompositionLimit',
            chemical_element='C + 1/6 Mn',
            limit_type=LimitType.MAXIMUM,
            maximum=0.40,
            minimum=None
        )
        blank_steel_plate.chemical_compositions['C'].set_value(0.20)
        blank_steel_plate.chemical_compositions['Mn'].set_value(1.19)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['C'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['C'].message
        assert blank_steel_plate.chemical_compositions['Mn'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Mn'].message
        blank_steel_plate.chemical_compositions['C'].set_value(0.20)
        blank_steel_plate.chemical_compositions['Mn'].set_value(1.20)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['C'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['C'].message
        assert blank_steel_plate.chemical_compositions['Mn'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Mn'].message
        blank_steel_plate.chemical_compositions['C'].set_value(0.20)
        blank_steel_plate.chemical_compositions['Mn'].set_value(1.21)
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.chemical_compositions['C'].valid_flag
        assert '[FAIL]' in blank_steel_plate.chemical_compositions['C'].message
        assert not blank_steel_plate.chemical_compositions['Mn'].valid_flag
        assert '[FAIL]' in blank_steel_plate.chemical_compositions['Mn'].message

    # Temperature
    def test_temperature(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        # For VL D, in the LongTeng agreement document, the possible maximum thickness is 19
        blank_steel_plate.thickness.value = 19
        limit_list = rule_maker.get_rules(blank_steel_plate)
        # For VL D, maximum thickness 19, the maximum test temperature should be -20
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='TemperatureLimit',
            limit_type=LimitType.MAXIMUM,
            maximum=-20
        )
        blank_steel_plate.temperature.value = -21
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.temperature.valid_flag
        assert '[PASS]' in blank_steel_plate.temperature.message
        blank_steel_plate.temperature.value = -20
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.temperature.valid_flag
        assert '[PASS]' in blank_steel_plate.temperature.message
        blank_steel_plate.temperature.value = -19
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.temperature.valid_flag
        assert '[FAIL]' in blank_steel_plate.temperature.message

    # Impact Energy
    def test_impact_energy(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        # For VL D, in the LongTeng agreement document, the possible maximum thickness is 19
        blank_steel_plate.thickness.value = 19
        limit_list = rule_maker.get_rules(blank_steel_plate)
        # For VL D, maximum thickness 19, direction LONGITUDINAL, minimum impact energy should be 27
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ImpactEnergyLimit',
            limit_type=LimitType.MINIMUM,
            minimum=27
        )
        blank_steel_plate.impact_energy_list = [
            ImpactEnergy(
                table_index=None,
                x_coordinate=None,
                y_coordinate=None,
                value=26,
                index=None,
                valid_flag=True,
                message=None,
                test_number='1'
            ),
            ImpactEnergy(
                table_index=None,
                x_coordinate=None,
                y_coordinate=None,
                value=27,
                index=None,
                valid_flag=True,
                message=None,
                test_number='2'
            ),
            ImpactEnergy(
                table_index=None,
                x_coordinate=None,
                y_coordinate=None,
                value=28,
                index=None,
                valid_flag=True,
                message=None,
                test_number='3'
            ),
            ImpactEnergy(
                table_index=None,
                x_coordinate=None,
                y_coordinate=None,
                value=29,
                index=None,
                valid_flag=True,
                message=None,
                test_number='Avg'
            )
        ]
        assert not limit.verify(blank_steel_plate)  # one of the energies must violates the limit
        assert blank_steel_plate.impact_energy_list[0].test_number == '1'
        assert not blank_steel_plate.impact_energy_list[0].valid_flag
        assert '[FAIL]' in blank_steel_plate.impact_energy_list[0].message
        assert blank_steel_plate.impact_energy_list[1].test_number == '2'
        assert blank_steel_plate.impact_energy_list[1].valid_flag
        assert '[PASS]' in blank_steel_plate.impact_energy_list[1].message
        assert blank_steel_plate.impact_energy_list[2].test_number == '3'
        assert blank_steel_plate.impact_energy_list[2].valid_flag
        assert '[PASS]' in blank_steel_plate.impact_energy_list[2].message
        assert blank_steel_plate.impact_energy_list[3].test_number == 'Avg'
        assert blank_steel_plate.impact_energy_list[3].valid_flag
        assert '[PASS]' in blank_steel_plate.impact_energy_list[3].message

    # Fine Grain Element
    def test_fine_grain_elements(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        # 5 kinds of situations for steel making types: BOC, CC; EAF, CC; value is None; invalid value; None
        # value is None
        blank_steel_plate.steel_making_type.value = None
        with pytest.raises(ValueError) as e:
            rule_maker.get_rules(blank_steel_plate)
        assert str(
            e.value) == f"The steel making type value {blank_steel_plate.steel_making_type.value} is not expected."
        # BOC, CC
        blank_steel_plate.steel_making_type.value = 'BOC, CC'
        limit_list = rule_maker.get_rules(blank_steel_plate)
        hit_limits = [limit for limit in limit_list if isinstance(limit, FineGrainElementLimitCombination)]
        assert len(hit_limits) == 1
        fine_grain_element_limit_combination = hit_limits[0]
        assert len(fine_grain_element_limit_combination.fine_grain_element_limits) == 1
        fine_grain_element_limit = fine_grain_element_limit_combination.fine_grain_element_limits[0]
        assert isinstance(fine_grain_element_limit, FineGrainElementLimit)
        assert len(fine_grain_element_limit.concurrent_limits) == 1
        chemical_composition_limit = fine_grain_element_limit.concurrent_limits[0]
        assert chemical_composition_limit.chemical_element == 'Al'
        assert chemical_composition_limit.limit_type == LimitType.MINIMUM
        assert chemical_composition_limit.minimum == 0.020
        # EAF, CC
        blank_steel_plate.steel_making_type.value = 'EAF, CC'
        limit_list = rule_maker.get_rules(blank_steel_plate)
        hit_limits = [limit for limit in limit_list if isinstance(limit, FineGrainElementLimitCombination)]
        assert len(hit_limits) == 1
        fine_grain_element_limit_combination = hit_limits[0]
        assert len(fine_grain_element_limit_combination.fine_grain_element_limits) == 1
        fine_grain_element_limit = fine_grain_element_limit_combination.fine_grain_element_limits[0]
        assert isinstance(fine_grain_element_limit, FineGrainElementLimit)
        assert len(fine_grain_element_limit.concurrent_limits) == 1
        chemical_composition_limit = fine_grain_element_limit.concurrent_limits[0]
        assert chemical_composition_limit.chemical_element == 'Al'
        assert chemical_composition_limit.limit_type == LimitType.MINIMUM
        assert chemical_composition_limit.minimum == 0.020
        # invalid value
        blank_steel_plate.steel_making_type.value = 'N/A'
        with pytest.raises(ValueError) as excinfo:
            rule_maker.get_rules(blank_steel_plate)
        assert str(excinfo.value) == (
            f"The steel making type value {blank_steel_plate.steel_making_type.value} is not expected."
        )
        # None
        blank_steel_plate.steel_making_type = None
        with pytest.raises(ValueError) as e:
            rule_maker.get_rules(blank_steel_plate)
        assert str(e.value) == "The steel making type is not instantiated in the steel plate."


class TestVLA32(BaseTester):

    def setup_class(self):
        self.specification = 'VL A32'

    # Special Rules
    # Specification
    def test_specification(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='SpecificationLimit',
            limit_type=LimitType.SCOPE,
            scope=['VL A', 'VL B', 'VL D', 'VL A32', 'VL A36', 'VL D32', 'VL D36']
        )
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.specification.valid_flag
        assert '[PASS]' in blank_steel_plate.specification.message
        blank_steel_plate.specification.value = 'VL E'
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.specification.valid_flag
        assert '[FAIL]' in blank_steel_plate.specification.message

    # Delivery Condition
    def test_delivery_condition(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='DeliveryConditionLimit',
            limit_type=LimitType.SCOPE,
            scope=['AR']
        )
        blank_steel_plate.delivery_condition.value = 'AR'
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.delivery_condition.valid_flag
        assert '[PASS]' in blank_steel_plate.delivery_condition.message
        blank_steel_plate.delivery_condition.value = 'TM'
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.delivery_condition.valid_flag
        assert '[FAIL]' in blank_steel_plate.delivery_condition.message

    # Thickness
    def test_thickness(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        # steel making type is None
        blank_steel_plate.steel_making_type.value = None
        with pytest.raises(ValueError) as e:
            rule_maker.get_rules(blank_steel_plate)
        assert str(
            e.value) == f"The steel making type value {blank_steel_plate.steel_making_type.value} is not expected."
        # steel making type is BOC, CC
        blank_steel_plate.steel_making_type.value = 'BOC, CC'
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ThicknessLimit',
            limit_type=LimitType.RANGE,
            maximum=17,
            minimum=0
        )
        blank_steel_plate.thickness.value = 16
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.thickness.valid_flag
        assert '[PASS]' in blank_steel_plate.thickness.message
        blank_steel_plate.thickness.value = 17
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.thickness.valid_flag
        assert '[PASS]' in blank_steel_plate.thickness.message
        blank_steel_plate.thickness.value = 18
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.thickness.valid_flag
        assert '[FAIL]' in blank_steel_plate.thickness.message
        # steel making type is EAF, CC
        blank_steel_plate.steel_making_type.value = 'EAF, CC'
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ThicknessLimit',
            limit_type=LimitType.RANGE,
            maximum=20,
            minimum=0
        )
        blank_steel_plate.thickness.value = 19
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.thickness.valid_flag
        assert '[PASS]' in blank_steel_plate.thickness.message
        blank_steel_plate.thickness.value = 20
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.thickness.valid_flag
        assert '[PASS]' in blank_steel_plate.thickness.message
        blank_steel_plate.thickness.value = 21
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.thickness.valid_flag
        assert '[FAIL]' in blank_steel_plate.thickness.message

    # Chemical Composition
    # C
    def test_element_c(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ChemicalCompositionLimit',
            chemical_element='C',
            limit_type=LimitType.MAXIMUM,
            maximum=0.18,
            minimum=None
        )
        blank_steel_plate.chemical_compositions['C'].set_value(0.17)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['C'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['C'].message
        blank_steel_plate.chemical_compositions['C'].set_value(0.18)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['C'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['C'].message
        blank_steel_plate.chemical_compositions['C'].set_value(0.19)
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.chemical_compositions['C'].valid_flag
        assert '[FAIL]' in blank_steel_plate.chemical_compositions['C'].message

    # Si
    def test_element_si(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ChemicalCompositionLimit',
            chemical_element='Si',
            limit_type=LimitType.MAXIMUM,
            maximum=0.50,
            minimum=None
        )
        blank_steel_plate.chemical_compositions['Si'].set_value(0.49)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Si'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Si'].message
        blank_steel_plate.chemical_compositions['Si'].set_value(0.50)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Si'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Si'].message
        blank_steel_plate.chemical_compositions['Si'].set_value(0.51)
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.chemical_compositions['Si'].valid_flag
        assert '[FAIL]' in blank_steel_plate.chemical_compositions['Si'].message

    # Mn
    def test_element_mn(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification

        blank_steel_plate.thickness.value = 12.4
        limit_list = rule_maker.get_rules(blank_steel_plate)
        self.get_limit(
            limit_list=limit_list,
            limit_class='ChemicalCompositionLimit',
            chemical_element='Mn',
            limit_type=LimitType.RANGE,
            maximum=1.60,
            minimum=0.70
        )

        blank_steel_plate.thickness.value = 12.5
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ChemicalCompositionLimit',
            chemical_element='Mn',
            limit_type=LimitType.RANGE,
            maximum=1.60,
            minimum=0.70
        )
        blank_steel_plate.chemical_compositions['Mn'].set_value(0.69)
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.chemical_compositions['Mn'].valid_flag
        assert '[FAIL]' in blank_steel_plate.chemical_compositions['Mn'].message
        blank_steel_plate.chemical_compositions['Mn'].set_value(0.70)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Mn'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Mn'].message
        blank_steel_plate.chemical_compositions['Mn'].set_value(0.71)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Mn'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Mn'].message
        blank_steel_plate.chemical_compositions['Mn'].set_value(1.59)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Mn'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Mn'].message
        blank_steel_plate.chemical_compositions['Mn'].set_value(1.60)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Mn'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Mn'].message
        blank_steel_plate.chemical_compositions['Mn'].set_value(1.61)
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.chemical_compositions['Mn'].valid_flag
        assert '[FAIL]' in blank_steel_plate.chemical_compositions['Mn'].message

        blank_steel_plate.thickness.value = 12.6
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ChemicalCompositionLimit',
            chemical_element='Mn',
            limit_type=LimitType.RANGE,
            maximum=1.60,
            minimum=0.90
        )
        blank_steel_plate.chemical_compositions['Mn'].set_value(0.89)
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.chemical_compositions['Mn'].valid_flag
        assert '[FAIL]' in blank_steel_plate.chemical_compositions['Mn'].message
        blank_steel_plate.chemical_compositions['Mn'].set_value(0.90)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Mn'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Mn'].message
        blank_steel_plate.chemical_compositions['Mn'].set_value(0.91)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Mn'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Mn'].message
        blank_steel_plate.chemical_compositions['Mn'].set_value(1.59)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Mn'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Mn'].message
        blank_steel_plate.chemical_compositions['Mn'].set_value(1.60)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Mn'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Mn'].message
        blank_steel_plate.chemical_compositions['Mn'].set_value(1.61)
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.chemical_compositions['Mn'].valid_flag
        assert '[FAIL]' in blank_steel_plate.chemical_compositions['Mn'].message

    # P
    def test_element_p(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ChemicalCompositionLimit',
            chemical_element='P',
            limit_type=LimitType.MAXIMUM,
            maximum=0.035,
            minimum=None
        )
        blank_steel_plate.chemical_compositions['P'].set_value(0.034)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['P'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['P'].message
        blank_steel_plate.chemical_compositions['P'].set_value(0.035)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['P'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['P'].message
        blank_steel_plate.chemical_compositions['P'].set_value(0.036)
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.chemical_compositions['P'].valid_flag
        assert '[FAIL]' in blank_steel_plate.chemical_compositions['P'].message

    # S
    def test_element_s(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ChemicalCompositionLimit',
            chemical_element='S',
            limit_type=LimitType.MAXIMUM,
            maximum=0.035,
            minimum=None
        )
        blank_steel_plate.chemical_compositions['S'].set_value(0.034)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['S'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['S'].message
        blank_steel_plate.chemical_compositions['S'].set_value(0.035)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['S'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['S'].message
        blank_steel_plate.chemical_compositions['S'].set_value(0.036)
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.chemical_compositions['S'].valid_flag
        assert '[FAIL]' in blank_steel_plate.chemical_compositions['S'].message

    # Cu
    def test_element_cu(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ChemicalCompositionLimit',
            chemical_element='Cu',
            limit_type=LimitType.MAXIMUM,
            maximum=0.35,
            minimum=None
        )
        blank_steel_plate.chemical_compositions['Cu'].set_value(0.34)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Cu'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Cu'].message
        blank_steel_plate.chemical_compositions['Cu'].set_value(0.35)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Cu'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Cu'].message
        blank_steel_plate.chemical_compositions['Cu'].set_value(0.36)
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.chemical_compositions['Cu'].valid_flag
        assert '[FAIL]' in blank_steel_plate.chemical_compositions['Cu'].message

    # Cr
    def test_element_cr(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ChemicalCompositionLimit',
            chemical_element='Cr',
            limit_type=LimitType.MAXIMUM,
            maximum=0.20,
            minimum=None
        )
        blank_steel_plate.chemical_compositions['Cr'].set_value(0.19)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Cr'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Cr'].message
        blank_steel_plate.chemical_compositions['Cr'].set_value(0.20)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Cr'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Cr'].message
        blank_steel_plate.chemical_compositions['Cr'].set_value(0.21)
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.chemical_compositions['Cr'].valid_flag
        assert '[FAIL]' in blank_steel_plate.chemical_compositions['Cr'].message

    # Ni
    def test_element_ni(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ChemicalCompositionLimit',
            chemical_element='Ni',
            limit_type=LimitType.MAXIMUM,
            maximum=0.40,
            minimum=None
        )
        blank_steel_plate.chemical_compositions['Ni'].set_value(0.39)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Ni'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Ni'].message
        blank_steel_plate.chemical_compositions['Ni'].set_value(0.40)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Ni'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Ni'].message
        blank_steel_plate.chemical_compositions['Ni'].set_value(0.41)
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.chemical_compositions['Ni'].valid_flag
        assert '[FAIL]' in blank_steel_plate.chemical_compositions['Ni'].message

    # Mo
    def test_element_mo(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ChemicalCompositionLimit',
            chemical_element='Mo',
            limit_type=LimitType.MAXIMUM,
            maximum=0.08,
            minimum=None
        )
        blank_steel_plate.chemical_compositions['Mo'].set_value(0.07)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Mo'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Mo'].message
        blank_steel_plate.chemical_compositions['Mo'].set_value(0.08)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Mo'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Mo'].message
        blank_steel_plate.chemical_compositions['Mo'].set_value(0.09)
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.chemical_compositions['Mo'].valid_flag
        assert '[FAIL]' in blank_steel_plate.chemical_compositions['Mo'].message

    # Ceq
    # Because all plates delivered by LongTeng is AR, No Ceq check should be performed
    def test_element_ceq(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        blank_steel_plate.delivery_condition.value = 'AR'
        limit_list = rule_maker.get_rules(blank_steel_plate)
        assert not any(
            [isinstance(limit, ChemicalCompositionLimit) and limit.chemical_element == 'Ceq' for limit in limit_list]
        )

    # Mechanical Properties
    # Yield Strength
    def test_yield_strength(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='YieldStrengthLimit',
            limit_type=LimitType.MINIMUM,
            minimum=315
        )
        blank_steel_plate.yield_strength.value = 314
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.yield_strength.valid_flag
        assert '[FAIL]' in blank_steel_plate.yield_strength.message
        blank_steel_plate.yield_strength.value = 315
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.yield_strength.valid_flag
        assert '[PASS]' in blank_steel_plate.yield_strength.message
        blank_steel_plate.yield_strength.value = 316
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.yield_strength.valid_flag
        assert '[PASS]' in blank_steel_plate.yield_strength.message

    # Tensile Strength
    def test_tensile_strength(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='TensileStrengthLimit',
            limit_type=LimitType.RANGE,
            maximum=570,
            minimum=440
        )
        blank_steel_plate.tensile_strength.value = 439
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.tensile_strength.valid_flag
        assert '[FAIL]' in blank_steel_plate.tensile_strength.message
        blank_steel_plate.tensile_strength.value = 440
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.tensile_strength.valid_flag
        assert '[PASS]' in blank_steel_plate.tensile_strength.message
        blank_steel_plate.tensile_strength.value = 441
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.tensile_strength.valid_flag
        assert '[PASS]' in blank_steel_plate.tensile_strength.message
        blank_steel_plate.tensile_strength.value = 569
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.tensile_strength.valid_flag
        assert '[PASS]' in blank_steel_plate.tensile_strength.message
        blank_steel_plate.tensile_strength.value = 570
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.tensile_strength.valid_flag
        assert '[PASS]' in blank_steel_plate.tensile_strength.message
        blank_steel_plate.tensile_strength.value = 571
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.tensile_strength.valid_flag
        assert '[FAIL]' in blank_steel_plate.tensile_strength.message

    # Elongation
    def test_elongation(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ElongationLimit',
            limit_type=LimitType.MINIMUM,
            minimum=22
        )
        blank_steel_plate.elongation.value = 21
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.elongation.valid_flag
        assert '[FAIL]' in blank_steel_plate.elongation.message
        blank_steel_plate.elongation.value = 22
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.elongation.valid_flag
        assert '[PASS]' in blank_steel_plate.elongation.message
        blank_steel_plate.elongation.value = 23
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.elongation.valid_flag
        assert '[PASS]' in blank_steel_plate.elongation.message

    # Temperature
    def test_temperature(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        # For VL D, in the LongTeng agreement document, the possible maximum thickness is 19
        limit_list = rule_maker.get_rules(blank_steel_plate)
        # For VL D, maximum thickness 19, the maximum test temperature should be -20
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='TemperatureLimit',
            limit_type=LimitType.MAXIMUM,
            maximum=0
        )
        blank_steel_plate.temperature.value = -1
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.temperature.valid_flag
        assert '[PASS]' in blank_steel_plate.temperature.message
        blank_steel_plate.temperature.value = 0
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.temperature.valid_flag
        assert '[PASS]' in blank_steel_plate.temperature.message
        blank_steel_plate.temperature.value = 1
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.temperature.valid_flag
        assert '[FAIL]' in blank_steel_plate.temperature.message

    # Impact Energy
    def test_impact_energy(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        # For VL D, in the LongTeng agreement document, the possible maximum thickness is 19
        blank_steel_plate.thickness.value = 20
        limit_list = rule_maker.get_rules(blank_steel_plate)
        # For VL D, maximum thickness 19, direction LONGITUDINAL, minimum impact energy should be 27
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ImpactEnergyLimit',
            limit_type=LimitType.MINIMUM,
            minimum=31
        )
        blank_steel_plate.impact_energy_list = [
            ImpactEnergy(
                table_index=None,
                x_coordinate=None,
                y_coordinate=None,
                value=30,
                index=None,
                valid_flag=True,
                message=None,
                test_number='1'
            ),
            ImpactEnergy(
                table_index=None,
                x_coordinate=None,
                y_coordinate=None,
                value=31,
                index=None,
                valid_flag=True,
                message=None,
                test_number='2'
            ),
            ImpactEnergy(
                table_index=None,
                x_coordinate=None,
                y_coordinate=None,
                value=32,
                index=None,
                valid_flag=True,
                message=None,
                test_number='3'
            ),
            ImpactEnergy(
                table_index=None,
                x_coordinate=None,
                y_coordinate=None,
                value=33,
                index=None,
                valid_flag=True,
                message=None,
                test_number='Avg'
            )
        ]
        assert not limit.verify(blank_steel_plate)  # one of the energies must violates the limit
        assert blank_steel_plate.impact_energy_list[0].test_number == '1'
        assert not blank_steel_plate.impact_energy_list[0].valid_flag
        assert '[FAIL]' in blank_steel_plate.impact_energy_list[0].message
        assert blank_steel_plate.impact_energy_list[1].test_number == '2'
        assert blank_steel_plate.impact_energy_list[1].valid_flag
        assert '[PASS]' in blank_steel_plate.impact_energy_list[1].message
        assert blank_steel_plate.impact_energy_list[2].test_number == '3'
        assert blank_steel_plate.impact_energy_list[2].valid_flag
        assert '[PASS]' in blank_steel_plate.impact_energy_list[2].message
        assert blank_steel_plate.impact_energy_list[3].test_number == 'Avg'
        assert blank_steel_plate.impact_energy_list[3].valid_flag
        assert '[PASS]' in blank_steel_plate.impact_energy_list[3].message

    # Fine Grain Element
    def test_fine_grain_elements(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        # 5 kinds of situations for steel making types: BOC, CC; EAF, CC; value is None; invalid value; None
        # value is None
        blank_steel_plate.steel_making_type.value = None
        with pytest.raises(ValueError) as e:
            rule_maker.get_rules(blank_steel_plate)
        assert str(
            e.value) == f"The steel making type value {blank_steel_plate.steel_making_type.value} is not expected."
        # BOC, CC
        blank_steel_plate.steel_making_type.value = 'BOC, CC'
        # when thickness <= 15, Al+Nb / Al+V apply; when thickness <= 17, Al applies.
        blank_steel_plate.thickness.value = 17
        limit_list = rule_maker.get_rules(blank_steel_plate)
        hit_limits = [limit for limit in limit_list if isinstance(limit, FineGrainElementLimitCombination)]
        assert len(hit_limits) == 1
        fine_grain_element_limit_combination = hit_limits[0]
        assert len(fine_grain_element_limit_combination.fine_grain_element_limits) == 1
        fine_grain_element_limit = fine_grain_element_limit_combination.fine_grain_element_limits[0]
        assert isinstance(fine_grain_element_limit, FineGrainElementLimit)
        assert len(fine_grain_element_limit.concurrent_limits) == 1
        chemical_composition_limit = fine_grain_element_limit.concurrent_limits[0]
        assert chemical_composition_limit.chemical_element == 'Al'
        assert chemical_composition_limit.limit_type == LimitType.MINIMUM
        assert chemical_composition_limit.minimum == 0.020

        blank_steel_plate.thickness.value = 15
        limit_list = rule_maker.get_rules(blank_steel_plate)
        hit_limits = [limit for limit in limit_list if isinstance(limit, FineGrainElementLimitCombination)]
        assert len(hit_limits) == 1
        fine_grain_element_limit_combination = hit_limits[0]
        assert len(fine_grain_element_limit_combination.fine_grain_element_limits) == 3
        # Al
        assert any(
            [
                isinstance(limit, FineGrainElementLimit)
                and len(limit.concurrent_limits) == 1
                and limit.concurrent_limits[0].chemical_element == 'Al'
                and limit.concurrent_limits[0].limit_type == LimitType.MINIMUM
                and limit.concurrent_limits[0].minimum == 0.020
                for limit in fine_grain_element_limit_combination.fine_grain_element_limits
            ]
        )
        # Al+Nb
        assert any(
            [
                isinstance(limit, FineGrainElementLimit)
                and len(limit.concurrent_limits) == 3
                and any(
                    [
                        concurrent_limit.chemical_element == 'Al'
                        and concurrent_limit.limit_type == LimitType.MINIMUM
                        and concurrent_limit.minimum == 0.015
                        for concurrent_limit in limit.concurrent_limits
                    ]
                )
                and any(
                    [
                        concurrent_limit.chemical_element == 'Nb'
                        and concurrent_limit.limit_type == LimitType.MINIMUM
                        and concurrent_limit.minimum == 0.010
                        for concurrent_limit in limit.concurrent_limits
                    ]
                )
                and any(
                    [
                        concurrent_limit.chemical_element == 'Nb + V + Ti'
                        and concurrent_limit.limit_type == LimitType.MAXIMUM
                        and concurrent_limit.maximum == 0.12
                        for concurrent_limit in limit.concurrent_limits
                    ]
                )
                for limit in fine_grain_element_limit_combination.fine_grain_element_limits
            ]
        )
        # Al+V
        assert any(
            [
                isinstance(limit, FineGrainElementLimit)
                and len(limit.concurrent_limits) == 3
                and any(
                    [
                        concurrent_limit.chemical_element == 'Al'
                        and concurrent_limit.limit_type == LimitType.MINIMUM
                        and concurrent_limit.minimum == 0.015
                        for concurrent_limit in limit.concurrent_limits
                    ]
                )
                and any(
                    [
                        concurrent_limit.chemical_element == 'V'
                        and concurrent_limit.limit_type == LimitType.MINIMUM
                        and concurrent_limit.minimum == 0.030
                        for concurrent_limit in limit.concurrent_limits
                    ]
                )
                and any(
                    [
                        concurrent_limit.chemical_element == 'Nb + V + Ti'
                        and concurrent_limit.limit_type == LimitType.MAXIMUM
                        and concurrent_limit.maximum == 0.12
                        for concurrent_limit in limit.concurrent_limits
                    ]
                )
                for limit in fine_grain_element_limit_combination.fine_grain_element_limits
            ]
        )
        # EAF, CC
        blank_steel_plate.steel_making_type.value = 'EAF, CC'
        limit_list = rule_maker.get_rules(blank_steel_plate)
        hit_limits = [limit for limit in limit_list if isinstance(limit, FineGrainElementLimitCombination)]
        assert len(hit_limits) == 1
        fine_grain_element_limit_combination = hit_limits[0]
        assert len(fine_grain_element_limit_combination.fine_grain_element_limits) == 3
        # Al
        assert any(
            [
                isinstance(limit, FineGrainElementLimit)
                and len(limit.concurrent_limits) == 1
                and limit.concurrent_limits[0].chemical_element == 'Al'
                and limit.concurrent_limits[0].limit_type == LimitType.MINIMUM
                and limit.concurrent_limits[0].minimum == 0.020
                for limit in fine_grain_element_limit_combination.fine_grain_element_limits
            ]
        )
        # Nb
        assert any(
            [
                isinstance(limit, FineGrainElementLimit)
                and len(limit.concurrent_limits) == 1
                and limit.concurrent_limits[0].chemical_element == 'Nb'
                and limit.concurrent_limits[0].limit_type == LimitType.RANGE
                and limit.concurrent_limits[0].maximum == 0.050
                and limit.concurrent_limits[0].minimum == 0.020
                for limit in fine_grain_element_limit_combination.fine_grain_element_limits
            ]
        )
        # Al+Nb
        assert any(
            [
                isinstance(limit, FineGrainElementLimit)
                and len(limit.concurrent_limits) == 3
                and any(
                    [
                        concurrent_limit.chemical_element == 'Al'
                        and concurrent_limit.limit_type == LimitType.MINIMUM
                        and concurrent_limit.minimum == 0.015
                        for concurrent_limit in limit.concurrent_limits
                    ]
                )
                and any(
                    [
                        concurrent_limit.chemical_element == 'Nb'
                        and concurrent_limit.limit_type == LimitType.MINIMUM
                        and concurrent_limit.minimum == 0.010
                        for concurrent_limit in limit.concurrent_limits
                    ]
                )
                and any(
                    [
                        concurrent_limit.chemical_element == 'Nb + V + Ti'
                        and concurrent_limit.limit_type == LimitType.MAXIMUM
                        and concurrent_limit.maximum == 0.12
                        for concurrent_limit in limit.concurrent_limits
                    ]
                )
                for limit in fine_grain_element_limit_combination.fine_grain_element_limits
            ]
        )
        # invalid value
        blank_steel_plate.steel_making_type.value = 'N/A'
        with pytest.raises(ValueError) as excinfo:
            rule_maker.get_rules(blank_steel_plate)
        assert str(excinfo.value) == (
            f"The steel making type value {blank_steel_plate.steel_making_type.value} is not expected."
        )
        # None
        blank_steel_plate.steel_making_type = None
        with pytest.raises(ValueError) as e:
            rule_maker.get_rules(blank_steel_plate)
        assert str(e.value) == "The steel making type is not instantiated in the steel plate."


class TestVLA36(BaseTester):

    def setup_class(self):
        self.specification = 'VL A36'

    # Special Rules
    # Specification
    def test_specification(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='SpecificationLimit',
            limit_type=LimitType.SCOPE,
            scope=['VL A', 'VL B', 'VL D', 'VL A32', 'VL A36', 'VL D32', 'VL D36']
        )
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.specification.valid_flag
        assert '[PASS]' in blank_steel_plate.specification.message
        blank_steel_plate.specification.value = 'VL E'
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.specification.valid_flag
        assert '[FAIL]' in blank_steel_plate.specification.message

    # Delivery Condition
    def test_delivery_condition(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='DeliveryConditionLimit',
            limit_type=LimitType.SCOPE,
            scope=['AR']
        )
        blank_steel_plate.delivery_condition.value = 'AR'
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.delivery_condition.valid_flag
        assert '[PASS]' in blank_steel_plate.delivery_condition.message
        blank_steel_plate.delivery_condition.value = 'TM'
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.delivery_condition.valid_flag
        assert '[FAIL]' in blank_steel_plate.delivery_condition.message

    # Thickness
    def test_thickness(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        # steel making type is None
        blank_steel_plate.steel_making_type.value = None
        with pytest.raises(ValueError) as e:
            rule_maker.get_rules(blank_steel_plate)
        assert str(
            e.value) == f"The steel making type value {blank_steel_plate.steel_making_type.value} is not expected."
        # steel making type is BOC, CC
        blank_steel_plate.steel_making_type.value = 'BOC, CC'
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ThicknessLimit',
            limit_type=LimitType.RANGE,
            maximum=17,
            minimum=0
        )
        blank_steel_plate.thickness.value = 16
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.thickness.valid_flag
        assert '[PASS]' in blank_steel_plate.thickness.message
        blank_steel_plate.thickness.value = 17
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.thickness.valid_flag
        assert '[PASS]' in blank_steel_plate.thickness.message
        blank_steel_plate.thickness.value = 18
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.thickness.valid_flag
        assert '[FAIL]' in blank_steel_plate.thickness.message
        # steel making type is EAF, CC
        blank_steel_plate.steel_making_type.value = 'EAF, CC'
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ThicknessLimit',
            limit_type=LimitType.RANGE,
            maximum=20,
            minimum=0
        )
        blank_steel_plate.thickness.value = 19
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.thickness.valid_flag
        assert '[PASS]' in blank_steel_plate.thickness.message
        blank_steel_plate.thickness.value = 20
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.thickness.valid_flag
        assert '[PASS]' in blank_steel_plate.thickness.message
        blank_steel_plate.thickness.value = 21
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.thickness.valid_flag
        assert '[FAIL]' in blank_steel_plate.thickness.message

    # Chemical Composition
    # C
    def test_element_c(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ChemicalCompositionLimit',
            chemical_element='C',
            limit_type=LimitType.MAXIMUM,
            maximum=0.18,
            minimum=None
        )
        blank_steel_plate.chemical_compositions['C'].set_value(0.17)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['C'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['C'].message
        blank_steel_plate.chemical_compositions['C'].set_value(0.18)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['C'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['C'].message
        blank_steel_plate.chemical_compositions['C'].set_value(0.19)
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.chemical_compositions['C'].valid_flag
        assert '[FAIL]' in blank_steel_plate.chemical_compositions['C'].message

    # Si
    def test_element_si(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ChemicalCompositionLimit',
            chemical_element='Si',
            limit_type=LimitType.MAXIMUM,
            maximum=0.50,
            minimum=None
        )
        blank_steel_plate.chemical_compositions['Si'].set_value(0.49)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Si'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Si'].message
        blank_steel_plate.chemical_compositions['Si'].set_value(0.50)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Si'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Si'].message
        blank_steel_plate.chemical_compositions['Si'].set_value(0.51)
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.chemical_compositions['Si'].valid_flag
        assert '[FAIL]' in blank_steel_plate.chemical_compositions['Si'].message

    # Mn
    def test_element_mn(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification

        blank_steel_plate.thickness.value = 12.4
        limit_list = rule_maker.get_rules(blank_steel_plate)
        self.get_limit(
            limit_list=limit_list,
            limit_class='ChemicalCompositionLimit',
            chemical_element='Mn',
            limit_type=LimitType.RANGE,
            maximum=1.60,
            minimum=0.70
        )

        blank_steel_plate.thickness.value = 12.5
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ChemicalCompositionLimit',
            chemical_element='Mn',
            limit_type=LimitType.RANGE,
            maximum=1.60,
            minimum=0.70
        )
        blank_steel_plate.chemical_compositions['Mn'].set_value(0.69)
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.chemical_compositions['Mn'].valid_flag
        assert '[FAIL]' in blank_steel_plate.chemical_compositions['Mn'].message
        blank_steel_plate.chemical_compositions['Mn'].set_value(0.70)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Mn'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Mn'].message
        blank_steel_plate.chemical_compositions['Mn'].set_value(0.71)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Mn'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Mn'].message
        blank_steel_plate.chemical_compositions['Mn'].set_value(1.59)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Mn'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Mn'].message
        blank_steel_plate.chemical_compositions['Mn'].set_value(1.60)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Mn'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Mn'].message
        blank_steel_plate.chemical_compositions['Mn'].set_value(1.61)
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.chemical_compositions['Mn'].valid_flag
        assert '[FAIL]' in blank_steel_plate.chemical_compositions['Mn'].message

        blank_steel_plate.thickness.value = 12.6
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ChemicalCompositionLimit',
            chemical_element='Mn',
            limit_type=LimitType.RANGE,
            maximum=1.60,
            minimum=0.90
        )
        blank_steel_plate.chemical_compositions['Mn'].set_value(0.89)
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.chemical_compositions['Mn'].valid_flag
        assert '[FAIL]' in blank_steel_plate.chemical_compositions['Mn'].message
        blank_steel_plate.chemical_compositions['Mn'].set_value(0.90)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Mn'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Mn'].message
        blank_steel_plate.chemical_compositions['Mn'].set_value(0.91)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Mn'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Mn'].message
        blank_steel_plate.chemical_compositions['Mn'].set_value(1.59)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Mn'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Mn'].message
        blank_steel_plate.chemical_compositions['Mn'].set_value(1.60)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Mn'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Mn'].message
        blank_steel_plate.chemical_compositions['Mn'].set_value(1.61)
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.chemical_compositions['Mn'].valid_flag
        assert '[FAIL]' in blank_steel_plate.chemical_compositions['Mn'].message

    # P
    def test_element_p(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ChemicalCompositionLimit',
            chemical_element='P',
            limit_type=LimitType.MAXIMUM,
            maximum=0.035,
            minimum=None
        )
        blank_steel_plate.chemical_compositions['P'].set_value(0.034)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['P'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['P'].message
        blank_steel_plate.chemical_compositions['P'].set_value(0.035)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['P'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['P'].message
        blank_steel_plate.chemical_compositions['P'].set_value(0.036)
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.chemical_compositions['P'].valid_flag
        assert '[FAIL]' in blank_steel_plate.chemical_compositions['P'].message

    # S
    def test_element_s(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ChemicalCompositionLimit',
            chemical_element='S',
            limit_type=LimitType.MAXIMUM,
            maximum=0.035,
            minimum=None
        )
        blank_steel_plate.chemical_compositions['S'].set_value(0.034)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['S'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['S'].message
        blank_steel_plate.chemical_compositions['S'].set_value(0.035)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['S'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['S'].message
        blank_steel_plate.chemical_compositions['S'].set_value(0.036)
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.chemical_compositions['S'].valid_flag
        assert '[FAIL]' in blank_steel_plate.chemical_compositions['S'].message

    # Cu
    def test_element_cu(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ChemicalCompositionLimit',
            chemical_element='Cu',
            limit_type=LimitType.MAXIMUM,
            maximum=0.35,
            minimum=None
        )
        blank_steel_plate.chemical_compositions['Cu'].set_value(0.34)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Cu'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Cu'].message
        blank_steel_plate.chemical_compositions['Cu'].set_value(0.35)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Cu'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Cu'].message
        blank_steel_plate.chemical_compositions['Cu'].set_value(0.36)
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.chemical_compositions['Cu'].valid_flag
        assert '[FAIL]' in blank_steel_plate.chemical_compositions['Cu'].message

    # Cr
    def test_element_cr(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ChemicalCompositionLimit',
            chemical_element='Cr',
            limit_type=LimitType.MAXIMUM,
            maximum=0.20,
            minimum=None
        )
        blank_steel_plate.chemical_compositions['Cr'].set_value(0.19)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Cr'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Cr'].message
        blank_steel_plate.chemical_compositions['Cr'].set_value(0.20)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Cr'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Cr'].message
        blank_steel_plate.chemical_compositions['Cr'].set_value(0.21)
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.chemical_compositions['Cr'].valid_flag
        assert '[FAIL]' in blank_steel_plate.chemical_compositions['Cr'].message

    # Ni
    def test_element_ni(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ChemicalCompositionLimit',
            chemical_element='Ni',
            limit_type=LimitType.MAXIMUM,
            maximum=0.40,
            minimum=None
        )
        blank_steel_plate.chemical_compositions['Ni'].set_value(0.39)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Ni'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Ni'].message
        blank_steel_plate.chemical_compositions['Ni'].set_value(0.40)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Ni'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Ni'].message
        blank_steel_plate.chemical_compositions['Ni'].set_value(0.41)
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.chemical_compositions['Ni'].valid_flag
        assert '[FAIL]' in blank_steel_plate.chemical_compositions['Ni'].message

    # Mo
    def test_element_mo(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ChemicalCompositionLimit',
            chemical_element='Mo',
            limit_type=LimitType.MAXIMUM,
            maximum=0.08,
            minimum=None
        )
        blank_steel_plate.chemical_compositions['Mo'].set_value(0.07)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Mo'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Mo'].message
        blank_steel_plate.chemical_compositions['Mo'].set_value(0.08)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Mo'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Mo'].message
        blank_steel_plate.chemical_compositions['Mo'].set_value(0.09)
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.chemical_compositions['Mo'].valid_flag
        assert '[FAIL]' in blank_steel_plate.chemical_compositions['Mo'].message

    # Ceq
    # Because all plates delivered by LongTeng is AR, No Ceq check should be performed
    def test_element_ceq(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        blank_steel_plate.delivery_condition.value = 'AR'
        limit_list = rule_maker.get_rules(blank_steel_plate)
        assert not any(
            [isinstance(limit, ChemicalCompositionLimit) and limit.chemical_element == 'Ceq' for limit in limit_list]
        )

    # Mechanical Properties
    # Yield Strength
    def test_yield_strength(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='YieldStrengthLimit',
            limit_type=LimitType.MINIMUM,
            minimum=355
        )
        blank_steel_plate.yield_strength.value = 354
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.yield_strength.valid_flag
        assert '[FAIL]' in blank_steel_plate.yield_strength.message
        blank_steel_plate.yield_strength.value = 355
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.yield_strength.valid_flag
        assert '[PASS]' in blank_steel_plate.yield_strength.message
        blank_steel_plate.yield_strength.value = 356
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.yield_strength.valid_flag
        assert '[PASS]' in blank_steel_plate.yield_strength.message

    # Tensile Strength
    def test_tensile_strength(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='TensileStrengthLimit',
            limit_type=LimitType.RANGE,
            maximum=630,
            minimum=490
        )
        blank_steel_plate.tensile_strength.value = 489
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.tensile_strength.valid_flag
        assert '[FAIL]' in blank_steel_plate.tensile_strength.message
        blank_steel_plate.tensile_strength.value = 490
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.tensile_strength.valid_flag
        assert '[PASS]' in blank_steel_plate.tensile_strength.message
        blank_steel_plate.tensile_strength.value = 491
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.tensile_strength.valid_flag
        assert '[PASS]' in blank_steel_plate.tensile_strength.message
        blank_steel_plate.tensile_strength.value = 629
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.tensile_strength.valid_flag
        assert '[PASS]' in blank_steel_plate.tensile_strength.message
        blank_steel_plate.tensile_strength.value = 630
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.tensile_strength.valid_flag
        assert '[PASS]' in blank_steel_plate.tensile_strength.message
        blank_steel_plate.tensile_strength.value = 631
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.tensile_strength.valid_flag
        assert '[FAIL]' in blank_steel_plate.tensile_strength.message

    # Elongation
    def test_elongation(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ElongationLimit',
            limit_type=LimitType.MINIMUM,
            minimum=21
        )
        blank_steel_plate.elongation.value = 20
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.elongation.valid_flag
        assert '[FAIL]' in blank_steel_plate.elongation.message
        blank_steel_plate.elongation.value = 21
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.elongation.valid_flag
        assert '[PASS]' in blank_steel_plate.elongation.message
        blank_steel_plate.elongation.value = 22
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.elongation.valid_flag
        assert '[PASS]' in blank_steel_plate.elongation.message

    # Temperature
    def test_temperature(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        # For VL D, in the LongTeng agreement document, the possible maximum thickness is 19
        limit_list = rule_maker.get_rules(blank_steel_plate)
        # For VL D, maximum thickness 19, the maximum test temperature should be -20
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='TemperatureLimit',
            limit_type=LimitType.MAXIMUM,
            maximum=0
        )
        blank_steel_plate.temperature.value = -1
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.temperature.valid_flag
        assert '[PASS]' in blank_steel_plate.temperature.message
        blank_steel_plate.temperature.value = 0
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.temperature.valid_flag
        assert '[PASS]' in blank_steel_plate.temperature.message
        blank_steel_plate.temperature.value = 1
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.temperature.valid_flag
        assert '[FAIL]' in blank_steel_plate.temperature.message

    # Impact Energy
    def test_impact_energy(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        # For VL D, in the LongTeng agreement document, the possible maximum thickness is 19
        blank_steel_plate.thickness.value = 20
        limit_list = rule_maker.get_rules(blank_steel_plate)
        # For VL D, maximum thickness 19, direction LONGITUDINAL, minimum impact energy should be 27
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ImpactEnergyLimit',
            limit_type=LimitType.MINIMUM,
            minimum=34
        )
        blank_steel_plate.impact_energy_list = [
            ImpactEnergy(
                table_index=None,
                x_coordinate=None,
                y_coordinate=None,
                value=33,
                index=None,
                valid_flag=True,
                message=None,
                test_number='1'
            ),
            ImpactEnergy(
                table_index=None,
                x_coordinate=None,
                y_coordinate=None,
                value=34,
                index=None,
                valid_flag=True,
                message=None,
                test_number='2'
            ),
            ImpactEnergy(
                table_index=None,
                x_coordinate=None,
                y_coordinate=None,
                value=35,
                index=None,
                valid_flag=True,
                message=None,
                test_number='3'
            ),
            ImpactEnergy(
                table_index=None,
                x_coordinate=None,
                y_coordinate=None,
                value=36,
                index=None,
                valid_flag=True,
                message=None,
                test_number='Avg'
            )
        ]
        assert not limit.verify(blank_steel_plate)  # one of the energies must violates the limit
        assert blank_steel_plate.impact_energy_list[0].test_number == '1'
        assert not blank_steel_plate.impact_energy_list[0].valid_flag
        assert '[FAIL]' in blank_steel_plate.impact_energy_list[0].message
        assert blank_steel_plate.impact_energy_list[1].test_number == '2'
        assert blank_steel_plate.impact_energy_list[1].valid_flag
        assert '[PASS]' in blank_steel_plate.impact_energy_list[1].message
        assert blank_steel_plate.impact_energy_list[2].test_number == '3'
        assert blank_steel_plate.impact_energy_list[2].valid_flag
        assert '[PASS]' in blank_steel_plate.impact_energy_list[2].message
        assert blank_steel_plate.impact_energy_list[3].test_number == 'Avg'
        assert blank_steel_plate.impact_energy_list[3].valid_flag
        assert '[PASS]' in blank_steel_plate.impact_energy_list[3].message

    # Fine Grain Element
    def test_fine_grain_elements(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        # 5 kinds of situations for steel making types: BOC, CC; EAF, CC; value is None; invalid value; None
        # value is None
        blank_steel_plate.steel_making_type.value = None
        with pytest.raises(ValueError) as e:
            rule_maker.get_rules(blank_steel_plate)
        assert str(
            e.value) == f"The steel making type value {blank_steel_plate.steel_making_type.value} is not expected."
        # BOC, CC
        blank_steel_plate.steel_making_type.value = 'BOC, CC'
        # when thickness <= 15, Al+Nb / Al+V apply; when thickness <= 17, Al applies.
        blank_steel_plate.thickness.value = 17
        limit_list = rule_maker.get_rules(blank_steel_plate)
        hit_limits = [limit for limit in limit_list if isinstance(limit, FineGrainElementLimitCombination)]
        assert len(hit_limits) == 1
        fine_grain_element_limit_combination = hit_limits[0]
        assert len(fine_grain_element_limit_combination.fine_grain_element_limits) == 1
        fine_grain_element_limit = fine_grain_element_limit_combination.fine_grain_element_limits[0]
        assert isinstance(fine_grain_element_limit, FineGrainElementLimit)
        assert len(fine_grain_element_limit.concurrent_limits) == 1
        chemical_composition_limit = fine_grain_element_limit.concurrent_limits[0]
        assert chemical_composition_limit.chemical_element == 'Al'
        assert chemical_composition_limit.limit_type == LimitType.MINIMUM
        assert chemical_composition_limit.minimum == 0.020

        blank_steel_plate.thickness.value = 15
        limit_list = rule_maker.get_rules(blank_steel_plate)
        hit_limits = [limit for limit in limit_list if isinstance(limit, FineGrainElementLimitCombination)]
        assert len(hit_limits) == 1
        fine_grain_element_limit_combination = hit_limits[0]
        assert len(fine_grain_element_limit_combination.fine_grain_element_limits) == 3
        # Al
        assert any(
            [
                isinstance(limit, FineGrainElementLimit)
                and len(limit.concurrent_limits) == 1
                and limit.concurrent_limits[0].chemical_element == 'Al'
                and limit.concurrent_limits[0].limit_type == LimitType.MINIMUM
                and limit.concurrent_limits[0].minimum == 0.020
                for limit in fine_grain_element_limit_combination.fine_grain_element_limits
            ]
        )
        # Al+Nb
        assert any(
            [
                isinstance(limit, FineGrainElementLimit)
                and len(limit.concurrent_limits) == 3
                and any(
                    [
                        concurrent_limit.chemical_element == 'Al'
                        and concurrent_limit.limit_type == LimitType.MINIMUM
                        and concurrent_limit.minimum == 0.015
                        for concurrent_limit in limit.concurrent_limits
                    ]
                )
                and any(
                    [
                        concurrent_limit.chemical_element == 'Nb'
                        and concurrent_limit.limit_type == LimitType.MINIMUM
                        and concurrent_limit.minimum == 0.010
                        for concurrent_limit in limit.concurrent_limits
                    ]
                )
                and any(
                    [
                        concurrent_limit.chemical_element == 'Nb + V + Ti'
                        and concurrent_limit.limit_type == LimitType.MAXIMUM
                        and concurrent_limit.maximum == 0.12
                        for concurrent_limit in limit.concurrent_limits
                    ]
                )
                for limit in fine_grain_element_limit_combination.fine_grain_element_limits
            ]
        )
        # Al+V
        assert any(
            [
                isinstance(limit, FineGrainElementLimit)
                and len(limit.concurrent_limits) == 3
                and any(
                    [
                        concurrent_limit.chemical_element == 'Al'
                        and concurrent_limit.limit_type == LimitType.MINIMUM
                        and concurrent_limit.minimum == 0.015
                        for concurrent_limit in limit.concurrent_limits
                    ]
                )
                and any(
                    [
                        concurrent_limit.chemical_element == 'V'
                        and concurrent_limit.limit_type == LimitType.MINIMUM
                        and concurrent_limit.minimum == 0.030
                        for concurrent_limit in limit.concurrent_limits
                    ]
                )
                and any(
                    [
                        concurrent_limit.chemical_element == 'Nb + V + Ti'
                        and concurrent_limit.limit_type == LimitType.MAXIMUM
                        and concurrent_limit.maximum == 0.12
                        for concurrent_limit in limit.concurrent_limits
                    ]
                )
                for limit in fine_grain_element_limit_combination.fine_grain_element_limits
            ]
        )
        # EAF, CC
        blank_steel_plate.steel_making_type.value = 'EAF, CC'
        limit_list = rule_maker.get_rules(blank_steel_plate)
        hit_limits = [limit for limit in limit_list if isinstance(limit, FineGrainElementLimitCombination)]
        assert len(hit_limits) == 1
        fine_grain_element_limit_combination = hit_limits[0]
        assert len(fine_grain_element_limit_combination.fine_grain_element_limits) == 3
        # Al
        assert any(
            [
                isinstance(limit, FineGrainElementLimit)
                and len(limit.concurrent_limits) == 1
                and limit.concurrent_limits[0].chemical_element == 'Al'
                and limit.concurrent_limits[0].limit_type == LimitType.MINIMUM
                and limit.concurrent_limits[0].minimum == 0.020
                for limit in fine_grain_element_limit_combination.fine_grain_element_limits
            ]
        )
        # Nb
        assert any(
            [
                isinstance(limit, FineGrainElementLimit)
                and len(limit.concurrent_limits) == 1
                and limit.concurrent_limits[0].chemical_element == 'Nb'
                and limit.concurrent_limits[0].limit_type == LimitType.RANGE
                and limit.concurrent_limits[0].maximum == 0.050
                and limit.concurrent_limits[0].minimum == 0.020
                for limit in fine_grain_element_limit_combination.fine_grain_element_limits
            ]
        )
        # Al+Nb
        assert any(
            [
                isinstance(limit, FineGrainElementLimit)
                and len(limit.concurrent_limits) == 3
                and any(
                    [
                        concurrent_limit.chemical_element == 'Al'
                        and concurrent_limit.limit_type == LimitType.MINIMUM
                        and concurrent_limit.minimum == 0.015
                        for concurrent_limit in limit.concurrent_limits
                    ]
                )
                and any(
                    [
                        concurrent_limit.chemical_element == 'Nb'
                        and concurrent_limit.limit_type == LimitType.MINIMUM
                        and concurrent_limit.minimum == 0.010
                        for concurrent_limit in limit.concurrent_limits
                    ]
                )
                and any(
                    [
                        concurrent_limit.chemical_element == 'Nb + V + Ti'
                        and concurrent_limit.limit_type == LimitType.MAXIMUM
                        and concurrent_limit.maximum == 0.12
                        for concurrent_limit in limit.concurrent_limits
                    ]
                )
                for limit in fine_grain_element_limit_combination.fine_grain_element_limits
            ]
        )
        # invalid value
        blank_steel_plate.steel_making_type.value = 'N/A'
        with pytest.raises(ValueError) as excinfo:
            rule_maker.get_rules(blank_steel_plate)
        assert str(excinfo.value) == (
            f"The steel making type value {blank_steel_plate.steel_making_type.value} is not expected."
        )
        # None
        blank_steel_plate.steel_making_type = None
        with pytest.raises(ValueError) as e:
            rule_maker.get_rules(blank_steel_plate)
        assert str(e.value) == "The steel making type is not instantiated in the steel plate."


class TestVLD32(BaseTester):

    def setup_class(self):
        self.specification = 'VL D32'

    # Special Rules
    # Specification
    def test_specification(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='SpecificationLimit',
            limit_type=LimitType.SCOPE,
            scope=['VL A', 'VL B', 'VL D', 'VL A32', 'VL A36', 'VL D32', 'VL D36']
        )
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.specification.valid_flag
        assert '[PASS]' in blank_steel_plate.specification.message
        blank_steel_plate.specification.value = 'VL E'
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.specification.valid_flag
        assert '[FAIL]' in blank_steel_plate.specification.message

    # Delivery Condition
    def test_delivery_condition(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='DeliveryConditionLimit',
            limit_type=LimitType.SCOPE,
            scope=['AR']
        )
        blank_steel_plate.delivery_condition.value = 'AR'
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.delivery_condition.valid_flag
        assert '[PASS]' in blank_steel_plate.delivery_condition.message
        blank_steel_plate.delivery_condition.value = 'TM'
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.delivery_condition.valid_flag
        assert '[FAIL]' in blank_steel_plate.delivery_condition.message

    # Thickness
    def test_thickness(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        # steel making type is None
        blank_steel_plate.steel_making_type.value = None
        with pytest.raises(ValueError) as e:
            rule_maker.get_rules(blank_steel_plate)
        assert str(
            e.value) == f"The steel making type value {blank_steel_plate.steel_making_type.value} is not expected."
        # steel making type is BOC, CC
        blank_steel_plate.steel_making_type.value = 'BOC, CC'
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ThicknessLimit',
            limit_type=LimitType.RANGE,
            maximum=17,
            minimum=0
        )
        blank_steel_plate.thickness.value = 16
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.thickness.valid_flag
        assert '[PASS]' in blank_steel_plate.thickness.message
        blank_steel_plate.thickness.value = 17
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.thickness.valid_flag
        assert '[PASS]' in blank_steel_plate.thickness.message
        blank_steel_plate.thickness.value = 18
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.thickness.valid_flag
        assert '[FAIL]' in blank_steel_plate.thickness.message
        # steel making type is EAF, CC
        blank_steel_plate.steel_making_type.value = 'EAF, CC'
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ThicknessLimit',
            limit_type=LimitType.RANGE,
            maximum=19,
            minimum=0
        )
        blank_steel_plate.thickness.value = 18
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.thickness.valid_flag
        assert '[PASS]' in blank_steel_plate.thickness.message
        blank_steel_plate.thickness.value = 19
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.thickness.valid_flag
        assert '[PASS]' in blank_steel_plate.thickness.message
        blank_steel_plate.thickness.value = 20
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.thickness.valid_flag
        assert '[FAIL]' in blank_steel_plate.thickness.message

    # Chemical Composition
    # C
    def test_element_c(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ChemicalCompositionLimit',
            chemical_element='C',
            limit_type=LimitType.MAXIMUM,
            maximum=0.18,
            minimum=None
        )
        blank_steel_plate.chemical_compositions['C'].set_value(0.17)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['C'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['C'].message
        blank_steel_plate.chemical_compositions['C'].set_value(0.18)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['C'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['C'].message
        blank_steel_plate.chemical_compositions['C'].set_value(0.19)
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.chemical_compositions['C'].valid_flag
        assert '[FAIL]' in blank_steel_plate.chemical_compositions['C'].message

    # Si
    def test_element_si(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ChemicalCompositionLimit',
            chemical_element='Si',
            limit_type=LimitType.MAXIMUM,
            maximum=0.50,
            minimum=None
        )
        blank_steel_plate.chemical_compositions['Si'].set_value(0.49)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Si'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Si'].message
        blank_steel_plate.chemical_compositions['Si'].set_value(0.50)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Si'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Si'].message
        blank_steel_plate.chemical_compositions['Si'].set_value(0.51)
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.chemical_compositions['Si'].valid_flag
        assert '[FAIL]' in blank_steel_plate.chemical_compositions['Si'].message

    # Mn
    def test_element_mn(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification

        blank_steel_plate.thickness.value = 12.4
        limit_list = rule_maker.get_rules(blank_steel_plate)
        self.get_limit(
            limit_list=limit_list,
            limit_class='ChemicalCompositionLimit',
            chemical_element='Mn',
            limit_type=LimitType.RANGE,
            maximum=1.60,
            minimum=0.70
        )

        blank_steel_plate.thickness.value = 12.5
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ChemicalCompositionLimit',
            chemical_element='Mn',
            limit_type=LimitType.RANGE,
            maximum=1.60,
            minimum=0.70
        )
        blank_steel_plate.chemical_compositions['Mn'].set_value(0.69)
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.chemical_compositions['Mn'].valid_flag
        assert '[FAIL]' in blank_steel_plate.chemical_compositions['Mn'].message
        blank_steel_plate.chemical_compositions['Mn'].set_value(0.70)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Mn'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Mn'].message
        blank_steel_plate.chemical_compositions['Mn'].set_value(0.71)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Mn'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Mn'].message
        blank_steel_plate.chemical_compositions['Mn'].set_value(1.59)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Mn'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Mn'].message
        blank_steel_plate.chemical_compositions['Mn'].set_value(1.60)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Mn'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Mn'].message
        blank_steel_plate.chemical_compositions['Mn'].set_value(1.61)
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.chemical_compositions['Mn'].valid_flag
        assert '[FAIL]' in blank_steel_plate.chemical_compositions['Mn'].message

        blank_steel_plate.thickness.value = 12.6
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ChemicalCompositionLimit',
            chemical_element='Mn',
            limit_type=LimitType.RANGE,
            maximum=1.60,
            minimum=0.90
        )
        blank_steel_plate.chemical_compositions['Mn'].set_value(0.89)
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.chemical_compositions['Mn'].valid_flag
        assert '[FAIL]' in blank_steel_plate.chemical_compositions['Mn'].message
        blank_steel_plate.chemical_compositions['Mn'].set_value(0.90)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Mn'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Mn'].message
        blank_steel_plate.chemical_compositions['Mn'].set_value(0.91)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Mn'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Mn'].message
        blank_steel_plate.chemical_compositions['Mn'].set_value(1.59)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Mn'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Mn'].message
        blank_steel_plate.chemical_compositions['Mn'].set_value(1.60)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Mn'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Mn'].message
        blank_steel_plate.chemical_compositions['Mn'].set_value(1.61)
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.chemical_compositions['Mn'].valid_flag
        assert '[FAIL]' in blank_steel_plate.chemical_compositions['Mn'].message

    # P
    def test_element_p(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ChemicalCompositionLimit',
            chemical_element='P',
            limit_type=LimitType.MAXIMUM,
            maximum=0.035,
            minimum=None
        )
        blank_steel_plate.chemical_compositions['P'].set_value(0.034)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['P'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['P'].message
        blank_steel_plate.chemical_compositions['P'].set_value(0.035)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['P'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['P'].message
        blank_steel_plate.chemical_compositions['P'].set_value(0.036)
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.chemical_compositions['P'].valid_flag
        assert '[FAIL]' in blank_steel_plate.chemical_compositions['P'].message

    # S
    def test_element_s(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ChemicalCompositionLimit',
            chemical_element='S',
            limit_type=LimitType.MAXIMUM,
            maximum=0.035,
            minimum=None
        )
        blank_steel_plate.chemical_compositions['S'].set_value(0.034)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['S'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['S'].message
        blank_steel_plate.chemical_compositions['S'].set_value(0.035)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['S'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['S'].message
        blank_steel_plate.chemical_compositions['S'].set_value(0.036)
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.chemical_compositions['S'].valid_flag
        assert '[FAIL]' in blank_steel_plate.chemical_compositions['S'].message

    # Cu
    def test_element_cu(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ChemicalCompositionLimit',
            chemical_element='Cu',
            limit_type=LimitType.MAXIMUM,
            maximum=0.35,
            minimum=None
        )
        blank_steel_plate.chemical_compositions['Cu'].set_value(0.34)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Cu'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Cu'].message
        blank_steel_plate.chemical_compositions['Cu'].set_value(0.35)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Cu'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Cu'].message
        blank_steel_plate.chemical_compositions['Cu'].set_value(0.36)
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.chemical_compositions['Cu'].valid_flag
        assert '[FAIL]' in blank_steel_plate.chemical_compositions['Cu'].message

    # Cr
    def test_element_cr(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ChemicalCompositionLimit',
            chemical_element='Cr',
            limit_type=LimitType.MAXIMUM,
            maximum=0.20,
            minimum=None
        )
        blank_steel_plate.chemical_compositions['Cr'].set_value(0.19)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Cr'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Cr'].message
        blank_steel_plate.chemical_compositions['Cr'].set_value(0.20)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Cr'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Cr'].message
        blank_steel_plate.chemical_compositions['Cr'].set_value(0.21)
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.chemical_compositions['Cr'].valid_flag
        assert '[FAIL]' in blank_steel_plate.chemical_compositions['Cr'].message

    # Ni
    def test_element_ni(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ChemicalCompositionLimit',
            chemical_element='Ni',
            limit_type=LimitType.MAXIMUM,
            maximum=0.40,
            minimum=None
        )
        blank_steel_plate.chemical_compositions['Ni'].set_value(0.39)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Ni'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Ni'].message
        blank_steel_plate.chemical_compositions['Ni'].set_value(0.40)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Ni'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Ni'].message
        blank_steel_plate.chemical_compositions['Ni'].set_value(0.41)
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.chemical_compositions['Ni'].valid_flag
        assert '[FAIL]' in blank_steel_plate.chemical_compositions['Ni'].message

    # Mo
    def test_element_mo(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ChemicalCompositionLimit',
            chemical_element='Mo',
            limit_type=LimitType.MAXIMUM,
            maximum=0.08,
            minimum=None
        )
        blank_steel_plate.chemical_compositions['Mo'].set_value(0.07)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Mo'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Mo'].message
        blank_steel_plate.chemical_compositions['Mo'].set_value(0.08)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Mo'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Mo'].message
        blank_steel_plate.chemical_compositions['Mo'].set_value(0.09)
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.chemical_compositions['Mo'].valid_flag
        assert '[FAIL]' in blank_steel_plate.chemical_compositions['Mo'].message

    # Ceq
    # Because all plates delivered by LongTeng is AR, No Ceq check should be performed
    def test_element_ceq(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        blank_steel_plate.delivery_condition.value = 'AR'
        limit_list = rule_maker.get_rules(blank_steel_plate)
        assert not any(
            [isinstance(limit, ChemicalCompositionLimit) and limit.chemical_element == 'Ceq' for limit in limit_list]
        )

    # Mechanical Properties
    # Yield Strength
    def test_yield_strength(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='YieldStrengthLimit',
            limit_type=LimitType.MINIMUM,
            minimum=315
        )
        blank_steel_plate.yield_strength.value = 314
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.yield_strength.valid_flag
        assert '[FAIL]' in blank_steel_plate.yield_strength.message
        blank_steel_plate.yield_strength.value = 315
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.yield_strength.valid_flag
        assert '[PASS]' in blank_steel_plate.yield_strength.message
        blank_steel_plate.yield_strength.value = 316
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.yield_strength.valid_flag
        assert '[PASS]' in blank_steel_plate.yield_strength.message

    # Tensile Strength
    def test_tensile_strength(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='TensileStrengthLimit',
            limit_type=LimitType.RANGE,
            maximum=570,
            minimum=440
        )
        blank_steel_plate.tensile_strength.value = 439
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.tensile_strength.valid_flag
        assert '[FAIL]' in blank_steel_plate.tensile_strength.message
        blank_steel_plate.tensile_strength.value = 440
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.tensile_strength.valid_flag
        assert '[PASS]' in blank_steel_plate.tensile_strength.message
        blank_steel_plate.tensile_strength.value = 441
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.tensile_strength.valid_flag
        assert '[PASS]' in blank_steel_plate.tensile_strength.message
        blank_steel_plate.tensile_strength.value = 569
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.tensile_strength.valid_flag
        assert '[PASS]' in blank_steel_plate.tensile_strength.message
        blank_steel_plate.tensile_strength.value = 570
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.tensile_strength.valid_flag
        assert '[PASS]' in blank_steel_plate.tensile_strength.message
        blank_steel_plate.tensile_strength.value = 571
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.tensile_strength.valid_flag
        assert '[FAIL]' in blank_steel_plate.tensile_strength.message

    # Elongation
    def test_elongation(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ElongationLimit',
            limit_type=LimitType.MINIMUM,
            minimum=22
        )
        blank_steel_plate.elongation.value = 21
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.elongation.valid_flag
        assert '[FAIL]' in blank_steel_plate.elongation.message
        blank_steel_plate.elongation.value = 22
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.elongation.valid_flag
        assert '[PASS]' in blank_steel_plate.elongation.message
        blank_steel_plate.elongation.value = 23
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.elongation.valid_flag
        assert '[PASS]' in blank_steel_plate.elongation.message

    # Temperature
    def test_temperature(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        # For VL D, in the LongTeng agreement document, the possible maximum thickness is 19
        limit_list = rule_maker.get_rules(blank_steel_plate)
        # For VL D, maximum thickness 19, the maximum test temperature should be -20
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='TemperatureLimit',
            limit_type=LimitType.MAXIMUM,
            maximum=-20
        )
        blank_steel_plate.temperature.value = -21
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.temperature.valid_flag
        assert '[PASS]' in blank_steel_plate.temperature.message
        blank_steel_plate.temperature.value = -20
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.temperature.valid_flag
        assert '[PASS]' in blank_steel_plate.temperature.message
        blank_steel_plate.temperature.value = -19
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.temperature.valid_flag
        assert '[FAIL]' in blank_steel_plate.temperature.message

    # Impact Energy
    def test_impact_energy(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        # For VL D, in the LongTeng agreement document, the possible maximum thickness is 19
        blank_steel_plate.thickness.value = 20
        limit_list = rule_maker.get_rules(blank_steel_plate)
        # For VL D, maximum thickness 19, direction LONGITUDINAL, minimum impact energy should be 27
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ImpactEnergyLimit',
            limit_type=LimitType.MINIMUM,
            minimum=31
        )
        blank_steel_plate.impact_energy_list = [
            ImpactEnergy(
                table_index=None,
                x_coordinate=None,
                y_coordinate=None,
                value=30,
                index=None,
                valid_flag=True,
                message=None,
                test_number='1'
            ),
            ImpactEnergy(
                table_index=None,
                x_coordinate=None,
                y_coordinate=None,
                value=31,
                index=None,
                valid_flag=True,
                message=None,
                test_number='2'
            ),
            ImpactEnergy(
                table_index=None,
                x_coordinate=None,
                y_coordinate=None,
                value=32,
                index=None,
                valid_flag=True,
                message=None,
                test_number='3'
            ),
            ImpactEnergy(
                table_index=None,
                x_coordinate=None,
                y_coordinate=None,
                value=33,
                index=None,
                valid_flag=True,
                message=None,
                test_number='Avg'
            )
        ]
        assert not limit.verify(blank_steel_plate)  # one of the energies must violates the limit
        assert blank_steel_plate.impact_energy_list[0].test_number == '1'
        assert not blank_steel_plate.impact_energy_list[0].valid_flag
        assert '[FAIL]' in blank_steel_plate.impact_energy_list[0].message
        assert blank_steel_plate.impact_energy_list[1].test_number == '2'
        assert blank_steel_plate.impact_energy_list[1].valid_flag
        assert '[PASS]' in blank_steel_plate.impact_energy_list[1].message
        assert blank_steel_plate.impact_energy_list[2].test_number == '3'
        assert blank_steel_plate.impact_energy_list[2].valid_flag
        assert '[PASS]' in blank_steel_plate.impact_energy_list[2].message
        assert blank_steel_plate.impact_energy_list[3].test_number == 'Avg'
        assert blank_steel_plate.impact_energy_list[3].valid_flag
        assert '[PASS]' in blank_steel_plate.impact_energy_list[3].message

    # Fine Grain Element
    def test_fine_grain_elements(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        # 5 kinds of situations for steel making types: BOC, CC; EAF, CC; value is None; invalid value; None
        # value is None
        blank_steel_plate.steel_making_type.value = None
        with pytest.raises(ValueError) as e:
            rule_maker.get_rules(blank_steel_plate)
        assert str(
            e.value) == f"The steel making type value {blank_steel_plate.steel_making_type.value} is not expected."
        # BOC, CC
        blank_steel_plate.steel_making_type.value = 'BOC, CC'
        # when thickness <= 15, Al+Nb / Al+V apply; when thickness <= 17, Al applies.
        blank_steel_plate.thickness.value = 17
        limit_list = rule_maker.get_rules(blank_steel_plate)
        hit_limits = [limit for limit in limit_list if isinstance(limit, FineGrainElementLimitCombination)]
        assert len(hit_limits) == 1
        fine_grain_element_limit_combination = hit_limits[0]
        assert len(fine_grain_element_limit_combination.fine_grain_element_limits) == 1
        fine_grain_element_limit = fine_grain_element_limit_combination.fine_grain_element_limits[0]
        assert isinstance(fine_grain_element_limit, FineGrainElementLimit)
        assert len(fine_grain_element_limit.concurrent_limits) == 1
        chemical_composition_limit = fine_grain_element_limit.concurrent_limits[0]
        assert chemical_composition_limit.chemical_element == 'Al'
        assert chemical_composition_limit.limit_type == LimitType.MINIMUM
        assert chemical_composition_limit.minimum == 0.020

        blank_steel_plate.thickness.value = 15
        limit_list = rule_maker.get_rules(blank_steel_plate)
        hit_limits = [limit for limit in limit_list if isinstance(limit, FineGrainElementLimitCombination)]
        assert len(hit_limits) == 1
        fine_grain_element_limit_combination = hit_limits[0]
        assert len(fine_grain_element_limit_combination.fine_grain_element_limits) == 3
        # Al
        assert any(
            [
                isinstance(limit, FineGrainElementLimit)
                and len(limit.concurrent_limits) == 1
                and limit.concurrent_limits[0].chemical_element == 'Al'
                and limit.concurrent_limits[0].limit_type == LimitType.MINIMUM
                and limit.concurrent_limits[0].minimum == 0.020
                for limit in fine_grain_element_limit_combination.fine_grain_element_limits
            ]
        )
        # Al+Nb
        assert any(
            [
                isinstance(limit, FineGrainElementLimit)
                and len(limit.concurrent_limits) == 3
                and any(
                    [
                        concurrent_limit.chemical_element == 'Al'
                        and concurrent_limit.limit_type == LimitType.MINIMUM
                        and concurrent_limit.minimum == 0.015
                        for concurrent_limit in limit.concurrent_limits
                    ]
                )
                and any(
                    [
                        concurrent_limit.chemical_element == 'Nb'
                        and concurrent_limit.limit_type == LimitType.MINIMUM
                        and concurrent_limit.minimum == 0.010
                        for concurrent_limit in limit.concurrent_limits
                    ]
                )
                and any(
                    [
                        concurrent_limit.chemical_element == 'Nb + V + Ti'
                        and concurrent_limit.limit_type == LimitType.MAXIMUM
                        and concurrent_limit.maximum == 0.12
                        for concurrent_limit in limit.concurrent_limits
                    ]
                )
                for limit in fine_grain_element_limit_combination.fine_grain_element_limits
            ]
        )
        # Al+V
        assert any(
            [
                isinstance(limit, FineGrainElementLimit)
                and len(limit.concurrent_limits) == 3
                and any(
                    [
                        concurrent_limit.chemical_element == 'Al'
                        and concurrent_limit.limit_type == LimitType.MINIMUM
                        and concurrent_limit.minimum == 0.015
                        for concurrent_limit in limit.concurrent_limits
                    ]
                )
                and any(
                    [
                        concurrent_limit.chemical_element == 'V'
                        and concurrent_limit.limit_type == LimitType.MINIMUM
                        and concurrent_limit.minimum == 0.030
                        for concurrent_limit in limit.concurrent_limits
                    ]
                )
                and any(
                    [
                        concurrent_limit.chemical_element == 'Nb + V + Ti'
                        and concurrent_limit.limit_type == LimitType.MAXIMUM
                        and concurrent_limit.maximum == 0.12
                        for concurrent_limit in limit.concurrent_limits
                    ]
                )
                for limit in fine_grain_element_limit_combination.fine_grain_element_limits
            ]
        )
        # EAF, CC
        blank_steel_plate.steel_making_type.value = 'EAF, CC'
        limit_list = rule_maker.get_rules(blank_steel_plate)
        hit_limits = [limit for limit in limit_list if isinstance(limit, FineGrainElementLimitCombination)]
        assert len(hit_limits) == 1
        fine_grain_element_limit_combination = hit_limits[0]
        assert len(fine_grain_element_limit_combination.fine_grain_element_limits) == 2
        # Al+Nb
        assert any(
            [
                isinstance(limit, FineGrainElementLimit)
                and len(limit.concurrent_limits) == 3
                and any(
                    [
                        concurrent_limit.chemical_element == 'Al'
                        and concurrent_limit.limit_type == LimitType.MINIMUM
                        and concurrent_limit.minimum == 0.015
                        for concurrent_limit in limit.concurrent_limits
                    ]
                )
                and any(
                    [
                        concurrent_limit.chemical_element == 'Nb'
                        and concurrent_limit.limit_type == LimitType.MINIMUM
                        and concurrent_limit.minimum == 0.010
                        for concurrent_limit in limit.concurrent_limits
                    ]
                )
                and any(
                    [
                        concurrent_limit.chemical_element == 'Nb + V + Ti'
                        and concurrent_limit.limit_type == LimitType.MAXIMUM
                        and concurrent_limit.maximum == 0.12
                        for concurrent_limit in limit.concurrent_limits
                    ]
                )
                for limit in fine_grain_element_limit_combination.fine_grain_element_limits
            ]
        )
        # Al+V
        assert any(
            [
                isinstance(limit, FineGrainElementLimit)
                and len(limit.concurrent_limits) == 3
                and any(
                    [
                        concurrent_limit.chemical_element == 'Al'
                        and concurrent_limit.limit_type == LimitType.MINIMUM
                        and concurrent_limit.minimum == 0.015
                        for concurrent_limit in limit.concurrent_limits
                    ]
                )
                and any(
                    [
                        concurrent_limit.chemical_element == 'V'
                        and concurrent_limit.limit_type == LimitType.MINIMUM
                        and concurrent_limit.minimum == 0.030
                        for concurrent_limit in limit.concurrent_limits
                    ]
                )
                and any(
                    [
                        concurrent_limit.chemical_element == 'Nb + V + Ti'
                        and concurrent_limit.limit_type == LimitType.MAXIMUM
                        and concurrent_limit.maximum == 0.12
                        for concurrent_limit in limit.concurrent_limits
                    ]
                )
                for limit in fine_grain_element_limit_combination.fine_grain_element_limits
            ]
        )
        # invalid value
        blank_steel_plate.steel_making_type.value = 'N/A'
        with pytest.raises(ValueError) as excinfo:
            rule_maker.get_rules(blank_steel_plate)
        assert str(excinfo.value) == (
            f"The steel making type value {blank_steel_plate.steel_making_type.value} is not expected."
        )
        # None
        blank_steel_plate.steel_making_type = None
        with pytest.raises(ValueError) as e:
            rule_maker.get_rules(blank_steel_plate)
        assert str(e.value) == "The steel making type is not instantiated in the steel plate."


class TestVLD36(BaseTester):

    def setup_class(self):
        self.specification = 'VL D36'

    # Special Rules
    # Specification
    def test_specification(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='SpecificationLimit',
            limit_type=LimitType.SCOPE,
            scope=['VL A', 'VL B', 'VL D', 'VL A32', 'VL A36', 'VL D32', 'VL D36']
        )
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.specification.valid_flag
        assert '[PASS]' in blank_steel_plate.specification.message
        blank_steel_plate.specification.value = 'VL E'
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.specification.valid_flag
        assert '[FAIL]' in blank_steel_plate.specification.message

    # Delivery Condition
    def test_delivery_condition(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='DeliveryConditionLimit',
            limit_type=LimitType.SCOPE,
            scope=['AR']
        )
        blank_steel_plate.delivery_condition.value = 'AR'
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.delivery_condition.valid_flag
        assert '[PASS]' in blank_steel_plate.delivery_condition.message
        blank_steel_plate.delivery_condition.value = 'TM'
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.delivery_condition.valid_flag
        assert '[FAIL]' in blank_steel_plate.delivery_condition.message

    # Thickness
    def test_thickness(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        # steel making type is None
        blank_steel_plate.steel_making_type.value = None
        with pytest.raises(ValueError) as e:
            rule_maker.get_rules(blank_steel_plate)
        assert str(
            e.value) == f"The steel making type value {blank_steel_plate.steel_making_type.value} is not expected."
        # steel making type is BOC, CC
        blank_steel_plate.steel_making_type.value = 'BOC, CC'
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ThicknessLimit',
            limit_type=LimitType.RANGE,
            maximum=17,
            minimum=0
        )
        blank_steel_plate.thickness.value = 16
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.thickness.valid_flag
        assert '[PASS]' in blank_steel_plate.thickness.message
        blank_steel_plate.thickness.value = 17
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.thickness.valid_flag
        assert '[PASS]' in blank_steel_plate.thickness.message
        blank_steel_plate.thickness.value = 18
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.thickness.valid_flag
        assert '[FAIL]' in blank_steel_plate.thickness.message
        # steel making type is EAF, CC
        blank_steel_plate.steel_making_type.value = 'EAF, CC'
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ThicknessLimit',
            limit_type=LimitType.RANGE,
            maximum=19,
            minimum=0
        )
        blank_steel_plate.thickness.value = 18
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.thickness.valid_flag
        assert '[PASS]' in blank_steel_plate.thickness.message
        blank_steel_plate.thickness.value = 19
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.thickness.valid_flag
        assert '[PASS]' in blank_steel_plate.thickness.message
        blank_steel_plate.thickness.value = 20
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.thickness.valid_flag
        assert '[FAIL]' in blank_steel_plate.thickness.message

    # Chemical Composition
    # C
    def test_element_c(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ChemicalCompositionLimit',
            chemical_element='C',
            limit_type=LimitType.MAXIMUM,
            maximum=0.18,
            minimum=None
        )
        blank_steel_plate.chemical_compositions['C'].set_value(0.17)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['C'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['C'].message
        blank_steel_plate.chemical_compositions['C'].set_value(0.18)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['C'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['C'].message
        blank_steel_plate.chemical_compositions['C'].set_value(0.19)
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.chemical_compositions['C'].valid_flag
        assert '[FAIL]' in blank_steel_plate.chemical_compositions['C'].message

    # Si
    def test_element_si(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ChemicalCompositionLimit',
            chemical_element='Si',
            limit_type=LimitType.MAXIMUM,
            maximum=0.50,
            minimum=None
        )
        blank_steel_plate.chemical_compositions['Si'].set_value(0.49)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Si'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Si'].message
        blank_steel_plate.chemical_compositions['Si'].set_value(0.50)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Si'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Si'].message
        blank_steel_plate.chemical_compositions['Si'].set_value(0.51)
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.chemical_compositions['Si'].valid_flag
        assert '[FAIL]' in blank_steel_plate.chemical_compositions['Si'].message

    # Mn
    def test_element_mn(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification

        blank_steel_plate.thickness.value = 12.4
        limit_list = rule_maker.get_rules(blank_steel_plate)
        self.get_limit(
            limit_list=limit_list,
            limit_class='ChemicalCompositionLimit',
            chemical_element='Mn',
            limit_type=LimitType.RANGE,
            maximum=1.60,
            minimum=0.70
        )

        blank_steel_plate.thickness.value = 12.5
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ChemicalCompositionLimit',
            chemical_element='Mn',
            limit_type=LimitType.RANGE,
            maximum=1.60,
            minimum=0.70
        )
        blank_steel_plate.chemical_compositions['Mn'].set_value(0.69)
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.chemical_compositions['Mn'].valid_flag
        assert '[FAIL]' in blank_steel_plate.chemical_compositions['Mn'].message
        blank_steel_plate.chemical_compositions['Mn'].set_value(0.70)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Mn'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Mn'].message
        blank_steel_plate.chemical_compositions['Mn'].set_value(0.71)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Mn'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Mn'].message
        blank_steel_plate.chemical_compositions['Mn'].set_value(1.59)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Mn'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Mn'].message
        blank_steel_plate.chemical_compositions['Mn'].set_value(1.60)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Mn'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Mn'].message
        blank_steel_plate.chemical_compositions['Mn'].set_value(1.61)
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.chemical_compositions['Mn'].valid_flag
        assert '[FAIL]' in blank_steel_plate.chemical_compositions['Mn'].message

        blank_steel_plate.thickness.value = 12.6
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ChemicalCompositionLimit',
            chemical_element='Mn',
            limit_type=LimitType.RANGE,
            maximum=1.60,
            minimum=0.90
        )
        blank_steel_plate.chemical_compositions['Mn'].set_value(0.89)
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.chemical_compositions['Mn'].valid_flag
        assert '[FAIL]' in blank_steel_plate.chemical_compositions['Mn'].message
        blank_steel_plate.chemical_compositions['Mn'].set_value(0.90)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Mn'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Mn'].message
        blank_steel_plate.chemical_compositions['Mn'].set_value(0.91)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Mn'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Mn'].message
        blank_steel_plate.chemical_compositions['Mn'].set_value(1.59)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Mn'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Mn'].message
        blank_steel_plate.chemical_compositions['Mn'].set_value(1.60)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Mn'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Mn'].message
        blank_steel_plate.chemical_compositions['Mn'].set_value(1.61)
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.chemical_compositions['Mn'].valid_flag
        assert '[FAIL]' in blank_steel_plate.chemical_compositions['Mn'].message

    # P
    def test_element_p(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ChemicalCompositionLimit',
            chemical_element='P',
            limit_type=LimitType.MAXIMUM,
            maximum=0.035,
            minimum=None
        )
        blank_steel_plate.chemical_compositions['P'].set_value(0.034)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['P'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['P'].message
        blank_steel_plate.chemical_compositions['P'].set_value(0.035)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['P'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['P'].message
        blank_steel_plate.chemical_compositions['P'].set_value(0.036)
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.chemical_compositions['P'].valid_flag
        assert '[FAIL]' in blank_steel_plate.chemical_compositions['P'].message

    # S
    def test_element_s(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ChemicalCompositionLimit',
            chemical_element='S',
            limit_type=LimitType.MAXIMUM,
            maximum=0.035,
            minimum=None
        )
        blank_steel_plate.chemical_compositions['S'].set_value(0.034)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['S'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['S'].message
        blank_steel_plate.chemical_compositions['S'].set_value(0.035)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['S'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['S'].message
        blank_steel_plate.chemical_compositions['S'].set_value(0.036)
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.chemical_compositions['S'].valid_flag
        assert '[FAIL]' in blank_steel_plate.chemical_compositions['S'].message

    # Cu
    def test_element_cu(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ChemicalCompositionLimit',
            chemical_element='Cu',
            limit_type=LimitType.MAXIMUM,
            maximum=0.35,
            minimum=None
        )
        blank_steel_plate.chemical_compositions['Cu'].set_value(0.34)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Cu'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Cu'].message
        blank_steel_plate.chemical_compositions['Cu'].set_value(0.35)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Cu'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Cu'].message
        blank_steel_plate.chemical_compositions['Cu'].set_value(0.36)
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.chemical_compositions['Cu'].valid_flag
        assert '[FAIL]' in blank_steel_plate.chemical_compositions['Cu'].message

    # Cr
    def test_element_cr(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ChemicalCompositionLimit',
            chemical_element='Cr',
            limit_type=LimitType.MAXIMUM,
            maximum=0.20,
            minimum=None
        )
        blank_steel_plate.chemical_compositions['Cr'].set_value(0.19)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Cr'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Cr'].message
        blank_steel_plate.chemical_compositions['Cr'].set_value(0.20)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Cr'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Cr'].message
        blank_steel_plate.chemical_compositions['Cr'].set_value(0.21)
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.chemical_compositions['Cr'].valid_flag
        assert '[FAIL]' in blank_steel_plate.chemical_compositions['Cr'].message

    # Ni
    def test_element_ni(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ChemicalCompositionLimit',
            chemical_element='Ni',
            limit_type=LimitType.MAXIMUM,
            maximum=0.40,
            minimum=None
        )
        blank_steel_plate.chemical_compositions['Ni'].set_value(0.39)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Ni'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Ni'].message
        blank_steel_plate.chemical_compositions['Ni'].set_value(0.40)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Ni'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Ni'].message
        blank_steel_plate.chemical_compositions['Ni'].set_value(0.41)
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.chemical_compositions['Ni'].valid_flag
        assert '[FAIL]' in blank_steel_plate.chemical_compositions['Ni'].message

    # Mo
    def test_element_mo(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ChemicalCompositionLimit',
            chemical_element='Mo',
            limit_type=LimitType.MAXIMUM,
            maximum=0.08,
            minimum=None
        )
        blank_steel_plate.chemical_compositions['Mo'].set_value(0.07)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Mo'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Mo'].message
        blank_steel_plate.chemical_compositions['Mo'].set_value(0.08)
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Mo'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Mo'].message
        blank_steel_plate.chemical_compositions['Mo'].set_value(0.09)
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.chemical_compositions['Mo'].valid_flag
        assert '[FAIL]' in blank_steel_plate.chemical_compositions['Mo'].message

    # Ceq
    # Because all plates delivered by LongTeng is AR, No Ceq check should be performed
    def test_element_ceq(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        blank_steel_plate.delivery_condition.value = 'AR'
        limit_list = rule_maker.get_rules(blank_steel_plate)
        assert not any(
            [isinstance(limit, ChemicalCompositionLimit) and limit.chemical_element == 'Ceq' for limit in limit_list]
        )

    # Mechanical Properties
    # Yield Strength
    def test_yield_strength(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='YieldStrengthLimit',
            limit_type=LimitType.MINIMUM,
            minimum=355
        )
        blank_steel_plate.yield_strength.value = 354
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.yield_strength.valid_flag
        assert '[FAIL]' in blank_steel_plate.yield_strength.message
        blank_steel_plate.yield_strength.value = 355
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.yield_strength.valid_flag
        assert '[PASS]' in blank_steel_plate.yield_strength.message
        blank_steel_plate.yield_strength.value = 356
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.yield_strength.valid_flag
        assert '[PASS]' in blank_steel_plate.yield_strength.message

    # Tensile Strength
    def test_tensile_strength(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='TensileStrengthLimit',
            limit_type=LimitType.RANGE,
            maximum=630,
            minimum=490
        )
        blank_steel_plate.tensile_strength.value = 489
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.tensile_strength.valid_flag
        assert '[FAIL]' in blank_steel_plate.tensile_strength.message
        blank_steel_plate.tensile_strength.value = 490
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.tensile_strength.valid_flag
        assert '[PASS]' in blank_steel_plate.tensile_strength.message
        blank_steel_plate.tensile_strength.value = 491
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.tensile_strength.valid_flag
        assert '[PASS]' in blank_steel_plate.tensile_strength.message
        blank_steel_plate.tensile_strength.value = 629
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.tensile_strength.valid_flag
        assert '[PASS]' in blank_steel_plate.tensile_strength.message
        blank_steel_plate.tensile_strength.value = 630
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.tensile_strength.valid_flag
        assert '[PASS]' in blank_steel_plate.tensile_strength.message
        blank_steel_plate.tensile_strength.value = 631
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.tensile_strength.valid_flag
        assert '[FAIL]' in blank_steel_plate.tensile_strength.message

    # Elongation
    def test_elongation(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        limit_list = rule_maker.get_rules(blank_steel_plate)
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ElongationLimit',
            limit_type=LimitType.MINIMUM,
            minimum=21
        )
        blank_steel_plate.elongation.value = 20
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.elongation.valid_flag
        assert '[FAIL]' in blank_steel_plate.elongation.message
        blank_steel_plate.elongation.value = 21
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.elongation.valid_flag
        assert '[PASS]' in blank_steel_plate.elongation.message
        blank_steel_plate.elongation.value = 22
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.elongation.valid_flag
        assert '[PASS]' in blank_steel_plate.elongation.message

    # Temperature
    def test_temperature(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        # For VL D, in the LongTeng agreement document, the possible maximum thickness is 19
        limit_list = rule_maker.get_rules(blank_steel_plate)
        # For VL D, maximum thickness 19, the maximum test temperature should be -20
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='TemperatureLimit',
            limit_type=LimitType.MAXIMUM,
            maximum=-20
        )
        blank_steel_plate.temperature.value = -21
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.temperature.valid_flag
        assert '[PASS]' in blank_steel_plate.temperature.message
        blank_steel_plate.temperature.value = -20
        assert limit.verify(blank_steel_plate)
        assert blank_steel_plate.temperature.valid_flag
        assert '[PASS]' in blank_steel_plate.temperature.message
        blank_steel_plate.temperature.value = -19
        assert not limit.verify(blank_steel_plate)
        assert not blank_steel_plate.temperature.valid_flag
        assert '[FAIL]' in blank_steel_plate.temperature.message

    # Impact Energy
    def test_impact_energy(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        # For VL D, in the LongTeng agreement document, the possible maximum thickness is 19
        blank_steel_plate.thickness.value = 20
        limit_list = rule_maker.get_rules(blank_steel_plate)
        # For VL D, maximum thickness 19, direction LONGITUDINAL, minimum impact energy should be 27
        limit = self.get_limit(
            limit_list=limit_list,
            limit_class='ImpactEnergyLimit',
            limit_type=LimitType.MINIMUM,
            minimum=34
        )
        blank_steel_plate.impact_energy_list = [
            ImpactEnergy(
                table_index=None,
                x_coordinate=None,
                y_coordinate=None,
                value=33,
                index=None,
                valid_flag=True,
                message=None,
                test_number='1'
            ),
            ImpactEnergy(
                table_index=None,
                x_coordinate=None,
                y_coordinate=None,
                value=34,
                index=None,
                valid_flag=True,
                message=None,
                test_number='2'
            ),
            ImpactEnergy(
                table_index=None,
                x_coordinate=None,
                y_coordinate=None,
                value=35,
                index=None,
                valid_flag=True,
                message=None,
                test_number='3'
            ),
            ImpactEnergy(
                table_index=None,
                x_coordinate=None,
                y_coordinate=None,
                value=36,
                index=None,
                valid_flag=True,
                message=None,
                test_number='Avg'
            )
        ]
        assert not limit.verify(blank_steel_plate)  # one of the energies must violates the limit
        assert blank_steel_plate.impact_energy_list[0].test_number == '1'
        assert not blank_steel_plate.impact_energy_list[0].valid_flag
        assert '[FAIL]' in blank_steel_plate.impact_energy_list[0].message
        assert blank_steel_plate.impact_energy_list[1].test_number == '2'
        assert blank_steel_plate.impact_energy_list[1].valid_flag
        assert '[PASS]' in blank_steel_plate.impact_energy_list[1].message
        assert blank_steel_plate.impact_energy_list[2].test_number == '3'
        assert blank_steel_plate.impact_energy_list[2].valid_flag
        assert '[PASS]' in blank_steel_plate.impact_energy_list[2].message
        assert blank_steel_plate.impact_energy_list[3].test_number == 'Avg'
        assert blank_steel_plate.impact_energy_list[3].valid_flag
        assert '[PASS]' in blank_steel_plate.impact_energy_list[3].message

    # Fine Grain Element
    def test_fine_grain_elements(self, rule_maker: LongTengRuleMaker, blank_steel_plate: SteelPlate):
        blank_steel_plate.specification.value = self.specification
        # 5 kinds of situations for steel making types: BOC, CC; EAF, CC; value is None; invalid value; None
        # value is None
        blank_steel_plate.steel_making_type.value = None
        with pytest.raises(ValueError) as e:
            rule_maker.get_rules(blank_steel_plate)
        assert str(
            e.value) == f"The steel making type value {blank_steel_plate.steel_making_type.value} is not expected."
        # BOC, CC
        blank_steel_plate.steel_making_type.value = 'BOC, CC'
        # when thickness <= 15, Al+Nb / Al+V apply; when thickness <= 17, Al applies.
        blank_steel_plate.thickness.value = 17
        limit_list = rule_maker.get_rules(blank_steel_plate)
        hit_limits = [limit for limit in limit_list if isinstance(limit, FineGrainElementLimitCombination)]
        assert len(hit_limits) == 1
        fine_grain_element_limit_combination = hit_limits[0]
        assert len(fine_grain_element_limit_combination.fine_grain_element_limits) == 1
        fine_grain_element_limit = fine_grain_element_limit_combination.fine_grain_element_limits[0]
        assert isinstance(fine_grain_element_limit, FineGrainElementLimit)
        assert len(fine_grain_element_limit.concurrent_limits) == 1
        chemical_composition_limit = fine_grain_element_limit.concurrent_limits[0]
        assert chemical_composition_limit.chemical_element == 'Al'
        assert chemical_composition_limit.limit_type == LimitType.MINIMUM
        assert chemical_composition_limit.minimum == 0.020

        blank_steel_plate.thickness.value = 15
        limit_list = rule_maker.get_rules(blank_steel_plate)
        hit_limits = [limit for limit in limit_list if isinstance(limit, FineGrainElementLimitCombination)]
        assert len(hit_limits) == 1
        fine_grain_element_limit_combination = hit_limits[0]
        assert len(fine_grain_element_limit_combination.fine_grain_element_limits) == 3
        # Al
        assert any(
            [
                isinstance(limit, FineGrainElementLimit)
                and len(limit.concurrent_limits) == 1
                and limit.concurrent_limits[0].chemical_element == 'Al'
                and limit.concurrent_limits[0].limit_type == LimitType.MINIMUM
                and limit.concurrent_limits[0].minimum == 0.020
                for limit in fine_grain_element_limit_combination.fine_grain_element_limits
            ]
        )
        # Al+Nb
        assert any(
            [
                isinstance(limit, FineGrainElementLimit)
                and len(limit.concurrent_limits) == 3
                and any(
                    [
                        concurrent_limit.chemical_element == 'Al'
                        and concurrent_limit.limit_type == LimitType.MINIMUM
                        and concurrent_limit.minimum == 0.015
                        for concurrent_limit in limit.concurrent_limits
                    ]
                )
                and any(
                    [
                        concurrent_limit.chemical_element == 'Nb'
                        and concurrent_limit.limit_type == LimitType.MINIMUM
                        and concurrent_limit.minimum == 0.010
                        for concurrent_limit in limit.concurrent_limits
                    ]
                )
                and any(
                    [
                        concurrent_limit.chemical_element == 'Nb + V + Ti'
                        and concurrent_limit.limit_type == LimitType.MAXIMUM
                        and concurrent_limit.maximum == 0.12
                        for concurrent_limit in limit.concurrent_limits
                    ]
                )
                for limit in fine_grain_element_limit_combination.fine_grain_element_limits
            ]
        )
        # Al+V
        assert any(
            [
                isinstance(limit, FineGrainElementLimit)
                and len(limit.concurrent_limits) == 3
                and any(
                    [
                        concurrent_limit.chemical_element == 'Al'
                        and concurrent_limit.limit_type == LimitType.MINIMUM
                        and concurrent_limit.minimum == 0.015
                        for concurrent_limit in limit.concurrent_limits
                    ]
                )
                and any(
                    [
                        concurrent_limit.chemical_element == 'V'
                        and concurrent_limit.limit_type == LimitType.MINIMUM
                        and concurrent_limit.minimum == 0.030
                        for concurrent_limit in limit.concurrent_limits
                    ]
                )
                and any(
                    [
                        concurrent_limit.chemical_element == 'Nb + V + Ti'
                        and concurrent_limit.limit_type == LimitType.MAXIMUM
                        and concurrent_limit.maximum == 0.12
                        for concurrent_limit in limit.concurrent_limits
                    ]
                )
                for limit in fine_grain_element_limit_combination.fine_grain_element_limits
            ]
        )
        # EAF, CC
        blank_steel_plate.steel_making_type.value = 'EAF, CC'
        limit_list = rule_maker.get_rules(blank_steel_plate)
        hit_limits = [limit for limit in limit_list if isinstance(limit, FineGrainElementLimitCombination)]
        assert len(hit_limits) == 1
        fine_grain_element_limit_combination = hit_limits[0]
        assert len(fine_grain_element_limit_combination.fine_grain_element_limits) == 2
        # Al+Nb
        assert any(
            [
                isinstance(limit, FineGrainElementLimit)
                and len(limit.concurrent_limits) == 3
                and any(
                    [
                        concurrent_limit.chemical_element == 'Al'
                        and concurrent_limit.limit_type == LimitType.MINIMUM
                        and concurrent_limit.minimum == 0.015
                        for concurrent_limit in limit.concurrent_limits
                    ]
                )
                and any(
                    [
                        concurrent_limit.chemical_element == 'Nb'
                        and concurrent_limit.limit_type == LimitType.MINIMUM
                        and concurrent_limit.minimum == 0.010
                        for concurrent_limit in limit.concurrent_limits
                    ]
                )
                and any(
                    [
                        concurrent_limit.chemical_element == 'Nb + V + Ti'
                        and concurrent_limit.limit_type == LimitType.MAXIMUM
                        and concurrent_limit.maximum == 0.12
                        for concurrent_limit in limit.concurrent_limits
                    ]
                )
                for limit in fine_grain_element_limit_combination.fine_grain_element_limits
            ]
        )
        # Al+V
        assert any(
            [
                isinstance(limit, FineGrainElementLimit)
                and len(limit.concurrent_limits) == 3
                and any(
                    [
                        concurrent_limit.chemical_element == 'Al'
                        and concurrent_limit.limit_type == LimitType.MINIMUM
                        and concurrent_limit.minimum == 0.015
                        for concurrent_limit in limit.concurrent_limits
                    ]
                )
                and any(
                    [
                        concurrent_limit.chemical_element == 'V'
                        and concurrent_limit.limit_type == LimitType.MINIMUM
                        and concurrent_limit.minimum == 0.030
                        for concurrent_limit in limit.concurrent_limits
                    ]
                )
                and any(
                    [
                        concurrent_limit.chemical_element == 'Nb + V + Ti'
                        and concurrent_limit.limit_type == LimitType.MAXIMUM
                        and concurrent_limit.maximum == 0.12
                        for concurrent_limit in limit.concurrent_limits
                    ]
                )
                for limit in fine_grain_element_limit_combination.fine_grain_element_limits
            ]
        )
        # invalid value
        blank_steel_plate.steel_making_type.value = 'N/A'
        with pytest.raises(ValueError) as excinfo:
            rule_maker.get_rules(blank_steel_plate)
        assert str(excinfo.value) == (
            f"The steel making type value {blank_steel_plate.steel_making_type.value} is not expected."
        )
        # None
        blank_steel_plate.steel_making_type = None
        with pytest.raises(ValueError) as e:
            rule_maker.get_rules(blank_steel_plate)
        assert str(e.value) == "The steel making type is not instantiated in the steel plate."


class TestFineGrainElementLimit(BaseTester):

    # Test single Al
    def test_single_al(self, blank_steel_plate: SteelPlate):
        al_limit = FineGrainElementLimit(
            concurrent_limits=[
                ChemicalCompositionLimit(
                    chemical_element='Al',
                    limit_type=LimitType.MINIMUM,
                    minimum=0.020
                )
            ]
        )
        blank_steel_plate.chemical_compositions['Al'].set_value(0.019)
        blank_steel_plate.chemical_compositions['Al'].valid_flag = True
        blank_steel_plate.chemical_compositions['Al'].message = None
        assert not al_limit.verify(blank_steel_plate)
        # not updated in this level, will be updated in LimitCombination level.
        assert blank_steel_plate.chemical_compositions['Al'].valid_flag
        # not updated in this level, will be updated in LimitCombination level.
        assert blank_steel_plate.chemical_compositions['Al'].message is None
        blank_steel_plate.chemical_compositions['Al'].set_value(0.020)
        blank_steel_plate.chemical_compositions['Al'].valid_flag = True
        blank_steel_plate.chemical_compositions['Al'].message = None
        assert al_limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Al'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Al'].message
        blank_steel_plate.chemical_compositions['Al'].set_value(0.021)
        blank_steel_plate.chemical_compositions['Al'].valid_flag = True
        blank_steel_plate.chemical_compositions['Al'].message = None
        assert al_limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Al'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Al'].message

    # Test single Nb
    def test_single_nb(self, blank_steel_plate: SteelPlate):
        al_limit = FineGrainElementLimit(
            concurrent_limits=[
                ChemicalCompositionLimit(
                    chemical_element='Nb',
                    limit_type=LimitType.RANGE,
                    maximum=0.050,
                    minimum=0.020
                )
            ]
        )
        blank_steel_plate.chemical_compositions['Nb'].set_value(0.019)
        blank_steel_plate.chemical_compositions['Nb'].valid_flag = True
        blank_steel_plate.chemical_compositions['Nb'].message = None
        assert not al_limit.verify(blank_steel_plate)
        # not updated in this level, will be updated in LimitCombination level.
        assert blank_steel_plate.chemical_compositions['Nb'].valid_flag
        # not updated in this level, will be updated in LimitCombination level.
        assert blank_steel_plate.chemical_compositions['Nb'].message is None
        blank_steel_plate.chemical_compositions['Nb'].set_value(0.020)
        blank_steel_plate.chemical_compositions['Nb'].valid_flag = True
        blank_steel_plate.chemical_compositions['Nb'].message = None
        assert al_limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Nb'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Nb'].message
        blank_steel_plate.chemical_compositions['Nb'].set_value(0.021)
        blank_steel_plate.chemical_compositions['Nb'].valid_flag = True
        blank_steel_plate.chemical_compositions['Nb'].message = None
        assert al_limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Nb'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Nb'].message
        blank_steel_plate.chemical_compositions['Nb'].set_value(0.049)
        blank_steel_plate.chemical_compositions['Nb'].valid_flag = True
        blank_steel_plate.chemical_compositions['Nb'].message = None
        assert al_limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Nb'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Nb'].message
        blank_steel_plate.chemical_compositions['Nb'].set_value(0.050)
        blank_steel_plate.chemical_compositions['Nb'].valid_flag = True
        blank_steel_plate.chemical_compositions['Nb'].message = None
        assert al_limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Nb'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Nb'].message
        blank_steel_plate.chemical_compositions['Nb'].set_value(0.051)
        blank_steel_plate.chemical_compositions['Nb'].valid_flag = True
        blank_steel_plate.chemical_compositions['Nb'].message = None
        assert not al_limit.verify(blank_steel_plate)
        # not updated in this level, will be updated in LimitCombination level.
        assert blank_steel_plate.chemical_compositions['Nb'].valid_flag
        # not updated in this level, will be updated in LimitCombination level.
        assert blank_steel_plate.chemical_compositions['Nb'].message is None

    # Test Al+Nb
    def test_al_plus_nb(self, blank_steel_plate: SteelPlate):
        # Al >= 0.015; Nb >= 0.010; Nb + V + Ti <= 0.12
        al_plus_nb_limit = FineGrainElementLimit(
            concurrent_limits=[
                ChemicalCompositionLimit(
                    chemical_element='Al',
                    limit_type=LimitType.MINIMUM,
                    minimum=0.015
                ),
                ChemicalCompositionLimit(
                    chemical_element='Nb',
                    limit_type=LimitType.MINIMUM,
                    minimum=0.010
                ),
                ChemicalCompositionLimit(
                    chemical_element='Nb + V + Ti',
                    limit_type=LimitType.MAXIMUM,
                    maximum=0.12
                )
            ]
        )
        # firstly, initial the steel plate to a state meet all the limits
        self.reset_chemical_composition(blank_steel_plate, 'Al', 0.015)
        self.reset_chemical_composition(blank_steel_plate, 'Nb', 0.010)
        self.reset_chemical_composition(blank_steel_plate, 'V', 0.010)
        self.reset_chemical_composition(blank_steel_plate, 'Ti', 0.010)
        assert al_plus_nb_limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Al'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Al'].message
        assert blank_steel_plate.chemical_compositions['Nb'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Nb'].message
        assert blank_steel_plate.chemical_compositions['V'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['V'].message
        assert blank_steel_plate.chemical_compositions['Ti'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Ti'].message
        # test Al fail
        self.reset_chemical_composition(blank_steel_plate, 'Al', 0.014)
        self.reset_chemical_composition(blank_steel_plate, 'Nb', 0.010)
        self.reset_chemical_composition(blank_steel_plate, 'V', 0.010)
        self.reset_chemical_composition(blank_steel_plate, 'Ti', 0.010)
        assert not al_plus_nb_limit.verify(blank_steel_plate)
        # not updated in this level, will be updated in LimitCombination level.
        assert blank_steel_plate.chemical_compositions['Al'].valid_flag
        assert blank_steel_plate.chemical_compositions['Al'].message is None
        assert blank_steel_plate.chemical_compositions['Nb'].valid_flag
        assert blank_steel_plate.chemical_compositions['Nb'].message is None
        assert blank_steel_plate.chemical_compositions['V'].valid_flag
        assert blank_steel_plate.chemical_compositions['V'].message is None
        assert blank_steel_plate.chemical_compositions['Ti'].valid_flag
        assert blank_steel_plate.chemical_compositions['Ti'].message is None
        # test Nb fail
        self.reset_chemical_composition(blank_steel_plate, 'Al', 0.015)
        self.reset_chemical_composition(blank_steel_plate, 'Nb', 0.009)
        self.reset_chemical_composition(blank_steel_plate, 'V', 0.010)
        self.reset_chemical_composition(blank_steel_plate, 'Ti', 0.010)
        assert not al_plus_nb_limit.verify(blank_steel_plate)
        # not updated in this level, will be updated in LimitCombination level.
        assert blank_steel_plate.chemical_compositions['Al'].valid_flag
        assert blank_steel_plate.chemical_compositions['Al'].message is None
        assert blank_steel_plate.chemical_compositions['Nb'].valid_flag
        assert blank_steel_plate.chemical_compositions['Nb'].message is None
        assert blank_steel_plate.chemical_compositions['V'].valid_flag
        assert blank_steel_plate.chemical_compositions['V'].message is None
        assert blank_steel_plate.chemical_compositions['Ti'].valid_flag
        assert blank_steel_plate.chemical_compositions['Ti'].message is None
        # test Nb + V + Ti fail
        self.reset_chemical_composition(blank_steel_plate, 'Al', 0.015)
        self.reset_chemical_composition(blank_steel_plate, 'Nb', 0.010)
        self.reset_chemical_composition(blank_steel_plate, 'V', 0.060)
        self.reset_chemical_composition(blank_steel_plate, 'Ti', 0.060)
        assert not al_plus_nb_limit.verify(blank_steel_plate)
        # not updated in this level, will be updated in LimitCombination level.
        assert blank_steel_plate.chemical_compositions['Al'].valid_flag
        assert blank_steel_plate.chemical_compositions['Al'].message is None
        assert blank_steel_plate.chemical_compositions['Nb'].valid_flag
        assert blank_steel_plate.chemical_compositions['Nb'].message is None
        assert blank_steel_plate.chemical_compositions['V'].valid_flag
        assert blank_steel_plate.chemical_compositions['V'].message is None
        assert blank_steel_plate.chemical_compositions['Ti'].valid_flag
        assert blank_steel_plate.chemical_compositions['Ti'].message is None

    def test_al_plus_v(self, blank_steel_plate: SteelPlate):
        # Al >= 0.015; V >= 0.030; Nb + V + Ti <= 0.12
        al_plus_nb_limit = FineGrainElementLimit(
            concurrent_limits=[
                ChemicalCompositionLimit(
                    chemical_element='Al',
                    limit_type=LimitType.MINIMUM,
                    minimum=0.015
                ),
                ChemicalCompositionLimit(
                    chemical_element='V',
                    limit_type=LimitType.MINIMUM,
                    minimum=0.030
                ),
                ChemicalCompositionLimit(
                    chemical_element='Nb + V + Ti',
                    limit_type=LimitType.MAXIMUM,
                    maximum=0.12
                )
            ]
        )
        # firstly, initial the steel plate to a state meet all the limits
        self.reset_chemical_composition(blank_steel_plate, 'Al', 0.015)
        self.reset_chemical_composition(blank_steel_plate, 'Nb', 0.010)
        self.reset_chemical_composition(blank_steel_plate, 'V', 0.030)
        self.reset_chemical_composition(blank_steel_plate, 'Ti', 0.010)
        assert al_plus_nb_limit.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Al'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Al'].message
        assert blank_steel_plate.chemical_compositions['Nb'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Nb'].message
        assert blank_steel_plate.chemical_compositions['V'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['V'].message
        assert blank_steel_plate.chemical_compositions['Ti'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Ti'].message
        # test Al fail
        self.reset_chemical_composition(blank_steel_plate, 'Al', 0.014)
        self.reset_chemical_composition(blank_steel_plate, 'Nb', 0.010)
        self.reset_chemical_composition(blank_steel_plate, 'V', 0.030)
        self.reset_chemical_composition(blank_steel_plate, 'Ti', 0.010)
        assert not al_plus_nb_limit.verify(blank_steel_plate)
        # not updated in this level, will be updated in LimitCombination level.
        assert blank_steel_plate.chemical_compositions['Al'].valid_flag
        assert blank_steel_plate.chemical_compositions['Al'].message is None
        assert blank_steel_plate.chemical_compositions['Nb'].valid_flag
        assert blank_steel_plate.chemical_compositions['Nb'].message is None
        assert blank_steel_plate.chemical_compositions['V'].valid_flag
        assert blank_steel_plate.chemical_compositions['V'].message is None
        assert blank_steel_plate.chemical_compositions['Ti'].valid_flag
        assert blank_steel_plate.chemical_compositions['Ti'].message is None
        # test V fail
        self.reset_chemical_composition(blank_steel_plate, 'Al', 0.015)
        self.reset_chemical_composition(blank_steel_plate, 'Nb', 0.010)
        self.reset_chemical_composition(blank_steel_plate, 'V', 0.029)
        self.reset_chemical_composition(blank_steel_plate, 'Ti', 0.010)
        assert not al_plus_nb_limit.verify(blank_steel_plate)
        # not updated in this level, will be updated in LimitCombination level.
        assert blank_steel_plate.chemical_compositions['Al'].valid_flag
        assert blank_steel_plate.chemical_compositions['Al'].message is None
        assert blank_steel_plate.chemical_compositions['Nb'].valid_flag
        assert blank_steel_plate.chemical_compositions['Nb'].message is None
        assert blank_steel_plate.chemical_compositions['V'].valid_flag
        assert blank_steel_plate.chemical_compositions['V'].message is None
        assert blank_steel_plate.chemical_compositions['Ti'].valid_flag
        assert blank_steel_plate.chemical_compositions['Ti'].message is None
        # test Nb + V + Ti fail
        self.reset_chemical_composition(blank_steel_plate, 'Al', 0.015)
        self.reset_chemical_composition(blank_steel_plate, 'Nb', 0.010)
        self.reset_chemical_composition(blank_steel_plate, 'V', 0.060)
        self.reset_chemical_composition(blank_steel_plate, 'Ti', 0.060)
        assert not al_plus_nb_limit.verify(blank_steel_plate)
        # not updated in this level, will be updated in LimitCombination level.
        assert blank_steel_plate.chemical_compositions['Al'].valid_flag
        assert blank_steel_plate.chemical_compositions['Al'].message is None
        assert blank_steel_plate.chemical_compositions['Nb'].valid_flag
        assert blank_steel_plate.chemical_compositions['Nb'].message is None
        assert blank_steel_plate.chemical_compositions['V'].valid_flag
        assert blank_steel_plate.chemical_compositions['V'].message is None
        assert blank_steel_plate.chemical_compositions['Ti'].valid_flag
        assert blank_steel_plate.chemical_compositions['Ti'].message is None

    def test_combination_al(self, blank_steel_plate: SteelPlate):
        limit_combination = LongTengRuleMaker.compose_fine_grain_element_limit_combination(['Al'])
        # Al >= 0.020
        self.reset_chemical_composition(blank_steel_plate, 'Al', 0.019)
        assert not limit_combination.verify(blank_steel_plate)
        assert not blank_steel_plate.chemical_compositions['Al'].valid_flag
        assert '[FAIL]' in blank_steel_plate.chemical_compositions['Al'].message
        self.reset_chemical_composition(blank_steel_plate, 'Al', 0.020)
        assert limit_combination.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Al'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Al'].message
        self.reset_chemical_composition(blank_steel_plate, 'Al', 0.021)
        assert limit_combination.verify(blank_steel_plate)
        assert blank_steel_plate.chemical_compositions['Al'].valid_flag
        assert '[PASS]' in blank_steel_plate.chemical_compositions['Al'].message

    def test_combination_alplusnb_alplusv(self, blank_steel_plate: SteelPlate):
        limit_combination = LongTengRuleMaker.compose_fine_grain_element_limit_combination(['Al+Nb', 'Al+V'])
        # Al+Nb: Al >= 0.015; Nb >= 0.010; Nb + V + Ti <= 0.12
        # Al+V: Al >= 0.015; V >= 0.030; Nb + V + Ti <= 0.12
        # 1. both fail
        self.reset_chemical_composition(blank_steel_plate, 'Al', 0.014)
        self.reset_chemical_composition(blank_steel_plate, 'Nb', 0.010)
        self.reset_chemical_composition(blank_steel_plate, 'V', 0.030)
        self.reset_chemical_composition(blank_steel_plate, 'Ti', 0.010)
        assert not limit_combination.verify(blank_steel_plate)
        for element in ['Al', 'Nb', 'V', 'Ti']:
            assert not blank_steel_plate.chemical_compositions[element].valid_flag
            assert '[FAIL]' in blank_steel_plate.chemical_compositions[element].message
        # 2. Al+Nb pass, Al+V fail
        self.reset_chemical_composition(blank_steel_plate, 'Al', 0.015)
        self.reset_chemical_composition(blank_steel_plate, 'Nb', 0.010)
        self.reset_chemical_composition(blank_steel_plate, 'V', 0.029)
        self.reset_chemical_composition(blank_steel_plate, 'Ti', 0.010)
        assert limit_combination.verify(blank_steel_plate)
        for element in ['Al', 'Nb', 'V', 'Ti']:
            assert blank_steel_plate.chemical_compositions[element].valid_flag
            assert '[PASS]' in blank_steel_plate.chemical_compositions[element].message
        # 3. Al+Nb fail, Al+V pass
        self.reset_chemical_composition(blank_steel_plate, 'Al', 0.015)
        self.reset_chemical_composition(blank_steel_plate, 'Nb', 0.009)
        self.reset_chemical_composition(blank_steel_plate, 'V', 0.030)
        self.reset_chemical_composition(blank_steel_plate, 'Ti', 0.010)
        assert limit_combination.verify(blank_steel_plate)
        for element in ['Al', 'Nb', 'V', 'Ti']:
            assert blank_steel_plate.chemical_compositions[element].valid_flag
            assert '[PASS]' in blank_steel_plate.chemical_compositions[element].message
        # 4. both pass
        self.reset_chemical_composition(blank_steel_plate, 'Al', 0.015)
        self.reset_chemical_composition(blank_steel_plate, 'Nb', 0.010)
        self.reset_chemical_composition(blank_steel_plate, 'V', 0.030)
        self.reset_chemical_composition(blank_steel_plate, 'Ti', 0.010)
        assert limit_combination.verify(blank_steel_plate)
        for element in ['Al', 'Nb', 'V', 'Ti']:
            assert blank_steel_plate.chemical_compositions[element].valid_flag
            assert '[PASS]' in blank_steel_plate.chemical_compositions[element].message

    def test_combination_al_alplusnb_alplusv(self, blank_steel_plate: SteelPlate):
        # Al >= 0.020
        # Al+Nb: Al >= 0.015; Nb >= 0.010; Nb + V + Ti <= 0.12
        # Al+V: Al >= 0.015; V >= 0.030; Nb + V + Ti <= 0.12
        limit_combination = LongTengRuleMaker.compose_fine_grain_element_limit_combination(['Al', 'Al+Nb', 'Al+V'])
        # 1. All fail
        self.reset_chemical_composition(blank_steel_plate, 'Al', 0.014)
        self.reset_chemical_composition(blank_steel_plate, 'Nb', 0.010)
        self.reset_chemical_composition(blank_steel_plate, 'V', 0.030)
        self.reset_chemical_composition(blank_steel_plate, 'Ti', 0.010)
        assert not limit_combination.verify(blank_steel_plate)
        for element in ['Al', 'Nb', 'V', 'Ti']:
            assert not blank_steel_plate.chemical_compositions[element].valid_flag
            assert '[FAIL]' in blank_steel_plate.chemical_compositions[element].message
        # 2. Al pass, Al+Nb fail, Al+V fail
        self.reset_chemical_composition(blank_steel_plate, 'Al', 0.020)
        self.reset_chemical_composition(blank_steel_plate, 'Nb', 0.009)
        self.reset_chemical_composition(blank_steel_plate, 'V', 0.029)
        self.reset_chemical_composition(blank_steel_plate, 'Ti', 0.010)
        assert limit_combination.verify(blank_steel_plate)
        for element in ['Al', 'Nb', 'V', 'Ti']:
            assert blank_steel_plate.chemical_compositions[element].valid_flag
            if element == 'Al':
                assert 'PASS' in blank_steel_plate.chemical_compositions[element].message
            else:
                assert blank_steel_plate.chemical_compositions[element].message is None
        # 3. Al fail, Al+Nb pass, Al+V fail
        self.reset_chemical_composition(blank_steel_plate, 'Al', 0.019)
        self.reset_chemical_composition(blank_steel_plate, 'Nb', 0.010)
        self.reset_chemical_composition(blank_steel_plate, 'V', 0.029)
        self.reset_chemical_composition(blank_steel_plate, 'Ti', 0.010)
        assert limit_combination.verify(blank_steel_plate)
        for element in ['Al', 'Nb', 'V', 'Ti']:
            assert blank_steel_plate.chemical_compositions[element].valid_flag
            assert 'PASS' in blank_steel_plate.chemical_compositions[element].message
        # 4. Al fail, Al+Nb fail, Al+V pass
        self.reset_chemical_composition(blank_steel_plate, 'Al', 0.019)
        self.reset_chemical_composition(blank_steel_plate, 'Nb', 0.009)
        self.reset_chemical_composition(blank_steel_plate, 'V', 0.030)
        self.reset_chemical_composition(blank_steel_plate, 'Ti', 0.010)
        assert limit_combination.verify(blank_steel_plate)
        for element in ['Al', 'Nb', 'V', 'Ti']:
            assert blank_steel_plate.chemical_compositions[element].valid_flag
            assert 'PASS' in blank_steel_plate.chemical_compositions[element].message
        # 5. Al pass, Al+Nb pass, Al+V fail
        self.reset_chemical_composition(blank_steel_plate, 'Al', 0.020)
        self.reset_chemical_composition(blank_steel_plate, 'Nb', 0.010)
        self.reset_chemical_composition(blank_steel_plate, 'V', 0.029)
        self.reset_chemical_composition(blank_steel_plate, 'Ti', 0.010)
        assert limit_combination.verify(blank_steel_plate)
        for element in ['Al', 'Nb', 'V', 'Ti']:
            assert blank_steel_plate.chemical_compositions[element].valid_flag
            if element == 'Al':
                assert 'PASS' in blank_steel_plate.chemical_compositions[element].message
            else:
                assert blank_steel_plate.chemical_compositions[element].message is None
        # 6. Al fail, Al+Nb pass, Al+V pass
        self.reset_chemical_composition(blank_steel_plate, 'Al', 0.019)
        self.reset_chemical_composition(blank_steel_plate, 'Nb', 0.010)
        self.reset_chemical_composition(blank_steel_plate, 'V', 0.030)
        self.reset_chemical_composition(blank_steel_plate, 'Ti', 0.010)
        assert limit_combination.verify(blank_steel_plate)
        for element in ['Al', 'Nb', 'V', 'Ti']:
            assert blank_steel_plate.chemical_compositions[element].valid_flag
            assert 'PASS' in blank_steel_plate.chemical_compositions[element].message
        # 7. All pass
        self.reset_chemical_composition(blank_steel_plate, 'Al', 0.020)
        self.reset_chemical_composition(blank_steel_plate, 'Nb', 0.010)
        self.reset_chemical_composition(blank_steel_plate, 'V', 0.030)
        self.reset_chemical_composition(blank_steel_plate, 'Ti', 0.010)
        assert limit_combination.verify(blank_steel_plate)
        for element in ['Al', 'Nb', 'V', 'Ti']:
            assert blank_steel_plate.chemical_compositions[element].valid_flag
            if element == 'Al':
                assert 'PASS' in blank_steel_plate.chemical_compositions[element].message
            else:
                assert blank_steel_plate.chemical_compositions[element].message is None
