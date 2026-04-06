import os
import argparse
import pandas as pd
from sklearn.model_selection import train_test_split

from preprocess import run_cleaning

# DEFAULTS
RAW_PATH = "data/raw/train.csv"
OUT_DIR  = "data/cleaned"
VAL_RATIO = 0.10 # fraction of the data set reserved for validation
SEED      = 42

def build_splits(raw_path: str, out_dir: str, val_ratio: float, seed: int):
    os.makedirs(out_dir, exist_ok=True)

    # load
    df = pd.read_csv(raw_path)

    # clean
    df = run_cleaning(df)

    # split – stratified on flag_has_gap so partial-tablet rows are balanced across both splits
    df_train, df_val = train_test_split(
        df,
        test_size=val_ratio,
        random_state=seed,
        stratify=df["flag_has_gap"],
    )

    # leakage check
    leak = set(df_train["transliteration"])
    
    # saving
    df.to_csv(       os.path.join(out_dir, "full_cleaned.csv"), index=False)
    df_train.to_csv( os.path.join(out_dir, "cleaned_train.csv"),        index=False)
    df_val.to_csv(   os.path.join(out_dir, "cleaned_val.csv"),          index=False)

    
    print(f"Saved to {out_dir}/")
    print(f"full_cleaned.csv ({len(df)} rows)")
    print(f"train.csv ({len(df_train)} rows, {len(df_train)/len(df)*100:.1f}%)")
    print(f"val.csv ({len(df_val)} rows,  {len(df_val)/len(df)*100:.1f}%)")
    print(f"Gap% – train: {df_train['flag_has_gap'].mean()*100:.1f}%  "
          f"val: {df_val['flag_has_gap'].mean()*100:.1f}%")
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build train/val splits for the cuneiform dataset.")
    parser.add_argument("--raw",       default=RAW_PATH,  help="Path to raw train.csv")
    parser.add_argument("--out",       default=OUT_DIR,   help="Output directory")
    parser.add_argument("--val_ratio", default=VAL_RATIO, type=float, help="Fraction for validation (default 0.10)")
    parser.add_argument("--seed",      default=SEED,      type=int,   help="Random seed (default 42)")
    args = parser.parse_args()

    build_splits(args.raw, args.out, args.val_ratio, args.seed)