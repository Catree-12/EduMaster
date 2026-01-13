<template>
  <div class="grading-manage">
    <div class="page-header">
      <h1>批改管理</h1>
      <p>批改学生作业和主观题</p>
    </div>

    <div class="grading-container">
      <!-- 左侧班期列表 -->
      <div class="sidebar">
        <div class="sidebar-header">
          <h3>班期列表</h3>
        </div>
        <div class="term-list">
          <div 
            v-for="term in terms" 
            :key="term.id"
            class="term-item"
            :class="{ active: activeTermId === term.id }"
            @click="selectTerm(term.id)"
          >
            <span class="term-name">{{ term.name }}</span>
            <span class="term-count" v-if="term.pendingCount > 0">{{ term.pendingCount }}</span>
          </div>
        </div>
      </div>

      <!-- 右侧主要内容 -->
      <div class="main-content">
        <div class="filter-section">
          <div class="filter-left">
            <div class="filter-tabs">
              <button 
                v-for="type in ['全部', '作业', '考试']"
                :key="type"
                :class="{ active: activeType === type }"
                @click="activeType = type"
                class="filter-btn"
              >
                {{ type }}
              </button>
            </div>
          </div>
          
          <div class="filter-right">
            <el-select v-model="selectedClassId" placeholder="筛选班级" clearable size="medium" style="width: 200px;">
              <el-option
                v-for="cls in currentTermClasses"
                :key="cls.id"
                :label="cls.name"
                :value="cls.id"
              />
            </el-select>
          </div>
        </div>

        <div v-if="filteredItems.length > 0" class="grading-list">
          <div v-for="item in filteredItems" :key="item.id" class="grading-card">
            <div class="card-header">
              <h3>{{ item.title }}</h3>
              <span class="item-type" :class="item.type">{{ item.type === 'homework' ? '📝 作业' : '📋 考试' }}</span>
            </div>

            <div class="card-info">
              <span>👤 {{ item.studentName }}</span>
              <span>🏫 {{ item.className }}</span>
              <span>📚 {{ item.courseName }}</span>
              <span>📅 提交时间: {{ item.submitTime }}</span>
            </div>

            <p class="card-description">{{ item.description }}</p>

            <div class="grading-stats">
              <span>主观题: {{ item.subjective }}题</span>
              <span>需要批改</span>
            </div>

            <button @click="startGrading(item.id)" class="grading-btn">
              开始批改
            </button>
          </div>
        </div>

        <div v-else class="no-content">
          <i class="el-icon-document-checked" style="font-size: 48px; color: #dcdfe6; margin-bottom: 1rem;"></i>
          <p>暂无待批改项目</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'GradingManage',
  data() {
    return {
      activeType: '全部',
      activeTermId: 1,
      selectedClassId: '',
      terms: [
        { id: 1, name: '2024春季班', pendingCount: 5 },
        { id: 2, name: '2023秋季班', pendingCount: 2 },
        { id: 3, name: '2023夏季班', pendingCount: 0 }
      ],
      classes: [
        { id: 101, termId: 1, name: 'Vue前端一班' },
        { id: 102, termId: 1, name: 'Vue前端二班' },
        { id: 201, termId: 2, name: 'Python基础班' }
      ],
      pendingItems: [
        {
          id: 1,
          termId: 1,
          classId: 101,
          className: 'Vue前端一班',
          title: '期末考试主观题',
          type: 'exam',
          studentName: '张三',
          courseName: 'Vue.js 从入门到精通',
          submitTime: '2024-01-20 14:30',
          description: '包含2道主观题需要批改',
          subjective: 2
        },
        {
          id: 2,
          termId: 1,
          classId: 102,
          className: 'Vue前端二班',
          title: '第三周作业',
          type: 'homework',
          studentName: '李四',
          courseName: 'Vue.js 从入门到精通',
          submitTime: '2024-01-19 10:15',
          description: '编程实现题需要代码审查',
          subjective: 1
        },
        {
          id: 3,
          termId: 2,
          classId: 201,
          className: 'Python基础班',
          title: '期末考试主观题',
          type: 'exam',
          studentName: '王五',
          courseName: 'Python 数据科学',
          submitTime: '2024-01-21 09:45',
          description: '包含3道主观题需要批改',
          subjective: 3
        },
        {
          id: 4,
          termId: 1,
          classId: 101,
          className: 'Vue前端一班',
          title: '组件通信作业',
          type: 'homework',
          studentName: '赵六',
          courseName: 'Vue.js 从入门到精通',
          submitTime: '2024-01-22 11:20',
          description: '请检查组件通信逻辑是否正确',
          subjective: 1
        },
        {
          id: 5,
          termId: 1,
          classId: 101,
          className: 'Vue前端一班',
          title: 'Vuex状态管理作业',
          type: 'homework',
          studentName: '钱七',
          courseName: 'Vue.js 从入门到精通',
          submitTime: '2024-01-23 09:00',
          description: 'Store模块化设计审查',
          subjective: 1
        }
      ]
    }
  },
  computed: {
    currentTermClasses() {
      return this.classes.filter(c => c.termId === this.activeTermId)
    },
    filteredItems() {
      return this.pendingItems.filter(item => {
        // 筛选班期
        if (item.termId !== this.activeTermId) return false
        
        // 筛选类型
        if (this.activeType !== '全部') {
          const typeMap = { '作业': 'homework', '考试': 'exam' }
          if (item.type !== typeMap[this.activeType]) return false
        }
        
        // 筛选班级
        if (this.selectedClassId && item.classId !== this.selectedClassId) return false
        
        return true
      })
    }
  },
  methods: {
    selectTerm(termId) {
      this.activeTermId = termId
      this.selectedClassId = '' // 切换班期时重置班级筛选
    },
    startGrading(id) {
      // 实际项目中跳转到具体的批改页面
      // this.$router.push(`/teacher/assignment/${id}/grading`)
      this.$message.success(`进入批改页面 (ID: ${id})`)
    }
  }
}
</script>

