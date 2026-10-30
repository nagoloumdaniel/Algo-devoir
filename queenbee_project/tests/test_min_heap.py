"""Tests unitaires du tas binaire (T-W2)."""

import random

import pytest

from src.min_heap import BinaryHeap


def test_heapify_respecte_la_propriete_de_tas():
    heap = BinaryHeap.heapify([9, 4, 7, 1, 8, 2, 6, 3, 5])
    assert heap.is_valid(), f"Propriété de tas violée : {heap!r}"
    assert heap.size() == 9


def test_heapify_liste_vide():
    heap = BinaryHeap.heapify([])
    assert heap.is_empty()


def test_insert_met_a_jour_taille_et_propriete():
    heap = BinaryHeap()
    for i, value in enumerate([5, 3, 8, 1, 9, 2]):
        heap.insert(value)
        assert heap.size() == i + 1
        assert heap.is_valid(), f"Tas invalide après insert({value}) : {heap!r}"


def test_extract_min_renvoie_les_elements_dans_l_ordre():
    values = list(range(100))
    random.Random(42).shuffle(values)
    heap = BinaryHeap()
    for v in values:
        heap.insert(v)
    extracted = [heap.extract_min() for _ in range(len(values))]
    assert extracted == sorted(values)
    assert heap.is_empty()


def test_get_min_ne_modifie_pas_le_tas():
    heap = BinaryHeap.heapify([4, 2, 6])
    before = heap.to_list()
    assert heap.get_min() == 2
    assert heap.get_min() == 2
    assert heap.to_list() == before
    assert heap.size() == 3


def test_redimensionnement_conserve_les_elements():
    heap = BinaryHeap(capacity=2)
    for v in [10, 4, 7, 1, 3]:
        heap.insert(v)
    assert heap.capacity >= 5, "Le tableau interne aurait dû être agrandi"
    assert sorted(heap.to_list()) == [1, 3, 4, 7, 10]
    assert [heap.extract_min() for _ in range(5)] == [1, 3, 4, 7, 10]


def test_doublons_et_tuples():
    heap = BinaryHeap()
    for item in [(2.0, 0, "B"), (1.0, 1, "A"), (2.0, 2, "C"), (1.0, 3, "D")]:
        heap.insert(item)
    assert [heap.extract_min()[2] for _ in range(4)] == ["A", "D", "B", "C"]


def test_operations_sur_tas_vide_levent_une_erreur():
    heap = BinaryHeap()
    with pytest.raises(IndexError):
        heap.extract_min()
    with pytest.raises(IndexError):
        heap.get_min()


def test_capacite_invalide():
    with pytest.raises(ValueError):
        BinaryHeap(capacity=0)


def test_str_et_repr():
    heap = BinaryHeap.heapify([3, 1])
    assert str(heap) == "BinaryHeap([1, 3])"
    assert "size=2" in repr(heap)