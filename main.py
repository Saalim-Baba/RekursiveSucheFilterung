import os

# Pfad zum Verzeichnis, das durchsucht werden soll
pfad = "C:/Users/Saalim/Documents"
hierarchie = input("Möchten Sie die Hierarchie anzeigen? (J/N): ")
auswahl = ''
dateiname_anfang = ''
datentyp_ende = ''
aufgelistet = []


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
    filter_bedigung = True
    if auswahl == 'F':
        return element.startswith(dateiname_anfang)
    elif auswahl == 'D':
        return element.endswith(f".{datentyp_ende}")
    else:
        return filter_bedigung


def rekursiv(verzeichnispfad, ebene=0):
    """
    Durchläuft Verzeichnisse rekursiv und filtert Dateien basierend auf der Benutzerauswahl.
    """
    elemente = os.listdir(verzeichnispfad)
    for element in elemente:
        voller_pfad = os.path.join(verzeichnispfad, element)
        try:
            if hierarchie == "N" and bedingung(element):
                aufgelistet.append(
                    f"{element.ljust(25)} ; {voller_pfad.ljust(20)} {os.path.getsize(voller_pfad) / 1000} KB")
            elif hierarchie == "J":
                ausgabe = f"{einzug(ebene)}{element} ; {os.path.getsize(voller_pfad) / 1000} KB"
                if os.path.isdir(voller_pfad):
                    ausgabe = f"{ausgabe} DIR"
                aufgelistet.append(ausgabe)
            if os.path.isdir(voller_pfad):
                rekursiv(voller_pfad, ebene + 1)
        except Exception:
            continue


if hierarchie == "N":
    auswahl = input("Filtern nach Dateiname (F), Datentyp (D) oder nichts (N): ").upper()
    if auswahl == 'F':
        dateiname_anfang = input("Dateiname: ")
    elif auswahl == 'D':
        datentyp_ende = input("Datentyp: ")

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
