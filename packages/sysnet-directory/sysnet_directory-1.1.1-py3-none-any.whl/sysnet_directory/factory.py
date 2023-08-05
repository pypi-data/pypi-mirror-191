import logging
import os
from copy import deepcopy

import ldap

# LDAP_SERVER_URI = 'ldap://localhost:11389'
LDAP_SERVER_URI = os.getenv('LDAP_SERVER_URI', 'ldap://10.0.101.7:389')
LDAP_BIND_DN = os.getenv('LDAP_BIND_DN', 'svc.ADreader.eSML')
LDAP_BIND_PASSWORD = os.getenv('LDAP_BIND_PASSWORD', 'xu#GnJNiPsc*kWeq2TDKQ')
# BASE_DN = os.getenv('LDAP_BASE_DN', 'OU=MZP,DC=ad,DC=mzp,DC=cz')
BASE_DN = os.getenv('LDAP_BASE_DN', 'OU=eSML,DC=ad,DC=mzp,DC=cz')
BASE_DN_GROUPS = 'OU=Groups,{}'.format(BASE_DN)
BASE_DN_USERS = 'OU=Users,{}'.format(BASE_DN)

logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s', level=logging.INFO)


class DirectoryException(Exception):
    """
    Chybová procedura modulu
    """
    pass


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class DirectoryFactory(object, metaclass=Singleton):
    def __init__(self, uri=LDAP_SERVER_URI, bind_dn=LDAP_BIND_DN, bind_password=LDAP_BIND_PASSWORD, base_dn=BASE_DN):
        try:
            self.uri = uri
            self.bind_dn = bind_dn
            self.bind_password = bind_password
            self.base_dn = base_dn
            self.base_dn_groups = 'OU=Groups,{}'.format(self.base_dn)
            self.base_dn_users = 'OU=Users,{}'.format(self.base_dn)
            self.client = create_ldap_client(uri=self.uri, dn=self.bind_dn, password=self.bind_password)
            if self.client is None:
                self.ready = False
                logging.error('DirectoryFactory failed')
            else:
                self.ready = True
                logging.info('DirectoryFactory created')
        except DirectoryException as e:
            self.client = None
            self.ready = False
            logging.error('DirectoryFactory failed: {}'.format(e))

    def reset(self, uri=LDAP_SERVER_URI, bind_dn=LDAP_BIND_DN, bind_password=LDAP_BIND_PASSWORD, base_dn=BASE_DN):
        self.__init__(uri=uri, bind_dn=bind_dn, bind_password=bind_password, base_dn=base_dn)
        return self

    def get_group_raw(self, key=None):
        """Vrátí seznam skupin

        Pro klíčové slovo názvu skupiny vrací seznam odpovídajících skupin.
        Lze použít zástupné znaky. Např. '20*' nebo '*3'
        Návratová hodnota je stavová indoemace a data

        Použití:
        status, data = get_group_raw('*3')

        :param key:  Klíčové slovo pro skupinu
        :return:    status - stavová informace (int). 101, pokud OK
                    data - seznam (list) tuplů obsahujících název a vlastní data
        """
        if not self.ready:
            raise DirectoryException('LDAP Factory not ready')
        search_filter = 'objectClass~=group'
        if key is not None:
            search_filter = '(&({})(CN={}))'.format(search_filter, key)
            # search_filter = '(&({})(CN~={}))'.format(search_filter, key)
        search_scope = ldap.SCOPE_SUBTREE
        retrieve_attributes = None
        try:
            l_search = self.client.search(self.base_dn_groups, search_scope, search_filter, retrieve_attributes)
            result_status, result_data = self.client.result(l_search)
            return result_status, result_data
        except ldap.LDAPError as e:
            raise DirectoryException('LDAPError: {}'.format(e))

    def get_user_raw(self, key=None, ou=None, head=False):
        """
        Pro klíčové slovo osoby (email, jméno) vrací seznam odpovídajících osob.
        Lze použít zástupné znaky. Např. 'Sekce*' nebo '*Namestek'
        Návratová hodnota je stavová indoemace a data

        Použití:
        status, data = get_user_raw('*Namestek')

        :param head: Vedoucí organizační jednotky
        :param ou:  Organizační jednotka
        :param key:  Klíčové slovo pro osobu
        :return:    status - stavová informace (int). 101, pokud OK
                    data - seznam (list) tuplů obsahujících název a vlastní data
        """
        if not self.ready:
            raise DirectoryException('LDAP Factory not ready')
        search_filter = 'objectClass~=person'
        sf = []
        if key is not None:
            # search_filter = '(&({0})(|(mail={1})(cn={1})(userPrincipalName={1})(title={1})))'.format(search_filter, key)
            sf.append('(|(mail={0})(cn={0})(userPrincipalName={0})(title={0}))'.format(key))
        if ou is not None:
            # search_filter = '(&({})(departmentNumber~={}))'.format(search_filter, ou)
            # extensionAttribute4
            sf.append('(|(departmentNumber={0})(extensionAttribute4={0})(extensionAttribute5={0}))'.format(ou))
        if head:
            # search_filter = '(&({})(extensionAttribute2=1))'.format(search_filter)
            sf.append('(extensionAttribute2=1)')
        if sf:
            k = ''.join(sf)
            search_filter = '(&({0}){1})'.format(search_filter, k)
        search_scope = ldap.SCOPE_SUBTREE
        retrieve_attributes = None
        try:
            print(search_filter)
            l_search = self.client.search(self.base_dn_users, search_scope, search_filter, retrieve_attributes)
            result_status, result_data = self.client.result(l_search)
            return result_status, result_data
        except ldap.LDAPError as e:
            raise DirectoryException('LDAPError: {}'.format(e))

    def get_group(self, key=None):
        """Vrátí seznam skupin

        Pro klíčové slovo názvu skupiny vrací seznam odpovídajících skupin.
        Lze použít zástupné znaky. Např. '20*' nebo '*3'
        Návratová hodnota je seznam (list) slovníků (dict)

        :param key:  Klíčové slovo názvu skupiny
        :return:
        """
        if not self.ready:
            raise DirectoryException('LDAP Factory not ready')
        status, data = self.get_group_raw(key=key)
        out = []
        for item in data:
            dn = item[0]
            m_from = item[1]['member']
            m_to = []
            for m in m_from:
                m_to.append(str(m, 'utf-8'))
            desc = _get_item_value_string(item[1], 'description')
            out.append({'dn': dn, 'member': m_to, 'description': desc})
        return out

    def get_user(self, key=None, ou=None, head=False):
        """
        Pro klíčové slovo osoby (email, jméno) vrací seznam odpovídajících osob.
        Lze použít zástupné znaky. Např. 'Sekce*' nebo '*Namestek'
        Návratová hodnota je seznam (list) slovníků (dict)

        :param head: Vedoucí organizační jednotky
        :param ou: Organizační jednotka
        :param key: Klíčové slovo pro osobu
        :return:
        """
        if not self.ready:
            raise DirectoryException('LDAP Factory not ready')
        status, data = self.get_user_raw(key=key, ou=ou, head=head)
        out = []
        for item in data:
            user = _user_to_dict(user_item=item)
            out.append(user)
        return out

    def get_all_users(self):
        return self.get_user()

    def get_all_groups(self):
        return self.get_group()

    def get_org_structure(self):
        """Vrátí organizační strukturu

        :return:
        """
        if not self.ready:
            raise DirectoryException('LDAP Factory not ready')
        out = _extract_org_structure(self.get_all_users())
        return out


