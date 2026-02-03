<template>
  <div class="homework-publish">
    <div class="publish-container">
      <!-- 页面顶部：信息确认区 -->
      <div class="header-section">
        <div class="title-area">
          <h2 class="homework-title">{{ homework.name }}</h2>
          <el-tag type="info" size="small">待发布</el-tag>
        </div>
        <div class="quick-actions">
          <el-button icon="el-icon-back" @click="goBack">返回</el-button>
          <el-button icon="el-icon-refresh-left" @click="resetForm">重置</el-button>
        </div>
      </div>

      <!-- 核心发布区 -->
      <div class="publish-content">
        <el-form :model="publishForm" :rules="rules" ref="publishForm" label-position="top">
          
          <!-- 第一部分：发布范围与时间 -->
          <div class="form-card">
            <h3 class="card-title">发布范围与时间</h3>
            
            <!-- 选择班期 -->
            <el-form-item label="选择班期" prop="termId">
              <el-select 
                v-model="publishForm.termId" 
                placeholder="请选择班期"
                style="width: 100%"
                @change="handleTermChange"
              >
                <el-option
                  v-for="term in termList"
                  :key="term.id"
                  :label="term.name"
                  :value="term.id"
                >
                  <span>{{ term.name }}</span>
                  <span style="color: #8492a6; font-size: 13px; margin-left: 8px;">
                    {{ term.startDate }} ~ {{ term.endDate }}
                  </span>
                </el-option>
              </el-select>
            </el-form-item>

            <el-form-item label="发放对象" prop="targets">
              <el-select 
                v-model="publishForm.targets" 
                multiple 
                placeholder="请选择班级或学生"
                style="width: 100%"
                filterable
                :disabled="!publishForm.termId"
              >
                <el-option-group label="班级">
                  <el-option
                    v-for="cls in filteredClassList"
                    :key="'class-' + cls.id"
                    :label="cls.name"
                    :value="'class-' + cls.id"
                  >
                    <span>{{ cls.name }}</span>
                    <span style="color: #8492a6; font-size: 13px; margin-left: 8px;">({{ cls.studentCount }}人)</span>
                  </el-option>
                </el-option-group>
                <el-option-group label="学生">
                  <el-option
                    v-for="student in filteredStudentList"
                    :key="'student-' + student.id"
                    :label="student.name"
                    :value="'student-' + student.id"
                  />
                </el-option-group>
              </el-select>
              <div v-if="!publishForm.termId" style="margin-top: 8px; font-size: 12px; color: #f56c6c;">
                <i class="el-icon-warning"></i> 请先选择班期
              </div>
            </el-form-item>

            <el-form-item label="起始时间" prop="startTime">
              <el-date-picker
                v-model="publishForm.startTime"
                type="datetime"
                placeholder="选择起始时间"
                style="width: 100%"
                :picker-options="startTimeOptions"
              />
            </el-form-item>

            <el-form-item label="截止时间" prop="deadline">
              <el-date-picker
                v-model="publishForm.deadline"
                type="datetime"
                placeholder="选择截止时间"
                style="width: 100%"
                :picker-options="deadlineOptions"
              />
            </el-form-item>
          </div>

          <!-- 第二部分：合格标准与重做 -->
          <div class="form-card">
            <h3 class="card-title">合格标准与重做</h3>
            
            <el-form-item label="及格标准" prop="passingScore">
              <el-input-number 
                v-model="publishForm.passingScore" 
                :min="0" 
                :max="homework.totalScore"
                placeholder="分值"
                style="width: 200px"
              />
              <span style="margin-left: 8px; color: #606266;">分（总分 {{ homework.totalScore }} 分）</span>
            </el-form-item>

            <el-form-item label="允许重做">
              <el-switch 
                v-model="publishForm.allowRedo"
                active-text="允许学生在截止前重新提交"
                inactive-text="不允许重做"
              />
            </el-form-item>
          </div>

          <!-- 第三部分：智能批阅设置 -->
          <div class="form-card highlight-card">
            <h3 class="card-title">
              <i class="el-icon-cpu" style="color: #409EFF; margin-right: 8px;"></i>
              智能批阅设置
            </h3>
            
            <el-form-item>
              <el-checkbox v-model="publishForm.enableAIGrading">
                <span style="font-weight: 500;">开启AI智能批阅</span>
              </el-checkbox>
              <div class="help-text" v-if="publishForm.enableAIGrading">
                <i class="el-icon-info"></i>
                系统将使用 TF-IDF 与余弦相似度算法，对填空题、简答题等主观题进行自动语义评分并给出建议分
              </div>
            </el-form-item>

            <el-form-item label="答案查看控制">
              <el-radio-group v-model="publishForm.answerViewControl">
                <el-radio label="after_submit">提交后可查看</el-radio>
                <el-radio label="after_grading">教师批阅后可查看</el-radio>
                <el-radio label="never">不允许查看</el-radio>
              </el-radio-group>
            </el-form-item>
          </div>

          <!-- 第四部分：基础防作弊 -->
          <div class="form-card">
            <h3 class="card-title">基础防作弊</h3>
            
            <el-form-item>
              <div class="checkbox-group">
                <el-checkbox v-model="publishForm.randomQuestions">题目乱序</el-checkbox>
                <span class="help-text">确保不同学生看到的题目排列顺序随机</span>
              </div>
            </el-form-item>

            <el-form-item>
              <div class="checkbox-group">
                <el-checkbox v-model="publishForm.randomOptions">选项乱序</el-checkbox>
                <span class="help-text">确保多选题/单选题的选项顺序随机</span>
              </div>
            </el-form-item>
          </div>

        </el-form>
      </div>

      <!-- 底部操作栏 -->
      <div class="footer-actions">
        <el-button size="large" @click="cancel">取消</el-button>
        <el-button type="primary" size="large" @click="confirmPublish" :loading="publishing">
          发布作业
        </el-button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HomeworkPublish',
  data() {
    return {
      publishing: false,
      homework: {
        id: null,
        name: '新建作业20260107184356',
        questionCount: 10,
        totalScore: 100
      },
      publishForm: {
        termId: '', // 新增班期ID
        targets: [],
        startTime: '',
        deadline: '',
        passingScore: 60,
        allowRedo: false,
        enableAIGrading: true,
        answerViewControl: 'after_grading',
        randomQuestions: false,
        randomOptions: false
      },
      originalForm: null,
      termList: [
        { id: 1, name: '2024春季班', startDate: '2024-03-01', endDate: '2024-06-30' },
        { id: 2, name: '2024秋季班', startDate: '2024-09-01', endDate: '2025-01-15' },
        { id: 3, name: '2025春季班', startDate: '2025-03-01', endDate: '2025-06-30' }
      ],
      classList: [
        { id: 1, name: '计算机科学2021级1班', studentCount: 45, termId: 1 },
        { id: 2, name: '计算机科学2021级2班', studentCount: 42, termId: 1 },
        { id: 3, name: '软件工程2021级1班', studentCount: 48, termId: 2 },
        { id: 4, name: '软件工程2022级1班', studentCount: 50, termId: 2 },
        { id: 5, name: '数据科学2023级1班', studentCount: 38, termId: 3 }
      ],
      studentList: [
        { id: 1, name: '张三', termId: 1 },
        { id: 2, name: '李四', termId: 1 },
        { id: 3, name: '王五', termId: 2 }
      ],
      rules: {
        termId: [
          { required: true, message: '请选择班期', trigger: 'change' }
        ],
        targets: [
          { required: true, message: '请选择发放对象', trigger: 'change' }
        ],
        startTime: [
          { required: true, message: '请选择起始时间', trigger: 'change' }
        ],
        deadline: [
          { required: true, message: '请选择截止时间', trigger: 'change' }
        ],
        passingScore: [
          { required: true, message: '请设置及格标准', trigger: 'blur' }
        ]
      },
      startTimeOptions: {
        disabledDate(time) {
          return time.getTime() < Date.now() - 8.64e7
        }
      },
      deadlineOptions: {
        disabledDate: (time) => {
          if (this.publishForm.startTime) {
            return time.getTime() < new Date(this.publishForm.startTime).getTime()
          }
          return time.getTime() < Date.now() - 8.64e7
        }
      }
    }
  },
  mounted() {
    const homeworkId = this.$route.params.id
    this.homework.id = homeworkId
    // TODO: 从后端加载作业信息
    console.log('加载作业信息:', homeworkId)
    
    // 保存原始表单数据用于重置
    this.originalForm = JSON.parse(JSON.stringify(this.publishForm))
  },
  computed: {
    // 根据选择的班期过滤班级
    filteredClassList() {
      if (!this.publishForm.termId) {
        return []
      }
      return this.classList.filter(cls => cls.termId === this.publishForm.termId)
    },
    // 根据选择的班期过滤学生
    filteredStudentList() {
      if (!this.publishForm.termId) {
        return []
      }
      return this.studentList.filter(student => student.termId === this.publishForm.termId)
    }
  },
  methods: {
    // 班期变化时清空已选对象
    handleTermChange() {
      this.publishForm.targets = []
    },
    goBack() {
      this.$router.back()
    },
    
    resetForm() {
      this.$confirm('确定要重置所有设置吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.publishForm = JSON.parse(JSON.stringify(this.originalForm))
        this.$message.success('已重置')
      }).catch(() => {})
    },
    
    cancel() {
      this.$confirm('取消后将不保存本次发布设置，确定要取消吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '再想想',
        type: 'warning'
      }).then(() => {
        this.$router.back()
      }).catch(() => {})
    },
    
    confirmPublish() {
      this.$refs.publishForm.validate((valid) => {
        if (valid) {
          // 验证截止时间必须晚于起始时间
          if (this.publishForm.startTime && this.publishForm.deadline) {
            if (new Date(this.publishForm.deadline) <= new Date(this.publishForm.startTime)) {
              this.$message.error('截止时间必须晚于起始时间')
              return false
            }
          }
          
          this.$confirm('确认发布该作业吗？发布后学生将可以看到并提交作业。', '确认发布', {
            confirmButtonText: '确认发布',
            cancelButtonText: '取消',
            type: 'info'
          }).then(() => {
            this.publishing = true
            
            const publishData = {
              ...this.publishForm,
              homeworkId: this.homework.id
            }
            
            // TODO: 调用发布接口
            console.log('发布数据:', publishData)
            
            setTimeout(() => {
              this.publishing = false
              this.$message.success('发布成功！')
              // 返回课程详情页
              this.$router.push('/teacher/courses')
            }, 1000)
          }).catch(() => {})
        } else {
          this.$message.warning('请完善必填信息')
          return false
        }
      })
    }
  }
}
</script>

