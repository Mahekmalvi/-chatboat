import requests
from bs4 import BeautifulSoup

def search_products(gender, occasion, note):
    """
    Scrapes Muskbliss site for products matching note/occasion/gender.
    For demo: searches by note as main query, filters by keywords.
    """
    # Try note as main keyword
    search_query = note or occasion or gender
    url = f"https://muskbliss.com/search?q={search_query}"
    try:
        response = requests.get(url, timeout=8)
        soup = BeautifulSoup(response.text, 'html.parser')
        # Parse product grid (Shopify theme)
        products = []
        for card in soup.select('.product-card, .product-item, .grid-product'):
            name = card.select_one('.product-card__title, .product-title, .grid-product__title')
            link = card.select_one('a')
            img = card.select_one('img')
            if not (name and link and img): continue
            prod_name = name.get_text(strip=True)
            prod_link = link['href']
            prod_img = img.get('src') or img.get('data-src')
            # Make full url if needed
            if prod_link.startswith('/'):
                prod_link = 'https://muskbliss.com' + prod_link
            if prod_img and prod_img.startswith('//'):
                prod_img = 'https:' + prod_img
            products.append({
                "name": prod_name,
                "img": prod_img,
                "link": prod_link
            })
            if len(products) >= 6: break  # Show up to 6
        return products
    except Exception as e:
        # On error, return empty
        return []