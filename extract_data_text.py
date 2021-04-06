import re


class TextScrapper:

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
                    return {"quantity": line.split(' ')[0]}, {"quantity_unit": line.split(' ')[1]}
                if re.search(' Menge ', line):
                    line = re.sub('\s\s+', ';', line).split(';')[1].strip()
                    return {"quantity": line.split(' ')[0]}, {"quantity_unit": line.split(' ')[1]}
        return {"quantity": None}, {"quantity_unit": None}

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

    def get_biofuel_percentage(self):
        # open the files
        with open(self.path_to_text, 'r') as f:
            # loop through each line in corpus
            for line_i, line in enumerate(f):
                # check if we have a regex match
                if re.search('% as biofuels', line):
                    percentage = line.split('%')[0].strip()
                    unit = line.split('as biofuels')[1].strip()
                    unit = re.sub('\s\s+', ';', unit).split(';')[0]
                    return {"biofuel_percentage": percentage}, {"biofuel_unit": unit}
                if re.search('% als Kraftstoff', line):
                    percentage = line.split('%')[0].strip()
                    unit = line.split('als Kraftstoff')[1].strip()
                    unit = re.sub('\s\s+', ';', unit).split(';')[0]
                    return {"biofuel_percentage": percentage}, {"biofuel_unit": unit}
        return {"biofuel_percentage": None}, {"biofuel_unit": None}

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
        pos_num = TextScrapper.get_number_pos(self)
        number_basic_proof = TextScrapper.get_number_basic_proof(self)
        issuer = TextScrapper.get_issuer(self)
        interface = TextScrapper.get_interface(self)
        quantity = TextScrapper.get_quantity(self)
        country_cultivation = TextScrapper.get_country_cultivation(self)
        first_formula = TextScrapper.get_first_formula(self)
        second_formula = TextScrapper.get_second_formula(self)
        date_of_insurance = TextScrapper.get_date_issuance(self)
        last_supplier = TextScrapper.get_last_supplier(self)
        biofuel_percentage = TextScrapper.get_biofuel_percentage(self)
        initial_operating = TextScrapper.get_initial_operating(self)
        date_delivery = TextScrapper.get_date_delivery(self)
        biomass = TextScrapper.get_biomass(self)

        all_fields.update(pos_num)
        all_fields.update(number_basic_proof)
        all_fields.update(issuer)
        all_fields.update(interface)
        all_fields.update(quantity[0])
        all_fields.update(quantity[1])
        all_fields.update(country_cultivation)
        all_fields.update(first_formula)
        all_fields.update(second_formula)
        all_fields.update(date_of_insurance)
        all_fields.update(last_supplier)
        all_fields.update(biofuel_percentage[0])
        all_fields.update(biofuel_percentage[1])
        all_fields.update(initial_operating)
        all_fields.update(date_delivery)
        all_fields.update(biomass[0])
        all_fields.update(biomass[1])

        return all_fields


#TextScrapper = TextScrapper("text_data/output.txt")
#a = TextScrapper.get_biomass()
#print(a)