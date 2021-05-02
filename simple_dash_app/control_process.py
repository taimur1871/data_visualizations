# Multi-dropdown options
from controls import COUNTIES, WELL_STATUSES, WELL_TYPES

def controls():
    # Create controls
    county_options = [
        {"label": str(COUNTIES[county]), "value": str(county)} for county in COUNTIES
    ]

    well_status_options = [
        {"label": str(WELL_STATUSES[well_status]), "value": str(well_status)}
        for well_status in WELL_STATUSES
    ]

    well_type_options = [
        {"label": str(WELL_TYPES[well_type]), "value": str(well_type)}
        for well_type in WELL_TYPES
    ]

    return county_options, well_status_options, well_type_options