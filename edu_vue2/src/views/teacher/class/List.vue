<template>
  <div class="class-management-container">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="title-section">
        <el-button icon="el-icon-arrow-left" type="text" @click="$router.back()" />
        <h1>班级管理</h1>
      </div>
      <p class="subtitle">创建、编辑和管理班级以及班级学生</p>
    </div>

    <!-- 班期选择和操作栏 -->
    <div class="action-bar">
      <div class="term-selector">
        <span class="label">班期：</span>
        <el-select
          v-model="selectedTermId"
          placeholder="选择班期"
          style="width: 250px"
          @change="loadClasses"
        >
          <el-option
            v-for="term in terms"
            :key="term.id"
            :label="term.name"
            :value="term.id"
          />
        </el-select>
      </div>
      <el-button type="primary" icon="el-icon-plus" @click="showCreateDialog">
        创建班级
      </el-button>
      <el-input
        v-model="searchText"
        placeholder="搜索班级名称..."
        style="width: 250px; margin-left: 15px"
        clearable
      >
        <i slot="prefix" class="el-icon-search"></i>
      </el-input>
    </div>

    <!-- 班级列表 -->
    <div class="classes-section">
      <el-card>
        <div slot="header" class="clearfix">
          <span>班级列表</span>
          <span class="class-count">共 {{ filteredClasses.length }} 个班级</span>
        </div>

        <!-- 无数据状态 -->
        <div v-if="filteredClasses.length === 0" class="empty-state">
          <i class="el-icon-folder" />
          <p>{{ selectedTermId ? '该班期还没有班级' : '请先选择班期' }}</p>
          <el-button type="primary" @click="showCreateDialog" v-if="selectedTermId">
            立即创建
          </el-button>
        </div>

        <!-- 班级表格 -->
        <el-table v-else :data="filteredClasses" style="width: 100%" stripe>
          <el-table-column prop="name" label="班级名称" width="150"></el-table-column>
          <el-table-column prop="code" label="班级代码" width="120"></el-table-column>
          <el-table-column prop="teacherName" label="班主任" width="120"></el-table-column>
          <el-table-column prop="studentCount" label="学生数" width="100">
            <template slot-scope="scope">
              <span style="color: #1890ff; font-weight: bold">{{ scope.row.studentCount || 0 }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="capacity" label="班级容量" width="100">
            <template slot-scope="scope">
              {{ scope.row.studentCount || 0 }} / {{ scope.row.capacity }}
            </template>
          </el-table-column>
          <el-table-column prop="status" label="状态" width="100">
            <template slot-scope="scope">
              <el-tag :type="getStatusType(scope.row.status)">
                {{ getStatusText(scope.row.status) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="250" fixed="right">
            <template slot-scope="scope">
              <el-button type="text" size="small" @click="manageStudents(scope.row)">
                管理学生
              </el-button>
              <el-button type="text" size="small" @click="editClass(scope.row)">
                编辑
              </el-button>
              <el-button type="text" size="small" @click="deleteClass(scope.row)">
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </div>

    <!-- 班级编辑对话框 -->
    <el-dialog
      :title="editingClass ? '编辑班级' : '创建班级'"
      :visible.sync="dialogVisible"
      width="500px"
      @close="resetForm"
    >
      <el-form
        ref="classForm"
        :model="formData"
        :rules="rules"
        label-width="100px"
      >
        <el-form-item label="班级名称" prop="name">
          <el-input v-model="formData.name" placeholder="例：一班" />
        </el-form-item>

        <el-form-item label="班级代码" prop="code">
          <el-input v-model="formData.code" placeholder="例：CLASS001" />
        </el-form-item>

        <el-form-item label="班主任" prop="teacherName">
          <el-select
            v-model="formData.teacherName"
            placeholder="选择班主任"
            filterable
          >
            <el-option label="张老师" value="张老师" />
            <el-option label="李老师" value="李老师" />
            <el-option label="王老师" value="王老师" />
          </el-select>
        </el-form-item>

        <el-form-item label="班级容量" prop="capacity">
          <el-input-number
            v-model="formData.capacity"
            :min="1"
            :max="100"
            style="width: 100%"
          />
        </el-form-item>

        <el-form-item label="描述" prop="description">
          <el-input
            v-model="formData.description"
            type="textarea"
            rows="3"
            placeholder="班级描述信息"
          />
        </el-form-item>
      </el-form>

      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveClass">保存</el-button>
      </span>
    </el-dialog>

    <!-- 学生管理对话框 -->
    <el-dialog
      title="管理班级学生"
      :visible.sync="studentDialogVisible"
      width="700px"
      @close="resetStudentDialog"
    >
      <div class="student-manager">
        <!-- 学生选择 -->
        <div class="student-selector">
          <h4>可添加的学生</h4>
          <el-transfer
            v-model="selectedStudents"
            :data="availableStudents"
            :titles="['可选学生', '班级学生']"
            filterable
            filter-placeholder="搜索学生"
          />
        </div>
      </div>

      <span slot="footer" class="dialog-footer">
        <el-button @click="studentDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveStudents">保存</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'ClassManagement',
  data() {
    return {
      terms: [],
      classes: [],
      students: [],
      selectedTermId: null,
      searchText: '',
      dialogVisible: false,
      studentDialogVisible: false,
      editingClass: null,
      currentClassId: null,
      selectedStudents: [],
      formData: {
        name: '',
        code: '',
        teacherName: '',
        capacity: 50,
        description: ''
      },
      rules: {
        name: [{ required: true, message: '班级名称不能为空', trigger: 'blur' }],
        code: [{ required: true, message: '班级代码不能为空', trigger: 'blur' }],
        teacherName: [{ required: true, message: '请选择班主任', trigger: 'change' }],
        capacity: [{ required: true, message: '请设置班级容量', trigger: 'blur' }]
      }
    }
  },
  computed: {
    filteredClasses() {
      return this.classes.filter(c =>
        c.name.toLowerCase().includes(this.searchText.toLowerCase())
      )
    },
    availableStudents() {
      return this.students.map(s => ({
        key: s.id,
        label: `${s.name} (${s.studentId})`
      }))
    }
  },
  created() {
    this.loadTerms()
    this.loadStudents()
    // 如果路由参数中有 termId，则选中该班期
    if (this.$route.query.termId) {
      this.selectedTermId = parseInt(this.$route.query.termId)
      this.loadClasses()
    }
  },
  methods: {
    // 加载班期列表
    loadTerms() {
      this.terms = [
        { id: 1, name: '2024年春季班' },
        { id: 2, name: '2024年秋季班' }
      ]
    },

    // 加载班级列表
    loadClasses() {
      if (!this.selectedTermId) {
        this.classes = []
        return
      }

      this.classes = [
        {
          id: 1,
          name: '一班',
          code: 'CLASS001',
          teacherName: '张老师',
          studentCount: 32,
          capacity: 50,
          status: 'active',
          description: '一班班级',
          termId: 1,
          students: [1, 2, 3]
        },
        {
          id: 2,
          name: '二班',
          code: 'CLASS002',
          teacherName: '李老师',
          studentCount: 28,
          capacity: 50,
          status: 'active',
          description: '二班班级',
          termId: 1,
          students: [4, 5, 6]
        }
      ].filter(c => c.termId === this.selectedTermId)
    },

    // 加载学生列表
    loadStudents() {
      this.students = [
        { id: 1, name: '张三', studentId: 'S001' },
        { id: 2, name: '李四', studentId: 'S002' },
        { id: 3, name: '王五', studentId: 'S003' },
        { id: 4, name: '赵六', studentId: 'S004' },
        { id: 5, name: '孙七', studentId: 'S005' },
        { id: 6, name: '周八', studentId: 'S006' }
      ]
    },

    // 获取状态文本
    getStatusText(status) {
      const statusMap = {
        active: '活跃',
        inactive: '非活跃',
        archived: '已归档'
      }
      return statusMap[status] || status
    },

    // 获取状态标签类型
    getStatusType(status) {
      const typeMap = {
        active: 'success',
        inactive: 'warning',
        archived: 'info'
      }
      return typeMap[status] || 'info'
    },

    // 显示创建对话框
    showCreateDialog() {
      this.editingClass = null
      this.resetForm()
      this.dialogVisible = true
    },

    // 编辑班级
    editClass(classItem) {
      this.editingClass = classItem
      this.formData = { ...classItem }
      this.dialogVisible = true
    },

    // 保存班级
    saveClass() {
      this.$refs.classForm.validate(valid => {
        if (!valid) return

        if (this.editingClass) {
          const index = this.classes.findIndex(c => c.id === this.editingClass.id)
          if (index !== -1) {
            this.classes[index] = { ...this.classes[index], ...this.formData }
            this.$message.success('班级更新成功')
          }
        } else {
          const newClass = {
            id: Math.max(...this.classes.map(c => c.id), 0) + 1,
            ...this.formData,
            studentCount: 0,
            status: 'active',
            termId: this.selectedTermId,
            students: []
          }
          this.classes.push(newClass)
          this.$message.success('班级创建成功')
        }

        this.dialogVisible = false
        this.resetForm()
      })
    },

    // 删除班级
    deleteClass(classItem) {
      this.$confirm(`确认删除班级 "${classItem.name}" 吗？`, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      })
        .then(() => {
          const index = this.classes.findIndex(c => c.id === classItem.id)
          if (index !== -1) {
            this.classes.splice(index, 1)
            this.$message.success('班级已删除')
          }
        })
        .catch(() => {})
    },

    // 管理班级学生
    manageStudents(classItem) {
      this.currentClassId = classItem.id
      this.selectedStudents = classItem.students || []
      this.studentDialogVisible = true
    },

    // 保存班级学生
    saveStudents() {
      const classItem = this.classes.find(c => c.id === this.currentClassId)
      if (classItem) {
        classItem.students = this.selectedStudents
        classItem.studentCount = this.selectedStudents.length
        this.$message.success('班级学生已更新')
      }
      this.studentDialogVisible = false
    },

    // 重置表单
    resetForm() {
      if (this.$refs.classForm) {
        this.$refs.classForm.clearValidate()
      }
      this.formData = {
        name: '',
        code: '',
        teacherName: '',
        capacity: 50,
        description: ''
      }
    },

    // 重置学生对话框
    resetStudentDialog() {
      this.selectedStudents = []
      this.currentClassId = null
    }
  }
}
</script>

<style scoped lang="scss">
.class-management-container {
  padding: 20px;
  background: #f5f7fa;
  min-height: 100vh;
}

.page-header {
  margin-bottom: 30px;

  .title-section {
    display: flex;
    align-items: center;
    gap: 10px;

    h1 {
      margin: 0;
      font-size: 28px;
      color: #333;
      font-weight: bold;
    }
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
  gap: 15px;

  .term-selector {
    display: flex;
    align-items: center;
    gap: 10px;

    .label {
      font-weight: bold;
      color: #333;
    }
  }
}

.classes-section {
  background: white;
  border-radius: 4px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.classes-section .clearfix {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.class-count {
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

.student-manager {
  padding: 20px 0;
}

.student-selector {
  h4 {
    margin-top: 0;
    margin-bottom: 15px;
    color: #333;
    font-weight: bold;
  }
}
</style>
