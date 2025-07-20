# Sports Joiner

Aplikacja webowa umożliwiająca organizowanie i dołączanie do wydarzeń sportowych.

## 🛠️ Technologie

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white&style=for-the-badge)
![Django](https://img.shields.io/badge/Django-092E20?logo=django&logoColor=white&style=for-the-badge)
![SQLite3](https://img.shields.io/badge/SQLite-003B57?logo=sqlite&logoColor=white&style=for-the-badge)
![Pillow](https://img.shields.io/badge/Pillow-6F4E37?logo=pillow&logoColor=white&style=for-the-badge)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?logo=html5&logoColor=white&style=for-the-badge)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?logo=css3&logoColor=white&style=for-the-badge)
![Bootstrap](https://img.shields.io/badge/Bootstrap-7952B3?logo=bootstrap&logoColor=white&style=for-the-badge)

## Struktura projektu

- `app/` – główna aplikacja Django (modele, widoki, formularze, szablony)
- `config/` – konfiguracja projektu Django
- `media/` – pliki przesyłane przez użytkowników (np. zdjęcia profilowe)
- `static/` – statyczne pliki CSS i obrazy
- `templates/` – szablony HTML

## Instalacja i uruchomienie

1. **Klonuj repozytorium:**
   git clone <adres_repozytorium> cd Sports_Joiner
   
3. **Utwórz i aktywuj wirtualne środowisko:**
  python -m venv venv venv\Scripts\activate

3. **Zainstaluj zależności:**
   pip install -r requirements.txt

4. **Wykonaj migracje bazy danych:**
   python manage.py migrate

5. **Uruchom serwer deweloperski:**
   python manage.py runserver

6. **Otwórz przeglądarkę i przejdź do:**
   http://127.0.0.1:8000/

## Licencja

Projekt edukacyjny – do własnego użytku.
