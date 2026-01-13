<template>
  <div class="exam-library">
    <!-- 顶部标题栏 -->
    <div class="header-bar">
      <el-button icon="el-icon-arrow-left" class="back-btn" @click="goBack">返回</el-button>
      <h2 class="title">试卷库</h2>
    </div>

    <!-- 操作栏 -->
    <div class="operation-bar">
      <div class="left-actions">
        <el-button type="primary" icon="el-icon-plus" @click="createExam">+ 新建考试</el-button>
        <el-button class="folder-btn" icon="el-icon-folder-add" @click="showCreateFolderDialog = true">新建文件夹</el-button>
      </div>
      <div class="right-actions">
        <el-input
          v-model="searchKeyword"
          placeholder="试卷名"
          prefix-icon="el-icon-search"
          class="search-input"
          clearable
          @input="handleSearch"
        />
      </div>
    </div>

    <!-- 数据表格 -->
    <div class="table-card">
      <el-table
        :data="filteredExams"
        style="width: 100%"
        @selection-change="handleSelectionChange"
        @row-click="handleRowClick"
      >
        <el-table-column type="selection" width="55" />
        
        <el-table-column label="文件夹/试卷名称" min-width="250">
          <template slot-scope="scope">
            <div class="exam-name clickable">
              <i :class="scope.row.isFolder ? 'el-icon-folder' : 'el-icon-document'" style="margin-right: 8px;"></i>
              <span>{{ scope.row.name }}</span>
            </div>
          </template>
        </el-table-column>

        <el-table-column label="题量" width="100" align="center">
          <template slot-scope="scope">
            {{ scope.row.isFolder ? '-' : scope.row.questionCount }}
          </template>
        </el-table-column>

        <el-table-column label="总分" width="100" align="center">
          <template slot-scope="scope">
            {{ scope.row.isFolder ? '-' : scope.row.totalScore.toFixed(1) }}
          </template>
        </el-table-column>

        <el-table-column label="难度" width="100" align="center">
          <template slot-scope="scope">
            <span v-if="!scope.row.isFolder" :class="['difficulty-tag', `difficulty-${scope.row.difficulty}`]">
              {{ scope.row.difficulty }}
            </span>
            <span v-else>-</span>
          </template>
        </el-table-column>

        <el-table-column label="创建者" width="120" align="center">
          <template slot-scope="scope">
            {{ scope.row.creator }}
          </template>
        </el-table-column>

        <el-table-column label="发放次数" width="120" align="center">
          <template slot-scope="scope">
            {{ scope.row.isFolder ? '-' : scope.row.publishCount }}
          </template>
        </el-table-column>

        <el-table-column label="创建时间" width="140" align="center">
          <template slot-scope="scope">
            {{ scope.row.createTime }}
          </template>
        </el-table-column>

        <el-table-column label="操作" width="240" align="center">
          <template slot-scope="scope">
            <div class="action-buttons" @click.stop>
              <el-button v-if="!scope.row.isFolder" type="primary" size="small" @click="publishExam(scope.row)">发布</el-button>
              <el-button v-if="!scope.row.isFolder" type="text" @click="archiveExam(scope.row)">封存</el-button>
              <el-dropdown trigger="click" @command="handleCommand($event, scope.row)">
                <el-button type="text">
                  更多<i class="el-icon-arrow-down el-icon--right"></i>
                </el-button>
                <el-dropdown-menu slot="dropdown">
                  <el-dropdown-item command="move">移动到</el-dropdown-item>
                  <el-dropdown-item command="edit">编辑</el-dropdown-item>
                  <el-dropdown-item command="copy">复制</el-dropdown-item>
                  <el-dropdown-item command="delete" style="color: #F56C6C;">删除</el-dropdown-item>
                </el-dropdown-menu>
              </el-dropdown>
            </div>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- 底部功能 -->
    <div class="footer-bar">
      <el-button type="text" icon="el-icon-delete" @click="goToRecycleBin">回收站</el-button>
    </div>

    <!-- 新建文件夹对话框 -->
    <el-dialog
      title="新建文件夹"
      :visible.sync="showCreateFolderDialog"
      width="400px"
    >
      <el-input
        v-model="newFolderName"
        placeholder="请输入文件夹名称"
        maxlength="50"
        show-word-limit
      />
      <span slot="footer" class="dialog-footer">
        <el-button @click="showCreateFolderDialog = false">取 消</el-button>
        <el-button type="primary" @click="createFolder">确 定</el-button>
      </span>
    </el-dialog>

    <!-- 移动到对话框 -->
    <el-dialog
      title="移动到"
      :visible.sync="showMoveDialog"
      width="400px"
    >
      <el-select v-model="moveToFolder" placeholder="请选择目标文件夹" style="width: 100%">
        <el-option
          v-for="folder in folders"
          :key="folder.id"
          :label="folder.name"
          :value="folder.id"
        />
      </el-select>
      <span slot="footer" class="dialog-footer">
        <el-button @click="showMoveDialog = false">取 消</el-button>
        <el-button type="primary" @click="confirmMove">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'ExamLibrary',
  data() {
    return {
      searchKeyword: '',
      selectedExams: [],
      showCreateFolderDialog: false,
      showMoveDialog: false,
      newFolderName: '',
      moveToFolder: '',
      currentOperatingItem: null,
      
      // 模拟数据 - 试卷库只显示未发布的试卷
      examList: [
        {
          id: 1,
          name: '新建试卷20260107184356',
          isFolder: false,
          questionCount: 1,
          totalScore: 5.0,
          difficulty: '易',
          creator: '韦佳成',
          publishCount: 0,
          published: false,
          createTime: '01-07 18:43',
          questions: [
            {
              id: 1,
              type: 'single',
              title: '下列哪个是JavaScript的特性？',
              options: ['动态类型', '静态类型', '强类型', '编译型'],
              answer: 0,
              points: 5
            }
          ]
        },
        {
          id: 2,
          name: '第一单元测试草稿',
          isFolder: false,
          questionCount: 10,
          totalScore: 50.0,
          difficulty: '易',
          creator: '李老师',
          publishCount: 0,
          published: false,
          createTime: '01-06 14:30',
          questions: [
            {
              id: 1,
              type: 'single',
              title: '以下哪个是闭包的特点？',
              options: ['访问外部变量', '内存泄漏', '函数嵌套', '变量提升'],
              answer: 0,
              points: 5
            },
            {
              id: 2,
              type: 'multiple',
              title: 'JavaScript的基本数据类型包括？',
              options: ['String', 'Number', 'Boolean', 'Object'],
              answer: [0, 1, 2],
              points: 5
            }
          ]
        },
        {
          id: 3,
          name: '数学试卷文件夹',
          isFolder: true,
          creator: '韦佳成',
          createTime: '01-02 09:15'
        }
      ]
    }
  },
  computed: {
    filteredExams() {
      if (!this.searchKeyword) {
        return this.examList
      }
      return this.examList.filter(exam => 
        exam.name.toLowerCase().includes(this.searchKeyword.toLowerCase())
      )
    },
    folders() {
      return this.examList.filter(item => item.isFolder)
    }
  },
  methods: {
    goBack() {
      this.$router.back()
    },
    
    createExam() {
      this.$router.push('/teacher/exam-create')
    },
    
    handleSearch() {
      // 搜索逻辑已在 computed 中实现
    },
    
    handleSelectionChange(selection) {
      this.selectedExams = selection
    },
    
    handleRowClick(row) {
      if (row.isFolder) {
        // 点击文件夹，进入文件夹
        this.$message.info(`进入文件夹: ${row.name}`)
        // TODO: 实现文件夹导航逻辑
      } else {
        // 点击试卷，查看试卷详情（显示题目）
        this.$router.push(`/teacher/exam/${row.id}/detail`)
      }
    },
    
    publishExam(exam) {
      // 跳转到发布设置页面
      this.$router.push(`/teacher/exam/${exam.id}/publish`)
    },
    
    archiveExam(exam) {
      this.$confirm(`确定要封存试卷"${exam.name}"吗？封存后将无法编辑。`, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$message.success('封存成功')
        // TODO: 调用封存接口
      }).catch(() => {})
    },
    
    handleCommand(command, row) {
      this.currentOperatingItem = row
      
      switch(command) {
        case 'move':
          this.showMoveDialog = true
          break
        case 'edit':
          this.editExam(row)
          break
        case 'copy':
          this.copyExam(row)
          break
        case 'delete':
          this.deleteExam(row)
          break
      }
    },
    
    editExam(exam) {
      if (exam.isFolder) {
        this.$message.info('文件夹无法编辑')
        return
      }
      // 跳转到创建/编辑页面，传递试卷数据
      this.$router.push({
        path: '/teacher/exam-create',
        query: { 
          id: exam.id,
          mode: 'edit'
        }
      })
      // 将试卷数据存储到 sessionStorage，供创建页面使用
      sessionStorage.setItem('editExamData', JSON.stringify(exam))
    },
    
    copyExam(exam) {
      this.$message.success(`已复制"${exam.name}"`)
      // TODO: 调用复制接口
    },
    
    deleteExam(exam) {
      this.$confirm(`确定要删除"${exam.name}"吗？删除后将移至回收站。`, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        const index = this.examList.findIndex(item => item.id === exam.id)
        if (index > -1) {
          this.examList.splice(index, 1)
          this.$message.success('已移至回收站')
        }
      }).catch(() => {})
    },
    
    createFolder() {
      if (!this.newFolderName.trim()) {
        this.$message.warning('请输入文件夹名称')
        return
      }
      
      const newFolder = {
        id: Date.now(),
        name: this.newFolderName,
        isFolder: true,
        creator: '当前用户',
        createTime: this.formatDateTime(new Date())
      }
      
      this.examList.unshift(newFolder)
      this.$message.success('创建成功')
      this.showCreateFolderDialog = false
      this.newFolderName = ''
    },
    
    confirmMove() {
      if (!this.moveToFolder) {
        this.$message.warning('请选择目标文件夹')
        return
      }
      
      this.$message.success('移动成功')
      this.showMoveDialog = false
      this.moveToFolder = ''
      // TODO: 调用移动接口
    },
    
    goToRecycleBin() {
      this.$router.push('/teacher/exam-recycle-bin')
    },
    
    formatDateTime(date) {
      const month = String(date.getMonth() + 1).padStart(2, '0')
      const day = String(date.getDate()).padStart(2, '0')
      const hours = String(date.getHours()).padStart(2, '0')
      const minutes = String(date.getMinutes()).padStart(2, '0')
      return `${month}-${day} ${hours}:${minutes}`
    }
  }
}
</script>

