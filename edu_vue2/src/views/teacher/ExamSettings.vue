<template>
  <div class="exam-settings">
    <div class="settings-card">
      <!-- 页面顶部：基本信息区 -->
      <div class="header-section">
        <div class="exam-title-area">
          <h2 class="exam-title">{{ exam.name }}</h2>
          <el-tag :type="getStatusType(exam.status)" size="small">{{ exam.status }}</el-tag>
        </div>
        <div class="exam-meta">
          <span>共 {{ exam.questionCount }} 题</span>
          <span>总分 {{ exam.totalScore }} 分</span>
        </div>
      </div>

      <!-- 核心设置区 -->
      <div class="settings-section">
        <el-form :model="settingsForm" :rules="rules" ref="settingsForm" label-width="120px" label-position="left">
          
          <!-- 发放对象 - 只读显示 -->
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

          <!-- 时间排期 -->
          <el-form-item label="开始时间" prop="startTime">
            <el-date-picker
              v-model="settingsForm.startTime"
              type="datetime"
              placeholder="选择开始时间"
              style="width: 100%"
              :picker-options="startTimeOptions"
            />
            <el-checkbox v-model="settingsForm.startImmediately" style="margin-left: 12px;">立即开始</el-checkbox>
          </el-form-item>

          <el-form-item label="截止时间" prop="endTime">
            <el-date-picker
              v-model="settingsForm.endTime"
              type="datetime"
              placeholder="选择截止时间"
              style="width: 100%"
              :picker-options="endTimeOptions"
            />
          </el-form-item>

          <!-- 时长控制 -->
          <el-form-item label="考试限时" prop="duration">
            <el-input-number 
              v-model="settingsForm.duration" 
              :min="1" 
              :max="300"
              placeholder="分钟"
              style="width: 200px"
            />
            <span style="margin-left: 8px; color: #606266;">分钟</span>
          </el-form-item>

          <!-- 基础防作弊选项 -->
          <el-form-item label="防作弊设置">
            <div class="checkbox-group">
              <el-checkbox v-model="settingsForm.randomQuestions">题目乱序</el-checkbox>
              <el-tooltip content="不同学生看到的题目顺序随机" placement="top">
                <i class="el-icon-question" style="color: #909399; margin-left: 4px;"></i>
              </el-tooltip>
            </div>
            <div class="checkbox-group">
              <el-checkbox v-model="settingsForm.randomOptions">选项乱序</el-checkbox>
              <el-tooltip content="同一题目的选项顺序随机" placement="top">
                <i class="el-icon-question" style="color: #909399; margin-left: 4px;"></i>
              </el-tooltip>
            </div>
          </el-form-item>

          <!-- 交卷控制 -->
          <el-form-item label="允许交卷时间" prop="allowSubmitAfter">
            <el-input-number 
              v-model="settingsForm.allowSubmitAfter" 
              :min="0" 
              :max="settingsForm.duration"
              placeholder="分钟"
              style="width: 200px"
            />
            <span style="margin-left: 8px; color: #606266;">分钟后允许交卷</span>
            <div style="margin-top: 8px; font-size: 12px; color: #909399;">
              设置为0表示开考即可交卷
            </div>
          </el-form-item>

          <el-form-item label="切屏限制" prop="switchLimit">
            <el-input-number 
              v-model="settingsForm.switchLimit" 
              :min="0" 
              :max="10"
              placeholder="次数"
              style="width: 200px"
            />
            <span style="margin-left: 8px; color: #606266;">次，超过则强制收卷</span>
            <div style="margin-top: 8px; font-size: 12px; color: #909399;">
              设置为0表示不限制切屏
            </div>
          </el-form-item>

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
  name: 'ExamSettings',
  data() {
    return {
      updating: false,
      exam: {
        id: null,
        name: '第一单元测试',
        questionCount: 20,
        totalScore: 100,
        status: '进行中'
      },
      // 原始发放对象（只读）
      originalTargets: ['计算机科学2021级1班', '计算机科学2021级2班', '张三', '李四'],
      settingsForm: {
        startTime: '',
        startImmediately: false,
        endTime: '',
        duration: 120,
        randomQuestions: false,
        randomOptions: false,
        allowSubmitAfter: 30,
        switchLimit: 3
      },
      rules: {
        startTime: [
          { required: true, message: '请选择开始时间', trigger: 'change' }
        ],
        endTime: [
          { required: true, message: '请选择截止时间', trigger: 'change' }
        ],
        duration: [
          { required: true, message: '请设置考试时长', trigger: 'blur' }
        ]
      },
      startTimeOptions: {
        disabledDate(time) {
          return time.getTime() < Date.now() - 8.64e7
        }
      },
      endTimeOptions: {
        disabledDate: (time) => {
          if (this.settingsForm.startTime) {
            return time.getTime() < new Date(this.settingsForm.startTime).getTime()
          }
          return time.getTime() < Date.now()
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
    const examId = this.$route.params.id
    this.exam.id = examId
    this.loadExamSettings()
  },
  methods: {
    loadExamSettings() {
      // TODO: 从后端加载考试设置信息
      console.log('加载考试设置:', this.exam.id)
      
      // 模拟加载已有设置
      this.settingsForm = {
        startTime: new Date('2024-01-18 14:00'),
        startImmediately: false,
        endTime: new Date('2024-01-18 16:00'),
        duration: 120,
        randomQuestions: true,
        randomOptions: false,
        allowSubmitAfter: 30,
        switchLimit: 3
      }
    },
    
    getStatusType(status) {
      const typeMap = {
        '进行中': 'success',
        '未开始': 'info',
        '已结束': 'info'
      }
      return typeMap[status] || 'info'
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
          // 验证截止时间必须晚于开始时间
          if (new Date(this.settingsForm.endTime) <= new Date(this.settingsForm.startTime)) {
            this.$message.error('截止时间必须晚于开始时间')
            return
          }

          this.$confirm('确认保存修改吗？', '确认修改', {
            confirmButtonText: '确认保存',
            cancelButtonText: '取消',
            type: 'info'
          }).then(() => {
            this.updating = true
            
            // 处理立即开始
            const updateData = {
              ...this.settingsForm,
              examId: this.exam.id,
              startTime: this.settingsForm.startImmediately ? new Date() : this.settingsForm.startTime
            }
            
            // TODO: 调用更新接口
            console.log('更新数据:', updateData)
            
            setTimeout(() => {
              this.updating = false
              this.$message.success('修改成功！')
              // 返回课程详情页
              this.$router.back()
            }, 1000)
          }).catch(() => {})
        } else {
          this.$message.warning('请完善必填信息')
          return false
        }
      })
    }
  },
  watch: {
    'settingsForm.startImmediately'(val) {
      if (val) {
        this.settingsForm.startTime = new Date()
      }
    }
  }
}
</script>

