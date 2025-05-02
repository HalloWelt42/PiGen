import os
import json
from decimal import Decimal, getcontext
import itertools
import signal
import sys

CHECKPOINT_FILE = "pi_checkpoint.json"
OUTPUT_FILE = "pi_output.txt"
BLOCK_SIZE = 100  # Ziffern pro Schreibvorgang
MAX_DIGITS = 100_000 # Berechnungsgrenze festlegen

def load_checkpoint():
    if os.path.exists(CHECKPOINT_FILE):
        with open(CHECKPOINT_FILE, "r") as f:
            data = json.load(f)
            getcontext().prec = data["precision"]
            return data["k"], Decimal(data["sum"]), data["digits_written"]

    # Kein Checkpoint vorhanden → Initialisierung
    initial_prec = max(1000, BLOCK_SIZE * 20)
    getcontext().prec = initial_prec + 2
    return 0, Decimal(0), 0

def save_checkpoint(k, pi_sum, digits_written):
    state = {
        "k": k,
        "sum": str(pi_sum),
        "precision": getcontext().prec,
        "digits_written": digits_written
    }
    with open(CHECKPOINT_FILE, "w") as f:
        json.dump(state, f)

def chudnovsky_term(k):
    from math import factorial
    num = Decimal(factorial(6 * k)) * (13591409 + 545140134 * k)
    den = Decimal(factorial(3 * k)) * (factorial(k) ** 3) * (Decimal(640320) ** (3 * k))
    term = num / den
    return term if (k % 2 == 0) else -term

def compute_pi(pi_sum):
    return (Decimal(426880) * Decimal(10005).sqrt()) / pi_sum

# Die Funktion berechnet die Zahl Pi mit der Chudnovsky-Formel.
def main():
    k, pi_sum, digits_written = load_checkpoint()

    # Wenn Output-Datei nicht existiert, schreibe "3." und beginne mit Zählung ab 0
    if not os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, "w") as f:
            f.write("3.")
        digits_written = 0
    elif digits_written == 0:
        # Kein Checkpoint, aber Datei existiert → Zählstand rekonstruieren
        with open(OUTPUT_FILE, "r") as f:
            content = f.read().strip()
            if content.startswith("3."):
                digits_written = len(content) - 2
            else:
                digits_written = len(content)

    def handler(signum, frame):
        print(f"\nAbbruch bei k={k}, geschriebenen Ziffern={digits_written}. Speichere…")
        save_checkpoint(k, pi_sum, digits_written)
        sys.exit(0)

    signal.signal(signal.SIGINT, handler)

    for k in itertools.count(start=k):
        if digits_written >= MAX_DIGITS:
            print(f"\nMaximale Anzahl von {MAX_DIGITS} Ziffern erreicht. Beende…")
            save_checkpoint(k, pi_sum, digits_written)
            break

        pi_sum += chudnovsky_term(k)

        # Präzision bei Bedarf erhöhen
        total_prec = digits_written + BLOCK_SIZE + 10
        if getcontext().prec < total_prec:
            getcontext().prec = total_prec

        # Pi berechnen und Nachkommastellen isolieren
        pi_str = str(compute_pi(pi_sum))
        if '.' not in pi_str:
            continue  # Sicherheit: falls unvollständiger String

        decimal_part = pi_str.split('.')[1]

        # Wenn genug neue Ziffern vorliegen → in Datei schreiben
        if len(decimal_part) >= digits_written + BLOCK_SIZE:
            next_block = decimal_part[digits_written: digits_written + BLOCK_SIZE]
            with open(OUTPUT_FILE, "a") as f:
                f.write(next_block)
            digits_written += len(next_block)
            save_checkpoint(k + 1, pi_sum, digits_written)
            print(f"\rAngehängt: {len(next_block)} Ziffern → insgesamt {digits_written} von {MAX_DIGITS}",end='',flush=True)


if __name__ == "__main__":
    main()
