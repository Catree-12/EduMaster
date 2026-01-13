<template>
  <div class="homework-detail">
    <div class="page-header">
      <div class="header-left">
        <el-button icon="el-icon-arrow-left" type="text" @click="goBack">返回</el-button>
        <el-checkbox v-model="showAnswers" style="margin-left: 20px;">显示答案</el-checkbox>
      </div>
      <div class="header-right">
        <el-button type="primary" @click="goToEdit">重新编辑</el-button>
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
    const id = this.$route.params.id
    // TODO: 从后端获取作业详情
    console.log('作业ID:', id)
  },
  methods: {
    goBack() {
      this.$router.back()
    },
    goToEdit() {
      this.$router.push(`/teacher/homework/${this.homework.id}/edit`)
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
</style>
