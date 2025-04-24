# -*- coding: utf-8 -*-

# -----------------------------------------------------------------------------
# Installer Patch ITA Yakuza 5 Remastered
# Autore: SavT
# Versione: v0.0.2
# -----------------------------------------------------------------------------

# --- Import Moduli Standard ---
import sys
import os
import platform
import webbrowser
import traceback
import shutil
import datetime

# --- Import Moduli Terze Parti ---
import pyzipper

# --- Import Moduli PyQt6 ---
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QFrame,
    QStackedWidget, QFileDialog, QTextEdit, QLineEdit, QMessageBox,
    QProgressBar, QHBoxLayout, QDialog, QDialogButtonBox, QInputDialog,
    QStyle,
    QCheckBox
)
from PyQt6.QtGui import (
    QPixmap, QFont, QIcon, QCursor, QPalette, QColor, QFontDatabase,
    QPainter
)
from PyQt6.QtCore import (
    Qt, QThread, pyqtSignal, QSize, QPoint, QTimer
)


# --- Funzione Resource Path ---
def resource_path(relative_path):
    """
    Ottiene il percorso assoluto alla risorsa, necessario per trovare i file
    sia in modalità sviluppo che quando l'applicazione è impacchettata
    con PyInstaller.
    """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# --- Costanti Globali ---
CHIAVE = "chiave.txt"
DEFAULT_FOLDER_NAME = "Yakuza 5/main"
LOG_FILE = "install_log.txt"
PACKAGE_FILE = "patch.pkg"
IMG_FILE = resource_path("assets/img.png")
LOGO_ICO = resource_path("assets/Logo.ico")
HEAD_ICON_PATH = resource_path("assets/head_icon.png")
YT_ICON = resource_path("assets/youtube.png")
GH_ICON = resource_path("assets/github.png")
WEB_ICON = resource_path("assets/web.png")
VERSIONE = "v0.0.2"
CREDITI = "Patch By SavT"
LICENZA = """1) La presente patch va utilizzata esclusivamente sul  gioco originale legittimamente detenuto per il quale è stata creata.
2) Questa patch è stata creata senza fini di lucro.
3) È assolutamente vietato vendere o cedere a terzi a qualsiasi titolo il gioco già patchato;
i trasgressori potranno essere puniti, ai sensi dell'art. 171bis, legge sul diritto d'autore, con la reclusione da 6 mesi a 3 anni.
4) Si declina la responsabilità derivante dall'uso scorretto di questo programma da parte di terzi.
5) Questa patch non contiene porzioni di codice del programma del gioco;
gli elementi che la formano non sono dotati di autonomia funzionale.
6) Per la creazione di tale patch non è stato necessario violare sistemi di protezione informatica,
   né dalla sua applicazione viene messa in atto tale condotta.
7) La patch è un prodotto amatoriale, pertanto l'autore declina la responsabilità di possibili malfunzionamenti;
l'utilizzo della stessa è da intendersi a vostro rischio e pericolo.
8) Si ricorda infine che i diritti sul gioco (software) appartengono ai rispettivi proprietari.
This patch does not contain copyrighted material, has no functional autonomy, and you must have your original own copy to apply it.
All game rights, intellectual property, logo/names and movies/images are property of Sega Corporation.
"""
YT_URL = "https://www.youtube.com/@SavT999"
GH_URL = "https://github.com/zSavT/Yakuza5-Patch-ITA"
WEB_URL = "https://savtchannel.altervista.org/"
DONAZIONI = "https://www.paypal.com/paypalme/verio12"

