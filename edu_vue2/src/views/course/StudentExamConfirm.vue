<template>
  <div class="exam-confirm-page">
    <div class="confirm-container">
      <div class="confirm-card">
        <h1 class="page-title">考试</h1>
        
        <!-- 考试信息表格 -->
        <div class="info-table">
          <div class="info-row">
            <div class="info-label">考试名称</div>
            <div class="info-value">{{ exam.name }}</div>
          </div>
          <div class="info-row">
            <div class="info-label">考试时长（分钟）</div>
            <div class="info-value">{{ exam.duration }}分钟</div>
          </div>
          <div class="info-row">
            <div class="info-label">考试时间</div>
            <div class="info-value">{{ exam.startTime }} 至 {{ exam.endTime }}</div>
          </div>
        </div>

        <!-- 考试说明 -->
        <div class="exam-instructions">
          <h3>考试说明：</h3>
          <ol>
            <li>离开或退出考试页面答题时不停止，请勿要中途离开考试界面。</li>
            <li>保持座位前的桌面干净，不要有与考试无关的内容。</li>
            <li>考试时间截止或答题时间结束，如果处于答题页面，将自动提交交卷。</li>
            <li>考试过程中如果出现页面卡死，题目空白情况，请尝试刷新网页或退出重新进入考试。</li>
          </ol>
        </div>

        <!-- 同意条款和按钮 -->
        <div class="confirm-actions">
          <label class="agreement-checkbox">
            <input type="checkbox" v-model="agreed" />
            <span>我已阅读并同意</span>
          </label>
          <button 
            class="start-exam-btn" 
            :disabled="!agreed"
            @click="startExam"
          >
            进入考试
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'StudentExamConfirm',
  data() {
    return {
      courseId: this.$route.params.courseId,
      examId: this.$route.params.examId,
      agreed: false,
      exam: {
        name: '',
        duration: 0,
        startTime: '',
        endTime: ''
      }
    }
  },
  created() {
    this.loadExamInfo()
  },
  methods: {
    loadExamInfo() {
      // TODO: 从API加载考试信息
      // 模拟数据
      this.exam = {
        name: '新建试卷20260115155523',
        duration: 60,
        startTime: '01-25 17:09',
        endTime: '01-28 17:09'
      }
    },
    
    startExam() {
      if (!this.agreed) {
        this.$message.warning('请先阅读并同意考试说明')
        return
      }
      
      // 跳转到考试答题页面
      // 兼容从课程详情页和考试中心进入的情况
      this.$router.push({
        path: `/student/course/${this.courseId || '1'}/exam/${this.examId}/answer`
      })
    }
  }
}
</script>

<style scoped>
.exam-confirm-page {
  min-height: 100vh;
  background: #f5f7fa;
  padding: 2rem;
  display: flex;
  justify-content: center;
  align-items: flex-start;
}

.confirm-container {
  width: 100%;
  max-width: 960px;
  margin: 0 auto;
}

.confirm-card {
  background: white;
  border-radius: 8px;
  padding: 3rem;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.page-title {
  text-align: center;
  font-size: 2rem;
  color: #2c3e50;
  margin: 0 0 2.5rem 0;
  font-weight: 600;
}

/* 信息表格 */
.info-table {
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  overflow: hidden;
  margin-bottom: 2rem;
}

.info-row {
  display: flex;
  border-bottom: 1px solid #e5e7eb;
}

.info-row:last-child {
  border-bottom: none;
}

.info-label {
  width: 200px;
  padding: 1rem 1.5rem;
  background: #f9fafb;
  color: #6b7280;
  font-weight: 500;
  border-right: 1px solid #e5e7eb;
}

.info-value {
  flex: 1;
  padding: 1rem 1.5rem;
  color: #1f2937;
  font-weight: 500;
}

/* 考试说明 */
.exam-instructions {
  background: #fffbeb;
  border: 1px solid #fbbf24;
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 2rem;
}

.exam-instructions h3 {
  margin: 0 0 1rem 0;
  color: #92400e;
  font-size: 1rem;
  font-weight: 600;
}

.exam-instructions ol {
  margin: 0;
  padding-left: 1.5rem;
  color: #78350f;
  line-height: 1.8;
}

.exam-instructions li {
  margin-bottom: 0.5rem;
}

/* 底部操作区 */
.confirm-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 2rem;
  border-top: 1px solid #e5e7eb;
}

.agreement-checkbox {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  user-select: none;
}

.agreement-checkbox input[type="checkbox"] {
  width: 18px;
  height: 18px;
  cursor: pointer;
}

.agreement-checkbox span {
  color: #4b5563;
  font-size: 0.9375rem;
}

.start-exam-btn {
  padding: 0.75rem 3rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.start-exam-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.start-exam-btn:disabled {
  background: #d1d5db;
  cursor: not-allowed;
  opacity: 0.6;
}

/* 响应式 */
@media (max-width: 768px) {
  .exam-confirm-page {
    padding: 1rem;
  }
  
  .confirm-card {
    padding: 1.5rem;
  }
  
  .info-label {
    width: 150px;
    padding: 0.75rem 1rem;
  }
  
  .info-value {
    padding: 0.75rem 1rem;
  }
  
  .confirm-actions {
    flex-direction: column;
    gap: 1.5rem;
    align-items: stretch;
  }
  
  .start-exam-btn {
    width: 100%;
  }
}
</style>
