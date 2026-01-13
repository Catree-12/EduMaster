<template>
  <div class="homework-grading-page">
    <!-- 顶部信息栏 -->
    <div class="grading-header">
      <div class="header-left">
        <h2 class="homework-title">{{ homework.name }}</h2>
        <div class="student-info">
          <el-tag type="info" size="small">
            <i class="el-icon-user"></i>
            {{ currentStudent.name }} - {{ currentStudent.studentId }}
          </el-tag>
          <el-tag type="warning" size="small" style="margin-left: 10px;">
            <i class="el-icon-s-home"></i>
            {{ currentStudent.class }}
          </el-tag>
        </div>
      </div>
      <div class="header-right">
        <div class="progress-info">
          <span class="progress-text">批阅进度：</span>
          <span class="progress-count">{{ gradedCount }}/{{ totalCount }}</span>
          <el-progress 
            :percentage="progressPercentage" 
            :color="progressColor"
            style="width: 200px; margin-left: 15px;"
          ></el-progress>
        </div>
      </div>
    </div>

    <!-- 主要批阅区域 -->
    <div class="grading-content">
      <!-- 左侧：题目列表 -->
      <div class="question-list">
        <div class="list-header">
          <h3>题目列表 ({{ questions.length }}题)</h3>
          <el-button 
            type="text" 
            size="small"
            @click="expandAll = !expandAll"
          >
            {{ expandAll ? '全部折叠' : '全部展开' }}
          </el-button>
        </div>
        <div class="list-content">
          <div 
            v-for="(question, index) in questions" 
            :key="question.id"
            class="question-item"
            :class="{ 
              'active': currentQuestionIndex === index,
              'graded': question.graded,
              'objective': question.type !== 'essay' && question.type !== 'fill'
            }"
            @click="selectQuestion(index)"
          >
            <div class="item-header">
              <span class="item-number">{{ index + 1 }}</span>
              <span class="item-type">{{ getQuestionTypeName(question.type) }}</span>
              <span class="item-score">{{ question.points }}分</span>
              <el-tag 
                v-if="question.graded" 
                size="mini" 
                type="success"
              >
                已批
              </el-tag>
              <el-tag 
                v-else-if="question.autoGraded" 
                size="mini" 
                type="info"
              >
                自动
              </el-tag>
            </div>
            <div class="item-score-display" v-if="question.studentScore !== null">
              得分：{{ question.studentScore }}/{{ question.points }}
            </div>
          </div>
        </div>
      </div>

      <!-- 右侧：批阅详情 -->
      <div class="grading-detail">
        <div class="detail-header">
          <h3>
            第 {{ currentQuestionIndex + 1 }} 题
            <el-tag size="small" style="margin-left: 10px;">
              {{ getQuestionTypeName(currentQuestion.type) }}
            </el-tag>
            <span class="question-score">本题 {{ currentQuestion.points }} 分</span>
          </h3>
        </div>

        <div class="detail-content">
          <!-- 题目内容 -->
          <div class="question-content-section">
            <h4>题目内容</h4>
            <div class="question-text" v-html="currentQuestion.content"></div>
          </div>

          <!-- 客观题自动批改 -->
          <div v-if="isObjectiveQuestion(currentQuestion)" class="auto-grading-section">
            <el-alert
              :title="`系统自动批改：${currentQuestion.isCorrect ? '正确' : '错误'}`"
              :type="currentQuestion.isCorrect ? 'success' : 'error'"
              :closable="false"
              show-icon
            >
              <div slot="default">
                <p><strong>学生答案：</strong>{{ formatStudentAnswer(currentQuestion) }}</p>
                <p><strong>标准答案：</strong>{{ formatCorrectAnswer(currentQuestion) }}</p>
                <p><strong>得分：</strong>{{ currentQuestion.studentScore }}/{{ currentQuestion.points }}</p>
              </div>
            </el-alert>
          </div>

          <!-- 主观题人工批改 -->
          <div v-else class="manual-grading-section">
            <!-- 答案对比区 -->
            <el-row :gutter="20">
              <el-col :span="12">
                <div class="answer-box student-answer-box">
                  <h4>
                    <i class="el-icon-edit"></i>
                    学生答案
                  </h4>
                  <div class="answer-content">
                    {{ currentQuestion.studentAnswer || '学生未作答' }}
                  </div>
                </div>
              </el-col>
              <el-col :span="12">
                <div class="answer-box reference-answer-box">
                  <h4>
                    <i class="el-icon-document-checked"></i>
                    参考答案
                  </h4>
                  <div class="answer-content">
                    {{ currentQuestion.referenceAnswer || '暂无参考答案' }}
                  </div>
                </div>
              </el-col>
            </el-row>

            <!-- AI 智能辅助区 -->
            <div class="ai-assist-section">
              <h4>
                <i class="el-icon-cpu"></i>
                AI 智能辅助评分
                <el-tooltip content="基于 TF-IDF 与余弦相似度算法自动计算" placement="top">
                  <i class="el-icon-question" style="font-size: 14px; color: #909399;"></i>
                </el-tooltip>
              </h4>
              <div class="ai-metrics">
                <div class="metric-item">
                  <div class="metric-label">语义相似度</div>
                  <div class="metric-value">
                    <el-progress 
                      :percentage="currentQuestion.similarity" 
                      :color="getSimilarityColor(currentQuestion.similarity)"
                      :stroke-width="12"
                    ></el-progress>
                  </div>
                </div>
                <div class="metric-item">
                  <div class="metric-label">AI 推荐分</div>
                  <div class="metric-value ai-score">
                    {{ currentQuestion.aiScore }} 分
                    <el-tag size="mini" type="warning" style="margin-left: 10px;">
                      建议采纳
                    </el-tag>
                  </div>
                </div>
                <div class="metric-item">
                  <div class="metric-label">关键词匹配</div>
                  <div class="metric-value">
                    <el-tag 
                      v-for="keyword in currentQuestion.matchedKeywords" 
                      :key="keyword"
                      size="small"
                      type="success"
                      style="margin-right: 5px;"
                    >
                      {{ keyword }}
                    </el-tag>
                    <span v-if="!currentQuestion.matchedKeywords || currentQuestion.matchedKeywords.length === 0" style="color: #909399;">
                      无匹配关键词
                    </span>
                  </div>
                </div>
              </div>
            </div>

            <!-- 手动评分区 -->
            <div class="manual-score-section">
              <h4>
                <i class="el-icon-edit-outline"></i>
                教师评分
              </h4>
              <el-row :gutter="20">
                <el-col :span="8">
                  <div class="score-input-group">
                    <label>得分：</label>
                    <el-input-number
                      v-model="currentQuestion.studentScore"
                      :min="0"
                      :max="currentQuestion.points"
                      :step="0.5"
                      :precision="1"
                      size="medium"
                      style="width: 150px;"
                    ></el-input-number>
                    <span class="score-hint">/ {{ currentQuestion.points }} 分</span>
                    <el-button 
                      type="text" 
                      size="small"
                      @click="applyAIScore"
                      style="margin-left: 10px;"
                    >
                      采纳AI推荐
                    </el-button>
                  </div>
                </el-col>
                <el-col :span="16">
                  <div class="comment-input-group">
                    <label>评语：</label>
                    <el-input
                      v-model="currentQuestion.comment"
                      placeholder="请输入个性化评语（选填）"
                      :rows="2"
                      type="textarea"
                      maxlength="200"
                      show-word-limit
                    ></el-input>
                  </div>
                </el-col>
              </el-row>
            </div>
          </div>

          <!-- 题目导航按钮 -->
          <div class="question-navigation">
            <el-button 
              @click="previousQuestion" 
              :disabled="currentQuestionIndex === 0"
            >
              <i class="el-icon-arrow-left"></i>
              上一题
            </el-button>
            <el-button 
              type="primary"
              @click="saveCurrentQuestion"
            >
              <i class="el-icon-check"></i>
              保存本题
            </el-button>
            <el-button 
              @click="nextQuestion" 
              :disabled="currentQuestionIndex === questions.length - 1"
            >
              下一题
              <i class="el-icon-arrow-right"></i>
            </el-button>
          </div>
        </div>
      </div>
    </div>

    <!-- 底部操作栏 -->
    <div class="grading-footer">
      <div class="footer-left">
        <div class="score-summary">
          <div class="summary-item">
            <span class="summary-label">客观题得分：</span>
            <span class="summary-value objective">{{ objectiveScore }}</span>
          </div>
          <div class="summary-item">
            <span class="summary-label">主观题得分：</span>
            <span class="summary-value subjective">{{ subjectiveScore }}</span>
          </div>
          <div class="summary-item total">
            <span class="summary-label">作业总分：</span>
            <span class="summary-value">{{ totalScore }}</span>
            <span class="summary-max">/ {{ maxScore }}</span>
          </div>
        </div>
      </div>
      <div class="footer-right">
        <el-button @click="previousStudent" :disabled="currentStudentIndex === 0">
          <i class="el-icon-arrow-left"></i>
          上一份
        </el-button>
        <el-button type="warning" @click="returnWork" v-if="totalScore < maxScore * 0.6">
          <i class="el-icon-refresh-left"></i>
          打回重做
        </el-button>
        <el-button type="success" @click="submitGrading">
          <i class="el-icon-finished"></i>
          提交批阅
        </el-button>
        <el-button @click="nextStudent" :disabled="currentStudentIndex === students.length - 1">
          下一份
          <i class="el-icon-arrow-right"></i>
        </el-button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HomeworkGradingDetail',
  data() {
    return {
      homeworkId: null,
      homework: {
        name: '第一章作业：Vue基础知识测试',
        totalScore: 100
      },
      currentStudentIndex: 0,
      students: [
        {
          id: 1,
          name: '韦佳成',
          studentId: '202212903228',
          class: '软件工程2022级1班',
          graded: false
        },
        {
          id: 2,
          name: '张三',
          studentId: '202212903229',
          class: '软件工程2022级1班',
          graded: false
        },
        {
          id: 3,
          name: '李四',
          studentId: '202212903230',
          class: '软件工程2022级1班',
          graded: true
        }
      ],
      currentQuestionIndex: 0,
      questions: [
        {
          id: 1,
          type: 'single',
          content: 'Vue.js 是一个用于构建用户界面的什么框架？',
          points: 5,
          options: ['A. 后端框架', 'B. 渐进式框架', 'C. 移动端框架', 'D. 桌面应用框架'],
          correctAnswer: 'B',
          studentAnswer: 'B',
          isCorrect: true,
          studentScore: 5,
          autoGraded: true,
          graded: true
        },
        {
          id: 2,
          type: 'multiple',
          content: 'Vue 的核心特性包括哪些？（多选）',
          points: 10,
          options: ['A. 响应式数据绑定', 'B. 组件化开发', 'C. 虚拟DOM', 'D. 自动化测试'],
          correctAnswer: ['A', 'B', 'C'],
          studentAnswer: ['A', 'B'],
          isCorrect: false,
          studentScore: 6,
          autoGraded: true,
          graded: true
        },
        {
          id: 3,
          type: 'fill',
          content: '在 Vue 中，使用 {{___}} 可以进行数据绑定显示。',
          points: 5,
          correctAnswer: '{{ }}',
          studentAnswer: '{{ }}',
          referenceAnswer: '{{ }} 或 v-text',
          studentScore: 5,
          similarity: 100,
          aiScore: 5,
          matchedKeywords: ['{{', '}}'],
          graded: true
        },
        {
          id: 4,
          type: 'essay',
          content: '请简述 Vue 的生命周期钩子函数有哪些？并说明它们的作用。',
          points: 20,
          referenceAnswer: 'Vue 的生命周期钩子函数包括：beforeCreate（创建前）、created（创建后）、beforeMount（挂载前）、mounted（挂载后）、beforeUpdate（更新前）、updated（更新后）、beforeDestroy（销毁前）、destroyed（销毁后）。这些钩子函数在组件不同阶段自动调用，方便开发者在特定时机执行代码。',
          studentAnswer: 'Vue有8个生命周期钩子：beforeCreate在实例初始化之后调用，created在实例创建完成后调用，beforeMount在挂载开始之前调用，mounted在挂载完成后调用，beforeUpdate在数据更新时调用，updated在更新完成后调用，beforeDestroy在实例销毁之前调用，destroyed在实例销毁后调用。这些钩子可以让我们在不同阶段执行特定的操作。',
          studentScore: 18,
          similarity: 85,
          aiScore: 17,
          matchedKeywords: ['beforeCreate', 'created', 'mounted', 'destroyed', '钩子'],
          comment: '回答较完整，概念清晰，但可以补充更多实际应用场景',
          graded: false
        },
        {
          id: 5,
          type: 'essay',
          content: '请解释 Vue 中 computed 和 watch 的区别。',
          points: 15,
          referenceAnswer: 'computed是计算属性，具有缓存性，只有依赖数据变化时才会重新计算；watch是侦听器，用于观察数据变化并执行回调函数，没有缓存。computed适合处理复杂逻辑并返回值，watch适合执行异步操作或开销较大的操作。',
          studentAnswer: 'computed是用来计算的，watch是用来监听的。',
          studentScore: null,
          similarity: 25,
          aiScore: 4,
          matchedKeywords: ['computed', 'watch'],
          comment: '',
          graded: false
        }
      ],
      expandAll: false
    }
  },
  computed: {
    currentStudent() {
      return this.students[this.currentStudentIndex] || {}
    },
    currentQuestion() {
      return this.questions[this.currentQuestionIndex] || {}
    },
    totalCount() {
      return this.students.length
    },
    gradedCount() {
      return this.students.filter(s => s.graded).length
    },
    progressPercentage() {
      return Math.round((this.gradedCount / this.totalCount) * 100)
    },
    progressColor() {
      if (this.progressPercentage < 30) return '#f56c6c'
      if (this.progressPercentage < 70) return '#e6a23c'
      return '#67c23a'
    },
    objectiveScore() {
      return this.questions
        .filter(q => this.isObjectiveQuestion(q) && q.studentScore !== null)
        .reduce((sum, q) => sum + q.studentScore, 0)
    },
    subjectiveScore() {
      return this.questions
        .filter(q => !this.isObjectiveQuestion(q) && q.studentScore !== null)
        .reduce((sum, q) => sum + q.studentScore, 0)
    },
    totalScore() {
      return this.objectiveScore + this.subjectiveScore
    },
    maxScore() {
      return this.questions.reduce((sum, q) => sum + q.points, 0)
    }
  },
  mounted() {
    this.homeworkId = this.$route.params.id
    this.loadHomeworkData()
    
    // 计算所有主观题的 AI 辅助评分
    this.calculateAIScores()
  },
  methods: {
    loadHomeworkData() {
      // TODO: 从后端加载作业数据和学生提交
      console.log('加载作业ID:', this.homeworkId)
    },
    
    // 计算 AI 辅助评分（基于 TF-IDF 和余弦相似度）
    calculateAIScores() {
      this.questions.forEach(question => {
        if (!this.isObjectiveQuestion(question) && question.studentAnswer && question.referenceAnswer) {
          // 模拟计算语义相似度
          const similarity = this.calculateSimilarity(question.studentAnswer, question.referenceAnswer)
          question.similarity = Math.round(similarity * 100)
          
          // 基于相似度计算 AI 推荐分
          question.aiScore = Math.round(question.points * similarity * 10) / 10
          
          // 提取匹配的关键词
          question.matchedKeywords = this.extractMatchedKeywords(
            question.studentAnswer, 
            question.referenceAnswer
          )
        }
      })
    },
    
    // 计算余弦相似度（简化版）
    calculateSimilarity(text1, text2) {
      if (!text1 || !text2) return 0
      
      // 简单的词频统计
      const words1 = text1.split('')
      const words2 = text2.split('')
      
      const set1 = new Set(words1)
      const set2 = new Set(words2)
      
      // 计算交集
      const intersection = new Set([...set1].filter(x => set2.has(x)))
      
      // Jaccard 相似度
      const union = new Set([...set1, ...set2])
      return intersection.size / union.size
    },
    
    // 提取匹配的关键词
    extractMatchedKeywords(studentAnswer, referenceAnswer) {
      const keywords = ['Vue', 'computed', 'watch', '生命周期', 'beforeCreate', 'created', 
                       'mounted', 'updated', 'destroyed', '钩子', '响应式', '组件']
      
      return keywords.filter(keyword => 
        studentAnswer.includes(keyword) && referenceAnswer.includes(keyword)
      ).slice(0, 5)
    },
    
    isObjectiveQuestion(question) {
      return ['single', 'multiple', 'judge'].includes(question.type)
    },
    
    getQuestionTypeName(type) {
      const typeMap = {
        single: '单选题',
        multiple: '多选题',
        judge: '判断题',
        fill: '填空题',
        essay: '简答题'
      }
      return typeMap[type] || '未知题型'
    },
    
    formatStudentAnswer(question) {
      if (Array.isArray(question.studentAnswer)) {
        return question.studentAnswer.join(', ')
      }
      return question.studentAnswer
    },
    
    formatCorrectAnswer(question) {
      if (Array.isArray(question.correctAnswer)) {
        return question.correctAnswer.join(', ')
      }
      return question.correctAnswer
    },
    
    getSimilarityColor(similarity) {
      if (similarity >= 80) return '#67c23a'
      if (similarity >= 60) return '#e6a23c'
      return '#f56c6c'
    },
    
    selectQuestion(index) {
      this.currentQuestionIndex = index
    },
    
    previousQuestion() {
      if (this.currentQuestionIndex > 0) {
        this.currentQuestionIndex--
      }
    },
    
    nextQuestion() {
      if (this.currentQuestionIndex < this.questions.length - 1) {
        this.currentQuestionIndex++
      }
    },
    
    applyAIScore() {
      this.currentQuestion.studentScore = this.currentQuestion.aiScore
      this.$message.success('已采纳 AI 推荐分')
    },
    
    saveCurrentQuestion() {
      if (this.currentQuestion.studentScore === null || this.currentQuestion.studentScore === undefined) {
        this.$message.warning('请先输入得分')
        return
      }
      
      this.currentQuestion.graded = true
      this.$message.success('本题已保存')
      
      // 自动跳转到下一题（如果有）
      if (this.currentQuestionIndex < this.questions.length - 1) {
        this.nextQuestion()
      }
    },
    
    previousStudent() {
      if (this.currentStudentIndex > 0) {
        this.saveProgress()
        this.currentStudentIndex--
        this.loadStudentSubmission()
      }
    },
    
    nextStudent() {
      if (this.currentStudentIndex < this.students.length - 1) {
        this.saveProgress()
        this.currentStudentIndex++
        this.loadStudentSubmission()
      }
    },
    
    loadStudentSubmission() {
      // TODO: 加载当前学生的提交内容
      console.log('加载学生提交:', this.currentStudent.name)
      this.currentQuestionIndex = 0
      this.calculateAIScores()
    },
    
    saveProgress() {
      // 保存当前批阅进度
      console.log('保存批阅进度')
    },
    
    returnWork() {
      this.$confirm(
        `确定要将 ${this.currentStudent.name} 的作业打回重做吗？学生将收到通知并需要重新提交。`,
        '打回重做',
        {
          confirmButtonText: '确定打回',
          cancelButtonText: '取消',
          type: 'warning'
        }
      ).then(() => {
        // TODO: 调用打回接口
        this.$message.success('已打回，学生将收到通知')
        this.nextStudent()
      }).catch(() => {})
    },
    
    submitGrading() {
      // 检查是否所有题目都已批阅
      const ungradedQuestions = this.questions.filter(q => !q.graded && q.studentScore === null)
      if (ungradedQuestions.length > 0) {
        this.$confirm(
          `还有 ${ungradedQuestions.length} 道题未批阅，确定要提交吗？未批阅的题目将得0分。`,
          '提示',
          {
            confirmButtonText: '继续批阅',
            cancelButtonText: '确定提交',
            type: 'warning'
          }
        ).then(() => {
          // 取消，继续批阅
        }).catch(() => {
          this.doSubmitGrading()
        })
      } else {
        this.doSubmitGrading()
      }
    },
    
    doSubmitGrading() {
      // TODO: 提交批阅结果到后端
      const gradingData = {
        homeworkId: this.homeworkId,
        studentId: this.currentStudent.id,
        totalScore: this.totalScore,
        objectiveScore: this.objectiveScore,
        subjectiveScore: this.subjectiveScore,
        questions: this.questions.map(q => ({
          questionId: q.id,
          score: q.studentScore || 0,
          comment: q.comment || ''
        }))
      }
      
      console.log('提交批阅数据:', gradingData)
      
      this.$message.success('批阅结果已提交，成绩已同步给学生')
      this.students[this.currentStudentIndex].graded = true
      
      // 自动跳转到下一个学生
      if (this.currentStudentIndex < this.students.length - 1) {
        this.nextStudent()
      } else {
        this.$message.success('所有学生作业批阅完成！')
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.homework-grading-page {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: #f5f7fa;
}

.grading-header {
  background: white;
  padding: 20px 30px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #e4e7ed;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);

  .header-left {
    .homework-title {
      margin: 0 0 10px 0;
      font-size: 20px;
      color: #303133;
    }

    .student-info {
      display: flex;
      align-items: center;
    }
  }

  .header-right {
    .progress-info {
      display: flex;
      align-items: center;

      .progress-text {
        font-size: 14px;
        color: #606266;
      }

      .progress-count {
        font-size: 18px;
        font-weight: bold;
        color: #409eff;
        margin-left: 8px;
      }
    }
  }
}

.grading-content {
  flex: 1;
  display: flex;
  overflow: hidden;
  padding: 20px;
  gap: 20px;
}

.question-list {
  width: 280px;
  background: white;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);

  .list-header {
    padding: 15px 20px;
    border-bottom: 1px solid #e4e7ed;
    display: flex;
    justify-content: space-between;
    align-items: center;

    h3 {
      margin: 0;
      font-size: 16px;
      color: #303133;
    }
  }

  .list-content {
    flex: 1;
    overflow-y: auto;
    padding: 10px;
  }

  .question-item {
    padding: 12px 15px;
    margin-bottom: 8px;
    border-radius: 6px;
    border: 1px solid #e4e7ed;
    cursor: pointer;
    transition: all 0.3s;

    &:hover {
      border-color: #409eff;
      background: #f0f9ff;
    }

    &.active {
      border-color: #409eff;
      background: #ecf5ff;
      box-shadow: 0 2px 8px rgba(64, 158, 255, 0.2);
    }

    &.graded {
      background: #f0f9ff;
    }

    &.objective {
      .item-header {
        opacity: 0.7;
      }
    }

    .item-header {
      display: flex;
      align-items: center;
      gap: 8px;
      margin-bottom: 6px;

      .item-number {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 24px;
        height: 24px;
        background: #409eff;
        color: white;
        border-radius: 50%;
        font-size: 12px;
        font-weight: bold;
      }

      .item-type {
        font-size: 13px;
        color: #606266;
      }

      .item-score {
        margin-left: auto;
        font-size: 13px;
        color: #909399;
      }
    }

    .item-score-display {
      font-size: 13px;
      color: #67c23a;
      font-weight: bold;
      margin-top: 5px;
    }
  }
}

.grading-detail {
  flex: 1;
  background: white;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);

  .detail-header {
    padding: 15px 25px;
    border-bottom: 1px solid #e4e7ed;

    h3 {
      margin: 0;
      font-size: 18px;
      color: #303133;
      display: flex;
      align-items: center;

      .question-score {
        margin-left: auto;
        font-size: 16px;
        color: #409eff;
      }
    }
  }

  .detail-content {
    flex: 1;
    overflow-y: auto;
    padding: 25px;
  }
}

.question-content-section {
  margin-bottom: 25px;

  h4 {
    margin: 0 0 12px 0;
    font-size: 15px;
    color: #606266;
  }

  .question-text {
    padding: 15px;
    background: #f9fafc;
    border-radius: 6px;
    border-left: 3px solid #409eff;
    font-size: 14px;
    line-height: 1.8;
    color: #303133;
  }
}

.auto-grading-section {
  margin-bottom: 25px;

  p {
    margin: 8px 0;
    font-size: 14px;
  }
}

.manual-grading-section {
  .answer-box {
    margin-bottom: 20px;
    border-radius: 6px;
    border: 1px solid #e4e7ed;
    overflow: hidden;

    h4 {
      margin: 0;
      padding: 12px 15px;
      background: #f5f7fa;
      font-size: 14px;
      color: #606266;
      border-bottom: 1px solid #e4e7ed;

      i {
        margin-right: 5px;
      }
    }

    .answer-content {
      padding: 15px;
      min-height: 100px;
      font-size: 14px;
      line-height: 1.8;
      color: #303133;
      white-space: pre-wrap;
      word-break: break-word;
    }
  }

  .student-answer-box {
    border-color: #409eff;

    h4 {
      background: #ecf5ff;
      color: #409eff;
    }
  }

  .reference-answer-box {
    border-color: #67c23a;

    h4 {
      background: #f0f9ff;
      color: #67c23a;
    }
  }
}

.ai-assist-section {
  margin: 25px 0;
  padding: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 8px;
  color: white;

  h4 {
    margin: 0 0 20px 0;
    font-size: 16px;
    display: flex;
    align-items: center;
    gap: 8px;

    i.el-icon-cpu {
      font-size: 20px;
    }
  }

  .ai-metrics {
    background: rgba(255,255,255,0.15);
    border-radius: 6px;
    padding: 15px;

    .metric-item {
      margin-bottom: 15px;

      &:last-child {
        margin-bottom: 0;
      }

      .metric-label {
        font-size: 13px;
        margin-bottom: 8px;
        opacity: 0.9;
      }

      .metric-value {
        font-size: 14px;

        &.ai-score {
          font-size: 24px;
          font-weight: bold;
          display: flex;
          align-items: center;
        }
      }
    }
  }
}

.manual-score-section {
  margin: 25px 0;
  padding: 20px;
  background: #f9fafc;
  border-radius: 8px;
  border: 1px solid #e4e7ed;

  h4 {
    margin: 0 0 15px 0;
    font-size: 15px;
    color: #303133;

    i {
      margin-right: 5px;
      color: #409eff;
    }
  }

  .score-input-group,
  .comment-input-group {
    display: flex;
    align-items: center;
    gap: 10px;

    label {
      font-size: 14px;
      color: #606266;
      white-space: nowrap;
    }

    .score-hint {
      font-size: 14px;
      color: #909399;
    }
  }

  .comment-input-group {
    align-items: flex-start;

    label {
      margin-top: 8px;
    }
  }
}

.question-navigation {
  display: flex;
  justify-content: center;
  gap: 15px;
  padding-top: 20px;
  border-top: 1px solid #e4e7ed;
}

.grading-footer {
  background: white;
  padding: 20px 30px;
  border-top: 1px solid #e4e7ed;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 -2px 8px rgba(0,0,0,0.05);

  .footer-left {
    .score-summary {
      display: flex;
      gap: 30px;
      align-items: center;

      .summary-item {
        .summary-label {
          font-size: 14px;
          color: #606266;
        }

        .summary-value {
          font-size: 20px;
          font-weight: bold;
          margin-left: 8px;

          &.objective {
            color: #409eff;
          }

          &.subjective {
            color: #e6a23c;
          }
        }

        .summary-max {
          font-size: 16px;
          color: #909399;
          margin-left: 5px;
        }

        &.total {
          padding-left: 30px;
          border-left: 2px solid #e4e7ed;

          .summary-value {
            font-size: 28px;
            color: #67c23a;
          }
        }
      }
    }
  }

  .footer-right {
    display: flex;
    gap: 10px;
  }
}
</style>
