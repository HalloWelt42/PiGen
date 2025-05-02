# Pi-Generator mit Checkpointing (Chudnovsky-Algorithmus)

Dieses Python-Projekt berechnet die Kreiszahl π fortlaufend und speichert regelmäßig Ergebnisse in eine Datei, sodass die Berechnung jederzeit unterbrechbar und fortsetzbar ist.

Die Berechnung erfolgt blockweise: Alle 100 neuen Ziffern werden dauerhaft in eine Datei geschrieben (`pi_output.txt`) und der Zustand (Iteration, Zwischensumme, Präzision) wird in einer separaten JSON-Datei (`pi_checkpoint.json`) gespeichert.

---

## ✨ Features

- **Chudnovsky-Algorithmus** zur hocheffizienten Berechnung von π
- Fortschritt wird automatisch gespeichert (Checkpoint)
- Die Berechnung läuft unendlich, bis man sie manuell mit `Ctrl+C` abbricht
- Bei Neustart wird der letzte Stand geladen und exakt dort weitergerechnet
- Fortschritt wird alle 100 Stellen in der Konsole angezeigt und gespeichert
- Ideal für Langzeitrechnungen, Forschung oder Demonstrationen

---

## 🧠 Verwendeter Algorithmus: Chudnovsky-Methode

Der Algorithmus basiert auf einer sehr schnell konvergenten Reihe, die erstmals 1988 von den Brüdern **David und Gregory Chudnovsky** vorgestellt wurde. Sie wurde zur Berechnung vieler Weltrekorde für Nachkommastellen von π eingesetzt.

> Diese Methode basiert auf einer Reihe mit extrem schneller Konvergenz, die auf Arbeiten von **Srinivasa Ramanujan** zurückgeht. Sie nutzt Eigenschaften sogenannter **Heegner-Zahlen**, insbesondere 163.

Weitere Infos:

- [Wikipedia – Chudnovsky-Algorithmus (DE)](https://de.wikipedia.org/wiki/Chudnovsky-Algorithmus)
- [Wikipedia – Chudnovsky algorithm (EN)](https://en.wikipedia.org/wiki/Chudnovsky_algorithm)
- [Mathematischer Beweis (arXiv)](https://arxiv.org/abs/1809.00533)

---

## 📂 Dateien


| Datei                | Beschreibung                                   |
| -------------------- | ---------------------------------------------- |
| `calc.py`            | Hauptprogramm zur Berechnung von π            |
| `pi_output.txt`      | Datei mit den berechneten π-Ziffern           |
| `pi_checkpoint.json` | Zwischenspeicher zum Fortsetzen der Berechnung |

---


Keine Garantie auf Korrektheit!
