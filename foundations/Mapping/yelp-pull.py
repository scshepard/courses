#
# yelp-pull.py
# Pull top 20 Yelp results for 'lunch' from every neighborhood in NYC
#
# NOTE: Be sure to deduplicate the results!

from yelpapi import YelpAPI
import unicodecsv
import time

def business_row(business):
    return [ business['location']['address'][0], 
     business['location']['city'],
     business['categories'][0][0],
     business['rating'],
     business['url'] ]

# Pulled the list from the neighborhoods shapefile at
# http://www.nyc.gov/html/dcp/html/bytes/applbyte.shtml#other
# Used http://dbfconv.com to convert the dbf (the data part of a shapefile) into a csv
neighborhoods = [ "Wakefield, Bronx", "Co-op City, Bronx", "Eastchester, Bronx", "Fieldston, Bronx", "Riverdale, Bronx", "Kingsbridge, Bronx", "Marble Hill, Manhattan", "Woodlawn, Bronx", "Norwood, Bronx", "Williamsbridge, Bronx", "Baychester, Bronx", "Pelham Parkway, Bronx", "City Island, Bronx", "Bedford Park, Bronx", "University Heights, Bronx", "Morris Heights, Bronx", "Fordham, Bronx", "East Tremont, Bronx", "West Farms, Bronx", "High  Bridge, Bronx", "Melrose, Bronx", "Mott Haven, Bronx", "Port Morris, Bronx", "Longwood, Bronx", "Hunts Point, Bronx", "Morrisania, Bronx", "Soundview, Bronx", "Clason Point, Bronx", "Throgs Neck, Bronx", "Country Club, Bronx", "Parkchester, Bronx", "Westchester Square, Bronx", "Van Nest, Bronx", "Morris Park, Bronx", "Belmont, Bronx", "Spuyten Duyvil, Bronx", "North Riverdale, Bronx", "Pelham Bay, Bronx", "Schuylerville, Bronx", "Edgewater Park, Bronx", "Castle Hill, Bronx", "Olinville, Bronx", "Pelham Gardens, Bronx", "Concourse, Bronx", "Unionport, Bronx", "Edenwald, Bronx", "Bay Ridge, Brooklyn", "Bensonhurst, Brooklyn", "Sunset Park, Brooklyn", "Greenpoint, Brooklyn", "Gravesend, Brooklyn", "Brighton Beach, Brooklyn", "Sheepshead Bay, Brooklyn", "Manhattan Terrace, Brooklyn", "Flatbush, Brooklyn", "Crown Heights, Brooklyn", "East Flatbush, Brooklyn", "Kensington, Brooklyn", "Windsor Terrace, Brooklyn", "Prospect Heights, Brooklyn", "Brownsville, Brooklyn", "Williamsburg, Brooklyn", "Bushwick, Brooklyn", "Bedford Stuyvesant, Brooklyn", "Brooklyn Heights, Brooklyn", "Cobble Hill, Brooklyn", "Carroll Gardens, Brooklyn", "Red Hook, Brooklyn", "Gowanus, Brooklyn", "Fort Greene, Brooklyn", "Park Slope, Brooklyn", "Cypress Hills, Brooklyn", "East New York, Brooklyn", "Starrett City, Brooklyn", "Canarsie, Brooklyn", "Flatlands, Brooklyn", "Mill Island, Brooklyn", "Manhattan Beach, Brooklyn", "Coney Island, Brooklyn", "Bath Beach, Brooklyn", "Borough Park, Brooklyn", "Dyker Heights, Brooklyn", "Gerritsen Beach, Brooklyn", "Marine Park, Brooklyn", "Clinton Hill, Brooklyn", "Sea Gate, Brooklyn", "Downtown, Brooklyn", "Boerum Hill, Brooklyn", "Prospect Lefferts Gardens, Brooklyn", "Ocean Hill, Brooklyn", "City Line, Brooklyn", "Bergen Beach, Brooklyn", "Midwood, Brooklyn", "Prospect Park South, Brooklyn", "Georgetown, Brooklyn", "Spring Creek, Brooklyn", "East Williamsburg, Brooklyn", "North Side, Brooklyn", "South Side, Brooklyn", "Navy Yard, Brooklyn", "Ocean Parkway, Brooklyn", "Fort Hamilton, Brooklyn", "Chinatown, Manhattan", "Washington Heights, Manhattan", "Inwood, Manhattan", "Hamilton Heights, Manhattan", "Manhattanville, Manhattan", "Central Harlem, Manhattan", "East Harlem, Manhattan", "Upper East Side, Manhattan", "Yorkville, Manhattan", "Lenox Hill, Manhattan", "Roosevelt Island, Manhattan", "Upper West Side, Manhattan", "Lincoln Square, Manhattan", "Clinton, Manhattan", "Midtown, Manhattan", "Murray Hill, Manhattan", "Chelsea, Manhattan", "Greenwich Village, Manhattan", "East Village, Manhattan", "Lower East Side, Manhattan", "Tribeca, Manhattan", "Little Italy, Manhattan", "Soho, Manhattan", "West Village, Manhattan", "Manhattan Valley, Manhattan", "Morningside Heights, Manhattan", "Gramercy, Manhattan", "Battery Park City, Manhattan", "Financial District, Manhattan", "Astoria, Queens", "Woodside, Queens", "Jackson Heights, Queens", "Elmhurst, Queens", "Howard Beach, Queens", "South Corona, Queens", "Forest Hills, Queens", "Kew Gardens, Queens", "Richmond Hill, Queens", "Downtown Flushing, Queens", "Long Island City, Queens", "Sunnyside, Queens", "East Elmhurst, Queens", "Maspeth, Queens", "Ridgewood, Queens", "Glendale, Queens", "Rego Park, Queens", "Woodhaven, Queens", "Ozone Park, Queens", "South Ozone Park, Queens", "College Point, Queens", "Whitestone, Queens", "Bayside, Queens", "Auburndale, Queens", "Little Neck, Queens", "Douglaston, Queens", "Glen Oaks, Queens", "Bellerose, Queens", "Kew Gardens Hills, Queens", "Fresh Meadows, Queens", "Briarwood, Queens", "Jamaica Center, Queens", "Oakland Gardens, Queens", "Queens Village, Queens", "Hollis, Queens", "South Jamaica, Queens", "St. Albans, Queens", "Rochdale, Queens", "Springfield Gardens, Queens", "Cambria Heights, Queens", "Rosedale, Queens", "Far Rockaway, Queens", "Broad Channel, Queens", "Breezy Point, Queens", "Steinway, Queens", "Beechhurst, Queens", "Bay Terrace, Queens", "Edgemere, Queens", "Arverne, Queens", "Seaside, Queens", "Neponsit, Queens", "Murray Hill, Queens", "Floral Park, Queens", "Holliswood, Queens", "Jamaica Estates, Queens", "Queensboro Hill, Queens", "Hillcrest, Queens", "Ravenswood, Queens", "Lindenwood, Queens", "Laurelton, Queens", "Lefrak City, Queens", "Belle Harbor, Queens", "Rockaway Park, Queens", "Somerville, Queens", "Brookville, Queens", "Bellaire, Queens", "North Corona, Queens", "Forest Hills Gardens, Queens", "St. George, Staten Island", "New Brighton, Staten Island", "Stapleton, Staten Island", "Rosebank, Staten Island", "West Brighton, Staten Island", "Grymes Hill, Staten Island", "Todt Hill, Staten Island", "South Beach, Staten Island", "Port Richmond, Staten Island", "Mariner's Harbor, Staten Island", "Port Ivory, Staten Island", "Castleton Corners, Staten Island", "New Springville, Staten Island", "Travis, Staten Island", "New Dorp, Staten Island", "Oakwood, Staten Island", "Great Kills, Staten Island", "Eltingville, Staten Island", "Annadale, Staten Island", "Woodrow, Staten Island", "Tottenville, Staten Island", "Tompkinsville, Staten Island", "Silver Lake, Staten Island", "Sunnyside, Staten Island", "Ditmas Park, Brooklyn", "Wingate, Brooklyn", "Rugby, Brooklyn", "Park Hill, Staten Island", "Westerleigh, Staten Island", "Graniteville, Staten Island", "Arlington, Staten Island", "Arrochar, Staten Island", "Grasmere, Staten Island", "Old Town, Staten Island", "Dongan Hills, Staten Island", "Midland Beach, Staten Island", "Grant City, Staten Island", "New Dorp Beach, Staten Island", "Bay Terrace, Staten Island", "Huguenot, Staten Island", "Pleasant Plains, Staten Island", "Butler Manor, Staten Island", "Charleston, Staten Island", "Rossville, Staten Island", "Arden Heights, Staten Island", "Greenridge, Staten Island", "Heartland Village, Staten Island", "Chelsea, Staten Island", "Bloomfield, Staten Island", "Bulls Head, Staten Island", "Carnegie Hill, Manhattan", "Noho, Manhattan", "Civic Center, Manhattan", "Midtown South, Manhattan", "Richmond Town, Staten Island", "Shore Acres, Staten Island", "Clifton, Staten Island", "Concord, Staten Island", "Emerson Hill, Staten Island", "Randall Manor, Staten Island", "Howland Hook, Staten Island", "Elm Park, Staten Island", "Remsen Village, Brooklyn", "New Lots, Brooklyn", "Paerdegat Basin, Brooklyn", "Mill Basin, Brooklyn", "Jamaica Hills, Queens", "Utopia, Queens", "Pomonok, Queens", "Astoria Heights, Queens", "Claremont Village, Bronx", "Concourse Village, Bronx", "Mount Eden, Bronx", "Mount Hope, Bronx", "Sutton Place, Manhattan", "Hunters Point, Queens", "Turtle Bay, Manhattan", "Tudor City, Manhattan", "Stuyvesant Town, Manhattan", "Flatiron, Manhattan", "Sunnyside Gardens, Queens", "Blissville, Queens", "Fulton Ferry, Brooklyn", "Vinegar Hill, Brooklyn", "Weeksville, Brooklyn", "Broadway Junction, Brooklyn", "Dumbo, Brooklyn", "Manor Heights, Staten Island", "Willowbrook, Staten Island", "Sandy Ground, Staten Island", "Egbertville, Staten Island", "Roxbury, Queens", "Homecrest, Brooklyn", "Middle Village, Queens", "Prince's Bay, Staten Island", "Lighthouse Hill, Staten Island", "Richmond Valley, Staten Island", "Malba, Queens", "Highland Park, Brooklyn", "Madison, Brooklyn" ]

# You'll have to put your own keys here -
# register at http://www.yelp.com/developers/
yelp_api = YelpAPI(CONSUMER_KEY, CONSUMER_SECRET, TOKEN, TOKEN_SECRET)

with open('lunch-morningside-heights-yelp.csv', 'wb') as csvfile:
    business_writer = unicodecsv.writer(csvfile)
    business_writer.writerow(["Name", "Address", "City", "Category", "Rating", "URL"])

    for neighborhood in ["Morningside Heights"]:
        # Pause for a second so Yelp doesn't get unhappy with us
        time.sleep(1)

        print "Processing %s" % neighborhood
        response = yelp_api.search_query(term='lunch', location='%s, New York' % neighborhood, limit=20)

        for business in response['businesses']:
            # When we call business_row, maybe some are missing categories or addresses etc
            # If that happens, let's just ignore the error and keep on trucking
            try:
                business_writer.writerow(business_row(business))
            except:
                print "Failed!"
                pass
