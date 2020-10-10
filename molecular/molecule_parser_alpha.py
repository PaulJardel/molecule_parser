from typing import Dict

from molecular.monitoring.log import get_logger

logger = get_logger()

class MoleculeParserAlpha:
    """
    This class allows to parse molecules, and get the number of atoms that compose it.

    It is mainly string operations.
    See documentation used : https://docs.python.org/3/library/stdtypes.html
    """

    tag_dict = {
        "A": 1,
        "B": 2,
        "C": 3,
        "D": 4,
        "E": 5
    }


    def parse_molecule(self, molecule: str) -> Dict[str, int]:

        # check if the molecule has a valid format for parenthesis
        if not self._is_valid_parenthesis(molecule=molecule):
            logger.info(f"Molecule '{molecule}' has not a valid format.")
            return None

        atoms_dict = {}
        parenthesis_char = {"(", ")", "{", "}", "[", "]"}
        for index, character in enumerate(molecule):
            # checking all characters until last one
            if index < len(molecule)-1:

                # pass lowercase
                if character.islower():
                    if molecule[index+1].isdigit():
                        atom_multiplier = molecule[index+1].isdigit()
                    else:
                        atom_multiplier = 1
                    continue

                # pass digit
                if character.isdigit():
                    continue

                # pass parenthesis
                if character in parenthesis_char:
                    continue

                # get atom name
                atom = self._get_atom(character=molecule[index], character_next=molecule[index+1])

                # get atom multiplier (= multiplier is the digit just after the atom name)
                atom_multiplier = 1
                # get atom multiplier for atoms with 1 char (for example O2 : multiplier = 2)
                if(len(atom)==1 and molecule[index+1].isdigit()):
                    atom_multiplier = int(molecule[index+1])
                # get atom multiplier for atoms with 2 char (for example Mg3 : multiplier = 3)
                if(len(atom)==2 and index<len(molecule)-2 and molecule[index+2].isdigit()):
                    atom_multiplier = int(molecule[index+2])

                # get parenthesis multiplier (= multiplier of all surrounding parenthesis)
                parenthesis_multiplier = self._get_parenthesis_multiplier(molecule=molecule, current_index=index)
                
                logger.info(f'atom = {atom} / atom_multiplier = {atom_multiplier} / parenthesis_multiplier = {parenthesis_multiplier}')

                # add/update atom on atom dictionary, with the good amount of atoms
                if atom in atoms_dict:
                    count_atom = atoms_dict[atom]
                else:
                    count_atom = 1
                atoms_dict[atom] = count_atom * atom_multiplier * parenthesis_multiplier
                
            # checking last character : we take into account only if it is an atom
            else:
                logger.info(f'last character = {index} {character} {molecule[index]}')
                if character not in parenthesis_char and not character.islower() and not character.isdigit():
                    atom = molecule[index]
                    if atom in atoms_dict:
                        count_atom = atoms_dict[atom]
                    else:
                        count_atom = 1
                    atoms_dict[atom] = count_atom
        
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

    def _get_atom(self, character: str, character_next: str) -> str:
        """
        This method returns the current atom from the molecule string
        :param character: the current character to analyse
        :param character_next: the next character to analyse, used to check for atoms with lower letter
        :return: the name of the atom
        """
        if character.isupper() and character_next.islower():
            return f"{character}{character_next}"
        else:
            return character

    def _get_parenthesis_multiplier(self, molecule=str, current_index=int) -> int:
        """
        This method returns the parenthesis multipler.
        It will check for all current surrounding parenthesis, and return the miltiplified amount.
        For example : H(S4[SO]3)2 will return, for 'S' : 3*2.
        Here, we do not check for the "atom multiplier" (4 on the example)
        :param molecule: the molecule to analyse
        :param index: the current index on the main process analysis
        :return: the name of the atom
        """
        parenthesis_multiplier = 1
        closing_parenthesis_char = {")", "}", "]"}
        end_molecule = molecule[current_index:len(molecule)]
        logger.info(f"end_molecule = {end_molecule}")
        for index, character in enumerate(end_molecule):
            # checking all characters until last one
            if index < len(end_molecule)-1:
                logger.info(f"character = {character} next = {end_molecule[index+1]}")
                if character in closing_parenthesis_char and end_molecule[index+1].isdigit():
                    logger.info(f"************ {character}  --- {parenthesis_multiplier} * {end_molecule[index+1]}")
                    parenthesis_multiplier = parenthesis_multiplier * int(end_molecule[index+1])
        return parenthesis_multiplier


if __name__ == '__main__':
    molecule_parser = MoleculeParser()

    wrong_format_molecule  = '(Mg3[T)]'
    atoms_dict = molecule_parser.parse_molecule(molecule=wrong_format_molecule)

    water = 'H2O'
    atoms_dict = molecule_parser.parse_molecule(molecule=water)

    magnesium_hydroxide  = '(Mg3[T2(Y)](OH)2)'
    atoms_dict = molecule_parser.parse_molecule(molecule=magnesium_hydroxide)

    fremy_salt = 'K4[ON(SO3)2]2'
    atoms_dict = molecule_parser.parse_molecule(molecule=fremy_salt)
