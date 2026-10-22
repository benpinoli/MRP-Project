"""Run from repository root; no live vendor connection or sf_quant import."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/"src"))
from samsung_research.e01 import main

if __name__ == "__main__":
    main()
