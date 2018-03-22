from math import pi, tan


def circ_to_rad(c):
    """
    circumference to radius
    """
    return (1.0 * c) / (2 * pi)


SOCCER = dict(
    cascade='detection/haarcascades/soccer.xml',
    size=5,
    min_weight_ounce=14,
    max_weight_ounce=16,
    min_weight_gram=396.893,
    max_weight_gram=453.592,
    min_circumference_inch=27,
    max_circumference_inch=28,
    min_circumference_cm=68.58,
    max_circumference_cm=71.12,
    min_radius_inch=circ_to_rad(27),
    max_radius_inch=circ_to_rad(28),
    min_radius_cm=circ_to_rad(68.58),
    max_radius_cm=circ_to_rad(71.12),
)

BASKETBALL = dict(
    cascade='detection/haarcascades/basketball.xml',
    size=7,
    min_weight_gram=567,
    max_weight_gram=650,
    min_circumference_cm=74.9,
    max_circumference_cm=78.0,
    min_radius_cm=circ_to_rad(74.9),
    max_radius_cm=circ_to_rad(78.0),
)

FOCAL_LENGTH = 1