<template>
  <div class="exam-grading">
    <div class="page-header">
      <el-button icon="el-icon-arrow-left" type="text" @click="goBack">返回</el-button>
    </div>

    <div class="grading-header">
      <h1>{{ exam.name }}</h1>
      
      <div class="header-toolbar">
        <el-select v-model="selectedClass" placeholder="默认班级" style="width: 200px;">
          <el-option label="默认班级" value=""></el-option>
          <el-option 
            v-for="cls in classes" 
            :key="cls.id" 
            :label="cls.name" 
            :value="cls.id"
          ></el-option>
        </el-select>

        <el-button icon="el-icon-share">发布补考</el-button>
        <el-button icon="el-icon-bell">督促未交学生</el-button>
        
        <div class="stats-display">
          <span class="stat-item" v-for="stat in statsButtons" :key="stat.type">
            <i :class="stat.icon"></i>
            {{ stat.label }}
          </span>
        </div>

        <el-input 
          v-model="searchKeyword" 
          placeholder="请输入姓名或学号"
          suffix-icon="el-icon-search"
          clearable
          style="width: 250px;"
        />
      </div>
    </div>

    <div class="grading-content">
      <!-- 标签页切换 -->
      <div class="tabs">
        <div 
          :class="['tab-item', { active: activeTab === 'byStudent' }]"
          @click="activeTab = 'byStudent'"
        >
          按人批阅
        </div>
        <div 
          :class="['tab-item', { active: activeTab === 'byQuestion' }]"
          @click="activeTab = 'byQuestion'"
        >
          按题批阅
        </div>
      </div>

      <!-- 提交状态筛选 -->
      <div class="status-filter">
        <el-radio-group v-model="submissionStatus">
          <el-radio label="submitted">已交</el-radio>
          <el-radio label="unsubmitted">未交</el-radio>
        </el-radio-group>
        
        <div class="status-summary">
          全部 {{ totalStudents }} 名学生，已交 {{ submittedCount }}，未交 {{ unsubmittedCount }}
        </div>
      </div>

      <!-- 学生列表 -->
      <el-table 
        :data="filteredStudents" 
        style="width: 100%"
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55"></el-table-column>
        
        <el-table-column prop="name" label="姓名" width="120"></el-table-column>
        
        <el-table-column prop="studentId" label="学号/工号" width="150">
          <template slot-scope="scope">
            <i class="el-icon-sort" style="margin-right: 5px; color: #999;"></i>
            {{ scope.row.studentId }}
          </template>
        </el-table-column>

        <!-- 已交状态显示的列 -->
        <template v-if="submissionStatus === 'submitted'">
          <el-table-column label="提交时间" width="180">
            <template slot-scope="scope">
              <i class="el-icon-sort" style="margin-right: 5px; color: #999;"></i>
              {{ scope.row.submittedAt || '-' }}
            </template>
          </el-table-column>

          <el-table-column label="考试用时" width="120">
            <template slot-scope="scope">
              <i class="el-icon-sort" style="margin-right: 5px; color: #999;"></i>
              {{ scope.row.examDuration || '-' }}
            </template>
          </el-table-column>

          <el-table-column label width="80">
            <template>
              <div class="icon-group">
                <i class="el-icon-chat-dot-square" style="color: #999; font-size: 18px;"></i>
                <i class="el-icon-paperclip" style="color: #999; font-size: 18px; margin-left: 8px;"></i>
              </div>
            </template>
          </el-table-column>

          <el-table-column label="正确率" width="100">
            <template slot-scope="scope">
              {{ scope.row.correctRate || '-' }}
            </template>
          </el-table-column>

          <el-table-column label="状态" width="120">
            <template slot="header">
              <el-dropdown trigger="click" @command="handleStatusFilter">
                <span class="el-dropdown-link">
                  状态 <i class="el-icon-arrow-up" style="transform: rotate(180deg);"></i>
                </span>
                <el-dropdown-menu slot="dropdown">
                  <el-dropdown-item command="all">全部</el-dropdown-item>
                  <el-dropdown-item command="pending">待批阅</el-dropdown-item>
                  <el-dropdown-item command="completed">已完成</el-dropdown-item>
                </el-dropdown-menu>
              </el-dropdown>
            </template>
            <template slot-scope="scope">
              {{ getStatusLabel(scope.row.status) }}
            </template>
          </el-table-column>

          <el-table-column label="批阅时间" width="180"></el-table-column>

          <el-table-column label="批阅人" width="120"></el-table-column>

          <el-table-column prop="score" label="成绩" width="100">
            <template slot-scope="scope">
              <i class="el-icon-sort" style="margin-right: 5px; color: #999;"></i>
              {{ scope.row.score !== null ? scope.row.score : '-' }}
            </template>
          </el-table-column>

          <el-table-column label="操作" width="150">
            <template slot-scope="scope">
              <el-button type="text" @click="viewSubmission(scope.row)">查看</el-button>
              <el-button type="text" style="color: #1890ff;">
                <i class="el-icon-more"></i>
              </el-button>
            </template>
          </el-table-column>
        </template>

        <!-- 未交状态显示的列 -->
        <template v-else>
          <el-table-column label width="120">
            <template>
              <div class="icon-group">
                <i class="el-icon-chat-dot-square" style="color: #999; font-size: 18px;"></i>
              </div>
            </template>
          </el-table-column>

          <el-table-column label="状态" width="120">
            <template slot="header">
              <el-dropdown trigger="click" @command="handleStatusFilter">
                <span class="el-dropdown-link">
                  状态 <i class="el-icon-arrow-up" style="transform: rotate(180deg);"></i>
                </span>
                <el-dropdown-menu slot="dropdown">
                  <el-dropdown-item command="all">全部</el-dropdown-item>
                  <el-dropdown-item command="received">已领取</el-dropdown-item>
                  <el-dropdown-item command="unviewed">未查看</el-dropdown-item>
                  <el-dropdown-item command="pending">待重做</el-dropdown-item>
                </el-dropdown-menu>
              </el-dropdown>
            </template>
            <template slot-scope="scope">
              {{ getStatusLabel(scope.row.status) }}
            </template>
          </el-table-column>

          <el-table-column prop="score" label="成绩" width="150">
            <template slot-scope="scope">
              <i class="el-icon-sort" style="margin-right: 5px; color: #999;"></i>
              {{ scope.row.score !== null ? scope.row.score : '0.0' }}
            </template>
          </el-table-column>

          <el-table-column label="操作" width="200">
            <template slot-scope="scope">
              <el-button type="text" size="small" @click="督促(scope.row)">督促</el-button>
              <el-button type="text" size="small" @click="加时(scope.row)">加时</el-button>
            </template>
          </el-table-column>
        </template>
      </el-table>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ExamGrading',
  data() {
    return {
      activeTab: 'byStudent',
      submissionStatus: 'submitted', // 'submitted' or 'unsubmitted'
      statusFilter: 'all', // 状态筛选
      selectedClass: '',
      searchKeyword: '',
      exam: {
        id: 1,
        name: '新建试卷2025062002075'
      },
      classes: [
        { id: 1, name: '高一（1）班' },
        { id: 2, name: '高一（2）班' }
      ],
      students: [
        {
          id: 1,
          name: '韦佳威',
          studentId: '202212903228',
          submittedAt: '11-29 16:59',
          examDuration: '45分钟',
          correctRate: '80%',
          status: 'pending',
          reviewer: '',
          score: 0,
          isSubmitted: true
        },
        {
          id: 2,
          name: '张三',
          studentId: '202212903229',
          submittedAt: null,
          examDuration: null,
          correctRate: null,
          status: 'unviewed',
          reviewer: '',
          score: 0.0,
          isSubmitted: false
        },
        {
          id: 3,
          name: '李四',
          studentId: '202212903230',
          submittedAt: '11-30 10:30',
          examDuration: '50分钟',
          correctRate: '90%',
          status: 'completed',
          reviewer: '韦佳威',
          score: 90,
          isSubmitted: true
        }
      ],
      selectedStudents: [],
      statsButtons: [
        { type: 'chart', label: '', icon: 'el-icon-s-data' },
        { type: 'pie', label: '', icon: 'el-icon-pie-chart' },
        { type: 'bar', label: '', icon: 'el-icon-s-marketing' },
        { type: 'column', label: '', icon: 'el-icon-data-line' }
      ]
    }
  },
  computed: {
    filteredStudents() {
      let filtered = this.students.filter(s => {
        if (this.submissionStatus === 'submitted') {
          return s.isSubmitted
        } else {
          return !s.isSubmitted
        }
      })

      // 状态筛选
      if (this.statusFilter !== 'all') {
        filtered = filtered.filter(s => s.status === this.statusFilter)
      }

      if (this.searchKeyword) {
        filtered = filtered.filter(s => 
          s.name.includes(this.searchKeyword) || 
          s.studentId.includes(this.searchKeyword)
        )
      }

      return filtered
    },
    totalStudents() {
      return this.students.length
    },
    submittedCount() {
      return this.students.filter(s => s.isSubmitted).length
    },
    unsubmittedCount() {
      return this.students.filter(s => !s.isSubmitted).length
    }
  },
  methods: {
    goBack() {
      this.$router.back()
    },
    handleSelectionChange(selection) {
      this.selectedStudents = selection
    },
    getStatusLabel(status) {
      const statusMap = {
        all: '全部',
        pending: '待批阅',
        completed: '已完成',
        unviewed: '未查看',
        viewed: '已查看',
        received: '已领取'
      }
      return statusMap[status] || '全部'
    },
    handleStatusFilter(status) {
      this.statusFilter = status
    },
    viewSubmission(student) {
      // 跳转到详细批阅页面
      this.$router.push({
        path: `/teacher/exam/${this.$route.params.id}/grading-detail`,
        query: {
          studentId: student.id,
          studentName: student.name
        }
      })
    },
    督促(student) {
      this.$message.success(`已督促 ${student.name} 提交考试`)
    },
    加时(student) {
      this.$prompt('请输入延长时间（分钟）', '加时', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        inputPattern: /^\d+$/,
        inputErrorMessage: '请输入有效的分钟数'
      }).then(({ value }) => {
        this.$message.success(`已为 ${student.name} 延长 ${value} 分钟`)
      }).catch(() => {})
    }
  },
  mounted() {
    // const examId = this.$route.params.id
    // TODO: 根据examId加载考试详情和学生提交情况
  }
}
</script>

