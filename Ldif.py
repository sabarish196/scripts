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
