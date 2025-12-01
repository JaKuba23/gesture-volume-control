# MOTUS

```
 ███╗   ███╗ ██████╗ ████████╗██╗   ██╗███████╗
 ████╗ ████║██╔═══██╗╚══██╔══╝██║   ██║██╔════╝
 ██╔████╔██║██║   ██║   ██║   ██║   ██║███████╗
 ██║╚██╔╝██║██║   ██║   ██║   ██║   ██║╚════██║
 ██║ ╚═╝ ██║╚██████╔╝   ██║   ╚██████╔╝███████║
 ╚═╝     ╚═╝ ╚═════╝    ╚═╝    ╚═════╝ ╚══════╝
```

**Profesjonalny system sterowania głośnością gestami dla macOS wykorzystujący uczenie maszynowe**

[English Documentation](../../README.md)

[![CI Status](https://github.com/JaKuba23/motus/workflows/CI/badge.svg)](https://github.com/JaKuba23/motus/actions)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

---

## Przegląd

Motus to aplikacja produkcyjna umożliwiająca bezdotykowe sterowanie głośnością systemową poprzez intuicyjne gesty dłoni. Zbudowana z wykorzystaniem śledzenia dłoni MediaPipe oraz wizji komputerowej OpenCV, demonstruje zaawansowaną integrację uczenia maszynowego dla interakcji człowiek-komputer na platformie macOS.

## Kluczowe Funkcje

- Wykrywanie punktów orientacyjnych dłoni w czasie rzeczywistym za pomocą MediaPipe Hands (śledzenie 21 punktów)
- Sterowanie głośnością gestami z 5-stopniową precyzją (0-100%)
- System aktywacji poprzez gest kciuka w górę
- Adaptacyjny algorytm wygładzania dla redukcji drgań
- Zoptymalizowane dla procesorów Apple Silicon (M1/M2)
- Kompleksowy zestaw testów z pokryciem kodu 80%+
- Wsparcie Docker dla rozwoju wieloplatformowego
- Implementacja type-safe z pełną zgodnością mypy strict

## Szybki Start

### Wymagania

- macOS 11.0 lub nowszy
- Python 3.10, 3.11 lub 3.12
- Kamera internetowa z włączonymi uprawnieniami
- Minimum 4GB RAM (zalecane 8GB dla optymalnej wydajności)

### Instalacja

```bash
# Sklonuj repozytorium
git clone https://github.com/JaKuba23/motus.git
cd motus

# Utwórz wirtualne środowisko
python3 -m venv venv
source venv/bin/activate

# Zainstaluj zależności
pip install --upgrade pip
pip install -r requirements.txt
```

### Uruchomienie Aplikacji

```bash
# Standardowe uruchomienie
python -m motus

# Alternatywnie
python src/motus/main.py
```

### Uprawnienia Kamery

Włącz dostęp do kamery w Ustawieniach Systemowych:

```
Ustawienia Systemowe → Prywatność i Bezpieczeństwo → Kamera → Włącz dla Terminala/Python
```

## Użytkowanie

### Podstawowe Sterowanie

| Gest | Poziom Głośności | Opis |
|------|------------------|------|
| Zaciśnięta pięść | 0% | Wyciszenie |
| 1 palec wyprostowany | 20% | Niska głośność |
| 2 palce wyprostowane | 40% | Średnio-niska głośność |
| 3 palce wyprostowane | 60% | Średnia głośność |
| 4 palce wyprostowane | 80% | Średnio-wysoka głośność |
| Otwarta dłoń (5 palców) | 100% | Maksymalna głośność |
| Kciuk w górę | Przełącznik | Włącz/wyłącz sterowanie |

### Polecenia Klawiatury

- `Q` - Zakończ aplikację

### Wskazówki dla Optymalnej Wydajności

- Umieść dłoń 30-60cm od kamery
- Zapewnij odpowiednie oświetlenie (zalecane >300 lux)
- Utrzymuj dłoń w pełni widoczną w kadrze
- Wykonuj płynne ruchy dla gładkich przejść głośności

## Architektura

```
motus/
├── src/motus/              # Kod źródłowy
│   ├── __init__.py         # Inicjalizacja pakietu
│   ├── main.py             # Punkt wejścia aplikacji
│   ├── config.py           # Zarządzanie konfiguracją
│   ├── hand_tracking.py    # Integracja MediaPipe
│   ├── gestures.py         # Algorytmy rozpoznawania gestów
│   └── mac_controls.py     # Sterowanie głośnością macOS przez AppleScript
├── tests/                  # Zestaw testów
│   ├── unit/               # Testy jednostkowe
│   └── integration/        # Testy integracyjne
├── docs/                   # Rozszerzona dokumentacja
├── .github/                # Przepływy pracy CI/CD
└── pyproject.toml          # Konfiguracja projektu
```

### Stos Technologiczny

| Komponent | Technologia | Wersja |
|-----------|-------------|---------|
| Śledzenie Dłoni | MediaPipe Hands | 0.10.13 |
| Wizja Komputerowa | OpenCV | 4.8.1 |
| Obliczenia Numeryczne | NumPy | 1.26.4 |
| Sterowanie Głośnością | AppleScript (osascript) | Natywny |
| Testowanie | pytest | 7.4+ |
| Sprawdzanie Typów | mypy | 1.5+ |

## Konfiguracja

Konfiguruj poprzez zmienne środowiskowe:

```bash
# Źródło kamery (indeks lub ścieżka do pliku wideo)
export CAMERA_SOURCE=0

# Tryb bezgłowy (bez GUI)
export HEADLESS=1
```

Edytuj konfigurację w `src/motus/config.py`:

```python
@dataclass(frozen=True)
class AppConfig:
    smoothing_window: int = 5           # Klatki dla średniej ruchomej
    toggle_cooldown: float = 1.0        # Sekundy między przełączeniami
    min_detection_confidence: float = 0.7
    min_tracking_confidence: float = 0.5
    target_fps: int = 30
```

## Rozwój

### Konfiguracja Środowiska Deweloperskiego

```bash
# Zainstaluj zależności deweloperskie
pip install -r requirements-dev.txt

# Zainstaluj hooki pre-commit
pre-commit install
```

### Uruchom Testy

```bash
# Uruchom wszystkie testy z pokryciem
pytest --cov=motus --cov-report=term-missing

# Uruchom konkretny zestaw testów
pytest tests/unit/
pytest tests/integration/

# Uruchom z markerami
pytest -m unit
pytest -m integration
```

### Jakość Kodu

```bash
# Formatuj kod
black src/ tests/
isort src/ tests/

# Linting
flake8 src/ tests/

# Sprawdzanie typów
mypy src/motus --strict

# Skanowanie bezpieczeństwa
bandit -r src/motus
safety check
```

## Deployment Docker

### Budowanie i Uruchamianie

```bash
# Zbuduj obraz
docker compose build

# Uruchom w trybie headless
docker compose up

# Uruchom z plikiem wideo
docker compose run --rm -e CAMERA_SOURCE=/app/video.mp4 app
```

### Ograniczenia

Deployment Docker na macOS ma ograniczenia:
- Kamera hosta nie może być dostępna z kontenera
- Sterowanie głośnością systemową niedostępne w kontenerze
- Nadaje się tylko do testów/pipelineów CI

Do użytku produkcyjnego na macOS uruchamiaj natywnie poza Dockerem.

## Wydajność

Benchmarki na Apple M1 MacBook Pro (16GB RAM):

| Metryka | Wartość |
|---------|---------|
| Częstotliwość Klatek | 30-60 FPS |
| Użycie CPU | 8-15% (jeden rdzeń) |
| Użycie Pamięci | ~250MB |
| Opóźnienie Detekcji | <33ms (30 FPS) |
| Czas Reakcji Gestu | 100-200ms |

## Rozwiązywanie Problemów

### Kamera Się Nie Otwiera

- Zamknij aplikacje używające kamery (Zoom, FaceTime, etc.)
- Zweryfikuj uprawnienia kamery w Ustawieniach Systemowych
- Sprawdź czy kamera nie jest wyłączona sprzętowo
- Zrestartuj Terminal/IDE

### Problemy z Detekcją Dłoni

- Popraw warunki oświetleniowe
- Upewnij się, że dłoń jest w pełni w kadrze
- Dostosuj `min_detection_confidence` w konfiguracji
- Wyczyść obiektyw kamery

### Problemy z Wydajnością

- Zamknij aplikacje wymagające dużo zasobów
- Zmniejsz `target_fps` w konfiguracji
- Wyłącz rysowanie punktów orientacyjnych dłoni (`draw=False`)
- Użyj niższej rozdzielczości kamery poprzez `CAMERA_SOURCE`

## Współpraca

Zapraszamy do współpracy! Zobacz [CONTRIBUTING.md](../../CONTRIBUTING.md) dla:

- Konfiguracji środowiska deweloperskiego
- Standardów kodowania
- Wymagań testowych
- Procesu pull requestów

## Bezpieczeństwo

Dla luk bezpieczeństwa, zobacz [SECURITY.md](../../SECURITY.md).

Nie otwieraj publicznych issues dla kwestii bezpieczeństwa.

## Dokumentacja

- [Dokumentacja Architektury](../architecture.md)
- [Referencja API](../api.md)
- [Przewodnik Deploymentu](../deployment.md)
- [Angielska Dokumentacja](../../README.md)

## Changelog

Zobacz [CHANGELOG.md](../../CHANGELOG.md) dla historii wersji.

## Licencja

Ten projekt jest licencjonowany na licencji MIT - zobacz plik [LICENSE](../../LICENSE).

## Podziękowania

- [MediaPipe](https://google.github.io/mediapipe/) od Google za framework śledzenia dłoni
- [OpenCV](https://opencv.org/) za bibliotekę wizji komputerowej
- Inspirowane systemami sterowania gestami w motoryzacji

## Autor

**Stworzony przez JaKuba23**

- GitHub: [@JaKuba23](https://github.com/JaKuba23)
- Portfolio: [jakuba23.dev](https://jakuba23.dev)

---

**Profesjonalny Projekt Portfolio AI/ML**

Demonstruje: Wizję Komputerową | Uczenie Maszynowe | Przetwarzanie w Czasie Rzeczywistym | Integrację Systemową | Profesjonalną Inżynierię Oprogramowania

---

## Status Projektu

**Gotowy do Produkcji** - Pełne testy, dokumentacja i możliwość wdrożenia

- Pipeline CI/CD z GitHub Actions
- 80%+ pokrycie testami
- Type-safe z mypy strict mode
- Skanowanie bezpieczeństwa z Bandit
- Automatyczne aktualizacje zależności przez Dependabot

---

Jeśli ten projekt jest przydatny, rozważ danie gwiazdki ⭐

