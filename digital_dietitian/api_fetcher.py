import requests

API_URL = "https://world.openfoodfacts.org/api/v0/product/{barcode}.json"

def fetch_nutrition(barcode):
    """
    Fetch nutrition facts from Open Food Facts.
    Returns a dict with keys: 'product_name', 'nutriments' or raises Exception.
    """
    resp = requests.get(API_URL.format(barcode=barcode), timeout=5)
    resp.raise_for_status()
    data = resp.json()
    if data.get('status') != 1:
        raise ValueError("Product not found")
    product = data['product']
    nutriments = product.get('nutriments', {})
    return {
        'name': product.get('product_name', 'Unknown'),
        'calories': nutriments.get('energy-kcal_100g', 0),
        'protein': nutriments.get('proteins_100g', 0),
        'fat': nutriments.get('fat_100g', 0),
        'carbs': nutriments.get('carbohydrates_100g', 0),
        'sugar': nutriments.get('sugars_100g', 0),
        'sodium': nutriments.get('sodium_100g', 0),
    }
