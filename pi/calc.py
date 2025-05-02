import os
import json
import decimal
from decimal import Decimal, getcontext
import itertools
import signal
import sys

CHECKPOINT_FILE = "pi_checkpoint.json"
OUTPUT_FILE = "pi_output.txt"
BLOCK_SIZE = 100  # Ziffern pro Schreibvorgang

def load_checkpoint():
    if os.path.exists(CHECKPOINT_FILE):
        with open(CHECKPOINT_FILE, "r") as f:
            data = json.load(f)
            # Kontext wiederherstellen
            getcontext().prec = data["precision"]
            return data["k"], Decimal(data["sum"]), data["digits_written"]
    # Erster Lauf: k=0, Summe=0, keine Ziffern geschrieben
    initial_prec = BLOCK_SIZE * 10  # ausreichend Reserve
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
    num = Decimal(factorial(6*k)) * (13591409 + 545140134*k)
    den = Decimal(factorial(3*k)) * (factorial(k)**3) * (Decimal(640320) ** (3*k))
    term = num / den
    return term if (k % 2 == 0) else -term

def compute_pi(pi_sum):
    return (Decimal(426880) * Decimal(10005).sqrt()) / pi_sum

def append_pi_digits(pi_str, digits_written):
    """Hängt die nächsten BLOCK_SIZE Ziffern ab digits_written an OUTPUT_FILE an."""
    next_block = pi_str[digits_written : digits_written + BLOCK_SIZE]
    with open(OUTPUT_FILE, "a") as f:
        f.write(next_block)
    return len(next_block)

def main():
    k, pi_sum, digits_written = load_checkpoint()

    # Erst bei neuem Lauf: wenn OUTPUT_FILE nicht existiert, schreibe "3."
    if not os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, "w") as f:
            f.write("3.")
        digits_written = 0  # Nach dem Dezimalpunkt angefangen zu zählen

    def handler(signum, frame):
        print(f"\nAbbruch bei k={k}, geschriebenen Ziffern={digits_written}. Speichere…")
        save_checkpoint(k, pi_sum, digits_written)
        sys.exit(0)

    signal.signal(signal.SIGINT, handler)

    for k in itertools.count(start=k):
        pi_sum += chudnovsky_term(k)
        # Wir brauchen mindestens so viele Stellen im Kontext
        total_prec = digits_written + BLOCK_SIZE + 2
        if getcontext().prec < total_prec:
            getcontext().prec = total_prec

        # Pi neu berechnen und in String umwandeln
        pi_str = str(compute_pi(pi_sum))

        # Sobald wir mindestens eine neue 100-Ziffern-Block haben:
        if len(pi_str) - 2 >= digits_written + BLOCK_SIZE:
            added = append_pi_digits(pi_str, digits_written)
            digits_written += added
            save_checkpoint(k + 1, pi_sum, digits_written)
            print(f"Angehängt: {added} Ziffern → insgesamt {digits_written}")

if __name__ == "__main__":
    main()