# --- Stylesheet (Tema stile Yakuza Stats Menu) ---
YAKUZA_STYLESHEET = """
/* Stile Globale */
QWidget {
    background-color: #101218; /* Sfondo quasi nero/bluastro */
    color: #e8e8e8; /* Testo chiaro */
    font-family: "Segoe UI", Arial, Helvetica, sans-serif; /* Font pulito */
    font-size: 10pt;
}
/* Stile per le finestre principali e dialoghi custom */
QWidget#InstallerWizard, QDialog#CustomConfirmDialog, QDialog#CompletionDialog {
    /* Nessuno stile specifico qui, eredita da QWidget */
}

/* Etichette Generiche */
QLabel { background-color: transparent; padding: 1px; }

/* Etichette Specifiche per Ruolo */
QLabel#TitleLabel       { font-size: 18pt; font-weight: bold; color: #ffffff; margin-bottom: 15px; }
QLabel#SubtitleLabel    { font-size: 11pt; color: #bbccd0; margin-bottom: 8px; } /* Grigio-ciano chiaro */
QLabel#StatusLabel      { color: #c0c8d0; font-size: 10pt; padding: 5px; min-height: 3.5em; alignment: 'AlignCenter'; }
QLabel#VersionLabel, QLabel#AuthorLabel { color: #505868; font-size: 9pt; } /* Grigio/Blu scuro */
QLabel#HeadIcon         { background-color: transparent; }
QLabel#KeyInputLabel    { font-size: 9pt; color: #bbccd0; padding-right: 5px; } /* Label per input chiave */

/* Etichette Dialoghi Custom */
QLabel#DialogMainText   { font-size: 11pt; color: #ffffff; }
QLabel#DialogInfoText   { color: #bbccd0; font-size: 9pt; padding-top: 5px; }
QLabel#DialogWarningText{ color: #ff8030; font-weight: bold; font-size: 9pt; padding-top: 8px; } /* Arancio per warning */

/* Pulsanti Generici */
QPushButton {
    background-color: #181a22; color: #e0e0e0; border: 1px solid #383c48;
    padding: 9px 20px; border-radius: 0px; /* Angoli retti */
    font-weight: bold; min-width: 90px; outline: none;
}
QPushButton:hover { background-color: #20242f; border: 1px solid #00e0ff; color: #ffffff; } /* Bordo Ciano hover */
QPushButton:pressed { background-color: #101218; border: 1px solid #00a0cc; }
QPushButton:disabled { background-color: #15181e; color: #404850; border-color: #282c38; }

/* Pulsanti Primari (Azione Principale: Next, Install, Accept, OK) */
QPushButton#NextButton, QPushButton#InstallButton, QPushButton#AcceptButton {
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #e04020, stop:0.7 #ff8030, stop:1 #ff9a40); /* Gradiente Rosso-Arancio */
    color: #ffffff; border: 1px solid #b03018; font-weight: bold; }
QPushButton#NextButton:hover, QPushButton#InstallButton:hover, QPushButton#AcceptButton:hover {
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #f05030, stop:0.7 #ff9040, stop:1 #ffae50); /* Gradiente più chiaro */
    border: 1px solid #d04020; color: #ffffff; }
QPushButton#NextButton:pressed, QPushButton#InstallButton:pressed, QPushButton#AcceptButton:pressed {
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #c03010, stop:0.7 #e07020, stop:1 #e08a30); /* Gradiente più scuro */
    border: 1px solid #a02810; }
QPushButton#NextButton:disabled, QPushButton#InstallButton:disabled, QPushButton#AcceptButton:disabled {
    background-color: #502818; color: #805040; border-color: #402010; }

/* Pulsanti Secondari (Annulla, Riprova, Esci, No) */
QPushButton#CancelButton, QPushButton#RetryButton {
     background-color: #181a22; border: 1px solid #00a0cc; color: #00e0ff; /* Sfondo scuro, accento Ciano */
}
QPushButton#CancelButton:hover, QPushButton#RetryButton:hover {
     background-color: #20242f; border: 1px solid #33ffff; color: #66ffff; /* Ciano più brillante */
}
QPushButton#CancelButton:pressed, QPushButton#RetryButton:pressed {
     background-color: #101218; border: 1px solid #0080aa; color: #00c0dd;
}

/* Pulsanti Link (Icone Social/Web) */
QPushButton#LinkButton { background-color: transparent; border: none; padding: 1px; border-radius: 2px; min-width: 30px; }
QPushButton#LinkButton:hover { background-color: rgba(0, 224, 255, 0.15); } /* Hover Ciano trasparente */
QPushButton#LinkButton:pressed { background-color: rgba(0, 224, 255, 0.3); }

/* Pulsante Nascosto per Chiave AES */
QPushButton#HiddenKeyButton { background-color: transparent; border: none; padding: 0px; margin: 0px; min-width: 10px; max-width: 10px; min-height: 10px; max-height: 10px; border-radius: 0px; }
/* QPushButton#HiddenKeyButton:hover { background-color: rgba(255, 255, 0, 0.3); } */ /* Debug hover */

/* Campi di Input e Aree di Testo */
QLineEdit, QTextEdit {
    background-color: #15181e; border: 1px solid #383c48; color: #e8e8e8;
    border-radius: 0px; padding: 8px; font-size: 10pt;
    selection-background-color: #00a0cc; selection-color: #ffffff; /* Selezione Ciano */
}
QLineEdit:focus, QTextEdit:focus { border: 1px solid #00e0ff; background-color: #1c1f28; } /* Focus Ciano */
QLineEdit::placeholder { color: #505868; } /* Colore testo placeholder */
QLineEdit#KeyInputField { font-size: 9pt; padding: 6px; } /* Stile specifico per campo chiave */

/* Barra di Progresso */
QProgressBar { border: none; border-radius: 0px; background-color: #080a0f; text-align: center; height: 8px; } /* Sottile, senza bordo */
QProgressBar::chunk { background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #e04020, stop:1 #ff8030); border-radius: 0px; margin: 0px; } /* Gradiente Rosso-Arancio */

/* Pulsante Sfoglia Cartella */
QPushButton#BrowseButton {
    padding: 5px; min-width: 34px; max-width: 34px; min-height: 34px; max-height: 34px;
    background-color: #181a22; border: 1px solid #383c48; border-radius: 0px;
    color: #00e0ff; /* Colore per icona standard o testo fallback */
}
QPushButton#BrowseButton:hover { background-color: #20242f; border: 1px solid #00e0ff; }
QPushButton#BrowseButton:pressed { background-color: #101218; }

/* Finestre di Dialogo Standard (QMessageBox, QInputDialog) */
QMessageBox, QInputDialog { background-color: #181a22; border: 1px solid #383c48; } /* Stile base scuro */
QMessageBox QLabel, QInputDialog QLabel { color: #e8e8e8; background-color: transparent; font-size: 10pt; min-width: 250px; }
/* Nota: I pulsanti interni usano lo stile generico QPushButton definito sopra */

/* MODIFICA: Stile per Checkbox */
QCheckBox { spacing: 5px; /* Spazio tra box e testo */ }
QCheckBox::indicator { width: 16px; height: 16px; border: 1px solid #383c48; border-radius: 0px; background-color: #15181e; }
QCheckBox::indicator:hover { border: 1px solid #00e0ff; }
QCheckBox::indicator:checked {
    background-color: #e04020; /* Colore check arancio/rosso */
    border: 1px solid #00e0ff; /* MODIFICA: Bordo CIANO acceso quando selezionato */
    image: url(assets/v.png);           /* MODIFICA: Assicura che il segno di spunta di default sia nascosto */
}
QCheckBox::indicator:checked:hover { background-color: #f05030; border: 1px solid #d04020; }
QCheckBox::indicator:disabled { background-color: #15181e; border: 1px solid #282c38; }

/* Barre di Scorrimento */
QScrollBar:vertical   { border: none; background: #101218; width: 8px; margin: 0px; }
QScrollBar::handle:vertical { background: #383c48; min-height: 25px; border-radius: 0px; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; background: none; }
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: none; }
QScrollBar:horizontal { border: none; background: #101218; height: 8px; margin: 0px; }
QScrollBar::handle:horizontal { background: #383c48; min-width: 25px; border-radius: 0px; }
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width: 0px; background: none; }
QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal { background: none; }
"""

def leggi_chiave(nome_file):
    """
    Legge una chiave di decriptazione da un file.
    Args:
        nome_file (str): Il nome del file da cui leggere la chiave.
    Returns:
        str: La chiave di decriptazione letta dal file, o None se si verificano errori.
    """
    try:
        # Verifica se il file esiste
        if not os.path.exists(nome_file):
            print(f"Errore: Il file '{nome_file}' non esiste.")
            return None

        # Verifica se il file è leggibile
        if not os.access(nome_file, os.R_OK):
            print(f"Errore: Il file '{nome_file}' non ha i permessi di lettura.")
            return None

        with open(nome_file, 'r') as file:
            chiave = file.readline().strip()  # Legge la prima riga e rimuove spazi bianchi

        # Verifica se la chiave è vuota
        if not chiave:
            print(f"Avviso: Il file '{nome_file}' è vuoto o non contiene una chiave valida.")
            return None

        print(f"Chiave di decriptazione letta con successo dal file '{nome_file}'.")
        return chiave.encode('utf-8')

    except Exception as e:
        print(f"Si è verificato un errore durante la lettura del file '{nome_file}': {e}")
        return None