def create_ldap_client(uri=LDAP_SERVER_URI, dn=LDAP_BIND_DN, password=LDAP_BIND_PASSWORD):
    """vytvoří klienta LDAP

    Vatvoří klienta LDAP serveru

    :param uri: URI serveru LDAP v podobě naoř. ldap://localhost:11389
    :type uri: str
    :param dn:  Ověřování totožnosti přístupu k serveru - uživatelské jméno nebo Bind DN
    :type dn: str
    :param password:    Ověřování totožnosti přístupu k serveru - heslo
    :type password: str
    :return:
    :rtype: ldap.ldapobject.SimpleLDAPObject
    """
    try:
        out = ldap.initialize(uri)
        out.protocol_version = ldap.VERSION3
        out.simple_bind_s(dn, password)
    except ldap.SERVER_DOWN:
        logging.error('LDAP server {} is not reachable'.format(uri))
        out = None
    except ldap.INVALID_CREDENTIALS:
        logging.error('Invalid LDAP credentials')
        out = None
    return out


def _user_to_dict(user_item):
    dn = user_item[0]
    member = []
    if 'memberOf' in user_item[1]:
        for it in user_item[1]['memberOf']:
            member.append(str(it, 'utf-8'))
    title = _get_item_value_string(user_item[1], 'title')
    name = _get_item_value_string(user_item[1], 'displayName')
    mail = _get_item_value_string(user_item[1], 'mail')
    first_name = _get_item_value_string(user_item[1], 'givenName')
    last_name = _get_item_value_string(user_item[1], 'sn')
    is_head = _get_item_value_boolean(user_item[1], 'extensionAttribute2')
    head_ou = None
    division = []
    # organizace
    organization_level_0 = {
        'code': 'MZP',
        'value': _get_item_value_string(user_item[1], 'company')
    }
    division.append(organization_level_0)
    # sekce
    organization_level_1 = {
        'code': _get_item_value_string(user_item[1], 'extensionAttribute5'),
        'value': _get_item_value_string(user_item[1], 'extensionAttribute7')
    }
    if organization_level_1['code'] != '':
        head_ou = organization_level_1['code']
        division.append(organization_level_1)
    # odbor
    organization_level_2 = {
        'code': _get_item_value_string(user_item[1], 'extensionAttribute4'),
        'value': _get_item_value_string(user_item[1], 'extensionAttribute6')
    }
    if organization_level_2['code'] != '':
        head_ou = organization_level_2['code']
        division.append(organization_level_2)
    # oddělení
    organization_level_3 = {
        'code': _get_item_value_string(user_item[1], 'departmentNumber'),
        'value': _get_item_value_string(user_item[1], 'department')
    }
    if organization_level_3['code'] != '':
        head_ou = organization_level_3['code']
        division.append(organization_level_3)
    degree = _get_item_value_string(user_item[1], 'extensionAttribute8')
    higher = ''
    if len(division) > 1:
        higher = division[-2]['code']
    org_info = {'is_head': is_head, 'ou': head_ou, 'higher_ou': higher}
    out = {
        'dn': dn, 'member': member, 'title': title, 'name': name, 'username': mail, 'email': mail,
        'first_name': first_name, 'last_name': last_name, 'degree': degree, 'division': division,
        'org_info': org_info
    }
    return out


