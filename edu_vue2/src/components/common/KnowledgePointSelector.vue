<template>
  <el-dialog
    title="关联知识点"
    :visible.sync="dialogVisible"
    width="900px"
    :close-on-click-modal="false"
    top="8vh"
    @close="handleClose"
  >
    <div v-loading="loading" class="knowledge-dialog-content">
      <!-- 顶部操作按钮 -->
      <div class="knowledge-actions">
        <el-button 
          type="primary"
          size="small"
          @click="handleAddSameLevelKnowledge"
        >
          ➕ 添加同级知识点
        </el-button>
        <el-button 
          type="info"
          size="small"
          @click="handleAddChildLevelKnowledge"
          :disabled="!selectedKnowledgeNode"
        >
          ➕ 添加子级知识点
        </el-button>
        <span v-if="selectedKnowledgeNode" class="selected-node-hint">
          当前选中：{{ selectedKnowledgeNode.name }}
        </span>
      </div>

      <!-- 左右分栏布局 -->
      <div class="knowledge-body">
        <!-- 左侧：知识点树 -->
        <div class="knowledge-left">
          <div class="knowledge-tree-container">
            <el-input
              v-model="searchText"
              placeholder="搜索知识点..."
              prefix-icon="el-icon-search"
              size="small"
              clearable
              style="margin-bottom: 12px;"
            />
            
            <!-- 根节点添加输入框 -->
            <div v-if="showRootInput" class="tree-add-input-item">
              <input
                ref="rootInput"
                v-model="newRootName"
                type="text"
                placeholder="输入知识点名称"
                class="tree-input"
                @keyup.enter="confirmAddRoot"
                @keyup.esc="cancelAddRoot"
              />
              <button @click="confirmAddRoot" class="tree-btn-confirm">✓</button>
              <button @click="cancelAddRoot" class="tree-btn-cancel">✕</button>
            </div>

            <div v-if="treeData.length === 0 && !showRootInput" class="empty-tree">
              <p>暂无知识点</p>
              <p class="hint">点击上方"添加同级知识点"开始创建</p>
            </div>
            
            <div v-else class="tree-list">
              <knowledge-tree-item
                v-for="node in filteredTree"
                :key="node.id"
                :node="node"
                :selected-node="selectedKnowledgeNode"
                :selected-ids="selectedIds"
                @node-click="handleNodeClick"
                @toggle-select="toggleKnowledgeSelection"
                @start-edit="startEditKnowledgeNode"
                @confirm-edit="confirmEditKnowledge"
                @cancel-edit="cancelEditKnowledge"
                @delete-node="deleteKnowledgeNode"
                @confirm-add-child="confirmAddChild"
                @cancel-add-child="cancelAddChild"
              />
            </div>
          </div>
        </div>

        <!-- 右侧：已选择的知识点 -->
        <div class="knowledge-right">
          <div class="selected-header">
            <span class="selected-title">已选择 ({{ selectedIds.length }})</span>
          </div>
          <div class="selected-list">
            <div v-if="selectedIds.length === 0" class="selected-empty">
              暂未选择知识点
            </div>
            <div
              v-for="nodeId in selectedIds"
              :key="nodeId"
              class="selected-item"
            >
              <span class="selected-item-name">{{ getNodeNameById(nodeId) || `ID:${nodeId}` }}</span>
              <i class="el-icon-close" @click="removeSelectedKnowledge(nodeId)"></i>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <span slot="footer">
      <el-button @click="handleCancel">取消</el-button>
      <el-button type="primary" @click="handleConfirm">确定</el-button>
    </span>
  </el-dialog>
</template>

<script>
import KnowledgeTreeItem from './KnowledgeTreeItem.vue'

