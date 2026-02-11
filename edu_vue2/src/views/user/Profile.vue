<template>
  <div class="my-profile">
    <div class="profile-header">
      <div class="profile-card">
        <!-- 头像 -->
        <div class="avatar-section">
          <el-avatar :size="80" :src="avatar" :icon="avatar ? '' : 'el-icon-user-solid'"></el-avatar>
          <el-upload
            class="avatar-upload"
            :action="uploadUrl"
            :headers="uploadHeaders"
             name="avatar"
            :show-file-list="false"
            :on-success="handleAvatarSuccess"
            :before-upload="beforeAvatarUpload"
          >
            <el-button size="small" type="text">更换头像</el-button>
          </el-upload>
        </div>
        
        <!-- 基本信息显示 -->
        <div class="user-info">
          <h2>{{ nickname }}</h2>
          <p class="real_name">用户名：@{{ real_name }}</p>
          <p class="email">{{ email }}</p>
          <!-- <div class="identity-tags">
            <el-tag v-if="isStudent" size="small" type="info">学生 - {{ studentId }}</el-tag>
            <el-tag v-if="isTeacher" size="small" :type="isTeacherVerified ? 'success' : 'warning'">
              教师 - {{ teacherId }} {{ isTeacherVerified ? '(已认证)' : '(未认证)' }}
            </el-tag>
          </div> -->
        </div>
      </div>
    </div>

    <div class="profile-content">
      <el-tabs v-model="activeTab" type="card">
        <!-- 个人信息标签页 -->
        <el-tab-pane label="个人信息" name="info">
          <div class="tab-content">
            <el-form :model="formData" ref="infoForm" label-width="100px" :disabled="!editingInfo">
              <!-- 第一行: 用户名 + 昵称 -->
              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="用户名" prop="real_name">
                    <el-input v-model="formData.real_name" placeholder="请输入用户名"></el-input>
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="昵称" prop="nickname">
                    <el-input v-model="formData.nickname" placeholder="请输入昵称"></el-input>
                  </el-form-item>
                </el-col>
              </el-row>

              <!-- 第二行: 邮箱 + 手机号 -->
              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="邮箱">
                    <el-input v-model="email" disabled>
                      <template #append>
                        <el-tooltip content="邮箱不可修改" placement="top">
                          <i class="el-icon-lock"></i>
                        </el-tooltip>
                      </template>
                    </el-input>
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="手机号" prop="phone">
                    <el-input v-model="formData.phone" placeholder="请输入手机号"></el-input>
                  </el-form-item>
                </el-col>
              </el-row>

              <!-- 第三行: 学号 + 工号 (如果有) -->
              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="学号">
                    <el-input :value="studentId || ''" disabled>
                      <template #append>
                        <!-- <el-tooltip content="学号由系统分配，不可修改" placement="top">
                          <i class="el-icon-lock"></i>
                        </el-tooltip> -->
                      </template>
                    </el-input>
                  </el-form-item>
                </el-col>

                <el-col :span="12">
                  <el-form-item label="工号">
                    <el-input :value="teacherId || '无'" disabled>
                      <template #append>
                        <!-- <el-tooltip content="工号由系统分配，不可修改" placement="top">
                          <i class="el-icon-lock"></i>
                        </el-tooltip> -->
                      </template>
                    </el-input>
                  </el-form-item>
                </el-col>
              </el-row>

              <!-- 第四行: 性别 + 学校 -->
              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="性别" prop="gender">
                    <el-select v-model="formData.gender" placeholder="请选择性别" style="width: 100%">
                      <el-option label="男" value="male"></el-option>
                      <el-option label="女" value="female"></el-option>
                      <el-option label="保密" value="secret"></el-option>
                    </el-select>
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="学校" prop="school">
                    <el-input v-model="formData.school" placeholder="请输入学校名称"></el-input>
                  </el-form-item>
                </el-col>
              </el-row>

              <!-- 第五行: 专业 + 注册时间 -->
              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="专业" prop="major">
                    <el-input v-model="formData.major" placeholder="请输入专业名称"></el-input>
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="注册时间">
                    <el-input v-model="createdAt" disabled></el-input>
                  </el-form-item>
                </el-col>
              </el-row>

              <!-- 第六行: 个人简介 (独占一行) -->
              <el-form-item label="个人简介" prop="bio">
                <el-input
                  type="textarea"
                  v-model="formData.bio"
                  :rows="4"
                  placeholder="介绍一下自己吧..."
                  maxlength="500"
                  show-word-limit
                ></el-input>
              </el-form-item>
            </el-form>

            <div class="action-buttons">
              <el-button v-if="!editingInfo" type="primary" @click="startEditInfo">编辑资料</el-button>
              <template v-else>
                <el-button type="primary" :loading="saving" @click="saveInfo">保存</el-button>
                <el-button @click="cancelEditInfo">取消</el-button>
              </template>
            </div>
          </div>
        </el-tab-pane>

        <!-- 密码设置标签页 -->
        <el-tab-pane label="密码设置" name="password">
          <div class="tab-content">
            <el-form :model="passwordForm" ref="passwordForm" label-width="100px" :rules="passwordRules">
              <el-form-item label="当前密码" prop="old_password">
                <el-input
                  v-model="passwordForm.old_password"
                  type="password"
                  placeholder="请输入当前密码"
                  show-password
                ></el-input>
              </el-form-item>
              <el-form-item label="新密码" prop="new_password">
                <el-input
                  v-model="passwordForm.new_password"
                  type="password"
                  placeholder="请输入新密码(至少6位)"
                  show-password
                ></el-input>
              </el-form-item>
              <el-form-item label="确认新密码" prop="confirm_password">
                <el-input
                  v-model="passwordForm.confirm_password"
                  type="password"
                  placeholder="请再次输入新密码"
                  show-password
                ></el-input>
              </el-form-item>
            </el-form>
            <div class="action-buttons">
              <el-button type="primary" :loading="changingPassword" @click="savePassword">修改密码</el-button>
              <el-button @click="resetPasswordForm">重置</el-button>
            </div>
          </div>
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import { userAPI, authAPI } from '@/api'

