# LS Speed Dashboard
Static page (no build). `index.html` reads `data.json`.

**Manual refresh:** open the page → *Upload CSV* (raw "SLA Raw Data" CSV) → view updates in-browser.
To publish it for everyone: *⬇ data.json* → replace `data.json` in the repo → commit.

**Automated refresh:** push the raw file to `data/raw.csv` (or `raw.xlsx`); `.github/workflows/refresh.yml` rebuilds `data.json`. Any scheduled job/script can do that push.

**Publish:** repo → Settings → Pages → Deploy from branch `main` / root.
Required CSV columns: order_date, year_week_num_in_year, service_profile, service_type_bucket, app_flag, mega_cat, analytic_super_category, sum_sla, total_units, d0_units, d1_units, d2_units, d4_units, d6_units, d8_units.
