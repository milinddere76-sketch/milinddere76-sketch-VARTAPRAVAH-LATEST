import axios from "axios";

const api = axios.create({
  baseURL: "http://157.180.24.243:8000",
});

export default api;
