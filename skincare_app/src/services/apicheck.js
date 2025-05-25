import apiConnect from "./apiConnect";

export async function check() {
  try {
    console.log("Pressing button to check connection ...");
    const response = await apiConnect.get("/check_connection");
    console.log("Connection checked", response.data);
    return response.data;
  } catch (error) {
    console.error(
      "Error checking Connection",
      error.response?.data || error.message
    );
  }
}
