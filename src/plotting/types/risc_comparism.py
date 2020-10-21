from .lib.commons import plot_helper_comparism

label_illness_density = 'Aktiv Infizierte je 100.000 Einwohner'


def plot(cdf, type, child_type, key):
    plot_helper_comparism(
        cdf, type, child_type, key,
        'density_of_illness',
        label_illness_density,
        'Infektionsrisiko',
        'risc'
    )
