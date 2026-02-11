/**
 * API 测试工具
 * 用于测试后端接口是否正常工作
 * 在浏览器控制台运行: window.testAPI.testLogin()
 */

import { authAPI, userAPI } from '@/api'

const testAPI = {
  /**
   * 测试登录接口
   */
  async testLogin(email = 'test@example.com', password = 'password123') {
    console.log('🧪 测试登录接口...')
    console.log('请求参数:', { email, password })
    
    try {
      const response = await authAPI.login({ email, password })
      console.log('✅ 登录成功!')
      console.log('响应数据:', response)
      return response
    } catch (error) {
      console.error('❌ 登录失败!')
      console.error('错误信息:', error.response?.data || error.message)
      throw error
    }
  },

  /**
   * 测试注册接口
   */
  async testRegister(data = {
    username: '测试用户',
    email: 'newuser@example.com',
    password: 'password123',
    password_confirm: 'password123',
    role: 'student'
  }) {
    console.log('🧪 测试注册接口...')
    console.log('请求参数:', data)
    
    try {
      const response = await authAPI.register(data)
      console.log('✅ 注册成功!')
      console.log('响应数据:', response)
      return response
    } catch (error) {
      console.error('❌ 注册失败!')
      console.error('错误信息:', error.response?.data || error.message)
      throw error
    }
  },

  /**
   * 测试获取当前用户信息
   */
  async testGetCurrentUser() {
    console.log('🧪 测试获取当前用户信息...')
    
    try {
      const response = await authAPI.getCurrentUser()
      console.log('✅ 获取成功!')
      console.log('用户信息:', response)
      return response
    } catch (error) {
      console.error('❌ 获取失败!')
      console.error('错误信息:', error.response?.data || error.message)
      throw error
    }
  },

  /**
   * 测试忘记密码
   */
  async testForgetPassword(email = 'test@example.com') {
    console.log('🧪 测试忘记密码接口...')
    console.log('请求参数:', { email })
    
    try {
      const response = await authAPI.forgetPassword({ email })
      console.log('✅ 邮件发送成功!')
      console.log('响应数据:', response)
      return response
    } catch (error) {
      console.error('❌ 邮件发送失败!')
      console.error('错误信息:', error.response?.data || error.message)
      throw error
    }
  },

  /**
   * 测试更新用户信息
   */
  async testUpdateProfile(data = { username: '更新后的名字', bio: '这是个人简介' }) {
    console.log('🧪 测试更新用户信息...')
    console.log('请求参数:', data)
    
    try {
      const response = await userAPI.updateUserInfo(data)
      console.log('✅ 更新成功!')
      console.log('响应数据:', response)
      return response
    } catch (error) {
      console.error('❌ 更新失败!')
      console.error('错误信息:', error.response?.data || error.message)
      throw error
    }
  },

  /**
   * 测试完整的登录流程
   */
  async testFullLoginFlow(email = 'test@example.com', password = 'password123') {
    console.log('🧪 开始完整登录流程测试...\n')
    
    try {
      // 1. 登录
      console.log('步骤 1: 登录')
      const loginResponse = await this.testLogin(email, password)
      
      // 2. 获取当前用户信息
      console.log('\n步骤 2: 获取当前用户信息')
      const userInfo = await this.testGetCurrentUser()
      
      // 3. 更新用户信息
      console.log('\n步骤 3: 更新用户信息')
      await this.testUpdateProfile({ bio: '测试更新于 ' + new Date().toLocaleString() })
      
      console.log('\n✅ 完整流程测试通过!')
      return { loginResponse, userInfo }
    } catch (error) {
      console.error('\n❌ 流程测试失败!')
      throw error
    }
  },

  /**
   * 检查后端连接状态
   */
  async checkBackendStatus() {
    console.log('🧪 检查后端连接状态...')
    const baseURL = process.env.VUE_APP_API_URL || 'http://localhost:8000/api'
    console.log('API 地址:', baseURL)
    
    try {
      const response = await fetch(baseURL)
      console.log('✅ 后端服务正常运行!')
      console.log('状态码:', response.status)
      return true
    } catch (error) {
      console.error('❌ 无法连接到后端服务!')
      console.error('错误:', error.message)
      console.log('请确保后端服务已启动: python manage.py runserver')
      return false
    }
  }
}

// 将测试工具挂载到 window 对象，方便在控制台调用
if (typeof window !== 'undefined') {
  window.testAPI = testAPI
}

export default testAPI
