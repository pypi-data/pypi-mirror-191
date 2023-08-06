__docformat__ = "google"
"""Calculations module."""
import numpy as np
from typing import Callable
from abc import ABC
from abc import abstractmethod
from .input_data import MayerBondOrders
from .input_data import CoordinatesOfAtoms
from typing import TypeAlias
from dataclasses import dataclass


@dataclass
class PairOfAtoms:
    """PairOfAtoms.

    Object represents Pair of Atoms

    Attributes:
        atom_1 (str): First atom name.
        atom_2 (str): Second atom name.
        MBO_min (float): Minimum Mayer bond order cut off.
        MBO_max (float | str):Max Mayer bond order cut off. Float or 'INF' - for infinite value.capitalize()
        id (str): Bond id eg. 'P-O'

    """

    atom_1: str
    atom_2: str
    MBO_min: float
    MBO_max: float | str
    id: str


class Calculations(ABC):
    """Calculations base class."""

    @abstractmethod
    def calculate(cls, *args, **kwars) -> type:
        pass

    @abstractmethod
    def to_string(self, *args, **kwars) -> str:
        pass


class Statistics(ABC):
    """Statistics base class"""
    @abstractmethod
    def calculate_statistics(self) -> type:
        pass


class Histogram(Calculations):
    """Object represents histogram."""
    _histogram: Callable = np.histogram
    x: list[float] = []
    """Position of bin on x axis."""
    y: list[int] = []
    """Quantity."""

    @classmethod
    def calculate(cls, values: list[float], bins: int):
        """Calculate histogram.

        Args:
            values (list[float]): List of values.
            bins (int): Number of bins in histogram.

        Returns:
            **Histogram**: Histogram object.

        """
        histogram = cls._histogram(values, bins)

        y = histogram[0]
        x = histogram[1]
        y = y.tolist()
        x = x.tolist()

        first_loop = True
        new_x = []
        for item in x:
            if first_loop:
                first_loop = False
                previous = item
            else:
                new_x.append((item
                              + previous) / 2)
                previous = item

        histogram = cls()
        histogram.x = new_x
        histogram.y = y
        return histogram

    def to_string(self, bond_id: str, atom_symbol_1: str, atom_symbol_2: str)\
            -> str:
        """Make string from Histogram object

        Args:
            bond_id (str): eg. P-O.
            atom_symbol_1 (str): Symbol of atom 1.
            atom_symbol_2 (str): Symbol of atom 2.
        Returns:
            **str**: String.

        """
        string = f'Bond id: {bond_id} - atom_1_id: {atom_symbol_1}, atom_2_id: {atom_symbol_2}\n\n'
        string = string + 'Interval/2' + ' ' + 'Count' + '\n\n'
        for i in range(len(self.x)):
            string = string + \
                str(round(self.x[i], 9)) + ' ' + \
                str(round(self.y[i], 9)) + '\n'

        string = string + '\n'

        return string


@dataclass
class CoordinationNumber:
    """Object stores coordination number of given atom and
    Mayer bond orders corresponding to the bonds in the
    coordination polyhedron."""

    id_atom_1: int
    """Central atom id."""
    cn: int
    """Value of coordination number."""
    bonds: dict[int, float]
    """**Key** - ligand id, **value** - Mayer bond order."""


