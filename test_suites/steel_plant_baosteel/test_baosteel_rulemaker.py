from typing import Dict

import pytest

from certificate_verification import BaoSteelRuleMaker, LimitType, ImpactEnergyLimit
from common import SteelPlate, SerialNumber, ChemicalElementValue, Thickness, Specification, DeliveryCondition, \
    YieldStrength, TensileStrength, Elongation, Temperature, ImpactEnergy, PositionDirectionImpact, Direction
from test_suites.common.conftest import BaseTester


@pytest.fixture(scope='module')
def rule_maker():
    return BaoSteelRuleMaker()


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
    plate.position_direction_impact = PositionDirectionImpact(
        table_index=None,
        x_coordinate=None,
        y_coordinate=None,
        value=Direction.LONGITUDINAL,
        index=None
    )
    return plate


class TestSpecialRules(BaseTester):

    def test_special_rules(self, rule_maker: BaoSteelRuleMaker, plate: SteelPlate):
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='SpecificationLimit',
            limit_type=LimitType.SCOPE,
            scope=[
                'VL A', 'VL B', 'VL D', 'VL E',
                'VL A27S', 'VL D27S', 'VL E27S', 'VL F27S',
                'VL A32', 'VL D32', 'VL E32', 'VL F32',
                'VL A36', 'VL D36', 'VL E36', 'VL F36',
                'VL A40', 'VL D40', 'VL E40', 'VL F40'
            ]
        )


class TestChemicalCompositionNormalStrengthSteel(BaseTester):

    def test_vl_a(self, rule_maker: BaoSteelRuleMaker, plate: SteelPlate):
        plate.specification.value = 'VL A'
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='ChemicalCompositionLimit',
            chemical_element='C',
            limit_type=LimitType.MAXIMUM,
            maximum=0.21
        )
        self.get_limit(
            limit_list=limits,
            limit_class='ChemicalCompositionLimit',
            chemical_element='Si',
            limit_type=LimitType.MAXIMUM,
            maximum=0.50
        )
        self.get_limit(
            limit_list=limits,
            limit_class='ChemicalCompositionLimit',
            chemical_element='Mn',
            limit_type=LimitType.MINIMUM,
            minimum=0.525
        )
        self.get_limit(
            limit_list=limits,
            limit_class='ChemicalCompositionLimit',
            chemical_element='P',
            limit_type=LimitType.MAXIMUM,
            maximum=0.035
        )
        self.get_limit(
            limit_list=limits,
            limit_class='ChemicalCompositionLimit',
            chemical_element='S',
            limit_type=LimitType.MAXIMUM,
            maximum=0.035
        )
        self.get_limit(
            limit_list=limits,
            limit_class='ChemicalCompositionLimit',
            chemical_element='Cu',
            limit_type=LimitType.MAXIMUM,
            maximum=0.35
        )
        self.get_limit(
            limit_list=limits,
            limit_class='ChemicalCompositionLimit',
            chemical_element='Cr',
            limit_type=LimitType.MAXIMUM,
            maximum=0.20
        )
        self.get_limit(
            limit_list=limits,
            limit_class='ChemicalCompositionLimit',
            chemical_element='Ni',
            limit_type=LimitType.MAXIMUM,
            maximum=0.40
        )
        self.get_limit(
            limit_list=limits,
            limit_class='ChemicalCompositionLimit',
            chemical_element='Mo',
            limit_type=LimitType.MAXIMUM,
            maximum=0.08
        )
        self.get_limit(
            limit_list=limits,
            limit_class='ChemicalCompositionLimit',
            chemical_element='C + 1/6 Mn',
            limit_type=LimitType.MAXIMUM,
            maximum=0.40
        )

    def test_vl_b(self, rule_maker: BaoSteelRuleMaker, plate: SteelPlate):
        plate.specification.value = 'VL B'
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='ChemicalCompositionLimit',
            chemical_element='C',
            limit_type=LimitType.MAXIMUM,
            maximum=0.21
        )
        self.get_limit(
            limit_list=limits,
            limit_class='ChemicalCompositionLimit',
            chemical_element='Si',
            limit_type=LimitType.MAXIMUM,
            maximum=0.35
        )
        # the plate has 4 impact test instances
        self.get_limit(
            limit_list=limits,
            limit_class='ChemicalCompositionLimit',
            chemical_element='Mn',
            limit_type=LimitType.MINIMUM,
            minimum=0.60
        )
        self.get_limit(
            limit_list=limits,
            limit_class='ChemicalCompositionLimit',
            chemical_element='P',
            limit_type=LimitType.MAXIMUM,
            maximum=0.035
        )
        self.get_limit(
            limit_list=limits,
            limit_class='ChemicalCompositionLimit',
            chemical_element='S',
            limit_type=LimitType.MAXIMUM,
            maximum=0.035
        )
        self.get_limit(
            limit_list=limits,
            limit_class='ChemicalCompositionLimit',
            chemical_element='Cu',
            limit_type=LimitType.MAXIMUM,
            maximum=0.35
        )
        self.get_limit(
            limit_list=limits,
            limit_class='ChemicalCompositionLimit',
            chemical_element='Cr',
            limit_type=LimitType.MAXIMUM,
            maximum=0.20
        )
        self.get_limit(
            limit_list=limits,
            limit_class='ChemicalCompositionLimit',
            chemical_element='Ni',
            limit_type=LimitType.MAXIMUM,
            maximum=0.40
        )
        self.get_limit(
            limit_list=limits,
            limit_class='ChemicalCompositionLimit',
            chemical_element='Mo',
            limit_type=LimitType.MAXIMUM,
            maximum=0.08
        )
        self.get_limit(
            limit_list=limits,
            limit_class='ChemicalCompositionLimit',
            chemical_element='C + 1/6 Mn',
            limit_type=LimitType.MAXIMUM,
            maximum=0.40
        )
        plate.impact_energy_list = []
        limits = rule_maker.get_rules(plate)
        # now there is no impact test values, the minimum value should be raised to 0.80
        self.get_limit(
            limit_list=limits,
            limit_class='ChemicalCompositionLimit',
            chemical_element='Mn',
            limit_type=LimitType.MINIMUM,
            minimum=0.80
        )

    def test_vl_d(self, rule_maker: BaoSteelRuleMaker, plate: SteelPlate):
        plate.specification.value = 'VL D'
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='ChemicalCompositionLimit',
            chemical_element='C',
            limit_type=LimitType.MAXIMUM,
            maximum=0.21
        )
        self.get_limit(
            limit_list=limits,
            limit_class='ChemicalCompositionLimit',
            chemical_element='Si',
            limit_type=LimitType.RANGE,
            minimum=0.10,
            maximum=0.35
        )
        self.get_limit(
            limit_list=limits,
            limit_class='ChemicalCompositionLimit',
            chemical_element='Mn',
            limit_type=LimitType.MINIMUM,
            minimum=0.60
        )
        self.get_limit(
            limit_list=limits,
            limit_class='ChemicalCompositionLimit',
            chemical_element='P',
            limit_type=LimitType.MAXIMUM,
            maximum=0.035
        )
        self.get_limit(
            limit_list=limits,
            limit_class='ChemicalCompositionLimit',
            chemical_element='S',
            limit_type=LimitType.MAXIMUM,
            maximum=0.035
        )
        self.get_limit(
            limit_list=limits,
            limit_class='ChemicalCompositionLimit',
            chemical_element='Cu',
            limit_type=LimitType.MAXIMUM,
            maximum=0.35
        )
        self.get_limit(
            limit_list=limits,
            limit_class='ChemicalCompositionLimit',
            chemical_element='Cr',
            limit_type=LimitType.MAXIMUM,
            maximum=0.20
        )
        self.get_limit(
            limit_list=limits,
            limit_class='ChemicalCompositionLimit',
            chemical_element='Ni',
            limit_type=LimitType.MAXIMUM,
            maximum=0.40
        )
        self.get_limit(
            limit_list=limits,
            limit_class='ChemicalCompositionLimit',
            chemical_element='Mo',
            limit_type=LimitType.MAXIMUM,
            maximum=0.08
        )
        self.get_limit(
            limit_list=limits,
            limit_class='ChemicalCompositionLimit',
            chemical_element='C + 1/6 Mn',
            limit_type=LimitType.MAXIMUM,
            maximum=0.40
        )

    def test_vl_e(self, rule_maker: BaoSteelRuleMaker, plate: SteelPlate):
        plate.specification.value = 'VL E'
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='ChemicalCompositionLimit',
            chemical_element='C',
            limit_type=LimitType.MAXIMUM,
            maximum=0.18
        )
        self.get_limit(
            limit_list=limits,
            limit_class='ChemicalCompositionLimit',
            chemical_element='Si',
            limit_type=LimitType.RANGE,
            minimum=0.10,
            maximum=0.35
        )
        self.get_limit(
            limit_list=limits,
            limit_class='ChemicalCompositionLimit',
            chemical_element='Mn',
            limit_type=LimitType.MINIMUM,
            minimum=0.70
        )
        self.get_limit(
            limit_list=limits,
            limit_class='ChemicalCompositionLimit',
            chemical_element='P',
            limit_type=LimitType.MAXIMUM,
            maximum=0.035
        )
        self.get_limit(
            limit_list=limits,
            limit_class='ChemicalCompositionLimit',
            chemical_element='S',
            limit_type=LimitType.MAXIMUM,
            maximum=0.035
        )
        self.get_limit(
            limit_list=limits,
            limit_class='ChemicalCompositionLimit',
            chemical_element='Cu',
            limit_type=LimitType.MAXIMUM,
            maximum=0.35
        )
        self.get_limit(
            limit_list=limits,
            limit_class='ChemicalCompositionLimit',
            chemical_element='Cr',
            limit_type=LimitType.MAXIMUM,
            maximum=0.20
        )
        self.get_limit(
            limit_list=limits,
            limit_class='ChemicalCompositionLimit',
            chemical_element='Ni',
            limit_type=LimitType.MAXIMUM,
            maximum=0.40
        )
        self.get_limit(
            limit_list=limits,
            limit_class='ChemicalCompositionLimit',
            chemical_element='Mo',
            limit_type=LimitType.MAXIMUM,
            maximum=0.08
        )
        self.get_limit(
            limit_list=limits,
            limit_class='ChemicalCompositionLimit',
            chemical_element='C + 1/6 Mn',
            limit_type=LimitType.MAXIMUM,
            maximum=0.40
        )


