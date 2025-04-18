def parsing_file(raw_data):
    parsed_data = []
    for _, row in raw_data.iterrows():
        swift_code = row['SWIFT CODE'].strip().upper()
        is_headquarter = swift_code.endswith('XXX')
        institution_code = swift_code[:8].upper()
        parsed_data.append({
            'country_iso2_code': row['COUNTRY ISO2 CODE'].strip().upper(),
            'swift_code': swift_code,
            'name': row['NAME'].strip(),
            'is_headquarter': is_headquarter,
            'institution_code': institution_code
            })
    return parsed_data