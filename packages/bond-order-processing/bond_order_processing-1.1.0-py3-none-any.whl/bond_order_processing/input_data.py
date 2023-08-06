__docformat__ = "google"
"""Input data module."""
from abc import ABC
from abc import abstractmethod
import re
from dataclasses import dataclass
from math import degrees
from math import acos
from enum import Enum
import numpy as np
from numpy.typing import NDArray
from typing import TypeAlias
from typing import Optional


x: TypeAlias = float
"""x-cartesian coordinate"""
y: TypeAlias = float
"""y-cartesian coordinate"""
z: TypeAlias = float
"""z-cartesian coordinate"""
vector: TypeAlias = tuple[x, y, z]
"""euclidean vector"""
deg: TypeAlias = float
"""angle in degrees"""


class LoadedData(Enum):
    """Enumeration used by **InputDataFromCPMD**."""
    UnitCell = 1
    MayerBondOrders = 2
    Populations = 3
    CoordinatesOfAtoms = 4


class Constants:
    """This class holds constants used in calculations in module
    **input_data**."""
    _CONSTANT_TO_CALCULATE_ANGSTROMS_FROM_BOHR: float = 0.52917720859
    """The length of the bohr radius in angstroms."""


@dataclass
class UnitCell(Constants):
    """Unit cell.

    Object represent unit cell.

    Attributes:
        a (float): Angstroms
        b (float): Angstroms
        c (float): Angstroms
        lattice_vectors (tuple[vector]): Table represents lattice vectors.
        alfa (deg): deg
        beta (deg): deg
        gamma (deg): deg

    """

    lattice_vectors: tuple[vector] | tuple = ()
    converted_to_angstroms: bool = False

    a: float = 0
    b: float = 0
    c: float = 0

    alfa: deg = 0
    beta: deg = 0
    gamma: deg = 0

    def calculate_edges_lengths(self) -> tuple[x, y, z] | None:
        """Calculate edge lengths

        Example:
        >>> unit_cell = UnitCell()
        >>> unit_cell.lattice_vectors = ((1, 0, 0),\
                                         (0, 1, 0),\
                                         (0, 0, 1))
        >>> unit_cell.calculate_edges_lengths()
        (1.0, 1.0, 1.0)
        >>> unit_cell.a
        1.0

        Returns:
            **tuple[x, y, z] | None**: To calculate edges lattice_vectors
                                   are required else returns None
        """
        if self.lattice_vectors == ():
            return None
        else:
            self.a = (self.lattice_vectors[0][0] ** 2
                      + self.lattice_vectors[0][1] ** 2
                      + self.lattice_vectors[0][2] ** 2) ** (1/2)
            self.b = (self.lattice_vectors[1][0] ** 2
                      + self.lattice_vectors[1][1] ** 2
                      + self.lattice_vectors[1][2] ** 2) ** (1/2)
            self.c = (self.lattice_vectors[2][0] ** 2
                      + self.lattice_vectors[2][1] ** 2
                      + self.lattice_vectors[2][2] ** 2) ** (1/2)
            return (self.a, self.b, self.c)

    def calculate_interaxial_angles(self) -> tuple[deg, deg, deg] | None:
        """Calculate interaxial angles.

        Example:
        >>> unit_cell = UnitCell()
        >>> unit_cell.lattice_vectors = ((1, 1, 0),\
                                         (0, 1, 0),\
                                         (0, 0, 1))
        >>> angles = unit_cell.calculate_interaxial_angles()
        >>> round(angles[0], 1)
        90.0
        >>> round(angles[1], 1)
        90.0
        >>> round(angles[2], 1)
        45.0

        Returns:
            **tuple[deg, deg, deg] | None**: To calculate angles lattice_vectors
                                         are required else returns None
        """
        if self.lattice_vectors == ():
            return None
        else:
            if self.a == 0 or self.b == 0 or self.c == 0:
                self.calculate_edges_lengths()

            self.alfa = degrees(acos((
                self.lattice_vectors[1][0]
                * self.lattice_vectors[2][0]
                + self.lattice_vectors[1][1]
                * self.lattice_vectors[2][1]
                + self.lattice_vectors[1][2]
                * self.lattice_vectors[2][2])
                / (self.b * self.c)))

            self.beta = degrees(acos((
                self.lattice_vectors[0][0]
                * self.lattice_vectors[2][0]
                + self.lattice_vectors[0][1]
                * self.lattice_vectors[2][1]
                + self.lattice_vectors[0][2]
                * self.lattice_vectors[2][2])
                / (self.a * self.c)))

            self.gamma = degrees(acos((
                self.lattice_vectors[0][0]
                * self.lattice_vectors[1][0]
                + self.lattice_vectors[0][1]
                * self.lattice_vectors[1][1]
                + self.lattice_vectors[0][2]
                * self.lattice_vectors[1][2])
                / (self.a * self.b)))

            return (self.alfa, self.beta, self.gamma)

    def convert_cell_data_to_angstroms(self) -> None:
        """Convert cell data to angstroms.

        You can use it to convert data in lattice_vectors, a, b and c
        from Bohr units to angstroms.

        Example:
        >>> unit_cell = UnitCell()
        >>> unit_cell.lattice_vectors = ((1, 1, 0),\
                                         (0, 1, 0),\
                                         (0, 0, 1))
        >>> unit_cell.convert_cell_data_to_angstroms()
        >>> unit_cell.lattice_vectors
        ((0.52917720859, 0.52917720859, 0.0), (0.0, 0.52917720859, 0.0), \
(0.0, 0.0, 0.52917720859))

        """
        if self.converted_to_angstroms is False:
            new_lattice_vectors = []
            for vector in self.lattice_vectors:
                new_lattice_vectors.append((
                    vector[0] * self._CONSTANT_TO_CALCULATE_ANGSTROMS_FROM_BOHR,
                    vector[1] * self._CONSTANT_TO_CALCULATE_ANGSTROMS_FROM_BOHR,
                    vector[2] * self._CONSTANT_TO_CALCULATE_ANGSTROMS_FROM_BOHR))

            self.lattice_vectors = tuple(new_lattice_vectors)

            if self.a != 0 and self.b != 0 and self.c != 0:
                self.a = self.a\
                    * self._CONSTANT_TO_CALCULATE_ANGSTROMS_FROM_BOHR
                self.b = self.b\
                    * self._CONSTANT_TO_CALCULATE_ANGSTROMS_FROM_BOHR
                self.c = self.c\
                    * self._CONSTANT_TO_CALCULATE_ANGSTROMS_FROM_BOHR

            self.converted_to_angstroms = True


