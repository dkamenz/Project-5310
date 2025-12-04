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
    "listing_status",
    "square_feet",
    "min_price",
    "max_price",
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
        "listing_status": prop.get("listing", {}).get("listingStatus"),
        "min_price": prop.get("price", {}).get("value") or prop.get("minPrice"),
        "max_price": prop.get("price", {}).get("value") or prop.get("maxPrice"),
    }

    units = prop.get("unitsGroup", [])

    
    if units:
        for unit in units:
            row = base.copy()
            row["square_feet"] = unit.get("livingArea") or prop.get("livingArea")
            row["bedrooms"] = unit.get("bedrooms")
            row["min_price"] = unit.get("minPrice", row["min_price"])
            row["max_price"] = unit.get("maxPrice", row["max_price"])
            rows.append(row)


    else:
        row = base.copy()
        row["square_feet"] = prop.get("livingArea") 
        row["bedrooms"] = prop.get("bedrooms")
        rows.append(row)

# Write CSV
with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=columns)
    writer.writeheader()
    writer.writerows(rows)

print(f"CSV created: {output_file} ({len(rows)} rows)")
