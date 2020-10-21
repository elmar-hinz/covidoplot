from .lib.commons import plot_helper_comparism

label_confirmed_density = 'bestätigte Fälle je 100.000 Einwohner'

def plot(cdf, type, child_type, key):
    plot_helper_comparism(
        cdf, type, child_type, key,
        'density_of_cases',
        label_confirmed_density,
        'Relative Fallzahlen',
        'relative'
    )

