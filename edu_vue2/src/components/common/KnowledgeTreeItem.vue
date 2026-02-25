<template>
  <div class="tree-item">
    <div :class="['tree-item-content', { 'selected': selectedNode && selectedNode.id === node.id }]">
      <!-- 展开/收缩图标 -->
      <span 
        v-if="hasChildren" 
        class="expand-icon" 
        @click.stop="toggleExpand"
      >
        <i :class="isExpanded ? 'el-icon-caret-bottom' : 'el-icon-caret-right'"></i>
      </span>
      <span v-else class="expand-icon-placeholder"></span>
      
      <!-- 复选框 -->
      <el-checkbox
        :value="isSelected"
        @change="handleToggle"
        @click.native.stop
        class="tree-checkbox"
      />
      
      <!-- 编辑模式 -->
      <template v-if="node.isEditing">
        <input
          v-model="localEditName"
          type="text"
          class="tree-input-inline"
          @click.stop
          @keyup.enter="handleConfirmEdit"
          @keyup.esc="$emit('cancel-edit', node)"
        />
        <button @click.stop="handleConfirmEdit" class="tree-btn-confirm">✓</button>
        <button @click.stop="$emit('cancel-edit', node)" class="tree-btn-cancel">✕</button>
      </template>
      
      <!-- 显示模式 -->
      <template v-else>
        <span class="tree-item-label" @click.stop="handleNodeClick">
          {{ node.name }}
        </span>
        <div class="tree-item-actions" @click.stop>
          <button @click="$emit('start-edit', node)" class="tree-btn-edit">编辑</button>
          <button @click="$emit('delete-node', node)" class="tree-btn-delete">删除</button>
        </div>
      </template>
    </div>
    
    <!-- 子节点添加输入框 -->
    <div v-if="node.showChildInput" class="tree-add-input-item child-input">
      <input
        v-model="localNewChildName"
        type="text"
        placeholder="输入子知识点名称"
        class="tree-input"
        @click.stop
        @keyup.enter="handleConfirmAddChild"
        @keyup.esc="$emit('cancel-add-child', node)"
      />
      <button @click.stop="handleConfirmAddChild" class="tree-btn-confirm">✓</button>
      <button @click.stop="$emit('cancel-add-child', node)" class="tree-btn-cancel">✕</button>
    </div>
    
    <!-- 递归渲染子节点 -->
    <div v-if="hasChildren && isExpanded" class="tree-children">
      <knowledge-tree-item
        v-for="child in node.children"
        :key="child.id"
        :node="child"
        :selected-node="selectedNode"
        :selected-ids="selectedIds"
        @node-click="$emit('node-click', $event)"
        @toggle-select="$emit('toggle-select', $event)"
        @start-edit="$emit('start-edit', $event)"
        @confirm-edit="$emit('confirm-edit', $event)"
        @cancel-edit="$emit('cancel-edit', $event)"
        @delete-node="$emit('delete-node', $event)"
        @confirm-add-child="$emit('confirm-add-child', $event)"
        @cancel-add-child="$emit('cancel-add-child', $event)"
      />
    </div>
  </div>
</template>

<script>
export default {
  name: 'KnowledgeTreeItem',
  props: {
    node: {
      type: Object,
      required: true
    },
    selectedNode: {
      type: Object,
      default: null
    },
    selectedIds: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      localEditName: '',
      localNewChildName: '',
      isExpanded: true // 默认展开
    }
  },
  computed: {
    isSelected() {
      return this.selectedIds.includes(this.node.id)
    },
    hasChildren() {
      return this.node.children && this.node.children.length > 0
    }
  },
  watch: {
    'node.editName': {
      immediate: true,
      handler(val) {
        this.localEditName = val
      }
    },
    'node.newChildName': {
      immediate: true,
      handler(val) {
        this.localNewChildName = val
      }
    }
  },
  methods: {
    handleNodeClick() {
      this.$emit('node-click', this.node)
    },
    handleToggle() {
      this.$emit('toggle-select', this.node.id)
    },
    toggleExpand() {
      this.isExpanded = !this.isExpanded
    },
    handleConfirmEdit() {
      this.$emit('confirm-edit', { ...this.node, editName: this.localEditName })
    },
    handleConfirmAddChild() {
      this.$emit('confirm-add-child', { ...this.node, newChildName: this.localNewChildName })
    }
  }
}
</script>

<style lang="scss" scoped>
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

  .expand-icon {
    width: 16px;
    margin-right: 4px;
    cursor: pointer;
    color: #606266;
    font-size: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    
    &:hover {
      color: #409eff;
    }
  }

  .expand-icon-placeholder {
    width: 16px;
    margin-right: 4px;
  }

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
</style>
