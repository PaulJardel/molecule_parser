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

    def parse_molecule(self, molecule: str) -> Dict[str, int]:
        """
        This method returns the dictionary of atoms for a specified molecule.
        :param molecule: the molecule to parse
        :return: the dictionary of atoms, containing the amount for each atom
        """
        logger.info(f"Molecule : '{molecule}'")

        # check if the molecule has a valid format for parenthesis
        if not self._is_valid_parenthesis(molecule=molecule):
            logger.info(f"Molecule '{molecule}' has not a valid format.\n")
            return None

        # get list of molecule elements
        list_molecules_elements = self.get_list_molecules_elements(molecule=molecule)
        logger.info(f'list_molecules_elements = {list_molecules_elements}')

        # recursively parse each molecule element, counting them, using parenthesis_multiplier
        atoms_dict = self.parse_group(list_molecules_elements=reversed(list_molecules_elements), atoms_dict={})
        logger.info(f"Dictionary of atoms for '{molecule}' : {atoms_dict}\n")

        return atoms_dict

    def _is_valid_parenthesis(self, molecule: str) -> bool:
        """
        This method ensures the validity of the number of parenthesis opening / closing.
        For the second part of the function, it was inspired by :
        https://www.w3resource.com/python-exercises/class-exercises/python-class-exercise-3.php
        https://docs.python.org/3/tutorial/datastructures.html
        :param molecule: the molecule to analyse
        :return: True if the parenthesis are valid (opened / closed for each one, on the good order)
        """
        only_parenthesis = ''
        parenthesis_char = {"(", ")", "{", "}", "[", "]"}
        for character in molecule:
            if character in parenthesis_char:
                only_parenthesis += character

        stack = []
        parenthesis_opposites = {"(": ")", "{": "}", "[": "]"}
        for parenthese in only_parenthesis:
            if parenthese in parenthesis_opposites:
                stack.append(parenthese)
            elif len(stack) == 0 or parenthesis_opposites[stack.pop()] != parenthese:
                return False
        return len(stack) == 0

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

    def parse_group(self, list_molecules_elements, atoms_dict, parenthesis_multiplier=1):
        """
        This method returns the updated dictionary of atoms for a specified molecule.
        Here we handle the mulitplier of atoms, defined by the parenthesis.
        The recursiveness of this method allows to multiply the parenthesis_multiplier at each parenthesis.
        We 'read' the molecule from right to left, so that we catch the multiplier first. Easier fot calculation.
        :param list_molecules_elements: the molecule, parsed by molecule elements
        :param atoms_dict: the dictionary of atoms to construct / return
        :param parenthesis_multiplier: the parenthesis_multiplier, which evolve at each opened/closed parenthesis
        :return: the dictionary of atoms, containing the amount for each atom
        """
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

    magnesium_hydroxide = 'Mg(OH)2'
    atoms_dict = molecule_parser.parse_molecule(molecule=magnesium_hydroxide)

    fremy_salt = 'K4[ON(SO3)2]2'
    atoms_dict = molecule_parser.parse_molecule(molecule=fremy_salt)
