import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'

// 导入封装好的 http 实例
import http from '@/api/http'

Vue.config.productionTip = false

// 注册插件
Vue.use(ElementUI)

// ==================== 统一修改 Message 默认配置 ====================
const DEFAULT_DURATION = 500; // 统一设置为 0.5s

// 1. 拦截基础 Message 函数: this.$message(...)
const originalMessage = ElementUI.Message;

const newMessage = function(options) {
  if (typeof options === 'string') {
    options = { message: options };
  }
  // 注入默认时长
  options.duration = options.duration || DEFAULT_DURATION;
  return originalMessage(options);
};

// 2. 拦截快捷方法: this.$message.success/error/warning/info
['success', 'warning', 'info', 'error'].forEach(type => {
  newMessage[type] = (options) => {
    if (typeof options === 'string') {
      options = { message: options };
    }
    options.type = type;
    options.duration = options.duration || DEFAULT_DURATION;
    return originalMessage(options);
  };
});

// 3. 挂载到 Vue 原型
Vue.prototype.$message = newMessage;


// ==================== 配置全局 HTTP 请求 ====================
// 将封装好的 axios 实例挂载到 Vue 原型上
Vue.prototype.$http = http

// ==================== 开发环境测试工具 ====================
if (process.env.NODE_ENV === 'development') {
  // 引入 API 测试工具，方便在控制台测试接口
  import('@/utils/apiTest').then(module => {
    window.testAPI = module.default
    console.log('💡 开发模式：可在控制台使用 testAPI 测试接口')
    console.log('示例: testAPI.checkBackendStatus()')
    console.log('示例: testAPI.testLogin("user@example.com", "password")')
  })
}

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')