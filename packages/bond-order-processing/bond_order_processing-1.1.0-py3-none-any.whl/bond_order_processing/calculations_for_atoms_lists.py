"""Calculations in this module are made for PairOfAtoms
objects lists. This module is added in version: 1.1.0.


Example:

    >>> from bond_order_processing.input_data import LoadedData
    >>> from bond_order_processing.calculations_for_atoms_lists import CoordinationNumbers
    >>> from bond_order_processing.input_data import InputDataFromCPMD
    >>> from bond_order_processing.calculations import PairOfAtoms
    >>> 
    >>> path_to_input_file = r'./egzamples_instructions/out1.txt'
    >>> 
    >>> input_data = InputDataFromCPMD()
    >>> input_data.load_input_data(path_to_input_file, LoadedData.MayerBondOrders)
    >>> mayer_bond_orders = input_data.return_data(LoadedData.MayerBondOrders)
    >>> 
    >>> pairs_of_atoms = [PairOfAtoms("P", "O", 0.2, 2.0, "P-O"), PairOfAtoms("Fe", "O", 0.2, 2.0, "Fe-O")]
    >>> # Calculate percentage of coordination numbers of P
    >>> coordinations_numbers_stats = CoordinationNumbersFromPairOfAtoms.calculate(pairs_of_atoms, mayer_bond_orders).calculate_statistics()
    >>> coordinations_numbers_stats.coordination_numbers['P-O'].statistics
    {4: 100.0}
    
"""
__docformat__ = "google"
from .calculations import Calculations
from .calculations import Statistics
from .calculations import PairOfAtoms
from .calculations import Histogram
from .input_data import MayerBondOrders
from .input_data import CoordinatesOfAtoms
from .calculations import CoordinationNumbers
from .calculations import Connections
from .calculations import BondLength
from .calculations import Covalence
from .calculations import QiUnits


class _FromPairOfAtoms:
    @ staticmethod
    def _get_unique_atom_symbols(pair_of_atoms: list[PairOfAtoms])\
            -> list[str]:
        unique_symbols = []
        for item in pair_of_atoms:
            if item.atom_1 not in unique_symbols:
                unique_symbols.append(item.atom_1)
            if item.atom_2 not in unique_symbols:
                unique_symbols.append(item.atom_2)

        return unique_symbols


class HistogramsFromPairOfAtoms(Calculations):
    """Calculate histograms for list of pairs of atoms."""
    _Histogram: type = Histogram
    histograms: dict[str, Histogram]
    """**key** - bond_id, **value** - Histogram object"""
    _atoms_names: dict[str, (str, str)]

    @classmethod
    def calculate(cls, pair_of_atoms: list[PairOfAtoms],
                  mayer_bond_orders: MayerBondOrders,
                  bins: int):
        """Calculate HistogramsFromPairOfAtoms object.

        Args:
            pair_of_atoms (list[PairOfAtoms]): list of PairOfAtoms objects.
            mayer_bond_orders (MayerBondOrders): MayerBondOrders object.
            bins (int): Number of bins in histogram.

        Returns:
            **HistogramsFromPairOfAtoms**: HistogramsFromPairOfAtoms object

        """
        self = cls()
        self.histograms = {}
        self._atoms_names = {}
        for item in pair_of_atoms:
            mbos = mayer_bond_orders\
                .get_mayer_bond_orders_list_between_two_atoms(
                    item.atom_1, item.atom_2)

            if type(item.MBO_max) is str:
                if item.MBO_max == 'INF':
                    mbos = [mbo for mbo in mbos if item.MBO_min < mbo]
                else:
                    raise ValueError("Wrong type of max_mayer_bond_order!!!!")
            else:
                mbos = [mbo for mbo in mbos if item.MBO_max > mbo
                        and item.MBO_min < mbo]

            self._atoms_names.update({item.id: (item.atom_1, item.atom_2)})
            histogram = cls._Histogram.calculate(mbos, bins)
            self.histograms.update({item.id: histogram})
        return self

    def remove_duplicates(self):
        """Removes duplicates, which have the same atoms symbols.
            Use when you perform calculations for list[PairOfAtoms]
            when ids are different for the same atoms pairs.
        """

        temp = []
        for key in list(self._atoms_names.keys()):
            if self._atoms_names[key] in temp:
                del self._atoms_names[key]
                del self.histograms[key]
            else:
                temp.append(self._atoms_names[key])

        return self

    def to_string(self) -> str:
        """Make string from HistogramsFromPairOfAtoms object

        Returns:
            **str**: String

        """
        string = ""
        for key, histogram in self.histograms.items():
            atom_id_1, atom_id_2 = self._atoms_names[key]
            string += histogram.to_string(key, atom_id_1, atom_id_2)

        return string