# --- Classe Worker Installazione ---
class InstallWorker(QThread):
    """
    Thread separato per eseguire l'estrazione dell'archivio patch.pkg
    e opzionalmente il backup dei file originali.

    Segnali:
        progress(int): Emette la percentuale di progresso (0-100).
        finished(bool, str): Emette al termine. True/False per successo/fallimento,
                             e una stringa con il messaggio di stato.
        backup_status(str): Emette messaggi sullo stato del processo di backup.
    """
    progress = pyqtSignal(int)
    finished = pyqtSignal(bool, str)
    backup_status = pyqtSignal(str)

    def __init__(self, dest_path, aes_key, do_backup):
        """
        Inizializza il worker.
        Args:
            dest_path (str): Percorso della cartella di destinazione.
            aes_key (bytes): Chiave AES per decriptare l'archivio.
            do_backup (bool): Se True, esegue il backup prima dell'estrazione.
        """
        super().__init__()
        self.dest_path = dest_path
        self.aes_key = aes_key
        self.do_backup = do_backup
        self._is_interruption_requested = False

    def requestInterruption(self):
        """Richiede l'interruzione del processo di estrazione."""
        self._is_interruption_requested = True

    def isInterruptionRequested(self):
        """Controlla se è stata richiesta l'interruzione."""
        return self._is_interruption_requested

    def run(self):
        """Esegue il processo di backup (se richiesto) e estrazione nel thread."""
        try:
            package_path = resource_path(PACKAGE_FILE)
            if not os.path.exists(package_path):
                raise FileNotFoundError(f"File della patch non trovato: {PACKAGE_FILE}")

            with pyzipper.AESZipFile(package_path) as zf:
                zf.setpassword(self.aes_key)
                file_infos = zf.infolist()
                total_files = len(file_infos)

                # --- Logica di Backup ---
                if self.do_backup:
                    self.backup_status.emit("Avvio backup file originali...")
                    backup_folder_name = f"_backup_patch_ita_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
                    backup_base_path = os.path.join(self.dest_path, backup_folder_name)
                    backup_count = 0
                    try:
                        os.makedirs(backup_base_path, exist_ok=True)
                        print(f"Creata cartella backup: {backup_base_path}")

                        for file_info in file_infos:
                            if self.isInterruptionRequested():
                                self.finished.emit(False, "Backup annullato dall'utente.")
                                return

                            if not file_info.is_dir():
                                source_file_path = os.path.join(self.dest_path, file_info.filename)
                                if os.path.isfile(source_file_path):
                                    backup_file_path = os.path.join(backup_base_path, file_info.filename)
                                    backup_file_dir = os.path.dirname(backup_file_path)
                                    os.makedirs(backup_file_dir, exist_ok=True)
                                    print(f"Backing up: {source_file_path} -> {backup_file_path}")
                                    shutil.copy2(source_file_path, backup_file_path)
                                    backup_count += 1

                        if backup_count > 0:
                            self.backup_status.emit(f"Backup di {backup_count} file completato in '{backup_folder_name}'.")
                            print(f"Backup completato: {backup_count} file.")
                        else:
                            self.backup_status.emit("Nessun file originale trovato da backuppare.")
                            print("Nessun file da backuppare.")

                    except (shutil.Error, OSError, IOError) as backup_error:
                        error_msg = f"Errore durante il backup:\n{backup_error}"
                        print(f"Errore backup: {error_msg}")
                        with open(LOG_FILE, 'a', encoding='utf-8') as f: f.write(error_msg + "\n")
                        self.finished.emit(False, error_msg + "\nL'installazione è stata interrotta.")
                        return
                # --- Fine Logica di Backup ---


                # --- Logica di Estrazione ---
                if total_files == 0:
                    self.finished.emit(True, "Installazione completata (archivio vuoto).")
                    return

                for i, file_info in enumerate(file_infos):
                    if self.isInterruptionRequested():
                        self.finished.emit(False, "Installazione annullata dall'utente.")
                        return

                    file = file_info.filename
                    target_path = os.path.join(self.dest_path, file)

                    if file_info.is_dir():
                        os.makedirs(target_path, exist_ok=True)
                        self.progress.emit(int(((i + 1) / total_files) * 100))
                        continue

                    os.makedirs(os.path.dirname(target_path), exist_ok=True)

                    try:
                        with zf.open(file_info) as source, open(target_path, "wb") as target:
                            chunk_size = 1024 * 512
                            while True:
                                if self.isInterruptionRequested():
                                    try:
                                        target.close()
                                        os.remove(target_path)
                                    except OSError: pass
                                    self.finished.emit(False, "Installazione annullata dall'utente.")
                                    return
                                chunk = source.read(chunk_size)
                                if not chunk: break
                                target.write(chunk)
                    except Exception as write_error:
                         raise IOError(f"Errore scrittura file {target_path}: {write_error}") from write_error

                    self.progress.emit(int(((i + 1) / total_files) * 100))

            if not self.isInterruptionRequested():
                self.finished.emit(True, "Installazione completata con successo!")

        # --- Gestione Errori Specifici ---
        except FileNotFoundError as e:
             with open(LOG_FILE, 'a', encoding='utf-8') as f: f.write(f"Errore FileNotFoundError: {str(e)}\n")
             self.finished.emit(False, str(e))
        except (pyzipper.BadZipFile, RuntimeError) as e:
            error_msg = f"Errore: {PACKAGE_FILE} è corrotto, la chiave AES usata non è valida o file zip non valido."
            with open(LOG_FILE, 'a', encoding='utf-8') as f: f.write(f"{error_msg} Dettaglio: {type(e).__name__}: {str(e)}\n")
            self.finished.emit(False, error_msg)
        except IOError as e:
            error_msg = f"Errore di I/O durante l'estrazione:\n{str(e)}"
            with open(LOG_FILE, 'a', encoding='utf-8') as f: f.write(error_msg + "\n")
            self.finished.emit(False, error_msg + "\nVerifica permessi e spazio disco.")
        except Exception as e:
            error_msg = f"Errore imprevisto durante l'estrazione:\n{type(e).__name__}: {str(e)}"
            with open(LOG_FILE, 'a', encoding='utf-8') as f:
                f.write(error_msg + "\n")
                traceback.print_exc(file=f)
            self.finished.emit(False, error_msg)


