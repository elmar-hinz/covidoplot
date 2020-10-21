from .lib.commons import plot_helper_comparism

label_confirmed = 'bestätigte Fälle'


def plot(cdf, type, child_type, key):
    plot_helper_comparism(
        cdf, type, child_type, key,
        'confirmed',
        label_confirmed,
        'Absolute Fallzahlen',
        'absolute'
    )

