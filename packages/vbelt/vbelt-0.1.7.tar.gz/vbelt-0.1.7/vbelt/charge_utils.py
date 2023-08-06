from math import ceil
from itertools import islice
import numpy as np


class Charge:
    def __init__(self, poscar, chg, aug):
        self.poscar = poscar
        self.tot_chg = chg
        self.tot_aug = aug
        self.dif_part = None
        self.dif_nc_part = None

    def add_dif(self, chg, aug):
        self.dif_part = Charge(self.poscar, chg, aug)

    def add_nc_dif(self, x_dif, y_dif, z_dif):
        raise NotImplementedError("Non colinear density is not implemented yet.")

    @property
    def grid_shape(self):
        return self.tot_chg.shape

    @property
    def aug_shape(self):
        return [e.shape[0] for e in self.tot_aug]

    def __add__(self, other):
        if not isinstance(other, Charge):
            raise ValueError("Can only sum Charge instances together.")

        if self.grid_shape != other.grid_shape:
            raise ValueError("Incompatible grids.")

        aug_sums = []

        if self.aug_shape and other.aug_shape:
            if self.aug_shape != other.aug_shape:
                raise ValueError("Incompatible augmentation part shape.")

            for a, b in zip(self.tot_aug, other.tot_aug):
                aug_sums.append(a + b)

        chg_sum = Charge(self.poscar, self.tot_chg + other.tot_chg, aug_sums)

        if self.dif_part and other.dif_part:
            chg_sum.dif_part = self.dif_part + other.dif_part
        # TODO handle non colinear case

        return chg_sum

    def __sub__(self, other):
        return self + (-1.0 * other)

    def __mul__(self, other):
        return other * self

    def __rmul__(self, x):
        if not isinstance(x, (float, int, complex)):
            raise ValueError(
                "Charge instance can only be multiplied by a numerical scalar."
            )

        res = Charge(self.poscar, x * self.tot_chg, [x * e for e in self.tot_aug])

        if self.dif_part:
            res.dif_part = x * self.dif_part
        # TODO handle non colinear case

        return res

    def __div__(self, x):
        if not isinstance(x, (float, int, complex)):
            raise ValueError(
                "Charge instance can only be divided by a numerical scalar."
            )

        return (1.0 / x) * self

    def total_only(self):
        if self.dif_part is None and self.dif_nc_part is None:
            return self

        return Charge(self.tot_chg, self.tot_aug)

    @classmethod
    def read_from(cls, file):
        # Keep the poscar part in text form.
        poscar = []
        poscar.extend(islice(file, 6))
        head = next(file)
        poscar.append(head)

        nlines = sum(map(int, head.split()))

        poscar.extend(islice(file, nlines + 2))

        (regular_sum, augmented_sum, after) = read_channel(file)

        chg = cls(poscar, regular_sum, augmented_sum)

        dif_data = []

        while after is not None:
            (regular_dif, augmented_dif, after) = read_channel(file, after)

            dif_data.append((regular_dif, augmented_dif))

        if len(dif_data) == 1:
            # Spin polarized
            chg.add_dif(*dif_data[0])
        elif len(dif_data) == 3:
            # Non colinear spin
            chg.add_nc_dif(*dif_data)

        return chg

    def write_to(self, file):
        file.writelines(self.poscar)

        write_channel(file, self)

        if self.dif_part:
            write_channel(file, self.dif_part)

    def split(self):
        "Split the Charge object into a spin up and a spin down object."
        if self.dif_part is None:
            raise ValueError("No spin related data available.")

        return 0.5 * (self + self.dif_part), 0.5 * (self - self.dif_part)


def read_channel(file, head=None):
    head_ = head or next(file)
    ngx, ngy, ngz = map(int, head_.split())
    regular_data = read_block(file, (ngx, ngy, ngz))

    after = next(file, None)

    augmented_part = []
    while after is not None:
        if after[:24] != "augmentation occupancies":
            break
        i, n = map(int, after[24:].split())

        proj_data = read_block(file, (n,))

        augmented_part.append(proj_data)

    while after is not None and after != head_:
        after = next(file, None)

    return (regular_data, augmented_part, after)


def read_block(file, shape):
    npts = prod(shape)
    line = next(file)
    l1 = line.split()

    nlines = ceil(npts / len(l1) - 1.0)

    # While this can seem a stupid way of writing this, it is actually
    # pretty fast because:
    # - one huge split is much faster than thousands of small ones
    # - the string->float is delegated to numpy in a single call
    block = line + " " + " ".join(islice(file, nlines))
    return np.array(block.split(), dtype=float).reshape(shape)


def write_channel(file, chg):
    fmt = " {: >4d}" * len(chg.tot_chg.shape)
    file.write(fmt.format(*chg.tot_chg.shape) + "\n")

    line = chg.tot_chg.reshape((-1,))

    write_block(file, line, " %+16.11E", 5)

    for i, d in chg.tot_aug:
        file.write(f"augmentation part {i:>3} {len(d):>3}\n")
        write_block(file, d, " %+13.7E", 5)


def write_block(file, data, fmt, stride):
    bound = stride * (len(data) // stride)
    well_shaped = data[:bound].reshape((-1, stride))

    np.savetxt(file, well_shaped, fmt=fmt, delimiter="")

    if bound < len(data):
        fmt = fmt * (len(data) - bound) + "\n"
        file.write(fmt % tuple(data[bound : bound + stride]))


def prod(numbers):
    t = 1
    for n in numbers:
        t *= n
    return t
