import sys
from shlex import quote

import numpy as np

from pysh import cd, mkdir, cp, in_dir, ensure_abs_path, ls, cat

from ase.build import sort
from ase.dft.kpoints import monkhorst_pack

import chevron

from . import poscar as ps
from .misc import electronegativity
from .jobtool import calc_nband, calc_par


class Batch:
    def __init__(self):
        self.potcars = ""
        self.batch_preset = "medium2"
        self.ncpu = 1
        self.ncpu_per_node = 1

    def gencalcs(self, name, bundle_name, computations, encut, sc, make_faulted_cell):
        sc = sort(sc, tags=[electronegativity[at.symbol] for at in sc])
        faulted = make_faulted_cell(sc)
        self.prepare_bundle(sc, faulted, name, bundle_name, encut, computations)

    def prepare_bundle(self, sc, faulted, name, bundle_name, encut, computations):
        d = ensure_abs_path(bundle_name)
        mkdir(d)
        with in_dir(d):
            sc.write("sc.POSCAR", format="vasp")
            faulted.write("faulted.POSCAR", format="vasp")

            nions = len(faulted)
            nelect = self.makepot(faulted, "POTCAR")

            magmom = len(sc)

            print("NIONS", nions)
            print("NELECT", nelect)

            for exc, kden, sp, d, after, cmds in map(
                lambda p: (p[0], p[1], p[2], ensure_abs_path(p[3]), p[4], p[5]),
                computations,
            ):
                mkdir(d)

                # Prepare k-mesh
                kpoints = monkhorst_pack(kden)

                if sp:
                    # Shift to include Gamma
                    kpoints -= min(kpoints, key=lambda v: np.linalg.norm(v)).reshape(
                        (1, 3)
                    )

                kpoints = np.fmod(kpoints + 0.5, 1.0) - 0.5
                ibz = apply_symmetries(kpoints)
                nkpt = len(ibz)

                kpar, ncore = calc_par(nkpt, self.ncpu, self.ncpu_per_node)
                nband = calc_nband(nions, magmom, nelect, kpar, self.ncpu, ncore, 2)

                report(d, self.ncpu, nkpt, kpar, ncore, nband)

                cp("faulted.POSCAR", d.add("POSCAR"))
                cp("POTCAR", d.add("POTCAR"))

                with in_dir(d):
                    if exc:
                        ferwe, ferdo = make_fer(nelect, nband, nkpt, exc)

                    with open("INCAR", "w") as f:
                        f.write(
                            chevron.render(
                                tmpl_sp if sp else tmpl_opt,
                                {
                                    "encut": encut,
                                    "name": name,
                                    "ncore": ncore,
                                    "kpar": kpar,
                                    "base": not exc,
                                    "excited": {
                                        "ferwe": ferwe,
                                        "ferdo": ferdo,
                                    }
                                    if exc
                                    else False,
                                },
                            )
                        )

                    if sp:
                        cmt = f"G-centered {kden}"
                    else:
                        cmt = f"MP {kden}"

                    with open("KPOINTS", "w") as f:
                        f.write(
                            chevron.render(
                                tmpl_kpt,
                                {
                                    "comment": cmt,
                                    "nkpt": nkpt,
                                    "kpts": "\n".join(
                                        f"{x:-13.10f} {y:-13.10f} {z:-13.10f} {w}"
                                        for (x, y, z), w in ibz.items()
                                    ),
                                },
                            )
                        )

                    with open("setup_job.sh", "w") as f:
                        afters = " ".join(f"--after {p}" for p in after)
                        type_ = "" if sp else "--optim"
                        cmd = " ".join(f"--cmd {quote(cmd)}" for cmd in cmds)
                        nnode = self.ncpu // self.ncpu_per_node
                        print(
                            f"batch-vasp --preset {self.batch_preset} --nn {nnode} {afters} {type_} {cmd}",
                            file=f,
                        )

    def makepot(self, struct, target):
        species = []
        pops = []

        # Collect species even if some species repeated not consecutive
        for at in struct:
            if not species or species[-1] != at.symbol:
                species.append(at.symbol)
                pops.append(1)
            else:
                pops[-1] += 1

        target_ = ensure_abs_path(target)

        nelect = 0

        with in_dir(self.potcars):
            for i, (s, pop) in enumerate(zip(species, pops)):
                candidates = list(ls().name(s + "(_.*|)").sort())

                if len(candidates) == 1:
                    p = candidates[0]
                else:
                    print("POTCAR selection.")
                    print(
                        " ".join(
                            sp if i != j else f">{sp}<" for j, sp in enumerate(species)
                        )
                    )
                    p = ask("Select the prefered potential.", candidates)

                cat(p, target_, overwrite=False)

                nelect += pop * get_zval(p)

        return nelect


