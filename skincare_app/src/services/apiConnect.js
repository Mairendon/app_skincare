import axios from "axios";

const apiConnect = axios.create({
  baseURL: "http://192.168.0.32:8000",
  // baseURL: "http://localhost:8000",
});

export default apiConnect;
