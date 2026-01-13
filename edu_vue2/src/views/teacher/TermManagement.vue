<template>
  <div class="term-management-container">
    <!-- 页面头部 -->
    <div class="page-header">
      <h1>班期管理</h1>
      <p class="subtitle">创建、编辑和管理课程班期</p>
    </div>

    <!-- 操作栏 -->
    <div class="action-bar">
      <el-button type="primary" icon="el-icon-plus" @click="showCreateDialog">
        创建班期
      </el-button>
      <el-input
        v-model="searchText"
        placeholder="搜索班期名称..."
        style="width: 250px; margin-left: 15px"
        clearable
      >
        <i slot="prefix" class="el-icon-search"></i>
      </el-input>
    </div>

    <!-- 班期列表 -->
    <div class="terms-section">
      <el-card>
        <div slot="header" class="clearfix">
          <span>班期列表</span>
          <span class="term-count">共 {{ filteredTerms.length }} 个班期</span>
        </div>

        <!-- 无数据状态 -->
        <div v-if="filteredTerms.length === 0" class="empty-state">
          <i class="el-icon-document" />
          <p>还没有创建任何班期</p>
          <el-button type="primary" @click="showCreateDialog">
            立即创建
          </el-button>
        </div>

        <!-- 班期表格 -->
        <el-table v-else :data="filteredTerms" style="width: 100%" stripe>
          <el-table-column prop="name" label="班期名称" width="180"></el-table-column>
          <el-table-column prop="courseId" label="所属课程" width="150">
            <template slot-scope="scope">
              {{ getCourseNameById(scope.row.courseId) || '未指定' }}
            </template>
          </el-table-column>
          <el-table-column prop="startDate" label="开始日期" width="120">
            <template slot-scope="scope">
              {{ scope.row.startDate | formatDate }}
            </template>
          </el-table-column>
          <el-table-column prop="endDate" label="结束日期" width="120">
            <template slot-scope="scope">
              {{ scope.row.endDate | formatDate }}
            </template>
          </el-table-column>
          <el-table-column prop="classCount" label="班级数" width="80">
            <template slot-scope="scope">
              <span style="color: #1890ff; font-weight: bold">{{ scope.row.classCount || 0 }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="studentCount" label="学生数" width="80">
            <template slot-scope="scope">
              {{ scope.row.studentCount || 0 }}
            </template>
          </el-table-column>
          <el-table-column prop="status" label="状态" width="100">
            <template slot-scope="scope">
              <el-tag :type="getStatusType(scope.row.status)">
                {{ getStatusText(scope.row.status) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="200" fixed="right">
            <template slot-scope="scope">
              <el-button type="text" size="small" @click="editTerm(scope.row)">
                编辑
              </el-button>
              <el-button type="text" size="small" @click="manageClasses(scope.row)">
                管理班级
              </el-button>
              <el-button type="text" size="small" @click="deleteTerm(scope.row)">
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </div>

    <!-- 班期编辑对话框 -->
    <el-dialog
      :title="editingTerm ? '编辑班期' : '创建班期'"
      :visible.sync="dialogVisible"
      width="500px"
      @close="resetForm"
    >
      <el-form
        ref="termForm"
        :model="formData"
        :rules="rules"
        label-width="100px"
      >
        <el-form-item label="班期名称" prop="name">
          <el-input v-model="formData.name" placeholder="例：2024年春季班" />
        </el-form-item>

        <el-form-item label="所属课程" prop="courseId">
          <el-select
            v-model="formData.courseId"
            placeholder="选择课程"
            filterable
          >
            <el-option
              v-for="course in courses"
              :key="course.id"
              :label="course.title"
              :value="course.id"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="开始日期" prop="startDate">
          <el-date-picker
            v-model="formData.startDate"
            type="date"
            placeholder="选择开始日期"
            style="width: 100%"
          />
        </el-form-item>

        <el-form-item label="结束日期" prop="endDate">
          <el-date-picker
            v-model="formData.endDate"
            type="date"
            placeholder="选择结束日期"
            style="width: 100%"
          />
        </el-form-item>

        <el-form-item label="描述" prop="description">
          <el-input
            v-model="formData.description"
            type="textarea"
            rows="3"
            placeholder="班期描述信息"
          />
        </el-form-item>
      </el-form>

      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveTerm">保存</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'TermManagement',
  filters: {
    formatDate(date) {
      if (!date) return '-'
      const d = new Date(date)
      return d.toLocaleDateString('zh-CN')
    }
  },
  data() {
    return {
      terms: [],
      courses: [],
      searchText: '',
      dialogVisible: false,
      editingTerm: null,
      formData: {
        name: '',
        courseId: '',
        startDate: null,
        endDate: null,
        description: ''
      },
      rules: {
        name: [{ required: true, message: '班期名称不能为空', trigger: 'blur' }],
        courseId: [{ required: true, message: '请选择所属课程', trigger: 'change' }],
        startDate: [{ required: true, message: '请选择开始日期', trigger: 'change' }],
        endDate: [{ required: true, message: '请选择结束日期', trigger: 'change' }]
      }
    }
  },
  computed: {
    userId() {
      return this.$store.state.user.id
    },
    filteredTerms() {
      return this.terms.filter(term =>
        term.name.toLowerCase().includes(this.searchText.toLowerCase())
      )
    }
  },
  created() {
    this.loadTerms()
    this.loadCourses()
  },
  methods: {
    // 加载班期列表
    loadTerms() {
      this.terms = [
        {
          id: 1,
          name: '2024年春季班',
          courseId: 1,
          startDate: '2024-01-01',
          endDate: '2024-05-31',
          classCount: 3,
          studentCount: 45,
          status: 'active',
          description: '春季学期班期'
        },
        {
          id: 2,
          name: '2024年秋季班',
          courseId: 1,
          startDate: '2024-09-01',
          endDate: '2025-01-31',
          classCount: 2,
          studentCount: 30,
          status: 'upcoming',
          description: '秋季学期班期'
        }
      ]
    },

    // 加载课程列表
    loadCourses() {
      this.courses = [
        { id: 1, title: 'Vue.js 全栈开发' },
        { id: 2, title: 'React 开发实战' },
        { id: 3, title: 'Node.js 后端开发' }
      ]
    },

    // 根据课程ID获取课程名称
    getCourseNameById(courseId) {
      const course = this.courses.find(c => c.id === courseId)
      return course ? course.title : ''
    },

    // 获取状态文本
    getStatusText(status) {
      const statusMap = {
        active: '进行中',
        upcoming: '即将开始',
        finished: '已结束',
        canceled: '已取消'
      }
      return statusMap[status] || status
    },

    // 获取状态标签类型
    getStatusType(status) {
      const typeMap = {
        active: 'success',
        upcoming: 'info',
        finished: 'warning',
        canceled: 'danger'
      }
      return typeMap[status] || 'info'
    },

    // 显示创建对话框
    showCreateDialog() {
      this.editingTerm = null
      this.resetForm()
      this.dialogVisible = true
    },

    // 编辑班期
    editTerm(term) {
      this.editingTerm = term
      this.formData = { ...term }
      this.dialogVisible = true
    },

    // 保存班期
    saveTerm() {
      this.$refs.termForm.validate(valid => {
        if (!valid) return

        if (this.editingTerm) {
          // 编辑
          const index = this.terms.findIndex(t => t.id === this.editingTerm.id)
          if (index !== -1) {
            this.terms[index] = { ...this.terms[index], ...this.formData }
            this.$message.success('班期更新成功')
          }
        } else {
          // 创建
          const newTerm = {
            id: Math.max(...this.terms.map(t => t.id), 0) + 1,
            ...this.formData,
            classCount: 0,
            studentCount: 0,
            status: 'upcoming'
          }
          this.terms.push(newTerm)
          this.$message.success('班期创建成功')
        }

        this.dialogVisible = false
        this.resetForm()
      })
    },

    // 删除班期
    deleteTerm(term) {
      this.$confirm(`确认删除班期 "${term.name}" 吗？`, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      })
        .then(() => {
          const index = this.terms.findIndex(t => t.id === term.id)
          if (index !== -1) {
            this.terms.splice(index, 1)
            this.$message.success('班期已删除')
          }
        })
        .catch(() => {})
    },

    // 管理班级
    manageClasses(term) {
      this.$router.push({
        name: 'ClassManagement',
        query: { termId: term.id }
      })
    },

    // 重置表单
    resetForm() {
      if (this.$refs.termForm) {
        this.$refs.termForm.clearValidate()
      }
      this.formData = {
        name: '',
        courseId: '',
        startDate: null,
        endDate: null,
        description: ''
      }
    }
  }
}
</script>

<style scoped lang="scss">
.term-management-container {
  padding: 20px;
  background: #f5f7fa;
  min-height: 100vh;
}

.page-header {
  margin-bottom: 30px;

  h1 {
    margin: 0;
    font-size: 28px;
    color: #333;
    font-weight: bold;
  }

  .subtitle {
    margin: 10px 0 0 0;
    color: #999;
    font-size: 14px;
  }
}

.action-bar {
  margin-bottom: 20px;
  display: flex;
  align-items: center;
}

.terms-section {
  background: white;
  border-radius: 4px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.terms-section .clearfix {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.term-count {
  color: #999;
  font-size: 12px;
  font-weight: normal;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;

  i {
    font-size: 64px;
    color: #ddd;
    display: block;
    margin-bottom: 20px;
  }

  p {
    font-size: 14px;
    color: #999;
    margin-bottom: 20px;
  }
}
</style>
