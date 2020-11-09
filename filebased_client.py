import json

import requests

data_file_loation = 'data/birmingham.json'


def download_latest_file():
    with open(data_file_loation, 'w') as f:
        file_url = "https://ratings.food.gov.uk/OpenDataFiles/FHRS402en-GB.json"

        r = requests.get(file_url)
        f.write(json.dumps(r.json()))


if __name__ == "__main__":
    # download_latest_file()
    with open(data_file_loation, 'r') as f:
        bdata = json.load(f)

    establishments = bdata["FHRSEstablishment"]["EstablishmentCollection"]["EstablishmentDetail"]

    for e in establishments:
        print(e)
