from dotenv import load_dotenv
from serpapi import GoogleSearch
import os

load_dotenv()

def search_clothing_item(image_url):
    
    # Define the SerpApi endpoint and parameters
    api_key = os.getenv("SERPAPI_KEY")
    search = GoogleSearch({
        "engine": "google_lens",
        "api_key": api_key,
        "url": image_url,
    })
    
    # Make the API call
    results = search.get_dict()
    search_metadata = results.get("search_metadata", {})
    status = search_metadata.get("status", "Unknown")
    
    # Check for successful response

    if status == "Success":
         # Get the top 8 queries

        queries = results.get("visual_matches", [])

        items = {}
        counter = 1
        for query in queries:
            if "price" in query:
                link = query.get("link", "No link available")
                thumbnail = query.get("thumbnail", "No thumbnail available")
                price = query.get("price", "No price available")
                extracted_price = price.get("extracted_value", "No extracted price available")
                
                # Use the counter as the key
                items[counter] = {
                    "link": link,
                    "thumbnail": thumbnail,
                    "extracted_price": extracted_price
                }
                
                counter += 1
                
                # Stop after 5 items
                if counter == 5:
                    break
        print(items)
    else:
       return {"error": "Failed to retrieve data"}



# Example usage
if __name__ == "__main__":
    image_url = "https://www.paragonjackets.com/wp-content/uploads/2023/05/Yeezy-Gap-Black-Hoodie.jpg"
    results = search_clothing_item(image_url)
