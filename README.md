# LifeOS Manual Explorer — deploy
1. Edit `wrangler.toml` → set `bucket_name` to your R2 bucket.
2. `npx wrangler deploy`
3. Bucket layout the app expects:
   `Vehicle Name/Manual Name/Section Name/PAGE-ID Title.(pdf|html|md|txt|png)`
   e.g. `2006 Scion xB/Repair Manual/Engine Mechanical/EM-01 Engine Removal.md`
4. Protect the site with Cloudflare Access (Zero Trust) — the API is read-only but public by default.

## Drill-down indexes
The checked-in `sample/` folder contains four navigation-tree fixtures. The app loads these through the Worker as test navigation data; their numbered page bodies are still expected in R2 at `<Vehicle>/pages/N.html`. For live manuals, upload each `tree.json` to R2 at `<Vehicle>/<Manual>/tree.json`.

Convert each index page, then upload to R2:
  python tools/build_tree.py 2.html "Repair and Diagnosis" > tree.json   -> 2006 Scion xB/Repair and Diagnosis/tree.json
  python tools/build_tree.py 3.html "Parts and Labor"      > tree.json   -> 2006 Scion xB/Parts and Labor/tree.json
Upload the pages themselves to  <Vehicle>/pages/N.html  (same numbers as the index links).
Repeat per vehicle (e.g. 2019 Subaru Crosstrek: use the "full tree" index page, not the split tree).