<style scoped lang="scss">
.exam-settings {
  min-height: 100vh;
  background-color: #F5F5F5;
  padding: 40px 20px;
  display: flex;
  justify-content: center;
  align-items: flex-start;

  .settings-card {
    width: 100%;
    max-width: 800px;
    background: #FFFFFF;
    border-radius: 12px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
    overflow: hidden;

    .header-section {
      padding: 32px 40px;
      border-bottom: 1px solid #EBEEF5;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: #FFFFFF;

      .exam-title-area {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 12px;

        .exam-title {
          margin: 0;
          font-size: 24px;
          font-weight: 600;
        }

        .el-tag {
          background-color: rgba(255, 255, 255, 0.2);
          border-color: transparent;
          color: #FFFFFF;
        }
      }

      .exam-meta {
        display: flex;
        gap: 20px;
        font-size: 14px;
        opacity: 0.9;

        span:before {
          content: '•';
          margin-right: 6px;
        }

        span:first-child:before {
          content: '';
          margin-right: 0;
        }
      }
    }

    .settings-section {
      padding: 40px;

      .el-form-item {
        margin-bottom: 28px;

        ::v-deep .el-form-item__label {
          font-weight: 500;
          color: #303133;
        }
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

      .checkbox-group {
        display: flex;
        align-items: center;
        margin-bottom: 12px;

        &:last-child {
          margin-bottom: 0;
        }
      }
    }

    .footer-actions {
      padding: 20px 40px;
      border-top: 1px solid #EBEEF5;
      background-color: #FAFAFA;
      display: flex;
      justify-content: flex-end;
      gap: 12px;

      .el-button {
        min-width: 100px;
      }
    }
  }
}
</style>
