<template>
  <div class="messages-container">
    <div class="page-header">
      <h1>💬 消息中心</h1>
      <p class="subtitle">查看系统通知和消息</p>
    </div>

    <!-- 消息列表 -->
    <div class="messages-content">
      <el-tabs v-model="activeTab" type="card">
        <el-tab-pane label="系统通知" name="system">
          <div class="messages-list">
            <div v-for="msg in systemMessages" :key="msg.id" class="message-card" :class="{ unread: !msg.read }">
              <div class="message-icon">
                <i class="el-icon-bell"></i>
              </div>
              <div class="message-content">
                <h3>{{ msg.title }}</h3>
                <p>{{ msg.content }}</p>
                <span class="message-time">{{ msg.time }}</span>
              </div>
              <div class="message-actions">
                <el-button v-if="!msg.read" type="text" size="small" @click="markAsRead(msg.id)">
                  标记已读
                </el-button>
              </div>
            </div>
          </div>
        </el-tab-pane>

        <el-tab-pane label="课程消息" name="course">
          <div class="messages-list">
            <div v-for="msg in courseMessages" :key="msg.id" class="message-card" :class="{ unread: !msg.read }">
              <div class="message-icon course">
                <i class="el-icon-notebook-2"></i>
              </div>
              <div class="message-content">
                <h3>{{ msg.title }}</h3>
                <p>{{ msg.content }}</p>
                <span class="message-time">{{ msg.time }}</span>
              </div>
              <div class="message-actions">
                <el-button v-if="!msg.read" type="text" size="small" @click="markAsRead(msg.id)">
                  标记已读
                </el-button>
              </div>
            </div>
          </div>
        </el-tab-pane>

        <el-tab-pane label="作业消息" name="homework">
          <div class="messages-list">
            <div v-for="msg in homeworkMessages" :key="msg.id" class="message-card" :class="{ unread: !msg.read }">
              <div class="message-icon homework">
                <i class="el-icon-document"></i>
              </div>
              <div class="message-content">
                <h3>{{ msg.title }}</h3>
                <p>{{ msg.content }}</p>
                <span class="message-time">{{ msg.time }}</span>
              </div>
              <div class="message-actions">
                <el-button v-if="!msg.read" type="text" size="small" @click="markAsRead(msg.id)">
                  标记已读
                </el-button>
              </div>
            </div>
          </div>
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>

<script>
export default {
  name: 'MessageCenter',
  data() {
    return {
      activeTab: 'system',
      systemMessages: [
        {
          id: 1,
          title: '欢迎来到 EduMaster',
          content: '感谢您注册 EduMaster 在线教育平台！开始您的学习之旅吧。',
          time: '2024-01-26 10:00',
          read: false
        },
        {
          id: 2,
          title: '系统升级通知',
          content: '系统将于今晚22:00-24:00进行维护升级，期间可能无法访问，请合理安排学习时间。',
          time: '2024-01-25 15:30',
          read: true
        }
      ],
      courseMessages: [
        {
          id: 3,
          title: 'Vue.js 课程更新',
          content: '您学习的《Vue.js 从入门到精通》课程新增了第10章内容，快去学习吧！',
          time: '2024-01-26 09:15',
          read: false
        },
        {
          id: 4,
          title: '课程直播提醒',
          content: '《React 现代实战指南》将于今晚19:00开始直播答疑，请准时参加。',
          time: '2024-01-25 18:00',
          read: true
        }
      ],
      homeworkMessages: [
        {
          id: 5,
          title: '作业批改完成',
          content: '您提交的《HTML基础练习》作业已批改完成，得分：85分，快去查看老师评语吧！',
          time: '2024-01-26 08:30',
          read: false
        },
        {
          id: 6,
          title: '作业提交提醒',
          content: '《第三周练习题》将于明天23:59截止提交，请及时完成。',
          time: '2024-01-25 20:00',
          read: false
        }
      ]
    }
  },
  methods: {
    markAsRead(id) {
      // 查找并标记为已读
      let message = null
      if (this.activeTab === 'system') {
        message = this.systemMessages.find(m => m.id === id)
      } else if (this.activeTab === 'course') {
        message = this.courseMessages.find(m => m.id === id)
      } else if (this.activeTab === 'homework') {
        message = this.homeworkMessages.find(m => m.id === id)
      }
      
      if (message) {
        message.read = true
        this.$message.success('已标记为已读')
      }
    }
  }
}
</script>

<style scoped lang="scss">
.messages-container {
  padding: 1.5rem;
  background: #f9fafb;
  min-height: 100vh;
}

.page-header {
  margin-bottom: 1rem;
  text-align: center;
  padding: 0.8rem 1rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 8px;
  color: white;
  box-shadow: 0 2px 6px rgba(102, 126, 234, 0.2);

  h1 {
    margin: 0;
    font-size: 1.25rem;
    font-weight: 700;
  }

  .subtitle {
    margin: 0.25rem 0 0 0;
    color: rgba(255, 255, 255, 0.9);
    font-size: 0.875rem;
  }
}

.messages-content {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.messages-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-top: 1rem;
}

.message-card {
  display: flex;
  gap: 1rem;
  padding: 1.25rem;
  background: #f9fafb;
  border-radius: 8px;
  border-left: 4px solid transparent;
  transition: all 0.3s;

  &.unread {
    background: #f0f4ff;
    border-left-color: #667eea;
    box-shadow: 0 2px 8px rgba(102, 126, 234, 0.1);
  }

  &:hover {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    transform: translateY(-2px);
  }
}

.message-icon {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;

  i {
    font-size: 1.5rem;
    color: white;
  }

  &.course {
    background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
  }

  &.homework {
    background: linear-gradient(135deg, #27ae60 0%, #229954 100%);
  }
}

.message-content {
  flex: 1;

  h3 {
    margin: 0 0 0.5rem 0;
    font-size: 1rem;
    color: #1f2937;
    font-weight: 600;
  }

  p {
    margin: 0 0 0.5rem 0;
    font-size: 0.875rem;
    color: #6b7280;
    line-height: 1.5;
  }

  .message-time {
    font-size: 0.75rem;
    color: #9ca3af;
  }
}

.message-actions {
  display: flex;
  align-items: center;
}
</style>