export default {
  name: 'KnowledgePointSelector',
  components: {
    KnowledgeTreeItem
  },
  props: {
    visible: {
      type: Boolean,
      default: false
    },
    value: {
      type: Array,
      default: () => []
    },
    // 知识点树数据，如果传入则使用，否则内部管理
    knowledgeTree: {
      type: Array,
      default: null
    }
  },
  data() {
    return {
      dialogVisible: this.visible,
      loading: false,
      searchText: '',
      selectedKnowledgeNode: null,
      showRootInput: false,
      newRootName: '',
      // 内部管理的树数据
      internalTreeData: [],
      knowledgeIdCounter: 100,
      // 选中的知识点ID数组
      selectedIds: []
    }
  },
  computed: {
    // 使用外部传入的树数据或内部管理的树数据
    treeData() {
      return this.knowledgeTree !== null ? this.knowledgeTree : this.internalTreeData
    },
    filteredTree() {
      if (!this.searchText.trim()) {
        return this.treeData
      }
      const searchText = this.searchText.toLowerCase()
      const filterTree = (nodes) => {
        return nodes.filter(node => {
          const matches = node.name.toLowerCase().includes(searchText)
          let filteredChildren = []
          if (node.children && node.children.length > 0) {
            filteredChildren = filterTree(node.children)
          }
          return matches || filteredChildren.length > 0
        }).map(node => {
          if (node.children && node.children.length > 0) {
            return {
              ...node,
              children: filterTree(node.children)
            }
          }
          return node
        })
      }
      return filterTree(this.treeData)
    }
  },
  watch: {
    visible(val) {
      this.dialogVisible = val
      if (val) {
        this.init()
      }
    },
    dialogVisible(val) {
      this.$emit('update:visible', val)
    },
    treeData: {
      handler() {
        // 当树数据加载完成后,同步已选择的知识点
        if (this.treeData && this.treeData.length > 0) {
          this.syncSelectedFromValue()
        }
      },
      deep: true
    }
  },
  methods: {
    init() {
      this.searchText = ''
      this.selectedKnowledgeNode = null
      this.showRootInput = false
      this.newRootName = ''
      this.selectedIds = []
      this.closeAllInputs()
      
      // 从value prop同步已选中的知识点名称,转换为ID
      if (this.value && this.value.length > 0) {
        this.$nextTick(() => {
          this.syncSelectedFromValue()
        })
      }
      
      // 如果没有外部传入树数据，初始化默认数据
      if (!this.knowledgeTree && this.internalTreeData.length === 0) {
        this.internalTreeData = [
          {
            id: 1,
            name: 'JavaScript基础',
            isEditing: false,
            showChildInput: false,
            newChildName: '',
            children: [
              { id: 11, name: '数据类型', isEditing: false, showChildInput: false, newChildName: '', children: [] },
              { id: 12, name: '运算符', isEditing: false, showChildInput: false, newChildName: '', children: [] }
            ]
          },
          {
            id: 2,
            name: '闭包',
            isEditing: false,
            showChildInput: false,
            newChildName: '',
            children: []
          },
          {
            id: 3,
            name: '异步编程',
            isEditing: false,
            showChildInput: false,
            newChildName: '',
            children: [
              { id: 31, name: 'Promise', isEditing: false, showChildInput: false, newChildName: '', children: [] },
              { id: 32, name: 'async/await', isEditing: false, showChildInput: false, newChildName: '', children: [] }
            ]
          }
        ]
      }
    },
    handleClose() {
      this.dialogVisible = false
    },
    handleCancel() {
      this.dialogVisible = false
    },
    handleConfirm() {
      // 直接返回选中的ID数组(支持同名知识点)
      this.$emit('input', [...this.selectedIds])
      this.$emit('confirm', [...this.selectedIds])
      this.dialogVisible = false
    },
    handleNodeClick(node) {
      this.selectedKnowledgeNode = node
    },
    toggleKnowledgeSelection(nodeId) {
      const index = this.selectedIds.indexOf(nodeId)
      if (index > -1) {
        this.selectedIds.splice(index, 1)
      } else {
        this.selectedIds.push(nodeId)
      }
    },
    removeSelectedKnowledge(nodeId) {
      const index = this.selectedIds.indexOf(nodeId)
      if (index > -1) {
        this.selectedIds.splice(index, 1)
      }
    },
    // 根据ID获取节点名称
    getNodeNameById(nodeId) {
      if (!this.treeData || this.treeData.length === 0) {
        return ''
      }
      
      const findNode = (nodes, id) => {
        if (!nodes || !Array.isArray(nodes)) return null
        
        for (const node of nodes) {
          if (node.id === id) return node.name
          if (node.children && node.children.length > 0) {
            const found = findNode(node.children, id)
            if (found) return found
          }
        }
        return null
      }
      return findNode(this.treeData, nodeId) || ''
    },
    // 根据名称获取节点ID
    getNodeIdByName(nodeName) {
      if (!this.treeData || this.treeData.length === 0) {
        return null
      }
      
      const findNode = (nodes, name) => {
        if (!nodes || !Array.isArray(nodes)) return null
        
        for (const node of nodes) {
          if (node.name === name) return node.id
          if (node.children && node.children.length > 0) {
            const found = findNode(node.children, name)
            if (found) return found
          }
        }
        return null
      }
      return findNode(this.treeData, nodeName)
    },
    // 从value prop同步到selectedIds
    syncSelectedFromValue() {
      this.selectedIds = []
      if (this.value && this.value.length > 0) {
        // value现在是ID数组,直接使用
        this.selectedIds = [...this.value]
      }
    },
    handleAddSameLevelKnowledge() {
      console.log('点击了添加同级知识点')
      this.closeAllInputs()
      this.showRootInput = true
      this.newRootName = ''
      this.$nextTick(() => {
        this.$refs.rootInput && this.$refs.rootInput.focus()
      })
    },
    handleAddChildLevelKnowledge() {
      console.log('点击了添加子级知识点, 当前选中:', this.selectedKnowledgeNode)
      if (!this.selectedKnowledgeNode) {
        this.$message.warning('请先选择一个知识点')
        return
      }
      
      this.closeAllInputs()
      this.selectedKnowledgeNode.showChildInput = true
      this.selectedKnowledgeNode.newChildName = ''
      this.$forceUpdate()
    },
    closeAllInputs() {
      this.showRootInput = false
      const closeInputsRecursive = (nodes) => {
        nodes.forEach(node => {
          node.showChildInput = false
          node.newChildName = ''
          if (node.children && node.children.length > 0) {
            closeInputsRecursive(node.children)
          }
        })
      }
      closeInputsRecursive(this.treeData)
    },
    confirmAddRoot() {
      if (!this.newRootName.trim()) {
        this.$message.warning('知识点名称不能为空')
        return
      }
      
      if (this.knowledgeTree) {
        // 外部数据模式: emit事件给父组件处理,不显示消息
        this.$emit('add-root', { name: this.newRootName.trim() })
        this.showRootInput = false
        this.newRootName = ''
      } else {
        // 内部数据模式: 直接添加并显示消息
        const newNode = {
          id: ++this.knowledgeIdCounter,
          name: this.newRootName.trim(),
          isEditing: false,
          showChildInput: false,
          newChildName: '',
          children: []
        }
        this.internalTreeData.push(newNode)
        this.showRootInput = false
        this.newRootName = ''
        this.$message.success('知识点已添加')
      }
    },
    cancelAddRoot() {
      this.showRootInput = false
      this.newRootName = ''
    },
    confirmAddChild(parentNode) {
      if (!parentNode.newChildName || !parentNode.newChildName.trim()) {
        this.$message.warning('知识点名称不能为空')
        return
      }
      
      if (this.knowledgeTree) {
        // 外部数据模式: emit事件给父组件处理,不显示消息
        this.$emit('add-child', { 
          name: parentNode.newChildName.trim(), 
          parentId: parentNode.id 
        })
        parentNode.showChildInput = false
        parentNode.newChildName = ''
        this.$forceUpdate()
      } else {
        // 内部数据模式: 直接添加并显示消息
        const newNode = {
          id: ++this.knowledgeIdCounter,
          name: parentNode.newChildName.trim(),
          isEditing: false,
          showChildInput: false,
          newChildName: '',
          children: []
        }
        
        if (!parentNode.children) {
          this.$set(parentNode, 'children', [])
        }
        parentNode.children.push(newNode)
        
        parentNode.showChildInput = false
        parentNode.newChildName = ''
        this.$message.success('子知识点已添加')
        this.$forceUpdate()
      }
    },
    cancelAddChild(node) {
      node.showChildInput = false
      node.newChildName = ''
      this.$forceUpdate()
    },
    startEditKnowledgeNode(node) {
      console.log('开始编辑知识点:', node.name)
      this.closeAllInputs()
      node.isEditing = true
      node.editName = node.name
      this.$forceUpdate()
    },
    confirmEditKnowledge(node) {
      if (!node.editName || !node.editName.trim()) {
        this.$message.warning('知识点名称不能为空')
        return
      }
      
      if (node.editName === node.name) {
        node.isEditing = false
        return
      }
      
      if (this.knowledgeTree) {
        // 外部数据模式: emit事件给父组件处理,不显示消息
        this.$emit('edit-node', { 
          id: node.id, 
          name: node.editName.trim() 
        })
        node.isEditing = false
        this.$forceUpdate()
      } else {
        // 内部数据模式: 直接修改并显示消息
        node.name = node.editName.trim()
        node.isEditing = false
        this.$message.success('知识点已保存')
        this.$forceUpdate()
      }
    },
    cancelEditKnowledge(node) {
      node.isEditing = false
      node.editName = node.name
      this.$forceUpdate()
    },
    deleteKnowledgeNode(node) {
      this.$confirm(`确定删除知识点“${node.name}”吗？`, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        if (this.knowledgeTree) {
          // 外部数据模式: emit事件给父组件处理,不显示消息
          this.$emit('delete-node', { id: node.id })
        } else {
          // 内部数据模式: 直接删除并显示消息
          this.deleteNodeById(this.treeData, node.id)
          this.$message.success('知识点已删除')
        }
        if (this.selectedKnowledgeNode && this.selectedKnowledgeNode.id === node.id) {
          this.selectedKnowledgeNode = null
        }
      }).catch(() => {})
    },
    deleteNodeById(nodes, nodeId) {
      for (let i = 0; i < nodes.length; i++) {
        if (nodes[i].id === nodeId) {
          nodes.splice(i, 1)
          return true
        }
        if (nodes[i].children && nodes[i].children.length > 0) {
          if (this.deleteNodeById(nodes[i].children, nodeId)) {
            return true
          }
        }
      }
      return false
    }
  }
}
</script>

