<template>
  <div class="course-edit-container">
    <div class="page-header">
      <el-button icon="el-icon-arrow-left" type="text" @click="goBack">返回</el-button>
      <h1>编辑课程</h1>
    </div>

    <!-- 加载中 -->
    <div v-if="loading" class="loading-container">
      <el-skeleton :rows="10" animated />
    </div>

    <!-- 编辑表单 -->
    <div v-else class="edit-form-wrapper">
      <el-card shadow="hover">
        <el-tabs v-model="activeTab" type="card">
          <!-- 基本信息标签 -->
          <el-tab-pane label="基本信息" name="basic">
            <el-form
              ref="basicForm"
              :model="courseForm"
              :rules="basicRules"
              label-width="120px"
              size="medium"
            >
              <el-form-item label="课程名称" prop="title">
                <el-input
                  v-model="courseForm.title"
                  placeholder="请输入课程名称"
                  maxlength="100"
                  show-word-limit
                />
              </el-form-item>

              <el-form-item label="课程描述" prop="description">
                <el-input
                  v-model="courseForm.description"
                  type="textarea"
                  rows="4"
                  placeholder="请输入课程描述"
                  maxlength="500"
                  show-word-limit
                />
              </el-form-item>

              <el-form-item label="课程分类" prop="category">
                <el-select v-model="courseForm.category" placeholder="请选择分类">
                  <el-option label="Web 前端" value="web" />
                  <el-option label="后端开发" value="backend" />
                  <el-option label="移动开发" value="mobile" />
                  <el-option label="数据科学" value="data" />
                  <el-option label="DevOps" value="devops" />
                  <el-option label="其他" value="other" />
                </el-select>
              </el-form-item>

              <el-form-item label="课程价格" prop="price">
                <el-input-number
                  v-model="courseForm.price"
                  :min="0"
                  :max="99999"
                  controls-position="right"
                />
                <span class="unit">元</span>
              </el-form-item>

              <el-form-item label="课程封面" prop="coverImage">
                <el-upload
                  action="/api/upload/image"
                  :file-list="fileList"
                  :on-success="handleUploadSuccess"
                  limit="1"
                  accept="image/*"
                >
                  <el-button slot="trigger" type="primary" size="small">
                    更新图片
                  </el-button>
                </el-upload>
                <div v-if="courseForm.coverImage" class="preview">
                  <img :src="courseForm.coverImage" alt="封面预览" />
                </div>
              </el-form-item>

              <el-form-item label="学习人数" prop="capacity">
                <el-input-number
                  v-model="courseForm.capacity"
                  :min="1"
                  :max="10000"
                  controls-position="right"
                />
              </el-form-item>

              <el-form-item label="学习周期" prop="duration">
                <el-select v-model="courseForm.duration" placeholder="请选择课程时长">
                  <el-option label="4 周" value="4" />
                  <el-option label="8 周" value="8" />
                  <el-option label="12 周" value="12" />
                  <el-option label="16 周" value="16" />
                  <el-option label="自定进度" value="0" />
                </el-select>
              </el-form-item>

              <el-form-item label="难度级别" prop="level">
                <el-select v-model="courseForm.level" placeholder="请选择难度级别">
                  <el-option label="入门" value="beginner" />
                  <el-option label="中级" value="intermediate" />
                  <el-option label="高级" value="advanced" />
                  <el-option label="专家" value="expert" />
                </el-select>
              </el-form-item>

              <el-form-item label="前置要求" prop="prerequisites">
                <el-input
                  v-model="courseForm.prerequisites"
                  type="textarea"
                  rows="3"
                  placeholder="请输入学习本课程的前置要求（如有）"
                  maxlength="200"
                />
              </el-form-item>

              <el-form-item label="学习目标" prop="objectives">
                <el-input
                  v-model="courseForm.objectives"
                  type="textarea"
                  rows="4"
                  placeholder="请输入学生完成本课程后将学到什么"
                  maxlength="500"
                />
              </el-form-item>
            </el-form>
          </el-tab-pane>

          <!-- 课程内容标签 -->
          <el-tab-pane label="课程内容" name="content">
            <div class="content-section">
              <div class="section-header">
                <div>
                  <h3>章节管理</h3>
                  <p class="tip">在这里管理课程章节、课时和资源</p>
                </div>
                <el-button type="primary" icon="el-icon-plus" @click="handleAddChapter">添加章节</el-button>
              </div>

              <div class="chapter-list">
                <div v-for="(chapter, index) in chapters" :key="chapter.id" class="chapter-item">
                  <div class="chapter-header">
                    <div class="chapter-title">
                      <span class="chapter-index">第 {{ index + 1 }} 章</span>
                      <span v-if="!chapter.isEditing">{{ chapter.title }}</span>
                      <el-input 
                        v-else 
                        v-model="chapter.editTitle" 
                        size="small" 
                        style="width: 300px"
                        ref="chapterInput"
                      >
                        <el-button slot="append" icon="el-icon-check" @click="saveChapter(chapter)"></el-button>
                      </el-input>
                    </div>
                    <div class="chapter-actions">
                      <el-button type="text" icon="el-icon-plus" @click="handleAddLesson(chapter)">添加课时</el-button>
                      <el-button type="text" icon="el-icon-edit" @click="editChapter(chapter)">编辑</el-button>
                      <el-button type="text" icon="el-icon-delete" class="text-danger" @click="deleteChapter(index)">删除</el-button>
                    </div>
                  </div>

                  <div class="lesson-list">
                    <div v-for="(lesson, lIndex) in chapter.lessons" :key="lesson.id" class="lesson-item">
                      <div class="lesson-info">
                        <i class="el-icon-video-play lesson-icon" v-if="lesson.type === 'video'"></i>
                        <i class="el-icon-document lesson-icon" v-else></i>
                        <span class="lesson-index">{{ index + 1 }}-{{ lIndex + 1 }}</span>
                        <span>{{ lesson.title }}</span>
                        <el-tag size="mini" type="info" class="lesson-type-tag">{{ lesson.type === 'video' ? '视频' : '文档' }}</el-tag>
                      </div>
                      <div class="lesson-actions">
                        <el-button type="text" size="small" @click="editLesson(lesson)">编辑</el-button>
                        <el-button type="text" size="small" @click="uploadResource(lesson)">资源</el-button>
                        <el-button type="text" size="small" class="text-danger" @click="deleteLesson(chapter, lIndex)">删除</el-button>
                      </div>
                    </div>
                    <div v-if="chapter.lessons.length === 0" class="empty-lesson">
                      暂无课时，请点击上方"添加课时"
                    </div>
                  </div>
                </div>

                <div v-if="chapters.length === 0" class="empty-chapter">
                  <i class="el-icon-folder-opened"></i>
                  <p>暂无章节，请点击右上角添加</p>
                </div>
              </div>
            </div>
          </el-tab-pane>

          <!-- 班期管理标签 -->
          <el-tab-pane label="班期管理" name="terms">
            <div class="terms-section">
              <h3>班期与班级</h3>
              <p class="tip">为课程创建班期，在班期内创建班级</p>
              
              <!-- 班期选择和操作 -->
              <div class="term-controls">
                <el-select
                  v-model="selectedTermId"
                  placeholder="请选择班期"
                  clearable
                  style="width: 200px"
                >
                  <el-option
                    v-for="term in courseTerms"
                    :key="term.id"
                    :label="`${term.name} (${term.startDate} ~ ${term.endDate})`"
                    :value="term.id"
                  />
                </el-select>
                <el-button type="primary" @click="goToTermManagement" icon="el-icon-edit">
                  班期管理
                </el-button>
                <el-button type="primary" @click="goToClassManagement" icon="el-icon-circle-plus">
                  班级管理
                </el-button>
              </div>

              <!-- 班期列表 -->
              <div v-if="courseTerms.length > 0" class="term-list">
                <h4>班期列表</h4>
                <el-table :data="courseTerms" style="width: 100%">
                  <el-table-column prop="name" label="班期名称" width="120" />
                  <el-table-column prop="startDate" label="开始日期" width="120" />
                  <el-table-column prop="endDate" label="结束日期" width="120" />
                  <el-table-column prop="status" label="状态" width="100">
                    <template slot-scope="scope">
                      <el-tag :type="getStatusType(scope.row.status)">
                        {{ getStatusText(scope.row.status) }}
                      </el-tag>
                    </template>
                  </el-table-column>
                  <el-table-column prop="classCount" label="班级数" width="80" />
                  <el-table-column prop="studentCount" label="学生数" width="80" />
                  <el-table-column label="操作" width="150">
                    <template slot-scope="scope">
                      <el-button type="text" size="small" @click="viewTermClasses(scope.row)">
                        查看班级
                      </el-button>
                      <el-button type="text" size="small" @click="editTerm(scope.row)">
                        编辑
                      </el-button>
                    </template>
                  </el-table-column>
                </el-table>
              </div>

              <!-- 空状态 -->
              <div v-else class="empty-term">
                <i class="el-icon-document-copy" />
                <p>还没有为此课程创建班期</p>
                <p class="tip">请先在<strong>班期管理</strong>页面为该课程创建班期</p>
              </div>

              <!-- 班级列表 -->
              <div v-if="selectedTermId && termClasses.length > 0" class="class-list">
                <h4>班级列表 (班期: {{ getTermName(selectedTermId) }})</h4>
                <el-table :data="termClasses" style="width: 100%">
                  <el-table-column prop="name" label="班级名称" width="120" />
                  <el-table-column prop="code" label="班级代码" width="100" />
                  <el-table-column prop="teacherName" label="班级教师" width="120" />
                  <el-table-column prop="studentCount" label="学生数" width="80" />
                  <el-table-column prop="capacity" label="容纳人数" width="80" />
                  <el-table-column prop="status" label="状态" width="100">
                    <template slot-scope="scope">
                      <el-tag :type="getStatusType(scope.row.status)">
                        {{ getStatusText(scope.row.status) }}
                      </el-tag>
                    </template>
                  </el-table-column>
                  <el-table-column label="操作" width="150">
                    <template slot-scope="scope">
                      <el-button type="text" size="small" @click="editClass(scope.row)">
                        编辑
                      </el-button>
                      <el-button type="text" size="small" @click="viewClassStudents(scope.row)">
                        学生
                      </el-button>
                    </template>
                  </el-table-column>
                </el-table>
              </div>
            </div>
          </el-tab-pane>
        </el-tabs>

        <!-- 保存按钮 -->
        <div class="form-actions">
          <el-button @click="goBack">取消</el-button>
          <el-button type="primary" :loading="submitting" @click="saveCourse">
            保存更改
          </el-button>
          <el-button
            v-if="courseForm.status === 'draft'"
            type="success"
            :loading="submitting"
            @click="publishCourse"
          >
            发布课程
          </el-button>
          <el-button
            v-if="courseForm.status === 'published'"
            type="warning"
            :loading="submitting"
            @click="archiveCourse"
          >
            下架课程
          </el-button>
        </div>
      </el-card>
    </div>

    <!-- 课时编辑对话框 -->
    <el-dialog
      :title="lessonForm.id ? '编辑课时' : '添加课时'"
      :visible.sync="lessonDialogVisible"
      width="500px"
      :close-on-click-modal="false"
    >
      <el-form :model="lessonForm" ref="lessonForm" label-width="80px">
        <el-form-item label="课时标题" prop="title" :rules="[{ required: true, message: '请输入标题', trigger: 'blur' }]">
          <el-input v-model="lessonForm.title" placeholder="请输入课时标题"></el-input>
        </el-form-item>
        <el-form-item label="课时类型">
          <el-radio-group v-model="lessonForm.type">
            <el-radio label="video">视频</el-radio>
            <el-radio label="doc">文档</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="视频链接" v-if="lessonForm.type === 'video'">
          <el-input v-model="lessonForm.videoUrl" placeholder="请输入视频链接 (如: https://...)">
            <el-button slot="append" icon="el-icon-upload" @click="handleUploadVideo">上传</el-button>
          </el-input>
        </el-form-item>
        <el-form-item label="文档内容" v-if="lessonForm.type === 'doc'">
          <el-input type="textarea" v-model="lessonForm.content" rows="6" placeholder="请输入文档内容或Markdown"></el-input>
        </el-form-item>
        <el-form-item label="时长(分)">
          <el-input-number v-model="lessonForm.duration" :min="0" :step="1"></el-input-number>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="lessonDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="submitLesson">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'CourseEdit',
  data() {
    return {
      courseId: this.$route.params.id,
      activeTab: 'basic',
      loading: false,
      submitting: false,
      courseForm: {
        title: '',
        description: '',
        category: '',
        price: 0,
        coverImage: '',
        capacity: 100,
        duration: '8',
        level: 'beginner',
        prerequisites: '',
        objectives: '',
        status: 'draft'
      },
      basicRules: {
        title: [
          { required: true, message: '请输入课程名称', trigger: 'blur' },
          { min: 3, message: '课程名称至少3个字符', trigger: 'blur' }
        ],
        description: [
          { required: true, message: '请输入课程描述', trigger: 'blur' },
          { min: 10, message: '课程描述至少10个字符', trigger: 'blur' }
        ],
        category: [
          { required: true, message: '请选择课程分类', trigger: 'change' }
        ]
      },
      fileList: [],
      // 班期管理数据
      courseTerms: [],
      termClasses: [],
      selectedTermId: null,
      // 章节管理数据
      chapters: [
        {
          id: 1,
          title: '第一章：Vue.js 简介',
          isEditing: false,
          lessons: [
            { id: 101, title: '1.1 什么是 Vue.js', type: 'video', videoUrl: '', duration: 10, isEditing: false },
            { id: 102, title: '1.2 环境搭建', type: 'doc', content: '安装 Node.js...', duration: 5, isEditing: false }
          ]
        },
        {
          id: 2,
          title: '第二章：基础语法',
          isEditing: false,
          lessons: [
            { id: 201, title: '2.1 模板语法', type: 'video', videoUrl: '', duration: 15, isEditing: false }
          ]
        }
      ],
      // 课时编辑对话框
      lessonDialogVisible: false,
      currentChapter: null,
      lessonForm: {
        id: null,
        title: '',
        type: 'video',
        videoUrl: '',
        content: '',
        duration: 0
      }
    }
  },
  created() {
    this.fetchCourse()
    this.fetchCourseTerms()
  },
  methods: {
    // 章节管理方法
    handleAddChapter() {
      const newChapter = {
        id: Date.now(),
        title: '新章节',
        isEditing: true,
        editTitle: '新章节',
        lessons: []
      }
      this.chapters.push(newChapter)
      this.$nextTick(() => {
        // 如果有ref引用可以聚焦，这里简化处理
      })
    },
    editChapter(chapter) {
      chapter.editTitle = chapter.title
      chapter.isEditing = true
    },
    saveChapter(chapter) {
      if (!chapter.editTitle.trim()) {
        this.$message.warning('章节标题不能为空')
        return
      }
      chapter.title = chapter.editTitle
      chapter.isEditing = false
      this.$message.success('章节标题已更新')
    },
    deleteChapter(index) {
      this.$confirm('确定要删除该章节及其所有课时吗？', '提示', {
        type: 'warning'
      }).then(() => {
        this.chapters.splice(index, 1)
        this.$message.success('章节已删除')
      })
    },
    handleAddLesson(chapter) {
      this.currentChapter = chapter
      this.lessonForm = {
        id: null,
        title: '',
        type: 'video',
        videoUrl: '',
        content: '',
        duration: 0
      }
      this.lessonDialogVisible = true
    },
    editLesson(lesson) {
      this.lessonForm = { ...lesson }
      this.lessonDialogVisible = true
    },
    submitLesson() {
      this.$refs.lessonForm.validate(valid => {
        if (valid) {
          if (this.lessonForm.id) {
            // 编辑现有课时
            // 找到对应的章节和课时进行更新
            for (const chapter of this.chapters) {
              const index = chapter.lessons.findIndex(l => l.id === this.lessonForm.id)
              if (index !== -1) {
                this.$set(chapter.lessons, index, { ...this.lessonForm, isEditing: false })
                break
              }
            }
            this.$message.success('课时已更新')
          } else {
            // 添加新课时
            const newLesson = {
              ...this.lessonForm,
              id: Date.now(),
              isEditing: false
            }
            this.currentChapter.lessons.push(newLesson)
            this.$message.success('课时已添加')
          }
          this.lessonDialogVisible = false
        }
      })
    },
    handleUploadVideo() {
      this.$message.info('视频上传功能开发中...')
    },
    deleteLesson(chapter, index) {
      this.$confirm('确定要删除该课时吗？', '提示', {
        type: 'warning'
      }).then(() => {
        chapter.lessons.splice(index, 1)
        this.$message.success('课时已删除')
      })
    },
    uploadResource(lesson) {
      this.$message.info(`为课时 "${lesson.title}" 上传资源 (功能开发中)`)
    },

    // 获取课程详情
    fetchCourse() {
      this.loading = true
      this.$api.get(`/courses/${this.courseId}`)
        .then(res => {
          this.courseForm = res.data
          if (res.data.coverImage) {
            this.fileList = [{
              url: res.data.coverImage,
              name: 'cover'
            }]
          }
          this.loading = false
        })
        .catch(() => {
          // 使用模拟数据，防止页面无法加载
          this.courseForm = {
            title: 'Vue.js 深度剖析与实战',
            description: '从源码级别深入理解 Vue.js，构建复杂、高性能的前端应用。',
            category: 'web',
            price: 299,
            coverImage: 'https://via.placeholder.com/300x180/2c3e50/ffffff?text=Vue',
            capacity: 100,
            duration: '8',
            level: 'intermediate',
            prerequisites: 'HTML, CSS, JavaScript 基础',
            objectives: '掌握 Vue.js 核心原理',
            status: 'published'
          }
          if (this.courseForm.coverImage) {
            this.fileList = [{
              url: this.courseForm.coverImage,
              name: 'cover'
            }]
          }
          this.$message.warning('使用模拟数据预览')
          this.loading = false
        })
    },

    // 上传成功
    handleUploadSuccess(response) {
      if (response.code === 0) {
        this.courseForm.coverImage = response.data.url
        this.$message.success('图片上传成功')
      } else {
        this.$message.error(response.message || '上传失败')
      }
    },

    // 保存课程
    saveCourse() {
      this.$refs.basicForm.validate(valid => {
        if (valid) {
          this.submitting = true
          this.$api.put(`/courses/${this.courseId}`, this.courseForm)
            .then(() => {
              this.$message.success('课程已更新')
              this.submitting = false
            })
            .catch(err => {
              this.$message.error(err.response?.data?.message || '更新失败')
              this.submitting = false
            })
        }
      })
    },

    // 发布课程
    publishCourse() {
      this.$confirm('确认发布此课程？发布后需要管理员审核。', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      })
        .then(() => {
          this.submitting = true
          this.$api.put(`/courses/${this.courseId}/publish`)
            .then(() => {
              this.$message.success('课程已发布，请等待管理员审核')
              this.courseForm.status = 'pending_review'
              this.submitting = false
            })
            .catch(err => {
              this.$message.error(err.response?.data?.message || '发布失败')
              this.submitting = false
            })
        })
        .catch(() => {})
    },

    // 下架课程
    archiveCourse() {
      this.$confirm('确认下架此课程？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      })
        .then(() => {
          this.submitting = true
          this.$api.put(`/courses/${this.courseId}/archive`)
            .then(() => {
              this.$message.success('课程已下架')
              this.courseForm.status = 'archived'
              this.submitting = false
            })
            .catch(err => {
              this.$message.error(err.response?.data?.message || '操作失败')
              this.submitting = false
            })
        })
        .catch(() => {})
    },

    // 获取课程班期
    fetchCourseTerms() {
      this.$api.get(`/courses/${this.courseId}/terms`)
        .then(res => {
          this.courseTerms = res.data || []
        })
        .catch(() => {
          // 使用mock数据
          this.courseTerms = [
            {
              id: '1',
              name: '2024年秋季班',
              courseId: this.courseId,
              startDate: '2024-09-01',
              endDate: '2024-12-31',
              classCount: 2,
              studentCount: 45,
              status: 'active',
              description: '秋季开班'
            },
            {
              id: '2',
              name: '2025年春季班',
              courseId: this.courseId,
              startDate: '2025-03-01',
              endDate: '2025-06-30',
              classCount: 1,
              studentCount: 0,
              status: 'upcoming',
              description: '春季计划开班'
            }
          ]
        })
    },

    // 获取班级列表
    fetchTermClasses(termId) {
      if (!termId) {
        this.termClasses = []
        return
      }
      this.$api.get(`/terms/${termId}/classes`)
        .then(res => {
          this.termClasses = res.data || []
        })
        .catch(() => {
          // 使用mock数据
          this.termClasses = [
            {
              id: '1',
              name: '班级A',
              code: 'CLASS001',
              teacherName: '张老师',
              studentCount: 25,
              capacity: 30,
              status: 'active',
              termId: termId,
              students: []
            },
            {
              id: '2',
              name: '班级B',
              code: 'CLASS002',
              teacherName: '李老师',
              studentCount: 20,
              capacity: 30,
              status: 'active',
              termId: termId,
              students: []
            }
          ]
        })
    },

    // 查看班期的班级
    viewTermClasses(term) {
      this.selectedTermId = term.id
      this.fetchTermClasses(term.id)
    },

    // 查看班级学生
    viewClassStudents() {
      this.$message.info('班级学生功能将在班级管理页面实现')
    },

    // 编辑班期
    editTerm() {
      this.$router.push(`/teacher/term-management`)
    },

    // 编辑班级
    editClass(classItem) {
      this.$router.push(`/teacher/class-management?termId=${classItem.termId}`)
    },

    // 获取班期名称
    getTermName(termId) {
      const term = this.courseTerms.find(t => t.id === termId)
      return term ? term.name : ''
    },

    // 获取状态类型
    getStatusType(status) {
      const types = {
        'active': 'success',
        'upcoming': 'info',
        'finished': 'warning',
        'canceled': 'danger',
        'draft': 'info',
        'published': 'success',
        'archived': 'info'
      }
      return types[status] || 'info'
    },

    // 获取状态文本
    getStatusText(status) {
      const texts = {
        'active': '进行中',
        'upcoming': '即将开始',
        'finished': '已结束',
        'canceled': '已取消',
        'draft': '草稿',
        'published': '已发布',
        'pending_review': '待审核',
        'archived': '已下架'
      }
      return texts[status] || status
    },

    // 前往班期管理
    goToTermManagement() {
      this.$router.push(`/teacher/term-management?courseId=${this.courseId}`)
    },

    // 前往班级管理
    goToClassManagement() {
      this.$router.push(`/teacher/class-management?courseId=${this.courseId}`)
    },

    // 返回
    goBack() {
      this.$router.back()
    }
  },

  watch: {
    selectedTermId(newVal) {
      if (newVal) {
        this.fetchTermClasses(newVal)
      } else {
        this.termClasses = []
      }
    }
  }
}
</script>

