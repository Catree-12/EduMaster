<template>
  <div class="exam-publish">
    <div class="publish-card">
      <!-- 页面顶部：基本信息区 -->
      <div class="header-section">
        <div class="exam-title-area">
          <h2 class="exam-title">{{ exam.name }}</h2>
          <el-tag type="info" size="small">待发布</el-tag>
        </div>
        <div class="exam-meta">
          <span>共 {{ exam.questionCount }} 题</span>
          <span>总分 {{ exam.totalScore }} 分</span>
        </div>
      </div>

      <!-- 核心设置区 -->
      <div class="settings-section">
        <el-form :model="publishForm" :rules="rules" ref="publishForm" label-width="120px" label-position="left">
          
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

          <!-- 发放对象 -->
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

          <!-- 时间排期 -->
          <el-form-item label="开始时间" prop="startTime">
            <el-date-picker
              v-model="publishForm.startTime"
              type="datetime"
              placeholder="选择开始时间"
              style="width: 100%"
              :picker-options="startTimeOptions"
            />
            <el-checkbox v-model="publishForm.startImmediately" style="margin-left: 12px;">立即开始</el-checkbox>
          </el-form-item>

          <el-form-item label="截止时间" prop="endTime">
            <el-date-picker
              v-model="publishForm.endTime"
              type="datetime"
              placeholder="选择截止时间"
              style="width: 100%"
              :picker-options="endTimeOptions"
            />
          </el-form-item>

          <!-- 时长控制 -->
          <el-form-item label="考试限时" prop="duration">
            <el-input-number 
              v-model="publishForm.duration" 
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
              <el-checkbox v-model="publishForm.randomQuestions">题目乱序</el-checkbox>
              <el-tooltip content="不同学生看到的题目顺序随机" placement="top">
                <i class="el-icon-question" style="color: #909399; margin-left: 4px;"></i>
              </el-tooltip>
            </div>
            <div class="checkbox-group">
              <el-checkbox v-model="publishForm.randomOptions">选项乱序</el-checkbox>
              <el-tooltip content="同一题目的选项顺序随机" placement="top">
                <i class="el-icon-question" style="color: #909399; margin-left: 4px;"></i>
              </el-tooltip>
            </div>
          </el-form-item>

          <!-- 交卷控制 -->
          <el-form-item label="允许交卷时间" prop="allowSubmitAfter">
            <el-input-number 
              v-model="publishForm.allowSubmitAfter" 
              :min="0" 
              :max="publishForm.duration"
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
              v-model="publishForm.switchLimit" 
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
        <el-button type="primary" size="large" @click="confirmPublish" :loading="publishing">
          确认发布
        </el-button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ExamPublish',
  data() {
    return {
      publishing: false,
      exam: {
        id: null,
        name: '新建试卷20260107184356',
        questionCount: 20,
        totalScore: 100
      },
      publishForm: {
        termId: '', // 新增班期ID
        targets: [],
        startTime: '',
        startImmediately: false,
        endTime: '',
        duration: 120,
        randomQuestions: false,
        randomOptions: false,
        allowSubmitAfter: 30,
        switchLimit: 3
      },
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
          if (this.publishForm.startTime) {
            return time.getTime() < new Date(this.publishForm.startTime).getTime()
          }
          return time.getTime() < Date.now()
        }
      }
    }
  },
  mounted() {
    const examId = this.$route.params.id
    this.exam.id = examId
    // TODO: 从后端加载试卷信息
    console.log('加载试卷信息:', examId)
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
          // 验证截止时间必须晚于开始时间
          if (new Date(this.publishForm.endTime) <= new Date(this.publishForm.startTime)) {
            this.$message.error('截止时间必须晚于开始时间')
            return
          }

          this.$confirm('确认发布该试卷吗？发布后学生将在指定时间看到考试。', '确认发布', {
            confirmButtonText: '确认发布',
            cancelButtonText: '取消',
            type: 'info'
          }).then(() => {
            this.publishing = true
            
            // 处理立即开始
            const publishData = {
              ...this.publishForm,
              examId: this.exam.id,
              startTime: this.publishForm.startImmediately ? new Date() : this.publishForm.startTime
            }
            
            // TODO: 调用发布接口
            console.log('发布数据:', publishData)
            
            setTimeout(() => {
              this.publishing = false
              this.$message.success('发布成功！')
              // 返回课程列表页
              this.$router.push('/courses/mycourses')
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
    'publishForm.startImmediately'(val) {
      if (val) {
        this.publishForm.startTime = new Date()
      }
    }
  }
}
</script>

<style scoped lang="scss">
.exam-publish {
  min-height: 100vh;
  background-color: #F5F5F5;
  padding: 40px 20px;
  display: flex;
  justify-content: center;
  align-items: flex-start;

  .publish-card {
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

::v-deep .el-select-dropdown__item {
  height: auto;
  padding: 8px 20px;
}
</style>
