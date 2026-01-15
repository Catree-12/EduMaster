<template>
  <div class="homework-detail">
    <div class="page-header">
      <div class="header-left">
        <el-button icon="el-icon-arrow-left" type="text" @click="goBack">返回</el-button>
        <el-checkbox v-if="!isEditing" v-model="showAnswers" style="margin-left: 20px;">显示答案</el-checkbox>
      </div>
      <div class="header-right">
        <el-button v-if="!isEditing" type="primary" @click="startEdit">重新编辑</el-button>
        <template v-else>
          <el-button @click="cancelEdit">取消</el-button>
          <el-button type="primary" @click="saveEdit">保存</el-button>
        </template>
      </div>
    </div>

    <div class="homework-info">
      <h1>{{ homework.name }}</h1>
      <p class="description">{{ homework.description }}</p>
      <div class="meta">
        <span>共 {{ homework.questions.length }} 道题</span>
        <span>总分 {{ homework.totalPoints }} 分</span>
        <span>创建于 {{ homework.createdAt }}</span>
      </div>
    </div>

    <div class="questions-container">
      <div v-for="(question, index) in homework.questions" :key="question.id" class="question-card">
        <div class="question-header">
          <span class="question-number">第 {{ index + 1 }} 题</span>
          <span class="question-type">{{ getQuestionTypeLabel(question.type) }}</span>
          <span class="question-points">{{ question.points }} 分</span>
        </div>

        <!-- 查看模式 -->
        <template v-if="!isEditing">
          <div class="question-title">{{ question.title }}</div>

          <div v-if="question.type === 'single' || question.type === 'multiple'" class="question-options">
            <div 
              v-for="(option, optIdx) in question.options" 
              :key="optIdx" 
              class="option"
              :class="{ 
                correct: showAnswers && isCorrectAnswer(question, optIdx)
              }"
            >
              <span class="option-label">{{ String.fromCharCode(65 + optIdx) }}.</span>
              <span>{{ option }}</span>
              <i v-if="showAnswers && isCorrectAnswer(question, optIdx)" class="el-icon-check correct-icon"></i>
            </div>
          </div>

          <div v-if="showAnswers && question.type === 'fill'" class="question-answer">
            <strong>参考答案：</strong>{{ question.answer }}
          </div>

          <div v-if="showAnswers && question.type === 'judge'" class="question-answer">
            <strong>正确答案：</strong>{{ question.answer ? '正确' : '错误' }}
          </div>

          <div v-if="showAnswers && question.type === 'essay'" class="question-answer">
            <strong>参考答案：</strong>
            <p>{{ question.answer }}</p>
          </div>
        </template>

        <!-- 编辑模式 -->
        <template v-else>
          <div class="edit-section">
            <div class="form-item">
              <label>题目内容：</label>
              <el-input 
                v-model="question.title" 
                type="textarea" 
                :rows="3"
                placeholder="请输入题目内容"
              />
            </div>

            <!-- 单选题/多选题编辑 -->
            <div v-if="question.type === 'single' || question.type === 'multiple'" class="form-item">
              <label>选项：</label>
              <div v-for="(option, optIdx) in question.options" :key="optIdx" class="option-edit">
                <span class="option-label">{{ String.fromCharCode(65 + optIdx) }}.</span>
                <el-input v-model="question.options[optIdx]" placeholder="请输入选项内容" />
                <el-checkbox 
                  v-if="question.type === 'single'"
                  :value="question.answer === optIdx"
                  @change="question.answer = optIdx"
                >
                  正确答案
                </el-checkbox>
                <el-checkbox 
                  v-else
                  :value="question.answer.includes(optIdx)"
                  @change="toggleMultipleAnswer(question, optIdx)"
                >
                  正确答案
                </el-checkbox>
              </div>
            </div>

            <!-- 填空题编辑 -->
            <div v-if="question.type === 'fill'" class="form-item">
              <label>参考答案：</label>
              <el-input v-model="question.answer" placeholder="请输入参考答案" />
            </div>

            <!-- 判断题编辑 -->
            <div v-if="question.type === 'judge'" class="form-item">
              <label>正确答案：</label>
              <el-radio-group v-model="question.answer">
                <el-radio :label="true">正确</el-radio>
                <el-radio :label="false">错误</el-radio>
              </el-radio-group>
            </div>

            <!-- 简答题编辑 -->
            <div v-if="question.type === 'essay'" class="form-item">
              <label>参考答案：</label>
              <el-input 
                v-model="question.answer" 
                type="textarea" 
                :rows="4"
                placeholder="请输入参考答案"
              />
            </div>

            <div class="form-item">
              <label>分值：</label>
              <el-input-number v-model="question.points" :min="1" :max="100" />
            </div>
          </div>
        </template>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HomeworkDetail',
  data() {
    return {
      showAnswers: true,
      isPublished: false, // 是否已发布
      isEditing: false, // 是否处于编辑模式
      originalQuestions: null, // 备份原始数据
      homework: {
        id: 1,
        name: '函数进阶练习',
        description: '掌握JavaScript高级函数概念',
        totalPoints: 100,
        createdAt: '2024-01-10',
        questions: [
          {
            id: 1,
            type: 'single',
            title: '下列哪个是闭包的特性？',
            options: ['访问外部变量', '内存泄漏', '函数嵌套', '变量提升'],
            answer: 0,
            points: 20
          },
          {
            id: 2,
            type: 'multiple',
            title: 'JavaScript中的数据类型包括？',
            options: ['String', 'Number', 'Boolean', 'Undefined'],
            answer: [0, 1, 2, 3],
            points: 20
          },
          {
            id: 3,
            type: 'fill',
            title: '在JavaScript中，___ 用于定义块级作用域变量。',
            answer: 'let',
            points: 20
          },
          {
            id: 4,
            type: 'judge',
            title: 'JavaScript是一门面向对象的编程语言。',
            answer: true,
            points: 20
          },
          {
            id: 5,
            type: 'essay',
            title: '请简述JavaScript中的事件循环机制。',
            answer: 'JavaScript的事件循环是一个处理异步操作的机制。它包括调用栈、任务队列和微任务队列。当调用栈为空时，事件循环会从任务队列中取出任务执行。',
            points: 20
          }
        ]
      }
    }
  },
  created() {
    // 检查是否已发布
    this.isPublished = this.$route.query.published === 'true'
    
    const id = this.$route.params.id
    // TODO: 从后端获取作业详情
    console.log('作业ID:', id)
  },
  methods: {
    goBack() {
      this.$router.back()
    },
    startEdit() {
      // 检查是否已发布
      if (!this.isPublished) {
        // 未发布的作业，跳转到新建作业页面
        this.$router.push({
          path: '/teacher/homework/create',
          query: { 
            id: this.homework.id,
            mode: 'edit'
          }
        })
        return
      }
      
      // 已发布的作业，在当前页面进入编辑模式
      this.originalQuestions = JSON.parse(JSON.stringify(this.homework.questions))
      this.isEditing = true
      this.$message.info('现在可以编辑题目内容')
    },
    cancelEdit() {
      // 取消编辑，恢复原始数据
      this.homework.questions = this.originalQuestions
      this.isEditing = false
      this.$message.info('已取消编辑')
    },
    saveEdit() {
      // 保存编辑
      this.$confirm('确定保存修改吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        // TODO: 调用API保存数据
        this.isEditing = false
        this.originalQuestions = null
        this.$message.success('保存成功')
      }).catch(() => {})
    },
    toggleMultipleAnswer(question, optIdx) {
      // 切换多选题答案
      if (!Array.isArray(question.answer)) {
        question.answer = []
      }
      const index = question.answer.indexOf(optIdx)
      if (index > -1) {
        question.answer.splice(index, 1)
      } else {
        question.answer.push(optIdx)
      }
    },
    getQuestionTypeLabel(type) {
      const labels = {
        single: '单选题',
        multiple: '多选题',
        fill: '填空题',
        judge: '判断题',
        essay: '简答题'
      }
      return labels[type] || type
    },
    isCorrectAnswer(question, optIdx) {
      if (question.type === 'single') {
        return question.answer === optIdx
      } else if (question.type === 'multiple') {
        return question.answer.includes(optIdx)
      }
      return false
    }
  }
}
</script>