<style scoped lang="scss">
.course-edit-container {
  padding: 20px;
  background: #f5f7fa;
  min-height: 100vh;
}

.page-header {
  margin-bottom: 30px;
  display: flex;
  align-items: center;
  gap: 20px;
}

.page-header h1 {
  margin: 0;
  font-size: 28px;
  color: #333;
}

.loading-container {
  max-width: 900px;
}

.edit-form-wrapper {
  max-width: 900px;
  background: white;
  border-radius: 4px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);

  ::v-deep .el-card {
    border: none;
    border-radius: 4px;
  }

  .unit {
    margin-left: 10px;
    color: #999;
    font-size: 12px;
  }

  /* 章节管理样式 */
  .content-section {
    padding: 20px;
  }

  .section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    border-bottom: 1px solid #ebeef5;
    padding-bottom: 15px;

    h3 {
      margin: 0 0 5px 0;
      font-size: 18px;
      color: #303133;
    }
  }

  .chapter-list {
    .chapter-item {
      border: 1px solid #ebeef5;
      border-radius: 4px;
      margin-bottom: 15px;
      background: #fff;

      .chapter-header {
        padding: 15px;
        background: #f5f7fa;
        border-bottom: 1px solid #ebeef5;
        display: flex;
        justify-content: space-between;
        align-items: center;

        .chapter-title {
          font-weight: bold;
          font-size: 16px;
          display: flex;
          align-items: center;
          gap: 10px;
        }

        .chapter-actions {
          display: flex;
          gap: 10px;
        }
      }

      .lesson-list {
        padding: 10px 15px;

        .lesson-item {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 10px 0;
          border-bottom: 1px dashed #ebeef5;

          &:last-child {
            border-bottom: none;
          }

          .lesson-info {
            display: flex;
            align-items: center;
            gap: 10px;
            color: #606266;

            .lesson-icon {
              font-size: 18px;
              color: #909399;
            }

            .lesson-type-tag {
              margin-left: 5px;
            }
          }
        }

        .empty-lesson {
          text-align: center;
          color: #909399;
          padding: 15px 0;
          font-size: 13px;
        }
      }
    }

    .empty-chapter {
      text-align: center;
      padding: 40px 0;
      color: #909399;
      border: 1px dashed #dcdfe6;
      border-radius: 4px;

      i {
        font-size: 48px;
        margin-bottom: 10px;
      }
    }
  }

  .tip {
    color: #909399;
    font-size: 13px;
    margin: 0;
  }

  .form-actions {
    display: flex;
    justify-content: center;
    gap: 20px;
    margin-top: 40px;
    padding-top: 20px;
    border-top: 1px solid #f0f0f0;

    ::v-deep .el-button {
      min-width: 120px;
    }
  }
}
</style>
