from pathlib import Path
import pandas as pd

def main():
    raw_dir = Path.cwd() / "data" / "raw"
    assert raw_dir.exists(), f"Raw data folder not found: {raw_dir}"

    csv_files = list(raw_dir.glob("*.csv"))
    assert csv_files, f"No CSV files found in {raw_dir} (run fetch step first)"

    expected_cols = {"ticker", "date", "open", "high", "low", "close", "volume"}

    for p in csv_files:
        print("Checking:", p.name)
        df = pd.read_csv(p)
        cols = {c.strip().lower() for c in df.columns}
        missing = expected_cols - cols
        assert not missing, f"{p.name} missing columns: {missing}"
        print(f"  OK ({len(df)} rows)")

    print("All fetch output checks passed.")

if __name__ == "__main__":
    main()