export default {
  name: 'MyProfile',
  data() {
    // 自定义验证规则：确认密码
    const validateConfirmPassword = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请再次输入新密码'))
      } else if (value !== this.passwordForm.new_password) {
        callback(new Error('两次输入的密码不一致'))
      } else {
        callback()
      }
    }

    return {
      activeTab: 'info',
      editingInfo: false,
      saving: false,
      changingPassword: false,
      
      // 可编辑字段的表单数据(对应后端updatable_fields)
      formData: {
        real_name: '',
        nickname: '',
        bio: '',
        gender: 'secret',
        school: '',
        major: '',
        phone: ''
      },
      originalFormData: {},
      
      // 密码修改表单
      passwordForm: {
        old_password: '',
        new_password: '',
        confirm_password: ''
      },
      
      // 密码验证规则
      passwordRules: {
        old_password: [
          { required: true, message: '请输入当前密码', trigger: 'blur' }
        ],
        new_password: [
          { required: true, message: '请输入新密码', trigger: 'blur' },
          { min: 6, message: '密码长度不能少于6位', trigger: 'blur' }
        ],
        confirm_password: [
          { required: true, validator: validateConfirmPassword, trigger: 'blur' }
        ]
      },

      // 头像上传配置(对应独立的AvatarUploadView)
      uploadUrl: `${process.env.VUE_APP_API_URL || '/api'}/users/avatar/`,
      uploadHeaders: {
        Authorization: `Bearer ${this.$store.state.user.token}`
      }
    }
  },
  
  computed: {
    ...mapGetters('user', [
      'userId',
      'real_name',
      'email',
      'avatar',
      'nickname',
      'phone',
      'bio',
      'gender',
      'school',
      'major',
      'hasStudentProfile',
      'hasTeacherProfile',
      'studentId',
      'teacherId',
      'createdAt'
    ]),
    // 本地计算属性
    isStudent() {
      return this.hasStudentProfile
    },
    isTeacher() {
      return this.hasTeacherProfile
    }
  },

  created() {
    this.loadUserProfile()
  },

  methods: {
    // 加载用户完整资料
    async loadUserProfile() {
      try {
        await this.$store.dispatch('user/getUserInfo')
        this.syncFormData()
      } catch (error) {
        console.error('加载用户资料失败:', error)
      }
    },

    // 同步表单数据(对应后端可更新字段)
    syncFormData() {
      this.formData = {
        real_name: this.real_name,
        nickname: this.nickname,
        bio: this.bio || '',
        gender: this.gender || 'secret',
        school: this.school || '',
        major: this.major || '',
        phone: this.phone || ''
      }
    },

    // 个人信息编辑
    startEditInfo() {
      this.originalFormData = { ...this.formData }
      this.editingInfo = true
    },

    async saveInfo() {
      // 验证必填字段
      if (!this.formData.nickname || !this.formData.nickname.trim()) {
        this.$message.error('昵称不能为空')
        return
      }

      this.saving = true
      try {
        // 调用API更新用户信息
        const updatedUser =await userAPI.updateUserInfo(this.formData)
        
        // 直接更新 Vuex，不需要再额外发一个 getUserInfo 请求了
        this.$store.dispatch('user/updateUserInfo', updatedUser);
        
        this.$message.success('个人信息保存成功')
        this.editingInfo = false
      } catch (error) {
        console.error('保存个人信息失败:', error)
        this.$message.error(error.message || '保存失败，请稍后重试')
      } finally {
        this.saving = false
      }
    },

    cancelEditInfo() {
      this.formData = { ...this.originalFormData }
      this.editingInfo = false
    },
    
    // 密码设置
    savePassword() {
      this.$refs.passwordForm.validate(async (valid) => {
        if (!valid) return

        this.changingPassword = true
        try {
          await authAPI.changePassword(this.passwordForm)
          this.$message.success('密码修改成功，3秒后将自动退出登录')
          
          // 清空表单
          this.resetPasswordForm()
          
          // 3秒后退出登录
          setTimeout(async () => {
            try {
              await this.$store.dispatch('user/logout')
              this.$router.push('/login')
            } catch (error) {
              console.error('退出登录失败:', error)
              // 即使API调用失败也清除本地状态并跳转
              this.$router.push('/login')
            }
          }, 3000)
        } catch (error) {
          console.error('修改密码失败:', error)
          this.$message.error(error.message || '修改密码失败')
        } finally {
          this.changingPassword = false
        }
      })
    },

    resetPasswordForm() {
      this.passwordForm = {
        old_password: '',
        new_password: '',
        confirm_password: ''
      }
      this.$refs.passwordForm?.clearValidate()
    },

    // 头像上传(处理后端AvatarUploadView返回)
    handleAvatarSuccess(response) {
      if (response.code === 200) {
        this.$message.success(response.message || '头像上传成功')
        // 重新加载用户信息以更新头像
        this.$store.dispatch('user/getUserInfo')
      } else {
        this.$message.error(response.message || '头像上传失败')
      }
    },

    beforeAvatarUpload(file) {
      const isImage = file.type.startsWith('image/')
      const isLt2M = file.size / 1024 / 1024 < 2

      if (!isImage) {
        this.$message.error('只能上传图片文件')
        return false
      }
      
      if (!isLt2M) {
        this.$message.error('图片大小不能超过 2MB')
        return false
      }
      return true
    }
  }
}
</script>

