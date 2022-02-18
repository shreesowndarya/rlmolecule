import pytest
import rdkit
from rlmolecule.builder import MoleculeBuilder
from rlmolecule.molecule_state import MoleculeState


@pytest.fixture
def builder() -> MoleculeBuilder:
    return MoleculeBuilder(max_atoms=5)


@pytest.fixture
def propane(builder: MoleculeBuilder) -> MoleculeState:
    return MoleculeState(
        rdkit.Chem.MolFromSmiles("CCC"), builder=builder, force_terminal=False
    )


def test_root(propane: MoleculeState):
    root = propane.get_root()
    assert root.smiles == "C"


def test_next_actions(propane: MoleculeState):
    next_actions = propane.next_actions
    butanes = list(filter(lambda x: x.smiles == "CCCC", next_actions))
    assert len(butanes) == 1
    assert butanes[0].forced_terminal is False
    assert next_actions[-1].forced_terminal is True
