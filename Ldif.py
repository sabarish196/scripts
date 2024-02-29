import csv
from ldap3 import LDIFParser

# Open the LDIF file for reading and CSV file for writing
with open('input.ldif', 'rb') as ldif_file, open('output.csv', 'w', newline='') as csv_file:
    ldif_parser = LDIFParser(ldif_file)

    # Initialize CSV writer
    csv_writer = csv.writer(csv_file)

    # Iterate over LDIF entries and write them to CSV
    for dn, entry in ldif_parser.parse():
        # Write DN as the first column
        csv_writer.writerow([dn])

        # Write attribute-value pairs as subsequent columns
        for attribute, values in entry.items():
            for value in values:
                csv_writer.writerow([attribute, value])



import ldif
import csv

def ldif_to_csv(input_file, output_file):
    with open(input_file, 'rb') as ldif_file, open(output_file, 'w', newline='') as csv_file:
        ldif_parser = ldif.LDIFRecordList(ldif_file)
        ldif_parser.parse()

        csv_writer = csv.writer(csv_file)

        for dn, entry in ldif_parser.all_records:
            csv_writer.writerow([dn])

            for attribute, values in entry.items():
                for value in values:
                    csv_writer.writerow([attribute, value])

# Usage example
ldif_to_csv('input.ldif', 'output.csv')



import csv
import ldap3

def ldif_to_csv(input_file, output_file):
    with open(input_file, 'rb') as ldif_file, open(output_file, 'w', newline='') as csv_file:
        ldif_parser = ldap3.ldif.LDIFRecordList(ldif_file)
        ldif_parser.parse()

        csv_writer = csv.writer(csv_file)

        for dn, entry in ldif_parser.all_records:
            csv_writer.writerow([dn])

            for attribute, values in entry.items():
                for value in values:
                    csv_writer.writerow([attribute, value])

# Usage example
ldif_to_csv('input.ldif', 'output.csv')


import ldif
import csv

def ldif_to_csv(input_file, output_file):
    with open(input_file, 'rb') as ldif_file, open(output_file, 'w', newline='') as csv_file:
        ldif_parser = ldif.LDIFParser(ldif_file)
        csv_writer = csv.writer(csv_file)

        for dn, entry in ldif_parser.parse():
            csv_writer.writerow([dn])

            for attribute, values in entry.items():
                for value in values:
                    csv_writer.writerow([attribute, value])

# Usage example
ldif_to_csv('input.ldif', 'output.csv')


import ldif
import csv

def cn_to_csv(input_file, output_file):
    with open(input_file, 'rb') as ldif_file, open(output_file, 'w', newline='') as csv_file:
        ldif_parser = ldif.LDIFParser(ldif_file)
        csv_writer = csv.writer(csv_file)

        # Write header to the CSV file
        csv_writer.writerow(['Common Name (cn)'])

        # Iterate over LDIF entries
        for _, entry in ldif_parser.parse():
            # Check if the entry contains the 'cn' attribute
            if 'cn' in entry:
                # Write the 'cn' attribute values to the CSV file
                for value in entry['cn']:
                    csv_writer.writerow([value])

# Usage example
cn_to_csv('input.ldif', 'output.csv')
