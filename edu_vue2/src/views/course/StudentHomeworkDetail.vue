<template>
  <div class="student-homework-detail">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-left">
        <el-button icon="el-icon-arrow-left" @click="goBack">返回课程</el-button>
        <div class="homework-info">
          <h1>{{ homework.name }}</h1>
          <div class="meta-info">
            <span class="question-count"><i class="el-icon-edit"></i> 共{{ homework.questions.length }}题</span>
            <span class="divider">|</span>
            <span><i class="el-icon-time"></i> 开始：{{ homework.startTime }}</span>
            <span class="divider">|</span>
            <span><i class="el-icon-time"></i> 截止：{{ homework.endTime }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 主体内容 -->
    <div class="homework-container">
      <!-- 中间：作业题目（可滚动） -->
      <div class="homework-wrapper">
        <main class="homework-content">
          <div 
            v-for="(question, index) in homework.questions" 
            :key="index" 
            :id="'question-' + index"
            class="question-block"
          >
            <div class="question-header">
              <span class="question-number">第 {{ index + 1 }} 题</span>
              <span class="question-type">{{ getQuestionType(question.type) }}</span>
              <span v-if="question.score" class="question-score">({{ question.score }}分)</span>
            </div>
            <div class="question-text">{{ question.text }}</div>
            
            <!-- 答题区域 -->
            <div class="answer-area">
              <el-input
                v-if="homework.status !== '已批改' && homework.status !== '已提交'"
                v-model="answers[index]"
                type="textarea"
                :rows="8"
                placeholder="请输入你的答案..."
              />
              <div v-else class="submitted-answer">
                <div class="answer-label">我的答案：</div>
                <div class="answer-content">{{ answers[index] || '未作答' }}</div>
              </div>
            </div>

            <!-- 批改结果 -->
            <div v-if="homework.status === '已批改' && question.teacherComment" class="teacher-comment">
              <div class="comment-label">教师评语：</div>
              <div class="comment-content">{{ question.teacherComment }}</div>
            </div>
          </div>
        </main>
      </div>

      <!-- 右侧：答题卡（固定） -->
      <aside class="question-nav">
        <div class="nav-header">
          <h3>答题卡</h3>
          <div class="progress-info">{{ answeredCount }}/{{ homework.questions.length }}</div>
        </div>
        
        <!-- 操作按钮 -->
        <div class="action-buttons" v-if="homework.status === '未提交'">
          <el-button 
            @click="saveDraft"
            size="medium"
            style="width: 100%"
          >
            保存草稿
          </el-button>
          <el-button 
            type="primary" 
            @click="submitHomework"
            size="medium"
            style="width: 100%; margin-top: 0.5rem;"
          >
            提交作业
          </el-button>
        </div>
        <div class="status-display" v-else>
          <el-tag v-if="homework.status === '已批改'" type="success" size="large" style="width: 100%; justify-content: center;">{{ homework.status }}</el-tag>
          <el-tag v-else-if="homework.status === '已提交'" type="info" size="large" style="width: 100%; justify-content: center;">{{ homework.status }}</el-tag>
        </div>
        
        <!-- 题型分类 -->
        <div v-if="questionTypeGroups.length > 1" class="type-groups">
          <div v-for="group in questionTypeGroups" :key="group.type" class="type-group">
            <div class="type-label">{{ group.label }}</div>
            <div class="question-grid">
              <div
                v-for="index in group.indices"
                :key="index"
                :class="['question-square', { 
                  answered: answers[index] && answers[index].trim() !== ''
                }]"
                @click="scrollToQuestion(index)"
              >
                {{ index + 1 }}
              </div>
            </div>
          </div>
        </div>

        <!-- 无分类情况 -->
        <div v-else class="question-grid">
          <div
            v-for="(question, index) in homework.questions"
            :key="index"
            :class="['question-square', { 
              answered: answers[index] && answers[index].trim() !== ''
            }]"
            @click="scrollToQuestion(index)"
          >
            {{ index + 1 }}
          </div>
        </div>

        <!-- 图例 -->
        <div class="legend">
          <div class="legend-item">
            <span class="dot answered"></span>
            <span>已答</span>
          </div>
          <div class="legend-item">
            <span class="dot"></span>
            <span>未答</span>
          </div>
        </div>
      </aside>
    </div>
  </div>
</template>

