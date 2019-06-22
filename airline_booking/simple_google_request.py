import requests

def main():
    #res = requests.get("http://data.fixer.io/api/latest?access_key=3a75480abfed168014d40340d05418e6&format=1&base=EUR&symbols=VND")
    base = input("Convert from: ")
    other = input("To: ")
    res = requests.get("http://data.fixer.io/api/latest?access_key=3a75480abfed168014d40340d05418e6&format=1",
                            params={"base": base, "symbols": other})
    if res.status_code != 200:
        raise Exception("ERROR: API request unsuccessful.")
#The API Endpoints already had it format=1 which mean in json format,
#therefore, we dont need this line of code.
    #data = res.json()
    print(res.text)

    data =res.json()
    rate = data["rates"][other]
    print(f" 1 {base} is equal to {rate} {other}")



if __name__ == "__main__":
    main()
