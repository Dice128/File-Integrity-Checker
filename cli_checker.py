#!/usr/bin/env python3
"""
cli_checker.py
Usage examples:
  - Generate baseline for file: python cli_checker.py --generate path/to/file
  - Generate baseline for folder: python cli_checker.py --generate-folder path/to/folder
  - Verify a file: python cli_checker.py --verify path/to/file
  - Verify all from baseline: python cli_checker.py --verify-all
"""

import hashlib
import json
import os
import argparse

BASELINE_FILE = "baseline.json"
HASH_ALGOS = ["md5", "sha1", "sha256"]

def calc_hash(path, algo="sha256", block_size=65536):
    h = hashlib.new(algo)
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(block_size), b""):
            h.update(block)
    return h.hexdigest()

def generate_baseline_for_file(path):
    path = os.path.abspath(path)
    if not os.path.isfile(path):
        raise FileNotFoundError(path)
    entry = {"path": path}
    for algo in HASH_ALGOS:
        entry[algo] = calc_hash(path, algo)
    return entry

def generate_baseline_for_folder(folder):
    entries = []
    for root, dirs, files in os.walk(folder):
        for fname in files:
            full = os.path.join(root, fname)
            try:
                entries.append(generate_baseline_for_file(full))
            except Exception as e:
                print(f"Skip {full}: {e}")
    return entries

def save_baseline(entries, outfile=BASELINE_FILE):
    # baseline is list of entries
    with open(outfile, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2)
    print(f"Baseline saved to {outfile}")

def load_baseline(infile=BASELINE_FILE):
    if not os.path.exists(infile):
        return []
    with open(infile, "r", encoding="utf-8") as f:
        return json.load(f)

def verify_file_against_entry(path, entry):
    results = {}
    for algo in HASH_ALGOS:
        actual = calc_hash(path, algo)
        expected = entry.get(algo)
        results[algo] = {"expected": expected, "actual": actual, "match": actual == expected}
    return results

def main():
    p = argparse.ArgumentParser(description="Simple File Integrity Checker (CLI)")
    p.add_argument("--generate", help="Generate baseline for a single file", metavar="FILE")
    p.add_argument("--generate-folder", help="Generate baseline for all files in folder", metavar="FOLDER")
    p.add_argument("--verify", help="Verify a single file against baseline", metavar="FILE")
    p.add_argument("--verify-all", action="store_true", help="Verify all files from baseline")
    p.add_argument("--baseline", help="Baseline file path (default baseline.json)", metavar="BASE")
    args = p.parse_args()

    baseline_file = args.baseline or BASELINE_FILE

    if args.generate:
        entry = generate_baseline_for_file(args.generate)
        save_baseline([entry], baseline_file)
        return

    if args.generate_folder:
        entries = generate_baseline_for_folder(args.generate_folder)
        save_baseline(entries, baseline_file)
        return

    if args.verify:
        entries = load_baseline(baseline_file)
        # find matching entry by path
        path_abs = os.path.abspath(args.verify)
        entry = next((e for e in entries if e["path"] == path_abs), None)
        if not entry:
            print("File not found in baseline. You can generate baseline first.")
            return
        results = verify_file_against_entry(path_abs, entry)
        for algo, res in results.items():
            print(f"{algo.upper()}: expected={res['expected']} actual={res['actual']} match={res['match']}")
        all_match = all(r["match"] for r in results.values())
        print("STATUS:", "ORIGINAL" if all_match else "MODIFIED")
        return

    if args.verify_all:
        entries = load_baseline(baseline_file)
        if not entries:
            print("No baseline found.")
            return
        for entry in entries:
            path = entry["path"]
            if not os.path.exists(path):
                print(f"[MISSING] {path}")
                continue
            results = verify_file_against_entry(path, entry)
            all_match = all(r["match"] for r in results.values())
            status = "ORIGINAL" if all_match else "MODIFIED"
            print(f"{status} - {path}")
        return

    p.print_help()

if __name__ == "__main__":
    main()
