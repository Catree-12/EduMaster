<template>
  <div class="filter-bar">
    <div v-if="showSearch" class="search-box">
      <input 
        v-model="localSearch"
        type="text" 
        :placeholder="searchPlaceholder"
        @input="$emit('search', localSearch)"
      >
    </div>

    <div v-if="filters.length > 0" class="filter-tabs">
      <button 
        v-for="filter in filters"
        :key="filter"
        :class="{ active: activeFilter === filter }"
        @click="$emit('filter-change', filter)"
        class="filter-btn"
      >
        {{ filter }}
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'FilterBar',
  props: {
    filters: {
      type: Array,
      default: () => []
    },
    activeFilter: String,
    showSearch: Boolean,
    searchPlaceholder: {
      type: String,
      default: '搜索...'
    }
  },
  data() {
    return {
      localSearch: ''
    }
  }
}
</script>

<style scoped>
.filter-bar {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  align-items: center;
}

.search-box {
  flex: 1;
  min-width: 250px;
}

.search-box input {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid #bdc3c7;
  border-radius: 4px;
  font-size: 0.9rem;
}

.search-box input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.filter-tabs {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.filter-btn {
  padding: 0.5rem 1.5rem;
  background-color: #ecf0f1;
  border: 1px solid #bdc3c7;
  color: #7f8c8d;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
  font-weight: 500;
}

.filter-btn.active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-color: transparent;
}

.filter-btn:hover {
  transform: translateY(-2px);
}
</style>
