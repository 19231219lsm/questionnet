import axios from 'axios'

export function request(config) {
    const instance = axios.create({
        baseURL: 'http://localhost:8000',
        //baseURL: 'http://39.104.170.158:8000',
        //向后端请求的目标地址（服务器地址）
        //本地测试用
        timeout: 5000
        //响应时间：单位为毫秒
    })
    instance.defaults.withCredentials = true
    return instance(config);
}