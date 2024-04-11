import os
import threading
from datetime import datetime

# Pfad zum Verzeichnis, das durchsucht werden soll
pfad = "C:/"
hierarchie = input("Möchten Sie die Hierarchie anzeigen? (J/N): ")
auswahl = ''
dateiname_anfang = ''
datentyp_ende = ''
aufgelistet = []
lock = threading.Lock()


def einzug(ebene):
    """
    Erstellt Einzüge für die hierarchische Darstellung basierend auf der Verzeichnisebene.
    """
    symbole = "|   " * (ebene - 1)
    if ebene > 0:
        symbole += "|-- "
    return symbole


def bedingung(element):
    """
    Überprüft, ob das aktuelle Element den Filterkriterien entspricht.
    """
    if auswahl == 'F':
        return element.startswith(dateiname_anfang)
    elif auswahl == 'D':
        return element.endswith(f".{datentyp_ende}")
    else:
        return True


def rekursiv(verzeichnispfad, ebene=0):
    """
    Durchläuft Verzeichnisse rekursiv und filtert Dateien basierend auf der Benutzerauswahl.
    """
    try:
        elemente = os.listdir(verzeichnispfad)
    except Exception:
        return
    threads = []
    for element in elemente:
        voller_pfad = os.path.join(verzeichnispfad, element)
        try:
            if os.path.isdir(voller_pfad):
                t = threading.Thread(target=rekursiv, args=(voller_pfad, ebene + 1))
                threads.append(t)
                t.start()
            elif bedingung(element):
                if hierarchie == "N":
                    with lock:
                        aufgelistet.append(
                            f"{element.ljust(25)} ; {voller_pfad.ljust(20)} {os.path.getsize(voller_pfad) / 1000} KB")
                elif hierarchie == "J":
                    ausgabe = f"{einzug(ebene)}{element} ; {os.path.getsize(voller_pfad) / 1000} KB"
                    with lock:
                        aufgelistet.append(ausgabe)
        except Exception:
            continue

    for t in threads:
        try:
            t.join()
        except Exception:
            continue


if hierarchie == "N":
    auswahl = input("Filtern nach Dateiname (F), Datentyp (D) oder nichts (N): ").upper()
    if auswahl == 'F':
        dateiname_anfang = input("Dateiname: ")
    elif auswahl == 'D':
        datentyp_ende = input("Datentyp: ")

startTime = datetime.now()
rekursiv(pfad)

if hierarchie == "N":
    gefiltert = input("Sortieren? (J/N): ")
    if gefiltert == "J":
        aufgelistet.sort()

if hierarchie == "J":
    print(pfad)

with open("Ergebnisse.txt", 'w') as datei:
    for zeile in aufgelistet:
        try:
            datei.write(zeile + "\n")
            print(zeile)
        except Exception:
            continue
print(datetime.now() - startTime)