def _extract_org_structure(user_list):
    """Extrahuje ornanizační strukturu ze seznamu uživatelů

    :param user_list: Seznam uživatelů
    :return:
    """
    org_structure = None
    for user in user_list:
        org_structure = _merge_user_to_os(user=user, org_structure=org_structure)
    return org_structure


def _merge_user_to_os(user=None, org_structure=None):
    # print(user['dn'])
    tree = _get_directory_tree(user=user)
    if (org_structure is None) or ('code' not in org_structure):
        org_structure = deepcopy(tree)
        return org_structure
    l0 = deepcopy(tree)
    l1 = None
    l2 = None
    l3 = None
    l4 = None
    if (l0 is not None) and l0['children']:
        l1 = deepcopy(l0['children'][0])
    if (l1 is not None) and l1['children']:
        l2 = deepcopy(l1['children'][0])
    if (l2 is not None) and l2['children']:
        l3 = deepcopy(l2['children'][0])
    if (l3 is not None) and l3['children']:
        l4 = deepcopy(l3['children'][0])
    os_l0 = org_structure
    os_l1 = None
    os_l2 = None
    os_l3 = None
    os_l4 = None
    if l0['code'] != os_l0['code']:
        raise DirectoryException('Organization code \"{}\"is invalid.'.format(l0['code']))
    if (os_l0 is not None) and os_l0['children'] and (l1 is not None):
        match1 = list(filter(lambda ou: ou['code'] == l1['code'], os_l0['children']))
        if bool(match1):
            os_l1 = match1[0]
    if (os_l1 is not None) and os_l1['children'] and (l2 is not None):
        match2 = list(filter(lambda ou: ou['code'] == l2['code'], os_l1['children']))
        if bool(match2):
            os_l2 = match2[0]
    if (os_l2 is not None) and os_l2['children'] and (l3 is not None):
        match3 = list(filter(lambda ou: ou['code'] == l3['code'], os_l2['children']))
        if bool(match3):
            os_l3 = match3[0]
    if (os_l3 is not None) and os_l3['children'] and (l4 is not None):
        match4 = list(filter(lambda ou: ou['code'] == l4['code'], os_l3['children']))
        if bool(match4):
            os_l4 = match4[0]
    if (os_l1 is None) and (l1 is not None):
        os_l0['children'].append(l1)
        return org_structure
    if (os_l2 is None) and (l2 is not None):
        os_l1['children'].append(l2)
        return org_structure
    if (os_l3 is None) and (l3 is not None):
        os_l2['children'].append(l3)
        return org_structure
    if (os_l4 is None) and (l4 is not None):
        os_l3['children'].append(l4)
    return org_structure


def _get_directory_tree(user):
    i = 0
    out = {}
    work = None
    parent = None
    for div in user['division']:
        if i == 0:
            out = deepcopy(div)
            parent = deepcopy(div)
            out['children'] = []
            work = out['children']
        else:
            ou = deepcopy(div)
            parent_next = deepcopy(div)
            ou['children'] = []
            ou['parent'] = deepcopy(parent)
            work.append(ou)
            work = ou['children']
            parent = parent_next
        i += 1
    return out


def _get_item_value_string(data_dict, item_name):
    if data_dict is None:
        return None
    out = ''
    if item_name in data_dict:
        out = str(data_dict[item_name][0], 'utf-8')
    return out


def _get_item_value_boolean(data_dict, item_name):
    out = False
    val = _get_item_value_string(data_dict=data_dict, item_name=item_name)
    if val == '1':
        out = True
    return out


DIRECTORY_FACTORY = DirectoryFactory()
