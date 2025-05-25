import apiConnect from "./apiConnect";
export async function searchProduct(product_name) {
  try {
    const response = await apiConnect.get("/products/search_by_name", {
      params: { product_name },
    });
    console.log("respose", response);
    return response.data.results || [];
  } catch (error) {
    console.error("Error fetching product:", error);
    return null;
  }
}
