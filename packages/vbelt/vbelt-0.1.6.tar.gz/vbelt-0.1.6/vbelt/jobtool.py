import os.path
from math import gcd, prod

from .script_utils import (
    MultiCmd,
    positional,
    optional,
    error_catch,
    error,
)

from .poscar import Poscar
from .potcar import Potcar, predict_nelect
from .incar import parse_incar
from .outcar_utils import get_int
from .misc import factorize


jobtool = MultiCmd(description=__doc__)


@jobtool.subcmd(
    positional("NCPU", type=int, help="Number of cores."),
    positional("PATH", default=".", type=str, help="Computation directory."),
    optional(
        "--nkpt",
        "-k",
        default="auto",
        help="Wether NKPT should be read from a previous computation of should be fixed arbitrary.",
    ),
)
def predict_nband(opts):
    with error_catch():
        incar = parse_incar(
            os.path.join(opts.path, "INCAR"),
            {
                "KPAR": {"cast": int, "default": 1},
                "NCORE": {"cast": int, "default": -1},
                "ISPIN": {"cast": int, "default": 1},
                "LSORBIT": {"cast": lambda v: v == ".TRUE.", "default": False},
                "NPAR": {"cast": int, "default": -1},
            },
        )

    with error_catch():
        p = Poscar.from_file(os.path.join(opts.path, "POSCAR"))

    with error_catch():
        pot = Potcar.from_file(os.path.join(opts.path, "POTCAR"))

    nelect = predict_nelect(p, pot)

    nions = len(p.raw)

    if incar["NCORE"] > 0:
        ncore = incar["NCORE"]
    elif incar["NPAR"] > 0:
        ncore = max((opts.ncpu // incar["KPAR"]) // incar["NPAR"], 1)
    else:
        ncore = 1

    nbands = calc_nband(
        nions,
        nions,
        nelect,
        incar["KPAR"],
        opts.ncpu,
        ncore,
        incar["ISPIN"],
        noncol=incar["LSORBIT"],
    )

    print(nbands)


@jobtool.subcmd(
    positional("NCPU", type=int, help="Number of cores."),
    positional("NCPU_PER_NODE", type=int, help="Number of core per nodes."),
    positional("PATH", default=".", type=str, help="Computation directory."),
    optional(
        "--nkpt",
        "-k",
        default="auto",
        help="Wether NKPT should be read from a previous computation of should be fixed arbitrary.",
    ),
)
def good_paral(opts):
    if opts.nkpt == "auto":
        try:
            with open(os.path.join(opts.path, "OUTCAR")) as f:
                nkpt = get_int(f, "NKPTS", after="k-points", expect_equal=True)
        except FileNotFoundError:
            error("Could not find a previous OUTCAR.")

        if nkpt is None:
            error("Could not find the value of NKPTS in OUTCAR.")

    else:
        nkpt = int(opts.nkpt)

    kpar, ncore = calc_par(nkpt, opts.ncpu, opts.ncpu_per_node)

    npar = max((opts.ncpu // kpar) // ncore, 1)

    print("KPAR =", kpar)
    print("NCORE =", ncore, "# or NPAR =", npar)


def calc_par(nkpt, ncpu, ncpu_per_node):
    kpar = gcd(nkpt, ncpu)

    if kpar > 6 or kpar == 1:
        kpar = max(k for k in range(1, min(7, nkpt)) if nkpt % k == 0)

    ncore_cpu = gcd(ncpu // kpar, ncpu_per_node)
    ncore_sqrt = int_sqrt(ncpu // kpar)

    ncore = min(ncore_cpu, ncore_sqrt)

    return kpar, ncore


def int_sqrt(n):
    prev = n

    for j in range(n, 0, -1):
        if n % j == 0:
            if j**2 == n:
                return j
            elif j**2 < n:
                return prev
            else:
                prev = j

    return prev


def calc_nband(nions, magmom, nelect, kpar, ncpu, ncore, ispin, noncol=False):
    if noncol:
        nmag = max(magmom)
    elif ispin > 1:
        nmag = int(magmom)
    else:
        nmag = 0

    ncpu_k = ncpu // kpar
    assert ncore <= ncpu_k
    npar = max(ncpu_k // ncore, 1)

    nmag = (nmag + 1) // 2

    nbands = (
        max(
            (nelect + 2) // 2 + max(nions // 2, 3),
            int(0.6 * nelect),
        )
        + nmag
    )

    if noncol:
        nbands *= 2

    return ((nbands + npar - 1) // npar) * npar