# --- Classe Dialogo Conferma Personalizzato ---
class CustomConfirmDialog(QDialog):
    """
    Dialogo di conferma personalizzato (es. per conferma installazione)
    con layout e stile controllati.
    """
    def __init__(self, parent=None, title="Conferma", text="", informative_text="", warning_text="", icon_pixmap=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.setObjectName("CustomConfirmDialog")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 15)
        main_layout.setSpacing(15)

        content_layout = QHBoxLayout()
        content_layout.setSpacing(20)

        if icon_pixmap:
            icon_label = QLabel()
            icon_label.setPixmap(icon_pixmap.scaled(48, 48, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
            icon_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
            content_layout.addWidget(icon_label, 0)

        text_layout = QVBoxLayout()
        text_layout.setSpacing(8)
        self.main_text_label = QLabel(text)
        self.main_text_label.setObjectName("DialogMainText")
        self.main_text_label.setWordWrap(True)
        text_layout.addWidget(self.main_text_label)

        if informative_text:
            self.info_text_label = QLabel(informative_text)
            self.info_text_label.setObjectName("DialogInfoText")
            self.info_text_label.setWordWrap(True)
            text_layout.addWidget(self.info_text_label)

        self.warning_label_container = QWidget()
        self.warning_layout = QVBoxLayout(self.warning_label_container)
        self.warning_layout.setContentsMargins(0,0,0,0)
        text_layout.addWidget(self.warning_label_container)

        content_layout.addLayout(text_layout, 1)
        main_layout.addLayout(content_layout)

        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Yes | QDialogButtonBox.StandardButton.No)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        yes_button = button_box.button(QDialogButtonBox.StandardButton.Yes)
        if yes_button:
            yes_button.setText("Sì")
            yes_button.setObjectName("AcceptButton")
            yes_button.setDefault(True)

        no_button = button_box.button(QDialogButtonBox.StandardButton.No)
        if no_button:
            no_button.setText("No")
            no_button.setObjectName("CancelButton")

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(button_box)
        btn_layout.addStretch()
        main_layout.addLayout(btn_layout)

        self.setMinimumWidth(450)
        self.adjustSize()

        if warning_text:
            self.setWarningText(warning_text)

    def setWarningText(self, text):
        """Aggiunge o rimuove dinamicamente il testo di warning."""
        for i in reversed(range(self.warning_layout.count())):
            widget = self.warning_layout.itemAt(i).widget()
            if widget is not None: widget.deleteLater()
        if text:
            warning_text_label = QLabel(text)
            warning_text_label.setObjectName("DialogWarningText")
            warning_text_label.setWordWrap(True)
            self.warning_layout.addWidget(warning_text_label)
            self.warning_label_container.setVisible(True)
        else:
            self.warning_label_container.setVisible(False)
        self.adjustSize()


# --- Classe Dialogo Completamento Personalizzato ---
class CompletionDialog(QDialog):
    """
    Dialogo mostrato al completamento con successo dell'installazione.
    Mostra un messaggio, un'icona e un pulsante OK che apre un URL.
    """
    def __init__(self, parent=None, title="Completato", text="", url_to_open=None):
        super().__init__(parent)
        self.url_to_open = url_to_open
        self.setWindowTitle(title)
        self.setModal(True)
        self.setObjectName("CompletionDialog")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 15)
        main_layout.setSpacing(15)

        content_layout = QHBoxLayout()
        content_layout.setSpacing(15)

        icon_label = QLabel()
        try:
            icon = self.style().standardIcon(QStyle.StandardPixmap.SP_MessageBoxInformation)
            icon_label.setPixmap(icon.pixmap(QSize(32, 32)))
        except Exception: pass
        icon_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        content_layout.addWidget(icon_label, 0)

        self.main_text_label = QLabel(text)
        self.main_text_label.setObjectName("DialogMainText")
        self.main_text_label.setWordWrap(True)
        self.main_text_label.setMinimumWidth(250)
        content_layout.addWidget(self.main_text_label, 1)

        main_layout.addLayout(content_layout)

        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        ok_button = button_box.button(QDialogButtonBox.StandardButton.Ok)
        if ok_button:
            ok_button.setText("OK")
            ok_button.setObjectName("AcceptButton")
            ok_button.setDefault(True)
            ok_button.clicked.connect(self.accept_and_open_url)
        else:
            button_box.accepted.connect(self.accept_and_open_url)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(button_box)
        btn_layout.addStretch()
        main_layout.addLayout(btn_layout)

        self.adjustSize()
        self.setMaximumWidth(450)

    def accept_and_open_url(self):
        """Slot chiamato quando si preme OK.
        Apre l'URL e chiude il dialogo."""
        url = self.url_to_open
        self.accept()
        if url:
            print(f"Opening URL: {url}")
            try:
                webbrowser.open(url)
                QTimer.singleShot(2000, QApplication.instance().quit)
            except Exception as e:
                print(f"Error opening URL {url}: {e}")
        else:
             QTimer.singleShot(2000, QApplication.instance().quit)


# --- Classi Schermate del Wizard ---

class WelcomeScreen(QWidget):
    """Schermata iniziale di benvenuto."""
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self); layout.setContentsMargins(30, 20, 30, 20); layout.setSpacing(15)
        top_bar = QHBoxLayout(); top_bar.setSpacing(10); top_bar.addStretch()
        for icon_path, url, tip in zip([YT_ICON, GH_ICON, WEB_ICON], [YT_URL, GH_URL, WEB_URL], ["YouTube", "GitHub", "Sito Web"]):
            try:
                if not os.path.exists(icon_path): continue
                btn = QPushButton(); btn.setObjectName("LinkButton"); btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor)); btn.setFlat(True); btn.setIcon(QIcon(icon_path)); btn.setIconSize(QSize(28, 28)); btn.setFixedSize(QSize(32, 32)); btn.setToolTip(tip); btn.clicked.connect(lambda _, link=url: webbrowser.open(link)); top_bar.addWidget(btn)
            except Exception as e: print(f"Err icon {icon_path}: {e}")
        layout.addLayout(top_bar); layout.addSpacing(10)
        image_label = QLabel(); image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        try:
            if os.path.exists(IMG_FILE): image_label.setPixmap(QPixmap(IMG_FILE).scaled(300, 180, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
            else: image_label.setText("Immagine non trovata")
        except Exception as e: image_label.setText(f"Err img: {e}")
        title = QLabel("Installer Patch ITA per Yakuza 5 Remastered"); title.setObjectName("TitleLabel"); title.setAlignment(Qt.AlignmentFlag.AlignCenter); title.setWordWrap(True)
        desc = QLabel("Questo programma installerà la traduzione italiana amatoriale."); desc.setObjectName("SubtitleLabel"); desc.setAlignment(Qt.AlignmentFlag.AlignCenter); desc.setWordWrap(True)
        btn_layout = QHBoxLayout(); self.cancel_btn = QPushButton("Esci"); self.cancel_btn.setObjectName("CancelButton")
        try: self.cancel_btn.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogCancelButton))
        except Exception: pass
        self.next_btn = QPushButton("Avanti"); self.next_btn.setObjectName("NextButton"); self.next_btn.setDefault(True)
        try: self.next_btn.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ArrowRight))
        except Exception: pass
        btn_layout.addWidget(self.cancel_btn); btn_layout.addStretch(); btn_layout.addWidget(self.next_btn)
        bottom_info_layout = QHBoxLayout(); version_label = QLabel(f"Versione Patch: {VERSIONE}"); version_label.setObjectName("VersionLabel"); version_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter); autore_label = QLabel(CREDITI); autore_label.setObjectName("AuthorLabel"); autore_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter); bottom_info_layout.addWidget(version_label); bottom_info_layout.addStretch(1); bottom_info_layout.addWidget(autore_label)
        layout.addWidget(image_label); layout.addWidget(title); layout.addWidget(desc); layout.addStretch(); layout.addLayout(btn_layout); layout.addSpacing(5); layout.addLayout(bottom_info_layout)

