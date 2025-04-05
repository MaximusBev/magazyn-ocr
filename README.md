
# Magazyn OCR – System do zarządzania zdjęciami i tekstem z obrazów

To aplikacja webowa stworzona z użyciem **Flask**, **OpenCV** i **Tesseract**, która umożliwia:
- Dodawanie zdjęć do folderów przypisanych firmom.
- Automatyczne rozpoznawanie tekstu na zdjęciach (OCR).
- Wyszukiwanie zdjęć na podstawie tekstu.
- Zarządzanie folderami i zdjęciami (usuwanie, podgląd).
- Profesjonalny i nowoczesny wygląd z animacjami oraz responsywnym interfejsem.

## Wymagania

Przed uruchomieniem należy zainstalować wymagane biblioteki:

```bash
pip install -r requirements.txt
```

Dodatkowo musisz mieć zainstalowany **Tesseract-OCR** z językiem `pol` (polski).

**Windows**: [https://github.com/UB-Mannheim/tesseract/wiki](https://github.com/UB-Mannheim/tesseract/wiki)  
Upewnij się, że ścieżka do Tesseract znajduje się w zmiennych środowiskowych.

## Uruchomienie aplikacji

```bash
python app.py
```

Następnie otwórz przeglądarkę i przejdź do: [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Funkcje

- ✅ Upload wielu zdjęć jednocześnie.
- ✅ Tworzenie nowych folderów lub wybór istniejących.
- ✅ Automatyczne OCR i zapisywanie wyników.
- ✅ Wyszukiwanie po fragmencie tekstu.
- ✅ Responsywny interfejs i ciemna estetyka.
- ✅ Możliwość usuwania zdjęć i folderów.

## Autor

Projekt został stworzony przez **Maksyma Seliuhina (Hoxa)**  
[https://hoxa.pl/en/home/](https://hoxa.pl/en/home/)