class Populations:
    """Populations from MULLIKEN, LOWDIN analysis."""

    mulliken: dict[int, tuple[str, float]] = {}
    lodwin: dict[int, tuple[str, float]] = {}
    valence: dict[int, tuple[str, float]] = {}

    def __init__(self) -> None:
        pass


class MayerBondOrders:
    """Object stores Mayer bond orders of atoms pairs."""
    rows = list[float]
    """Type alias."""
    mayer_bond_orders: list[rows] = []
    horizontal_atom_symbol: dict[int, str] = {}
    atom_id: list[int] = []
    vertical_atom_symbol: dict[int, str] = {}

    def __init__(self, mayer_bond_orders: list[rows],
                 atom_id: list[int],
                 horizontal_atom_symbol: dict[int, str] = {},
                 vertical_atom_symbol: dict[int, str] = {}):

        if (len(mayer_bond_orders) == len(atom_id) and
           len(mayer_bond_orders[0]) == len(atom_id)):
            self.mayer_bond_orders = mayer_bond_orders
            self.atom_id = atom_id
        else:
            raise ValueError("Size of mayer_bond_orders must fit"
                             + "to horizontal_atom_id and "
                             + "vertical_atom_id!!!")

        if (horizontal_atom_symbol != {} and vertical_atom_symbol != {}
            and len(horizontal_atom_symbol) == len(mayer_bond_orders)
                and len(vertical_atom_symbol) == len(mayer_bond_orders[0])):
            self.horizontal_atom_symbol = horizontal_atom_symbol
            self.vertical_atom_symbol = vertical_atom_symbol
        elif (horizontal_atom_symbol == {}
              and vertical_atom_symbol == {}):
            pass
        else:
            raise ValueError("Size of mayer_bond_orders must fit"
                             + "to horizontal_atom_symbol and "
                             + "vertical_atom_symbol!!!")

    def get_mayer_bond_order_between_atoms(self, atom_id_1: int, atom_id_2:
                                           int) -> float:
        """Get mayer bond order between atoms.

        Args:
            atom_id_1 (int): first atom id (row)
            atom_id_2 (int): second atom id (column)

        Returns:
            **float**: bond order
        """

        row = self.mayer_bond_orders[self.atom_id.index(atom_id_2)]
        return row[self.atom_id.index(atom_id_1)]

    def get_atoms_ids(self, atom_symbol: str) -> list[int]:
        """Get atoms ids in MayerBondOrders.

        Args:
            atom_symbol (str): Symbol of atom eg. P, Fe, ...

        Returns:
            **list[int]**: list of ids
        """
        ids = []
        for key, value in self.horizontal_atom_symbol.items():
            if value == atom_symbol:
                ids.append(key)

        return ids

    def check_atom_symbol_in_MBO(self, atom_symbol: str) -> bool:
        """Check atom symbol in MayerBondOrders object.

        Args:
            atom_symbol (str): Symbol of atom eg. 'P'.

        Returns:
            **bool**: True if in MayerBondOrders object.

        """
        if self.get_atoms_ids(atom_symbol) == []:
            return False
        else:
            return True

    def get_atom_symbols(self, atom_id_1: int, atom_id_2:
                         int) -> tuple[str, str] | None:
        """Get atom symbols of pair of atoms.

        Args:
            atom_id_1 (int): atom 1 id
            atom_id_2 (int): atom 2 id

        Returns:
            **tuple(str, str) | None**: Symbol of atom 1 and atom 2,
                                    if wrong id of atoms returns None or
                                    atoms symbols have not been used.

        """
        atom_1 = self.horizontal_atom_symbol.get(atom_id_1, None)
        atom_2 = self.vertical_atom_symbol.get(atom_id_2, None)

        if atom_1 is None or atom_2 is None:
            return None
        else:
            return (atom_1, atom_2)

    def get_all_mayer_bond_orders_of_atom(self, atom_id) -> list[float]:
        """Returns list of mayer bond orders of atom of given id.

        Args:
            atom_id (int): atom id.

        Returns:
            **list[float]**: list of mayer bond orders.
        """
        row = self.mayer_bond_orders[self.atom_id.index(atom_id)]
        return row

    def get_mayer_bond_orders_list_between_two_atoms(self, atom_symbol_1: str,
                                                     atom_symbol_2: str
                                                     ) -> list[float]:
        """Get Mayer bond orders list between two atoms.

        Args:
            atom_symbol_1 (str): atom symbol eg. "Fe"
            atom_symbol_2 (str): atom symbol eg. "Fe"

        Returns:
            **list[float]**: list of mayer bond orders
        """
        mayer_bond_orders = []
        for atom_id_1 in self.atom_id:
            if atom_symbol_1 == self.vertical_atom_symbol.get(atom_id_1):
                for atom_id_2 in range(atom_id_1 + 1, len(self.atom_id) + 1):
                    if atom_symbol_2 == self.vertical_atom_symbol.get(atom_id_2):
                        mayer_bond_orders.append(
                            self.get_mayer_bond_order_between_atoms(atom_id_1,
                                                                    atom_id_2))

        return mayer_bond_orders


