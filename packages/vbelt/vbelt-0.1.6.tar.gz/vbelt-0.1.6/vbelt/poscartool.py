"""A set of useful tools to manipulate VASP's POSCAR files.
"""
import re

from .script_utils import (
    MultiCmd,
    positional,
    flag,
    optional,
    error_catch,
    error,
    rest,
)

poscartool = MultiCmd(description=__doc__)


@poscartool.subcmd(
    positional("POSCAR", default="POSCAR", type=str, help="POSCAR file to nudge."),
    positional("OUTCAR", default="OUTCAR", type=str, help="VASP output file."),
    optional(
        "--amplitude",
        "-a",
        type=float,
        default=0.01,
        help="Total amplitude of the nudge in the forces direction.",
    ),
    optional(
        "--rattle",
        "-r",
        type=float,
        default=0.0,
        help="Add a random displacement of total amplitude FLOAT to the nudge.",
    ),
    flag(
        "--inplace",
        "-i",
        help="Directly overwrite the POSCAR instead of creating a new file with .nudge suffix.",
    ),
    optional(
        "--dest", "-o", type=str, default=None, help="Optional destination POSCAR"
    ),
    flag(
        "--direct", "-d", help="Write POSCAR in reduced coordinates."
    ),
)
def nudge(opts):
    from .forces import read_forces
    from .poscar import nudge

    with error_catch(), open(opts.outcar) as f:
        _, forces, _ = read_forces(f)

    if opts.dest is not None:
        dest = opts.dest
    elif opts.inplace:
        dest = opts.poscar
    else:
        dest = opts.poscar + ".nudge"

    with error_catch():
        nudge(opts.poscar, dest, forces, A=opts.amplitude, rattle=opts.rattle, cartesian=opts.cartesian)

    return 0


@poscartool.subcmd(
    positional("POSCAR", help="Source file."),
    positional("DEST", default=None, help="Destionation file."),
)
def xyz(opts):
    from .poscar import Poscar

    if opts.dest:
        dest = opts.dest
    else:
        dest = opts.poscar + ".xyz"

    poscar = Poscar.from_file(opts.poscar)

    with error_catch(), open(dest, "w") as f:
        print(len(poscar.raw), file=f)

        print(poscar.system_name, file=f)

        for sp, pos in poscar.species.items():
            for p in pos:
                print(sp, *p, file=f)


@poscartool.subcmd(
    positional("POSCAR", type=str, help="POSCAR file to observe."),
    positional("ATOM1", type=str, help="First atom."),
    positional(
        "ATOM2",
        default=None,
        type=str,
        help="Second atom, if ommited all atoms are considered.",
    ),
    optional(
        "--max", "-m", default=None, type=int, help="Maximum number of distances shown."
    ),
    flag("--raw", help="Just ouput values in A."),
)
def dist(opts):
    from .poscar import distance, Poscar

    poscar = Poscar.from_file(opts.poscar)
    at1 = parse_spec(poscar, opts.atom1)
    sp1 = spec(poscar, at1)

    if opts.atom2 is None:
        with error_catch():
            dists = [
                (distance(poscar, at1, (sp, i)), spec(poscar, (sp, i)))
                for sp, p in poscar.species.items()
                for i in range(len(p))
            ]

        dists.sort()

        if opts.max is not None:
            dists = dists[: opts.max]

        for d, sp in dists:
            if sp == sp1:
                continue
            if opts.raw:
                print(d)
            else:
                bond = f"{sp1}--{sp}"
                print(f"{bond:12}: {d: 9.5f} A")
    else:
        (s2, i2) = at2 = parse_spec(poscar, opts.atom2)

        if i2 is None:
            with error_catch():
                dists = [
                    (distance(poscar, at1, (s2, i)), spec(poscar, (s2, i)))
                    for i in range(len(poscar.species[s2]))
                ]

            dists.sort()

            if opts.max is not None:
                dists = dists[: opts.max]

            for d, sp in dists:
                if sp == sp1:
                    continue
                if opts.raw:
                    print(d)
                else:
                    bond = f"{sp1}--{sp}"
                    print(f"{bond:12}: {d: 9.5f} A")
        else:
            sp2 = spec(poscar, at2)
            d = distance(poscar, at1, at2)
            if opts.raw:
                print(d)
            else:
                print(f"{sp1}--{sp2}: {d:0.5f} A")


