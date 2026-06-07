export const API_BASE_URL = 'http://127.0.0.1:8003'

export const REQUEST_TIMEOUT_MS = 35000

export function optimizePrompt(payload) {
  return new Promise((resolve, reject) => {
    uni.request({
      url: `${API_BASE_URL}/api/prompt/optimize`,
      method: 'POST',
      header: {
        'Content-Type': 'application/json',
      },
      data: payload,
      timeout: REQUEST_TIMEOUT_MS,
      success: (res) => {
        if (res.statusCode >= 200 && res.statusCode < 300 && res.data) {
          resolve(res.data)
          return
        }
        reject(new Error('request_failed'))
      },
      fail: () => {
        reject(new Error('network_failed'))
      },
    })
  })
}