class PackageCheckScreen(QWidget):
    """Schermata per controllare l'esistenza e la validità del file patch.pkg."""
    def __init__(self, parent_wizard):
        super().__init__()
        self.parent_wizard = parent_wizard
        layout = QVBoxLayout(self); layout.setContentsMargins(30, 20, 30, 20); layout.setSpacing(15)
        title = QLabel("Controllo File Patch"); title.setObjectName("TitleLabel"); title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label = QLabel("Verifico..."); self.status_label.setObjectName("StatusLabel"); self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter); self.status_label.setWordWrap(True)
        self.key_input_widget = QWidget()
        self.key_input_layout = QVBoxLayout(self.key_input_widget)
        self.key_input_layout.setContentsMargins(0, 10, 0, 5); self.key_input_layout.setSpacing(5)
        key_input_label = QLabel("Chiave AES non valida. Inserisci una chiave alternativa:")
        key_input_label.setObjectName("KeyInputLabel"); key_input_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.key_input_field = QLineEdit(); self.key_input_field.setObjectName("KeyInputField")
        self.key_input_field.setEchoMode(QLineEdit.EchoMode.Password)
        self.key_input_field.setPlaceholderText("Inserisci chiave e premi Riprova (o lascia vuoto per default)")
        self.key_input_field.returnPressed.connect(self.check_package)
        self.key_input_layout.addWidget(key_input_label); self.key_input_layout.addWidget(self.key_input_field)
        self.key_input_widget.setVisible(False)
        self.retry_btn = QPushButton("Riprova Controllo"); self.retry_btn.setObjectName("RetryButton")
        self.retry_btn.clicked.connect(self.check_package); self.retry_btn.setVisible(False)
        try: self.retry_btn.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_BrowserReload))
        except Exception: pass
        retry_layout = QHBoxLayout(); retry_layout.addStretch(); retry_layout.addWidget(self.retry_btn); retry_layout.addStretch()
        btn_layout = QHBoxLayout(); self.cancel_btn = QPushButton("Esci"); self.cancel_btn.setObjectName("CancelButton")
        try: self.cancel_btn.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogCancelButton))
        except Exception: pass
        self.next_btn = QPushButton("Avanti"); self.next_btn.setObjectName("NextButton"); self.next_btn.setEnabled(False); self.next_btn.setDefault(True)
        try: self.next_btn.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ArrowRight))
        except Exception: pass
        btn_layout.addWidget(self.cancel_btn); btn_layout.addStretch(); btn_layout.addWidget(self.next_btn)
        layout.addWidget(title); layout.addSpacing(20); layout.addWidget(self.status_label); layout.addWidget(self.key_input_widget); layout.addSpacing(10); layout.addLayout(retry_layout); layout.addStretch(); layout.addLayout(btn_layout)

    def check_package(self):
        """Esegue il controllo del file patch.pkg usando la chiave AES corrente."""
        if self.key_input_widget.isVisible():
            new_key_text = self.key_input_field.text(); key_changed = False
            if new_key_text:
                try:
                    new_key_bytes = new_key_text.encode('utf-8')
                    if new_key_bytes != self.parent_wizard.current_aes_key:
                        self.parent_wizard.current_aes_key = new_key_bytes; print("Chiave AES aggiornata (da input)."); key_changed = True
                except Exception as e: QMessageBox.warning(self, "Errore Chiave", f"Chiave non valida: {e}"); print(f"Err key enc: {e}")
            else:
                 chiave_default = leggi_chiave(resource_path(CHIAVE))
                 if self.parent_wizard.current_aes_key != chiave_default:
                     self.parent_wizard.current_aes_key = chiave_default
                     print("Chiave AES reimpostata (da input vuoto)."); key_changed = True

        aes_key_to_use = self.parent_wizard.current_aes_key
        package_path = resource_path(PACKAGE_FILE)

        self.key_input_widget.setVisible(False)
        self.retry_btn.setVisible(False)
        self.status_label.setText("Verifico...")
        QApplication.processEvents()

        if not aes_key_to_use:
            self.status_label.setText(f"<font color='#ff8080'>❌ Errore: Chiave AES non disponibile.</font><br><font color='#bbccd0' size='-1'>Impossibile leggere {CHIAVE} e nessuna chiave inserita.</font>")
            self.next_btn.setEnabled(False); self.retry_btn.setVisible(True); self.key_input_widget.setVisible(True); self.key_input_field.setFocus()
            return

        if os.path.isfile(package_path):
            try:
                with pyzipper.AESZipFile(package_path) as zf: zf.setpassword(aes_key_to_use); test = zf.testzip()
                if test is None: # Successo
                    self.status_label.setText(f"<font color='#a8dda0'>✔️ File '{PACKAGE_FILE}' valido.</font>")
                    self.next_btn.setEnabled(True); self.retry_btn.setVisible(False); self.key_input_widget.setVisible(False)
                else: # Corruzione interna
                    self.status_label.setText(f"<font color='#ffd880'>⚠️ File '{PACKAGE_FILE}' corrotto (file: {test}).</font><br><font color='#bbccd0' size='-1'>Riscrivi la patch.</font>")
                    self.next_btn.setEnabled(False); self.retry_btn.setVisible(True); self.key_input_widget.setVisible(False)
            except (pyzipper.BadZipFile, RuntimeError) as e: # Errore chiave/corruzione zip
                 print(f"Package check bad key/zip error: {type(e).__name__}")
                 self.status_label.setText(f"<font color='#ffd880'>⚠️ Chiave AES non valida o archivio corrotto.</font><br><font color='#bbccd0' size='-1'>Inserisci chiave corretta e riprova.</font>")
                 self.next_btn.setEnabled(False); self.retry_btn.setVisible(True); self.key_input_widget.setVisible(True); self.key_input_field.setFocus()
            except Exception as e: # Altri errori
                 self.status_label.setText(f"<font color='#ff8080'>❌ Errore verifica: {type(e).__name__}</font>")
                 self.next_btn.setEnabled(False); self.retry_btn.setVisible(True); self.key_input_widget.setVisible(False); print(f"Pkg check err: {e}"); traceback.print_exc()
        else: # File non trovato
            self.status_label.setText(f"<font color='#ff8080'>❌ File '{PACKAGE_FILE}' non trovato.</font><br><font color='#bbccd0' size='-1'>Controlla cartella installer.</font>")
            self.next_btn.setEnabled(False); self.retry_btn.setVisible(False); self.key_input_widget.setVisible(False)

class LicenseScreen(QWidget):
    """Schermata per visualizzare e accettare la licenza d'uso."""
    def __init__(self):
        super().__init__(); layout = QVBoxLayout(self); layout.setContentsMargins(30, 20, 30, 20); layout.setSpacing(15)
        title = QLabel("Termini di Licenza d'Uso"); title.setObjectName("TitleLabel"); title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.license_text = QTextEdit(); self.license_text.setPlainText(LICENZA); self.license_text.setReadOnly(True); self.license_text.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth); self.license_text.setObjectName("LicenseText")
        btn_layout = QHBoxLayout(); self.cancel_btn = QPushButton("Esci"); self.cancel_btn.setObjectName("CancelButton")
        try: self.cancel_btn.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogCancelButton))
        except Exception: pass
        self.next_btn = QPushButton("Accetto e Continuo"); self.next_btn.setObjectName("AcceptButton"); self.next_btn.setDefault(True)
        try: self.next_btn.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogApplyButton))
        except Exception: pass
        btn_layout.addWidget(self.cancel_btn); btn_layout.addStretch(); btn_layout.addWidget(self.next_btn)
        layout.addWidget(title); layout.addWidget(self.license_text, 1); layout.addSpacing(10); layout.addLayout(btn_layout)

