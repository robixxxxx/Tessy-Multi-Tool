# Tessy-Multi-Tool

**Tessy-Multi-Tool** aplikacja desktopowa napisana w Pythonie, zawiera zestaw pomocniczych narzędzi ułatwiających pracę z TESSY. W skład aplikacji wchodzą :

- **Stub Generator** – automatyczne generowanie szkieletów (stubów) funkcji na podstawie zdefiniowanego szablonu.
- **Typical Values Manager** – zarządzanie zestawami typowych wartości, które można szybko wklejać do CTE.

---

## Spis treści

- [Wymagania](#wymagania)  
- [Instalacja](#instalacja)  
- [Uruchomienie](#uruchomienie)  
- [Przykłady użycia](#przykłady-użycia)   

---

## Wymagania

- Python ≥ 3.8  
- Biblioteka `pyperclip`  

---

## Instalacja

1. Sklonuj repozytorium:
   ```bash
   git clone https://github.com/robixxxxx/Tessy-Multi-Tool.git
   cd Tessy-Multi-Tool

2. Utwórz i aktywuj wirtualne środowisko (opcjonalnie):
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Linux / macOS
   .venv\Scripts\activate      # Windows

3. Zainstaluj zależności:
   ```bash
   pip install -r requirements.txt

## Uruchomienie

Aby uruchomić graficzny interfejs aplikacji uruchom plik main.pyw

## Przykłady użycia

1. Stub Generator
* Skopiuj definicję funkcji (np. bool foo(int x, int * y) ) z Twojego kodu lub z modułu Tessy.
* Kliknij przycisk Dodaj.
* Pojawi się okno ze wszystkimi parametrami wykrytymi w definicji — domyślnie wszystkie są zaznaczone. Odznacz te, których nie chcesz uwzględniać.
* Kliknij Zatwierdź.
* Możesz dodać kolejną funkcję wybierając Dodaj, lub przejść dalej, klikając Generuj.
* W sekcji podglądu zostaną wygenerowane definicje i deklaracje zmiennych, prolog oraz stub funkcji. 
* Aby zapisać wynik do pliku, kliknij przycisk Zapisz.

2. Typical Values
* Z listy wybierz typ danych, ponizej pojawią się wartosci dla danego typu:
   * minimalna
   * minimalna + 1
   * srodkowa
   * maksymalna -1
   * maksymalna 
* Po kliknięciu w daną wartosc kopiuje się ona do schowka w formacie odpowiednim do wklejenia w module CTE Tessy