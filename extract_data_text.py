import re


class YellowTextScrapper:
    """
    Extract data from the text
    """

    def __init__(self, path_to_text):
        self.path_to_text = path_to_text

    def get_number_pos(self):
        # open the files
        with open(self.path_to_text, 'r') as f:
            # loop through each line in corpus
            for line_i, line in enumerate(f):
                # check if we have a regex match
                if re.search('Number of the partial proof of sustainability', line):
                    return {"pos_num": line.split(':')[1].strip()}
                if re.search('Nummer des Teilnachweises', line):
                    return {"pos_num": line.split(':')[1].strip()}
        return {"pos_num": None}

    def get_number_basic_proof(self):
        # open the files
        with open(self.path_to_text, 'r') as f:
            # loop through each line in corpus
            for line_i, line in enumerate(f):
                # check if we have a regex match
                if re.search('Number of the basic proof', line):
                    return {"pos_basic_proof_num": line.split(':')[1].strip()}
                if re.search('Number of the proof divided', line):
                    return {"pos_basic_proof_num": line.split(':')[1].strip()}
                if re.search('Nummer des Basis-Nachweises', line):
                    return {"pos_basic_proof_num": line.split(':')[1].strip()}
        return {"pos_basic_proof_num": None}

    def get_issuer(self):
        # open the files
        with open(self.path_to_text, 'r') as f:
            # loop through each line in corpus
            for line_i, line in enumerate(f):
                # check if we have a regex match
                if re.search('issuer', line):
                    return {"issuer": line.split(':')[1].strip()}
                if re.search('Supplier', line):
                    return {"issuer": line.split(':')[1].strip()}
                if re.search('Aussteller', line):
                    return {"issuer": line.split(':')[1].strip()}
        return {"issuer": None}

    def get_interface(self):
        with open(self.path_to_text, 'r') as f:
            # loop through each line in corpus
            interface_line = -1
            first_line = False
            for line_i, line in enumerate(f):
                # check if we have a regex match
                if re.search('Interface', line):
                    interface_line = line_i
                if re.search('Schnittstelle', line):
                    interface_line = line_i
                if interface_line != -1 and line != '\n' and line_i > interface_line:
                    return {'interface': re.sub('\s\s\s\s+', ';', line).split(';')[0].strip()}
            return {"interface": None}

    def get_quantity(self):
        # open the files
        with open(self.path_to_text, 'r') as f:
            # loop through each line in corpus
            for line_i, line in enumerate(f):
                # check if we have a regex match
                if re.search(' Amount', line):
                    line = re.sub('\s\s+', ';', line).split(';')[1].strip()
                    return {"quantity": line.split(' ')[0]}, \
                           {"quantity_unit": line.split(' ')[1]}, \
                           {'quantity_mt': float(line.split(' ')[0]) * 0.883}
                if re.search(' Menge ', line):
                    line = re.sub('\s\s+', ';', line).split(';')[1].strip()
                    return {"quantity": line.split(' ')[0]}, \
                           {"quantity_unit": line.split(' ')[1]}, \
                           {'quantity_mt': float(line.split(' ')[0]) * 0.883}
        return {"quantity": None}, {"quantity_unit": None}, {'quantity_mt': None}

    def get_country_cultivation(self):
        # open the files
        with open(self.path_to_text, 'r') as f:
            next_line = False
            # loop through each line in corpus
            for line_i, line in enumerate(f):
                # check if we have a regex match
                if line.strip() == "Biomass (%)" or re.search('Code / Kürzel', line):
                    next_line = True
                if next_line and not (line.strip() == "Biomass (%)" or re.search('Code / Kürzel', line)):
                    biomass_percentage = re.sub('\s\s+', ';', line).split(';')[4].strip()
                    return {"country_cultivation": biomass_percentage}
        return {"country_cultivation": None}

    def get_certification_system(self):
        with open(self.path_to_text, 'r') as f:
            # loop through each line in corpus
            certification_line = -1
            for line_i, line in enumerate(f):
                # check if we have a regex match
                if re.search('Certification system / Voluntary scheme', line):
                    certification_line = line_i
                if certification_line != -1 and line != '\n' and line_i > certification_line:
                    return {
                        'certification': re.sub('\s\s\s\s+', ';', line).split(';')[2].strip()}
        return {"certification": None}

    # s = get_certification_system("text_data/output.txt")
    def get_first_formula(self):
        # open the files
        with open(self.path_to_text, 'r') as f:
            # loop through each line in corpus
            for line_i, line in enumerate(f):
                # check if we have a regex match
                if re.search('E=', line):
                    return {'first_formula': line}
        return {"first_formula": None}

    def get_second_formula(self):
        # open the files
        with open(self.path_to_text, 'r') as f:
            # loop through each line in corpus
            first_formula_found = False
            for line_i, line in enumerate(f):
                # check if we have a regex match
                if re.search('E=', line):
                    if not first_formula_found:
                        first_formula_found = True
                    else:
                        return {'second_formula': line}
        return {"second_formula": None}

    def get_date_issuance(self):
        # open the files
        with open(self.path_to_text, 'r') as f:
            # loop through each line in corpus
            for line_i, line in enumerate(f):
                # check if we have a regex match
                if re.search('Date of issuance', line):
                    line = re.sub('\s\s+', ';', line).split(';')[1].strip()
                    return {"issuance_date": line}
                if re.search('Ausstellungsdatum', line):
                    line = re.sub('\s\s+', ';', line).split(';')[1].strip()
                    return {"issuance_date": line}
        return {"issuance_date": None}

    def get_last_supplier(self):
        # open the files
        with open(self.path_to_text, 'r') as f:
            # loop through each line in corpus
            for line_i, line in enumerate(f):
                # check if we have a regex match
                if re.search('Last supplier', line):
                    line = line.split(':')[1].strip()
                    return {"last_supplier": line}
                if re.search('Letzter Lieferant', line):
                    line = line.split(':')[1].strip()
                    return {"last_supplier": line}
        return {"last_supplier": None}

    def get_ghg_reduction_percentage(self):
        # open the files
        with open(self.path_to_text, 'r') as f:
            # loop through each line in corpus
            for line_i, line in enumerate(f):
                # check if we have a regex match
                if re.search('% as biofuels', line):
                    percentage = line.split('%')[0].strip()
                    unit = line.split('as biofuels')[1].strip()
                    unit = re.sub('\s\s+', ';', unit).split(';')[0]
                    return {"ghg_reduction_percentage": percentage}, {"ghg_reduction_mass": unit}
                if re.search('% als Kraftstoff', line):
                    percentage = line.split('%')[0].strip()
                    unit = line.split('als Kraftstoff')[1].strip()
                    unit = re.sub('\s\s+', ';', unit).split(';')[0]
                    return {"ghg_reduction_percentage": percentage}, {"ghg_reduction_mass": unit}
        return {"ghg_reduction_percentage": None}, {"ghg_reduction_mass": None}

    def get_initial_operating(self):
        # open the files
        initial_operating_german = False
        with open(self.path_to_text, 'r') as f:
            # loop through each line in corpus
            for line_i, line in enumerate(f):
                # check if we have a regex match
                if re.search('initial operating', line):
                    line = re.sub('\s\s\s\s+', ';', line).split(';')[-2:]
                    line = "".join(line).strip().replace(" ", "")
                    if line == "yesXno":
                        return {"initial_operating": 'no'}
                    else:
                        return {"initial_operating": 'yes'}
                if re.search('Die Erstinbetriebnahme der Anlage zur', line):
                    initial_operating_german = True
                if initial_operating_german and not re.search('Die Erstinbetriebnahme der Anlage zur', line):
                    line = re.sub('\s\s\s\s+', ';', line).split(';')[-2:]
                    line = "".join(line).strip().replace(" ", "")
                    if line == "jaXnein":
                        return {"initial_operating": 'no'}
                    else:
                        return {"initial_operating": 'yes'}
        return {"initial_operating": None}

    def get_date_delivery(self):
        # open the files
        with open(self.path_to_text, 'r') as f:
            # loop through each line in corpus
            for line_i, line in enumerate(f):
                # check if we have a regex match
                if re.search('Date of delivery ', line):
                    line = re.sub('\s\s+', ';', line).split(';')[1].strip()
                    return {"delivery_date": line}
                if re.search('Lieferdatum ', line):
                    line = re.sub('\s\s+', ';', line).split(';')[1].strip()
                    return {"delivery_date": line}
        return {"delivery_date": None}

    def get_biomass(self):
        # open the files
        with open(self.path_to_text, 'r') as f:
            next_line = False
            # loop through each line in corpus
            for line_i, line in enumerate(f):
                # check if we have a regex match
                if line.strip() == "Biomass (%)" or re.search('Code / Kürzel', line):
                    next_line = True
                if next_line and not (line.strip() == "Biomass (%)" or re.search('Code / Kürzel', line)):
                    code_short_term = re.sub('\s\s+', ';', line).split(';')[1].strip()
                    biomass_percentage = re.sub('\s\s+', ';', line).split(';')[3].strip()
                    return {"biomass_percentage": biomass_percentage}, {"code_short_term": code_short_term}
        return {"biomass_percentage": None}, {"code_short_term": None}

    def get_all_fields(self):
        all_fields = {}
        pos_num = YellowTextScrapper.get_number_pos(self)
        number_basic_proof = YellowTextScrapper.get_number_basic_proof(self)
        issuer = YellowTextScrapper.get_issuer(self)
        interface = YellowTextScrapper.get_interface(self)
        quantity = YellowTextScrapper.get_quantity(self)
        country_cultivation = YellowTextScrapper.get_country_cultivation(self)
        first_formula = YellowTextScrapper.get_first_formula(self)
        second_formula = YellowTextScrapper.get_second_formula(self)
        date_of_insurance = YellowTextScrapper.get_date_issuance(self)
        last_supplier = YellowTextScrapper.get_last_supplier(self)
        ghg_reduction = YellowTextScrapper.get_ghg_reduction_percentage(self)
        initial_operating = YellowTextScrapper.get_initial_operating(self)
        date_delivery = YellowTextScrapper.get_date_delivery(self)
        biomass = YellowTextScrapper.get_biomass(self)

        all_fields.update(pos_num)
        all_fields.update(number_basic_proof)
        all_fields.update(issuer)
        all_fields.update(interface)
        all_fields.update(quantity[0])
        all_fields.update(quantity[1])
        all_fields.update(quantity[2])
        all_fields.update(country_cultivation)
        all_fields.update(first_formula)
        all_fields.update(second_formula)
        all_fields.update(date_of_insurance)
        all_fields.update(last_supplier)
        all_fields.update(ghg_reduction[0])
        all_fields.update(ghg_reduction[1])
        all_fields.update(initial_operating)
        all_fields.update(date_delivery)
        all_fields.update(biomass[0])
        all_fields.update(biomass[1])

        return all_fields