<script>
export default {
  name: 'StudentHomeworkDetail',
  data() {
    return {
      courseId: this.$route.params.courseId,
      homeworkId: this.$route.params.homeworkId,
      homework: {},
      answers: []
    }
  },
  computed: {
    answeredCount() {
      return this.answers.filter(a => a && a.trim() !== '').length
    },
    questionTypeGroups() {
      const groups = {}
      this.homework.questions.forEach((q, index) => {
        const type = q.type || 'other'
        if (!groups[type]) {
          groups[type] = {
            type: type,
            label: this.getQuestionType(type),
            indices: []
          }
        }
        groups[type].indices.push(index)
      })
      return Object.values(groups)
    }
  },
  created() {
    this.loadHomeworkData()
  },
  mounted() {
    // 禁用全局滚动
    document.body.style.overflow = 'hidden'
  },
  beforeDestroy() {
    // 恢复全局滚动
    document.body.style.overflow = ''
  },
  methods: {
    getQuestionType(type) {
      const typeMap = {
        'single': '单选题',
        'multiple': '多选题',
        'judge': '判断题',
        'blank': '填空题',
        'short': '简答题',
        'essay': '论述题',
        'other': '其他'
      }
      return typeMap[type] || '问答题'
    },

    goBack() {
      // 判断是否从作业中心进入（courseId='1'为作业中心标识）
      if (this.courseId === '1') {
        this.$router.push('/homework-center')
      } else {
        this.$router.push({
          path: `/student/course/${this.courseId}`,
          query: { tab: 'homework' }
        })
      }
    },

    loadHomeworkData() {
      // TODO: 从API加载真实数据
      // 模拟数据
      this.homework = {
        id: this.homeworkId,
        name: 'HTML基础练习',
        status: '未提交',
        startTime: '2024-01-20 09:00',
        endTime: '2024-01-27 23:59',
        description: '请认真完成以下HTML基础练习题目，巩固课堂所学知识。',
        questions: [
          {
            text: '请解释HTML5相比HTML4的主要改进有哪些？',
            score: 20,
            type: 'short'
          },
          {
            text: '请写出至少5个常用的HTML标签及其用途。',
            score: 30,
            type: 'short'
          },
          {
            text: '请描述HTML表单的基本结构，并举例说明。',
            score: 50,
            type: 'essay'
          }
        ]
      }

      // 初始化答案数组
      this.answers = new Array(this.homework.questions.length).fill('')
    },

    scrollToQuestion(index) {
      const element = document.getElementById('question-' + index)
      const container = document.querySelector('.homework-content')
      if (element && container) {
        const offsetTop = element.offsetTop - container.offsetTop - 20
        container.scrollTo({ top: offsetTop, behavior: 'smooth' })
      }
    },

    saveDraft() {
      this.$message.success('草稿已保存')
      // TODO: 调用API保存草稿
    },

    submitHomework() {
      // 检查是否所有题目都已作答
      const unanswered = this.answers.some(answer => !answer || answer.trim() === '')
      if (unanswered) {
        this.$confirm('还有题目未作答，确定要提交吗？', '提示', {
          confirmButtonText: '确定提交',
          cancelButtonText: '继续作答',
          type: 'warning'
        }).then(() => {
          this.doSubmit()
        }).catch(() => {})
      } else {
        this.$confirm('确定提交作业吗？提交后将无法修改', '提示', {
          confirmButtonText: '确定提交',
          cancelButtonText: '再检查一下',
          type: 'warning'
        }).then(() => {
          this.doSubmit()
        }).catch(() => {})
      }
    },

    doSubmit() {
      // TODO: 调用API提交作业
      this.$message.success('作业已提交')
      
      // 判断是否从作业中心进入，决定返回位置
      if (this.courseId === '1') {
        // 从作业中心进入，返回作业中心
        this.$router.push('/homework-center')
      } else {
        // 从课程详情进入，返回课程详情页
        this.$router.push({
          path: `/student/course/${this.courseId}`,
          query: { tab: 'homework' }
        })
      }
    }
  }
}
</script>

<style scoped>
.student-homework-detail {
  width: 100%;
  height: 100vh;
  background: #f9fafb;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.page-header {
  background: white;
  padding: 1.25rem 2rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-shrink: 0;
  z-index: 100;
  min-height: 80px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  flex: 1;
}

.homework-info {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.homework-info h1 {
  margin: 0;
  font-size: 1.3rem;
  color: #1f2937;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.meta-info {
  display: flex;
  align-items: center;
  gap: 1rem;
  font-size: 0.875rem;
  color: #6b7280;
}

.meta-info i {
  margin-right: 0.25rem;
}

.meta-info .question-count {
  color: #667eea;
  font-weight: 600;
}

.meta-info .divider {
  color: #d1d5db;
}

.homework-container {
  flex: 1;
  display: flex;
  gap: 1rem;
  padding: 1rem;
  min-height: 0;
  overflow: hidden;
}

/* 中间：内容包装器 */
.homework-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

/* 中间：题目区域 */
.homework-content {
  flex: 1;
  background: white;
  border-radius: 8px;
  padding: 2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  overflow-y: auto;
}

.question-block {
  margin-bottom: 3rem;
  padding: 1.5rem;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  transition: all 0.3s;
  scroll-margin-top: 1rem;
}

.question-block:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.question-block:last-child {
  margin-bottom: 0;
}

.question-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
  padding-bottom: 0.75rem;
  border-bottom: 2px solid #667eea;
}