class CoordinationNumbers(Calculations, Statistics):
    """Generate list of CoordinationNumber objects and processes it."""
    CoordinationNumber: type = CoordinationNumber

    list_coordinations_number: list[CoordinationNumber]
    """List of CoordinationNumber objects."""
    id_of_bond: str
    """Id of bond eg. 'P-O'"""
    atom_symbol: str
    """Symbol of atom."""
    statistics: dict[int, float] | None = None
    """**Key** - coordination number, **value** - percentages."""

    @classmethod
    def calculate(cls, mayer_bond_orders: MayerBondOrders,
                  atom_symbol_1: str, atom_symbol_2: str,
                  max_mayer_bond_order: float | str,
                  min_mayer_bond_order: float,
                  id_of_bond: str):
        """Calculate CoordinationNumbers object.

        Args:
            mayer_bond_orders (MayerBondOrders): MayerBondOrders object.
            atom_symbol_1 (str): Central atom symbol.
            atom_symbol_2 (str): Ligand symbol.
            max_mayer_bond_order (float): Max cut of radius, float or 'INF" if infinite value.
            min_mayer_bond_order (float): Min cut of radius.
            id_of_bond (str): id of bond eg. 'P-O'

        Returns:
            **CoordinationNumbers**: CoordinationNumbers object

        """

        if max_mayer_bond_order != "INF"\
                and not (type(max_mayer_bond_order) is float):
            raise ValueError("Wrong type of max_mayer_bond_order!!!!")

        atom_1_ids = mayer_bond_orders.get_atoms_ids(atom_symbol_1)
        atom_2_ids = mayer_bond_orders.get_atoms_ids(atom_symbol_2)

        list_coordinations_number = []
        for atom_1_id in atom_1_ids:

            coordination_number = cls.CoordinationNumber(atom_1_id, 0, {})

            for atom_2_id in atom_2_ids:
                if atom_1_id != atom_2_id:

                    mbo = mayer_bond_orders\
                        .get_mayer_bond_order_between_atoms(atom_1_id,
                                                            atom_2_id)
                    if (mbo > min_mayer_bond_order
                            and max_mayer_bond_order == 'INF'):
                        coordination_number.bonds.update({atom_2_id: mbo})
                        coordination_number.cn += 1
                    elif (type(max_mayer_bond_order) is float):
                        if (mbo > min_mayer_bond_order
                                and mbo < max_mayer_bond_order):
                            coordination_number.bonds.update({atom_2_id: mbo})
                            coordination_number.cn += 1
                    else:
                        continue

            list_coordinations_number.append(coordination_number)

        self = cls()
        self.id_of_bond = id_of_bond
        self.atom_symbol = atom_symbol_1
        self.list_coordinations_number = list_coordinations_number

        return self

    def calculate_statistics(self):
        """Calculate statistics of CoordinationNumbers.

        Statistic are in "statistics" attribute.

        Returns:
            CoordinationNumbers: CoordinationNumbers object

        """
        cns = self._get_list_of_coordination_numbers()
        quantities: dict = {}
        for cn in cns:
            for item in self.list_coordinations_number:
                if item.cn == cn:
                    if quantities.get(cn, None) is None:
                        quantities.update({cn: 1})
                    else:
                        quantities[cn] = quantities[cn] + 1

        number_of_atoms = len(self.list_coordinations_number)
        statistics = {}
        for key, value in quantities.items():
            statistics.update({key: (value/number_of_atoms) * 100})

        self.statistics = statistics

        return self

    def _get_list_of_coordination_numbers(self) -> list[int]:
        cns = []
        for item in self.list_coordinations_number:
            if item.cn not in cns:
                cns += [item.cn]

        return cns

    def to_string(self) -> str:
        """Make string from CoordinationNumbers object.

        Returns:
            **str**: String.

        """
        string = "## CN of " + str(self.atom_symbol) + " bond: "\
            + str(self.id_of_bond) + "\n\n"
        for item in self.list_coordinations_number:
            string = string + "id: " + str(item.id_atom_1) + " "\
                + "CN: " + str(item.cn)

            if item.cn != 0:
                string += "\n" + "Bond orders (id: mbo): "

            length = len(item.bonds)
            i = 1
            for key, value in item.bonds.items():
                string += str(key) + ': ' + str(value)
                if i < length:
                    string += ', '
                else:
                    pass
                i += 1

            string += '\n'
        string += '\n'

        if self.statistics is not None:
            string = string + "Statistics of: "\
                + str(self.atom_symbol) + "\n\n" + "CN %\n"
            for key, value in self.statistics.items():
                string = string + str(key) + ' ' + str(round(value, 3)) + '\n'

            string = string + '\n'

        return string


