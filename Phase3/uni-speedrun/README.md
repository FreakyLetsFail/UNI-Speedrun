# Uni Speedrun

Uni Speedrun ist ein konfigurierbares TUI-Dashboard zur Planung eines
Studienverlaufs. Das Projekt entsteht im Rahmen des Kurses DLBDSOOFPP01_D.

## Entwicklungsumgebung unter Windows

Voraussetzungen:

- Python 3.10 oder neuer
- Git
- Windows Terminal oder das Terminal in Visual Studio Code

```powershell
git clone <URL-DES-GITHUB-REPOSITORYS>
cd uni-speedrun
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python src/main.py
```

Für die Entwicklung und die Tests werden zusätzlich die Entwicklungsabhängigkeiten
installiert:

```powershell
python -m pip install -r requirements-dev.txt
python -m pytest
```

Die virtuelle Umgebung wird mit folgendem Befehl verlassen:

```powershell
deactivate
```

Die virtuelle Umgebung `.venv` wird nicht in Git gespeichert. Sie wird auf
jedem Rechner mit den oben genannten Befehlen neu erzeugt.



## Phase-3-Prototyp

Der aktuelle Prototyp enthält neben dem Dashboard:

- Studienplan in den Einstellungen bearbeiten
- Module hinzufügen, bearbeiten und löschen
- abgeschlossene Module im Archiv anzeigen
- Module über `[M]` starten bzw. abschließen (überführt aktives Modul in *Warte auf Ergebnis*)
- Statusübergang zu *Abgeschlossen* inkl. Note in den Einstellungen
- Fortschritt und gespeicherte Daten direkt aktualisieren
- Dashboard-Shortcuts direkt im Screen statt im Textual-Footer

Start unter macOS/Linux:

```bash
# Entweder direkt mit python3:
PYTHONPATH=src python3 -m uni_speedrun.main

# Oder mit aktivierter virtueller Umgebung:
source .venv/bin/activate
PYTHONPATH=src python -m uni_speedrun.main
```
