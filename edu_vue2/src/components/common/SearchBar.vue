<!-- SearchBar 搜索栏组件 -->
<template>
  <div class="search-bar">
    <el-input
      v-model="searchText"
      :placeholder="placeholder"
      prefix-icon="el-icon-search"
      clearable
      @input="handleInput"
      @clear="handleClear"
    >
      <el-button slot="append" icon="el-icon-search" @click="handleSearch"></el-button>
    </el-input>
  </div>
</template>

<script>
export default {
  name: 'SearchBar',
  props: {
    placeholder: {
      type: String,
      default: '请输入搜索关键词'
    },
    value: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      searchText: this.value
    }
  },
  watch: {
    value(newVal) {
      this.searchText = newVal
    }
  },
  methods: {
    handleInput(value) {
      this.$emit('input', value)
      this.$emit('change', value)
    },
    handleSearch() {
      this.$emit('search', this.searchText)
    },
    handleClear() {
      this.$emit('clear')
    }
  }
}
</script>

<style scoped>
.search-bar {
  width: 100%;
}
</style>
