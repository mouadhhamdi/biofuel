import re


def get_number_pos(path):
    # open the files
    with open(path, 'r') as f:
        # loop through each line in corpus
        for line_i, line in enumerate(f):
            # check if we have a regex match
            if re.search('Number of the partial proof of sustainability', line):
                return {"pos_num": line.split(':')[1].strip()}


def get_number_basic_proof(path):
    # open the files
    with open(path, 'r') as f:
        # loop through each line in corpus
        for line_i, line in enumerate(f):
            # check if we have a regex match
            if re.search('Number of the basic proof', line):
                return {"pos_basic_proof_num": line.split(':')[1].strip()}


def get_issuer(path):
    # open the files
    with open(path, 'r') as f:
        # loop through each line in corpus
        for line_i, line in enumerate(f):
            # check if we have a regex match
            if re.search('issuer', line):
                return {"issuer": line.split(':')[1].strip()}


#s = get_number_pos("output.txt")
#s1 = get_number_basic_proof("output.txt")
#s2 = get_issuer("output.txt")


def get_interface(path):
    with open(path, 'r') as f:
        # loop through each line in corpus
        interface_line = -1
        first_line = False
        for line_i, line in enumerate(f):
            # check if we have a regex match
            if re.search('Interface', line):
                interface_line = line_i
            if interface_line != -1 and line != '\n' and line_i > interface_line:
                return {'Interface': re.sub('\s\s\s\s+', ';', line).split(';')[0].strip()}


def get_certification_system(path):
    with open(path, 'r') as f:
        # loop through each line in corpus
        certification_line = -1
        for line_i, line in enumerate(f):
            # check if we have a regex match
            if re.search('Certification system / Voluntary scheme', line):
                certification_line = line_i
            if certification_line != -1 and line != '\n' and line_i > certification_line:
                return {'Certification system / Voluntary scheme': re.sub('\s\s\s\s+', ';', line).split(';')[2].strip()}

# s = get_certification_system("text_data/output.txt")
def get_first_formula(path):
    # open the files
    with open(path, 'r') as f:
        # loop through each line in corpus
        for line_i, line in enumerate(f):
            # check if we have a regex match
            if re.search('E=', line):
                print(line)
                return {'E': line}


def get_second_formula(path):
    # open the files
    with open(path, 'r') as f:
        # loop through each line in corpus
        first_formula_found = False
        for line_i, line in enumerate(f):
            # check if we have a regex match
            if re.search('E=', line):
                if not first_formula_found:
                    first_formula_found = True
                else:
                    print(line)
                    return {'E': line}

        print("No second line found")


f1 = get_first_formula("text_data/output.txt")
f2 = get_second_formula("text_data/output.txt")


def get_date_of_insurance(path):
    # open the files
    with open(path, 'r') as f:
        # loop through each line in corpus
        for line_i, line in enumerate(f):
            # check if we have a regex match
            if re.search('Date of issuance', line):
                print(line)
                return {"Date of issuance": line}


def get_date_of_delivery(path):
    # open the files
    with open(path, 'r') as f:
        # loop through each line in corpus
        for line_i, line in enumerate(f):
            # check if we have a regex match
            if re.search('Date of delivery ', line):
                print(re.sub('\s\s+', ' ', line))
                return {"Date of delivery ": line}

get_date_of_insurance("text_data/output.txt")
get_date_of_delivery("text_data/output.txt")

