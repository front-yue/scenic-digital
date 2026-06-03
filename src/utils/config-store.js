/**
 * 客户端配置管理工具
 *
 * 优先级：localStorage 用户配置 > .env 环境变量 > 空字符串
 * 用户通过 ConfigPanel 填写的配置会持久化到 localStorage，
 * 下次加载时自动使用，无需修改 .env 文件。
 */

const STORAGE_KEY = 'scenic_digital_user_config'

// 配置项定义（分组 + 元信息）
export const CONFIG_SCHEMA = [
  {
    group: '数字人配置',
    key: 'xmov',
    description: '魔珐星云 3D 数字人 SDK 凭证，用于驱动虚拟形象',
    fields: [
      {
        key: 'VITE_XMOV_APP_ID',
        label: 'App ID',
        placeholder: '请输入魔珐星云 App ID',
        envDefault: () => import.meta.env.VITE_XMOV_APP_ID || ''
      },
      {
        key: 'VITE_XMOV_APP_SECRET',
        label: 'App Secret',
        placeholder: '请输入魔珐星云 App Secret',
        envDefault: () => import.meta.env.VITE_XMOV_APP_SECRET || '',
        type: 'password'
      }
    ]
  },
  {
    group: '地图配置',
    key: 'amap',
    description: '高德地图 Web JS API 密钥，用于景区导航雷达',
    fields: [
      {
        key: 'VITE_AMAP_KEY',
        label: 'API Key',
        placeholder: '请输入高德地图 Key',
        envDefault: () => import.meta.env.VITE_AMAP_KEY || ''
      },
      {
        key: 'VITE_AMAP_SECURITY_CODE',
        label: 'Security Code',
        placeholder: '请输入高德地图安全密钥',
        envDefault: () => import.meta.env.VITE_AMAP_SECURITY_CODE || ''
      }
    ]
  },
  {
    group: '服务地址',
    key: 'services',
    description: '后端 API 服务地址，本地开发时使用默认值即可',
    fields: [
      {
        key: 'VITE_FAY_API_BASE_URL',
        label: 'Fay 服务地址',
        placeholder: 'http://127.0.0.1:5000',
        envDefault: () => import.meta.env.VITE_FAY_API_BASE_URL || ''
      },
      {
        key: 'VITE_SCENIC_API_BASE_URL',
        label: '文旅后端地址',
        placeholder: 'http://127.0.0.1:8888',
        envDefault: () => import.meta.env.VITE_SCENIC_API_BASE_URL || ''
      }
    ]
  }
]

/**
 * 从 localStorage 读取用户配置
 */
function loadUserConfig() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    return raw ? JSON.parse(raw) : {}
  } catch {
    return {}
  }
}

/**
 * 保存用户配置到 localStorage
 */
function saveUserConfig(config) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(config))
}

/**
 * 获取单个配置值（localStorage 优先 > .env 默认值）
 * @param {string} key - 配置键名，如 'VITE_XMOV_APP_ID'
 * @returns {string}
 */
export function getConfigValue(key) {
  const userConfig = loadUserConfig()
  if (userConfig[key] !== undefined && userConfig[key] !== '') {
    return userConfig[key]
  }
  // 从 schema 中找到 envDefault
  for (const group of CONFIG_SCHEMA) {
    for (const field of group.fields) {
      if (field.key === key) {
        return field.envDefault()
      }
    }
  }
  return ''
}

/**
 * 批量获取所有配置的当前值（用于 ConfigPanel 显示）
 * @returns {Object} { [key]: { value, source } }
 *   source: 'user' 表示用户填写, 'env' 表示环境变量默认值, 'empty' 表示未配置
 */
export function getAllConfigValues() {
  const userConfig = loadUserConfig()
  const result = {}

  for (const group of CONFIG_SCHEMA) {
    for (const field of group.fields) {
      const userValue = userConfig[field.key]
      const envValue = field.envDefault()

      if (userValue !== undefined && userValue !== '') {
        result[field.key] = { value: userValue, source: 'user' }
      } else if (envValue) {
        result[field.key] = { value: envValue, source: 'env' }
      } else {
        result[field.key] = { value: '', source: 'empty' }
      }
    }
  }

  return result
}

/**
 * 保存配置（仅保存用户修改过的值，空值不写入）
 * @param {Object} values - { [key]: value }
 */
export function saveConfigValues(values) {
  const config = {}
  for (const [key, value] of Object.entries(values)) {
    if (value && value.trim()) {
      config[key] = value.trim()
    }
  }
  saveUserConfig(config)
}

/**
 * 清除所有用户配置（恢复 .env 默认值）
 */
export function clearUserConfig() {
  localStorage.removeItem(STORAGE_KEY)
}

/**
 * 检查关键配置是否已就绪
 * @param {string[]} keys - 需要检查的配置键列表
 * @returns {{ ready: boolean, missing: string[] }}
 */
export function checkConfigReady(keys) {
  const missing = []
  for (const key of keys) {
    const value = getConfigValue(key)
    if (!value) missing.push(key)
  }
  return { ready: missing.length === 0, missing }
}