<style scoped lang="scss">
.homework-detail {
  padding: 20px;
  min-height: 100vh;
  background: #f5f7fa;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.header-left {
  display: flex;
  align-items: center;
}

.homework-info {
  background: white;
  padding: 30px;
  border-radius: 4px;
  margin-bottom: 20px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);

  h1 {
    margin: 0 0 10px 0;
    font-size: 24px;
    color: #333;
  }

  .description {
    margin: 0 0 15px 0;
    font-size: 14px;
    color: #666;
  }

  .meta {
    display: flex;
    gap: 20px;
    font-size: 13px;
    color: #999;
  }
}

.questions-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.question-card {
  background: white;
  padding: 25px;
  border-radius: 4px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.question-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 15px;

  .question-number {
    font-weight: bold;
    color: #333;
  }

  .question-type {
    padding: 2px 8px;
    background: #e6f7ff;
    color: #1890ff;
    border-radius: 2px;
    font-size: 12px;
  }

  .question-points {
    margin-left: auto;
    color: #f56c6c;
    font-weight: bold;
  }
}

.question-title {
  font-size: 16px;
  color: #333;
  margin-bottom: 15px;
  line-height: 1.6;
}

.question-options {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.option {
  display: flex;
  align-items: center;
  padding: 12px;
  background: #f9f9f9;
  border-radius: 4px;
  border: 1px solid #e0e0e0;

  &.correct {
    background: #f6ffed;
    border-color: #52c41a;
  }

  .option-label {
    margin-right: 10px;
    font-weight: bold;
    color: #666;
  }

  .correct-icon {
    margin-left: auto;
    color: #52c41a;
    font-size: 18px;
  }
}

.question-answer {
  padding: 15px;
  background: #f9f9f9;
  border-left: 3px solid #1890ff;
  border-radius: 2px;

  strong {
    color: #333;
  }

  p {
    margin: 10px 0 0 0;
    line-height: 1.6;
    color: #666;
  }
}

/* 编辑模式样式 */
.edit-section {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-item {
  display: flex;
  flex-direction: column;
  gap: 8px;

  label {
    font-weight: 600;
    color: #333;
    font-size: 14px;
  }
}

.option-edit {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 10px;

  .option-label {
    font-weight: bold;
    color: #666;
    min-width: 30px;
  }

  .el-input {
    flex: 1;
  }
}
</style>
