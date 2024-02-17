API
===

apis.py
-------

Moduł `apis.py` zawiera implementacje endpointów API.

create_contact
~~~~~~~~~~~~~~
Tworzy nowy kontakt.

Metoda HTTP: POST
Ścieżka: `/contacts/`
Argumenty:
- `contact`: Dane nowego kontaktu.
- `current_user`: Obecnie uwierzytelniony użytkownik.

get_all_contacts
~~~~~~~~~~~~~~~~~
Pobiera wszystkie kontakty lub wyszukuje kontakty według imienia, nazwiska lub adresu e-mail.

Metoda HTTP: GET
Ścieżka: `/contacts/`
Argumenty:
- `q`: Wyszukiwany ciąg znaków.
- `db`: Sesja bazy danych.

get_contact
~~~~~~~~~~~
Pobiera kontakt według ID.

Metoda HTTP: GET
Ścieżka: `/contacts/{contact_id}`
Argumenty:
- `contact_id`: ID kontaktu.
- `db`: Sesja bazy danych.
- `current_user`: Obecnie uwierzytelniony użytkownik.

update_contact
~~~~~~~~~~~~~~
Aktualizuje kontakt według ID.

Metoda HTTP: PUT
Ścieżka: `/contacts/{contact_id}`
Argumenty:
- `contact_id`: ID kontaktu do aktualizacji.
- `contact`: Nowe dane kontaktu.
- `db`: Sesja bazy danych.

delete_contact
~~~~~~~~~~~~~~
Usuwa kontakt według ID.

Metoda HTTP: DELETE
Ścieżka: `/contacts/{contact_id}`
Argumenty:
- `contact_id`: ID kontaktu do usunięcia.
- `db`: Sesja bazy danych.

get_birthdays_within_7_days
~~~~~~~~~~~~~~~~~~~~~~~~~~~
Pobiera kontakty z urodzinami w ciągu najbliższych 7 dni.

Metoda HTTP: GET
Ścieżka: `/contacts/birthdays/`
Argumenty:
- `db`: Sesja bazy danych.

upload_avatar
~~~~~~~~~~~~~
Przesyła awatar dla użytkownika.

Metoda HTTP: POST
Ścieżka: `/users/avatar/upload/`
Argumenty:
- `file`: Plik awatara do przesłania.
- `current_user`: Obecnie uwierzytelniony użytkownik.

login_for_access_token
~~~~~~~~~~~~~~~~~~~~~~
Loguje się, aby uzyskać token dostępu.

Metoda HTTP: POST
Ścieżka: `/token/`
Argumenty:
- `form_data`: Dane formularza z nazwą użytkownika i hasłem.