class TestChemicalCompositionHighStrengthSteel(BaseTester):

    def test_group1(self, rule_maker: BaoSteelRuleMaker, plate: SteelPlate):
        for specification in ['VL A27S', 'VL D27S', 'VL E27S']:
            plate.specification.value = specification
            limits = rule_maker.get_rules(plate)
            self.get_limit(
                limit_list=limits,
                limit_class='ChemicalCompositionLimit',
                chemical_element='C',
                limit_type=LimitType.MAXIMUM,
                maximum=0.18
            )
            self.get_limit(
                limit_list=limits,
                limit_class='ChemicalCompositionLimit',
                chemical_element='Si',
                limit_type=LimitType.MAXIMUM,
                maximum=0.5
            )
            self.get_limit(
                limit_list=limits,
                limit_class='ChemicalCompositionLimit',
                chemical_element='Mn',
                limit_type=LimitType.RANGE,
                minimum=0.70,
                maximum=1.60
            )
            self.get_limit(
                limit_list=limits,
                limit_class='ChemicalCompositionLimit',
                chemical_element='P',
                limit_type=LimitType.MAXIMUM,
                maximum=0.035
            )
            self.get_limit(
                limit_list=limits,
                limit_class='ChemicalCompositionLimit',
                chemical_element='S',
                limit_type=LimitType.MAXIMUM,
                maximum=0.035
            )
            self.get_limit(
                limit_list=limits,
                limit_class='ChemicalCompositionLimit',
                chemical_element='Cu',
                limit_type=LimitType.MAXIMUM,
                maximum=0.35
            )
            self.get_limit(
                limit_list=limits,
                limit_class='ChemicalCompositionLimit',
                chemical_element='Cr',
                limit_type=LimitType.MAXIMUM,
                maximum=0.20
            )
            self.get_limit(
                limit_list=limits,
                limit_class='ChemicalCompositionLimit',
                chemical_element='Ni',
                limit_type=LimitType.MAXIMUM,
                maximum=0.40
            )
            self.get_limit(
                limit_list=limits,
                limit_class='ChemicalCompositionLimit',
                chemical_element='Mo',
                limit_type=LimitType.MAXIMUM,
                maximum=0.08
            )

    def test_group2(self, rule_maker: BaoSteelRuleMaker, plate: SteelPlate):
        for specification in ['VL A32', 'VL D32', 'VL E32', 'VL A36', 'VL D36', 'VL E36', 'VL A40', 'VL D40', 'VL E40']:
            plate.specification.value = specification
            plate.thickness.value = 12.5
            limits = rule_maker.get_rules(plate)
            self.get_limit(
                limit_list=limits,
                limit_class='ChemicalCompositionLimit',
                chemical_element='C',
                limit_type=LimitType.MAXIMUM,
                maximum=0.18
            )
            self.get_limit(
                limit_list=limits,
                limit_class='ChemicalCompositionLimit',
                chemical_element='Si',
                limit_type=LimitType.MAXIMUM,
                maximum=0.5
            )
            self.get_limit(
                limit_list=limits,
                limit_class='ChemicalCompositionLimit',
                chemical_element='Mn',
                limit_type=LimitType.RANGE,
                minimum=0.70,
                maximum=1.60
            )
            self.get_limit(
                limit_list=limits,
                limit_class='ChemicalCompositionLimit',
                chemical_element='P',
                limit_type=LimitType.MAXIMUM,
                maximum=0.035
            )
            self.get_limit(
                limit_list=limits,
                limit_class='ChemicalCompositionLimit',
                chemical_element='S',
                limit_type=LimitType.MAXIMUM,
                maximum=0.035
            )
            self.get_limit(
                limit_list=limits,
                limit_class='ChemicalCompositionLimit',
                chemical_element='Cu',
                limit_type=LimitType.MAXIMUM,
                maximum=0.35
            )
            self.get_limit(
                limit_list=limits,
                limit_class='ChemicalCompositionLimit',
                chemical_element='Cr',
                limit_type=LimitType.MAXIMUM,
                maximum=0.20
            )
            self.get_limit(
                limit_list=limits,
                limit_class='ChemicalCompositionLimit',
                chemical_element='Ni',
                limit_type=LimitType.MAXIMUM,
                maximum=0.40
            )
            self.get_limit(
                limit_list=limits,
                limit_class='ChemicalCompositionLimit',
                chemical_element='Mo',
                limit_type=LimitType.MAXIMUM,
                maximum=0.08
            )
            plate.thickness.value = 12.6
            limits = rule_maker.get_rules(plate)
            self.get_limit(
                limit_list=limits,
                limit_class='ChemicalCompositionLimit',
                chemical_element='Mn',
                limit_type=LimitType.RANGE,
                minimum=0.90,
                maximum=1.60
            )

    def test_group3(self, rule_maker: BaoSteelRuleMaker, plate: SteelPlate):
        for specification in ['VL F27S', 'VL F32', 'VL F36', 'VL F40']:
            plate.specification.value = specification
            limits = rule_maker.get_rules(plate)
            self.get_limit(
                limit_list=limits,
                limit_class='ChemicalCompositionLimit',
                chemical_element='C',
                limit_type=LimitType.MAXIMUM,
                maximum=0.16
            )
            self.get_limit(
                limit_list=limits,
                limit_class='ChemicalCompositionLimit',
                chemical_element='Si',
                limit_type=LimitType.MAXIMUM,
                maximum=0.5
            )
            self.get_limit(
                limit_list=limits,
                limit_class='ChemicalCompositionLimit',
                chemical_element='Mn',
                limit_type=LimitType.RANGE,
                minimum=0.90,
                maximum=1.60
            )
            self.get_limit(
                limit_list=limits,
                limit_class='ChemicalCompositionLimit',
                chemical_element='P',
                limit_type=LimitType.MAXIMUM,
                maximum=0.025
            )
            self.get_limit(
                limit_list=limits,
                limit_class='ChemicalCompositionLimit',
                chemical_element='S',
                limit_type=LimitType.MAXIMUM,
                maximum=0.025
            )
            self.get_limit(
                limit_list=limits,
                limit_class='ChemicalCompositionLimit',
                chemical_element='Cu',
                limit_type=LimitType.MAXIMUM,
                maximum=0.35
            )
            self.get_limit(
                limit_list=limits,
                limit_class='ChemicalCompositionLimit',
                chemical_element='Cr',
                limit_type=LimitType.MAXIMUM,
                maximum=0.20
            )
            self.get_limit(
                limit_list=limits,
                limit_class='ChemicalCompositionLimit',
                chemical_element='Ni',
                limit_type=LimitType.MAXIMUM,
                maximum=0.80
            )
            self.get_limit(
                limit_list=limits,
                limit_class='ChemicalCompositionLimit',
                chemical_element='Mo',
                limit_type=LimitType.MAXIMUM,
                maximum=0.08
            )

    def test_ceq_group1(self, rule_maker: BaoSteelRuleMaker, plate: SteelPlate):
        # ceq is only required to check when delivery condition is TM
        plate.delivery_condition.value = 'TM'
        for specification in ['VL A27S', 'VL D27S', 'VL E27S', 'VL F27S']:
            plate.specification.value = specification
            plate.thickness.value = 49
            limits = rule_maker.get_rules(plate)
            self.get_limit(
                limit_list=limits,
                limit_class='ChemicalCompositionLimit',
                chemical_element='Ceq',
                limit_type=LimitType.MAXIMUM,
                maximum=0.34
            )
            plate.thickness.value = 50
            limits = rule_maker.get_rules(plate)
            self.get_limit(
                limit_list=limits,
                limit_class='ChemicalCompositionLimit',
                chemical_element='Ceq',
                limit_type=LimitType.MAXIMUM,
                maximum=0.34
            )
            plate.thickness.value = 51
            limits = rule_maker.get_rules(plate)
            self.get_limit(
                limit_list=limits,
                limit_class='ChemicalCompositionLimit',
                chemical_element='Ceq',
                limit_type=LimitType.MAXIMUM,
                maximum=0.36
            )
            plate.thickness.value = 99
            limits = rule_maker.get_rules(plate)
            self.get_limit(
                limit_list=limits,
                limit_class='ChemicalCompositionLimit',
                chemical_element='Ceq',
                limit_type=LimitType.MAXIMUM,
                maximum=0.36
            )
            plate.thickness.value = 100
            limits = rule_maker.get_rules(plate)
            self.get_limit(
                limit_list=limits,
                limit_class='ChemicalCompositionLimit',
                chemical_element='Ceq',
                limit_type=LimitType.MAXIMUM,
                maximum=0.36
            )
            plate.thickness.value = 101
            limits = rule_maker.get_rules(plate)
            self.get_limit(
                limit_list=limits,
                limit_class='ChemicalCompositionLimit',
                chemical_element='Ceq',
                limit_type=LimitType.MAXIMUM,
                maximum=0.38
            )
            plate.thickness.value = 149
            limits = rule_maker.get_rules(plate)
            self.get_limit(
                limit_list=limits,
                limit_class='ChemicalCompositionLimit',
                chemical_element='Ceq',
                limit_type=LimitType.MAXIMUM,
                maximum=0.38
            )
            plate.thickness.value = 150
            limits = rule_maker.get_rules(plate)
            self.get_limit(
                limit_list=limits,
                limit_class='ChemicalCompositionLimit',
                chemical_element='Ceq',
                limit_type=LimitType.MAXIMUM,
                maximum=0.38
            )

    def test_ceq_group2(self, rule_maker: BaoSteelRuleMaker, plate: SteelPlate):
        # ceq is only required to check when delivery condition is TM
        plate.delivery_condition.value = 'TM'
        for specification in ['VL A32', 'VL D32', 'VL E32', 'VL F32']:
            plate.specification.value = specification
            plate.thickness.value = 49
            limits = rule_maker.get_rules(plate)
            self.get_limit(
                limit_list=limits,
                limit_class='ChemicalCompositionLimit',
                chemical_element='Ceq',
                limit_type=LimitType.MAXIMUM,
                maximum=0.36
            )
            plate.thickness.value = 50
            limits = rule_maker.get_rules(plate)
            self.get_limit(
                limit_list=limits,
                limit_class='ChemicalCompositionLimit',
                chemical_element='Ceq',
                limit_type=LimitType.MAXIMUM,
                maximum=0.36
            )
            plate.thickness.value = 51
            limits = rule_maker.get_rules(plate)
            self.get_limit(
                limit_list=limits,
                limit_class='ChemicalCompositionLimit',
                chemical_element='Ceq',
                limit_type=LimitType.MAXIMUM,
                maximum=0.38
            )
            plate.thickness.value = 99
            limits = rule_maker.get_rules(plate)
            self.get_limit(
                limit_list=limits,
                limit_class='ChemicalCompositionLimit',
                chemical_element='Ceq',
                limit_type=LimitType.MAXIMUM,
                maximum=0.38
            )
            plate.thickness.value = 100
            limits = rule_maker.get_rules(plate)
            self.get_limit(
                limit_list=limits,
                limit_class='ChemicalCompositionLimit',
                chemical_element='Ceq',
                limit_type=LimitType.MAXIMUM,
                maximum=0.38
            )
            plate.thickness.value = 101
            limits = rule_maker.get_rules(plate)
            self.get_limit(
                limit_list=limits,
                limit_class='ChemicalCompositionLimit',
                chemical_element='Ceq',
                limit_type=LimitType.MAXIMUM,
                maximum=0.40
            )
            plate.thickness.value = 149
            limits = rule_maker.get_rules(plate)
            self.get_limit(
                limit_list=limits,
                limit_class='ChemicalCompositionLimit',
                chemical_element='Ceq',
                limit_type=LimitType.MAXIMUM,
                maximum=0.40
            )
            plate.thickness.value = 150
            limits = rule_maker.get_rules(plate)
            self.get_limit(
                limit_list=limits,
                limit_class='ChemicalCompositionLimit',
                chemical_element='Ceq',
                limit_type=LimitType.MAXIMUM,
                maximum=0.40
            )

    def test_ceq_group3(self, rule_maker: BaoSteelRuleMaker, plate: SteelPlate):
        # ceq is only required to check when delivery condition is TM
        plate.delivery_condition.value = 'TM'
        for specification in ['VL A36', 'VL D36', 'VL E36', 'VL F36']:
            plate.specification.value = specification
            plate.thickness.value = 49
            limits = rule_maker.get_rules(plate)
            self.get_limit(
                limit_list=limits,
                limit_class='ChemicalCompositionLimit',
                chemical_element='Ceq',
                limit_type=LimitType.MAXIMUM,
                maximum=0.38
            )
            plate.thickness.value = 50
            limits = rule_maker.get_rules(plate)
            self.get_limit(
                limit_list=limits,
                limit_class='ChemicalCompositionLimit',
                chemical_element='Ceq',
                limit_type=LimitType.MAXIMUM,
                maximum=0.38
            )
            plate.thickness.value = 51
            limits = rule_maker.get_rules(plate)
            self.get_limit(
                limit_list=limits,
                limit_class='ChemicalCompositionLimit',
                chemical_element='Ceq',
                limit_type=LimitType.MAXIMUM,
                maximum=0.40
            )
            plate.thickness.value = 99
            limits = rule_maker.get_rules(plate)
            self.get_limit(
                limit_list=limits,
                limit_class='ChemicalCompositionLimit',
                chemical_element='Ceq',
                limit_type=LimitType.MAXIMUM,
                maximum=0.40
            )
            plate.thickness.value = 100
            limits = rule_maker.get_rules(plate)
            self.get_limit(
                limit_list=limits,
                limit_class='ChemicalCompositionLimit',
                chemical_element='Ceq',
                limit_type=LimitType.MAXIMUM,
                maximum=0.40
            )
            plate.thickness.value = 101
            limits = rule_maker.get_rules(plate)
            self.get_limit(
                limit_list=limits,
                limit_class='ChemicalCompositionLimit',
                chemical_element='Ceq',
                limit_type=LimitType.MAXIMUM,
                maximum=0.42
            )
            plate.thickness.value = 149
            limits = rule_maker.get_rules(plate)
            self.get_limit(
                limit_list=limits,
                limit_class='ChemicalCompositionLimit',
                chemical_element='Ceq',
                limit_type=LimitType.MAXIMUM,
                maximum=0.42
            )
            plate.thickness.value = 150
            limits = rule_maker.get_rules(plate)
            self.get_limit(
                limit_list=limits,
                limit_class='ChemicalCompositionLimit',
                chemical_element='Ceq',
                limit_type=LimitType.MAXIMUM,
                maximum=0.42
            )

    def test_ceq_group4(self, rule_maker: BaoSteelRuleMaker, plate: SteelPlate):
        # ceq is only required to check when delivery condition is TM
        plate.delivery_condition.value = 'TM'
        for specification in ['VL A40', 'VL D40', 'VL E40', 'VL F40']:
            plate.specification.value = specification
            plate.thickness.value = 49
            limits = rule_maker.get_rules(plate)
            self.get_limit(
                limit_list=limits,
                limit_class='ChemicalCompositionLimit',
                chemical_element='Ceq',
                limit_type=LimitType.MAXIMUM,
                maximum=0.40
            )
            plate.thickness.value = 50
            limits = rule_maker.get_rules(plate)
            self.get_limit(
                limit_list=limits,
                limit_class='ChemicalCompositionLimit',
                chemical_element='Ceq',
                limit_type=LimitType.MAXIMUM,
                maximum=0.40
            )
            plate.thickness.value = 51
            limits = rule_maker.get_rules(plate)
            self.get_limit(
                limit_list=limits,
                limit_class='ChemicalCompositionLimit',
                chemical_element='Ceq',
                limit_type=LimitType.MAXIMUM,
                maximum=0.42
            )
            plate.thickness.value = 99
            limits = rule_maker.get_rules(plate)
            self.get_limit(
                limit_list=limits,
                limit_class='ChemicalCompositionLimit',
                chemical_element='Ceq',
                limit_type=LimitType.MAXIMUM,
                maximum=0.42
            )
            plate.thickness.value = 100
            limits = rule_maker.get_rules(plate)
            self.get_limit(
                limit_list=limits,
                limit_class='ChemicalCompositionLimit',
                chemical_element='Ceq',
                limit_type=LimitType.MAXIMUM,
                maximum=0.42
            )
            plate.thickness.value = 101
            limits = rule_maker.get_rules(plate)
            self.get_limit(
                limit_list=limits,
                limit_class='ChemicalCompositionLimit',
                chemical_element='Ceq',
                limit_type=LimitType.MAXIMUM,
                maximum=0.45
            )
            plate.thickness.value = 149
            limits = rule_maker.get_rules(plate)
            self.get_limit(
                limit_list=limits,
                limit_class='ChemicalCompositionLimit',
                chemical_element='Ceq',
                limit_type=LimitType.MAXIMUM,
                maximum=0.45
            )
            plate.thickness.value = 150
            limits = rule_maker.get_rules(plate)
            self.get_limit(
                limit_list=limits,
                limit_class='ChemicalCompositionLimit',
                chemical_element='Ceq',
                limit_type=LimitType.MAXIMUM,
                maximum=0.45
            )


