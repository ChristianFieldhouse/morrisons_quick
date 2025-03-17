import uiautomator2 as u2
import time
import re
import itertools
import math

# --- Part 1: Retrieve Aisle/Section Information via UI Automation ---

# Connect to the device (ensure your device is connected via ADB)
d = u2.connect()

shopping_list = ["toothpaste", "eggs", "frozen pizza", "milk", "yogurt", "bread"]
results = {}

# Dump the initial hierarchy (for debugging)
#print(d.dump_hierarchy())

for item in shopping_list:
    # Locate and click the search box (try multiple possible resource IDs)
    found_search_box = False
    for i in range(10):
        if d(resourceId=f"ion-input-{i}").exists:
            d(resourceId=f"ion-input-{i}").click()
            found_search_box = True
            break
    if not found_search_box:
        print("Search box not found")
        break

    # Clear any previous text and send new text
    d.clear_text()
    d.send_keys(item)
    d.press("enter")  # Trigger the search
    time.sleep(2)     # Wait for results to load

    # Dump the UI hierarchy as an XML string
    ui_xml = d.dump_hierarchy()

    # Use regex to extract the first occurrence of location info, ending at the next quotation mark
    # This will catch labels like "Aisle 5", "Fresh Produce Section", "Chilled Food Aisle", etc.
    match = re.search(r'((?:Aisle|Section|Chilled Food Aisle|Fresh Produce Section|Market St. Bakery Section)[^"]*)"', ui_xml)
    if match:
        label = match.group(1)
        print(f"Found location info for '{item}': {label}")
    else:
        label = None
        print(f"No location info found for '{item}'.")

    results[item] = label

print("\nRaw Results:")
for product, label in results.items():
    print(f"{product}: {label}")

# --- Part 2: Map Labels to Coordinates and Solve the TSP ---

def map_label(label):
    """
    Maps the aisle/section string to a coordinate.
    We treat the shop as two parallel lanes:
      - Front lane (lane 0): Fresh Produce and Aisles 1-11.
      - Back lane  (lane 1): Chilled Food and Aisles 12-22.
    """
    if label is None:
        return None
    if "Fresh Produce" in label:
        return (0, 0)  # front lane, position 0
    elif "Chilled Food" in label:
        return (1, 0)  # back lane, position 0
    elif "Market St. Bakery" in label:
        return (2, 7)
    else:
        m = re.search(r'Aisle\s*(\d+)', label)
        if m:
            aisle = int(m.group(1))
            if aisle <= 11:
                return (0, aisle)  # front lane
            else:
                # For back aisles, subtract 11 so that Aisle 12 becomes (1,1), 13 becomes (1,2), etc.
                return (1, aisle - 11)
    return None

def euclidean_distance(coord1, coord2):
    """Compute Euclidean distance between two 2D coordinates."""
    return math.sqrt((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)

# Map the found results to coordinates
locations = {}
for product, label in results.items():
    coord = map_label(label)
    if coord is not None:
        locations[product] = coord
    else:
        print(f"Could not map {product} with label '{label}'")

print("\nMapped Locations (lane, position):")
for product, coord in locations.items():
    print(f"{product}: {coord}")

# Solve the TSP over the shopping list using brute force.
# Assume starting position is at (0, 0) (Fresh Produce Section).
start = (0, 0)
best_order = None
best_total_distance = float('inf')

# Consider all orderings of the shopping list items
for perm in itertools.permutations(shopping_list):
    total_dist = 0
    current = start
    valid = True
    for item in perm:
        if item not in locations:
            valid = False
            break
        total_dist += euclidean_distance(current, locations[item])
        current = locations[item]
    if valid and total_dist < best_total_distance:
        best_total_distance = total_dist
        best_order = perm

print("\nOptimal Route:")
if best_order:
    print(f"Start at Fresh Produce (0,0)")
    for item in best_order:
        print(f"Then go to {item} - {results[item]}")
    print(f"Total distance: {best_total_distance:.2f} units")
else:
    print("Could not determine an optimal route. Check that all items were mapped correctly.")