class QiUnits(Calculations, Statistics):
    """Stores information about Qi units."""
    id_of_bond: str
    """Id of bonds in Qⁱ unit"""
    atom_symbol_1: str
    """Symbol of central atom"""
    atom_symbol_2: str
    """Symbol of ligands"""
    q_i_units: dict[int, int] = {}
    """Dictionary stores values of i of Qⁱ units. key - central atom id."""
    statistics: dict[int, float] | None = None
    """Dictionary stores percentages of Qⁱ units. key - value of i in Qⁱ"""

    @classmethod
    def calculate(cls, mayer_bond_orders: MayerBondOrders,
                  atom_symbol_1: str,
                  atom_symbol_2: str,
                  max_mayer_bond_order: float | str,
                  min_mayer_bond_order: float,
                  id_of_bond: str):
        """Calculate QiUnits object.

        Args:
            mayer_bond_orders (MayerBondOrders): Object MayerBondOrders.
            atom_symbol_1 (str): Symbol of central atom.
            atom_symbol_2 (str): Symbol of ligands.
            max_mayer_bond_order (float | str): Max Mayer bond order, float or 'INF' for infinite maximum value.
            min_mayer_bond_order (float): Min Mayer bond order.
            id_of_bond (str): Name of bond eg. 'P-O'.

        Raises:
            ValueError: "Wrong type of max_mayer_bond_order!!!!"

        Returns:
            **QiUnits**: Returns QiUnits object.

        """

        if max_mayer_bond_order != "INF"\
                and not (type(max_mayer_bond_order) is float):
            raise ValueError("Wrong type of max_mayer_bond_order!!!!")
        elif max_mayer_bond_order == "INF":
            inf = True
            max_mayer_bond_order = -1
            # -1 to prevent exception
        else:
            inf = False

        atom_1_ids = mayer_bond_orders.get_atoms_ids(atom_symbol_1)
        atom_2_ids = mayer_bond_orders.get_atoms_ids(atom_symbol_2)

        self = cls()
        self.id_of_bond = id_of_bond
        self.atom_symbol_1 = atom_symbol_1
        self.atom_symbol_2 = atom_symbol_2
        self.q_i_units = {}
        for atom_1_id in atom_1_ids:

            self.q_i_units.update({atom_1_id: 0})

            for atom_2_id in atom_2_ids:
                mbo = mayer_bond_orders\
                    .get_mayer_bond_order_between_atoms(atom_1_id,
                                                        atom_2_id)
                if (mbo > min_mayer_bond_order
                        and (mbo < max_mayer_bond_order or inf)):

                    for atom_3_id in atom_1_ids:
                        mbo = mayer_bond_orders\
                            .get_mayer_bond_order_between_atoms(atom_2_id,
                                                                atom_3_id)
                        if (mbo > min_mayer_bond_order
                                and (mbo < max_mayer_bond_order or inf)
                                and atom_3_id != atom_1_id):

                            self.q_i_units[atom_1_id] += 1
                            break

                        else:
                            continue

        return self

    def calculate_statistics(self):
        """Calculate statistics in object QiUnits.

        Returns:
            **QiUnits**: QiUnits object.

        """

        unique_values = []
        for value in self.q_i_units.values():
            if value not in unique_values:
                unique_values.append(value)

        quantities = {}
        for unique in unique_values:
            quantities.update({unique: 0})
            for value in self.q_i_units.values():
                if value == unique:
                    quantities[unique] += 1
                else:
                    continue

        quantity_of_all_Q_i = len(self.q_i_units)

        self.statistics = {}

        for key, value in quantities.items():
            self.statistics.update({key: (value/quantity_of_all_Q_i) * 100})

        return self

    def to_string(self) -> str:
        """Generate string representing object.

        Returns:
            **str**: String.

        """
        string = "Q_i of " + str(self.atom_symbol_1) + ' bond id: '\
            + str(self.id_of_bond) + "\n\n"

        string += "id Q_i[i]\n"

        for key, value in self.q_i_units.items():
            string = string + str(key) + ' ' + str(value) + '\n'

        string += '\n'

        if self.statistics is not None:
            string = string + 'Statistics of Q_i: ' + str(self.atom_symbol_1)\
                + ', bond id: ' + str(self.id_of_bond) + '\n\n'

            string += 'Q_i[i] [%]\n'

            for key, value in self.statistics.items():
                string = string + str(key) + ' ' + str(round(value, 3)) + '\n'

        string += '\n'

        return string


@dataclass
class Connection:
    """An object represents connections between two elements."""
    id_atom_2 = int
    mayer_bond_order = float

    atom_symbol_2: str
    """Ligant atom symbol."""
    bond_id: str
    """Bond id eg. 'P-O'"""
    quantity: int
    """Quantity of given connections"""
    bonds: dict[id_atom_2, mayer_bond_order]
    """**key**- ligand id, **value**-mayer bond order."""


