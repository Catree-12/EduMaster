<template>
  <aside class="sidebar">
    <el-menu
      :default-active="activeMenu"
      class="sidebar-menu"
      router
    >
      <el-menu-item index="/courses">
        <i class="el-icon-collection"></i>
        <span slot="title">课程中心</span>
      </el-menu-item>
      <el-menu-item index="/mycourse/teacher">
        <i class="el-icon-folder-opened"></i>
        <span slot="title">我教的课</span>
      </el-menu-item>
      <el-menu-item index="/mycourse/student">
        <i class="el-icon-reading"></i>
        <span slot="title">我学的课</span>
      </el-menu-item>
      <el-menu-item index="/community">
        <i class="el-icon-chat-line-round"></i>
        <span slot="title">公共社区</span>
      </el-menu-item>
      <el-menu-item index="/user/profile">
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
