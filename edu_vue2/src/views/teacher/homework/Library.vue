<template>
  <div class="homework-library">
    <div class="page-header">
      <el-button icon="el-icon-arrow-left" type="text" @click="goBack">返回</el-button>
    </div>

    <div class="toolbar">
      <el-button type="primary" icon="el-icon-plus" @click="goToCreateHomework">
        新建作业
      </el-button>
      <el-button icon="el-icon-folder-add" @click="showCreateFolderDialog = true">
        新建文件夹
      </el-button>
      <el-input
        v-model="searchQuery"
        placeholder="搜索"
        suffix-icon="el-icon-search"
        clearable
        style="width: 300px; margin-left: auto;"
      />
    </div>

    <div class="content-wrapper">
      <div class="header-row">
        <span class="all-count">全部作业</span>
        <span class="count">共 {{ filteredHomeworks.length }} 份</span>
      </div>

      <el-table
        :data="filteredHomeworks"
        style="width: 100%"
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55"></el-table-column>
        <el-table-column prop="name" label="文件夹/作业" min-width="300">
          <template slot-scope="scope">
            <span class="homework-name" @click="viewHomework(scope.row)" style="cursor: pointer;">
              <i :class="scope.row.isFolder ? 'el-icon-folder' : 'el-icon-document'" style="margin-right: 8px;"></i>
              {{ scope.row.name }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="questionCount" label="题量" width="100" align="center">
          <template slot-scope="scope">
            {{ scope.row.isFolder ? '-' : scope.row.questionCount }}
          </template>
        </el-table-column>
        <el-table-column prop="totalPoints" label="总分" width="100" align="center">
          <template slot-scope="scope">
            {{ scope.row.isFolder ? '-' : scope.row.totalPoints }}
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100" align="center">
          <template slot-scope="scope">
            <el-tag v-if="!scope.row.isFolder" :type="scope.row.published ? 'success' : 'info'" size="small">
              {{ scope.row.published ? '已发布' : '未发布' }}
            </el-tag>
            <span v-else>-</span>
          </template>
        </el-table-column>
        <el-table-column prop="creator" label="创建者" width="120" align="center">
        </el-table-column>
        <el-table-column prop="createdAt" label="创建时间" width="180" align="center">
        </el-table-column>
        <el-table-column label="操作" width="200" align="center">
          <template slot-scope="scope">
            <el-button v-if="!scope.row.isFolder" type="primary" size="small" @click="publishHomework(scope.row)">发布</el-button>
            <el-button type="text" size="small" @click="editHomework(scope.row)">编辑</el-button>
            <el-dropdown trigger="click" @command="handleCommand($event, scope.row)">
              <span class="el-dropdown-link">
                更多<i class="el-icon-arrow-down el-icon--right"></i>
              </span>
              <el-dropdown-menu slot="dropdown">
                <el-dropdown-item command="move">移动到</el-dropdown-item>
                <el-dropdown-item command="copy">复制</el-dropdown-item>
                <el-dropdown-item command="delete" style="color: #F56C6C;">删除</el-dropdown-item>
              </el-dropdown-menu>
            </el-dropdown>
          </template>
        </el-table-column>
      </el-table>

      <div v-if="filteredHomeworks.length === 0" class="empty-state">
        <i class="el-icon-document-copy" style="font-size: 64px; color: #dcdfe6;"></i>
        <p>暂无作业</p>
        <el-button type="primary" @click="goToCreateHomework">创建第一个作业</el-button>
      </div>
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
  </div>
</template>

<script>
export default {
  name: 'HomeworkLibrary',
  data() {
    return {
      searchQuery: '',
      selectedHomeworks: [],
      showCreateFolderDialog: false,
      newFolderName: '',
      homeworks: [
        {
          id: 'folder-1',
          name: '基础练习文件夹',
          isFolder: true,
          creator: '韦佳威',
          createdAt: '01-05 10:00'
        },
        {
          id: 1,
          name: '新建作业20251115184744',
          questionCount: 1,
          totalPoints: 100,
          creator: '韦佳威',
          createdAt: '11-15 18:47',
          published: false, // 是否已发布
          questions: [
            {
              id: 1,
              type: 'single',
              title: '下列哪个是闭包的特性？',
              options: ['访问外部变量', '内存泄漏', '函数嵌套', '变量提升'],
              answer: 0,
              points: 100
            }
          ]
        },
        {
          id: 2,
          name: '函数进阶练习',
          questionCount: 5,
          totalPoints: 100,
          creator: '韦佳威',
          createdAt: '2024-01-10',
          published: true, // 已发布过
          questions: [
            {
              id: 1,
              type: 'single',
              title: '下列哪个是闭包的特性？',
              options: ['访问外部变量', '内存泄漏', '函数嵌套', '变量提升'],
              answer: 0,
              points: 20
            },
            {
              id: 2,
              type: 'multiple',
              title: 'JavaScript中的数据类型包括？',
              options: ['String', 'Number', 'Boolean', 'Undefined'],
              answer: [0, 1, 2, 3],
              points: 20
            }
          ]
        }
      ]
    }
  },
  computed: {
    filteredHomeworks() {
      if (!this.searchQuery) return this.homeworks
      return this.homeworks.filter(hw => 
        hw.name.includes(this.searchQuery)
      )
    }
  },
  methods: {
    goBack() {
      this.$router.back()
    },
    goToCreateHomework() {
      this.$router.push('/teacher/homework/create')
    },
    viewHomework(hw) {
      if (hw.isFolder) {
        this.$message.info('这是一个文件夹')
        return
      }
      
      // 所有作业都跳转到详情页，显示完整题目
      this.$router.push({
        path: `/teacher/homework/${hw.id}/detail`,
        query: { published: hw.published }
      })
    },
    editHomework(hw) {
      if (hw.isFolder) {
        this.$message.info('文件夹无法编辑')
        return
      }
      
      // 跳转到创建页面进行编辑
      this.$router.push({
        path: '/teacher/homework/create',
        query: { 
          id: hw.id,
          mode: 'edit',
          published: hw.published
        }
      })
      sessionStorage.setItem('editHomeworkData', JSON.stringify(hw))
    },
    publishHomework(hw) {
      // 跳转到发布设置页面
      this.$router.push(`/teacher/homework/${hw.id}/publish`)
    },
    handleSelectionChange(selection) {
      this.selectedHomeworks = selection
    },
    handleCommand(command, hw) {
      switch(command) {
        case 'move':
          this.$message.info(`移动作业: ${hw.name}`)
          // TODO: 实现移动逻辑
          break
        case 'copy':
          this.$message.success(`已复制: ${hw.name}`)
          // TODO: 实现复制逻辑
          break
        case 'delete':
          this.deleteHomework(hw.id)
          break
      }
    },
    createFolder() {
      if (!this.newFolderName.trim()) {
        this.$message.warning('请输入文件夹名称')
        return
      }
      
      const newFolder = {
        id: `folder-${Date.now()}`,
        name: this.newFolderName,
        isFolder: true,
        creator: '当前用户',
        createdAt: this.formatDateTime(new Date())
      }
      
      this.homeworks.unshift(newFolder)
      this.$message.success('创建成功')
      this.showCreateFolderDialog = false
      this.newFolderName = ''
    },
    formatDateTime(date) {
      const month = String(date.getMonth() + 1).padStart(2, '0')
      const day = String(date.getDate()).padStart(2, '0')
      const hours = String(date.getHours()).padStart(2, '0')
      const minutes = String(date.getMinutes()).padStart(2, '0')
      return `${month}-${day} ${hours}:${minutes}`
    },
    deleteHomework(id) {
      this.$confirm('确定删除此作业？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.homeworks = this.homeworks.filter(hw => hw.id !== id)
        this.$message.success('作业已删除')
      }).catch(() => {})
    }
  }
}
</script>

<style scoped lang="scss">
.homework-library {
  padding: 20px;
  min-height: 100vh;
  background: #f5f7fa;
}

.page-header {
  margin-bottom: 20px;
}

.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.content-wrapper {
  background: white;
  border-radius: 4px;
  padding: 20px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.header-row {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 1px solid #e0e0e0;

  .all-count {
    font-size: 14px;
    color: #333;
  }

  .count {
    font-size: 13px;
    color: #999;
  }
}

.homework-name {
  color: #333;
  cursor: pointer;
  transition: color 0.3s;

  &:hover {
    color: #1890ff;
  }
}

.el-dropdown-link {
  cursor: pointer;
  color: #409EFF;
  font-size: 13px;
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

.empty-state {
  text-align: center;
  padding: 80px 20px;

  p {
    margin: 20px 0;
    font-size: 14px;
    color: #999;
  }
}
</style>
