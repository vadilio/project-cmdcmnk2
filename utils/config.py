import re
import pickle
from collections import UserDict
from datetime import datetime, timedelta
import difflib  # Для додаткового функціоналу вгадування команд
import os  # Для роботи з файловою системою

# Параметри:
# --- Збереження та Завантаження Даних ---
DATA_DIR = "personal_assistant_data"  # Назва папки для даних
CONTACTS_FILE = os.path.join(DATA_DIR, "contacts.pkl")
NOTES_FILE = os.path.join(DATA_DIR, "notes.pkl")
CONTACTS_CSV_FILE = os.path.join(DATA_DIR, "contacts.csv")