class CoordinationNumbersFromPairOfAtoms(Calculations, Statistics):
    """Calculate coordination numbers for list of pairs of atoms."""
    _CoordinationNumbers: type = CoordinationNumbers
    coordination_numbers: list[str, CoordinationNumbers]
    """**key** - bond_id, **value** - CoordinationNumbers object"""
    _atoms_names: dict[str, (str, str)]

    @classmethod
    def calculate(cls, pair_of_atoms: list[PairOfAtoms],
                  mayer_bond_orders: MayerBondOrders):
        """Calculate CoordinationNumbersFromPairOfAtoms object.

        Args:
            pair_of_atoms (list[PairOfAtoms]): list of PairOfAtoms objects.
            mayer_bond_orders (MayerBondOrders): MayerBondOrders object.

        Returns:
            **CoordinationNumbersFromPairOfAtoms**: CoordinationNumbersFromPairOfAtoms object.

        """
        self = cls()
        self.coordination_numbers = {}
        self._atoms_names = {}
        for item in pair_of_atoms:
            self._atoms_names.update({item.id: (item.atom_1, item.atom_2)})
            coordination = cls._CoordinationNumbers\
                .calculate(mayer_bond_orders,
                           item.atom_1, item.atom_2,
                           item.MBO_max, item.MBO_min,
                           item.id)
            self.coordination_numbers.update({item.id: coordination})
        return self

    def calculate_statistics(self):
        """Calculate statistic in **CoordinationNumbers** objects."""

        for keys in self.coordination_numbers.keys():
            self.coordination_numbers[keys].calculate_statistics()
        return self

    def to_string(self) -> str:
        """Make string from CoordinationNumbersFromPairOfAtoms object

        Returns:
            **str**: String

        """
        string = ""
        for coordination_numbers in self.coordination_numbers.values():
            string += coordination_numbers\
                .to_string()

        return string


class ConnectionsFromPairOfAtoms(Calculations):
    """Calculate connections for list of pairs of atoms."""
    _Connections: type = Connections
    connections: dict[str, Histogram]
    """**key** - bond_id, **value** - Connections object"""
    _atoms_names: dict[str, (str, str)]

    @classmethod
    def calculate(cls, pair_of_atoms: list[PairOfAtoms],
                  mayer_bond_orders: MayerBondOrders):
        """Calculate ConnectionsFromPairOfAtoms object.

        Args:
            pair_of_atoms (list[PairOfAtoms]): list of PairOfAtoms objects.
            mayer_bond_orders (MayerBondOrders): MayerBondOrders object.

        Returns:
            **ConnectionsFromPairOfAtoms**: ConnectionsFromPairOfAtoms object.

        """
        self = cls()
        self.connections = {}
        self._atoms_names = {}
        for item in pair_of_atoms:
            self._atoms_names.update({item.id: (item.atom_1, item.atom_2)})
            connections = cls._Connections\
                .calculate(mayer_bond_orders,
                           item.atom_1, pair_of_atoms)
            self.connections.update({item.id: connections})
        return self

    def to_string(self) -> str:
        """Make string from ConnectionsFromPairOfAtoms object

        Returns:
            **str**: String

        """
        string = ""
        for connections in self.connections.values():
            string += connections\
                .to_string()

        return string


