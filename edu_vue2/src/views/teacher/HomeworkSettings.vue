<template>
  <div class="homework-settings">
    <div class="settings-container">
      <!-- 页面顶部：信息确认区 -->
      <div class="header-section">
        <div class="title-area">
          <h2 class="homework-title">{{ homework.name }}</h2>
          <el-tag :type="getStatusType(homework.status)" size="small">{{ homework.status }}</el-tag>
        </div>
        <div class="quick-actions">
          <el-button icon="el-icon-back" @click="goBack">返回</el-button>
          <el-button icon="el-icon-refresh-left" @click="resetForm">重置</el-button>
        </div>
      </div>

      <!-- 核心设置区 -->
      <div class="settings-content">
        <el-form :model="settingsForm" :rules="rules" ref="settingsForm" label-position="top">
          
          <!-- 第一部分：发布范围与时间 -->
          <div class="form-card">
            <h3 class="card-title">发布范围与时间</h3>
            
            <el-form-item label="发放对象">
              <div class="readonly-targets">
                <el-tag
                  v-for="(target, index) in displayTargets"
                  :key="index"
                  size="medium"
                  style="margin-right: 8px; margin-bottom: 8px;"
                >
                  {{ target }}
                </el-tag>
              </div>
              <div style="margin-top: 8px; font-size: 12px; color: #909399;">
                发放对象不可修改
              </div>
            </el-form-item>

            <el-form-item label="起始时间" prop="startTime">
              <el-date-picker
                v-model="settingsForm.startTime"
                type="datetime"
                placeholder="选择起始时间"
                style="width: 100%"
                :picker-options="startTimeOptions"
              />
            </el-form-item>

            <el-form-item label="截止时间" prop="deadline">
              <el-date-picker
                v-model="settingsForm.deadline"
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
                v-model="settingsForm.passingScore" 
                :min="0" 
                :max="homework.totalScore"
                placeholder="分值"
                style="width: 200px"
              />
              <span style="margin-left: 8px; color: #606266;">分（总分 {{ homework.totalScore }} 分）</span>
            </el-form-item>

            <el-form-item label="允许重做">
              <el-switch 
                v-model="settingsForm.allowRedo"
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
              <el-checkbox v-model="settingsForm.enableAIGrading">
                <span style="font-weight: 500;">开启AI智能批阅</span>
              </el-checkbox>
              <div class="help-text" v-if="settingsForm.enableAIGrading">
                <i class="el-icon-info"></i>
                系统将使用 TF-IDF 与余弦相似度算法，对填空题、简答题等主观题进行自动语义评分并给出建议分
              </div>
            </el-form-item>

            <el-form-item label="答案查看控制">
              <el-radio-group v-model="settingsForm.answerViewControl">
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
                <el-checkbox v-model="settingsForm.randomQuestions">题目乱序</el-checkbox>
                <span class="help-text">确保不同学生看到的题目排列顺序随机</span>
              </div>
            </el-form-item>

            <el-form-item>
              <div class="checkbox-group">
                <el-checkbox v-model="settingsForm.randomOptions">选项乱序</el-checkbox>
                <span class="help-text">确保多选题/单选题的选项顺序随机</span>
              </div>
            </el-form-item>
          </div>

        </el-form>
      </div>

      <!-- 底部操作栏 -->
      <div class="footer-actions">
        <el-button size="large" @click="cancel">取消</el-button>
        <el-button type="primary" size="large" @click="confirmUpdate" :loading="updating">
          保存修改
        </el-button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HomeworkSettings',
  data() {
    return {
      updating: false,
      homework: {
        id: null,
        name: '函数进阶练习',
        questionCount: 10,
        totalScore: 100,
        status: '进行中'
      },
      originalTargets: ['计算机科学2021级1班', '计算机科学2021级2班'],
      settingsForm: {
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
      classList: [
        { id: 1, name: '计算机科学2021级1班', studentCount: 45 },
        { id: 2, name: '计算机科学2021级2班', studentCount: 42 }
      ],
      rules: {
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
          if (this.settingsForm.startTime) {
            return time.getTime() < new Date(this.settingsForm.startTime).getTime()
          }
          return time.getTime() < Date.now() - 8.64e7
        }
      }
    }
  },
  computed: {
    displayTargets() {
      return this.originalTargets
    }
  },
  mounted() {
    const homeworkId = this.$route.params.id
    this.homework.id = homeworkId
    this.loadHomeworkSettings()
  },
  methods: {
    loadHomeworkSettings() {
      // TODO: 从后端加载作业设置信息
      console.log('加载作业设置:', this.homework.id)
      
      // 模拟加载已有设置
      this.settingsForm = {
        deadline: new Date('2024-01-20 23:59'),
        passingScore: 60,
        allowRedo: true,
        enableAIGrading: true,
        answerViewControl: 'after_grading',
        randomQuestions: false,
        randomOptions: true
      }
      
      // 保存原始数据用于重置
      this.originalForm = JSON.parse(JSON.stringify(this.settingsForm))
    },
    
    getStatusType(status) {
      const typeMap = {
        '进行中': 'success',
        '未开始': 'info',
        '已结束': 'info'
      }
      return typeMap[status] || 'info'
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
        this.settingsForm = JSON.parse(JSON.stringify(this.originalForm))
        this.$message.success('已重置')
      }).catch(() => {})
    },
    
    cancel() {
      this.$confirm('取消后将不保存本次修改，确定要取消吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '再想想',
        type: 'warning'
      }).then(() => {
        this.$router.back()
      }).catch(() => {})
    },
    
    confirmUpdate() {
      this.$refs.settingsForm.validate((valid) => {
        if (valid) {
          // 验证截止时间必须晚于起始时间
          if (this.settingsForm.startTime && this.settingsForm.deadline) {
            if (new Date(this.settingsForm.deadline) <= new Date(this.settingsForm.startTime)) {
              this.$message.error('截止时间必须晚于起始时间')
              return false
            }
          }
          
          this.$confirm('确认保存修改吗？', '确认修改', {
            confirmButtonText: '确认保存',
            cancelButtonText: '取消',
            type: 'info'
          }).then(() => {
            this.updating = true
            
            const updateData = {
              ...this.settingsForm,
              homeworkId: this.homework.id
            }
            
            // TODO: 调用更新接口
            console.log('更新数据:', updateData)
            
            setTimeout(() => {
              this.updating = false
              this.$message.success('修改成功！')
              this.$router.back()
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
.homework-settings {
  min-height: 100vh;
  background-color: #F5F5F5;
  padding: 20px;

  .settings-container {
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

    .settings-content {
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

        .readonly-targets {
          display: flex;
          flex-wrap: wrap;
          padding: 12px;
          background-color: #F5F7FA;
          border-radius: 6px;
          min-height: 48px;

          .el-tag {
            background-color: #FFFFFF;
            border-color: #DCDFE6;
          }
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
