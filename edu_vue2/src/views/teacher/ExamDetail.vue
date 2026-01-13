<template>
  <div class="exam-detail">
    <div class="page-header">
      <div class="header-left">
        <el-button icon="el-icon-arrow-left" type="text" @click="goBack">返回</el-button>
        <el-checkbox v-model="showAnswers" style="margin-left: 20px;">显示答案</el-checkbox>
      </div>
      <div class="header-right">
        <el-button type="primary" @click="goToEdit">重新编辑</el-button>
      </div>
    </div>

    <div class="exam-info">
      <h1>{{ exam.name }}</h1>
      <p class="description">{{ exam.description }}</p>
      <div class="meta">
        <span>共 {{ exam.questions.length }} 道题</span>
        <span>总分 {{ exam.totalPoints }} 分</span>
        <span>考试时长 {{ exam.duration }} 分钟</span>
        <span>创建于 {{ exam.createdAt }}</span>
      </div>
    </div>

    <div class="questions-container">
      <div v-for="(question, index) in exam.questions" :key="question.id" class="question-card">
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
  name: 'ExamDetail',
  data() {
    return {
      showAnswers: true,
      exam: {
        id: 1,
        name: '期末考试',
        description: '本学期期末综合测试',
        totalPoints: 100,
        duration: 120,
        createdAt: '2024-01-10',
        questions: [
          {
            id: 1,
            type: 'single',
            title: '下列哪个是闭包的特性？',
            options: ['访问外部变量', '内存泄漏', '函数嵌套', '变量提升'],
            answer: 0,
            points: 5
          },
          {
            id: 2,
            type: 'multiple',
            title: 'JavaScript中的数据类型包括？',
            options: ['String', 'Number', 'Boolean', 'Undefined'],
            answer: [0, 1, 2, 3],
            points: 10
          },
          {
            id: 3,
            type: 'fill',
            title: '在JavaScript中，___ 用于定义块级作用域变量。',
            answer: 'let',
            points: 5
          },
          {
            id: 4,
            type: 'judge',
            title: 'null和undefined在JavaScript中是相同的。',
            answer: false,
            points: 5
          },
          {
            id: 5,
            type: 'essay',
            title: '请简述JavaScript的事件循环机制。',
            answer: 'JavaScript是单线程语言，通过事件循环机制实现异步操作。事件循环包括调用栈、任务队列和微任务队列。宏任务包括setTimeout、setInterval等，微任务包括Promise.then等。执行顺序是：同步代码 → 微任务 → 宏任务。',
            points: 20
          }
        ]
      }
    }
  },
  mounted() {
    const examId = this.$route.params.id
    // TODO: 根据 examId 从后端加载考试数据
    console.log('加载考试详情:', examId)
  },
  methods: {
    goBack() {
      this.$router.back()
    },
    goToEdit() {
      this.$router.push(`/teacher/exam-edit/${this.exam.id}`)
    },
    getQuestionTypeLabel(type) {
      const typeMap = {
        single: '单选题',
        multiple: '多选题',
        fill: '填空题',
        judge: '判断题',
        essay: '简答题'
      }
      return typeMap[type] || type
    },
    isCorrectAnswer(question, optionIndex) {
      if (question.type === 'single') {
        return question.answer === optionIndex
      } else if (question.type === 'multiple') {
        return question.answer.includes(optionIndex)
      }
      return false
    }
  }
}
</script>

<style scoped lang="scss">
.exam-detail {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;

  .page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 30px;
    padding-bottom: 20px;
    border-bottom: 1px solid #EBEEF5;

    .header-left {
      display: flex;
      align-items: center;
    }
  }

  .exam-info {
    margin-bottom: 30px;

    h1 {
      font-size: 28px;
      color: #303133;
      margin: 0 0 12px 0;
    }

    .description {
      font-size: 14px;
      color: #606266;
      margin: 0 0 16px 0;
      line-height: 1.6;
    }

    .meta {
      display: flex;
      gap: 24px;
      font-size: 14px;
      color: #909399;

      span {
        display: flex;
        align-items: center;

        &:before {
          content: '•';
          margin-right: 6px;
        }

        &:first-child:before {
          content: '';
          margin-right: 0;
        }
      }
    }
  }

  .questions-container {
    .question-card {
      background: #FFFFFF;
      border: 1px solid #EBEEF5;
      border-radius: 8px;
      padding: 24px;
      margin-bottom: 20px;
      transition: box-shadow 0.3s;

      &:hover {
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
      }

      .question-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 16px;

        .question-number {
          font-size: 16px;
          font-weight: 600;
          color: #303133;
        }

        .question-type {
          background: #ECF5FF;
          color: #409EFF;
          padding: 4px 12px;
          border-radius: 4px;
          font-size: 12px;
        }

        .question-points {
          margin-left: auto;
          color: #F56C6C;
          font-weight: 600;
        }
      }

      .question-title {
        font-size: 15px;
        color: #303133;
        line-height: 1.8;
        margin-bottom: 16px;
      }

      .question-options {
        .option {
          display: flex;
          align-items: center;
          padding: 12px 16px;
          margin-bottom: 8px;
          background: #F5F7FA;
          border-radius: 6px;
          transition: all 0.3s;

          &.correct {
            background: #F0F9FF;
            border: 1px solid #67C23A;
            color: #67C23A;
          }

          .option-label {
            font-weight: 600;
            margin-right: 8px;
            min-width: 24px;
          }

          .correct-icon {
            margin-left: auto;
            color: #67C23A;
            font-size: 18px;
          }
        }
      }

      .question-answer {
        margin-top: 16px;
        padding: 12px 16px;
        background: #F0F9FF;
        border-left: 3px solid #409EFF;
        border-radius: 4px;

        strong {
          color: #409EFF;
          margin-right: 8px;
        }

        p {
          margin: 8px 0 0 0;
          line-height: 1.6;
          color: #606266;
        }
      }
    }
  }
}
</style>
