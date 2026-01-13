<template>
  <aside class="sidebar">
    <el-menu
      :default-active="activeMenu"
      class="sidebar-menu"
      router
    >
      <el-menu-item index="/main/courses">
        <i class="el-icon-collection"></i>
        <span slot="title">课程中心</span>
      </el-menu-item>
      <el-menu-item index="/main/my-courses">
        <i class="el-icon-folder-opened"></i>
        <span slot="title">我的课程</span>
      </el-menu-item>
      <el-menu-item index="/main/community">
        <i class="el-icon-chat-line-round"></i>
        <span slot="title">公共社区</span>
      </el-menu-item>
      <el-menu-item index="/main/profile">
        <i class="el-icon-user"></i>
        <span slot="title">个人主页</span>
      </el-menu-item>
    </el-menu>
  </aside>
</template>

<script>
export default {
  name: 'AppSidebar',
  computed: {
    activeMenu() {
      return this.$route.path
    }
  }
}
</script>

<style scoped lang="scss">
.sidebar {
  width: 200px;
  background-color: #fff;
  border-right: 1px solid #ebeef5;
  overflow-y: auto;
}

.sidebar-menu {
  border-right: none;
}
</style>
