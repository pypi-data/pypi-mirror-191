from vbelt.outcar_utils import get_species, get_val


class Potcar:
    """A small subset of the informations stored in POTCAR.

    Only for reading purpose, most of the information is ignored.
    """

    def __init__(self, species):
        self.species = species

    @classmethod
    def from_file(self, path):
        species_info = []

        with open(path) as f:
            while True:
                name = get_species(f)

                if name is None:
                    break

                pomass_and_zval = get_val(
                    f, before="POMASS", after="mass", expect_equal=True
                )
                a, b = pomass_and_zval.split(";")
                mass = float(a.strip())
                zval = float(b.split("=")[1].strip())

                enlimits = get_val(f, before="ENMAX", after="eV", expect_equal=True)

                a, b = enlimits.split(";")
                enmax = float(a.strip())
                enmin = float(b.split("=")[1].strip())

                species_info.append(
                    {
                        "name": name,
                        "mass": mass,
                        "valence": zval,
                        "enmin": enmin,
                        "enmax": enmax,
                    }
                )

        return Potcar(species_info)


def predict_nelect(poscar, potcar):
    return sum(sp["valence"] * len(poscar.species[sp["name"]]) for sp in potcar.species)
