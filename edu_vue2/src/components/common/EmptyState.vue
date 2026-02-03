<!-- EmptyState 空状态组件 -->
<template>
  <div class="empty-state">
    <div class="empty-icon">
      <i :class="icon"></i>
    </div>
    <div class="empty-text">
      <p class="empty-title">{{ title }}</p>
      <p class="empty-description">{{ description }}</p>
    </div>
    <div v-if="showAction" class="empty-action">
      <slot name="action">
        <el-button type="primary" @click="handleAction">{{ actionText }}</el-button>
      </slot>
    </div>
  </div>
</template>

<script>
export default {
  name: 'EmptyState',
  props: {
    icon: {
      type: String,
      default: 'el-icon-box'
    },
    title: {
      type: String,
      default: '暂无数据'
    },
    description: {
      type: String,
      default: ''
    },
    showAction: {
      type: Boolean,
      default: false
    },
    actionText: {
      type: String,
      default: '立即操作'
    }
  },
  methods: {
    handleAction() {
      this.$emit('action')
    }
  }
}
</script>

<style scoped>
.empty-state {
  text-align: center;
  padding: 60px 20px;
}

.empty-icon {
  font-size: 64px;
  color: #c0c4cc;
  margin-bottom: 20px;
}

.empty-text {
  margin-bottom: 24px;
}

.empty-title {
  font-size: 16px;
  color: #606266;
  margin: 0 0 8px 0;
}

.empty-description {
  font-size: 14px;
  color: #909399;
  margin: 0;
}
</style>
