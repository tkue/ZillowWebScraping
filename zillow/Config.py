import os

# start_url = 'https://www.zillow.com/homes/Washington-DC_rb/'
start_url = 'https://www.zillow.com/washington-dc/cheap-apartments/?searchQueryState={%22pagination%22:{},%22mapBounds%22:{%22west%22:-77.28421118457032,%22east%22:-76.7445078154297,%22south%22:38.74390763696738,%22north%22:39.05406371342246},%22usersSearchTerm%22:%22Washington%20DC%22,%22regionSelection%22:[{%22regionId%22:41568,%22regionType%22:6}],%22isMapVisible%22:true,%22mapZoom%22:11,%22filterState%22:{%22sortSelection%22:{%22value%22:%22paymenta%22},%22isForSaleByAgent%22:{%22value%22:false},%22isForSaleByOwner%22:{%22value%22:false},%22isNewConstruction%22:{%22value%22:false},%22isForSaleForeclosure%22:{%22value%22:false},%22isComingSoon%22:{%22value%22:false},%22isAuction%22:{%22value%22:false},%22isPreMarketForeclosure%22:{%22value%22:false},%22isPreMarketPreForeclosure%22:{%22value%22:false},%22isMakeMeMove%22:{%22value%22:false},%22isForRent%22:{%22value%22:true},%22monthlyPayment%22:{%22max%22:2000},%22price%22:{%22max%22:530872},%22hasAirConditioning%22:{%22value%22:true}},%22isListVisible%22:true}'
# start_url = 'C:\\Users\\tomku\\Downloads\\Cheap Apartments For Rent _ Zillow.html'
download_path = os.path.abspath(os.curdir)
driver_path = 'lib\\chromedriver75.exe'
firefox_driver_path = 'lib\\geckodriver.exe'
csv_output = 'listings.csv'

def get_url(page: int):
    if not page or not page > 0:
        return 'https://www.zillow.com/washington-dc/cheap-apartments/?searchQueryState={%22pagination%22:{},%22mapBounds%22:{%22west%22:-77.28421118457032,%22east%22:-76.7445078154297,%22south%22:38.74390763696738,%22north%22:39.05406371342246},%22usersSearchTerm%22:%22Washington%20DC%22,%22regionSelection%22:[{%22regionId%22:41568,%22regionType%22:6}],%22isMapVisible%22:true,%22mapZoom%22:11,%22filterState%22:{%22sortSelection%22:{%22value%22:%22paymenta%22},%22isForSaleByAgent%22:{%22value%22:false},%22isForSaleByOwner%22:{%22value%22:false},%22isNewConstruction%22:{%22value%22:false},%22isForSaleForeclosure%22:{%22value%22:false},%22isComingSoon%22:{%22value%22:false},%22isAuction%22:{%22value%22:false},%22isPreMarketForeclosure%22:{%22value%22:false},%22isPreMarketPreForeclosure%22:{%22value%22:false},%22isMakeMeMove%22:{%22value%22:false},%22isForRent%22:{%22value%22:true},%22monthlyPayment%22:{%22max%22:2000},%22price%22:{%22max%22:530872},%22hasAirConditioning%22:{%22value%22:true}},%22isListVisible%22:true}'
    else:
        return 'https://www.zillow.com/washington-dc/cheap-apartments/{}_p/?searchQueryState={%22pagination%22:{%22currentPage%22:{}},%22mapBounds%22:{%22west%22:-77.28421118457032,%22east%22:-76.7445078154297,%22south%22:38.74390763696738,%22north%22:39.05406371342246},%22usersSearchTerm%22:%22Washington%20DC%22,%22regionSelection%22:[{%22regionId%22:41568,%22regionType%22:6}],%22mapZoom%22:11,%22filterState%22:{%22sortSelection%22:{%22value%22:%22paymenta%22},%22isForSaleByAgent%22:{%22value%22:false},%22isForSaleByOwner%22:{%22value%22:false},%22isNewConstruction%22:{%22value%22:false},%22isForSaleForeclosure%22:{%22value%22:false},%22isComingSoon%22:{%22value%22:false},%22isAuction%22:{%22value%22:false},%22isPreMarketForeclosure%22:{%22value%22:false},%22isPreMarketPreForeclosure%22:{%22value%22:false},%22isMakeMeMove%22:{%22value%22:false},%22isForRent%22:{%22value%22:true},%22monthlyPayment%22:{%22max%22:2000},%22price%22:{%22max%22:530872},%22hasAirConditioning%22:{%22value%22:true}},%22isListVisible%22:true,%22isMapVisible%22:false}'.format(page)