<style scoped>
.grading-manage {
  width: 100%;
  height: 100%;
}

.page-header {
  margin-bottom: 1.5rem;
}

.page-header h1 {
  color: #2c3e50;
  margin: 0 0 0.5rem 0;
  font-size: 1.75rem;
}

.page-header p {
  color: #95a5a6;
  margin: 0;
}

.grading-container {
  display: flex;
  gap: 1.5rem;
  min-height: 600px;
}

/* 左侧侧边栏 */
.sidebar {
  width: 240px;
  background: white;
  border-radius: 8px;
  border: 1px solid #ebeef5;
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
}

.sidebar-header {
  padding: 1rem;
  border-bottom: 1px solid #ebeef5;
}

.sidebar-header h3 {
  margin: 0;
  font-size: 1rem;
  color: #303133;
}

.term-list {
  flex: 1;
  padding: 0.5rem;
  overflow-y: auto;
}

.term-item {
  padding: 0.75rem 1rem;
  margin-bottom: 0.25rem;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: all 0.2s;
  color: #606266;
}

.term-item:hover {
  background-color: #f5f7fa;
}

.term-item.active {
  background-color: #ecf5ff;
  color: #409eff;
  font-weight: 500;
}

.term-count {
  background-color: #f56c6c;
  color: white;
  font-size: 12px;
  padding: 0 6px;
  border-radius: 10px;
  height: 18px;
  line-height: 18px;
}

/* 右侧主要内容 */
.main-content {
  flex: 1;
  background: white;
  border-radius: 8px;
  border: 1px solid #ebeef5;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
}

.filter-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.filter-tabs {
  display: flex;
  gap: 0.5rem;
}

.filter-btn {
  padding: 0.5rem 1.25rem;
  background-color: #f4f4f5;
  border: 1px solid #dcdfe6;
  color: #606266;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 14px;
}

.filter-btn:hover {
  color: #409eff;
  border-color: #c6e2ff;
  background-color: #ecf5ff;
}

.filter-btn.active {
  background-color: #409eff;
  color: white;
  border-color: #409eff;
}

.grading-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.grading-card {
  background: white;
  border: 1px solid #ebeef5;
  border-radius: 6px;
  padding: 1.25rem;
  transition: all 0.3s;
  position: relative;
}

.grading-card:hover {
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  border-color: #c6e2ff;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.card-header h3 {
  margin: 0;
  color: #303133;
  font-size: 1.1rem;
}

.item-type {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 12px;
  font-weight: normal;
}

.item-type.homework {
  background-color: #ecf5ff;
  color: #409eff;
}

.item-type.exam {
  background-color: #fdf6ec;
  color: #e6a23c;
}

.card-info {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
  font-size: 13px;
  color: #909399;
  margin-bottom: 0.75rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid #ebeef5;
}

.card-description {
  color: #606266;
  font-size: 14px;
  margin-bottom: 1rem;
  line-height: 1.5;
}

.grading-stats {
  display: flex;
  gap: 1rem;
  font-size: 13px;
  color: #f56c6c;
  margin-bottom: 1rem;
  font-weight: 500;
}

.grading-btn {
  width: 100%;
  padding: 0.6rem;
  background-color: #409eff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  transition: opacity 0.3s;
}

.grading-btn:hover {
  background-color: #66b1ff;
}

.no-content {
  text-align: center;
  padding: 4rem 0;
  color: #909399;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
</style>
