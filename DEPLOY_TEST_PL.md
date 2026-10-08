# Instalacja na nowym testowym repozytorium

1. Rozpakuj archiwum. W głównym katalogu powinny znajdować się bezpośrednio `app.py`, `requirements.txt`, `.streamlit/`, `pages/`, `sections/`, `src/`, `data/` i `tests/`.
2. Utwórz nowe puste repo GitHub, np. `dynamic-player-dna-test-2`.
3. Na stronie głównej pustego repo wybierz **uploading an existing file**. Przeciągnij **zawartość** rozpakowanego katalogu, nie folder nadrzędny.
4. Sprawdź ścieżki przed commitem: `app.py` i `requirements.txt` w głównym katalogu; `pages/modelling.py`, `pages/player_comparison.py`; `sections/pca_explorer.py`; `src/comparison_options.py`.
5. Kliknij **Commit changes**.
6. Streamlit Community Cloud: Create app -> repo `HubertGogola/dynamic-player-dna-test-2`, branch `main`, main file `app.py`, Python `3.12`, Deploy.
7. Sprawdź nawigację: Start / Player analysis / Modelling & reference, bez View more / View less. Potem Player comparison (role, scope, squad, Player A / Player B).

Informacja: publiczny plik `data/synthetic_player_data.csv` jest syntetyczny. Nie dodawaj żadnych eksportów klubowych ani surowych danych z pracy.
