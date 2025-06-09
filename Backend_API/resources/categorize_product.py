from typing import Optional

ROUTINE_ORDER = {
  "cleanser",
  "toner",
  "serum",
  "moisturizer",
  "sunscreen",
}

CATEGORY_KEYWORDS = {
  "cleanser": ["cleanser", "limpiador", "gel nettoyant", "face wash", "cleansing"],
  "toner": ["toner", "tónico", "tonique"],
  "serum": ["serum", "suero"],
  "moisturizer": ["moisturizer", "crema", "lotion", "hydrating"],
  "sunscreen": ["sunscreen", "spf", "protector solar"],
}

def detect_step_type(name:Optional[str], categories: Optional[str], description: Optional[str] = "") -> Optional[str]:
  combined_text = f"{name or ''} {categories or ''} {description or ''}".lower()
  for step in ROUTINE_ORDER:
    for keyword in CATEGORY_KEYWORDS[step]:
      if keyword in combined_text:
        return step
  
  return None

def order_products_by_routine(products: list[dict]) -> list[dict]:
  ordered = []
  for product in products:
    step = detect_step_type(
      product.get("product_name"),
      product.get("categories"),
      product.get("ingredients_text", "")
    )
    if step:
      product["step"] = step
      product["step_order"] = ROUTINE_ORDER.index(step)
      ordered.append(product)

    return sorted(ordered, key=lambda p: p["step_order"])
