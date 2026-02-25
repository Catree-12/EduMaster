<template>
  <el-dialog
    title="管理标签"
    :visible.sync="dialogVisible"
    width="700px"
    :close-on-click-modal="false"
    top="10vh"
    @close="handleClose"
  >
    <div v-loading="loading" class="tag-dialog-content">
      <!-- 顶部操作按钮 -->
      <div class="tag-actions">
        <el-button 
          type="primary"
          size="small"
          @click="handleAddTag"
        >
          ➕ 添加标签
        </el-button>
      </div>

      <!-- 左右分栏布局 -->
      <div class="tag-body">
        <!-- 左侧：标签列表 -->
        <div class="tag-left">
          <div class="tag-list-container">
            <el-input
              v-model="searchText"
              placeholder="搜索标签..."
              prefix-icon="el-icon-search"
              size="small"
              clearable
              style="margin-bottom: 12px;"
            />
            
            <!-- 添加输入框 -->
            <div v-if="showAddInput" class="tag-add-input-item">
              <input
                ref="addInput"
                v-model="newTagName"
                type="text"
                placeholder="输入标签名称"
                class="tag-input"
                @keyup.enter="confirmAddTag"
                @keyup.esc="cancelAddTag"
              />
              <button @click="confirmAddTag" class="tag-btn-confirm">✓</button>
              <button @click="cancelAddTag" class="tag-btn-cancel">✕</button>
            </div>

            <div v-if="internalTagData.length === 0 && !showAddInput" class="empty-list">
              <p>暂无标签</p>
              <p class="hint">点击上方"添加标签"开始创建</p>
            </div>
            
            <div v-else class="tag-list">
              <div
                v-for="tag in filteredTags"
                :key="tag.id"
                :class="['tag-item', { 
                  'editing': tag.isEditing, 
                  'selected': isTagSelected(tag.name) 
                }]"
              >
                <template v-if="tag.isEditing">
                  <input
                    v-model="tag.editName"
                    type="text"
                    class="tag-edit-input"
                    @keyup.enter="confirmEdit(tag)"
                    @keyup.esc="cancelEdit(tag)"
                  />
                  <button @click="confirmEdit(tag)" class="tag-btn-confirm">✓</button>
                  <button @click="cancelEdit(tag)" class="tag-btn-cancel">✕</button>
                </template>
                <template v-else>
                  <div class="tag-content" @click="toggleTagSelection(tag.name)">
                    <i v-if="isTagSelected(tag.name)" class="el-icon-check check-icon"></i>
                    <span class="tag-name">{{ tag.name }}</span>
                  </div>
                  <div class="tag-actions-inline">
                    <button @click.stop="startEdit(tag)" class="tag-btn-edit">
                      <i class="el-icon-edit"></i>
                    </button>
                    <button @click.stop="handleDelete(tag)" class="tag-btn-delete">
                      <i class="el-icon-delete"></i>
                    </button>
                  </div>
                </template>
              </div>
            </div>
          </div>
        </div>

        <!-- 右侧：已选择的标签 -->
        <div class="tag-right">
          <div class="selected-header">
            <span class="selected-title">已选择 ({{ selectedTags.length }})</span>
            <el-button
              v-if="selectedTags.length > 0"
              type="text"
              size="small"
              @click="clearSelection"
            >
              清空
            </el-button>
          </div>
          <div class="selected-list">
            <div v-if="selectedTags.length === 0" class="selected-empty">
              暂未选择标签
            </div>
            <div
              v-for="tagName in selectedTags"
              :key="tagName"
              class="selected-item"
            >
              <span class="selected-tag-name">{{ tagName }}</span>
              <i 
                class="el-icon-close remove-icon"
                @click="toggleTagSelection(tagName)"
              ></i>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 底部按钮 -->
    <div slot="footer" class="dialog-footer">
      <el-button @click="handleClose">取消</el-button>
      <el-button type="primary" @click="handleConfirm">确定</el-button>
    </div>
  </el-dialog>
</template>