class TestMechanicalPropertiesNormalStrengthSteel(BaseTester):

    def test_vl_a(self, rule_maker: BaoSteelRuleMaker, plate: SteelPlate):
        plate.specification.value = 'VL A'
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='YieldStrengthLimit',
            limit_type=LimitType.MINIMUM,
            minimum=235
        )
        self.get_limit(
            limit_list=limits,
            limit_class='TensileStrengthLimit',
            limit_type=LimitType.RANGE,
            minimum=400,
            maximum=520
        )
        self.get_limit(
            limit_list=limits,
            limit_class='ElongationLimit',
            limit_type=LimitType.MINIMUM,
            minimum=22
        )
        # Impact Test
        plate.thickness.value = 50
        limits = rule_maker.get_rules(plate)
        assert not any([isinstance(limit, ImpactEnergyLimit) for limit in limits])
        plate.thickness.value = 70
        plate.delivery_condition.value = 'N'
        limits = rule_maker.get_rules(plate)
        assert not any([isinstance(limit, ImpactEnergyLimit) for limit in limits])
        plate.delivery_condition.value = 'TM'
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='TemperatureLimit',
            limit_type=LimitType.MAXIMUM,
            maximum=20
        )
        self.get_limit(
            limit_list=limits,
            limit_class='PositionDirectionImpactLimit',
            limit_type=LimitType.SCOPE,
            scope=(Direction.LONGITUDINAL, Direction.TRANSVERSE)
        )
        plate.position_direction_impact.value = Direction.LONGITUDINAL
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='ImpactEnergyLimit',
            limit_type=LimitType.MINIMUM,
            minimum=34
        )
        plate.position_direction_impact.value = Direction.TRANSVERSE
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='ImpactEnergyLimit',
            limit_type=LimitType.MINIMUM,
            minimum=24
        )
        plate.thickness.value = 150
        plate.delivery_condition.value = 'N'
        limits = rule_maker.get_rules(plate)
        assert not any([isinstance(limit, ImpactEnergyLimit) for limit in limits])
        plate.delivery_condition.value = 'TM'
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='TemperatureLimit',
            limit_type=LimitType.MAXIMUM,
            maximum=20
        )
        self.get_limit(
            limit_list=limits,
            limit_class='PositionDirectionImpactLimit',
            limit_type=LimitType.SCOPE,
            scope=(Direction.LONGITUDINAL, Direction.TRANSVERSE)
        )
        plate.position_direction_impact.value = Direction.LONGITUDINAL
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='ImpactEnergyLimit',
            limit_type=LimitType.MINIMUM,
            minimum=41
        )
        plate.position_direction_impact.value = Direction.TRANSVERSE
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='ImpactEnergyLimit',
            limit_type=LimitType.MINIMUM,
            minimum=27
        )

    def test_vl_b(self, rule_maker: BaoSteelRuleMaker, plate: SteelPlate):
        plate.specification.value = 'VL B'
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='YieldStrengthLimit',
            limit_type=LimitType.MINIMUM,
            minimum=235
        )
        self.get_limit(
            limit_list=limits,
            limit_class='TensileStrengthLimit',
            limit_type=LimitType.RANGE,
            minimum=400,
            maximum=520
        )
        self.get_limit(
            limit_list=limits,
            limit_class='ElongationLimit',
            limit_type=LimitType.MINIMUM,
            minimum=22
        )
        # Impact Test
        plate.thickness.value = 25
        limits = rule_maker.get_rules(plate)
        assert not any([isinstance(limit, ImpactEnergyLimit) for limit in limits])
        plate.thickness.value = 50
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='TemperatureLimit',
            limit_type=LimitType.MAXIMUM,
            maximum=0
        )
        self.get_limit(
            limit_list=limits,
            limit_class='PositionDirectionImpactLimit',
            limit_type=LimitType.SCOPE,
            scope=(Direction.LONGITUDINAL, Direction.TRANSVERSE)
        )
        plate.position_direction_impact.value = Direction.LONGITUDINAL
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='ImpactEnergyLimit',
            limit_type=LimitType.MINIMUM,
            minimum=27
        )
        plate.position_direction_impact.value = Direction.TRANSVERSE
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='ImpactEnergyLimit',
            limit_type=LimitType.MINIMUM,
            minimum=20
        )
        plate.thickness.value = 70
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='TemperatureLimit',
            limit_type=LimitType.MAXIMUM,
            maximum=0
        )
        self.get_limit(
            limit_list=limits,
            limit_class='PositionDirectionImpactLimit',
            limit_type=LimitType.SCOPE,
            scope=(Direction.LONGITUDINAL, Direction.TRANSVERSE)
        )
        plate.position_direction_impact.value = Direction.LONGITUDINAL
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='ImpactEnergyLimit',
            limit_type=LimitType.MINIMUM,
            minimum=34
        )
        plate.position_direction_impact.value = Direction.TRANSVERSE
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='ImpactEnergyLimit',
            limit_type=LimitType.MINIMUM,
            minimum=24
        )
        plate.thickness.value = 150
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='TemperatureLimit',
            limit_type=LimitType.MAXIMUM,
            maximum=0
        )
        self.get_limit(
            limit_list=limits,
            limit_class='PositionDirectionImpactLimit',
            limit_type=LimitType.SCOPE,
            scope=(Direction.LONGITUDINAL, Direction.TRANSVERSE)
        )
        plate.position_direction_impact.value = Direction.LONGITUDINAL
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='ImpactEnergyLimit',
            limit_type=LimitType.MINIMUM,
            minimum=41
        )
        plate.position_direction_impact.value = Direction.TRANSVERSE
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='ImpactEnergyLimit',
            limit_type=LimitType.MINIMUM,
            minimum=27
        )

    def test_vl_d(self, rule_maker: BaoSteelRuleMaker, plate: SteelPlate):
        plate.specification.value = 'VL D'
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='YieldStrengthLimit',
            limit_type=LimitType.MINIMUM,
            minimum=235
        )
        self.get_limit(
            limit_list=limits,
            limit_class='TensileStrengthLimit',
            limit_type=LimitType.RANGE,
            minimum=400,
            maximum=520
        )
        self.get_limit(
            limit_list=limits,
            limit_class='ElongationLimit',
            limit_type=LimitType.MINIMUM,
            minimum=22
        )
        self.get_limit(
            limit_list=limits,
            limit_class='TemperatureLimit',
            limit_type=LimitType.MAXIMUM,
            maximum=-20
        )
        self.get_limit(
            limit_list=limits,
            limit_class='PositionDirectionImpactLimit',
            limit_type=LimitType.SCOPE,
            scope=(Direction.LONGITUDINAL, Direction.TRANSVERSE)
        )
        # Impact Test
        plate.thickness.value = 50
        plate.position_direction_impact.value = Direction.LONGITUDINAL
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='ImpactEnergyLimit',
            limit_type=LimitType.MINIMUM,
            minimum=27
        )
        plate.position_direction_impact.value = Direction.TRANSVERSE
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='ImpactEnergyLimit',
            limit_type=LimitType.MINIMUM,
            minimum=20
        )
        plate.thickness.value = 70
        plate.position_direction_impact.value = Direction.LONGITUDINAL
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='ImpactEnergyLimit',
            limit_type=LimitType.MINIMUM,
            minimum=34
        )
        plate.position_direction_impact.value = Direction.TRANSVERSE
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='ImpactEnergyLimit',
            limit_type=LimitType.MINIMUM,
            minimum=24
        )
        plate.thickness.value = 150
        plate.position_direction_impact.value = Direction.LONGITUDINAL
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='ImpactEnergyLimit',
            limit_type=LimitType.MINIMUM,
            minimum=41
        )
        plate.position_direction_impact.value = Direction.TRANSVERSE
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='ImpactEnergyLimit',
            limit_type=LimitType.MINIMUM,
            minimum=27
        )

    def test_vl_e(self, rule_maker: BaoSteelRuleMaker, plate: SteelPlate):
        plate.specification.value = 'VL E'
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='YieldStrengthLimit',
            limit_type=LimitType.MINIMUM,
            minimum=235
        )
        self.get_limit(
            limit_list=limits,
            limit_class='TensileStrengthLimit',
            limit_type=LimitType.RANGE,
            minimum=400,
            maximum=520
        )
        self.get_limit(
            limit_list=limits,
            limit_class='ElongationLimit',
            limit_type=LimitType.MINIMUM,
            minimum=22
        )
        self.get_limit(
            limit_list=limits,
            limit_class='TemperatureLimit',
            limit_type=LimitType.MAXIMUM,
            maximum=-40
        )
        self.get_limit(
            limit_list=limits,
            limit_class='PositionDirectionImpactLimit',
            limit_type=LimitType.SCOPE,
            scope=(Direction.LONGITUDINAL, Direction.TRANSVERSE)
        )
        # Impact Test
        plate.thickness.value = 50
        plate.position_direction_impact.value = Direction.LONGITUDINAL
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='ImpactEnergyLimit',
            limit_type=LimitType.MINIMUM,
            minimum=27
        )
        plate.position_direction_impact.value = Direction.TRANSVERSE
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='ImpactEnergyLimit',
            limit_type=LimitType.MINIMUM,
            minimum=20
        )
        plate.thickness.value = 70
        plate.position_direction_impact.value = Direction.LONGITUDINAL
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='ImpactEnergyLimit',
            limit_type=LimitType.MINIMUM,
            minimum=34
        )
        plate.position_direction_impact.value = Direction.TRANSVERSE
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='ImpactEnergyLimit',
            limit_type=LimitType.MINIMUM,
            minimum=24
        )
        plate.thickness.value = 150
        plate.position_direction_impact.value = Direction.LONGITUDINAL
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='ImpactEnergyLimit',
            limit_type=LimitType.MINIMUM,
            minimum=41
        )
        plate.position_direction_impact.value = Direction.TRANSVERSE
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='ImpactEnergyLimit',
            limit_type=LimitType.MINIMUM,
            minimum=27
        )


