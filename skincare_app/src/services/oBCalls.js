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
export async function generate_routine(products) {
  try {
    const response = await apiConnect.post("/routine", products);
    return response.data.routine;
  } catch (error) {
    console.error("Error to generate routine", error);
    return null;
  }
}
export async function generateFullRoutine(productNames) {
  try {
    const response = await apiConnect.post(
      "/products/generate_full_routine",
      productNames
    );
    return response.data.routine;
  } catch (error) {
    console.error("Error generating full routine:", error);
    return [];
  }
}
