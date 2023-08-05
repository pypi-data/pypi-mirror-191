# sysnet-directory

Tento balíček obsahuje procedury pro prohledávání osob a skupin na serveru LDAP (AD) 
a extrakci údajů organizační struktury ze získaných hodnot.
Je určen primárně pro projekt eSMLOUVY MŽP.

## Požadavky

Python 3.9+

## Instalace a použití
### pip install sysnet-shopping

(pokud potřebujete ke spuštění  `pip` with oprávnění rool: `sudo pip install sysnet-directory`)

Pak importujte balíček:

```python
import sysnet_directory
```

### Setuptools

Instalace via [Setuptools](http://pypi.python.org/pypi/setuptools).

```sh
python setup.py install --user sysnet-sysnet_directory
```
(nebo `sudo python setup.py install sysnet-directory` pro instalaci balíčku pro všechny uživatele)

A import balíčku:

```python
import sysnet_directory
```

## Použití v programu

Balíček poskytuje singleton `DIRECTORY_FACTORY`, který obsahuje veškerou funkcionalitu. 

### Vyhledání osoby

#### Klíčové slovo 

KLíčovým slovem pro hledání osoby může být jméno, adresa elektronické pošty nebo název funkce 
(to vše včetně zástupných znaků). Vrací seznam (list) slovníků (dictinary).

    from sysnet_directory.factory import DIRECTORY_FACTORY
    ...
    user_list = DIRECTORY_FACTORY.get_user('Jos*')
    user_list = DIRECTORY_FACTORY.get_all_users()

Pro případ potřeby lze tuto funkci zavolat jako "raw". Pak vrací surovou odpověď LDAP serveru. 
    
    user_list = DIRECTORY_FACTORY.get_user_raw('Jos*')

#### Organizační jednotka

Osoby lze vyhledávat rovněž podle kódu organizační jednotky:

    user_list = DIRECTORY_FACTORY.get_user(ou='210')

vrací všechny osoby z organizační jednotky 210.

#### Vedoucí funkce

Lze vyhledávat osoby podle vedoucí funkce:

    user_list = DIRECTORY_FACTORY.get_user(head=True)

Vrátí všechny vedoucí v organizaci

    user_list = DIRECTORY_FACTORY.get_user(ou='210', head=True)

Vrátí vedoucí v organizační jednotce 210

#### Informace o zařazení do organizační struktury

Vrácený slovník pro uživatele obsahuje kromě identifikačních a popisných údajů tyto struktury:

1. **division** - strom všech organizačních jednotek, kam uživatel spadá
2. **org_info** - příznak vedoucí funkce, kód aktuální organizační jednotky a kód nadřízené organizační jednotky

    
### Vyhledání skupiny

KLíčovým slovem pro hledání skupiny je její název včetně zástupných znaků. Vrací seznam (list) slovníků (dictinary).

    ...
    group_list = DIRECTORY_FACTORY.get_group('*3')
    group_list = DIRECTORY_FACTORY.get_all_groups()

Pro případ potřeby lze tuto funkci zavolat jako "raw". Pak vrací surovou odpověď LDAP serveru. 
    
    user_list = DIRECTORY_FACTORY.get_group_raw('Jos*')

### Organizační struktura

Factory obsahuje funkcionalitu, která dokáže z LDAP dat extrahovat organizační strukturu. 
Organizační struktura je ve stromové formě. Uzly jsou propojeny oběma směry. 

    ...
    os = DIRECTORY_FACTORY.get_org_structure()

### Ošetření chyb

Pokud se nepodaří připojit k LDAP serveru, modul nahlásí chybu a příznak ready u DIRECTORY_FACTORY je nastaven na False

    DIRECTORY_FACTORY.ready


## Systémové proměnné

Nastavení factory je řízeno systémovými proměnnými

- **LDAP_SERVER_URI** - ve formátu např `ldap://localhost:389`
- **LDAP_BIND_DN** - přihlašovací jméno k serveru
- **LDAP_BIND_PASSWORD** - heslo k přihlašovacímu jménu
- **LDAP_BASE_DN** - základní kontext. Např. `OU=eSML,DC=ad,DC=mzp,DC=cz`

Implicitní nastavení nebo nastavení přes systémové proměnné lze vždy přebít ruční operací **reset**

    DIRECTORY_FACTORY.reset(uri=<uri>, bind_dn=<name>, bind_password=<password>, base_dn=<context>)
