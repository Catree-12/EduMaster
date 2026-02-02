<template>
  <div class="exam-create-manual-wrapper">
    <!-- 使用原有的 ExamCreate 组件作为手动组卷页面 -->
    <exam-create />
  </div>
</template>

<script>
import ExamCreate from './ExamCreate.vue'

export default {
  name: 'ExamCreateManual',
  components: {
    ExamCreate
  }
}
</script>

<style scoped>
.exam-create-manual-wrapper {
  width: 100%;
  height: 100%;
}
</style>
