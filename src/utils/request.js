import axios from 'axios';

// ================= Fay 原核心服务请求实例 (5000端口) =================
export const fayRequest = axios.create({
  baseURL: import.meta.env.VITE_FAY_API_BASE_URL,
  timeout: 10000,
});

// 请求拦截器
fayRequest.interceptors.request.use(
  (config) => config,
  (error) => Promise.reject(error)
);

// 响应拦截器
fayRequest.interceptors.response.use(
  (response) => response.data,
  (error) => Promise.reject(error)
);

// ================= 智慧文旅数据服务请求实例 (8888端口) =================
export const scenicRequest = axios.create({
  baseURL: import.meta.env.VITE_SCENIC_API_BASE_URL,
  timeout: 10000,
});

// 请求拦截器
scenicRequest.interceptors.request.use(
  (config) => config,
  (error) => Promise.reject(error)
);

// 响应拦截器
scenicRequest.interceptors.response.use(
  (response) => response.data,
  (error) => Promise.reject(error)
);