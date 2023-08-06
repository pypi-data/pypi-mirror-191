import sys
from itertools import product
import numpy as np
from .misc import electronegativity


def nudge(poscar_src, poscar_dest, forces, A=0.01, rattle=0.0, cartesian=True):
    src = Poscar.from_file(poscar_src)

    if src.raw.shape != forces.shape:
        raise ValueError("Incompatible shapes of forces and positions.")

    nudged = src.raw

    norm = np.linalg.norm(forces)

    if norm > 0:
        nudged += A * forces / norm

    if rattle > 0:
        # rd is a randomly distrbuted set of displacement with stronger
        # intensities where the forces are intense
        if norm > 0:
            weigths = np.linalg.norm(forces, axis=-1)
        else:
            weigths = np.ones((forces.shape[0],))
        rd = np.random.normal(size=(nudged.shape))
        rd *= weigths.reshape((-1, 1))
        rd /= np.linalg.norm(rd)

        nudged += rattle * rd

    src.raw = nudged
    src.to_file(poscar_dest, cartesian=cartesian)


def distance(poscar, i, j):
    sp, si = i
    pi = poscar.species[sp][si, :]

    sp, sj = j
    pj = poscar.species[sp][sj, :]

    return periodic_dist(poscar.cell_parameters, pi, pj)


def calc_econ(poscar, at, species):
    sp, j = at

    dists = np.array(
        [
            distance(poscar, at, (sp2, i))
            for sp2 in species
            for i in range(len(poscar.species[sp2]))
            if sp != sp2 or i != j
        ]
    )

    d_p = np.min(dists)

    eps = 1.0

    while eps > 1e-6:
        old_dp = d_p
        weights = np.exp(1.0 - (dists / d_p) ** 6)
        d_p = np.sum(dists * weights) / np.sum(weights)
        eps = abs(d_p - old_dp) / old_dp

    return np.sum(np.exp(1.0 - (dists / d_p) ** 6))


def calc_econ_tol(poscar, at, species, tol=0.5):
    sp, j = at

    dists = np.array(
        [
            distance(poscar, at, (sp2, i))
            for sp2 in species
            for i in range(len(poscar.species[sp2]))
            if sp != sp2 or i != j
        ]
    )

    d_p = np.min(dists)

    eps = 1.0

    while eps > 1e-6:
        old_dp = d_p
        weights = np.exp(1.0 - (dists / d_p) ** 6)
        d_p = np.sum(dists * weights) / np.sum(weights)
        eps = abs(d_p - old_dp) / old_dp

    return len(dists[np.exp(1.0 - (dists / d_p) ** 6) >= tol])


def periodic_dist(lattice, p1, p2):
    return np.min(
        np.linalg.norm([p1 - p2 - t for t in gen_translat(lattice)], axis=-1), axis=0
    )


def gen_translat(lattice: np.ndarray):
    """Generate all translations to adjacent cells

    :param lattice: np.ndarray([a, b, c]) first lattice parameter
    """
    for d in product((-1, 0, 1), (-1, 0, 1), (-1, 0, 1)):
        yield np.array(d).dot(lattice)


def periodic_diff(lattice, p1, p2):
    dp = p1 - p2
    d = np.array([dp - t for t in gen_translat(lattice)])  # shape (27, n, 3)
    norms = np.linalg.norm(d, axis=2)  # shape = (27, n)
    best_translat = np.argmin(norms, axis=0)  # shape = (n,)

    n = d.shape[1]
    return d[best_translat, list(range(n)), :]


def get_disp(poscar1, poscar2, atoms=None):
    poscar1.recenter()
    poscar2.recenter()

    if atoms is None:
        p1 = poscar1.raw
        p2 = poscar2.raw
    else:
        p1 = np.ndarray((len(atoms), 3))
        p2 = np.ndarray((len(atoms), 3))

        for i, (sp, j) in enumerate(atoms):
            p1[i] = poscar1.species[sp][j]
            p2[i] = poscar2.species[sp][j]

    return periodic_diff(poscar1.cell_parameters, p1, p2)


