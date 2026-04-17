import { scenicRequest } from '@/utils/request';

/**
 * 根据地名获取高德地图经纬度坐标
 * @param {string} address - 地名（如：游客中心）
 * @returns {Promise} Axios 响应对象
 */
export const getGeocode = (address) => {
  return scenicRequest({
    url: '/api/map/geocode',
    method: 'get',
    params: { address }
  });
};