<style lang="scss" scoped>
.knowledge-dialog-content {
  .knowledge-actions {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 12px 0;
    margin-bottom: 16px;
    border-bottom: 1px solid #ebeef5;

    .selected-node-hint {
      margin-left: auto;
      color: #409eff;
      font-size: 14px;
    }
  }

  .knowledge-body {
    display: flex;
    gap: 20px;
    height: 500px;
  }

  .knowledge-left {
    flex: 1;
    display: flex;
    flex-direction: column;
    border: 1px solid #dcdfe6;
    border-radius: 4px;
    padding: 15px;
    background: #fff;

    .knowledge-tree-container {
      flex: 1;
      overflow-y: auto;
      
      .empty-tree {
        text-align: center;
        padding: 60px 20px;
        color: #909399;

        p {
          margin: 8px 0;
        }

        .hint {
          font-size: 12px;
          color: #c0c4cc;
        }
      }

      .tree-list {
        margin-top: 12px;
      }

      .tree-item {
        margin-bottom: 4px;
      }

      .tree-item-content {
        display: flex;
        align-items: center;
        padding: 6px 8px;
        border-radius: 4px;
        cursor: pointer;
        transition: background 0.2s;

        &:hover {
          background: #f5f7fa;
        }

        &.selected {
          background: #ecf5ff;
          border-left: 3px solid #409eff;
        }

        .tree-checkbox {
          margin-right: 8px;
        }

        .tree-item-label {
          flex: 1;
          font-size: 14px;
          color: #606266;
        }

        .tree-item-actions {
          opacity: 0;
          transition: opacity 0.2s;
          display: flex;
          gap: 4px;

          button {
            padding: 2px 8px;
            font-size: 12px;
            border: none;
            border-radius: 3px;
            cursor: pointer;
            transition: all 0.2s;

            &.tree-btn-edit {
              background: #ecf5ff;
              color: #409eff;

              &:hover {
                background: #409eff;
                color: white;
              }
            }

            &.tree-btn-delete {
              background: #fef0f0;
              color: #f56c6c;

              &:hover {
                background: #f56c6c;
                color: white;
              }
            }
          }
        }

        &:hover .tree-item-actions {
          opacity: 1;
        }

        .tree-input-inline {
          flex: 1;
          padding: 4px 8px;
          border: 1px solid #409eff;
          border-radius: 3px;
          font-size: 14px;

          &:focus {
            outline: none;
            border-color: #66b1ff;
          }
        }

        .tree-btn-confirm,
        .tree-btn-cancel {
          padding: 4px 8px;
          font-size: 12px;
          border: none;
          border-radius: 3px;
          cursor: pointer;
          transition: all 0.2s;
        }

        .tree-btn-confirm {
          background: #67c23a;
          color: white;

          &:hover {
            background: #85ce61;
          }
        }

        .tree-btn-cancel {
          background: #f56c6c;
          color: white;

          &:hover {
            background: #f78989;
          }
        }
      }

      .tree-add-input-item {
        display: flex;
        align-items: center;
        padding: 6px 8px;
        margin-bottom: 8px;
        background: #f0f9ff;
        border: 1px dashed #409eff;
        border-radius: 4px;

        &.child-input {
          margin-left: 24px;
          background: #f5f7fa;
          border-color: #909399;
        }

        .tree-input {
          flex: 1;
          padding: 4px 8px;
          border: 1px solid #dcdfe6;
          border-radius: 3px;
          font-size: 14px;
          margin-right: 8px;

          &:focus {
            outline: none;
            border-color: #409eff;
          }
        }

        .tree-btn-confirm,
        .tree-btn-cancel {
          padding: 4px 10px;
          font-size: 12px;
          border: none;
          border-radius: 3px;
          cursor: pointer;
          transition: all 0.2s;
        }

        .tree-btn-confirm {
          background: #67c23a;
          color: white;
          margin-right: 4px;

          &:hover {
            background: #85ce61;
          }
        }

        .tree-btn-cancel {
          background: #f56c6c;
          color: white;

          &:hover {
            background: #f78989;
          }
        }
      }

      .tree-children {
        margin-left: 24px;
        border-left: 1px dashed #dcdfe6;
        padding-left: 12px;
      }
    }
  }

  .knowledge-right {
    width: 280px;
    display: flex;
    flex-direction: column;
    border: 1px solid #dcdfe6;
    border-radius: 4px;
    background: #f9fafb;

    .selected-header {
      padding: 12px 15px;
      border-bottom: 1px solid #ebeef5;
      background: white;
      font-weight: bold;
      color: #303133;

      .selected-title {
        font-size: 14px;
      }
    }

    .selected-list {
      flex: 1;
      overflow-y: auto;
      padding: 10px;

      .selected-empty {
        text-align: center;
        padding: 40px 20px;
        color: #909399;
        font-size: 14px;
      }

      .selected-item {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 8px 12px;
        margin-bottom: 6px;
        background: white;
        border: 1px solid #e4e7ed;
        border-radius: 4px;
        transition: all 0.2s;

        &:hover {
          border-color: #409eff;
          background: #ecf5ff;
        }

        .selected-item-name {
          flex: 1;
          font-size: 14px;
          color: #606266;
        }

        .el-icon-close {
          cursor: pointer;
          color: #c0c4cc;
          font-size: 14px;
          transition: color 0.2s;

          &:hover {
            color: #f56c6c;
          }
        }
      }
    }
  }
}
</style>
