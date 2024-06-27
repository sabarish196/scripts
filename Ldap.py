import sys
from ldap3 import Server, Connection, ALL, SUBTREE

def get_user_ids_from_args():
    if len(sys.argv) < 2:
        print("Usage: python script_name.py user1 user2 user3 ...")
        sys.exit(1)
    return sys.argv[1:]

def check_user_groups(conn, base_dn, user_ids, required_groups):
    for user_id in user_ids:
        search_filter = f'(sAMAccountName={user_id})'
        
        conn.search(
            search_base=base_dn,
            search_filter=search_filter,
            search_scope=SUBTREE,
            attributes=['memberOf']
        )
        
        if conn.entries:
            user_entry = conn.entries[0]
            user_groups = [str(group).split(',')[0].split('=')[1] for group in user_entry.memberOf]
            
            not_in_groups = [group for group in required_groups if group not in user_groups]
            
            if not_in_groups:
                print(f"User {user_id} is not part of the groups: {', '.join(not_in_groups)}")
            else:
                print(f"User {user_id} is part of all required groups.")
        else:
            print(f"User {user_id} not found.")

def main():
    ldap_server = 'ldap://your_ldap_server'
    ldap_user = 'your_bind_user'
    ldap_password = 'your_password'
    base_dn = 'dc=example,dc=com'

    required_groups = ['az-grp-1', 'az-grp-2', 'az-grp-4']

    user_ids = get_user_ids_from_args()

    server = Server(ldap_server, get_info=ALL)
    conn = Connection(server, ldap_user, ldap_password, auto_bind=True)

    check_user_groups(conn, base_dn, user_ids, required_groups)

    conn.unbind()

if __name__ == "__main__":
    main()
