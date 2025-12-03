import json
import csv


input_file = "data/zillow_scraped.json" 
output_file = "data/apts_2025_raw.csv"

with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)


columns = [
    "zpid",
    "address",
    "cityname",
    "state",
    "zipcode",
    "latitude",
    "longitude",
    "title",
    "listingStatus",
    "minPrice",
    "maxPrice",
    "bedrooms"
]

rows = []

for item in data.get("searchResults", []):
    prop = item["property"]

    base = {
        "zpid": prop.get("zpid"),
        "address": prop.get("address", {}).get("streetAddress"),
        "cityname": prop.get("address", {}).get("city"),
        "state": prop.get("address", {}).get("state"),
        "zipcode": prop.get("address", {}).get("zipcode"),
        "latitude": prop.get("location", {}).get("latitude"),
        "longitude": prop.get("location", {}).get("longitude"),
        "title": prop.get("title"),
        "listingStatus": prop.get("listingStatus"),
        "minPrice": prop.get("minPrice"),
        "maxPrice": prop.get("maxPrice"),
    }

    units = prop.get("unitsGroup", [])

    if units:
        for unit in units:
            row = base.copy()
            row["bedrooms"] = unit.get("bedrooms")
            row["minPrice"] = unit.get("minPrice", row["minPrice"])
            rows.append(row)
    else:
        row = base.copy()
        row["bedrooms"] = None
        rows.append(row)

with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=columns)
    writer.writeheader()
    writer.writerows(rows)

print(f"CSV created: {output_file} ({len(rows)} rows)")
