"""Auto-generated file, do not edit by hand. BR metadata"""
from ..phonemetadata import NumberFormat, PhoneNumberDesc, PhoneMetadata

PHONE_METADATA_BR = PhoneMetadata(id='BR', country_code=55, international_prefix='00(?:1[245]|2[1-35]|31|4[13]|[56]5|99)',
    general_desc=PhoneNumberDesc(national_number_pattern='(?:[1-46-9]\\d\\d|5(?:[0-46-9]\\d|5[0-46-9]))\\d{8}|[1-9]\\d{9}|[3589]\\d{8}|[34]\\d{7}', possible_length=(8, 9, 10, 11)),
    fixed_line=PhoneNumberDesc(national_number_pattern='(?:[14689][1-9]|2[12478]|3[1-578]|5[13-5]|7[13-579])[2-5]\\d{7}', example_number='1123456789', possible_length=(10,), possible_length_local_only=(8,)),
    mobile=PhoneNumberDesc(national_number_pattern='(?:[14689][1-9]|2[12478]|3[1-578]|5[13-5]|7[13-579])(?:7|9\\d)\\d{7}', example_number='11961234567', possible_length=(10, 11), possible_length_local_only=(8, 9)),
    toll_free=PhoneNumberDesc(national_number_pattern='800\\d{6,7}', example_number='800123456', possible_length=(9, 10)),
    premium_rate=PhoneNumberDesc(national_number_pattern='300\\d{6}|[59]00\\d{6,7}', example_number='300123456', possible_length=(9, 10)),
    shared_cost=PhoneNumberDesc(national_number_pattern='(?:30[03]\\d{3}|4(?:0(?:0\\d|20)|370))\\d{4}|300\\d{5}', example_number='40041234', possible_length=(8, 10)),
    no_international_dialling=PhoneNumberDesc(national_number_pattern='30(?:0\\d{5,7}|3\\d{7})|40(?:0\\d|20)\\d{4}|800\\d{6,7}', possible_length=(8, 9, 10)),
    national_prefix='0',
    national_prefix_for_parsing='(?:0|90)(?:(1[245]|2[1-35]|31|4[13]|[56]5|99)(\\d{10,11}))?',
    national_prefix_transform_rule='\\2',
    number_format=[NumberFormat(pattern='(\\d{3,6})', format='\\1', leading_digits_pattern=['1(?:1[25-8]|2[357-9]|3[02-68]|4[12568]|5|6[0-8]|8[015]|9[0-47-9])|321|610']),
        NumberFormat(pattern='(\\d{4})(\\d{4})', format='\\1-\\2', leading_digits_pattern=['300|4(?:0[02]|37)', '4(?:02|37)0|[34]00']),
        NumberFormat(pattern='(\\d{4})(\\d{4})', format='\\1-\\2', leading_digits_pattern=['[2-57]', '[2357]|4(?:[0-24-9]|3(?:[0-689]|7[1-9]))']),
        NumberFormat(pattern='(\\d{3})(\\d{2,3})(\\d{4})', format='\\1 \\2 \\3', leading_digits_pattern=['(?:[358]|90)0'], national_prefix_formatting_rule='0\\1'),
        NumberFormat(pattern='(\\d{5})(\\d{4})', format='\\1-\\2', leading_digits_pattern=['9']),
        NumberFormat(pattern='(\\d{2})(\\d{4})(\\d{4})', format='\\1 \\2-\\3', leading_digits_pattern=['(?:[14689][1-9]|2[12478]|3[1-578]|5[13-5]|7[13-579])[2-57]'], national_prefix_formatting_rule='(\\1)', domestic_carrier_code_formatting_rule='0 $CC (\\1)'),
        NumberFormat(pattern='(\\d{2})(\\d{5})(\\d{4})', format='\\1 \\2-\\3', leading_digits_pattern=['[16][1-9]|[2-57-9]'], national_prefix_formatting_rule='(\\1)', domestic_carrier_code_formatting_rule='0 $CC (\\1)')],
    intl_number_format=[NumberFormat(pattern='(\\d{4})(\\d{4})', format='\\1-\\2', leading_digits_pattern=['300|4(?:0[02]|37)', '4(?:02|37)0|[34]00']),
        NumberFormat(pattern='(\\d{3})(\\d{2,3})(\\d{4})', format='\\1 \\2 \\3', leading_digits_pattern=['(?:[358]|90)0']),
        NumberFormat(pattern='(\\d{2})(\\d{4})(\\d{4})', format='\\1 \\2-\\3', leading_digits_pattern=['(?:[14689][1-9]|2[12478]|3[1-578]|5[13-5]|7[13-579])[2-57]']),
        NumberFormat(pattern='(\\d{2})(\\d{5})(\\d{4})', format='\\1 \\2-\\3', leading_digits_pattern=['[16][1-9]|[2-57-9]'])],
    mobile_number_portable_region=True)
