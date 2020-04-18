from geopy.geocoders import GoogleV3

api_key = 'AIzaSyANBKTnUtFUgYga3F-gzM6qwdNFaUul8Gg'
geolocator = GoogleV3(api_key=api_key)
locations = geolocator.reverse("22.5757344, 88.4048656")
if locations:
    print(locations[0].address)  # select first location