class BondLengthFromPairOfAtoms(Calculations):
    """Calculate bonds lengths for list of pairs of atoms."""
    _BondLength: type = BondLength
    bond_lengths: dict[str, BondLength]
    """**key** - bond_id, **value** - BondLength object"""
    _atoms_names: dict[str, (str, str)]

    @classmethod
    def calculate(cls, pair_of_atoms: list[PairOfAtoms],
                  mayer_bond_orders: MayerBondOrders,
                  coordinates_of_atoms: CoordinatesOfAtoms) -> type:
        """Calculate BondLengthFromPairOfAtoms object.

        Args:
            pair_of_atoms (list[PairOfAtoms]): list of PairOfAtoms objects.
            mayer_bond_orders (MayerBondOrders): MayerBondOrders object.
            coordinates_of_atoms (CoordinatesOfAtoms): CoordinatesOfAtoms.

        Returns:
            **BondLengthFromPairOfAtoms**: BondLengthFromPairOfAtoms object.

        """
        self = cls()
        self.bond_lengths = {}
        self._atoms_names = {}
        for item in pair_of_atoms:
            self._atoms_names.update({item.id: (item.atom_1, item.atom_2)})
            bond_lengths = cls._BondLength\
                .calculate(mayer_bond_orders,
                           coordinates_of_atoms,
                           item.atom_1, item.atom_2,
                           item.MBO_max, item.MBO_min,
                           item.id)
            self.bond_lengths.update({item.id: bond_lengths})
        return self

    def to_string(self) -> str:
        """Make string from BondLengthFromPairOfAtoms object

        Returns:
            **str**: String

        """
        string = ""
        for bond_length in self.bond_lengths.values():
            string += bond_length.to_string()

        return string


class CovalenceFromPairOfAtoms(Calculations, _FromPairOfAtoms):
    """Covalence for list of pairs of atoms."""
    _Covalence: type = Covalence
    covalence: dict[str, Covalence]
    """**key** - atom_name, **value** - Covalence object"""
    _atoms_names: list[str]

    @classmethod
    def calculate(cls, pair_of_atoms: list[PairOfAtoms],
                  mayer_bond_orders: MayerBondOrders):
        """Calculate CovalenceFromPairOfAtoms object.

        Args:
            pair_of_atoms (list[PairOfAtoms]): list of PairOfAtoms objects.
            mayer_bond_orders (MayerBondOrders): MayerBondOrders object.

        Returns:
            **CovalenceFromPairOfAtoms**: CovalenceFromPairOfAtoms object.

        """
        self = cls()
        self.covalence = {}
        self._atoms_names = []

        unique_atom_symbols = super()\
            ._get_unique_atom_symbols(pair_of_atoms)

        for item in unique_atom_symbols:
            self._atoms_names.append(item)
            covalence = cls._Covalence\
                .calculate(mayer_bond_orders, item)
            self.covalence.update({item: covalence})
        return self

    def to_string(self) -> str:
        """Make string from CovalenceFromPairOfAtoms object

        Returns:
            **str**: String

        """
        string = ""
        for connections in self.covalence.values():
            string += connections\
                .to_string()

        return string


class QiUnitsFromPairOfAtoms(Calculations, Statistics):
    """Calculate Qⁱ for list of pairs of atoms."""
    _QiUnits: type = QiUnits
    qi_units: dict[str, QiUnits]
    """**key** - bond_id, **value** - QiUnits object"""
    _atoms_names: list[str]

    @classmethod
    def calculate(cls, pair_of_atoms: list[PairOfAtoms],
                  mayer_bond_orders: MayerBondOrders):
        """Calculate QiUnitsFromPairOfAtoms object.

        Args:
            pair_of_atoms (list[PairOfAtoms]): list of PairOfAtoms objects.
            mayer_bond_orders (MayerBondOrders): MayerBondOrders object.

        Returns:
            **QiUnitsFromPairOfAtoms**: QiUnitsFromPairOfAtoms object.

        """
        self = cls()
        self.qi_units = {}
        self._atoms_names = {}
        for item in pair_of_atoms:
            self._atoms_names.update({item.id: (item.atom_1, item.atom_2)})
            qi_units = cls._QiUnits\
                .calculate(mayer_bond_orders,
                           item.atom_1, item.atom_2,
                           item.MBO_max, item.MBO_min,
                           item.id)

            self.qi_units.update({item.id: qi_units})
        return self

    def calculate_statistics(self):
        """Calculate statistic in **QiUnits** objects."""

        for keys in self.qi_units.keys():
            self.qi_units[keys].calculate_statistics()
        return self

    def to_string(self) -> str:
        """Make string from **QiUnitsFromPairOfAtoms** object

        Returns:
            **str**: String

        """
        string = ""
        for qi_units in self.qi_units.values():
            string += qi_units\
                .to_string()

        return string
