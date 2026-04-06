"""Cleaning and normalisation functions for the Akkadian dataset.
"""

import re
import unicodedata
import pandas as pd

# cleaning functions


def clean_transliteration(text: str) -> str:
    """
    KEPT (linguistically meaningful):
      - {d} and {ki} determinatives
      - <gap> lacuna marker
      - Subscript digits ₀–₉ (part of the transliteration system)
      - Decimal fractions (ancient quantity notation, e.g. 17.8333 ma-na)
      - + sign (tablet-join marker)
      - All Assyriological diacritics (š, ṭ, ḫ, ṣ, etc.)

    FIXED:
      - Strip leading/trailing whitespace
      - Collapse multiple internal spaces to one
      - NFC Unicode normalisation (preserves diacritics)
      - Remove stray Hebrew ד (wrong-charset encoding artefact)
    """
    text = unicodedata.normalize('NFC', text)
    text = text.strip()
    text = re.sub(r'  +', ' ', text)
    text = text.replace('ד', '')
    return text

def clean_translation(text: str) -> str:
    """
    KEPT:
      - <gap> lacuna marker (marks damaged/missing tablet text)
      - Unicode fractions ½ ⅓ ⅔ ⅚ (legitimate ancient measures)
      - Straight double quotes (speech quotations are common in tablets)

    FIXED:
      - Strip leading/trailing whitespace
      - NFC Unicode normalisation
      - <of<gap> → <gap>  (malformed gap variant, 1 row)
      - "" → "            (double-quote duplication artefact, 103 rows)
      - Hebrew ד → space  (OCR/encoding artefact, appears mid-word)
      - Curly/smart quotes → straight (' ' → '  and  " " → ")
      - Collapse multiple internal spaces
    """
    text = unicodedata.normalize('NFC', text)
    text = text.strip()
    
    # fix malformed gap variant before other substitutions
    text = re.sub(r'<of<gap>', '<gap>', text)
    
    # fix double-quote duplication artefact
    text = re.sub(r'""', '"', text)
    
    # remove stray Hebrew character (appears concatenated with English word)
    text = re.sub(r'ד', ' ', text)
    
    # normalize curly/smart quotes to straight
    text = text.replace("\u2018", "'").replace("\u2019", "'")  # single quotes
    text = text.replace("\u201c", '"').replace("\u201d", '"')  # double quotes
    
    return text
    
    
# flag function 

def add_flags(df: pd.DataFrame) -> pd.DataFrame:
    """
        Flags added:
      - has_transliteration: True if 'transliteration' is non-empty after cleaning
      - has_translation: True if 'translation' is non-empty after cleaning
      - has_gap: True if either 'transliteration' or 'translation' contains the <gap> marker
      """
      
    df = df.copy()
    df["translit_len"] = df["transliteration"].str.len()
    df["transl_len"] = df["translation"].str.len()
    df["len_ratio"] = df["transl_len"] / df["translit_len"].replace(0, 1)  # to avoid division by 0
    
    df["flag_very_short_translation"] = df["transl_len"] < 20
    df["flag_very_long_translation"] = df["len_ratio"] > 3
    df["flag_low_ratio"] = df["len_ratio"] < 0.15
    df["flag_has_gap"]                = (
        df["transliteration"].str.contains("<gap>", regex=False) |
        df["translation"].str.contains("<gap>", regex=False)
    )
    
    return df


def run_cleaning(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["transliteration"] = df["transliteration"].apply(clean_transliteration)
    df["translation"]     = df["translation"].apply(clean_translation)
    
    before = len(df)
    df = df.drop_duplicates(subset=["transliteration", "translation"], keep="first")
    dropped = before - len(df)
    if dropped:
        print(f"Dropped {dropped} duplicate rows")
        
    df = add_flags(df)
    print(f"Cleaning done. {len(df)} rows remain.")
    return df
