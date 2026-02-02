<template>
  <div>
    <exam-create-manual v-if="mode === 'manual'" />
    <exam-create-intelligent v-else-if="mode === 'intelligent'" />

    <div v-else class="exam-create-selection">
      <div class="selection-container">
        <h1 class="page-title">新建考试</h1>
        <p class="page-subtitle">选择创建试卷的方式</p>
        
        <div class="selection-cards">
          <div class="selection-card" @click="goToManual">
            <div class="card-icon manual">
              <i class="el-icon-edit-outline"></i>
            </div>
            <h3>手动组卷</h3>
            <p>手动添加和编辑试题，完全掌控试卷结构和内容</p>
            <ul class="feature-list">
              <li>自由添加各类题型</li>
              <li>手动设置分值和答案</li>
              <li>灵活调整题目顺序</li>
              <li>精确控制试卷难度</li>
            </ul>
          </div>
          
          <div class="selection-card" @click="goToIntelligent">
            <div class="card-icon intelligent">
              <i class="el-icon-magic-stick"></i>
            </div>
            <h3>智能组卷</h3>
            <p>根据知识点、难度等条件，从题库智能筛选组卷</p>
            <ul class="feature-list">
              <li>快速从题库选题</li>
              <li>按知识点分布组卷</li>
              <li>自动平衡试卷难度</li>
              <li>智能计算分值分布</li>
            </ul>
          </div>
        </div>
        
        <div class="back-action">
          <el-button @click="goBack">返回</el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ExamCreateManual from './ExamCreateManual.vue'
import ExamCreateIntelligent from './ExamCreateIntelligent.vue'

export default {
  name: 'ExamCreateSelection',
  components: {
    ExamCreateManual,
    ExamCreateIntelligent
  },
  computed: {
    mode() {
      return this.$route.query.mode
    }
  },
  methods: {
    goToManual() {
      this.$router.push({
        path: '/teacher/exam-create',
        query: { mode: 'manual' }
      })
    },
    goToIntelligent() {
      this.$router.push({
        path: '/teacher/exam-create',
        query: { mode: 'intelligent' }
      })
    },
    goBack() {
      if (this.mode) {
        this.$router.replace('/teacher/exam-create')
        return
      }
      this.$router.back()
    }
  }
}
</script>

<style scoped lang="scss">
.exam-create-selection {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
}

.selection-container {
  max-width: 1100px;
  width: 100%;
}

.page-title {
  text-align: center;
  font-size: 36px;
  font-weight: 700;
  color: white;
  margin: 0 0 12px 0;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.page-subtitle {
  text-align: center;
  font-size: 16px;
  color: rgba(255, 255, 255, 0.9);
  margin: 0 0 50px 0;
}

.selection-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 30px;
  margin-bottom: 40px;
}

.selection-card {
  background: white;
  border-radius: 16px;
  padding: 40px 30px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  
  &:hover {
    transform: translateY(-8px);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
  }
  
  .card-icon {
    width: 80px;
    height: 80px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 24px;
    
    i {
      font-size: 40px;
      color: white;
    }
    
    &.manual {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    &.intelligent {
      background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    }
  }
  
  h3 {
    text-align: center;
    font-size: 24px;
    font-weight: 600;
    color: #303133;
    margin: 0 0 12px 0;
  }
  
  > p {
    text-align: center;
    font-size: 14px;
    color: #909399;
    margin: 0 0 24px 0;
    line-height: 1.6;
  }
  
  .feature-list {
    list-style: none;
    padding: 0;
    margin: 0;
    
    li {
      font-size: 14px;
      color: #606266;
      padding: 8px 0;
      padding-left: 24px;
      position: relative;
      
      &:before {
        content: '✓';
        position: absolute;
        left: 0;
        color: #67c23a;
        font-weight: bold;
      }
    }
  }
}

.back-action {
  text-align: center;
  
  .el-button {
    background: white;
    border-color: white;
    color: #667eea;
    padding: 12px 40px;
    font-size: 14px;
    
    &:hover {
      background: rgba(255, 255, 255, 0.9);
    }
  }
}

@media (max-width: 768px) {
  .selection-cards {
    grid-template-columns: 1fr;
  }
}
</style>
