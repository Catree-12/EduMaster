<template>
  <div class="homework-edit">
    <div class="page-header">
      <el-button icon="el-icon-arrow-left" type="text" @click="goBack">返回</el-button>
      <div class="header-right">
        <el-button @click="goBack">取消</el-button>
        <el-button type="primary" @click="saveHomework">保存</el-button>
      </div>
    </div>

    <div class="edit-container">
      <el-card class="info-card">
        <h2>作业信息</h2>
        <el-form :model="homework" label-width="100px">
          <el-form-item label="作业名称">
            <el-input v-model="homework.name" placeholder="请输入作业名称"></el-input>
          </el-form-item>
          <el-form-item label="作业描述">
            <el-input 
              v-model="homework.description" 
              type="textarea" 
              rows="3"
              placeholder="请输入作业描述"
            ></el-input>
          </el-form-item>
        </el-form>
      </el-card>

      <el-card class="questions-card">
        <div class="card-header">
          <h2>题目列表（共 {{ homework.questions.length }} 题，总分 {{ totalPoints }} 分）</h2>
          <el-tag type="info">仅可编辑题目内容，不可添加或删除题目</el-tag>
        </div>

        <div v-for="(question, index) in homework.questions" :key="question.id" class="question-edit-card">
          <div class="question-header">
            <span class="question-number">第 {{ index + 1 }} 题</span>
            <el-tag size="small">{{ getQuestionTypeLabel(question.type) }}</el-tag>
            <el-input-number 
              v-model="question.points" 
              :min="1" 
              :max="100" 
              size="small"
              style="margin-left: auto;"
            ></el-input-number>
            <span style="margin-left: 5px;">分</span>
          </div>

          <el-form label-width="80px">
            <el-form-item label="题目">
              <el-input 
                v-model="question.title" 
                type="textarea" 
                rows="2"
                placeholder="请输入题目"
              ></el-input>
            </el-form-item>

            <!-- 单选题/多选题 -->
            <template v-if="question.type === 'single' || question.type === 'multiple'">
              <el-form-item label="选项">
                <div v-for="(option, optIdx) in question.options" :key="optIdx" class="option-edit">
                  <span class="option-label">{{ String.fromCharCode(65 + optIdx) }}.</span>
                  <el-input v-model="question.options[optIdx]" placeholder="请输入选项内容"></el-input>
                  <el-checkbox 
                    v-if="question.type === 'single'"
                    :value="question.answer === optIdx"
                    @change="setAnswer(question, optIdx)"
                  >
                    正确答案
                  </el-checkbox>
                  <el-checkbox 
                    v-else
                    :value="question.answer.includes(optIdx)"
                    @change="toggleAnswer(question, optIdx)"
                  >
                    正确答案
                  </el-checkbox>
                </div>
              </el-form-item>
            </template>

            <!-- 填空题 -->
            <el-form-item v-if="question.type === 'fill'" label="参考答案">
              <el-input v-model="question.answer" placeholder="请输入参考答案"></el-input>
            </el-form-item>

            <!-- 判断题 -->
            <el-form-item v-if="question.type === 'judge'" label="正确答案">
              <el-radio-group v-model="question.answer">
                <el-radio :label="true">正确</el-radio>
                <el-radio :label="false">错误</el-radio>
              </el-radio-group>
            </el-form-item>

            <!-- 简答题 -->
            <el-form-item v-if="question.type === 'essay'" label="参考答案">
              <el-input 
                v-model="question.answer" 
                type="textarea" 
                rows="4"
                placeholder="请输入参考答案"
              ></el-input>
            </el-form-item>
          </el-form>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HomeworkEdit',
  data() {
    return {
      homework: {
        id: 1,
        name: '函数进阶练习',
        description: '掌握JavaScript高级函数概念',
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
            answer: 'JavaScript的事件循环是一个处理异步操作的机制。',
            points: 20
          }
        ]
      }
    }
  },
  computed: {
    totalPoints() {
      return this.homework.questions.reduce((sum, q) => sum + q.points, 0)
    }
  },
  created() {
    const id = this.$route.params.id
    // TODO: 从后端获取作业详情
    console.log('编辑作业ID:', id)
  },
  methods: {
    goBack() {
      this.$router.back()
    },
    saveHomework() {
      // 验证
      if (!this.homework.name) {
        this.$message.error('请输入作业名称')
        return
      }

      // TODO: 调用API保存
      this.$message.success('作业已保存')
      this.goBack()
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
    setAnswer(question, optIdx) {
      question.answer = optIdx
    },
    toggleAnswer(question, optIdx) {
      if (!Array.isArray(question.answer)) {
        question.answer = []
      }
      const index = question.answer.indexOf(optIdx)
      if (index > -1) {
        question.answer.splice(index, 1)
      } else {
        question.answer.push(optIdx)
      }
    }
  }
}
</script>

<style scoped lang="scss">
.homework-edit {
  padding: 20px;
  min-height: 100vh;
  background: #f5f7fa;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;

  .header-right {
    display: flex;
    gap: 10px;
  }
}

.edit-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.info-card, .questions-card {
  h2 {
    margin: 0 0 20px 0;
    font-size: 18px;
    color: #333;
  }
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.question-edit-card {
  padding: 20px;
  background: #f9f9f9;
  border-radius: 4px;
  margin-bottom: 15px;
  border: 1px solid #e0e0e0;
}

.question-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 1px solid #e0e0e0;

  .question-number {
    font-weight: bold;
    color: #333;
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