<script>
export default {
  name: 'TagSelector',
  props: {
    visible: { type: Boolean, default: false },
    value: { type: Array, default: () => [] },
    tagData: { type: Array, default: () => [] }
  },
  data() {
    return {
      dialogVisible: this.visible,
      loading: false, // 整个弹窗的 loading
      searchText: '',
      showAddInput: false,
      newTagName: '',
      selectedTags: [],
      internalTagData: [],
      tagIdCounter: 100,
      
      // 【修复点 1】必须在这里定义，否则 this.actionLoading 是 undefined
      actionLoading: false, 
      pendingAction: null
    }
  },
  computed: {
    filteredTags() {
      if (!this.searchText.trim()) return this.internalTagData
      const searchText = this.searchText.toLowerCase()
      return this.internalTagData.filter(tag => tag.name.toLowerCase().includes(searchText))
    }
  },
  watch: {
    visible(val) {
      this.dialogVisible = val
      if (val) {
        this.syncFromProps()
      }
    },
    dialogVisible(val) {
      this.$emit('update:visible', val)
    },
    value: {
      handler() {
        this.syncFromProps()
      },
      deep: true
    },
    tagData: {
      handler(newVal) {
        if (newVal && newVal.length > 0) {
          const oldLength = this.internalTagData ? this.internalTagData.length : 0
          
          // 深度拷贝更新内部数据
          this.internalTagData = this.addEditingProperty(JSON.parse(JSON.stringify(newVal)))
          
          // 更新 ID 计数器
          if (newVal.length > 0) {
            this.tagIdCounter = Math.max(...newVal.map(t => t.id || 0)) + 1
          }

          // 检测是否有新标签加入，如果有且匹配 lastAddedTagName，则自动选中
          if (this.lastAddedTagName && newVal.length > oldLength) {
            const newTag = newVal.find(t => t.name === this.lastAddedTagName)
            if (newTag && !this.selectedTags.includes(newTag.name)) {
              this.selectedTags.push(newTag.name)
            }
            // 重置标记
            this.lastAddedTagName = ''
          }
        } else if (!newVal || newVal.length === 0) {
          this.internalTagData = []
        }
      },
      deep: true,
      immediate: true
    }
  },
  methods: {
    syncFromProps() {
      this.selectedTags = [...(this.value || [])]
      if (this.tagData && this.tagData.length > 0) {
        this.internalTagData = this.addEditingProperty(JSON.parse(JSON.stringify(this.tagData)))
      }
    },
    addEditingProperty(tags) {
      return tags.map(tag => ({ ...tag, isEditing: false, editName: tag.name }))
    },
    toggleTagSelection(tagName) {
      const index = this.selectedTags.indexOf(tagName)
      if (index > -1) this.selectedTags.splice(index, 1)
      else this.selectedTags.push(tagName)
    },
    isTagSelected(tagName) {
      return this.selectedTags.includes(tagName)
    },
    clearSelection() {
      this.selectedTags = []
    },
    handleAddTag() {
      this.showAddInput = true
      this.newTagName = ''
      this.$nextTick(() => {
        if (this.$refs.addInput) this.$refs.addInput.focus()
      })
    },

    // --- 核心修改：确认添加 ---
 async confirmAddTag() {
    const tagName = this.newTagName.trim()
    if (!tagName) {
      this.$message.warning('标签名称不能为空')
      return
    }
    if (this.internalTagData.some(tag => tag.name === tagName)) {
      this.$message.warning('该标签已存在')
      return
    }

    this.actionLoading = true
    
    try {
      const result = await this.emitAndWait('add', { name: tagName })
      
      if (result && result.id) {
        // 【修改点 1】不再手动 push 到 internalTagData！
        // 父组件成功后会更新 tagData 属性，watch 会自动同步过来
        
        // 记录名字，以便在 watch 中自动选中
        this.lastAddedTagName = result.name
        
        this.showAddInput = false
        this.newTagName = ''
        this.$message.success('标签已添加')
      }
    } catch (error) {
      if (!error.handled) this.$message.error(error.message || '添加失败')
    } finally {
      this.actionLoading = false
    }
  },

    cancelAddTag() {
      this.showAddInput = false
      this.newTagName = ''
    },
    startEdit(tag) {
      tag.editName = tag.name
      tag.isEditing = true
    },

    // --- 核心修改：确认编辑 ---
    async confirmEdit(tag) {
      const newName = tag.editName.trim()
      if (!newName) {
        this.$message.warning('标签名称不能为空')
        return
      }
      if (this.internalTagData.find(t => t.id !== tag.id && t.name === newName)) {
        this.$message.warning('该标签名称已存在')
        return
      }

      this.actionLoading = true
      const oldName = tag.name // 缓存旧名

      try {
        await this.emitAndWait('edit', { id: tag.id, oldName, newName })
        
        // 成功后更新本地
        tag.name = newName
        tag.isEditing = false
        
        // 同步更新已选列表
        const selectedIndex = this.selectedTags.indexOf(oldName)
        if (selectedIndex > -1) {
          this.selectedTags.splice(selectedIndex, 1, newName)
        }
        this.$message.success('保存成功')
      } catch (error) {
        if (!error.handled) this.$message.error('保存失败')
      } finally {
        this.actionLoading = false
      }
    },

    cancelEdit(tag) {
      tag.editName = tag.name
      tag.isEditing = false
    },

    // --- 核心修改：删除 ---
    async handleDelete(tag) {
      this.$confirm(`确定要删除标签"${tag.name}"吗？`, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        this.actionLoading = true
        try {
          await this.emitAndWait('delete', { id: tag.id })
          
          const index = this.internalTagData.findIndex(t => t.id === tag.id)
          if (index > -1) this.internalTagData.splice(index, 1)
          
          const selectedIndex = this.selectedTags.indexOf(tag.name)
          if (selectedIndex > -1) this.selectedTags.splice(selectedIndex, 1)
          
          this.$message.success('删除成功')
        } catch (error) {
          if (!error.handled) this.$message.error('删除失败')
        } finally {
          this.actionLoading = false
        }
      }).catch(() => {})
    },

    // --- 核心修复：发射事件并等待 ---
    emitAndWait(event, payload) {
      return new Promise((resolve, reject) => {
        let isResolved = false

        const callback = (error, result) => {
          if (isResolved) return // 防止重复调用
          isResolved = true
          if (error) {
            reject({ message: error, handled: true })
          } else {
            resolve(result)
          }
        }

        // 注入 callback
        this.$emit(event, { ...payload, callback })

        // 【修复点 2】超时保护：如果 15 秒父组件还没回调，强制失败
        // 防止父组件代码报错导致子组件永久 loading
        setTimeout(() => {
          if (!isResolved) {
            console.error(`[TagSelector] ${event} operation timeout! Parent did not call callback.`)
            reject({ message: '操作超时，请稍后重试', handled: false })
          }
        }, 15000)
      })
    },

    handleConfirm() {
      this.$emit('input', this.selectedTags)
      this.$emit('confirm', this.selectedTags)
      this.dialogVisible = false
    },
    handleClose() {
      this.dialogVisible = false
      this.actionLoading = false
      this.searchText = ''
      this.showAddInput = false
      this.newTagName = ''
    }
  }
}
</script>

