# stáhnout dotazy
# zjistit, jestli jsou nové dotazy
# vytvořit příslušné složky an interním disku
# odeslání odpovědí ze složek ready2send, odeslané soubory přesunout do složky sent
# notifikace o provedených úkonech

import os
import datetime
from datetime import date
import shutil
import logging
import sys

if len(sys.argv) == 1:
    print("Prosim, vlozte dva argumenty.")
    exit(1)
elif sys.argv[1] == "--help":
    print("Vlozte dva argumenty - 1. cesta ke slozce na sdilenem disku, 2. cesta ke slozce na internim disku")
    exit(0)
elif len(sys.argv) == 3:
    root = sys.argv[1]
    internal = sys.argv[2]
else:
    print("Vlozte dva argumenty.")
    exit(1)

logging.basicConfig(level=logging.DEBUG)

if not os.path.exists(root):
    print("Zadana cesta na sdilenem disku neexistuje.")
    exit(1)
if not os.path.exists(internal):
    print("Zadana cesta na internim disku neexistuje.")
    exit(1)

for folder in os.listdir(root):
    section = os.path.join(root, folder)
    if folder == ".DS_Store":
        continue
    for file in os.listdir(os.path.join(section, 'Dotazy')):
        if not file.endswith('.xls'):
            continue
        product = os.path.join(section, 'Odpovedi', file)
        source_file = os.path.join(section, 'Dotazy', file)
        source_file_pdf = source_file.replace(".xls", ".pdf")
        # dokumenty, které byly zpracovány jsou ve složce Odpovedi
        if os.path.exists(product):
            logging.info("Dokument %s jiz byl zpracovan" % file)
        # dokumenty, které nejsou ve složce Odpovedi (můžou být ve složce ready2send)
        else:
            logging.info("Zacinam zpracovavat dokument %s" % file)
            # pomocné dokumenty .info
            info = source_file.replace(".xls", ".info")
            current_date = date.today()
            # pokud existuje dokument.info (tzn. už byl jednou načten), otevři ho a načti ho a zkopíruj na sdílený disk do Odpovedi
            if os.path.exists(info):
                logging.info("Dokument %s jiz byl nacten" % file)
                with open(info, "r") as f:
                    data = f.read()
                    date = datetime.datetime.strptime(data, "%Y-%m-%d").date()
                s1 = "%s_%s" % (date.month, date.year)
                s2 = "%s_%s" % (date.day, date.month)
                path = os.path.join(internal, folder, "Odpovedi", s1, s2)
                path_ready2send = os.path.join(path, "ready2send", file)
                path_sent = os.path.join(path, "sent", file)
                # jestli dokument existuje ve složce ready2sent, tak ho zkopíruj na sdílený disk do Odpovedi a zkopíruj ho do složky odeslané
                if os.path.exists(path_ready2send):
                    shutil.copy(path_ready2send, product)
                    shutil.move(path_ready2send, path_sent)
                    logging.info("Dokument %s byl zkopirovan na sdileny disk do slozky Odpovedi a presunut do slozky sent" % file)
                    # uklizení již použitých dokumentů .info
                    os.remove(info)
                else:
                    pass

            # když dokument.info neexistuje, zapiš do něj aktuální datum
            else:
                with open(info, "w") as f:
                    f.write(current_date.isoformat())
                    logging.info("Byl vytvoren dokument %s " % info)
                s1 = "%s_%s" % (current_date.month, current_date.year)
                s2 = "%s_%s" % (current_date.day, current_date.month)
                path_prefix = os.path.join(internal, folder, "Dotazy", s1, s2)
                path_prefix_pdf = os.path.join(path_prefix, "PDF")
                path = os.path.join(internal, folder, "Odpovedi", s1, s2)
                path_prefix_ready2send = os.path.join(path, "ready2send")
                path_prefix_sent = os.path.join(path, "sent")
                # vytvoř mezi level složek a zkopíruj je z Dotazu (sdílený disk) do Dotazů (interní disk)
                os.makedirs(path_prefix_pdf)
                os.makedirs(path_prefix_ready2send)
                os.makedirs(path_prefix_sent)
                shutil.copy(source_file, path_prefix)
                if os.path.exists(source_file_pdf):
                    shutil.copy(source_file_pdf, path_prefix_pdf)
                else:
                    logging.info("Dokument %s neexistuje ve verzi PDF " % file)
                logging.info("Dokument %s byl zkopirovan na interni disk do slozky Dotazy" % file)
