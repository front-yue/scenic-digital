import request from '../utils/request';

/**
 * 开启 Fay 直播
 * @returns {Promise<{result: string}>}
 */
export function startFayLive() {
  return request({
    url: '/api/start-live',
    method: 'post', // 假设后端使用 GET 请求，如果是 POST 请修改
  });
}

/**
 * 关闭 Fay 直播
 * @returns {Promise<{result: string}>}
 */
export function stopFayLive() {
  return request({
    url: '/api/stop-live',
    method: 'post', // 假设后端使用 GET 请求，如果是 POST 请修改
  });
}

/**
 * 获取 Fay 服务运行状态
 * @returns {Promise<{status: boolean}>}
 */
export function getFayStatus() {
  return request({
    url: '/api/get-run-status',
    method: 'post',
  });
}
