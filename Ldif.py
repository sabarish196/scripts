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


from ldap3 import Server, Connection, SUBTREE

# LDAP server configuration
ldap_server = Server('ldap://your_ldap_server_address')
ldap_username = 'your_ldap_username'
ldap_password = 'your_ldap_password'

# LDAP query parameters
base_dn = 'ou=users,dc=example,dc=com'  # Adjust this to your LDAP structure
search_filter = '(&(objectClass=user)(loginShell=/bin/bash))'  # LDAP filter to find users with /bin/bash shell

try:
    # Establish connection to LDAP server
    ldap_conn = Connection(ldap_server, user=ldap_username, password=ldap_password, auto_bind=True)

    # Perform LDAP search
    ldap_conn.search(search_base=base_dn,
                     search_filter=search_filter,
                     search_scope=SUBTREE,
                     attributes=['cn', 'uid', 'loginShell'])

    # Display results
    if ldap_conn.entries:
        print("Service accounts with login shell /bin/bash:")
        for entry in ldap_conn.entries:
            print(f"CN: {entry.cn}, UID: {entry.uid}")
    else:
        print("No service accounts found with login shell /bin/bash.")

    # Disconnect from LDAP server
    ldap_conn.unbind()
except Exception as e:
    print(f"An error occurred: {e}")



from ldap3 import Server, Connection, SUBTREE, ALL_ATTRIBUTES
import csv

# LDAP server configuration
ldap_server = Server('ldap://your_ldap_server_address')
ldap_username = 'your_ldap_username'
ldap_password = 'your_ldap_password'

# LDAP query parameters
base_dn = 'ou=users,dc=example,dc=com'  # Adjust this to your LDAP structure
search_filter = '(&(objectClass=user)(loginShell=/bin/bash))'  # LDAP filter to find users with /bin/bash shell

# CSV file configuration
output_csv = 'service_accounts.csv'

try:
    # Establish connection to LDAP server
    ldap_conn = Connection(ldap_server, user=ldap_username, password=ldap_password, auto_bind=True)

    # Perform LDAP search
    ldap_conn.search(search_base=base_dn,
                     search_filter=search_filter,
                     search_scope=SUBTREE,
                     attributes=ALL_ATTRIBUTES)

    # Write results to CSV
    with open(output_csv, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['CN', 'UID', 'memberOf'])

        # Iterate over search results
        for entry in ldap_conn.entries:
            cn = entry.cn.value
            uid = entry.uid.value
            member_of = entry.memberOf.values if 'memberOf' in entry else []

            # Write entry to CSV
            csv_writer.writerow([cn, uid, ';'.join(member_of)])

    print(f"Service account details exported to {output_csv}")

    # Disconnect from LDAP server
    ldap_conn.unbind()
except Exception as e:
    print(f"An error occurred: {e}")


from ldap3 import Server, Connection, SUBTREE, ALL_ATTRIBUTES
import csv
import re

# LDAP server configuration
ldap_server = Server('ldap://your_ldap_server_address')
ldap_username = 'your_ldap_username'
ldap_password = 'your_ldap_password'

# LDAP query parameters
base_dn = 'ou=users,dc=example,dc=com'  # Adjust this to your LDAP structure
search_filter = '(&(objectClass=user)(loginShell=/bin/bash))'  # LDAP filter to find users with /bin/bash shell

# CSV file configuration
output_csv = 'service_accounts.csv'

def extract_cn_from_memberof(member_of):
    cn_list = []
    for entry in member_of:
        # Use regular expression to extract CN value from each memberOf entry
        match = re.search(r'CN=([^,]+)', entry)
        if match:
            cn_list.append(match.group(1))
    return ';'.join(cn_list)

try:
    # Establish connection to LDAP server
    ldap_conn = Connection(ldap_server, user=ldap_username, password=ldap_password, auto_bind=True)

    # Perform LDAP search
    ldap_conn.search(search_base=base_dn,
                     search_filter=search_filter,
                     search_scope=SUBTREE,
                     attributes=ALL_ATTRIBUTES)

    # Write results to CSV
    with open(output_csv, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['CN', 'UID', 'memberOf'])

        # Iterate over search results
        for entry in ldap_conn.entries:
            cn = entry.cn.value
            uid = entry.uid.value
            member_of = entry.memberOf.values if 'memberOf' in entry else []
            cn_list = extract_cn_from_memberof(member_of)

            # Write entry to CSV
            csv_writer.writerow([cn, uid, cn_list])

    print(f"Service account details exported to {output_csv}")

    # Disconnect from LDAP server
    ldap_conn.unbind()
except Exception as e:
    print(f"An error occurred: {e}")
