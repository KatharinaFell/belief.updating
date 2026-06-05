from otree.api import DecimalUnit
class USD(DecimalUnit):
    input_places = 2
    input_unit_label = '$'
    currency_code = 'USD'
    storage_places = 4
    output_min_places = 2
    output_max_places = 2
class EUR(DecimalUnit):
    input_places = 2
    input_unit_label = '€'
    currency_code = 'EUR'
    storage_places = 4
    output_min_places = 2
    output_max_places = 2