<style scoped lang="scss">
.homework-publish {
  min-height: 100vh;
  background-color: #F5F5F5;
  padding: 20px;

  .publish-container {
    max-width: 900px;
    margin: 0 auto;

    .header-section {
      background: #FFFFFF;
      border-radius: 8px;
      padding: 24px 32px;
      margin-bottom: 20px;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
      display: flex;
      justify-content: space-between;
      align-items: center;

      .title-area {
        display: flex;
        align-items: center;
        gap: 12px;

        .homework-title {
          margin: 0;
          font-size: 22px;
          font-weight: 600;
          color: #303133;
        }
      }

      .quick-actions {
        display: flex;
        gap: 12px;
      }
    }

    .publish-content {
      .form-card {
        background: #FFFFFF;
        border-radius: 8px;
        padding: 24px 32px;
        margin-bottom: 20px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);

        &.highlight-card {
          border: 2px solid #E6F7FF;
          background: linear-gradient(to bottom, #FFFFFF 0%, #F0F9FF 100%);
        }

        .card-title {
          margin: 0 0 24px 0;
          font-size: 16px;
          font-weight: 600;
          color: #303133;
          padding-bottom: 12px;
          border-bottom: 2px solid #F0F0F0;
          display: flex;
          align-items: center;
        }

        .el-form-item {
          margin-bottom: 24px;

          &:last-child {
            margin-bottom: 0;
          }
        }

        .checkbox-group {
          display: flex;
          flex-direction: column;
          gap: 8px;
        }

        .help-text {
          margin-top: 8px;
          font-size: 13px;
          color: #909399;
          line-height: 1.6;
          display: flex;
          align-items: flex-start;
          gap: 6px;

          i {
            margin-top: 2px;
          }
        }
      }
    }

    .footer-actions {
      background: #FFFFFF;
      border-radius: 8px;
      padding: 20px 32px;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
      display: flex;
      justify-content: flex-end;
      gap: 12px;
      position: sticky;
      bottom: 20px;

      .el-button {
        min-width: 120px;
      }
    }
  }
}

::v-deep .el-form-item__label {
  font-weight: 500;
  color: #303133;
  padding-bottom: 8px;
}

::v-deep .el-switch__label {
  font-size: 13px;
}

::v-deep .el-radio {
  margin-right: 20px;
  margin-bottom: 12px;
}
</style>