def apply_symmetries(kpoints):
    s = {}

    for v in kpoints:
        if tuple(-v) not in s:
            s[tuple(v)] = 1
        else:
            s[tuple(-v)] += 1

    return s


def get_zval(p):
    with open(p, "r") as f:
        for line in f:
            if "ZVAL" in line:
                return int(float(line.split("ZVAL")[1].split()[1]))


def calc_magmom_col(struct):
    """Compute initial spin in collinear computation."""

    def at_unpaired(at):
        nelect = at.number
        # keep only valence
        for shell in shells:
            if nelect < 2 * shell:
                valence_shell = shell
                break
            nelect -= 2 * shell

        # Maximize spin
        if nelect <= valence_shell:
            return nelect
        else:
            return 2 * valence_shell - nelect

    return sum(at_unpaired(at) for at in struct) / 2.0


def make_fer(nelect, nband, nkpt, excite):
    vbm_down = nelect // 2
    vbm_up = nelect - vbm_down

    print("nelect", nelect)
    print("vbm_up", vbm_up)
    print("vbm_down", vbm_down)

    occ_0_up = [1] * vbm_up + [0] * (nband - vbm_up)
    occ_0_down = [1] * vbm_down + [0] * (nband - vbm_down)

    occ_up, occ_down = excite(occ_0_up, occ_0_down, vbm_up - 1, vbm_down - 1)

    one_k_up = fortran_array(occ_up)
    one_k_down = fortran_array(occ_down)

    return " ".join(one_k_up for _ in range(nkpt)), " ".join(
        one_k_down for _ in range(nkpt)
    )


def fortran_array(lst):
    assert all(isinstance(i, int) for i in lst)

    elems = []

    prev = 0.5
    acc = 0
    for e in lst:
        if e == prev:
            acc += 1
        else:
            if acc:
                elems.append(f"{acc}*{float(prev):.01f}")
            prev = e
            acc = 1

    if acc:
        elems.append(f"{acc}*{float(prev):.01f}")

    return " ".join(elems)


def ask(msg, collection):
    print(msg)
    for i, elem in enumerate(collection, start=1):
        print(f"{i}. {elem}")

    res = ""
    while not res.isdecimal() or int(res) < 1 or int(res) > len(collection):
        res = input(f"Select an option (1 - {len(collection)}) > ")
        if not res:
            res = "1"

    return collection[int(res) - 1]


def report(d, ncpu, nkpt, kpar, ncore, nband):
    print("Computation at", d)
    print("NKPT", nkpt)
    print("KPAR", kpar)
    print("NCORE", ncore)
    print("NPAR", (ncpu // kpar) // ncore)
    print("NBAND", nband)
    print("")


size = {"s": 1, "p": 3, "d": 5, "f": 7}
shells = [size[s] for s in "1s2s2p3s3p4s3d4p5s4d5p6s4f5d3p7s5f6d7p"[1::2]]


tmpl_sp = """\
SYSTEM = {{name}}

PREC = Accurate
ENCUT = {{encut}}
LREAL = .FALSE.
ISPIN = 2

NSW = 0
EDIFF = 1.0E-7
{{#base}}

ISMEAR = 0
SIGMA = 0.01
{{/base}}
{{#excited}}

ISMEAR = -2

FERWE = {{ferwe}}
FERDO = {{ferdo}}
{{/excited}}

KPAR = {{kpar}}
NCORE = {{ncore}}
"""

tmpl_opt = """\
SYSTEM = {{name}}

PREC = Normal
ENCUT = {{encut}}
LREAL = Auto
ISPIN = 2

ISYM = 0

NSW = 100
EDIFF = 1.0E-5
EDIFFG = -1.0E-2

ISIF = 2
IBRION = 2
{{#base}}

ISMEAR = 0
SIGMA = 0.05
{{/base}}
{{#excited}}

ISMEAR = -2

FERWE = {{ferwe}}
FERDO = {{ferdo}}
{{/excited}}

KPAR = {{kpar}}
NCORE = {{ncore}}
"""

tmpl_kpt = """\
{{comment}}
{{nkpt}}
Reciprocal
{{kpts}}
"""
