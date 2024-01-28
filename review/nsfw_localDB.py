import pandas as pd
import sqlite3
from contextlib import contextmanager

# Function to establish SQLite connection
@contextmanager
def sqlite_connection(db_path):
    conn = sqlite3.connect(db_path)
    try:
        yield conn
    finally:
        conn.close()

# Function to prepare data and update stores_ovenseconds        
def update_storestation_ws(stationid, configuration, storeno): 
    update_query = f"UPDATE StoreStations SET Configuration = ? WHERE StationId = ? AND StoreNo = '{storeno}';"
    conn.execute(update_query, (configuration, stationid))

# Provide the path to your SQLite database
db_path = 'C:/automations_folders/Algo.db/Algo.db'
configuration = '{ "type": "kds", "style": "makePrep4Orders", "zoom": "100", "timeFormat": 12, "ordersDisplay": "4", "shelves": 0, "shelvesCols": "2V", "selectCook": "none", "multiScreens": [ "frying" ], "newWingStreetWatermarks": { "show": true, "position": "vertical" }, "customSortItems": true, "fullOrder": false, "isDeclinedPaymentEnabled": true, "declinedPaymentTitle": { "en": "Declined", "he": "your text", "es": "your text" }, "refreshRate": 1500, "saleType": { "ta": "CO", "del": "Delivery", "dine": "Dine-In" }, "saleImg": false, "sounds": [ { "name": "newOrder", "sound": "make" }, { "name": "actionChange", "sound": "make" }, { "name": "updatedItems", "sound": "updatedItems" }, { "name": "shelfAlert", "sound": "shelfAlert" }, { "name": "error", "sound": "error" }, { "name": "reshuffle", "sound": "newMake" } ], "device": "win", "expandCookInstructions": true, "showQuantityForSingleItem": true, "hiddenOrders": true, "bumpSelection": true, "isUSADate": true, "bumpItemSelection": true, "bump": { "1": "bumpOrderClick1", "2": "bumpOrderClick2", "3": "bumpOrderClick3", "4": "bumpOrderClick4", "m": "bumpHandleOrdersRefresh", "9": "bumpFullScreenOrder", "5": "bumpRefreshPage", "<": "bumpScrollUp", "0": "bumpToggleAllIngrids", ">": "bumpScrollDown", "6": "bumpReshuffle", "r": "bumpUndo", "+": "bumpNextOrder", "-": "bumpPrevOrder", "7": "bumpCancel", "u": "bumpApprove" }, "oldStyleKdsId": false, "allowReshuffle": false, "showPrepAhead": true, "langs": [ { "lang": "English", "langVal": "en_us", "default": true } ] }'
stationid = 'WingStreet-KDS'
stores = input("Enter the storeno, separate by comma:").split(',')

with sqlite_connection(db_path) as conn:
    for storeno in stores:
        storeno = storeno.strip()   # Remove leading/trailing whitespaces if any
        # Call the function with the user-provided stores:
        update_storestation_ws(stationid, configuration, storeno)
        conn.commit()  # Commit the changes to the database

# Step 1: Get a list of stores with a specific configuration value
stores_with_specific_configuration = []
with sqlite_connection(db_path) as conn:
    select_stores_query = f"SELECT DISTINCT StoreNo FROM StoreStations WHERE Configuration = ?;"
    stores_with_specific_configuration = conn.execute(select_stores_query, (configuration,)).fetchall()
    stores_with_specific_configuration = [str(store[0]) for store in stores_with_specific_configuration]

# Calculate the number of stores updated
num_stores_updated = len(stores_with_specific_configuration)

# Step 2: Filter the DataFrame based on the list of stores
filtered_df_by_configuration = df[df['StoreNo'].isin(stores_with_specific_configuration)]

# Print the list of stores and the filtered DataFrame
# print(f"Stores with the specified configuration: {num_stores_updated} ")
# print("Stores: ", stores_with_specific_configuration)
print(f"Stores with the specified configuration ({num_stores_updated} stores): \n  { ' , '.join(stores_with_specific_configuration)}")



# Execute a SELECT query to fetch all data after updates
with sqlite_connection(db_path) as conn:
    select_query_all = "SELECT StoreNo, Configuration, StationId FROM StoreStations ;"
    df_after_updates = pd.read_sql_query(select_query_all, conn)

    # Step 3: Filter the DataFrame after updates based on the specified configuration
    df_after_updates_filtered = df_after_updates[df_after_updates['Configuration'] == configuration]

# Print the DataFrame after all updates and filtering
print("\nDataFrame after updates and filtering:")
df_after_updates_filtered

