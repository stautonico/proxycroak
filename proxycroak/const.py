DATABASE_VENDORS = ["sqlite"]


# In theory, we should only need newer sets (SVI+) since all the rest have ptcgo codes
SET_IDS = {
    "SVI": "sv1",
    "PAL": "sv2",
    "OBF": "sv3",
    "MEW": "sv3pt5",
    "PAR": "sv4",

    # Exceptions for GG and TGs
    "BRS-TG": "swsh9tg",
    "ASR-TG": "swsh10tg",
    "LOR-TG": "swsh11tg",
    "SIT-TG": "swsh12tg",
    "CRZ-GG": "swsh12pt5gg",

    # Exceptions for Shiny Vaults
    "HIF-SV": "sma",
    "SHF-SV": "swsh45sv",
}