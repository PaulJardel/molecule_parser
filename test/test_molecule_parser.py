import pytest

from molecular.molecule_parser import MoleculeParser


def test__is_valid_parenthesis():
    # Given
    water = 'H2O'
    expected_water = True

    magnesium_hydroxide = 'Mg(OH)2'
    expected_magnesium_hydroxide = True

    fremy_salt = 'K4[ON(SO3)2]2'
    expected_fremy_salt = True

    wrong_format_molecule_1  = "H(O"
    expected_wrong_format_molecule_1 = False

    wrong_format_molecule_2  = "(Mg3[T)]"
    expected_wrong_format_molecule_2 = False

    # When
    molecule_parser = MoleculeParser()
    result_water = molecule_parser._is_valid_parenthesis(molecule=water)
    result_magnesium_hydroxide = molecule_parser._is_valid_parenthesis(molecule=magnesium_hydroxide)
    result_fremy_salt = molecule_parser._is_valid_parenthesis(molecule=fremy_salt)
    result_wrong_format_molecule_1 = molecule_parser._is_valid_parenthesis(molecule=wrong_format_molecule_1)
    result_wrong_format_molecule_2 = molecule_parser._is_valid_parenthesis(molecule=wrong_format_molecule_2)

    # Then
    assert result_water == expected_water
    assert result_magnesium_hydroxide == expected_magnesium_hydroxide
    assert result_fremy_salt == expected_fremy_salt
    assert result_wrong_format_molecule_1 == expected_wrong_format_molecule_1
    assert result_wrong_format_molecule_2 == expected_wrong_format_molecule_2
