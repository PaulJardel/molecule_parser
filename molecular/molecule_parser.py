from typing import Dict
import re

from molecular.monitoring.log import get_logger

logger = get_logger()


class MoleculeParser:
    """
    This class allows to parse molecules, and get the number of atoms that compose it.

    It is mainly string operations.
    See documentation used : https://docs.python.org/3/library/stdtypes.html
    """

    def get_list_molecules_elements(self, molecule: str) -> Dict[str, int]:
        """
        This method returns the list of molecule elements.
        A molecule element can be :
        - atom_name : an atom can be composed of 1 letter uppercase, or 1 letter uppercase + 1 letter lowercase
        - atom_multiplier : the multiplier linked to the atom. For example : 'H(S4[SO]3)2', atom multipler of S = 4.
        - parenthesis : can be one of the following : "(", ")", "[", "]", "{", "}"
        - parenthesis_multiplier : multiplified amount of all current surrounding parenthesis
        :param molecule: the molecule to analyse
        :return: the list of molecule elements, composing the molecule
        """
        return re.findall(r'[A-Z][a-z]?|[()\[\]{}]|[0-9]', molecule)

    def parse_molecule(self, molecule: str) -> Dict[str, int]:

        logger.info(f"Molecule : '{molecule}'")

        # get list of molecule elements
        list_molecules_elements = self.get_list_molecules_elements(molecule=molecule)
        logger.info(f'list_molecules_elements = {list_molecules_elements}')

        atoms_dict = self.parse_group(reversed(list_molecules_elements), {})
        logger.info(f"Dictionary of atoms for '{molecule}' : {atoms_dict}\n")

        return atoms_dict

    def parse_group(self, list_molecules_elements, atoms_dict, parenthesis_multiplier=1):
        _parenthesis_multiplier = parenthesis_multiplier
        starting_parenthesis_char = {"(", "{", "["}
        closing_parenthesis_char = {")", "}", "]"}
        for molecule_element in list_molecules_elements:

            # entering a parenthesis : we use the parenthesis_multiplier
            if molecule_element in closing_parenthesis_char:
                self.parse_group(
                    list_molecules_elements=list_molecules_elements,
                    atoms_dict=atoms_dict,
                    parenthesis_multiplier=_parenthesis_multiplier)
            # exiting a parenthesis : we do not use the parenthesis_multiplier anymore
            elif molecule_element in starting_parenthesis_char:
                break
            elif molecule_element.isdecimal():
                _parenthesis_multiplier = parenthesis_multiplier * int(molecule_element)
                continue
            elif molecule_element.isalpha():
                atoms_dict[molecule_element] = atoms_dict.get(molecule_element, 0) + _parenthesis_multiplier
            _parenthesis_multiplier = parenthesis_multiplier
        return atoms_dict


if __name__ == '__main__':
    molecule_parser = MoleculeParser()

    wrong_format_molecule = '(Mg3[T)]'
    atoms_dict = molecule_parser.parse_molecule(molecule=wrong_format_molecule)

    water = 'H2O'
    atoms_dict = molecule_parser.parse_molecule(molecule=water)

    magnesium_hydroxide = '(Mg3[T2(Y)](OH)2)'
    atoms_dict = molecule_parser.parse_molecule(molecule=magnesium_hydroxide)

    fremy_salt = 'K4[ON(SO3)2]2'
    atoms_dict = molecule_parser.parse_molecule(molecule=fremy_salt)