.question-number {
  font-weight: 700;
  color: #1f2937;
  font-size: 1.125rem;
}

.question-type {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  font-size: 0.75rem;
  border-radius: 12px;
  font-weight: 500;
}

.question-score {
  color: #667eea;
  font-weight: 600;
  font-size: 1rem;
}

.question-text {
  color: #374151;
  line-height: 1.8;
  margin-bottom: 1.5rem;
  font-size: 1rem;
}

.answer-area {
  margin-top: 1rem;
}

.submitted-answer {
  padding: 1rem;
  background: #f9fafb;
  border-radius: 6px;
}

.answer-label {
  font-weight: 600;
  color: #6b7280;
  margin-bottom: 0.5rem;
  font-size: 0.875rem;
}

.answer-content {
  color: #1f2937;
  line-height: 1.6;
  white-space: pre-wrap;
}

.teacher-comment {
  margin-top: 1rem;
  padding: 1rem;
  background: #fef3c7;
  border-radius: 6px;
  border-left: 4px solid #f59e0b;
}

.comment-label {
  font-weight: 600;
  color: #92400e;
  margin-bottom: 0.5rem;
  font-size: 0.875rem;
}

.comment-content {
  color: #78350f;
  line-height: 1.6;
}

/* 右侧：题目导航 */
.question-nav {
  width: 300px;
  flex-shrink: 0;
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  display: flex;
  flex-direction: column;
  height: 100%;
  overflow: hidden;
}

.nav-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
  padding-bottom: 0.75rem;
  border-bottom: 2px solid #667eea;
  flex-shrink: 0;
}

.nav-header h3 {
  margin: 0;
  font-size: 1rem;
  color: #1f2937;
  font-weight: 600;
}

.progress-info {
  color: #667eea;
  font-weight: 700;
  font-size: 1rem;
}

/* 操作按钮区域 */
.action-buttons {
  margin-bottom: 0.75rem;
  flex-shrink: 0;
}

.status-display {
  margin-bottom: 0.75rem;
  flex-shrink: 0;
}

.nav-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem;
  border-radius: 6px;
  background: #f9fafb;
  cursor: pointer;
  transition: all 0.2s;
  border: 2px solid transparent;
}

.nav-item:hover {
  background: #f3f4f6;
  border-color: #667eea;
}

.nav-item.answered {
  background: #d1fae5;
  border-color: #10b981;
}

.nav-item.answered .item-number {
  background: #10b981;
  color: white;
}

.item-number {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: #e5e7eb;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 0.875rem;
  color: #6b7280;
  flex-shrink: 0;
}

.item-label {
  flex: 1;
  font-size: 0.875rem;
  color: #374151;
  font-weight: 500;
}

/* 题型分类 */
.type-groups {
  flex: 1;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding-right: 0.5rem;
}

.type-group {
  display: flex;
  flex-direction: column;
  gap: 0.625rem;
}

.type-label {
  font-size: 0.8125rem;
  color: #6b7280;
  font-weight: 600;
  padding-bottom: 0.375rem;
  border-bottom: 1px solid #e5e7eb;
  flex-shrink: 0;
}

/* 题目方块网格 */
.question-grid {
  flex: 1;
  overflow-y: auto;
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 0.5rem;
  padding-right: 0.5rem;
  align-content: start;
}

.question-square {
  width: 100%;
  aspect-ratio: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  background: white;
  border: 2px solid #d1d5db;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.875rem;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.2s;
}

.question-square:hover {
  border-color: #667eea;
  background: #f3f4ff;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(102, 126, 234, 0.15);
}

.question-square.answered {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-color: #667eea;
  color: white;
}

.question-square.answered:hover {
  background: linear-gradient(135deg, #5568d3 0%, #64408a 100%);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

/* 图例 */
.legend {
  margin-top: 0.75rem;
  padding-top: 0.75rem;
  border-top: 1px solid #e5e7eb;
  display: flex;
  gap: 1rem;
  flex-shrink: 0;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  font-size: 0.8125rem;
  color: #6b7280;
}

.legend-item .dot {
  width: 16px;
  height: 16px;
  border: 2px solid #d1d5db;
  border-radius: 3px;
  background: white;
}

.legend-item .dot.answered {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-color: #667eea;
}


</style>