class InstallScreen(QWidget):
    """Schermata per selezionare la cartella e avviare l'installazione."""
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self); self.layout.setContentsMargins(30, 20, 30, 20); self.layout.setSpacing(15)

        # Titolo con icona
        title_layout = QHBoxLayout(); title_layout.setSpacing(10); title_icon_label = QLabel()
        try:
            icon = self.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon); title_icon_label.setPixmap(icon.pixmap(QSize(32, 32)))
        except Exception as e: print(f"Err title icon: {e}")
        title = QLabel("Selezione Cartella di Installazione"); title.setObjectName("TitleLabel"); title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_layout.addStretch(1); title_layout.addWidget(title_icon_label, 0, Qt.AlignmentFlag.AlignVCenter); title_layout.addWidget(title, 0, Qt.AlignmentFlag.AlignVCenter); title_layout.addStretch(1)

        # Etichetta percorso
        path_label = QLabel("Installa la patch nella cartella principale di Yakuza 5:"); path_label.setObjectName("SubtitleLabel")

        # Input percorso e bottone sfoglia
        self.path_input = QLineEdit(); self.path_input.setPlaceholderText("Es: C:/.../Steam/steamapps/common/Yakuza 5")
        self.browse_btn = QPushButton(); self.browse_btn.setObjectName("BrowseButton")
        try:
            icon = self.style().standardIcon(QStyle.StandardPixmap.SP_DirOpenIcon); self.browse_btn.setIcon(icon); self.browse_btn.setIconSize(QSize(18, 18))
        except Exception as e: self.browse_btn.setText("...") # Fallback testo
        self.browse_btn.setFixedSize(34, 34); self.browse_btn.setToolTip("Sfoglia cartelle"); self.browse_btn.clicked.connect(self.select_folder)
        path_layout = QHBoxLayout(); path_layout.addWidget(path_label); path_layout.addStretch()
        path_input_layout = QHBoxLayout(); path_input_layout.addWidget(self.path_input, 1); path_input_layout.addSpacing(5); path_input_layout.addWidget(self.browse_btn)

        # MODIFICA: Aggiunta Checkbox per il Backup
        self.backup_checkbox = QCheckBox("Crea backup dei file originali prima dell'installazione")
        self.backup_checkbox.setChecked(True) # Imposta come selezionato di default (opzionale)
        self.backup_checkbox.setToolTip("Se selezionato, i file che verranno sovrascritti dalla patch\nsaranno prima copiati in una sottocartella '_backup_patch_ita_...'")

        # Pulsanti Install/Cancel
        self.install_btn = QPushButton("Installa Patch"); self.install_btn.setObjectName("InstallButton"); self.install_btn.setDefault(True)
        try: self.install_btn.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogSaveButton))
        except Exception as e: print(f"Err install icon: {e}")
        self.cancel_btn = QPushButton("Annulla"); self.cancel_btn.setObjectName("CancelButton")
        try: self.cancel_btn.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogCancelButton))
        except Exception as e: print(f"Err cancel icon: {e}")

        # Barra progresso e stato
        self.progress_bar = QProgressBar(); self.progress_bar.setValue(0); self.progress_bar.setTextVisible(False)
        self.status_label = QLabel("Pronto per l'installazione."); self.status_label.setObjectName("StatusLabel"); self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Icona animata (testa) sulla barra progresso
        self.head_icon = QLabel(self); self.head_icon.setObjectName("HeadIcon")
        try:
            if os.path.exists(HEAD_ICON_PATH): self.head_icon.setPixmap(QPixmap(HEAD_ICON_PATH).scaled(22, 22, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
            else: self.head_icon.setText("»"); self.head_icon.setStyleSheet("color: #ff8030; font-size: 16pt; font-weight: bold;")
            self.head_icon.setFixedSize(24, 24); self.head_icon.setAlignment(Qt.AlignmentFlag.AlignCenter); self.head_icon.hide()
            self.head_icon.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents); self.progress_bar.valueChanged.connect(self.update_icon_position)
        except Exception as e: print(f"Err head icon: {e}")

        # Layout pulsanti inferiori
        btn_layout = QHBoxLayout(); btn_layout.addWidget(self.cancel_btn); btn_layout.addStretch(); btn_layout.addWidget(self.install_btn)

        # Assemblaggio layout schermata
        self.layout.addLayout(title_layout)
        self.layout.addLayout(path_layout)
        self.layout.addLayout(path_input_layout)
        self.layout.addSpacing(10) # Spazio prima del checkbox
        self.layout.addWidget(self.backup_checkbox) # MODIFICA: Aggiunto checkbox al layout
        self.layout.addSpacing(20) # Spazio dopo il checkbox
        self.layout.addWidget(self.progress_bar)
        self.layout.addWidget(self.status_label)
        self.layout.addStretch()
        self.layout.addLayout(btn_layout)

        self.set_default_path() # Imposta percorso iniziale

    def set_default_path(self):
        """Tenta di determinare e impostare il percorso di installazione predefinito."""
        default_path = ""; base = os.path.expanduser("~")
        try:
            if platform.system() == "Windows":
                potential_bases = [
                    os.path.join(os.environ.get("ProgramFiles(x86)", "C:/Program Files (x86)"), "Steam/steamapps/common"),
                    os.path.join(os.environ.get("ProgramFiles", "C:/Program Files"), "Steam/steamapps/common")
                ]
                # Aggiungi ricerca in altri drive comuni se possibile
                import string
                available_drives = ['%s:' % d for d in string.ascii_uppercase if os.path.exists('%s:' % d)]
                for drive in available_drives:
                    if drive.lower() != 'c:':
                         potential_bases.append(os.path.join(drive, "Program Files (x86)/Steam/steamapps/common"))
                         potential_bases.append(os.path.join(drive, "Program Files/Steam/steamapps/common"))
                         potential_bases.append(os.path.join(drive, "SteamLibrary/steamapps/common")) # Librerie Steam alternative

            elif platform.system() == "Linux":
                potential_bases = [
                    os.path.expanduser("~/.steam/steam/steamapps/common"),
                    os.path.expanduser("~/.local/share/Steam/steamapps/common"),
                    os.path.expanduser("~/.var/app/com.valvesoftware.Steam/data/Steam/steamapps/common"), # Flatpak
                    "/home/deck/.local/share/Steam/steamapps/common" # Steam Deck specifico
                ]
                # Cerca altre librerie Steam in ~/.steam/steam/steamapps/libraryfolders.vdf? (più complesso)
            else: # macOS o altri
                potential_bases = [
                    os.path.expanduser("~/Library/Application Support/Steam/steamapps/common")
                ]

            found_base = None
            target_game_folder = os.path.join(DEFAULT_FOLDER_NAME) # Solo il nome della cartella gioco

            # 1. Cerca la cartella esatta del gioco
            for base_path in potential_bases:
                if os.path.isdir(os.path.join(base_path, target_game_folder)):
                    found_base = base_path
                    break

            # 2. Se non trovata, cerca almeno la cartella 'common' genitore
            if not found_base:
                 for base_path in potential_bases:
                     if os.path.isdir(base_path):
                         found_base = base_path
                         break

            # Usa la base trovata o il default dell'utente
            base = found_base if found_base else base

            # Costruisci il path finale
            default_path = os.path.join(base, target_game_folder)

        except Exception as e:
            print(f"Error determining default path: {e}")
            # Fallback al path utente + nome gioco
            default_path = os.path.join(os.path.expanduser("~"), DEFAULT_FOLDER_NAME)

        # Normalizza e imposta
        self.path_input.setText(os.path.normpath(default_path).replace("\\", "/")) # Usa slash per consistenza


    def select_folder(self):
        """Apre un dialogo per selezionare la cartella di installazione."""
        current_path = self.path_input.text(); start_dir = current_path
        # Tenta di usare la directory genitore se il path corrente non è una dir valida
        if not os.path.isdir(current_path): start_dir = os.path.dirname(current_path)
        # Se anche il genitore non è valido, usa la home
        if not os.path.isdir(start_dir): start_dir = os.path.expanduser("~")
        # Apri il dialogo
        folder = QFileDialog.getExistingDirectory(self, "Seleziona la cartella principale di Yakuza 5 Remastered", start_dir)
        if folder: self.path_input.setText(folder.replace("\\", "/")) # Usa slash per consistenza

    def update_icon_position(self, value):
        """Aggiorna la posizione dell'icona 'testa' sulla barra di progresso."""
        try:
            # Mostra/nascondi icona ai bordi
            if value > 1 and value < 100: self.head_icon.show()
            else: self.head_icon.hide()

            if not self.progress_bar.isVisible() or self.progress_bar.width() <= 0: return

            bar_rect = self.progress_bar.geometry()
            # Mappa le coordinate della barra al genitore (InstallScreen)
            bar_top_left_in_parent = self.progress_bar.mapToParent(self.progress_bar.rect().topLeft())
            bar_x = bar_top_left_in_parent.x()
            bar_y = bar_top_left_in_parent.y()
            bar_w = bar_rect.width()
            icon_w = self.head_icon.width()
            icon_h = self.head_icon.height()

            # Calcola la posizione X dell'icona in base al valore percentuale
            padding = 0
            effective_bar_width = bar_w - (2 * padding)
            ratio = max(0, min(1, value / 100.0)) # Clamp ratio [0, 1]
            x = bar_x + padding + int(effective_bar_width * ratio) - (icon_w // 2)
            x = max(bar_x + padding, min(x, bar_x + bar_w - icon_w - padding))

            # Calcola la posizione Y per centrare verticalmente l'icona nella barra
            y = bar_y + (bar_rect.height() - icon_h) // 2

            # Muovi l'icona
            self.head_icon.move(x, y)
            self.head_icon.raise_()
        except Exception as e:
            print(f"Err icon pos: {e}")
            self.head_icon.hide()

    def resizeEvent(self, event):
        """Gestisce l'evento di ridimensionamento per riposizionare l'icona."""
        super().resizeEvent(event)
        self.update_icon_position(self.progress_bar.value())


# --- Classe Wizard Principale ---
class InstallerWizard(QWidget):
    """
    Finestra principale dell'installer che gestisce le diverse schermate (pagine)
    e la logica di navigazione e installazione.
    """
    def __init__(self):
        super().__init__()
        self.install_worker = None
        self.current_aes_key = leggi_chiave(resource_path(CHIAVE))
        self.setObjectName("InstallerWizard")

        # Impostazioni finestra principale
        try: self.setWindowIcon(QIcon(LOGO_ICO))
        except Exception as e: print(f"Error setting window icon: {e}")
        self.setWindowTitle(f"Installer Patch ITA Yakuza 5 Remastered ({VERSIONE})")
        self.setMinimumSize(640, 520)

        # Contenitore principale
        container = QWidget(self)
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addWidget(container)

        # Layout interno al container
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        self.stack = QStackedWidget()
        container_layout.addWidget(self.stack)

        # Creazione istanze schermate
        self.welcome = WelcomeScreen()
        self.check_pkg = PackageCheckScreen(self)
        self.license = LicenseScreen()
        self.install = InstallScreen()

        # Aggiunta schermate
        self.stack.addWidget(self.welcome)
        self.stack.addWidget(self.check_pkg)
        self.stack.addWidget(self.license)
        self.stack.addWidget(self.install)

        # Pulsante Nascosto
        self.hidden_key_button = QPushButton(self)
        self.hidden_key_button.setObjectName("HiddenKeyButton")
        self.hidden_key_button.setFixedSize(10, 10)
        self.hidden_key_button.setFlat(True)
        self.hidden_key_button.setToolTip("Inserisci chiave AES personalizzata")
        self.hidden_key_button.setStyleSheet("background-color:transparent;border:none;")
        self.hidden_key_button.clicked.connect(self.show_custom_key_dialog)
        self.hidden_key_button.raise_()

        # Connessioni navigazione
        self.welcome.next_btn.clicked.connect(self.go_to_check)
        self.check_pkg.next_btn.clicked.connect(lambda: self.stack.setCurrentWidget(self.license))
        self.license.next_btn.clicked.connect(lambda: self.stack.setCurrentWidget(self.install))
        self.install.install_btn.clicked.connect(self.confirm_installation)

        # Connessioni Esci/Annulla
        self.welcome.cancel_btn.clicked.connect(self.close)
        self.check_pkg.cancel_btn.clicked.connect(self.close)
        self.license.cancel_btn.clicked.connect(self.close)
        self.install.cancel_btn.clicked.connect(self.handle_cancel_install)

        self.position_hidden_button()

    def position_hidden_button(self):
        """Posiziona il bottone nascosto nell'angolo in alto a destra."""
        margin = 5
        button_size = self.hidden_key_button.size()
        x = self.width() - button_size.width() - margin
        y = margin
        self.hidden_key_button.move(x, y)

    def resizeEvent(self, event):
        """Riposiziona il bottone nascosto e aggiorna icona progresso."""
        super().resizeEvent(event)
        self.position_hidden_button()
        if self.stack.currentWidget() == self.install:
            self.install.update_icon_position(self.install.progress_bar.value())

    def show_custom_key_dialog(self):
        """Mostra dialogo per inserire chiave AES manuale."""
        current_key_str = "";
        try:
             if self.current_aes_key:
                 current_key_str = self.current_aes_key.decode('utf-8', errors='ignore')
        except Exception: pass

        text, ok = QInputDialog.getText(self, "Chiave AES Personalizzata",
                                        "Inserisci la chiave AES (stringa):",
                                        QLineEdit.EchoMode.Password, current_key_str)
        key_changed = False
        if ok and text:
            try:
                new_key_bytes = text.encode('utf-8')
                if new_key_bytes != self.current_aes_key:
                    self.current_aes_key = new_key_bytes
                    print("Chiave AES aggiornata (manuale).")
                    key_changed = True
            except Exception as e: QMessageBox.warning(self,"Errore Chiave",f"Errore codifica chiave: {e}"); print(f"Err key enc: {e}")
        elif ok and not text:
             chiave_default = leggi_chiave(resource_path(CHIAVE))
             if self.current_aes_key != chiave_default:
                 self.current_aes_key = chiave_default
                 print("Chiave AES reimpostata al default (manuale).")
                 key_changed = True

        if key_changed and self.stack.currentWidget() == self.check_pkg:
             print("Rieseguo check dopo cambio chiave manuale.")
             self.check_pkg.check_package()

    def go_to_check(self):
        """Passa alla schermata check ed esegue il controllo."""
        self.check_pkg.check_package()
        self.stack.setCurrentWidget(self.check_pkg)

    def confirm_installation(self):
        """Mostra conferma prima di installare."""
        dest_path = self.install.path_input.text()
        if not dest_path:
            QMessageBox.warning(self, "Percorso Mancante", "Specifica la cartella di installazione.")
            return

        do_backup = self.install.backup_checkbox.isChecked()
        dest_path = os.path.normpath(dest_path)
        abs_path = os.path.abspath(dest_path)
        base_dir = os.path.dirname(abs_path)

        if not os.path.isdir(base_dir):
            QMessageBox.warning(self, "Percorso Non Valido", f"La directory base '{base_dir}' non esiste o non è valida.")
            return

        common_files = ['Yakuza4.exe', 'data', '_CommonRedist']
        found = [f for f in common_files if os.path.exists(os.path.join(dest_path, f))]
        warn_msg = ""
        icon = self.style().standardIcon(QStyle.StandardPixmap.SP_MessageBoxQuestion)
        icon_pixmap = icon.pixmap(QSize(48, 48))

        if not found and os.path.isdir(dest_path):
            warn_msg = "<b>Attenzione:</b> La cartella selezionata esiste ma non sembra contenere Yakuza 5."
            warn_icon = self.style().standardIcon(QStyle.StandardPixmap.SP_MessageBoxWarning)
            icon_pixmap = warn_icon.pixmap(QSize(48, 48))
        elif not os.path.exists(dest_path):
            warn_msg = f"Nota: La cartella '{os.path.basename(dest_path)}' verrà creata."

        dialog = CustomConfirmDialog(
            parent=self, title="Conferma Installazione",
            text=f"Installare la patch in:<br><br><b>{dest_path}</b>",
            informative_text="Procedere con l'operazione?",
            warning_text=warn_msg, icon_pixmap=icon_pixmap
        )
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.perform_installation(dest_path, do_backup)

    def perform_installation(self, dest_path, do_backup):
        """Avvia l'installazione nel thread."""
        if self.install_worker and self.install_worker.isRunning(): return

        if not self.current_aes_key:
            QMessageBox.critical(self, "Errore Chiave AES", f"Impossibile procedere: chiave AES non valida o non trovata ({CHIAVE}).")
            return

        try:
            os.makedirs(dest_path, exist_ok=True)
        except OSError as e:
            QMessageBox.critical(self, "Errore Cartella", f"Impossibile creare o accedere alla cartella di destinazione:\n{dest_path}\nErrore: {e}")
            return

        # Disabilita UI
        self.install.install_btn.setEnabled(False)
        self.install.cancel_btn.setText("Annulla"); self.install.cancel_btn.setObjectName("CancelButton")
        self.install.path_input.setEnabled(False); self.install.browse_btn.setEnabled(False)
        self.install.backup_checkbox.setEnabled(False)
        self.install.status_label.setText("Avvio preparazione operazione...")
        self.install.progress_bar.setValue(0)
        self.install.head_icon.hide()

        # Avvia worker
        self.install_worker = InstallWorker(dest_path, self.current_aes_key, do_backup)
        self.install_worker.progress.connect(self.update_progress)
        self.install_worker.finished.connect(self.on_finished)
        self.install_worker.backup_status.connect(self.update_backup_status)
        self.install_worker.start()

    def update_backup_status(self, message):
        """Aggiorna status label per backup."""
        self.install.status_label.setText(message)
        QApplication.processEvents()

    def update_progress(self, value):
        """Aggiorna barra e status label per installazione."""
        self.install.progress_bar.setValue(value)
        if value > 0 and value < 100:
            self.install.status_label.setText(f"Installazione in corso... {value}%")
        self.install.update_icon_position(value)


    def on_finished(self, success, message):
        """Chiamato al termine del worker."""
        # Riabilita UI
        self.install.install_btn.setEnabled(True)
        self.install.cancel_btn.setText("Chiudi"); self.install.cancel_btn.setObjectName("CancelButton")
        self.install.cancel_btn.setEnabled(True)
        self.install.path_input.setEnabled(True); self.install.browse_btn.setEnabled(True)
        self.install.backup_checkbox.setEnabled(True)
        self.install.head_icon.hide()

        self.install_worker = None

        # Gestione Risultati
        if success:
            self.install.progress_bar.setValue(100)
            self.install.status_label.setText(message)
            completion_dialog = CompletionDialog(
                parent=self, title="Installazione Completata",
                text="Operazione completata con successo.",
                url_to_open=DONAZIONI
            )
            completion_dialog.exec()
        else: # Fallimento
            print(f"DEBUG: on_finished received error message: '{message}'")
            self.install.progress_bar.setValue(0)

            # Gestione messaggi specifici di errore
            if message == "Installazione annullata dall'utente." or message == "Backup annullato dall'utente.":
                 self.install.status_label.setText("Operazione annullata.")
            elif "chiave AES usata non è valida" in message or "archivio è corrotto" in message or "file zip non valido" in message:
                 self.install.status_label.setText("Errore: Chiave AES / Archivio.")
                 QMessageBox.warning(self, "Errore Chiave AES o Archivio",
                                    f"Si è verificato un errore durante l'estrazione:\n{message}\n\n"
                                    "La chiave AES fornita non è corretta o il file patch.pkg è corrotto.\n\n"
                                    "Puoi provare a inserire una chiave diversa usando il piccolo pulsante "
                                    "trasparente in alto a destra, quindi riprova l'installazione. "
                                    "Se il problema persiste, verifica l'integrità del file patch.pkg.")
            elif "Errore durante il backup" in message:
                 self.install.status_label.setText("Errore durante il backup.")
                 QMessageBox.critical(self, "Errore di Backup", message)
            else: # Altri errori
                self.install.status_label.setText("Errore durante l'operazione.")
                QMessageBox.critical(self, "Errore",
                                     f"Si è verificato un errore:\n{message}\n\n"
                                     f"Controlla il file '{LOG_FILE}' per maggiori dettagli tecnici.")

    def handle_cancel_install(self):
        """Gestisce click su Annulla/Chiudi."""
        if self.install_worker and self.install_worker.isRunning():
             msg_box=QMessageBox(self); msg_box.setWindowTitle("Annulla Operazione"); msg_box.setText("Interrompere l'operazione in corso?"); msg_box.setIcon(QMessageBox.Icon.Question); msg_box.setStandardButtons(QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No); msg_box.setDefaultButton(QMessageBox.StandardButton.No); yes_b=msg_box.button(QMessageBox.StandardButton.Yes); yes_b.setObjectName("CancelButton"); no_b=msg_box.button(QMessageBox.StandardButton.No); no_b.setObjectName("AcceptButton");
             if msg_box.exec()==QMessageBox.StandardButton.Yes:
                 self.install_worker.requestInterruption()
                 self.install.status_label.setText("Annullamento in corso...");
                 self.install.cancel_btn.setEnabled(False)
        else:
             self.close()

    def closeEvent(self, event):
        """Gestisce chiusura finestra."""
        if self.install_worker and self.install_worker.isRunning():
            msg_box=QMessageBox(self); msg_box.setWindowTitle("Operazione In Corso"); msg_box.setText("Operazione in corso. Interrompere e uscire?"); msg_box.setIcon(QMessageBox.Icon.Warning); msg_box.setStandardButtons(QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No); msg_box.setDefaultButton(QMessageBox.StandardButton.No); yes_b=msg_box.button(QMessageBox.StandardButton.Yes); yes_b.setObjectName("CancelButton"); no_b=msg_box.button(QMessageBox.StandardButton.No); no_b.setObjectName("AcceptButton");
            if msg_box.exec()==QMessageBox.StandardButton.Yes:
                 self.install_worker.requestInterruption()
                 event.accept()
            else:
                 event.ignore()
        else:
             event.accept()


# --- Blocco Principale di Avvio Applicazione ---
if __name__ == "__main__":
    # Abilita High DPI Scaling (metodo originale con hasattr per compatibilità)
    if hasattr(Qt.ApplicationAttribute, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
    if hasattr(Qt.ApplicationAttribute, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)

    # Crea l'applicazione Qt
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setStyleSheet(YAKUZA_STYLESHEET)

    # Crea e mostra il wizard
    wizard = InstallerWizard()
    wizard.show()

    # Avvia loop eventi
    sys.exit(app.exec())