class Connections(Calculations):
    """Object represents connections of given atom to nearest neighbors.
    """
    atom_1_id: TypeAlias = int
    Connection: type = Connection

    connections: dict[atom_1_id, list[Connection]]
    """Key - central atom, values - list to Connection objects."""
    atom_symbol_1: str
    """Symbol of central atom."""

    @ classmethod
    def calculate(cls, mayer_bond_orders: MayerBondOrders,
                  atom_symbol_1: str,
                  pairs_atoms_list: list[PairOfAtoms]
                  ):
        """Calculate Connections object.

        Args:
            mayer_bond_orders (MayerBondOrders): MayerBondOrders object.
            atom_symbol_1 (str): Central atom symbol.
            pairs_atoms_list (list[PairOfAtoms]): list of PairsOfAtoms objects.

        Raises:
            ValueError: "Wrong type of max_mayer_bond_order!!!!"

        Returns:
            **Connections**: Connections object.

        """

        pair_atom_list_containing_atom_1 = []
        for pair_atom in pairs_atoms_list:
            if pair_atom.atom_1 == atom_symbol_1\
                    or pair_atom.atom_2 == atom_symbol_1:

                pair_atom_list_containing_atom_1.append(pair_atom)
            else:
                continue

        atom_1_ids = mayer_bond_orders.get_atoms_ids(atom_symbol_1)
        connections = {}
        for atom_1_id in atom_1_ids:

            connections.update({atom_1_id: []})

            for pair_atoms in pair_atom_list_containing_atom_1:
                if (v := pair_atoms.atom_1) != atom_symbol_1:
                    atom_symbol_2 = v
                else:
                    atom_symbol_2 = pair_atoms.atom_2

                connection = cls.Connection(
                    atom_symbol_2, pair_atoms.id, 0, {})

                atom_2_ids = mayer_bond_orders.get_atoms_ids(atom_symbol_2)

                for atom_2_id in atom_2_ids:
                    if pair_atoms.MBO_max != "INF"\
                            and not (type(pair_atoms.MBO_max) is float):
                        raise ValueError(
                            "Wrong type of max_mayer_bond_order!!!!")

                    mbo = mayer_bond_orders\
                        .get_mayer_bond_order_between_atoms(atom_1_id,
                                                            atom_2_id)

                    if (mbo > pair_atoms.MBO_min
                            and pair_atoms.MBO_max == 'INF'):

                        connection.quantity += 1
                        connection.bonds.update({atom_2_id: mbo})

                    elif (pair_atoms.MBO_max != 'INF'):
                        if (mbo > pair_atoms.MBO_min
                                and pair_atoms.MBO_max > mbo):

                            connection.quantity += 1
                            connection.bonds.update({atom_2_id: mbo})

                connections[atom_1_id].append(connection)

        self = cls()
        self.connections = connections
        self.atom_symbol_1 = atom_symbol_1

        return self

    def to_string(self) -> str:
        """Generates string representation of object.

        Returns:
            **str**: string.

        """
        string = '## Connections of: ' + str(self.atom_symbol_1) + '\n\n'

        for atom_1_id, list_of_connections in self.connections.items():
            string = string + "### Central atom id: " + str(atom_1_id) + "\n"

            for connection in list_of_connections:

                string = string + f"Bond id: {str(connection.bond_id)} "\
                    + f"(second atom: {str(connection.atom_symbol_2)})\n"\
                    + f"quantity: {connection.quantity}\n"\
                    + "Bonds:\n"

                string_id_line = "id: "
                string_mbo_line = "mbo: "

                for id, mbo in connection.bonds.items():
                    string_id_line += f"{id} "
                    string_mbo_line += f"{round(mbo, 3)} "

                string = string + string_id_line + '\n'\
                    + string_mbo_line + '\n\n'

        return string


class Covalence(Calculations):
    """Object storages covalences of atoms"""
    covalence: dict[int, float]
    """Key - id of atom, value - covalence calculated from Mayer bond orders."""
    atom_symbol: str
    """Atom symbol."""

    @ classmethod
    def calculate(cls, mayer_bond_orders: MayerBondOrders,
                  atom_symbol: str):
        """Calculate Covalence object.

        Args:
            mayer_bond_orders (MayerBondOrders): MayerBondOrders object.
            atom_symbol (str): Atom symbol.

        Returns:
            **Covalence**: Covalence object.

        """

        atom_ids = mayer_bond_orders.get_atoms_ids(atom_symbol)

        self = cls()
        self.atom_symbol = atom_symbol
        self.covalence = {}
        for id in atom_ids:
            mbos = mayer_bond_orders.get_all_mayer_bond_orders_of_atom(id)
            self.covalence.update({id: sum(mbos)})

        return self

    def to_string(self) -> str:
        """Generates string representation of object.

        Returns:
            **str**: String.

        """
        string = f'Covalence of {self.atom_symbol}.\n\n'\
            + 'id COV\n'

        for id, value in self.covalence.items():
            string = string + f'{id} {value:.3f}\n'
        string += '\n'

        return string


