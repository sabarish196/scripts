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
