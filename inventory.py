from collections import Counter
import pandas as pd


def count_inventory(detections):

    counts = Counter(
        item["name"] for item in detections
    )

    inventory_data = []

    for object_name, quantity in counts.items():

        inventory_data.append({
            "Object": object_name.title(),
            "Quantity": quantity
        })

    df = pd.DataFrame(
        inventory_data,
        columns=["Object", "Quantity"]
    )

    total_objects = sum(counts.values())

    return df, total_objects
