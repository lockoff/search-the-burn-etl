import json
import os
import sys

def get_format_str(key, line_len):
    return "%s" + (" " * (line_len - len(key))) + "%d"

def count_key_appearances(records):
    counts = {}
    for record in records:
        for key in record:
            counts[key] = counts.get(key, 0) + 1
    return counts

def count_key_non_default(records, key, default):
    count = 0
    for record in records:
        if key in record and record[key] is not None and record[key] != default:
            count += 1
    return count

def count_keys_non_default(records, key_defaults):
    counts = {}
    for key in key_defaults:
        counts[key] = count_key_non_default(records, key, key_defaults[key])
    return counts

def print_key_counts(counts):
    for key in counts:
        print get_format_str(key, 32) % (key, counts[key])

def present_counts(records):
    print "Total Num Records: %d" % len(records)
    print "Records with Key Present:"
    key_counts = count_key_appearances(records)
    print_key_counts(key_counts)

def non_default_counts(records, key_defaults):
    print "Records with Non-Default Value for Keys: "
    key_counts = count_keys_non_default(records, key_defaults)
    print_key_counts(key_counts)

def read_json(path):
    with open(path) as file:
        return json.load(file)

def event_counts(events_path):
    events = read_json(events_path)
    present_counts(events)
    default_values = {
        "occurrence_set": [],
        "description": "",
        "hosted_by_camp": {},
        "url": "",
        "located_at_art": False,
        "title": "",
        "all_day": False,
        "id": 0,
        "year": {},
        "print_description": "",
        "check_location": False,
        "slug": "",
        "other_location": "",
        "event_type": {}
    }
    non_default_counts(events, default_values)
    event_types = [event["event_type"] for event in events]
    type_counts = {}
    for event_type in event_types:
        event_type_key = event_type["label"]
        type_counts[event_type_key] = type_counts.get(event_type_key, 0) + 1
    print "Counting Event Types:"
    print_key_counts(type_counts)

def camp_counts(camps_path):
    camps = read_json(camps_path)
    present_counts(camps)
    default_values = {
        "description": "",
        "url": "",
        "contact_email": "",
        "year": {},
        "id": 0,
        "name": ""
    }
    non_default_counts(camps, default_values)

def counts(data_dir):
    events_path = os.path.join(data_dir, "events.json")
    camps_path = os.path.join(data_dir, "camps.json")
    print "Statistics for Events:"
    event_counts(events_path)
    print "----------------------------------------------------"
    print "Statistics for Camps:"
    camp_counts(camps_path)

if __name__ == '__main__':
    counts(sys.argv[1])