<style scoped lang="scss">
.exam-library {
  min-height: 100vh;
  background-color: #F5F5F5;
  padding: 20px;

  .header-bar {
    display: flex;
    align-items: center;
    margin-bottom: 20px;
    position: relative;

    .back-btn {
      position: absolute;
      left: 0;
    }

    .title {
      flex: 1;
      text-align: center;
      font-size: 20px;
      font-weight: 600;
      color: #303133;
      margin: 0;
    }
  }

  .operation-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;

    .left-actions {
      display: flex;
      gap: 12px;

      .el-button--primary {
        background-color: #5B4FE0;
        border-color: #5B4FE0;
        border-radius: 6px;

        &:hover {
          background-color: #4A3FD0;
          border-color: #4A3FD0;
        }
      }

      .folder-btn {
        color: #409EFF;
        border-color: #409EFF;
        background-color: #ECF5FF;
        border-radius: 6px;

        &:hover {
          color: #66B1FF;
          border-color: #66B1FF;
          background-color: #ECF5FF;
        }
      }
    }

    .right-actions {
      .search-input {
        width: 260px;

        ::v-deep .el-input__inner {
          border-radius: 20px;
        }
      }
    }
  }

  .table-card {
    background-color: #FFFFFF;
    border-radius: 8px;
    padding: 20px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);

    .exam-name {
      display: flex;
      align-items: center;
      font-size: 14px;

      &.clickable {
        cursor: pointer;
        
        &:hover {
          color: #409EFF;
        }
      }

      i {
        font-size: 16px;
        color: #909399;
      }
    }

    .difficulty-tag {
      padding: 2px 8px;
      border-radius: 4px;
      font-size: 12px;

      &.difficulty-易 {
        background-color: #E8F8F5;
        color: #00C48C;
      }

      &.difficulty-中 {
        background-color: #FFF4E6;
        color: #FF9800;
      }

      &.difficulty-难 {
        background-color: #FFEBEE;
        color: #F44336;
      }
    }

    .action-buttons {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;

      .el-button--primary {
        padding: 5px 12px;
      }

      .el-button--text {
        padding: 5px 8px;
      }
    }
  }

  .footer-bar {
    margin-top: 20px;
    padding-left: 20px;

    .el-button--text {
      color: #909399;
      font-size: 14px;

      &:hover {
        color: #606266;
      }

      i {
        margin-right: 4px;
      }
    }
  }
}

::v-deep .el-table {
  .el-table__header th {
    background-color: #FAFAFA;
    color: #606266;
    font-weight: 600;
  }

  .el-table__row {
    &:hover {
      background-color: #F5F7FA;
    }
  }
}

::v-deep .el-dialog {
  border-radius: 8px;

  .el-dialog__header {
    border-bottom: 1px solid #EBEEF5;
    padding: 16px 20px;
  }

  .el-dialog__body {
    padding: 20px;
  }

  .el-dialog__footer {
    border-top: 1px solid #EBEEF5;
    padding: 12px 20px;
  }
}
</style>