class CoordinatesOfAtoms(Constants):
    """Object represents coordinates of atoms.

    Args:
        atom_coordinates_table (list[tuple[atom_id, str, x, y, z]], optional): \
        Table with atom coordinates.

    Attributes:
        ids (list[atom_id]): ids of atoms.
        atom_symbols (dict[atom_id, str]): \
        Dictionary storing symbols of atoms, key is atom id.

    Types:
        atom_id = int

    """

    atom_id: TypeAlias = int
    """Type alias"""
    ids: list[atom_id]
    _coordinates: dict[atom_id, vector]
    atom_symbols: dict[atom_id, str]
    _unit_cell: UnitCell | None

    def __init__(self, atom_coordinates_table: list[tuple[atom_id, str, x, y,
                                                          z]] = []) -> None:

        self.ids = []
        self._coordinates = {}
        self.atom_symbols = {}
        self._unit_cell = None

        if atom_coordinates_table != []:
            while atom_coordinates_table != []:
                row = atom_coordinates_table.pop(0)
                self.ids.append(row[0])
                self.atom_symbols.update({row[0]: row[1]})
                self._coordinates.update({row[0]: (row[2], row[3], row[4])})

    def add_new_atom(self, id: int, atom_symbol: str, coordinates:
                     tuple[x, y, z]) -> None:
        """Add new atom coordinates to CoordinatesOfAtoms object.

        Args:
            id (int): id of new atom.
            atom_symbol (str): Symbol of new atom.
            coordinates (tuple[x, y, z]): Coordinates of new atom.

        """
        self.ids.append(id)
        self.atom_symbols.update({id: atom_symbol})
        self._coordinates.update({id: coordinates})

    def get_atom_coordinates(self, id: int) -> tuple[x, y, z] | None:
        """Get atoms coordinates.

        Args:
            id (int): atom id

        Returns:
            **tuple[x, y, z] | None**: Returns atom coordinates or None if atom of
                                   given id does not exist.

        """
        return self._coordinates.get(id, None)

    def get_atom_coordinates_converted_in_angstrom(self, id: int)\
            -> tuple[x, y, z] | None:
        """Get atom coordinates converted in angstroms if they were stored as
        Bohr units. Not change stored values.

        Example:
        >>> coordinates_of_atoms = CoordinatesOfAtoms()
        >>> coordinates_of_atoms.add_new_atom(1, 'P', (1, 1, 1))
        >>> coordinates_of_atoms.get_atom_coordinates_converted_in_angstrom(1)
        (0.52917720859, 0.52917720859, 0.52917720859)

        Args:
            id (int): atom id

        Returns:
            **tuple[x, y, z]**: coordinates in angstroms

        """
        temp_coordinates = self._coordinates.get(id, None)
        if temp_coordinates is not None:
            coordinates = (
                self._CONSTANT_TO_CALCULATE_ANGSTROMS_FROM_BOHR
                * temp_coordinates[0],
                self._CONSTANT_TO_CALCULATE_ANGSTROMS_FROM_BOHR
                * temp_coordinates[1],
                self._CONSTANT_TO_CALCULATE_ANGSTROMS_FROM_BOHR
                * temp_coordinates[2])
            return coordinates
        else:
            return None

    def convert_stored_coordinates_to_angstroms(self) -> None:
        """Converts stored coordinates from bohr units to angstroms.

        Example:
        >>> coordinates_of_atoms = CoordinatesOfAtoms()
        >>> coordinates_of_atoms.add_new_atom(1, 'P', (1, 1, 1))
        >>> coordinates_of_atoms.add_new_atom(2, 'P', (0, 0, 0))
        >>> coordinates_of_atoms.convert_stored_coordinates_to_angstroms()
        >>> coordinates_of_atoms.get_atom_coordinates(1)
        (0.52917720859, 0.52917720859, 0.52917720859)

        """

        for id, coord in self._coordinates.items():
            self._coordinates[id] = (
                self._CONSTANT_TO_CALCULATE_ANGSTROMS_FROM_BOHR * coord[0],
                self._CONSTANT_TO_CALCULATE_ANGSTROMS_FROM_BOHR * coord[1],
                self._CONSTANT_TO_CALCULATE_ANGSTROMS_FROM_BOHR * coord[2],
            )

    def get_atom_symbol(self, id: int) -> str | None:
        """Get atom symbol

        Args:
            id (int): atom id

        Returns:
            **Union[str, None]**: Returns atom symbol or None if atom of
                        given id does not exist.

        """
        return self.atom_symbols.get(id)

    @property
    def coordinates(self) -> list[vector]:
        coordinates = [value for value in self._coordinates.values()]
        return coordinates

    def add_unit_cell(self, unit_cell: UnitCell):
        self._unit_cell = unit_cell

    def remove_unit_cell(self):
        self._unit_cell = None

    def get_distance_between_atoms(self, atom_id_1: int, atom_id_2: int)\
            -> float | None:
        """ Calculate distance between two atoms.

        Args:
            atom_id_1 (int): id of first atom
             atom_id_2 (int): id of second atom
        Returns:
            **float | None**: Distance in angstroms or Bohr units.

        """

        if type(self._unit_cell) is not UnitCell:
            raise Exception("Unit cell not added or wrong type of"
                            + " unit_cell, use .add_unit_cell(self, unit_cell) method!!!")

        atom_coord_1_v = self._coordinates.get(atom_id_1, None)
        atom_coord_2_v = self._coordinates.get(atom_id_2, None)

        if atom_coord_1_v is None or atom_coord_2_v is None:
            return None
        else:
            atom_coord_1 = np.array(atom_coord_1_v)
            atom_coord_2 = np.array(atom_coord_2_v)

        vector_between_atoms = atom_coord_1 - atom_coord_2

        length = float(np.linalg.norm(vector_between_atoms))

        lattice_vectors_list = []
        for vector in self._unit_cell.lattice_vectors:
            lattice_vectors_list.append(np.array(vector))

        def get_lower_distance(length: float, vector_1: NDArray,
                               vector_2: NDArray) -> float:
            vector_between_atoms = vector_1 - vector_2

            new_length = float(np.linalg.norm(vector_between_atoms))

            if new_length < length:
                length = new_length

            return length

        for vector in lattice_vectors_list:
            atom_2_coord_in_neighboring_unit = atom_coord_2 + vector

            length = get_lower_distance(length, atom_coord_1,
                                        atom_2_coord_in_neighboring_unit)

        for vector in lattice_vectors_list:
            atom_2_coord_in_neighboring_unit = atom_coord_2 - vector

            length = get_lower_distance(length, atom_coord_1,
                                        atom_2_coord_in_neighboring_unit)

        for i in range(3):
            for j in range(i + 1, 3):
                translation = lattice_vectors_list[i] + lattice_vectors_list[j]
                atom_2_coord_in_neighboring_unit = atom_coord_2 + translation

                length = get_lower_distance(length, atom_coord_1,
                                            atom_2_coord_in_neighboring_unit)

                atom_2_coord_in_neighboring_unit = atom_coord_2 - translation

                length = get_lower_distance(length, atom_coord_1,
                                            atom_2_coord_in_neighboring_unit)

                translation = lattice_vectors_list[i] - lattice_vectors_list[j]
                atom_2_coord_in_neighboring_unit = atom_coord_2 + translation

                length = get_lower_distance(length, atom_coord_1,
                                            atom_2_coord_in_neighboring_unit)

                atom_2_coord_in_neighboring_unit = atom_coord_2 - translation

                length = get_lower_distance(length, atom_coord_1,
                                            atom_2_coord_in_neighboring_unit)

        translation = lattice_vectors_list[0] + lattice_vectors_list[1]\
            + lattice_vectors_list[2]

        atom_2_coord_in_neighboring_unit = atom_coord_2 + translation

        length = get_lower_distance(length, atom_coord_1,
                                    atom_2_coord_in_neighboring_unit)

        atom_2_coord_in_neighboring_unit = atom_coord_2 - translation

        length = get_lower_distance(length, atom_coord_1,
                                    atom_2_coord_in_neighboring_unit)

        translation = lattice_vectors_list[0] - lattice_vectors_list[1]\
            + lattice_vectors_list[2]

        atom_2_coord_in_neighboring_unit = atom_coord_2 + translation

        length = get_lower_distance(length, atom_coord_1,
                                    atom_2_coord_in_neighboring_unit)

        atom_2_coord_in_neighboring_unit = atom_coord_2 - translation

        length = get_lower_distance(length, atom_coord_1,
                                    atom_2_coord_in_neighboring_unit)

        translation = lattice_vectors_list[0] - lattice_vectors_list[1]\
            - lattice_vectors_list[2]

        atom_2_coord_in_neighboring_unit = atom_coord_2 + translation

        length = get_lower_distance(length, atom_coord_1,
                                    atom_2_coord_in_neighboring_unit)

        atom_2_coord_in_neighboring_unit = atom_coord_2 - translation

        length = get_lower_distance(length, atom_coord_1,
                                    atom_2_coord_in_neighboring_unit)

        translation = lattice_vectors_list[0] + lattice_vectors_list[1]\
            - lattice_vectors_list[2]

        atom_2_coord_in_neighboring_unit = atom_coord_2 + translation

        length = get_lower_distance(length, atom_coord_1,
                                    atom_2_coord_in_neighboring_unit)

        atom_2_coord_in_neighboring_unit = atom_coord_2 - translation

        length = get_lower_distance(length, atom_coord_1,
                                    atom_2_coord_in_neighboring_unit)

        return length


