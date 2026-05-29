import { scenicRequest } from '../utils/request';

/**
 * 获取所有系统配置
 */
export const getAllConfig = () => {
  return scenicRequest({
    url: '/api/config/',
    method: 'get'
  });
};

/**
 * 获取单个系统配置
 * @param {String} key 配置键名
 */
export const getConfig = (key) => {
  return scenicRequest({
    url: `/api/config/${key}`,
    method: 'get'
  });
};

/**
 * 更新系统配置
 * @param {String} key 配置键名
 * @param {String} value 配置值
 */
export const updateConfig = (key, value) => {
  return scenicRequest({
    url: `/api/config/${key}`,
    method: 'put',
    data: { value }
  });
};
