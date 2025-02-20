import streamlit as st
import requests
import pandas as pd

def fetch_and_process_data(query, api_key):
    """
    Fetch and process basic product data
    """
    base_url = "https://serpapi.com/search.json"
    params = {
        "engine": "google_shopping",
        "q": query,
        "api_key": api_key,
        "gl": "in",     # India location
        "currency": "INR"
    }
    
    try:
        response = requests.get(base_url, params=params)
        if response.status_code != 200:
            st.error("Failed to fetch data")
            return None
            
        data = response.json()
        results = data.get("shopping_results", [])
        
        # Extract only required fields
        processed_data = []
        for item in results[:4]:  # Get top 4 results
            price = item.get("price", "0")
            price = price.replace("₹", "").replace(",", "").replace("INR", "").strip()
            try:
                price = float(price)
            except ValueError:
                price = 0
                
            processed_data.append({
                "Product Name": item.get("title", ""),
                "Platform": item.get("source", ""),
                "Price (₹)": price
            })
            
        return pd.DataFrame(processed_data)
        
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

def main():
    st.title("Price Comparison Table")
    
    # Input fields
    api_key = "YOUR API KEY"  
    search_query = st.text_input("Enter product name")
    
    if st.button("Compare Prices"):
        if not api_key or not search_query:
            st.warning("Please enter both API key and product name")
            return
            
        df = fetch_and_process_data(search_query, api_key)
        
        if df is not None and not df.empty:
            # Sort by price
            df = df.sort_values('Price (₹)')
            
            # Highlight lowest price
            lowest_price = df['Price (₹)'].min()
            st.write("Lowest price: ₹", f"{lowest_price:,.2f}")
            
            # Display table
            st.table(df.style.highlight_min(color='lightgreen', subset=['Price (₹)']))

if __name__ == "__main__":
    main()
