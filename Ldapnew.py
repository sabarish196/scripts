from ldap3 import Server, Connection, SUBTREE

# LDAP server settings
ldap_server = 'ldap://your_ldap_server'
ldap_user = 'your_username'
ldap_password = 'your_password'

# Bases to search
bases = ['base1', 'base2']

# Search filter
search_filter = '(loginshell=/bin/bash)'

# Fields to retrieve
attributes = ['cn', 'memberof']

# Output file
output_file = 'ldap_output.txt'

def connect_to_ldap():
    server = Server(ldap_server)
    conn = Connection(server, user=ldap_user, password=ldap_password)
    if not conn.bind():
        raise Exception('LDAP connection error: {}'.format(conn.result))
    return conn

def search_and_save_results(conn):
    with open(output_file, 'w') as f:
        for base in bases:
            conn.search(base, search_filter, attributes=attributes, search_scope=SUBTREE)
            for entry in conn.entries:
                cn = entry.cn.value if 'cn' in entry else ''
                memberof = ','.join(entry.memberof) if 'memberof' in entry else ''
                f.write(f'CN: {cn}, Memberof: {memberof}\n')

if __name__ == "__main__":
    ldap_conn = connect_to_ldap()
    search_and_save_results(ldap_conn)
    ldap_conn.unbind()
    print(f'Results saved to {output_file}')



from ldap3 import Server, Connection, SUBTREE

# LDAP server settings
ldap_server = 'ldap://your_ldap_server'
ldap_user = 'your_username'
ldap_password = 'your_password'

# Bases to search
bases = ['base1', 'base2']

# Search filter
search_filter = '(loginshell=/bin/bash)'

# Fields to retrieve
attributes = ['cn', 'memberof']

# Output file
output_file = 'ldap_output.txt'

def connect_to_ldap():
    server = Server(ldap_server)
    conn = Connection(server, user=ldap_user, password=ldap_password)
    if not conn.bind():
        raise Exception('LDAP connection error: {}'.format(conn.result))
    return conn

def extract_cn_from_memberof(memberof_values):
    cn_list = []
    for value in memberof_values:
        cn_list.append(value.split(',')[0].split('=')[1])
    return ','.join(cn_list)

def search_and_save_results(conn):
    with open(output_file, 'w') as f:
        for base in bases:
            conn.search(base, search_filter, attributes=attributes, search_scope=SUBTREE)
            for entry in conn.entries:
                cn = entry.cn.value if 'cn' in entry else ''
                memberof = extract_cn_from_memberof(entry.memberof) if 'memberof' in entry else ''
                f.write(f'CN: {cn}, Memberof: {memberof}\n')

if __name__ == "__main__":
    ldap_conn = connect_to_ldap()
    search_and_save_results(ldap_conn)
    ldap_conn.unbind()
    print(f'Results saved to {output_file}')


from ldap3 import Server, Connection, SUBTREE

# LDAP server settings
ldap_server = 'ldap://your_ldap_server'
ldap_user = 'your_username'
ldap_password = 'your_password'

# Bases to search
bases = ['base1', 'base2']

# Search filter
search_filter = '(loginshell=/bin/bash)'

# Fields to retrieve
attributes = ['cn', 'memberof']

# Server file
server_file = 'server.txt'

def connect_to_ldap():
    server = Server(ldap_server)
    conn = Connection(server, user=ldap_user, password=ldap_password)
    if not conn.bind():
        raise Exception('LDAP connection error: {}'.format(conn.result))
    return conn

def extract_cn_from_memberof(memberof_values):
    cn_list = []
    for value in memberof_values:
        cn_list.append(value.split(',')[0].split('=')[1])
    return cn_list

def search_and_compare(conn, servers):
    for base in bases:
        conn.search(base, search_filter, attributes=attributes, search_scope=SUBTREE)
        for entry in conn.entries:
            cn = entry.cn.value if 'cn' in entry else ''
            memberof = extract_cn_from_memberof(entry.memberof) if 'memberof' in entry else []
            for server in servers:
                if cn in server['users']:
                    print(f"CN: {cn}, Server: {server['name']}")

def parse_server_file():
    servers = []
    with open(server_file, 'r') as f:
        for line in f:
            server_info = line.strip().split(':')
            server = {'name': server_info[0], 'groups': server_info[1], 'users': server_info[2].split(',')}
            servers.append(server)
    return servers

if __name__ == "__main__":
    ldap_conn = connect_to_ldap()
    servers = parse_server_file()
    search_and_compare(ldap_conn, servers)
    ldap_conn.unbind()


import csv
from ldap3 import Server, Connection, SUBTREE

# LDAP server settings
ldap_server = 'ldap://your_ldap_server'
ldap_user = 'your_username'
ldap_password = 'your_password'

# Bases to search
bases = ['base1', 'base2']

# Search filter
search_filter = '(loginshell=/bin/bash)'

# Fields to retrieve
attributes = ['cn', 'memberof']

# Server file
server_file = 'server.txt'

# Output CSV file
output_csv_file = 'ldap_output.csv'

def connect_to_ldap():
    server = Server(ldap_server)
    conn = Connection(server, user=ldap_user, password=ldap_password)
    if not conn.bind():
        raise Exception('LDAP connection error: {}'.format(conn.result))
    return conn

def extract_cn_from_memberof(memberof_values):
    cn_list = []
    for value in memberof_values:
        cn_list.append(value.split(',')[0].split('=')[1])
    return cn_list

def search_and_compare(conn, servers):
    unique_results = set()
    for base in bases:
        conn.search(base, search_filter, attributes=attributes, search_scope=SUBTREE)
        for entry in conn.entries:
            cn = entry.cn.value if 'cn' in entry else ''
            memberof = extract_cn_from_memberof(entry.memberof) if 'memberof' in entry else []
            for server in servers:
                if cn in server['users']:
                    unique_results.add((cn, server['name']))
    return unique_results

def parse_server_file():
    servers = []
    with open(server_file, 'r') as f:
        for line in f:
            server_info = line.strip().split(':')
            server = {'name': server_info[0], 'groups': server_info[1], 'users': server_info[2].split(',')}
            servers.append(server)
    return servers

def append_to_csv(results):
    with open(output_csv_file, 'a', newline='') as f:
        writer = csv.writer(f)
        for result in results:
            writer.writerow(result)

if __name__ == "__main__":
    ldap_conn = connect_to_ldap()
    servers = parse_server_file()
    unique_results = search_and_compare(ldap_conn, servers)
    append_to_csv(unique_results)
    ldap_conn.unbind()
