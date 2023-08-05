"""Auto-generated file, do not edit by hand. IT metadata"""
from ..phonemetadata import NumberFormat, PhoneNumberDesc, PhoneMetadata

PHONE_METADATA_IT = PhoneMetadata(id='IT', country_code=39, international_prefix='00',
    general_desc=PhoneNumberDesc(national_number_pattern='0\\d{5,10}|1\\d{8,10}|3(?:[0-8]\\d{7,10}|9\\d{7,8})|(?:55|70)\\d{8}|8\\d{5}(?:\\d{2,4})?', possible_length=(6, 7, 8, 9, 10, 11, 12)),
    fixed_line=PhoneNumberDesc(national_number_pattern='0669[0-79]\\d{1,6}|0(?:1(?:[0159]\\d|[27][1-5]|31|4[1-4]|6[1356]|8[2-57])|2\\d\\d|3(?:[0159]\\d|2[1-4]|3[12]|[48][1-6]|6[2-59]|7[1-7])|4(?:[0159]\\d|[23][1-9]|4[245]|6[1-5]|7[1-4]|81)|5(?:[0159]\\d|2[1-5]|3[2-6]|4[1-79]|6[4-6]|7[1-578]|8[3-8])|6(?:[0-57-9]\\d|6[0-8])|7(?:[0159]\\d|2[12]|3[1-7]|4[2-46]|6[13569]|7[13-6]|8[1-59])|8(?:[0159]\\d|2[3-578]|3[1-356]|[6-8][1-5])|9(?:[0159]\\d|[238][1-5]|4[12]|6[1-8]|7[1-6]))\\d{2,7}', example_number='0212345678', possible_length=(6, 7, 8, 9, 10, 11)),
    mobile=PhoneNumberDesc(national_number_pattern='3[1-9]\\d{8}|3[2-9]\\d{7}', example_number='3123456789', possible_length=(9, 10)),
    toll_free=PhoneNumberDesc(national_number_pattern='80(?:0\\d{3}|3)\\d{3}', example_number='800123456', possible_length=(6, 9)),
    premium_rate=PhoneNumberDesc(national_number_pattern='(?:0878\\d{3}|89(?:2\\d|3[04]|4(?:[0-4]|[5-9]\\d\\d)|5[0-4]))\\d\\d|(?:1(?:44|6[346])|89(?:38|5[5-9]|9))\\d{6}', example_number='899123456', possible_length=(6, 8, 9, 10)),
    shared_cost=PhoneNumberDesc(national_number_pattern='84(?:[08]\\d{3}|[17])\\d{3}', example_number='848123456', possible_length=(6, 9)),
    personal_number=PhoneNumberDesc(national_number_pattern='1(?:78\\d|99)\\d{6}', example_number='1781234567', possible_length=(9, 10)),
    voip=PhoneNumberDesc(national_number_pattern='55\\d{8}', example_number='5512345678', possible_length=(10,)),
    voicemail=PhoneNumberDesc(national_number_pattern='3[2-8]\\d{9,10}', example_number='33101234501', possible_length=(11, 12)),
    no_international_dialling=PhoneNumberDesc(national_number_pattern='848\\d{6}', possible_length=(9,)),
    number_format=[NumberFormat(pattern='(\\d{4,5})', format='\\1', leading_digits_pattern=['1(?:0|9[246])', '1(?:0|9(?:2[2-9]|[46]))']),
        NumberFormat(pattern='(\\d{6})', format='\\1', leading_digits_pattern=['1(?:1|92)']),
        NumberFormat(pattern='(\\d{2})(\\d{4,6})', format='\\1 \\2', leading_digits_pattern=['0[26]']),
        NumberFormat(pattern='(\\d{3})(\\d{3,6})', format='\\1 \\2', leading_digits_pattern=['0[13-57-9][0159]|8(?:03|4[17]|9[2-5])', '0[13-57-9][0159]|8(?:03|4[17]|9(?:2|3[04]|[45][0-4]))']),
        NumberFormat(pattern='(\\d{4})(\\d{2,6})', format='\\1 \\2', leading_digits_pattern=['0(?:[13-579][2-46-8]|8[236-8])']),
        NumberFormat(pattern='(\\d{4})(\\d{4})', format='\\1 \\2', leading_digits_pattern=['894']),
        NumberFormat(pattern='(\\d{2})(\\d{3,4})(\\d{4})', format='\\1 \\2 \\3', leading_digits_pattern=['0[26]|5']),
        NumberFormat(pattern='(\\d{3})(\\d{3})(\\d{3,4})', format='\\1 \\2 \\3', leading_digits_pattern=['1(?:44|[679])|[378]']),
        NumberFormat(pattern='(\\d{3})(\\d{3,4})(\\d{4})', format='\\1 \\2 \\3', leading_digits_pattern=['0[13-57-9][0159]|14']),
        NumberFormat(pattern='(\\d{2})(\\d{4})(\\d{5})', format='\\1 \\2 \\3', leading_digits_pattern=['0[26]']),
        NumberFormat(pattern='(\\d{4})(\\d{3})(\\d{4})', format='\\1 \\2 \\3', leading_digits_pattern=['0']),
        NumberFormat(pattern='(\\d{3})(\\d{4})(\\d{4,5})', format='\\1 \\2 \\3', leading_digits_pattern=['3'])],
    intl_number_format=[NumberFormat(pattern='(\\d{2})(\\d{4,6})', format='\\1 \\2', leading_digits_pattern=['0[26]']),
        NumberFormat(pattern='(\\d{3})(\\d{3,6})', format='\\1 \\2', leading_digits_pattern=['0[13-57-9][0159]|8(?:03|4[17]|9[2-5])', '0[13-57-9][0159]|8(?:03|4[17]|9(?:2|3[04]|[45][0-4]))']),
        NumberFormat(pattern='(\\d{4})(\\d{2,6})', format='\\1 \\2', leading_digits_pattern=['0(?:[13-579][2-46-8]|8[236-8])']),
        NumberFormat(pattern='(\\d{4})(\\d{4})', format='\\1 \\2', leading_digits_pattern=['894']),
        NumberFormat(pattern='(\\d{2})(\\d{3,4})(\\d{4})', format='\\1 \\2 \\3', leading_digits_pattern=['0[26]|5']),
        NumberFormat(pattern='(\\d{3})(\\d{3})(\\d{3,4})', format='\\1 \\2 \\3', leading_digits_pattern=['1(?:44|[679])|[378]']),
        NumberFormat(pattern='(\\d{3})(\\d{3,4})(\\d{4})', format='\\1 \\2 \\3', leading_digits_pattern=['0[13-57-9][0159]|14']),
        NumberFormat(pattern='(\\d{2})(\\d{4})(\\d{5})', format='\\1 \\2 \\3', leading_digits_pattern=['0[26]']),
        NumberFormat(pattern='(\\d{4})(\\d{3})(\\d{4})', format='\\1 \\2 \\3', leading_digits_pattern=['0']),
        NumberFormat(pattern='(\\d{3})(\\d{4})(\\d{4,5})', format='\\1 \\2 \\3', leading_digits_pattern=['3'])],
    main_country_for_code=True,
    mobile_number_portable_region=True)