class BlueTextScrapper:
    """
    Extract data from the text
    """

    def __init__(self, path_to_text):
        self.path_to_text = path_to_text

    def get_number_pos(self):
        pattern = r'Unique Number of Sustainability\s+(.*)'
        with open(self.path_to_text, 'r') as f:
            # loop through each line in corpus
            for line_i, line in enumerate(f):
                # check if we have a regex match
                if re.search('Unique Number of Sustainability', line):
                    return {"pos_num": re.search(pattern, line).group(1)}
        return {"pos_num": None}

    def get_number_basic_proof(self):
        return {"pos_basic_proof_num": None}

    def get_issuer(self):
        with open(self.path_to_text, 'r') as f:
            for line_number, line in enumerate(f):
                # check which line contains 'Name'
                if re.search('Name', line):
                    break
            # remove leading, trailing and middle spaces
            next_line = f.readline().strip()
            next_line = re.sub(' {2,1000}', '***', next_line)
            # extract issuer
            issuer = next_line.split('***')[0]
            return {"issuer": issuer}
        return {"issuer": None}

    def get_interface(self):
        with open(self.path_to_text, 'r') as f:
            for line_number, line in enumerate(f):
                # check which line contains 'Name'
                if re.search('Certificate Number', line):
                    break
            # remove leading, trailing and middle spaces
            next_line = f.readline().strip()
            next_line = re.sub(' {2,1000}', '***', next_line)
            # extract interface
            interface = next_line.split('***')[0]
            return {"interface": interface}
        return {"interface": None}

    def get_quantity(self):
        pattern = r'Quantity:\s+([0-9,.]*)'
        with open(self.path_to_text, 'r') as f:
            # loop through each line in corpus
            for line_i, line in enumerate(f):
                # check if we have a regex match
                if re.search('Quantity', line):
                    line = re.sub('\s\s+', ';', line)
                    print(line.split(';'))
                    print(line.split(';')[2].replace(',', ''))
                    return {"quantity": line.split(';')[2].replace(',', '')}, \
                           {"quantity_unit": line.split(';')[3]}, \
                           {'quantity_mt': float(line.split(';')[2].replace(',', '')) * 0.883}

        return {"quantity": None}, \
               {"quantity_unit": None}, \
               {'quantity_mt': None}

    def get_country_cultivation(self):
        pattern = r'Country.*\s{2,100}([A-Z, a-z]*)'
        with open(self.path_to_text, 'r') as f:
            # loop through each line in corpus
            for line_i, line in enumerate(f):
                # check if we have a regex match
                if re.search('Country', line):
                    return {"country_cultivation": re.search(pattern, line).group(1)}
        return {"country_cultivation": None}

    def get_first_formula(self):
        # open the files
        with open(self.path_to_text, 'r') as f:
            # loop through each line in corpus
            for line_i, line in enumerate(f):
                # check if we have a regex match
                if re.search('E=', line):
                    return {'first_formula': line}
        return {"first_formula": None}

    def get_second_formula(self):
        # open the files
        with open(self.path_to_text, 'r') as f:
            # loop through each line in corpus
            first_formula_found = False
            for line_i, line in enumerate(f):
                if first_formula_found:
                    return {'second_formula': 'E='+line}
                # check if we have a regex match
                if re.search('E=', line):
                    if not first_formula_found:
                        first_formula_found = True
        return {"second_formula": None}

    def get_date_issuance(self):
        pattern = r'\ADate of Issuance:\s{2,100}([0-9/]*)'
        with open(self.path_to_text, 'r') as f:
            # loop through each line in corpus
            for line_i, line in enumerate(f):
                # check if we have a regex match
                if re.search('Date of Issuance', line):
                    issuance_date = re.search(pattern, line).group(1)
                    issuance_date = issuance_date.replace('/','.')
                    return {"issuance_date": issuance_date}
        return {"issuance_date": None}

    def get_last_supplier(self):
        # open the files
        with open(self.path_to_text, 'r') as f:
            # loop through each line in corpus
            for line_i, line in enumerate(f):
                # check if we have a regex match
                if re.search('Last supplier', line):
                    line = line.split(':')[1].strip()
                    return {"last_supplier": line}
                if re.search('Letzter Lieferant', line):
                    line = line.split(':')[1].strip()
                    return {"last_supplier": line}
        return {"last_supplier": None}

    def get_ghg_reduction_percentage(self):
        pattern = r'\s+([0-9.]*)% \(for biofuels ([A-Z a-z/,.0-9]*)\).*'
        with open(self.path_to_text, 'r') as f:
            # loop through each line in corpus
            for line_i, line in enumerate(f):
                # check if we have a regex match
                if re.search('for biofuels', line):
                    ghg_reduction_percentage = re.search(pattern, line).group(1)
                    ghg_reduction_mass = re.search(pattern, line).group(2)
                    return {"ghg_reduction_percentage": ghg_reduction_percentage},{"ghg_reduction_mass": ghg_reduction_mass}
        return {"ghg_reduction_percentage": None,"ghg_reduction_mass": None}

    def get_initial_operating(self):
        # open the files
        initial_operating_german = False
        with open(self.path_to_text, 'r') as f:
            # loop through each line in corpus
            for line_i, line in enumerate(f):
                # check if we have a regex match
                if re.search('The installation where the final', line):
                    line = re.sub('\s\s\s\s+', ';', line).split(';')[-2:]
                    line = "".join(line).strip().replace(" ", "")
                    if line == "yesXno":
                        return {"initial_operating": 'no'}
                    elif line == "Xyesno":
                        return {"initial_operating": 'yes'}
                    else:
                        return {"initial_operating": None}
        return {"initial_operating": None}

    def get_date_delivery(self):
        # open the files
        with open(self.path_to_text, 'r') as f:
            # loop through each line in corpus
            date_line = False
            for line_i, line in enumerate(f):
                # check if we have a regex match
                if date_line:
                    line = line.strip().split(' ')[2].strip()
                    return {"delivery_date": line}
                if re.search('Place and date of dispatch:', line):
                    date_line = True
        return {"delivery_date": None}

    def get_biomass(self):
        # open the files
        with open(self.path_to_text, 'r') as f:
            next_line = False
            # loop through each line in corpus
            for line_i, line in enumerate(f):
                # check if we have a regex match
                if line.strip() == "Biomass (%)" or re.search('Code / Kürzel', line):
                    next_line = True
                if next_line and not (line.strip() == "Biomass (%)" or re.search('Code / Kürzel', line)):
                    code_short_term = re.sub('\s\s+', ';', line).split(';')[1].strip()
                    biomass_percentage = re.sub('\s\s+', ';', line).split(';')[3].strip()
                    return {"biomass_percentage": biomass_percentage}, {"code_short_term": code_short_term}
        return {"biomass_percentage": None}, {"code_short_term": None}

    def get_all_fields(self):
        all_fields = {}
        pos_num = BlueTextScrapper.get_number_pos(self)
        number_basic_proof = BlueTextScrapper.get_number_basic_proof(self)
        issuer = BlueTextScrapper.get_issuer(self)
        interface = BlueTextScrapper.get_interface(self)
        quantity = BlueTextScrapper.get_quantity(self)
        country_cultivation = BlueTextScrapper.get_country_cultivation(self)
        first_formula = BlueTextScrapper.get_first_formula(self)
        second_formula = BlueTextScrapper.get_second_formula(self)
        date_of_insurance = BlueTextScrapper.get_date_issuance(self)
        last_supplier = BlueTextScrapper.get_last_supplier(self)
        ghg_reduction = BlueTextScrapper.get_ghg_reduction_percentage(self)
        initial_operating = BlueTextScrapper.get_initial_operating(self)
        date_delivery = BlueTextScrapper.get_date_delivery(self)
        biomass = BlueTextScrapper.get_biomass(self)

        all_fields.update(pos_num)
        all_fields.update(number_basic_proof)
        all_fields.update(issuer)
        all_fields.update(interface)
        all_fields.update(quantity[0])
        all_fields.update(quantity[1])
        all_fields.update(quantity[2])
        all_fields.update(country_cultivation)
        all_fields.update(first_formula)
        all_fields.update(second_formula)
        all_fields.update(date_of_insurance)
        all_fields.update(last_supplier)
        all_fields.update(ghg_reduction[0])
        all_fields.update(ghg_reduction[1])
        all_fields.update(initial_operating)
        all_fields.update(date_delivery)
        all_fields.update(biomass[0])
        all_fields.update(biomass[1])

        return all_fields


# TextScrapper = TextScrapper("data/text_data/output.txt")
# a = TextScrapper.get_all_fields()
# print(a)