<style scoped>
.my-profile {
  padding: 2rem;
  max-width: 900px;
  margin: 0 auto;
}

.profile-header {
  margin-bottom: 2rem;
}

.profile-card {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  gap: 2rem;
  align-items: center;
}

.avatar-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  flex-shrink: 0;
}

.avatar-upload {
  margin-top: 0.5rem;
}

.user-info {
  flex: 1;
}

.user-info h2 {
  margin: 0 0 0.5rem 0;
  color: #2c3e50;
}

.real_name {
  color: #95a5a6;
  margin: 0 0 0.25rem 0;
  font-size: 0.9rem;
}

.email {
  color: #7f8c8d;
  margin: 0 0 0.75rem 0;
  font-size: 0.9rem;
}

.profile-content {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.tab-content {
  padding: 1.5rem 0;
}

.action-buttons {
  margin-top: 2rem;
  display: flex;
  gap: 1rem;
}

/* 表单样式优化 */
.el-form {
  max-width: 600px;
}

.el-form-item {
  margin-bottom: 22px;
}

/* 只读字段样式 */
.el-form-item >>> .el-input.is-disabled .el-input__inner {
  background-color: #f5f7fa;
  border-color: #e4e7ed;
  color: #909399;
  cursor: not-allowed;
}

.el-form-item >>> .el-input-group__append {
  background-color: #f5f7fa;
  border-color: #e4e7ed;
}

/* 标签样式 */
.el-tag {
  margin-top: 0.5rem;
}

@media (max-width: 768px) {
  .profile-card {
    flex-direction: column;
    text-align: center;
  }
  
  .el-form {
    max-width: 100%;
  }
}
</style>
