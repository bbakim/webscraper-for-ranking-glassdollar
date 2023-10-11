from fastapi import FastAPI
import requests
import json
import uvicorn

app = FastAPI()

# ID list to find all enterprise IDs
corporate_ids = []

# API endpoint URL
url = "https://ranking.glassdollar.com/graphql"

# Request headers to communicate with the website
headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9,tr-TR;q=0.8,tr;q=0.7",
    "Content-Type": "application/json",
    "Cookie": "pubconsent-v2=YAAAAAAAAAAA; euconsent-v2=CPzHq4APzHq4AAZACBENDZCsAP_AAH_AAAAAJrNV_H__bW9r8X7_aft0eY1P9_j77uQxBhfJE-4F3LvW_JwXx2E5NF36tqoKmRoEu3ZBIUNlHJHUTVmwaogVryHsak2cpTNKJ6BkkFMRM2dYCF5vm4tjeQKY5_p_d3fx2D-t_dv839z3z81Xn3d5f--0-PCdU5-9Dfn9fRfb-9IP9_78v8v8_l_rk2_eT13_pcvr_D--f_87_XW-8E1ACTDQuIAuwICQm0DCKBACMKwgIoFAAAAJA0QEALgwKdkYBLrARACBFAAcEAIQAUZAAgAAAgAQiACQIoEAAEAgEAAIAEAgEABAwACgAsBAIAAQHQMUwoAFAsIEiMiIUwIQoEggJbKhBKC4QVwgCLLACgERsFAAgAAEVgACAsXgMASAlQkECXUG0AABAAgFFKFQgk9MAA4JGy1B4IAA.YAAAAAAAAAAA",
    "Origin": "https://ranking.glassdollar.com",
    "Referer": "https://ranking.glassdollar.com/",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
}

@app.get("/fetch-and-save-data")
async def fetch_and_save_data():
    try:
        # Initialize page number and a flag to check if there are more pages
        page_number = 1
        more_pages = True

        while more_pages:
            # Request payload to fetch corporates for the current page
            payload = {
                "operationName": "Corporates",
                "variables": {
                    "filters": {
                        "industry": [],
                        "hq_city": []
                    },
                    "page": page_number,
                    "sortBy": "name"
                },
                "query": """
                    query Corporates($filters: CorporateFilters, $page: Int, $sortBy: String) {
                        corporates(filters: $filters, page: $page, sortBy: $sortBy) {
                            rows {
                                id
                                name
                            }
                            count
                        }
                    }
                """
            }

            response = requests.post(url, headers=headers, json=payload)

            if response.status_code == 200:
                response_data = response.json()
                corporate_data = response_data.get("data", {}).get("corporates", {})
                rows = corporate_data.get("rows", [])
                total_count = corporate_data.get("count", 0)

                # Append IDs from the current page to the corporate_ids list
                for row in rows:
                    corporate_ids.append(row.get("id"))

                # Check if there are more pages to fetch
                if len(corporate_ids) < total_count:
                    page_number += 1
                else:
                    more_pages = False
            else:
                print(f"Failed to fetch data for page {page_number}. Status code: {response.status_code}")
                break

    except Exception as e:
        print(f"An error occurred: {e}")

    # IDs that are in the list will be printed
    print("Company IDs:", corporate_ids)

    # Base URL is created because all detailed info of enterprises have this base URL
    base_referer_url = "https://ranking.glassdollar.com/corporates/"

    # The gathered information will be stored in a list
    corporate_data_list = []

    for corporate_id in corporate_ids:
        referer_url = base_referer_url + corporate_id

        # Request payload will be reformatted each time with enterprise's unique IDs
        payload = {
            "query": f"""
                {{
                    corporate(id: "{corporate_id}") {{
                        id
                        name
                        description
                        logo_url
                        hq_city
                        hq_country
                        website_url
                        linkedin_url
                        twitter_url
                        startup_partners_count
                        startup_partners {{
                            company_name
                            logo_url: logo
                            city
                            website
                            country
                            theme_gd
                        }}
                        startup_themes
                    }}
                }}
            """
        }

        try:
            # Referer header for the current corporate ID is updated
            headers["Referer"] = referer_url
            response = requests.post(url, headers=headers, json=payload)

            if response.status_code == 200:
                response_data = response.json()
                corporate_data = response_data.get("data", {}).get("corporate", {})
                
                # Add the retrieved data to the list
                corporate_data_list.append(corporate_data)
                
                # To inform the user that the enterprise data has been added
                current_corporate_name = corporate_data.get("name", "")
                print(f"{current_corporate_name} data has been retrieved.")

            else:
                print(f"Failed to retrieve data for corporate ID {corporate_id}!")

        except Exception as e:
            print(f"An error occurred for corporate ID {corporate_id}: {e}")

    # Save the list of corporate data to a JSON file
    with open("corporate_data.json", "w") as json_file:
        json.dump(corporate_data_list, json_file, indent=4)

def run_fastapi_app():
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")


if __name__ == "__main__":
    # URL that needed to proceed when the application starts
    print("URL: http://localhost:8000/docs")
    run_fastapi_app()
