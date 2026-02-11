<template>
  <div class="course-create-container">
    <div class="page-header">
      <el-button icon="el-icon-arrow-left" circle @click="goBack"></el-button>
      <div class="header-content">
        <h1 class="page-title">创建新课程</h1>
        <p class="page-subtitle">填写课程基本信息，开启教学之旅</p>
      </div>
    </div>

    <div class="create-form-wrapper">
      <div class="form-layout">
        <div class="form-card">
          <el-form
            ref="courseForm"
            :model="courseForm"
            :rules="rules"
            label-width="100px"
            size="medium"
          >
            <div class="form-section">
              <div class="section-header">
                <i class="el-icon-document section-icon"></i>
                <h3 class="section-title">基本信息</h3>
              </div>
              
              <el-form-item label="课程名称" prop="title">
                <el-input
                  v-model="courseForm.title"
                  placeholder="请输入课程名称"
                  maxlength="100"
                  show-word-limit
                />
              </el-form-item>

              <el-form-item label="课程分类" prop="category">
                <el-select 
                  v-model="courseForm.category" 
                  placeholder="请选择分类" 
                  style="width: 100%;"
                  filterable
                >
                  <el-option label="计算机" value="计算机" />
                  <el-option label="经济学" value="经济学" />
                  <el-option label="农林园艺" value="农林园艺" />
                  <el-option label="医药卫生" value="医药卫生" />
                  <el-option label="理学" value="理学" />
                  <el-option label="历史" value="历史" />
                  <el-option label="哲学" value="哲学" />
                  <el-option label="法学" value="法学" />
                  <el-option label="文学文化" value="文学文化" />
                  <el-option label="艺术设计" value="艺术设计" />
                  <el-option label="外语" value="外语" />
                  <el-option label="教育教学" value="教育教学" />
                  <el-option label="管理学" value="管理学" />
                  <el-option label="工学" value="工学" />
                  <el-option label="其他" value="其他" />
                </el-select>
              </el-form-item>

              <el-form-item label="难度等级" prop="difficulty">
                <el-radio-group v-model="courseForm.difficulty" size="medium">
                  <el-radio-button label="初级">初级</el-radio-button>
                  <el-radio-button label="中级">中级</el-radio-button>
                  <el-radio-button label="高级">高级</el-radio-button>
                </el-radio-group>
              </el-form-item>

              <el-form-item label="课程描述">
                <el-input
                  v-model="courseForm.description"
                  type="textarea"
                  rows="6"
                  placeholder="请输入课程描述（选填）"
                  maxlength="500"
                  show-word-limit
                />
              </el-form-item>

              <el-form-item label="课程封面">
                <el-upload
                  ref="coverUpload"
                  action="/api/upload/image"
                  :on-success="handleUploadSuccess"
                  :on-error="handleUploadError"
                  :show-file-list="false"
                  accept="image/*"
                >
                  <el-button size="small" icon="el-icon-upload">
                    {{ courseForm.cover ? '更换封面' : '上传封面' }}
                  </el-button>
                  <div slot="tip" class="el-upload__tip">
                    建议尺寸: 800x600px，支持jpg/png格式
                  </div>
                </el-upload>
              </el-form-item>
            </div>

            <div class="form-actions">
              <el-button size="large" @click="goBack">取消</el-button>
              <el-button type="primary" size="large" :loading="submitting" @click="createCourse">
                {{ submitting ? '创建中...' : '创建课程' }}
              </el-button>
            </div>
          </el-form>
        </div>

        <div class="preview-card">
          <div class="preview-header">
            <i class="el-icon-view"></i>
            <span>课程预览</span>
          </div>
          <div class="preview-content">
            <div class="preview-cover">
              <img v-if="courseForm.cover" :src="courseForm.cover" alt="课程封面" />
              <div v-else class="no-cover">
                <i class="el-icon-picture-outline"></i>
                <p>暂无封面预览</p>
              </div>
            </div>
            <div class="preview-info">
              <div class="preview-tags">
                <el-tag :type="difficultyTag.type" size="mini" effect="dark">
                  {{ difficultyTag.label }}
                </el-tag>
                <el-tag v-if="courseForm.category" type="info" size="mini" style="margin-left: 8px">
                  {{ courseForm.category }}
                </el-tag>
              </div>
              
              <h3 class="preview-title">{{ courseForm.title || '尚未输入课程名称' }}</h3>
              
              <p class="preview-desc">{{ courseForm.description || '暂无描述内容...' }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CourseCreate',
  data() {
    return {
      courseForm: {
        title: '',
        description: '',
        category: '', // 单选：对应后端 ForeignKey
        difficulty: '初级', // 默认初级
        cover: '' // 封面图片URL
      },
      rules: {
        title: [
          { required: true, message: '请输入课程名称', trigger: 'blur' },
          { min: 1, max: 20, message: '长度在 1 到 20 个字符', trigger: 'blur' }
        ],
        category: [
          { required: true, message: '请选择课程分类', trigger: 'change' }
        ],
        difficulty: [
          { required: true, message: '请选择难度等级', trigger: 'change' }
        ]
      },
      submitting: false
    }
  },
  computed: {
    // 动态计算难度标签的样式和文字
    difficultyTag() {
      const maps = {
        beginner: { label: '初级', type: 'success' },
        intermediate: { label: '中级', type: 'warning' },
        advanced: { label: '高级', type: 'danger' }
      }
      return maps[this.courseForm.difficulty] || maps.beginner
    }
  },
  methods: {
    handleUploadSuccess(res) {
      // 根据后端返回结构处理
      if (res.code === 200) {
        this.courseForm.cover = res.data.url || res.data
        this.$message.success('封面上传成功')
      } else {
        this.$message.error(res.message || '上传失败')
      }
    },
    handleUploadError() {
      this.$message.error('图片上传失败')
    },
    async createCourse() {
      this.$refs.courseForm.validate(async (valid) => {
        if (!valid) return
        
        this.submitting = true
        try {
          // 调用后端创建课程接口
          const { teacherAPI } = require('@/api')
          
          // 准备请求数据(只发送后端需要的字段)
          const requestData = {
            title: this.courseForm.title,
            description: this.courseForm.description,
            category: this.courseForm.category, // 传分类名称
            difficulty: this.courseForm.difficulty,
            cover: this.courseForm.cover // 如果后端需要封面URL，可以直接传

          }
          
          // 如果有封面则添加
          if (this.courseForm.cover) {
            requestData.cover = this.courseForm.cover
          }
          
          // 调用API创建课程
          const response = await teacherAPI.createCourse(requestData)
          
          this.$message.success('课程创建成功')
          
          // 跳转到课程编辑页面(可以继续编辑章节等)
          if (response.course_id) {
            this.$router.push({
              path: `/teacher/course/${response.course_id}`,
              query: { new: 'true' }
            })
          } else {
            // 如果没有返回course_id,跳转到课程列表
            this.$router.push('/courses/mycourses')
          }
        } catch (error) {
          console.error('创建课程失败:', error)
          this.$message.error(error.message || '创建失败,请稍后重试')
        } finally {
          this.submitting = false
        }
      })
    },
    goBack() {
      this.$router.back()
    }
  }
}
</script>