@pytest.fixture
def temperature_map():
    return {
        'VL A27S': 0,
        'VL A32': 0,
        'VL A36': 0,
        'VL A40': 0,
        'VL D27S': -20,
        'VL D32': -20,
        'VL D36': -20,
        'VL D40': -20,
        'VL E27S': -40,
        'VL E32': -40,
        'VL E36': -40,
        'VL E40': -40,
        'VL F27S': -60,
        'VL F32': -60,
        'VL F36': -60,
        'VL F40': -60
    }


class TestMechanicalPropertiesHighStrengthSteel(BaseTester):

    def test_group1(self, rule_maker: BaoSteelRuleMaker, plate: SteelPlate, temperature_map: Dict[str, int]):
        for specification in ['VL A27S', 'VL D27S', 'VL E27S', 'VL F27S']:
            plate.specification.value = specification
            plate.thickness.value = 50
            plate.position_direction_impact.value = Direction.LONGITUDINAL
            limits = rule_maker.get_rules(plate)
            self.get_limit(
                limit_list=limits,
                limit_class='YieldStrengthLimit',
                limit_type=LimitType.MINIMUM,
                minimum=265
            )
            self.get_limit(
                limit_list=limits,
                limit_class='TensileStrengthLimit',
                limit_type=LimitType.RANGE,
                minimum=400,
                maximum=530
            )
            self.get_limit(
                limit_list=limits,
                limit_class='ElongationLimit',
                limit_type=LimitType.MINIMUM,
                minimum=22
            )
            self.get_limit(
                limit_list=limits,
                limit_class='TemperatureLimit',
                limit_type=LimitType.MAXIMUM,
                maximum=temperature_map[plate.specification.value]
            )
            self.get_limit(
                limit_list=limits,
                limit_class='PositionDirectionImpactLimit',
                limit_type=LimitType.SCOPE,
                scope=(Direction.LONGITUDINAL, Direction.TRANSVERSE)
            )
            self.get_limit(
                limit_list=limits,
                limit_class='ImpactEnergyLimit',
                limit_type=LimitType.MINIMUM,
                minimum=27
            )
            plate.position_direction_impact.value = Direction.TRANSVERSE
            limits = rule_maker.get_rules(plate)
            self.get_limit(
                limit_list=limits,
                limit_class='ImpactEnergyLimit',
                limit_type=LimitType.MINIMUM,
                minimum=20
            )
            plate.thickness.value = 70
            plate.position_direction_impact.value = Direction.LONGITUDINAL
            limits = rule_maker.get_rules(plate)
            self.get_limit(
                limit_list=limits,
                limit_class='ImpactEnergyLimit',
                limit_type=LimitType.MINIMUM,
                minimum=34
            )
            plate.position_direction_impact.value = Direction.TRANSVERSE
            limits = rule_maker.get_rules(plate)
            self.get_limit(
                limit_list=limits,
                limit_class='ImpactEnergyLimit',
                limit_type=LimitType.MINIMUM,
                minimum=24
            )
            plate.thickness.value = 150
            plate.position_direction_impact.value = Direction.LONGITUDINAL
            limits = rule_maker.get_rules(plate)
            self.get_limit(
                limit_list=limits,
                limit_class='ImpactEnergyLimit',
                limit_type=LimitType.MINIMUM,
                minimum=41
            )
            plate.position_direction_impact.value = Direction.TRANSVERSE
            limits = rule_maker.get_rules(plate)
            self.get_limit(
                limit_list=limits,
                limit_class='ImpactEnergyLimit',
                limit_type=LimitType.MINIMUM,
                minimum=27
            )

    def test_group2(self, rule_maker: BaoSteelRuleMaker, plate: SteelPlate, temperature_map: Dict[str, int]):
        for specification in ['VL A32', 'VL D32', 'VL E32', 'VL F32']:
            plate.specification.value = specification
            plate.thickness.value = 50
            plate.position_direction_impact.value = Direction.LONGITUDINAL
            limits = rule_maker.get_rules(plate)
            self.get_limit(
                limit_list=limits,
                limit_class='YieldStrengthLimit',
                limit_type=LimitType.MINIMUM,
                minimum=315
            )
            self.get_limit(
                limit_list=limits,
                limit_class='TensileStrengthLimit',
                limit_type=LimitType.RANGE,
                minimum=440,
                maximum=570
            )
            self.get_limit(
                limit_list=limits,
                limit_class='ElongationLimit',
                limit_type=LimitType.MINIMUM,
                minimum=22
            )
            self.get_limit(
                limit_list=limits,
                limit_class='TemperatureLimit',
                limit_type=LimitType.MAXIMUM,
                maximum=temperature_map[plate.specification.value]
            )
            self.get_limit(
                limit_list=limits,
                limit_class='PositionDirectionImpactLimit',
                limit_type=LimitType.SCOPE,
                scope=(Direction.LONGITUDINAL, Direction.TRANSVERSE)
            )
            self.get_limit(
                limit_list=limits,
                limit_class='ImpactEnergyLimit',
                limit_type=LimitType.MINIMUM,
                minimum=31
            )
            plate.position_direction_impact.value = Direction.TRANSVERSE
            limits = rule_maker.get_rules(plate)
            self.get_limit(
                limit_list=limits,
                limit_class='ImpactEnergyLimit',
                limit_type=LimitType.MINIMUM,
                minimum=22
            )
            plate.thickness.value = 70
            plate.position_direction_impact.value = Direction.LONGITUDINAL
            limits = rule_maker.get_rules(plate)
            self.get_limit(
                limit_list=limits,
                limit_class='ImpactEnergyLimit',
                limit_type=LimitType.MINIMUM,
                minimum=38
            )
            plate.position_direction_impact.value = Direction.TRANSVERSE
            limits = rule_maker.get_rules(plate)
            self.get_limit(
                limit_list=limits,
                limit_class='ImpactEnergyLimit',
                limit_type=LimitType.MINIMUM,
                minimum=26
            )
            plate.thickness.value = 150
            plate.position_direction_impact.value = Direction.LONGITUDINAL
            limits = rule_maker.get_rules(plate)
            self.get_limit(
                limit_list=limits,
                limit_class='ImpactEnergyLimit',
                limit_type=LimitType.MINIMUM,
                minimum=46
            )
            plate.position_direction_impact.value = Direction.TRANSVERSE
            limits = rule_maker.get_rules(plate)
            self.get_limit(
                limit_list=limits,
                limit_class='ImpactEnergyLimit',
                limit_type=LimitType.MINIMUM,
                minimum=31
            )

    def test_group3(self, rule_maker: BaoSteelRuleMaker, plate: SteelPlate, temperature_map: Dict[str, int]):
        for specification in ['VL A36', 'VL D36', 'VL E36', 'VL F36']:
            plate.specification.value = specification
            plate.thickness.value = 50
            plate.position_direction_impact.value = Direction.LONGITUDINAL
            limits = rule_maker.get_rules(plate)
            self.get_limit(
                limit_list=limits,
                limit_class='YieldStrengthLimit',
                limit_type=LimitType.MINIMUM,
                minimum=355
            )
            self.get_limit(
                limit_list=limits,
                limit_class='TensileStrengthLimit',
                limit_type=LimitType.RANGE,
                minimum=490,
                maximum=630
            )
            self.get_limit(
                limit_list=limits,
                limit_class='ElongationLimit',
                limit_type=LimitType.MINIMUM,
                minimum=21
            )
            self.get_limit(
                limit_list=limits,
                limit_class='TemperatureLimit',
                limit_type=LimitType.MAXIMUM,
                maximum=temperature_map[plate.specification.value]
            )
            self.get_limit(
                limit_list=limits,
                limit_class='PositionDirectionImpactLimit',
                limit_type=LimitType.SCOPE,
                scope=(Direction.LONGITUDINAL, Direction.TRANSVERSE)
            )
            self.get_limit(
                limit_list=limits,
                limit_class='ImpactEnergyLimit',
                limit_type=LimitType.MINIMUM,
                minimum=34
            )
            plate.position_direction_impact.value = Direction.TRANSVERSE
            limits = rule_maker.get_rules(plate)
            self.get_limit(
                limit_list=limits,
                limit_class='ImpactEnergyLimit',
                limit_type=LimitType.MINIMUM,
                minimum=24
            )
            plate.thickness.value = 70
            plate.position_direction_impact.value = Direction.LONGITUDINAL
            limits = rule_maker.get_rules(plate)
            self.get_limit(
                limit_list=limits,
                limit_class='ImpactEnergyLimit',
                limit_type=LimitType.MINIMUM,
                minimum=41
            )
            plate.position_direction_impact.value = Direction.TRANSVERSE
            limits = rule_maker.get_rules(plate)
            self.get_limit(
                limit_list=limits,
                limit_class='ImpactEnergyLimit',
                limit_type=LimitType.MINIMUM,
                minimum=27
            )
            plate.thickness.value = 150
            plate.position_direction_impact.value = Direction.LONGITUDINAL
            limits = rule_maker.get_rules(plate)
            self.get_limit(
                limit_list=limits,
                limit_class='ImpactEnergyLimit',
                limit_type=LimitType.MINIMUM,
                minimum=50
            )
            plate.position_direction_impact.value = Direction.TRANSVERSE
            limits = rule_maker.get_rules(plate)
            self.get_limit(
                limit_list=limits,
                limit_class='ImpactEnergyLimit',
                limit_type=LimitType.MINIMUM,
                minimum=34
            )

    def test_group4(self, rule_maker: BaoSteelRuleMaker, plate: SteelPlate, temperature_map: Dict[str, int]):
        for specification in ['VL A40', 'VL D40', 'VL E40', 'VL F40']:
            plate.specification.value = specification
            plate.thickness.value = 50
            plate.position_direction_impact.value = Direction.LONGITUDINAL
            limits = rule_maker.get_rules(plate)
            self.get_limit(
                limit_list=limits,
                limit_class='YieldStrengthLimit',
                limit_type=LimitType.MINIMUM,
                minimum=390
            )
            self.get_limit(
                limit_list=limits,
                limit_class='TensileStrengthLimit',
                limit_type=LimitType.RANGE,
                minimum=510,
                maximum=660
            )
            self.get_limit(
                limit_list=limits,
                limit_class='ElongationLimit',
                limit_type=LimitType.MINIMUM,
                minimum=20
            )
            self.get_limit(
                limit_list=limits,
                limit_class='TemperatureLimit',
                limit_type=LimitType.MAXIMUM,
                maximum=temperature_map[plate.specification.value]
            )
            self.get_limit(
                limit_list=limits,
                limit_class='PositionDirectionImpactLimit',
                limit_type=LimitType.SCOPE,
                scope=(Direction.LONGITUDINAL, Direction.TRANSVERSE)
            )
            self.get_limit(
                limit_list=limits,
                limit_class='ImpactEnergyLimit',
                limit_type=LimitType.MINIMUM,
                minimum=39
            )
            plate.position_direction_impact.value = Direction.TRANSVERSE
            limits = rule_maker.get_rules(plate)
            self.get_limit(
                limit_list=limits,
                limit_class='ImpactEnergyLimit',
                limit_type=LimitType.MINIMUM,
                minimum=26
            )
            plate.thickness.value = 70
            plate.position_direction_impact.value = Direction.LONGITUDINAL
            limits = rule_maker.get_rules(plate)
            self.get_limit(
                limit_list=limits,
                limit_class='ImpactEnergyLimit',
                limit_type=LimitType.MINIMUM,
                minimum=46
            )
            plate.position_direction_impact.value = Direction.TRANSVERSE
            limits = rule_maker.get_rules(plate)
            self.get_limit(
                limit_list=limits,
                limit_class='ImpactEnergyLimit',
                limit_type=LimitType.MINIMUM,
                minimum=31
            )
            plate.thickness.value = 150
            plate.position_direction_impact.value = Direction.LONGITUDINAL
            limits = rule_maker.get_rules(plate)
            self.get_limit(
                limit_list=limits,
                limit_class='ImpactEnergyLimit',
                limit_type=LimitType.MINIMUM,
                minimum=55
            )
            plate.position_direction_impact.value = Direction.TRANSVERSE
            limits = rule_maker.get_rules(plate)
            self.get_limit(
                limit_list=limits,
                limit_class='ImpactEnergyLimit',
                limit_type=LimitType.MINIMUM,
                minimum=37
            )