class Poscar:
    def __init__(self, cell_parameters, species, species_names=None):
        """Create a Poscar type object, storing unit cell infos.

        :param cell_parameters: a 3x3 np.array with lattice vectors in line
        :param species: a dict[str, np.array] where the key is the name of the
          species and the array list positions.
          WARNING: Positions are in cartesian representation, not in fractional
          representation. Unit is Angstrom.
        """
        self.cell_parameters = cell_parameters
        self.species = species
        self._system_name = None
        if species_names is None:
            self._species_names = sorted(
                self.species.keys(), key=lambda p: electronegativity[p]
            )
        else:
            self._species_names = list(species_names)

    @property
    def raw(self):
        return np.vstack([self.species[n] for n in self._species_names])

    @raw.setter
    def raw(self, raw_data):
        offset = 0
        for n in self._species_names:
            slc = slice(offset, offset + len(self.species[n]), 1)
            self.species[n] = raw_data[slc]
            offset += len(self.species[n])

    @property
    def system_name(self):
        if self._system_name:
            return self._system_name
        else:
            species = list(self.species.items())
            # sort by increasing electronegativity
            species.sort(key=lambda p: electronegativity[p[0]])
            return " ".join(f"{label}{len(pos)}" for label, pos in species)

    @system_name.setter
    def system_name(self, val):
        self._system_name = val if val is None else str(val)

    @classmethod
    def from_cell(cls, cell):
        species = {}
        positions = cell.positions
        accum = 0
        for name, number in zip(cell.atoms_types, cell.nb_atoms):
            species[name] = positions[accum : accum + number]
            accum += number

        species_names = list(cell.atoms_types)
        params = cell.cell_parameters

        return Poscar(params, species, species_names=species_names)

    @classmethod
    def from_file(cls, filename, recenter=True):
        with open(filename) as f:
            next(f)  # system name
            fac = float(next(f))
            params = fac * np.array(
                [
                    np.array(l.strip().split(), dtype="float")
                    for _, l in zip(range(3), f)
                ]
            )

            labels = next(f).strip().split()
            atoms_pop = list(map(int, next(f).strip().split()))
            if len(labels) != len(atoms_pop):
                raise ValueError(f"{filename} is not a coherent POSCAR file.")

            mode = next(f).strip()[0].lower()

            species = {}
            if mode == "d":
                for spec, n in zip(labels, atoms_pop):
                    if spec in species:
                        raise NotImplementedError(
                            "Repeated non contiguous species block is not suppoerted yet."
                        )
                    pos = []
                    for _, line in zip(range(n), f):
                        ls = line.strip()
                        if not ls:
                            raise ValueError(
                                f"{filename} is not a coherent POSCAR file."
                            )
                        x, y, z, *_ = ls.split()
                        pos.append(np.array([x, y, z], dtype="float").dot(params))
                    species[spec] = np.array(pos)
            else:
                for spec, n in zip(labels, atoms_pop):
                    if spec in species:
                        raise NotImplementedError(
                            "Repeated non contiguous species block is not suppoerted yet."
                        )
                    pos = []
                    for _, line in zip(range(n), f):
                        ls = line.strip()
                        if not ls:
                            raise ValueError(
                                f"{filename} is not a coherent POSCAR file."
                            )
                        x, y, z, *_ = ls.split()
                        pos.append(np.array([x, y, z], dtype="float"))
                    species[spec] = np.array(pos)

        p = Poscar(params, species, species_names=labels)
        if recenter:
            p.recenter()
        return p

    def to_file(self, path="POSCAR", cartesian=True):
        """Write a POSCAR file

        The property system_name may be set to change the comment at the top of
        the file.
        :param path: path to the file to write
        :param cartesian: if True, write the file in cartesian representation,
          if False, write in fractional representation
        """
        with open(path, "w+") as out:
            species = [(n, self.species[n]) for n in self._species_names]

            out.write(f"{self.system_name}\n")
            out.write("1.0\n")
            np.savetxt(
                out, self.cell_parameters, "%15.12f", delimiter="\t", newline="\n"
            )

            out.write(" ".join(f"{name:6}" for name, _lst in species))
            out.write("\n")
            out.write(" ".join(f"{len(lst):6}" for _name, lst in species))
            out.write("\n")

            if cartesian:
                out.write("Cartesian\n")
                for _name, lst in species:
                    for pos in lst:
                        out.write("  ".join(f"{x:.8f}" for x in pos))
                        out.write("\n")
            else:
                out.write("Direct\n")
                inv_params = np.linalg.inv(self.cell_parameters)
                for _name, lst in species:
                    for pos in lst:
                        d_pos = pos.dot(inv_params)
                        out.write("  ".join(f"{x:.8f}" for x in d_pos))
                        out.write("\n")

    def recenter(self):
        for sp, pos in self.species.items():
            for v in self.cell_parameters:
                n = np.linalg.norm(v)
                d = v / n

                proj = pos @ d

                pos -= np.floor_divide(proj / n, 1.0).reshape((-1, 1)) * v.reshape(
                    (1, 3)
                )


coord_methods = {
    "econ": calc_econ,
    "econ_tol": calc_econ_tol,
}