class InputData(ABC):
    """Input data.

    Load data from file and create objects.

    """

    populations: Populations | None = None
    unit_cell: UnitCell | None = None
    mayer_bond_orders: MayerBondOrders | None = None
    coordinates_of_atoms: CoordinatesOfAtoms | None = None

    def __init__(self, Populations: type = Populations,
                 UnitCell: type = UnitCell,
                 MayerBondOrders: type = MayerBondOrders,
                 CoordinatesOfAtoms: type = CoordinatesOfAtoms):
        """Constructor.

        Args:
            Populations (type, optional): Defaults to Populations.
            UnitCell (type, optional): Defaults to UnitCell.
            MayerBondOrders (type, optional): Defaults to MayerBondOrders.
            CoordinatesOfAtoms (type, optional): Defaults to CoordinatesOfAtoms.

        """

        self.Populations = Populations
        self.UnitCell = UnitCell
        self.MayerBondOrders = MayerBondOrders
        self.CoordinatesOfAtoms = CoordinatesOfAtoms
        self.LoadedData = LoadedData

    @abstractmethod
    def load_input_data(self, path: str, *args) -> None:
        """Load input data from file.

        Args:
            path (str): Path to file.
            *args: LoadData.UnitCell, LoadedData.MayerBondOrders,\
                LoadData.Populations or LoadData.CoordinatesOfAtoms

        """
        pass

    @staticmethod
    def check_is_correct_file(data_in_file: str, fingerprint: str) -> bool:
        if fingerprint in data_in_file:
            return True
        else:
            return False


