import { scenicRequest } from '../utils/request';

// =================== 景区基础信息 API ===================

/**
 * 获取景区基础信息
 */
export const getScenicInfo = () => {
  return scenicRequest({
    url: '/api/scenic/info',
    method: 'get'
  });
};

/**
 * 更新景区基础信息
 * @param {Number} id 景区ID
 * @param {Object} data 景区数据对象
 */
export const updateScenicInfo = (id, data) => {
  return scenicRequest({
    url: `/api/scenic/info/${id}`,
    method: 'put',
    data
  });
};


// =================== 景点列表与客流 API ===================

/**
 * 获取所有景点列表及其客流状态
 */
export const getScenicSpots = () => {
  return scenicRequest({
    url: '/api/scenic/spots',
    method: 'get'
  });
};

/**
 * 新增景点
 * @param {Object} data 景点数据对象
 */
export const addScenicSpot = (data) => {
  return scenicRequest({
    url: '/api/scenic/spots',
    method: 'post',
    data
  });
};

/**
 * 更新景点信息
 * @param {Number} id 景点ID
 * @param {Object} data 景点数据对象
 */
export const updateScenicSpot = (id, data) => {
  return scenicRequest({
    url: `/api/scenic/spots/${id}`,
    method: 'put',
    data
  });
};

/**
 * 删除景点
 * @param {Number} id 景点ID
 */
export const deleteScenicSpot = (id) => {
  return scenicRequest({
    url: `/api/scenic/spots/${id}`,
    method: 'delete'
  });
};

/**
 * 更新景点当前客流 (用于演示控制)
 * @param {Number} id 景点ID
 * @param {Number} current_visitors 当前人数
 */
export const updateSpotFlow = (id, current_visitors) => {
  return scenicRequest({
    url: `/api/scenic/spots/${id}/flow`,
    method: 'put',
    data: { current_visitors }
  });
};

// =================== 文件上传 API ===================

/**
 * 上传图片
 * @param {File} file 图片文件对象
 */
export const uploadImage = (file) => {
  const formData = new FormData();
  formData.append('file', file);
  
  return scenicRequest({
    url: '/api/upload',
    method: 'post',
    data: formData,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });
};
