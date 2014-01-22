from contextlib import contextmanager
import flask
import ldap
import ldap.filter


@contextmanager
def open_ldap_server():
    app = flask.current_app
    ldap_server = LdapServer(
        app.config.get('LDAP_SERVER', 'ldap://localhost'),
        app.config.get('LDAP_BASE_DN', ''),
        app.config.get('LDAP_LOGIN'),
    )
    try:
        yield ldap_server
    finally:
        ldap_server.close()


def get_value(attrs, name, default=None):
    values = attrs.get(name)
    return values[0].decode('utf-8') if values else default


def get_member_groups(attrs):
    for group_dn in attrs.get('memberOf', []):
        (attr, group_name) = group_dn.split(',', 1)[0].split('=')
        assert attr.lower() == 'cn'
        yield group_name


class LdapServer(object):

    def __init__(self, uri, base_dn, login=None):
        self.conn = ldap.initialize(uri)
        self.base_dn = base_dn
        if login is not None:
            (username, password) = login
            result = self.conn.bind_s(username, password)
            if result != (97, []):
                raise RuntimeError("LDAP login failed")

    def close(self):
        self.conn.unbind_s()

    def get_user_info(self, user_id):
        filters = ldap.filter.filter_format(
            '(&(objectClass=user)(sAMAccountName=%s))',
            [user_id],
        )
        results = self.conn.search_s(
            self.base_dn,
            ldap.SCOPE_SUBTREE,
            filters,
            ['memberOf', 'givenName', 'mail', 'company'],
        )
        if len(results) < 1:
            raise RuntimeError("User %r not found" % user_id)
        dn, attrs = results[0]
        return {
            'name': get_value(attrs, 'givenName', ''),
            'email': get_value(attrs, 'mail', None),
            'company': get_value(attrs, 'company', None),
            'groups': list(get_member_groups(attrs)),
        }

    def get_emails_for_group(self, group_name):
        results = self.conn.search_s(
            self.base_dn,
            ldap.SCOPE_SUBTREE,
            '(objectClass=user)',
            ['memberOf', 'mail', 'givenName'],
        )
        rv = []
        for dn, attrs in results:
            if group_name in get_member_groups(attrs):
                email = get_value(attrs, 'mail', None)
                full_name = get_value(attrs, 'givenName', None)
                if email:
                    rv.append({'email': email, 'full_name': full_name})
        return rv