<style scoped lang="scss">
.exam-grading {
  padding: 20px;
  min-height: 100vh;
  background: #f5f7fa;
}

.page-header {
  margin-bottom: 20px;
}

.grading-header {
  background: white;
  padding: 20px;
  border-radius: 4px;
  margin-bottom: 20px;

  h1 {
    margin: 0 0 20px 0;
    font-size: 20px;
    color: #333;
  }

  .header-toolbar {
    display: flex;
    align-items: center;
    gap: 15px;
    flex-wrap: wrap;
  }

  .stats-display {
    display: flex;
    gap: 10px;
    margin-left: auto;

    .stat-item {
      padding: 5px 10px;
      background: #f5f5f5;
      border-radius: 4px;
      cursor: pointer;
      transition: all 0.3s;

      &:hover {
        background: #e0e0e0;
      }

      i {
        font-size: 16px;
        color: #666;
      }
    }
  }
}

.grading-content {
  background: white;
  border-radius: 4px;
  padding: 20px;
}

.tabs {
  display: flex;
  border-bottom: 2px solid #f0f0f0;
  margin-bottom: 20px;

  .tab-item {
    padding: 12px 24px;
    cursor: pointer;
    color: #666;
    font-size: 15px;
    position: relative;
    transition: all 0.3s;

    &:hover {
      color: #1890ff;
    }

    &.active {
      color: #1890ff;
      font-weight: bold;

      &::after {
        content: '';
        position: absolute;
        bottom: -2px;
        left: 0;
        right: 0;
        height: 2px;
        background: #1890ff;
      }
    }
  }
}

.status-filter {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;

  .status-summary {
    font-size: 14px;
    color: #666;
  }
}

.el-dropdown-link {
  color: #1890ff;
  cursor: pointer;
  font-size: 13px;
  display: flex;
  align-items: center;
  gap: 5px;
}

.icon-group {
  display: flex;
  align-items: center;
}

::v-deep .el-table {
  th {
    background: #fafafa;
    color: #333;
    font-weight: normal;
  }

  td {
    padding: 12px 0;
  }
}
</style>
