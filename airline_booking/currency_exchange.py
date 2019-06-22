import requests
import json

def main():
    base = input("Convert from: ")
    other = input("To: ")
    res = requests.get("http://data.fixer.io/api/latest&format=1",
                        params={"access_key":"3a75480abfed168014d40340d05418e6","base": base, "symbols": other})
    if res.status_code != 200:
        raise Exception("ERROR: API request unsuccessful.")

    print(res.text)
    data = res.json()
    rate = data["rates"][other]
    print(f" 1 {base} is equal to {rate} {other}")


if __name__ == "__main__":
    main()
