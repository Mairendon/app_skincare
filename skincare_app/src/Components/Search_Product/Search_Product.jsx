import React, { useState } from "react";
import { searchProduct } from "../../services/oBCalls";

function Search_Product() {
  const [productName, setProductName] = useState("");
  const [productResults, setProductResults] = useState([]);

  const handleSearchProduct = async () => {
    const results = await searchProduct(productName);

    setProductResults(results);
  };

  return (
    <div style={{ marginTop: "100px" }}>
      <form onSubmit={(e) => e.preventDefault()}>
        <label>Product Name</label>
        <input
          type="text"
          className="product-name"
          name="product_name"
          placeholder="Enter product name"
          value={productName}
          onChange={(e) => setProductName(e.target.value)}
        />
        <button type="button" onClick={handleSearchProduct}>
          Search by name
        </button>
      </form>

      <div>
        {productResults.length > 0 ? (
          productResults.map((product, index) => (
            <div key={index}>
              <h3>{product.product_name || "No name"}</h3>
              <p>{product.brands}</p>
              {/* <p>{product.ingredients_text}</p> */}
              <p>{product.product_type}</p>
              <p>{product.categories_tags}</p>
              <p>{product.categories}</p>
              <img
                src={product.image_url}
                alt={product.product_name}
                style={{ width: "100px" }}
              />
              <hr />
            </div>
          ))
        ) : (
          <p>No products found</p>
        )}
      </div>
    </div>
  );
}

export default Search_Product;