class InputDataFromCPMD(InputData):
    """Loads data from CPMD file and create objects."""
    _fingerprint: str = "The CPMD consortium"
    _fingerprint_beginning_populations: str = "POPULATION ANALYSIS FROM PROJECTED"\
        + " WAVEFUNCTIONS"
    _fingerprint_end_populations: str = "ChkSum\(POP_MUL\)"
    _fingerprint_coordinates_of_atoms: str = "ATOM             COORDINATES"\
        + "                   CHARGES"
    _fingerprint_end_coordinates_of_atoms: str = "ChkSum\(CHARGES\)"
    _fingerprint_mayer_bond_orders: str = "MAYER BOND ORDERS FROM PROJECTED"\
        + " WAVEFUNCTIONS"

    _fingerprints_unit_cell: tuple[str, str, str] = ("LATTICE VECTOR A1\(BOHR\):",
                                                     "LATTICE VECTOR A2\(BOHR\):",
                                                     "LATTICE VECTOR A3\(BOHR\):")

    _valid_population_columns_names: tuple[str, str, str, str] = (
        'ATOM', 'MULLIKEN', 'LOWDIN', 'VALENCE')

    _valid_coordinatios_columns_names: tuple[str, str, str] = (
        'X', 'Y', 'Z')

    def load_input_data(self, path: str, *args) -> None:
        """Loads input data from CPMD file.

        Args:
            path (str): path to file
            *args: LoadData.UnitCell, LoadedData.MayerBondOrders,
            LoadData.Populations or LoadData.CoordinatesOfAtoms

        """
        with open(path, 'r') as file:
            data = file.read()

        if self.check_is_correct_file(data, self._fingerprint) is not True:
            raise Exception("Wrong input file!")
        else:
            if self.LoadedData.UnitCell in args:
                self.unit_cell = self._load_unit_cell(data)
            if self.LoadedData.MayerBondOrders in args:
                self.mayer_bond_orders = \
                    self._load_mayer_bond_orders(data)
            if self.LoadedData.Populations in args:
                self.populations = self._load_populations(data)
            if self.LoadedData.CoordinatesOfAtoms in args:
                self.coordinates_of_atoms = \
                    self._load_coordinates_of_atoms(data)

    def return_data(self, loaded_data: LoadedData)\
            -> Populations | UnitCell | MayerBondOrders | CoordinatesOfAtoms\
            | None:
        """ Returns loaded data.

        Args:

        Returns:
            **Populations | UnitCell | MayerBondOrders | CoordinatesOfAtoms**:

        """
        if loaded_data is LoadedData.UnitCell:
            return self.unit_cell
        elif loaded_data is LoadedData.MayerBondOrders:
            return self.mayer_bond_orders
        elif loaded_data is LoadedData.Populations:
            return self.populations
        elif loaded_data is LoadedData.CoordinatesOfAtoms:
            return self.coordinates_of_atoms
        else:
            raise TypeError("Type is not LoadedData!!!!")

    def _load_populations(self, file: str) -> Populations | None:

        rows = self._get_rows_of_data_from_file(file,
                                                self._fingerprint_beginning_populations,
                                                self._fingerprint_end_populations)
        labels: list = []
        if rows is not None:
            for row in rows:
                have_string = True if re.search('[a-zA-Z]+', row) is \
                    not None else False

                have_number = True if re.search('[0-9]+', row) is \
                    not None else False

                if have_string and not have_number:
                    labels = row.split()
                    populations = Populations()
                    continue
                elif have_string and have_number:
                    splited = row.split()
                    if len(labels) + 1 != len(splited):
                        raise Exception(
                            'Wrong quantity of columns in input file!')
                    else:
                        populations = self._add_populations_attributes(
                            populations, splited, labels)
            return populations
        else:
            return None

    @classmethod
    def _add_populations_attributes(cls, populations: Populations,
                                    splited: list, labels: list[str])\
            -> Populations:
        i = 0
        for item in splited:
            if i == 0:
                id = int(item)
            elif labels[i-1] == cls._valid_population_columns_names[0]:
                symbol = item
            elif labels[i-1] == cls._valid_population_columns_names[1]:
                mulliken_value = float(item)
            elif labels[i-1] == cls._valid_population_columns_names[2]:
                lowdin_value = float(item)
            elif labels[i-1] == cls._valid_population_columns_names[3]:
                valence_value = float(item)
            i += 1

        populations.lodwin.update({id: (symbol, lowdin_value)})
        populations.mulliken.update({id: (symbol, mulliken_value)})
        populations.valence.update({id: (symbol, valence_value)})

        return populations

    def _load_coordinates_of_atoms(self, file: str)\
            -> CoordinatesOfAtoms | None:
        rows = self._get_rows_of_data_from_file(file,
                                                self._fingerprint_coordinates_of_atoms,
                                                self._fingerprint_end_coordinates_of_atoms)
        if rows is not None:
            for row in rows:
                have_string = True if re.search('[a-zA-Z]+', row) is \
                    not None else False

                have_number = True if re.search('[0-9]+', row) is \
                    not None else False

                if have_string and not have_number:
                    labels = row.split()
                    coordinates_of_atoms = self.CoordinatesOfAtoms()
                    continue
                elif have_string and have_number:
                    splited = row.split()
                    if len(labels) + 2 != len(splited):
                        raise Exception(
                            'Wrong quantity of columns in input file!')
                    else:
                        coordinates_of_atoms = self._add_coordinations_attributes(
                            coordinates_of_atoms, splited, labels
                        )
            return coordinates_of_atoms
        else:
            return None

    @classmethod
    def _add_coordinations_attributes(cls, coordinates_of_atoms:
                                      CoordinatesOfAtoms,
                                      splited: list, labels: list[str])\
            -> CoordinatesOfAtoms:
        i = 0
        for item in splited:
            if i == 0:
                atom_id = int(item)
            elif i == 1:
                atom_symbol = item
            elif labels[i - 2] == cls._valid_coordinatios_columns_names[0]:
                x = float(item)
            elif labels[i - 2] == cls._valid_coordinatios_columns_names[1]:
                y = float(item)
            elif labels[i - 2] == cls._valid_coordinatios_columns_names[2]:
                z = float(item)
            i += 1

        coordinates_of_atoms.add_new_atom(atom_id, atom_symbol, (x, y, z))
        return coordinates_of_atoms

    @staticmethod
    def _get_rows_of_data_from_file(file: str,
                                    finger_print_begin: str, finger_print_end)\
            -> list[str] | None:
        """Get rows fo data from file

        Args:
            finger_print_begin (str): fingerprint on beginning of data
            finger_print_end (str): fingerprint on end of data

        Returns:
            **list[str]**: rows of string data

        """

        regex = f'(?<={finger_print_begin})[\s\S]*' \
            + f'(?={finger_print_end})'

        match = re.search(regex, file)
        if match is not None:
            return match[0].split('\n')
        else:
            return None

    def _load_mayer_bond_orders(self, file: str) -> MayerBondOrders:
        match = re.search(
            f"(?<={self._fingerprint_mayer_bond_orders}\n\n)([\S ]+\n)*", file)
        if match is None:
            raise Exception("Mayers bond orders aren't in file or wrong file"
                            + "format!!!!")
        rows = match[0].split('\n')
        rows = [row for row in rows if row != '']
        number_of_atoms = int(rows[-1].split()[0])
        n = number_of_atoms // 8
        m = 1 if number_of_atoms % 8 > 0 else 0
        number_of_tables = m + n

        number_of_rows = (len(rows)) * number_of_tables
        match = re.search(
            f"(?<={self._fingerprint_mayer_bond_orders}\n\n)([\S ]+\n*){{{number_of_rows}}}", file)

        if match is None:
            raise Exception("Mayers bond orders aren't in file or wrong file"
                            + "format!!!!")
        rows_full_table = []
        tables = match[0].split('\n\n')
        first_table = True
        for table in tables:
            splited = table.split('\n')
            i = 0
            for item in splited:
                if first_table:
                    row = item.split()
                    rows_full_table.append(row)
                elif i == 0:
                    row = item.split()
                    rows_full_table[i].extend(row)
                else:
                    row = item.split()
                    rows_full_table[i].extend(row[2:])
                i += 1
            first_table = False

        row_horizontal = rows_full_table.pop(0)
        i = 0
        j = 0
        horizontal_atom_symbol = {}
        horizontal_atom_id = []
        for item in row_horizontal:
            if i % 2 == 0:
                j += 1
                horizontal_atom_id.append(int(item))
            else:
                horizontal_atom_symbol.update(
                    {horizontal_atom_id[j - 1]: str(item)})
            i += 1

        vertical_atom_symbol = {}
        vertical_atom_id = []
        new_rows_full_table = []
        for row in rows_full_table:
            vertical_atom_id.append(int(row.pop(0)))
            vertical_atom_symbol.update(
                {vertical_atom_id[-1]: str(row.pop(0))})
            row_f = [float(item) for item in row]
            new_rows_full_table.append(row_f)

        if horizontal_atom_id == vertical_atom_id:
            mayer_bond_order = self.MayerBondOrders(new_rows_full_table,
                                                    horizontal_atom_id,
                                                    horizontal_atom_symbol,
                                                    vertical_atom_symbol)
        else:
            raise Exception(
                "The condition: 'horizontal_atom_id == vertical_atom_id' "
                + "must be met ")
        return mayer_bond_order

    @classmethod
    def _load_unit_cell(cls, file: str):
        vectors = []
        for item in cls._fingerprints_unit_cell:
            regex = f'(?<={item})[ \S]+'
            match = re.search(regex, file)
            if match is None:
                raise Exception(" wrong file format!!!!")
            row = match[0].split()
            row_f = [float(item) for item in row]
            vectors.append(row_f)
        unit_cell = UnitCell()
        unit_cell.lattice_vectors = tuple(item
                                          for item in vectors)
        return unit_cell
