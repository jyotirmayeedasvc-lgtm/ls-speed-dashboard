#!/usr/bin/env python3
"""Aggregate raw SLA data (CSV, or xlsx sheet 'SLA Raw Data') into data.json.
Usage: python build_data.py data/raw.csv [data.json]
"""
import csv, json, sys, datetime

NUMS = ["sum_sla", "total_units", "d0_units", "d1_units", "d2_units", "d4_units", "d6_units", "d8_units"]
DIMS = ["service_profile", "service_type_bucket", "app_flag", "mega_cat", "analytic_super_category"]


def read_rows(path):
    if path.lower().endswith((".xlsx", ".xlsm")):
        import openpyxl
        ws = openpyxl.load_workbook(path, read_only=True)["SLA Raw Data"]
        it = ws.iter_rows(values_only=True)
        hdr = [str(h).strip() if h is not None else "" for h in next(it)]
        for r in it:
            yield dict(zip(hdr, r))
    else:
        with open(path, newline="", encoding="utf-8-sig") as f:
            yield from csv.DictReader(f)


def num(v):
    try:
        return float(v) if v not in (None, "") else 0.0
    except ValueError:
        return 0.0


def main(src, out="data.json"):
    agg = {}
    for r in read_rows(src):
        d = num(r.get("order_date"))
        if not d:
            continue  # blank trailing rows
        key = (int(d), int(num(r.get("year_week_num_in_year"))),
               *[(str(r.get(c) or "").strip() or "NA") for c in DIMS])
        a = agg.setdefault(key, [0.0] * len(NUMS))
        for i, c in enumerate(NUMS):
            a[i] += num(r.get(c))
    rows = [list(k) + [round(x) for x in v] for k, v in sorted(agg.items())]
    with open(out, "w") as f:
        json.dump({"generated": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
                   "rows": rows}, f, separators=(",", ":"))
    print(f"{len(rows)} aggregated rows -> {out}")


if __name__ == "__main__":
    main(sys.argv[1], *(sys.argv[2:3]))
