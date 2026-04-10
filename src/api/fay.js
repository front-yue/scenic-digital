import { fayRequest } from '../utils/request';

/**
 * 开启 Fay 直播
 * @returns {Promise<{result: string}>}
 */
export function startFayLive() {
  return fayRequest({
    url: '/api/start-live',
    method: 'post', // 假设后端使用 GET 请求，如果是 POST 请修改
  });
}

/**
 * 关闭 Fay 直播
 * @returns {Promise<{result: string}>}
 */
export function stopFayLive() {
  return fayRequest({
    url: '/api/stop-live',
    method: 'post', // 假设后端使用 GET 请求，如果是 POST 请修改
  });
}

/**
 * 获取 Fay 服务运行状态
 * @returns {Promise<{status: boolean}>}
 */
export function getFayStatus() {
  return fayRequest({
    url: '/api/get-run-status',
    method: 'post',
  });
}

/**
 * 获取麦克风及扬声器状态
 * @returns {Promise<{mic: boolean, speaker: boolean}>}
 */
export function getAudioConfig() {
  return fayRequest({
    url: '/api/get-audio-config',
    method: 'get',
  });
}

/**
 * 麦克风开关
 * @param {boolean} [enabled] true=开启，false=关闭；不传参数则自动切换当前状态
 * @returns {Promise<{status: string, enabled: boolean, msg: string}>}
 */
export function toggleMicrophone(enabled) {
  const data = typeof enabled === 'boolean' ? { enabled } : {};
  return fayRequest({
    url: '/api/toggle-microphone',
    method: 'post',
    data,
  });
}
