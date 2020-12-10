from typing import (
    Iterable,
    )

from rdkit.Chem.rdchem import Mol
from rdkit.Chem.rdmolfiles import (
    MolToSmiles,
    )

from alphazero.graph_node import GraphNode
from molecule_game.molecule_tools import (
    build_molecules,
    )


class MoleculeNode(GraphNode):
    
    def __init__(self, parent: 'MoleculeGame', molecule: Mol) -> None:
        self._parent: 'MoleculeGame' = parent
        self._molecule: Mol = molecule
        self._smiles = MolToSmiles(self._molecule)
    
    def __eq__(self, other: any) -> bool:
        return self._smiles == other._smiles
    
    def __hash__(self) -> int:
        return hash(self._smiles)
    
    def __repr__(self) -> str:
        return self._smiles
    
    def get_successors(self) -> Iterable['MoleculeNode']:
        # TODO: should these functions be brought into this class?
        num_atoms = self.molecule.GetNumAtoms()
        parent = self._parent
        molecule = self._molecule
        
        if num_atoms < self._parent.config.max_atoms:
            yield from (MoleculeNode(parent, molecule)
                        for molecule in build_molecules(molecule, **parent.config.build_kwargs))
    
    @property
    def smiles(self) -> str:
        return self._smiles
    
    @property
    def molecule(self) -> Mol:
        return self._molecule
    
    @property
    def parent(self) -> any:
        return self._parent