<style scoped>
.tag-dialog-content {
  min-height: 400px;
}

.tag-actions {
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  gap: 12px;
}

.tag-body {
  display: flex;
  gap: 20px;
  height: 450px;
}

.tag-left {
  flex: 1;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.tag-list-container {
  padding: 16px;
  flex: 1;
  overflow-y: auto;
}

.tag-add-input-item {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
  padding: 8px 12px;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.tag-input {
  flex: 1;
  padding: 6px 12px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  font-size: 14px;
  outline: none;
  transition: border-color 0.3s;
}

.tag-input:focus {
  border-color: #409eff;
}

.tag-btn-confirm,
.tag-btn-cancel {
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  transition: all 0.3s;
}

.tag-btn-confirm {
  background-color: #67c23a;
  color: white;
}

.tag-btn-confirm:hover {
  background-color: #5daf34;
}

.tag-btn-cancel {
  background-color: #f56c6c;
  color: white;
}

.tag-btn-cancel:hover {
  background-color: #dd6161;
}

.empty-list {
  text-align: center;
  padding: 60px 20px;
  color: #909399;
}

.empty-list p {
  margin: 8px 0;
  font-size: 14px;
}

.empty-list .hint {
  font-size: 12px;
  color: #c0c4cc;
}

.tag-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.tag-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 12px;
  border: 1px solid #e4e7ed;
  border-radius: 4px;
  background-color: white;
  transition: all 0.3s;
  cursor: pointer;
}

.tag-item:hover {
  border-color: #c0c4cc;
  background-color: #f5f7fa;
}

.tag-item.selected {
  border-color: #409eff;
  background-color: #ecf5ff;
}

.tag-item.editing {
  background-color: #f5f7fa;
  cursor: default;
}

.tag-content {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 8px;
}

.check-icon {
  color: #409eff;
  font-size: 16px;
  font-weight: bold;
}

.tag-name {
  font-size: 14px;
  color: #303133;
}

.tag-edit-input {
  flex: 1;
  padding: 6px 12px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  font-size: 14px;
  outline: none;
}

.tag-edit-input:focus {
  border-color: #409eff;
}

.tag-actions-inline {
  display: flex;
  gap: 8px;
  opacity: 0;
  transition: opacity 0.3s;
}

.tag-item:hover .tag-actions-inline {
  opacity: 1;
}

.tag-btn-edit,
.tag-btn-delete {
  padding: 4px 8px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s;
  background-color: transparent;
}

.tag-btn-edit {
  color: #409eff;
}

.tag-btn-edit:hover {
  background-color: #ecf5ff;
}

.tag-btn-delete {
  color: #f56c6c;
}

.tag-btn-delete:hover {
  background-color: #fef0f0;
}

.tag-right {
  width: 250px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.selected-header {
  padding: 12px 16px;
  background-color: #f5f7fa;
  border-bottom: 1px solid #dcdfe6;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.selected-title {
  font-size: 14px;
  font-weight: 500;
  color: #303133;
}

.selected-list {
  flex: 1;
  padding: 16px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

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
  background-color: #ecf5ff;
  border: 1px solid #d9ecff;
  border-radius: 4px;
  transition: all 0.3s;
}

.selected-item:hover {
  background-color: #d9ecff;
}

.selected-tag-name {
  flex: 1;
  font-size: 14px;
  color: #409eff;
  font-weight: 500;
}

.remove-icon {
  color: #909399;
  cursor: pointer;
  font-size: 14px;
  transition: color 0.3s;
}

.remove-icon:hover {
  color: #f56c6c;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}
</style>
