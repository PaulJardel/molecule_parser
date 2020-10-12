from molecular.molecule_parser import MoleculeParser


def test__is_valid_parenthesis():
    # Given
    water = 'H2O'
    expected_water = True

    magnesium_hydroxide = 'Mg(OH)2'
    expected_magnesium_hydroxide = True

    fremy_salt = 'K4[ON(SO3)2]2'
    expected_fremy_salt = True

    wrong_format_molecule_1 = "H(O"
    expected_wrong_format_molecule_1 = False

    wrong_format_molecule_2 = "(Mg3[T)]"
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


def test_get_list_molecules_elements():
    # Given
    water = 'H2O'
    expected_water = ['H', '2', 'O']

    magnesium_hydroxide = 'Mg(OH)2'
    expected_magnesium_hydroxide = ['Mg', '(', 'O', 'H', ')', '2']

    fremy_salt = 'K4[ON(SO3)2]2'
    expected_fremy_salt = ['K', '4', '[', 'O', 'N', '(', 'S', 'O', '3', ')', '2', ']', '2']

    # When
    molecule_parser = MoleculeParser()
    result_water = molecule_parser.get_list_molecules_elements(molecule=water)
    result_magnesium_hydroxide = molecule_parser.get_list_molecules_elements(molecule=magnesium_hydroxide)
    result_fremy_salt = molecule_parser.get_list_molecules_elements(molecule=fremy_salt)

    # Then
    assert result_water == expected_water
    assert result_magnesium_hydroxide == expected_magnesium_hydroxide
    assert result_fremy_salt == expected_fremy_salt


def test_parse_group():
    # Given
    list_water = ['H', '2', 'O']
    expected_water = {'O': 1, 'H': 2}

    list_magnesium_hydroxide = ['Mg', '(', 'O', 'H', ')', '2']
    expected_magnesium_hydroxide = {'H': 2, 'O': 2, 'Mg': 1}

    list_fremy_salt = ['K', '4', '[', 'O', 'N', '(', 'S', 'O', '3', ')', '2', ']', '2']
    expected_fremy_salt = {'O': 14, 'S': 4, 'N': 2, 'K': 4}

    # When
    molecule_parser = MoleculeParser()
    result_water = molecule_parser.parse_group(list_molecules_elements=reversed(list_water), atoms_dict={})
    result_magnesium_hydroxide = molecule_parser.parse_group(list_molecules_elements=reversed(list_magnesium_hydroxide), atoms_dict={})
    result_fremy_salt = molecule_parser.parse_group(list_molecules_elements=reversed(list_fremy_salt), atoms_dict={})

    # Then
    assert result_water == expected_water
    assert result_magnesium_hydroxide == expected_magnesium_hydroxide
    assert result_fremy_salt == expected_fremy_salt