class BondLength(Calculations):
    """Object stored bond lengths of pairs of atoms."""
    atom_id_1: TypeAlias = int
    atom_id_2: TypeAlias = int

    id_of_bond: str
    """Id of bond eg. 'P-O'"""
    atom_symbol_1: str
    """Atom 1 symbol."""
    atom_symbol_2: str
    """Atom 2 symbol."""
    lengths: dict[atom_id_1, dict[atom_id_2, float]]
    """**values**- length between atoms."""
    mbos: dict[atom_id_1, dict[atom_id_2, float]]
    """**values**- Mayer bond orders"""

    @ classmethod
    def calculate(cls,
                  mayer_bond_orders: MayerBondOrders,
                  coordinates_of_atoms: CoordinatesOfAtoms,
                  atom_symbol_1: str,
                  atom_symbol_2: str,
                  max_mayer_bond_order: float | str,
                  min_mayer_bond_order: float,
                  id_of_bond: str):
        """Calculate BondLength object.

        Args:
            mayer_bond_orders (MayerBondOrders): MayerBondOrders object.
            coordinates_of_atoms (CoordinatesOfAtoms): CoordinatesOfAtom object.
            atom_symbol_1 (str): Symbol of atom 1.
            atom_symbol_2 (str): Symbol of atom 2.
            max_mayer_bond_order (float | str): max value of Mayer bond order or 'INF for infinite value.
            min_mayer_bond_order (float): min value of Mayer bond order.
            id_of_bond (str): id of bond eg. 'P-O'

        Raises:
            ValueError: "Wrong type of max_mayer_bond_order!!!!"

        Returns:
            **BondLength**: BondLength object.

        """

        if max_mayer_bond_order != "INF"\
                and not (type(max_mayer_bond_order) is float):
            raise ValueError("Wrong type of max_mayer_bond_order!!!!")
        elif max_mayer_bond_order == "INF":
            inf = True
            max_mayer_bond_order = -1
            # -1 to prevent exception
        else:
            inf = False

        atom_1_ids = mayer_bond_orders.get_atoms_ids(atom_symbol_1)
        atom_2_ids = mayer_bond_orders.get_atoms_ids(atom_symbol_2)

        self = cls()
        self.id_of_bond = id_of_bond
        self.atom_symbol_1 = atom_symbol_1
        self.atom_symbol_2 = atom_symbol_2
        self.lengths = {}
        self.mbos = {}

        for atom_1_id in atom_1_ids:
            self.lengths.update({atom_1_id: {}})
            self.mbos.update({atom_1_id: {}})
            for atom_2_id in atom_2_ids:
                mbo = mayer_bond_orders\
                    .get_mayer_bond_order_between_atoms(atom_1_id,
                                                        atom_2_id)

                length = coordinates_of_atoms\
                    .get_distance_between_atoms(atom_1_id, atom_2_id)

                if mbo > min_mayer_bond_order and (
                    mbo < max_mayer_bond_order
                    or inf is True
                ):
                    self.lengths[atom_1_id].update({atom_2_id: length})
                    self.mbos[atom_1_id].update({atom_2_id: mbo})
                else:
                    continue

        # remove empty keys.

        for key in list(self.lengths.keys()):
            if self.lengths[key] == {}:
                del self.lengths[key]
                del self.mbos[key]

        return self

    def to_string(self) -> str:
        """Generates string representation of object.

        Returns:
            **str**: String.

        """
        string = f'Bond lengths of bond id: {self.id_of_bond} '\
            + f'(atoms: {self.atom_symbol_1}, {self.atom_symbol_2}):\n\n'\
            + 'id_1 id_2 length mbo\n'

        for key_1 in self.lengths.keys():
            for key_2 in self.lengths[key_1].keys():
                string = string + f'{key_1} {key_2} '\
                    + f'{self.lengths[key_1][key_2]} '\
                    + f'{self.mbos[key_1][key_2]}\n'

        string += '\n'

        return string
