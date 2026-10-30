"""
Tas binaire minimum (Min-Heap) implémenté de zéro — T-W2.

Aucune dépendance externe : le module ``heapq`` de Python n'est PAS utilisé.

Représentation
--------------
Le tas est un arbre binaire presque complet stocké dans un tableau :
    - la racine est à l'indice 0 ;
    - le parent de i est à (i - 1) // 2 ;
    - les enfants de i sont à 2i + 1 et 2i + 2.

Propriété de tas (min) : pour tout i > 0, tab[parent(i)] <= tab[i].
La racine contient donc toujours le plus petit élément.

Complexités
-----------
    insert       O(log n)   remontée (bubble_up) sur la hauteur de l'arbre
    extract_min  O(log n)   descente (bubble_down) sur la hauteur de l'arbre
    get_min      O(1)       lecture de la racine
    heapify      O(n)       construction ascendante (Floyd)
    size         O(1)

Le tableau interne a une capacité fixe qui double lorsqu'il est plein
(redimensionnement amorti en O(1) par insertion).

Exemple
-------
>>> h = BinaryHeap()
>>> h.insert(5); h.insert(1); h.insert(3)
>>> h.extract_min()
1
>>> h.get_min()
3
>>> len(h)
2
"""



class BinaryHeap:
    """Tas binaire minimum redimensionnable.

    Les éléments doivent être comparables entre eux avec ``<``.
    Pour Dijkstra on y range des tuples ``(distance, compteur, noeud)`` :
    la comparaison de tuples se fait sur la distance d'abord, et le compteur
    (unique) départage les égalités sans jamais avoir à comparer les noeuds.
    """

    DEFAULT_CAPACITY = 16

    def __init__(self, capacity=DEFAULT_CAPACITY):
        if capacity < 1:
            raise ValueError("La capacité initiale doit être >= 1")
        self._data = [None] * capacity   # tableau de taille fixe
        self._size = 0                   # nombre d'éléments réellement présents
        self.comparisons = 0             # compteur d'opérations (pour le benchmark)

    # ------------------------------------------------------------------ #
    # Accesseurs
    # ------------------------------------------------------------------ #
    def size(self):
        """Nombre d'éléments dans le tas. O(1)."""
        return self._size

    def __len__(self):
        return self._size

    def is_empty(self):
        """True si le tas ne contient aucun élément. O(1)."""
        return self._size == 0

    @property
    def capacity(self):
        """Capacité actuelle du tableau interne (avant prochain redimensionnement)."""
        return len(self._data)

    def get_min(self):
        """Renvoie le minimum SANS le retirer. O(1).

        >>> h = BinaryHeap(); h.insert(4); h.insert(2)
        >>> h.get_min()
        2
        """
        if self._size == 0:
            raise IndexError("get_min() sur un tas vide")
        return self._data[0]

    # ------------------------------------------------------------------ #
    # Opérations principales
    # ------------------------------------------------------------------ #
    def insert(self, item):
        """Ajoute un élément. O(log n) (O(1) amorti pour le redimensionnement).

        L'élément est placé dans la première case libre (dernière feuille),
        puis remonté tant qu'il est plus petit que son parent.
        """
        if self._size == len(self._data):
            self._resize(2 * len(self._data))
        self._data[self._size] = item
        self._size += 1
        self._bubble_up(self._size - 1)

    def extract_min(self):
        """Retire et renvoie le plus petit élément. O(log n).

        La racine est remplacée par la dernière feuille, qui est ensuite
        redescendue jusqu'à ce que la propriété de tas soit rétablie.
        """
        if self._size == 0:
            raise IndexError("extract_min() sur un tas vide")
        minimum = self._data[0]
        self._size -= 1
        last = self._data[self._size]
        self._data[self._size] = None        # libère la référence
        if self._size > 0:
            self._data[0] = last
            self._bubble_down(0)
        return minimum

    @classmethod
    def heapify(cls, items):
        """Construit un tas à partir d'un itérable en O(n) (algorithme de Floyd).

        On recopie les éléments tels quels, puis on fait descendre chaque
        noeud interne, du dernier vers la racine. La somme des hauteurs des
        noeuds d'un arbre presque complet est O(n), d'où le coût linéaire
        (contre O(n log n) pour n insertions successives).

        >>> BinaryHeap.heapify([5, 3, 8, 1]).extract_min()
        1
        """
        items = list(items)
        heap = cls(capacity=max(cls.DEFAULT_CAPACITY, len(items)))
        for i, item in enumerate(items):
            heap._data[i] = item
        heap._size = len(items)
        # Le dernier noeud interne est le parent de la dernière feuille.
        for i in range(heap._size // 2 - 1, -1, -1):
            heap._bubble_down(i)
        return heap

    # ------------------------------------------------------------------ #
    # Mécanique interne
    # ------------------------------------------------------------------ #
    def _less(self, i, j):
        """Compare data[i] < data[j] en comptant la comparaison."""
        self.comparisons += 1
        return self._data[i] < self._data[j]

    def _swap(self, i, j):
        self._data[i], self._data[j] = self._data[j], self._data[i]

    def _bubble_up(self, index):
        """Remonte l'élément en ``index`` tant qu'il est < à son parent."""
        while index > 0:
            parent = (index - 1) // 2
            if self._less(index, parent):
                self._swap(index, parent)
                index = parent
            else:
                break

    def _bubble_down(self, index):
        """Descend l'élément en ``index`` vers son plus petit enfant si besoin."""
        while True:
            left = 2 * index + 1
            right = left + 1
            smallest = index
            if left < self._size and self._less(left, smallest):
                smallest = left
            if right < self._size and self._less(right, smallest):
                smallest = right
            if smallest == index:
                break
            self._swap(index, smallest)
            index = smallest

    def _resize(self, new_capacity):
        """Recopie les éléments dans un tableau de ``new_capacity`` cases. O(n)."""
        new_data = [None] * new_capacity
        for i in range(self._size):
            new_data[i] = self._data[i]
        self._data = new_data

    # ------------------------------------------------------------------ #
    # Vérification et affichage
    # ------------------------------------------------------------------ #
    def is_valid(self):
        """Vérifie la propriété de tas sur tout le tableau (utile en test)."""
        for i in range(1, self._size):
            if self._data[i] < self._data[(i - 1) // 2]:
                return False
        return True

    def to_list(self):
        """Copie des éléments dans l'ordre du tableau interne (pas trié)."""
        return self._data[:self._size]

    def __str__(self):
        return f"BinaryHeap({self.to_list()})"

    def __repr__(self):
        return (f"BinaryHeap(size={self._size}, capacity={len(self._data)}, "
                f"data={self.to_list()})")