class TestFineGrainElementNormalStrengthSteel(BaseTester):

    def test_vl_a(self, rule_maker: BaoSteelRuleMaker, plate: SteelPlate):
        plate.specification.value = 'VL A'
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='DeliveryConditionLimit',
            limit_type=LimitType.SCOPE,
            scope=['N', 'AR', 'TM']
        )
        plate.delivery_condition.value = 'N'
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='ThicknessLimit',
            limit_type=LimitType.RANGE,
            maximum=80,
            minimum=0
        )
        plate.thickness.value = 35  # should hit Al+Ti, Al, Al+Nb, Al+Nb+Ti
        limits = rule_maker.get_rules(plate)
        self.check_fine_grain_element_combiantion(
            limit_list=limits,
            steel_plant='BAOSHAN IRON & STEEL CO., LTD.',
            strength='normal',
            include=['Al', 'Al+Ti', 'Al+Nb', 'Al+Nb+Ti']
        )
        plate.thickness.value = 80  # should hit Al, Al+Nb, Al+Nb+Ti
        limits = rule_maker.get_rules(plate)
        self.check_fine_grain_element_combiantion(
            limit_list=limits,
            steel_plant='BAOSHAN IRON & STEEL CO., LTD.',
            strength='normal',
            include=['Al', 'Al+Nb', 'Al+Nb+Ti']
        )
        plate.delivery_condition.value = 'AR'
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='ThicknessLimit',
            limit_type=LimitType.RANGE,
            minimum=0,
            maximum=50
        )
        plate.thickness.value = 50
        limits = rule_maker.get_rules(plate)
        self.check_fine_grain_element_combiantion(
            limit_list=limits,
            steel_plant='BAOSHAN IRON & STEEL CO., LTD.',
            strength='normal',
            include=['Al+Ti']
        )
        plate.delivery_condition.value = 'TM'
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='ThicknessLimit',
            limit_type=LimitType.RANGE,
            minimum=0,
            maximum=100
        )
        plate.thickness.value = 100
        limits = rule_maker.get_rules(plate)
        self.check_fine_grain_element_combiantion(
            limit_list=limits,
            steel_plant='BAOSHAN IRON & STEEL CO., LTD.',
            strength='normal',
            include=['Al+Nb+Ti']
        )

    def test_vl_b(self, rule_maker: BaoSteelRuleMaker, plate: SteelPlate):
        plate.specification.value = 'VL B'
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='DeliveryConditionLimit',
            limit_type=LimitType.SCOPE,
            scope=['N', 'AR', 'TM']
        )
        plate.delivery_condition.value = 'N'
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='ThicknessLimit',
            limit_type=LimitType.RANGE,
            maximum=80,
            minimum=0
        )
        plate.thickness.value = 35  # should hit Al+Ti, Al, Al+Nb, Al+Nb+Ti
        limits = rule_maker.get_rules(plate)
        self.check_fine_grain_element_combiantion(
            limit_list=limits,
            steel_plant='BAOSHAN IRON & STEEL CO., LTD.',
            strength='normal',
            include=['Al', 'Al+Ti', 'Al+Nb', 'Al+Nb+Ti']
        )
        plate.thickness.value = 80  # should hit Al, Al+Nb, Al+Nb+Ti
        limits = rule_maker.get_rules(plate)
        self.check_fine_grain_element_combiantion(
            limit_list=limits,
            steel_plant='BAOSHAN IRON & STEEL CO., LTD.',
            strength='normal',
            include=['Al', 'Al+Nb', 'Al+Nb+Ti']
        )
        plate.delivery_condition.value = 'AR'
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='ThicknessLimit',
            limit_type=LimitType.RANGE,
            minimum=0,
            maximum=50
        )
        plate.thickness.value = 50
        limits = rule_maker.get_rules(plate)
        self.check_fine_grain_element_combiantion(
            limit_list=limits,
            steel_plant='BAOSHAN IRON & STEEL CO., LTD.',
            strength='normal',
            include=['Al+Ti']
        )
        plate.delivery_condition.value = 'TM'
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='ThicknessLimit',
            limit_type=LimitType.RANGE,
            minimum=0,
            maximum=100
        )
        plate.thickness.value = 100
        limits = rule_maker.get_rules(plate)
        self.check_fine_grain_element_combiantion(
            limit_list=limits,
            steel_plant='BAOSHAN IRON & STEEL CO., LTD.',
            strength='normal',
            include=['Al+Nb+Ti']
        )

    def test_vl_d(self, rule_maker: BaoSteelRuleMaker, plate: SteelPlate):
        plate.specification.value = 'VL D'
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='DeliveryConditionLimit',
            limit_type=LimitType.SCOPE,
            scope=['N', 'AR', 'TM']
        )
        plate.delivery_condition.value = 'AR'
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='ThicknessLimit',
            limit_type=LimitType.RANGE,
            minimum=0,
            maximum=35
        )
        plate.thickness.value = 35
        limits = rule_maker.get_rules(plate)
        self.check_fine_grain_element_combiantion(
            limit_list=limits,
            steel_plant='BAOSHAN IRON & STEEL CO., LTD.',
            strength='normal',
            include=['Al+Ti']
        )
        plate.delivery_condition.value = 'N'
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='ThicknessLimit',
            limit_type=LimitType.RANGE,
            maximum=80,
            minimum=0
        )
        plate.thickness.value = 35
        limits = rule_maker.get_rules(plate)
        self.check_fine_grain_element_combiantion(
            limit_list=limits,
            steel_plant='BAOSHAN IRON & STEEL CO., LTD.',
            strength='normal',
            include=['Al+Ti', 'Al+Nb', 'Al+Nb+Ti']
        )
        plate.thickness.value = 80
        limits = rule_maker.get_rules(plate)
        self.check_fine_grain_element_combiantion(
            limit_list=limits,
            steel_plant='BAOSHAN IRON & STEEL CO., LTD.',
            strength='normal',
            include=['Al+Nb', 'Al+Nb+Ti']
        )
        plate.delivery_condition.value = 'TM'
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='ThicknessLimit',
            limit_type=LimitType.RANGE,
            minimum=0,
            maximum=100
        )
        plate.thickness.value = 100
        limits = rule_maker.get_rules(plate)
        self.check_fine_grain_element_combiantion(
            limit_list=limits,
            steel_plant='BAOSHAN IRON & STEEL CO., LTD.',
            strength='normal',
            include=['Al+Nb+Ti']
        )

    def test_vl_e(self, rule_maker: BaoSteelRuleMaker, plate: SteelPlate):
        plate.specification.value = 'VL E'
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='DeliveryConditionLimit',
            limit_type=LimitType.SCOPE,
            scope=['N', 'TM']
        )
        plate.delivery_condition.value = 'N'
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='ThicknessLimit',
            limit_type=LimitType.RANGE,
            maximum=80,
            minimum=0
        )
        plate.thickness.value = 35
        limits = rule_maker.get_rules(plate)
        self.check_fine_grain_element_combiantion(
            limit_list=limits,
            steel_plant='BAOSHAN IRON & STEEL CO., LTD.',
            strength='normal',
            include=['Al+Ti', 'Al+Nb', 'Al+Nb+Ti']
        )
        plate.thickness.value = 80
        limits = rule_maker.get_rules(plate)
        self.check_fine_grain_element_combiantion(
            limit_list=limits,
            steel_plant='BAOSHAN IRON & STEEL CO., LTD.',
            strength='normal',
            include=['Al+Nb', 'Al+Nb+Ti']
        )
        plate.delivery_condition.value = 'TM'
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='ThicknessLimit',
            limit_type=LimitType.RANGE,
            minimum=0,
            maximum=100
        )
        plate.thickness.value = 100
        limits = rule_maker.get_rules(plate)
        self.check_fine_grain_element_combiantion(
            limit_list=limits,
            steel_plant='BAOSHAN IRON & STEEL CO., LTD.',
            strength='normal',
            include=['Al+Nb+Ti']
        )


