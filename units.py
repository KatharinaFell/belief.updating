from otree.api import DecimalUnit
class USD(DecimalUnit):
    input_places = 2
    input_unit_label = '$'
    currency_code = 'USD'
    storage_places = 4
    display_min_places = 2
    display_max_places = 2
class EUR(DecimalUnit):
    input_places = 2
    input_unit_label = '€'
    currency_code = 'EUR'
    storage_places = 4
    display_min_places = 2
    display_max_places = 2