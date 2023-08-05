"""Auto-generated file, do not edit by hand. AT metadata"""
from ..phonemetadata import NumberFormat, PhoneNumberDesc, PhoneMetadata

PHONE_METADATA_AT = PhoneMetadata(id='AT', country_code=43, international_prefix='00',
    general_desc=PhoneNumberDesc(national_number_pattern='1\\d{3,12}|2\\d{6,12}|43(?:(?:0\\d|5[02-9])\\d{3,9}|2\\d{4,5}|[3467]\\d{4}|8\\d{4,6}|9\\d{4,7})|5\\d{4,12}|8\\d{7,12}|9\\d{8,12}|(?:[367]\\d|4[0-24-9])\\d{4,11}', possible_length=(4, 5, 6, 7, 8, 9, 10, 11, 12, 13), possible_length_local_only=(3,)),
    fixed_line=PhoneNumberDesc(national_number_pattern='1(?:11\\d|[2-9]\\d{3,11})|(?:316|463|(?:51|66|73)2)\\d{3,10}|(?:2(?:1[467]|2[13-8]|5[2357]|6[1-46-8]|7[1-8]|8[124-7]|9[1458])|3(?:1[1-578]|3[23568]|4[5-7]|5[1378]|6[1-38]|8[3-68])|4(?:2[1-8]|35|7[1368]|8[2457])|5(?:2[1-8]|3[357]|4[147]|5[12578]|6[37])|6(?:13|2[1-47]|4[135-8]|5[468])|7(?:2[1-8]|35|4[13478]|5[68]|6[16-8]|7[1-6]|9[45]))\\d{4,10}', example_number='1234567890', possible_length=(4, 5, 6, 7, 8, 9, 10, 11, 12, 13), possible_length_local_only=(3,)),
    mobile=PhoneNumberDesc(national_number_pattern='6(?:5[0-3579]|6[013-9]|[7-9]\\d)\\d{4,10}', example_number='664123456', possible_length=(7, 8, 9, 10, 11, 12, 13)),
    toll_free=PhoneNumberDesc(national_number_pattern='800\\d{6,10}', example_number='800123456', possible_length=(9, 10, 11, 12, 13)),
    premium_rate=PhoneNumberDesc(national_number_pattern='(?:8[69][2-68]|9(?:0[01]|3[019]))\\d{6,10}', example_number='900123456', possible_length=(9, 10, 11, 12, 13)),
    shared_cost=PhoneNumberDesc(national_number_pattern='8(?:10|2[018])\\d{6,10}|828\\d{5}', example_number='810123456', possible_length=(8, 9, 10, 11, 12, 13)),
    voip=PhoneNumberDesc(national_number_pattern='5(?:0[1-9]|17|[79]\\d)\\d{2,10}|7[28]0\\d{6,10}', example_number='780123456', possible_length=(5, 6, 7, 8, 9, 10, 11, 12, 13)),
    national_prefix='0',
    national_prefix_for_parsing='0',
    number_format=[NumberFormat(pattern='(\\d{4})', format='\\1', leading_digits_pattern=['14']),
        NumberFormat(pattern='(\\d)(\\d{3,12})', format='\\1 \\2', leading_digits_pattern=['1(?:11|[2-9])'], national_prefix_formatting_rule='0\\1'),
        NumberFormat(pattern='(\\d{3})(\\d{2})', format='\\1 \\2', leading_digits_pattern=['517'], national_prefix_formatting_rule='0\\1'),
        NumberFormat(pattern='(\\d{2})(\\d{3,5})', format='\\1 \\2', leading_digits_pattern=['5[079]'], national_prefix_formatting_rule='0\\1'),
        NumberFormat(pattern='(\\d{6})', format='\\1', leading_digits_pattern=['[18]']),
        NumberFormat(pattern='(\\d{3})(\\d{3,10})', format='\\1 \\2', leading_digits_pattern=['(?:31|4)6|51|6(?:5[0-3579]|[6-9])|7(?:20|32|8)|[89]'], national_prefix_formatting_rule='0\\1'),
        NumberFormat(pattern='(\\d{4})(\\d{3,9})', format='\\1 \\2', leading_digits_pattern=['[2-467]|5[2-6]'], national_prefix_formatting_rule='0\\1'),
        NumberFormat(pattern='(\\d{2})(\\d{3})(\\d{3,4})', format='\\1 \\2 \\3', leading_digits_pattern=['5'], national_prefix_formatting_rule='0\\1'),
        NumberFormat(pattern='(\\d{2})(\\d{4})(\\d{4,7})', format='\\1 \\2 \\3', leading_digits_pattern=['5'], national_prefix_formatting_rule='0\\1')],
    intl_number_format=[NumberFormat(pattern='(\\d)(\\d{3,12})', format='\\1 \\2', leading_digits_pattern=['1(?:11|[2-9])']),
        NumberFormat(pattern='(\\d{3})(\\d{2})', format='\\1 \\2', leading_digits_pattern=['517']),
        NumberFormat(pattern='(\\d{2})(\\d{3,5})', format='\\1 \\2', leading_digits_pattern=['5[079]']),
        NumberFormat(pattern='(\\d{3})(\\d{3,10})', format='\\1 \\2', leading_digits_pattern=['(?:31|4)6|51|6(?:5[0-3579]|[6-9])|7(?:20|32|8)|[89]']),
        NumberFormat(pattern='(\\d{4})(\\d{3,9})', format='\\1 \\2', leading_digits_pattern=['[2-467]|5[2-6]']),
        NumberFormat(pattern='(\\d{2})(\\d{3})(\\d{3,4})', format='\\1 \\2 \\3', leading_digits_pattern=['5']),
        NumberFormat(pattern='(\\d{2})(\\d{4})(\\d{4,7})', format='\\1 \\2 \\3', leading_digits_pattern=['5'])],
    mobile_number_portable_region=True)
