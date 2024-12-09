import zillow


__KEY = 'X1-ZWz1hbqm0j5w5n_26nu3'

if __name__ == '__main__':
    api = zillow.ValuationApi()

    address = "816 N Oakland St"
    postal_code = "22203"

    data = api.GetSearchResults(__KEY, address, postal_code)


    print(data)