class TestFineGrainElementHighStrengthSteel(BaseTester):

    def test_vl_a27s(self, rule_maker: BaoSteelRuleMaker, plate: SteelPlate):
        plate.specification.value = 'VL A27S'
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='DeliveryConditionLimit',
            limit_type=LimitType.SCOPE,
            scope=['AR', 'N', 'NR', 'TM']
        )
        plate.delivery_condition.value = 'AR'
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='ThicknessLimit',
            limit_type=LimitType.RANGE,
            minimum=0,
            maximum=20
        )
        plate.thickness.value = 20
        limits = rule_maker.get_rules(plate)
        self.check_fine_grain_element_combiantion(
            limit_list=limits,
            steel_plant='BAOSHAN IRON & STEEL CO., LTD.',
            strength='high',
            include=['Al+Ti']
        )
        plate.delivery_condition.value = 'N'
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='ThicknessLimit',
            limit_type=LimitType.RANGE,
            maximum=80,
            minimum=0
        )
        plate.thickness.value = 30
        limits = rule_maker.get_rules(plate)
        self.check_fine_grain_element_combiantion(
            limit_list=limits,
            steel_plant='BAOSHAN IRON & STEEL CO., LTD.',
            strength='high',
            include=['Al+Ti', 'Al+Nb+Ti']
        )
        plate.thickness.value = 80
        limits = rule_maker.get_rules(plate)
        self.check_fine_grain_element_combiantion(
            limit_list=limits,
            steel_plant='BAOSHAN IRON & STEEL CO., LTD.',
            strength='high',
            include=['Al+Nb+Ti']
        )
        plate.delivery_condition.value = 'NR'
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='ThicknessLimit',
            limit_type=LimitType.RANGE,
            minimum=0,
            maximum=40
        )
        plate.thickness.value = 30
        limits = rule_maker.get_rules(plate)
        self.check_fine_grain_element_combiantion(
            limit_list=limits,
            steel_plant='BAOSHAN IRON & STEEL CO., LTD.',
            strength='high',
            include=['Al+Ti', 'Al+Nb+Ti']
        )
        plate.thickness.value = 40
        limits = rule_maker.get_rules(plate)
        self.check_fine_grain_element_combiantion(
            limit_list=limits,
            steel_plant='BAOSHAN IRON & STEEL CO., LTD.',
            strength='high',
            include=['Al+Nb+Ti']
        )
        plate.delivery_condition.value = 'TM'
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='ThicknessLimit',
            limit_type=LimitType.RANGE,
            minimum=0,
            maximum=90
        )
        plate.thickness.value = 90
        limits = rule_maker.get_rules(plate)
        self.check_fine_grain_element_combiantion(
            limit_list=limits,
            steel_plant='BAOSHAN IRON & STEEL CO., LTD.',
            strength='high',
            include=['Al+Nb+Ti']
        )

    def test_vl_a32(self, rule_maker: BaoSteelRuleMaker, plate: SteelPlate):
        plate.specification.value = 'VL A32'
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='DeliveryConditionLimit',
            limit_type=LimitType.SCOPE,
            scope=['AR', 'N', 'NR', 'TM']
        )
        plate.delivery_condition.value = 'AR'
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='ThicknessLimit',
            limit_type=LimitType.RANGE,
            minimum=0,
            maximum=20
        )
        plate.thickness.value = 20
        limits = rule_maker.get_rules(plate)
        self.check_fine_grain_element_combiantion(
            limit_list=limits,
            steel_plant='BAOSHAN IRON & STEEL CO., LTD.',
            strength='high',
            include=['Al+Ti']
        )
        plate.delivery_condition.value = 'N'
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='ThicknessLimit',
            limit_type=LimitType.RANGE,
            maximum=80,
            minimum=0
        )
        plate.thickness.value = 30
        limits = rule_maker.get_rules(plate)
        self.check_fine_grain_element_combiantion(
            limit_list=limits,
            steel_plant='BAOSHAN IRON & STEEL CO., LTD.',
            strength='high',
            include=['Al+Ti', 'Al+Nb+Ti']
        )
        plate.thickness.value = 80
        limits = rule_maker.get_rules(plate)
        self.check_fine_grain_element_combiantion(
            limit_list=limits,
            steel_plant='BAOSHAN IRON & STEEL CO., LTD.',
            strength='high',
            include=['Al+Nb+Ti']
        )
        plate.delivery_condition.value = 'NR'
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='ThicknessLimit',
            limit_type=LimitType.RANGE,
            minimum=0,
            maximum=40
        )
        plate.thickness.value = 30
        limits = rule_maker.get_rules(plate)
        self.check_fine_grain_element_combiantion(
            limit_list=limits,
            steel_plant='BAOSHAN IRON & STEEL CO., LTD.',
            strength='high',
            include=['Al+Ti', 'Al+Nb+Ti']
        )
        plate.thickness.value = 40
        limits = rule_maker.get_rules(plate)
        self.check_fine_grain_element_combiantion(
            limit_list=limits,
            steel_plant='BAOSHAN IRON & STEEL CO., LTD.',
            strength='high',
            include=['Al+Nb+Ti']
        )
        plate.delivery_condition.value = 'TM'
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='ThicknessLimit',
            limit_type=LimitType.RANGE,
            minimum=0,
            maximum=90
        )
        plate.thickness.value = 50
        limits = rule_maker.get_rules(plate)
        self.check_fine_grain_element_combiantion(
            limit_list=limits,
            steel_plant='BAOSHAN IRON & STEEL CO., LTD.',
            strength='high',
            include=['Al+Ti', 'Al+Nb+Ti']
        )
        plate.thickness.value = 90
        limits = rule_maker.get_rules(plate)
        self.check_fine_grain_element_combiantion(
            limit_list=limits,
            steel_plant='BAOSHAN IRON & STEEL CO., LTD.',
            strength='high',
            include=['Al+Nb+Ti']
        )

    def test_vl_a36(self, rule_maker: BaoSteelRuleMaker, plate: SteelPlate):
        plate.specification.value = 'VL A36'
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='DeliveryConditionLimit',
            limit_type=LimitType.SCOPE,
            scope=['AR', 'N', 'NR', 'TM']
        )
        plate.delivery_condition.value = 'AR'
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='ThicknessLimit',
            limit_type=LimitType.RANGE,
            minimum=0,
            maximum=20
        )
        plate.thickness.value = 20
        limits = rule_maker.get_rules(plate)
        self.check_fine_grain_element_combiantion(
            limit_list=limits,
            steel_plant='BAOSHAN IRON & STEEL CO., LTD.',
            strength='high',
            include=['Al+Ti']
        )
        plate.delivery_condition.value = 'NR'
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='ThicknessLimit',
            limit_type=LimitType.RANGE,
            minimum=0,
            maximum=40
        )
        plate.thickness.value = 30
        limits = rule_maker.get_rules(plate)
        self.check_fine_grain_element_combiantion(
            limit_list=limits,
            steel_plant='BAOSHAN IRON & STEEL CO., LTD.',
            strength='high',
            include=['Al+Ti', 'Al+Nb+Ti']
        )
        plate.thickness.value = 40
        limits = rule_maker.get_rules(plate)
        self.check_fine_grain_element_combiantion(
            limit_list=limits,
            steel_plant='BAOSHAN IRON & STEEL CO., LTD.',
            strength='high',
            include=['Al+Nb+Ti']
        )
        plate.delivery_condition.value = 'N'
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='ThicknessLimit',
            limit_type=LimitType.RANGE,
            maximum=80,
            minimum=0
        )
        plate.thickness.value = 80
        limits = rule_maker.get_rules(plate)
        self.check_fine_grain_element_combiantion(
            limit_list=limits,
            steel_plant='BAOSHAN IRON & STEEL CO., LTD.',
            strength='high',
            include=['Al+Nb+Ti']
        )
        plate.delivery_condition.value = 'TM'
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='ThicknessLimit',
            limit_type=LimitType.RANGE,
            minimum=0,
            maximum=90
        )
        plate.thickness.value = 50
        limits = rule_maker.get_rules(plate)
        self.check_fine_grain_element_combiantion(
            limit_list=limits,
            steel_plant='BAOSHAN IRON & STEEL CO., LTD.',
            strength='high',
            include=['Al+Ti', 'Al+Nb+Ti']
        )
        plate.thickness.value = 90
        limits = rule_maker.get_rules(plate)
        self.check_fine_grain_element_combiantion(
            limit_list=limits,
            steel_plant='BAOSHAN IRON & STEEL CO., LTD.',
            strength='high',
            include=['Al+Nb+Ti']
        )

    def test_vl_a40(self, rule_maker: BaoSteelRuleMaker, plate: SteelPlate):
        plate.specification.value = 'VL A40'
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='DeliveryConditionLimit',
            limit_type=LimitType.SCOPE,
            scope=['TM']
        )
        plate.delivery_condition.value = 'TM'
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='ThicknessLimit',
            limit_type=LimitType.RANGE,
            minimum=0,
            maximum=90
        )
        plate.thickness.value = 90
        limits = rule_maker.get_rules(plate)
        self.check_fine_grain_element_combiantion(
            limit_list=limits,
            steel_plant='BAOSHAN IRON & STEEL CO., LTD.',
            strength='high',
            include=['Al+Nb+Ti']
        )

    def test_vl_d27s(self, rule_maker: BaoSteelRuleMaker, plate: SteelPlate):
        plate.specification.value = 'VL D27S'
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='DeliveryConditionLimit',
            limit_type=LimitType.SCOPE,
            scope=['AR', 'N', 'NR', 'TM']
        )
        plate.delivery_condition.value = 'AR'
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='ThicknessLimit',
            limit_type=LimitType.RANGE,
            minimum=0,
            maximum=20
        )
        plate.thickness.value = 20
        limits = rule_maker.get_rules(plate)
        self.check_fine_grain_element_combiantion(
            limit_list=limits,
            steel_plant='BAOSHAN IRON & STEEL CO., LTD.',
            strength='high',
            include=['Al+Ti']
        )
        plate.delivery_condition.value = 'NR'
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='ThicknessLimit',
            limit_type=LimitType.RANGE,
            minimum=0,
            maximum=40
        )
        plate.thickness.value = 40
        limits = rule_maker.get_rules(plate)
        self.check_fine_grain_element_combiantion(
            limit_list=limits,
            steel_plant='BAOSHAN IRON & STEEL CO., LTD.',
            strength='high',
            include=['Al+Nb+Ti']
        )
        plate.delivery_condition.value = 'N'
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='ThicknessLimit',
            limit_type=LimitType.RANGE,
            maximum=80,
            minimum=0
        )
        plate.thickness.value = 30
        limits = rule_maker.get_rules(plate)
        self.check_fine_grain_element_combiantion(
            limit_list=limits,
            steel_plant='BAOSHAN IRON & STEEL CO., LTD.',
            strength='high',
            include=['Al+Ti', 'Al+Nb+Ti']
        )
        plate.thickness.value = 80
        limits = rule_maker.get_rules(plate)
        self.check_fine_grain_element_combiantion(
            limit_list=limits,
            steel_plant='BAOSHAN IRON & STEEL CO., LTD.',
            strength='high',
            include=['Al+Nb+Ti']
        )
        plate.delivery_condition.value = 'TM'
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='ThicknessLimit',
            limit_type=LimitType.RANGE,
            minimum=0,
            maximum=90
        )
        plate.thickness.value = 90
        limits = rule_maker.get_rules(plate)
        self.check_fine_grain_element_combiantion(
            limit_list=limits,
            steel_plant='BAOSHAN IRON & STEEL CO., LTD.',
            strength='high',
            include=['Al+Nb+Ti']
        )

    def test_vl_d32(self, rule_maker: BaoSteelRuleMaker, plate: SteelPlate):
        plate.specification.value = 'VL D32'
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='DeliveryConditionLimit',
            limit_type=LimitType.SCOPE,
            scope=['AR', 'N', 'NR', 'TM']
        )
        plate.delivery_condition.value = 'AR'
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='ThicknessLimit',
            limit_type=LimitType.RANGE,
            minimum=0,
            maximum=20
        )
        plate.thickness.value = 20
        limits = rule_maker.get_rules(plate)
        self.check_fine_grain_element_combiantion(
            limit_list=limits,
            steel_plant='BAOSHAN IRON & STEEL CO., LTD.',
            strength='high',
            include=['Al+Ti']
        )
        plate.delivery_condition.value = 'N'
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='ThicknessLimit',
            limit_type=LimitType.RANGE,
            maximum=80,
            minimum=0
        )
        plate.thickness.value = 30
        limits = rule_maker.get_rules(plate)
        self.check_fine_grain_element_combiantion(
            limit_list=limits,
            steel_plant='BAOSHAN IRON & STEEL CO., LTD.',
            strength='high',
            include=['Al+Ti', 'Al+Nb+Ti']
        )
        plate.thickness.value = 80
        limits = rule_maker.get_rules(plate)
        self.check_fine_grain_element_combiantion(
            limit_list=limits,
            steel_plant='BAOSHAN IRON & STEEL CO., LTD.',
            strength='high',
            include=['Al+Nb+Ti']
        )
        plate.delivery_condition.value = 'NR'
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='ThicknessLimit',
            limit_type=LimitType.RANGE,
            minimum=0,
            maximum=40
        )
        plate.thickness.value = 40
        limits = rule_maker.get_rules(plate)
        self.check_fine_grain_element_combiantion(
            limit_list=limits,
            steel_plant='BAOSHAN IRON & STEEL CO., LTD.',
            strength='high',
            include=['Al+Nb+Ti']
        )
        plate.delivery_condition.value = 'TM'
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='ThicknessLimit',
            limit_type=LimitType.RANGE,
            minimum=0,
            maximum=90
        )
        plate.thickness.value = 50
        limits = rule_maker.get_rules(plate)
        self.check_fine_grain_element_combiantion(
            limit_list=limits,
            steel_plant='BAOSHAN IRON & STEEL CO., LTD.',
            strength='high',
            include=['Al+Ti', 'Al+Nb+Ti']
        )
        plate.thickness.value = 90
        limits = rule_maker.get_rules(plate)
        self.check_fine_grain_element_combiantion(
            limit_list=limits,
            steel_plant='BAOSHAN IRON & STEEL CO., LTD.',
            strength='high',
            include=['Al+Nb+Ti']
        )

    def test_vl_d36(self, rule_maker: BaoSteelRuleMaker, plate: SteelPlate):
        plate.specification.value = 'VL D36'
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='DeliveryConditionLimit',
            limit_type=LimitType.SCOPE,
            scope=['AR', 'N', 'NR', 'TM']
        )
        plate.delivery_condition.value = 'AR'
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='ThicknessLimit',
            limit_type=LimitType.RANGE,
            minimum=0,
            maximum=20
        )
        plate.thickness.value = 20
        limits = rule_maker.get_rules(plate)
        self.check_fine_grain_element_combiantion(
            limit_list=limits,
            steel_plant='BAOSHAN IRON & STEEL CO., LTD.',
            strength='high',
            include=['Al+Ti']
        )
        plate.delivery_condition.value = 'N'
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='ThicknessLimit',
            limit_type=LimitType.RANGE,
            maximum=80,
            minimum=0
        )
        plate.thickness.value = 80
        limits = rule_maker.get_rules(plate)
        self.check_fine_grain_element_combiantion(
            limit_list=limits,
            steel_plant='BAOSHAN IRON & STEEL CO., LTD.',
            strength='high',
            include=['Al+Nb+Ti']
        )
        plate.delivery_condition.value = 'NR'
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='ThicknessLimit',
            limit_type=LimitType.RANGE,
            minimum=0,
            maximum=40
        )
        plate.thickness.value = 40
        limits = rule_maker.get_rules(plate)
        self.check_fine_grain_element_combiantion(
            limit_list=limits,
            steel_plant='BAOSHAN IRON & STEEL CO., LTD.',
            strength='high',
            include=['Al+Nb+Ti']
        )
        plate.delivery_condition.value = 'TM'
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='ThicknessLimit',
            limit_type=LimitType.RANGE,
            minimum=0,
            maximum=90
        )
        plate.thickness.value = 50
        limits = rule_maker.get_rules(plate)
        self.check_fine_grain_element_combiantion(
            limit_list=limits,
            steel_plant='BAOSHAN IRON & STEEL CO., LTD.',
            strength='high',
            include=['Al+Ti', 'Al+Nb+Ti']
        )
        plate.thickness.value = 90
        limits = rule_maker.get_rules(plate)
        self.check_fine_grain_element_combiantion(
            limit_list=limits,
            steel_plant='BAOSHAN IRON & STEEL CO., LTD.',
            strength='high',
            include=['Al+Nb+Ti']
        )

    def test_vl_d40(self, rule_maker: BaoSteelRuleMaker, plate: SteelPlate):
        plate.specification.value = 'VL D40'
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='DeliveryConditionLimit',
            limit_type=LimitType.SCOPE,
            scope=['TM']
        )
        plate.delivery_condition.value = 'TM'
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='ThicknessLimit',
            limit_type=LimitType.RANGE,
            minimum=0,
            maximum=90
        )
        plate.thickness.value = 90
        limits = rule_maker.get_rules(plate)
        self.check_fine_grain_element_combiantion(
            limit_list=limits,
            steel_plant='BAOSHAN IRON & STEEL CO., LTD.',
            strength='high',
            include=['Al+Nb+Ti']
        )

    def test_vl_e27s(self, rule_maker: BaoSteelRuleMaker, plate: SteelPlate):
        plate.specification.value = 'VL E27S'
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='DeliveryConditionLimit',
            limit_type=LimitType.SCOPE,
            scope=['N', 'TM']
        )
        plate.delivery_condition.value = 'N'
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='ThicknessLimit',
            limit_type=LimitType.RANGE,
            maximum=80,
            minimum=0
        )
        plate.thickness.value = 80
        limits = rule_maker.get_rules(plate)
        self.check_fine_grain_element_combiantion(
            limit_list=limits,
            steel_plant='BAOSHAN IRON & STEEL CO., LTD.',
            strength='high',
            include=['Al+Nb+Ti']
        )
        plate.delivery_condition.value = 'TM'
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='ThicknessLimit',
            limit_type=LimitType.RANGE,
            minimum=0,
            maximum=90
        )
        plate.thickness.value = 90
        limits = rule_maker.get_rules(plate)
        self.check_fine_grain_element_combiantion(
            limit_list=limits,
            steel_plant='BAOSHAN IRON & STEEL CO., LTD.',
            strength='high',
            include=['Al+Nb+Ti']
        )

    def test_vl_e32(self, rule_maker: BaoSteelRuleMaker, plate: SteelPlate):
        plate.specification.value = 'VL E32'
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='DeliveryConditionLimit',
            limit_type=LimitType.SCOPE,
            scope=['N', 'TM']
        )
        plate.delivery_condition.value = 'N'
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='ThicknessLimit',
            limit_type=LimitType.RANGE,
            maximum=80,
            minimum=0
        )
        plate.thickness.value = 80
        limits = rule_maker.get_rules(plate)
        self.check_fine_grain_element_combiantion(
            limit_list=limits,
            steel_plant='BAOSHAN IRON & STEEL CO., LTD.',
            strength='high',
            include=['Al+Nb+Ti']
        )
        plate.delivery_condition.value = 'TM'
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='ThicknessLimit',
            limit_type=LimitType.RANGE,
            minimum=0,
            maximum=90
        )
        plate.thickness.value = 50
        limits = rule_maker.get_rules(plate)
        self.check_fine_grain_element_combiantion(
            limit_list=limits,
            steel_plant='BAOSHAN IRON & STEEL CO., LTD.',
            strength='high',
            include=['Al+Ti', 'Al+Nb+Ti']
        )
        plate.thickness.value = 90
        limits = rule_maker.get_rules(plate)
        self.check_fine_grain_element_combiantion(
            limit_list=limits,
            steel_plant='BAOSHAN IRON & STEEL CO., LTD.',
            strength='high',
            include=['Al+Nb+Ti']
        )

    def test_vl_e36(self, rule_maker: BaoSteelRuleMaker, plate: SteelPlate):
        plate.specification.value = 'VL E36'
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='DeliveryConditionLimit',
            limit_type=LimitType.SCOPE,
            scope=['N', 'TM']
        )
        plate.delivery_condition.value = 'N'
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='ThicknessLimit',
            limit_type=LimitType.RANGE,
            maximum=80,
            minimum=0
        )
        plate.thickness.value = 80
        limits = rule_maker.get_rules(plate)
        self.check_fine_grain_element_combiantion(
            limit_list=limits,
            steel_plant='BAOSHAN IRON & STEEL CO., LTD.',
            strength='high',
            include=['Al+Nb+Ti']
        )
        plate.delivery_condition.value = 'TM'
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='ThicknessLimit',
            limit_type=LimitType.RANGE,
            minimum=0,
            maximum=90
        )
        plate.thickness.value = 50
        limits = rule_maker.get_rules(plate)
        self.check_fine_grain_element_combiantion(
            limit_list=limits,
            steel_plant='BAOSHAN IRON & STEEL CO., LTD.',
            strength='high',
            include=['Al+Ti', 'Al+Nb+Ti']
        )
        plate.thickness.value = 90
        limits = rule_maker.get_rules(plate)
        self.check_fine_grain_element_combiantion(
            limit_list=limits,
            steel_plant='BAOSHAN IRON & STEEL CO., LTD.',
            strength='high',
            include=['Al+Nb+Ti']
        )

    def test_vl_e40(self, rule_maker: BaoSteelRuleMaker, plate: SteelPlate):
        plate.specification.value = 'VL E40'
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='DeliveryConditionLimit',
            limit_type=LimitType.SCOPE,
            scope=['TM']
        )
        plate.delivery_condition.value = 'TM'
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='ThicknessLimit',
            limit_type=LimitType.RANGE,
            minimum=0,
            maximum=90
        )
        plate.thickness.value = 90
        limits = rule_maker.get_rules(plate)
        self.check_fine_grain_element_combiantion(
            limit_list=limits,
            steel_plant='BAOSHAN IRON & STEEL CO., LTD.',
            strength='high',
            include=['Al+Nb+Ti']
        )

    def test_vl_f27s(self, rule_maker: BaoSteelRuleMaker, plate: SteelPlate):
        plate.specification.value = 'VL F27S'
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='DeliveryConditionLimit',
            limit_type=LimitType.SCOPE,
            scope=['TM']
        )
        plate.delivery_condition.value = 'TM'
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='ThicknessLimit',
            limit_type=LimitType.RANGE,
            minimum=0,
            maximum=68
        )
        plate.thickness.value = 68
        limits = rule_maker.get_rules(plate)
        self.check_fine_grain_element_combiantion(
            limit_list=limits,
            steel_plant='BAOSHAN IRON & STEEL CO., LTD.',
            strength='high',
            include=['Al+Nb+Ti']
        )

    def test_vl_f32(self, rule_maker: BaoSteelRuleMaker, plate: SteelPlate):
        plate.specification.value = 'VL F32'
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='DeliveryConditionLimit',
            limit_type=LimitType.SCOPE,
            scope=['TM']
        )
        plate.delivery_condition.value = 'TM'
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='ThicknessLimit',
            limit_type=LimitType.RANGE,
            minimum=0,
            maximum=68
        )
        plate.thickness.value = 68
        limits = rule_maker.get_rules(plate)
        self.check_fine_grain_element_combiantion(
            limit_list=limits,
            steel_plant='BAOSHAN IRON & STEEL CO., LTD.',
            strength='high',
            include=['Al+Nb+Ti']
        )

    def test_vl_f36(self, rule_maker: BaoSteelRuleMaker, plate: SteelPlate):
        plate.specification.value = 'VL F36'
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='DeliveryConditionLimit',
            limit_type=LimitType.SCOPE,
            scope=['TM']
        )
        plate.delivery_condition.value = 'TM'
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='ThicknessLimit',
            limit_type=LimitType.RANGE,
            minimum=0,
            maximum=68
        )
        plate.thickness.value = 68
        limits = rule_maker.get_rules(plate)
        self.check_fine_grain_element_combiantion(
            limit_list=limits,
            steel_plant='BAOSHAN IRON & STEEL CO., LTD.',
            strength='high',
            include=['Al+Nb+Ti']
        )

    def test_vl_f40(self, rule_maker: BaoSteelRuleMaker, plate: SteelPlate):
        plate.specification.value = 'VL F40'
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='DeliveryConditionLimit',
            limit_type=LimitType.SCOPE,
            scope=['TM']
        )
        plate.delivery_condition.value = 'TM'
        limits = rule_maker.get_rules(plate)
        self.get_limit(
            limit_list=limits,
            limit_class='ThicknessLimit',
            limit_type=LimitType.RANGE,
            minimum=0,
            maximum=68
        )
        plate.thickness.value = 68
        limits = rule_maker.get_rules(plate)
        self.check_fine_grain_element_combiantion(
            limit_list=limits,
            steel_plant='BAOSHAN IRON & STEEL CO., LTD.',
            strength='high',
            include=['Al+Nb+Ti']
        )