<style scoped lang="scss">
/* 保持你原有的样式基础上，微调预览区 */
.course-create-container {
  padding: 20px;
  background: #f5f7fa;
  min-height: 100vh;
}

.page-header {
  margin-bottom: 24px;
  background: white;
  padding: 20px 30px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  gap: 16px;
  border-left: 5px solid #667eea;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);

  .header-content {
    .page-title { margin: 0; font-size: 22px; color: #303133; }
    .page-subtitle { margin: 4px 0 0 0; font-size: 13px; color: #909399; }
  }
}

.create-form-wrapper {
  max-width: 1200px;
  margin: 0 auto;

  .form-layout {
    display: grid;
    grid-template-columns: 1fr 380px;
    gap: 24px;
  }

  .form-card {
    background: white;
    border-radius: 12px;
    padding: 30px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.05);
  }

  .section-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 25px;
    border-bottom: 1px solid #f0f0f0;
    padding-bottom: 15px;
    .section-icon { color: #667eea; font-size: 20px; }
    .section-title { margin: 0; font-size: 17px; }
  }
}

.preview-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  height: fit-content;
  position: sticky;
  top: 20px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.05);

  .preview-header {
    margin-bottom: 15px;
    font-weight: bold;
    display: flex;
    align-items: center;
    gap: 8px;
    color: #606266;
  }

  .preview-cover {
    width: 100%;
    height: 190px;
    background: #f5f7fa;
    border-radius: 8px;
    overflow: hidden;
    img { width: 100%; height: 100%; object-fit: cover; }
    .no-cover {
      height: 100%;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      color: #c0c4cc;
      i { font-size: 40px; }
    }
  }

  .preview-info {
    padding: 15px 5px;
    .preview-tags { margin-bottom: 10px; }
    .preview-title { margin: 0 0 10px 0; font-size: 18px; color: #303133; }
    .preview-desc { font-size: 13px; color: #909399; line-height: 1.6; }
  }
}

.form-actions {
  margin-top: 30px;
  text-align: right;
  border-top: 1px solid #f0f0f0;
  padding-top: 20px;
}
</style>