@poscartool.subcmd(
    positional("POSCAR", type=str, help="POSCAR file to observe."),
    positional("ATOM", type=str, help="Investigated atom."),
    positional("SPECIES", type=str, help="Coordinating species."),
    optional("--method", "-m", default="econ", help="Computation method."),
)
def coord(opts):
    """Evalueate a coordination number for a given atom and a coordinating species."""
    from .poscar import Poscar, coord_methods

    poscar = Poscar.from_file(opts.poscar)
    at = parse_spec(poscar, opts.atom)

    fn = coord_methods.get(opts.method, None)

    if fn is None:
        error(f"Unkown method {opts.method}, try one of {list(coord_methods.keys())}.")

    with error_catch():
        coord = fn(poscar, at, opts.species.split(","))

    print(f"{coord:0.03f}")


@poscartool.subcmd(
    positional("POSCAR1", help="Displaced positions."),
    positional("POSCAR2", help="Reference positions."),
    optional("--ref", "-r", default=None, help="Atom to consider fixed."),
    flag("--direct", "-d", help="Output in lattice coordinates."),
    flag("--no-center", "-C", help="Do not force the mean displacement to be null."),
    rest("ATOMS", default=[], help="Atoms to consider."),
)
def disp(opts):
    """Compute the displacement between two structures."""
    from .poscar import get_disp, Poscar
    import numpy as np

    poscar1 = Poscar.from_file(opts.poscar1)
    poscar2 = Poscar.from_file(opts.poscar2)

    if opts.ref is not None:
        with error_catch():
            sp, i = parse_spec(poscar1, opts.ref)

        offset = poscar1.species[sp][i] - poscar2.species[sp][i]

        poscar1.raw = poscar1.raw - offset.reshape((1, 3))

    if not opts.atoms:
        ats = None
    else:
        ats = [parse_spec(poscar1, at) for at in opts.atoms]

    with error_catch():
        disps = get_disp(poscar1, poscar2, ats)

    norms = np.linalg.norm(disps, axis=-1)

    if not opts.no_center:
        disps -= np.sum(disps, axis=0)

    if opts.direct:
        disps = disps @ np.linalg.inv(poscar1.cell_parameters)

    if ats is None:
        ats = list(range(len(disps)))

    for at, (x, y, z), n in zip(ats, disps, norms):
        sp = spec(poscar1, at)
        print(f"{sp:<3}:", f"{x:9.05f}, {y:9.05f}, {z:9.05f} ({n:9.05f} A)")


@poscartool.subcmd(
    positional("POSCAR", help="Positions to process."),
    optional("--dest", "-o", default="POSCAR.sub", help="Displaced positions."),
    optional("--ref", "-r", default=None, help="Reference atom to group around."),
    optional("--offset", "-s", default=None, help="Offset to apply to all atoms."),
    rest("ATOMS", help="Atoms to keep."),
)
def subset(opts):
    from itertools import groupby
    import numpy as np
    from .poscar import Poscar, periodic_diff

    poscar = Poscar.from_file(opts.poscar)

    with error_catch():
        ats = {
            k: [i for _, i in l]
            for k, l in groupby(
                (parse_spec(poscar, at) for at in opts.atoms),
                lambda p: p[0],
            )
        }
    if opts.ref is not None:
        with error_catch():
            rsp, ri = parse_spec(poscar, opts.ref)
            rpos = poscar.species[rsp][ri].reshape((1, 3))

    if opts.offset is not None:
        with error_catch():
            offset = np.array(opts.offset.split(","), dtype=float).reshape(1, 3)
    else:
        offset = np.zeros((1, 3))

    species = {}
    for k, l in ats.items():
        species[k] = np.ndarray((len(l), 3))

        for i, j in enumerate(l):
            species[k][i] = poscar.species[k][j]

        if opts.ref is not None:
            species[k] = periodic_diff(poscar.cell_parameters, species[k], rpos)

        species[k] += offset

    new = Poscar(poscar.cell_parameters, species)

    with error_catch():
        new.to_file(opts.dest)


def spec(poscar, sp):
    if isinstance(sp, int):
        i = sp
        for n in poscar._species_names:
            if i < len(poscar.species[n]):
                return f"{n}{i + 1}"
            else:
                i -= len(poscar.species[n])
        raise ValueError(f"{i} is larger than the number of atoms.")
    else:
        n, i = sp
        return f"{n}{i + 1}"


def parse_spec(poscar, spec):
    try:
        i = int(spec) - 1
    except ValueError:
        with error_catch():
            if m := re.match("([A-Z][a-z]?)([0-9]+)", spec):
                sp, i = m.groups()
                return (sp, int(i) - 1)
            elif m := re.match("([A-Z][a-z]?)", spec):
                (sp,) = m.groups()
                return (sp, None)
            else:
                raise ValueError(f"Unrecognize atom specification {spec}")
    for n in poscar._species_names:
        if i < len(poscar.species[n]):
            return (n, i)
        else:
            i -= len(poscar.species[n])
    raise ValueError(f"{i} is larger than the number of atoms.")
