<template>
  <div class="system-settings">
    <div class="page-header">
      <h1>系统设置</h1>
      <p class="subtitle">配置平台参数和功能选项</p>
    </div>

    <el-tabs v-model="activeTab" type="border-card">
      <!-- 基本设置 -->
      <el-tab-pane label="基本设置" name="basic">
        <el-form :model="basicSettings" label-width="150px">
          <el-form-item label="平台名称">
            <el-input v-model="basicSettings.platformName" style="width: 400px"></el-input>
          </el-form-item>
          <el-form-item label="平台简介">
            <el-input 
              type="textarea" 
              :rows="4"
              v-model="basicSettings.platformDesc" 
              style="width: 400px">
            </el-input>
          </el-form-item>
          <el-form-item label="联系邮箱">
            <el-input v-model="basicSettings.contactEmail" style="width: 400px"></el-input>
          </el-form-item>
          <el-form-item label="客服电话">
            <el-input v-model="basicSettings.phone" style="width: 400px"></el-input>
          </el-form-item>
          <el-form-item label="平台Logo">
            <el-upload
              class="logo-uploader"
              action="#"
              :show-file-list="false"
              :auto-upload="false">
              <img v-if="basicSettings.logo" :src="basicSettings.logo" class="logo">
              <i v-else class="el-icon-plus logo-uploader-icon"></i>
            </el-upload>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="saveBasicSettings">保存设置</el-button>
          </el-form-item>
        </el-form>
      </el-tab-pane>

      <!-- 课程设置 -->
      <el-tab-pane label="课程设置" name="course">
        <el-form :model="courseSettings" label-width="180px">
          <el-form-item label="课程审核开关">
            <el-switch 
              v-model="courseSettings.auditEnabled"
              active-text="开启"
              inactive-text="关闭">
            </el-switch>
            <p class="setting-tip">关闭后课程发布无需审核，直接上架</p>
          </el-form-item>
          <el-form-item label="课程默认有效期（天）">
            <el-input-number 
              v-model="courseSettings.defaultValidDays" 
              :min="0"
              :max="3650">
            </el-input-number>
            <p class="setting-tip">0 表示永久有效</p>
          </el-form-item>
          <el-form-item label="允许用户创建课程">
            <el-switch 
              v-model="courseSettings.allowUserCreate"
              active-text="允许"
              inactive-text="禁止">
            </el-switch>
          </el-form-item>
          <el-form-item label="课程最大章节数">
            <el-input-number 
              v-model="courseSettings.maxChapters" 
              :min="1"
              :max="100">
            </el-input-number>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="saveCourseSettings">保存设置</el-button>
          </el-form-item>
        </el-form>
      </el-tab-pane>

      <!-- 考试设置 -->
      <el-tab-pane label="考试设置" name="exam">
        <el-form :model="examSettings" label-width="180px">
          <el-form-item label="考试默认时长（分钟）">
            <el-input-number 
              v-model="examSettings.defaultDuration" 
              :min="10"
              :max="480">
            </el-input-number>
          </el-form-item>
          <el-form-item label="及格分数线">
            <el-input-number 
              v-model="examSettings.passingScore" 
              :min="0"
              :max="100">
            </el-input-number>
          </el-form-item>
          <el-form-item label="允许重考次数">
            <el-input-number 
              v-model="examSettings.maxRetries" 
              :min="0"
              :max="10">
            </el-input-number>
            <p class="setting-tip">0 表示无限次</p>
          </el-form-item>
          <el-form-item label="自动批改客观题">
            <el-switch 
              v-model="examSettings.autoGrading"
              active-text="开启"
              inactive-text="关闭">
            </el-switch>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="saveExamSettings">保存设置</el-button>
          </el-form-item>
        </el-form>
      </el-tab-pane>

      <!-- 证书设置 -->
      <el-tab-pane label="证书设置" name="certificate">
        <el-form :model="certSettings" label-width="180px">
          <el-form-item label="启用电子证书">
            <el-switch 
              v-model="certSettings.enabled"
              active-text="启用"
              inactive-text="禁用">
            </el-switch>
          </el-form-item>
          <el-form-item label="证书颁发条件">
            <el-radio-group v-model="certSettings.condition">
              <el-radio label="pass">考试及格</el-radio>
              <el-radio label="complete">完成课程</el-radio>
              <el-radio label="both">两者都满足</el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item label="证书编号前缀">
            <el-input v-model="certSettings.numberPrefix" style="width: 200px"></el-input>
          </el-form-item>
          <el-form-item label="允许分享证书">
            <el-switch 
              v-model="certSettings.allowShare"
              active-text="允许"
              inactive-text="禁止">
            </el-switch>
          </el-form-item>
          <el-form-item label="证书模板">
            <el-upload
              class="template-uploader"
              action="#"
              :show-file-list="false"
              :auto-upload="false">
              <el-button type="primary" size="small">上传模板</el-button>
            </el-upload>
            <p class="setting-tip">推荐尺寸: 1920x1080px</p>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="saveCertSettings">保存设置</el-button>
          </el-form-item>
        </el-form>
      </el-tab-pane>

      <!-- 邮件设置 -->
      <el-tab-pane label="邮件设置" name="email">
        <el-form :model="emailSettings" label-width="150px">
          <el-form-item label="SMTP服务器">
            <el-input v-model="emailSettings.smtpHost" style="width: 400px"></el-input>
          </el-form-item>
          <el-form-item label="SMTP端口">
            <el-input-number v-model="emailSettings.smtpPort" :min="1" :max="65535"></el-input-number>
          </el-form-item>
          <el-form-item label="发件邮箱">
            <el-input v-model="emailSettings.senderEmail" style="width: 400px"></el-input>
          </el-form-item>
          <el-form-item label="邮箱密码">
            <el-input 
              type="password" 
              v-model="emailSettings.senderPassword" 
              show-password
              style="width: 400px">
            </el-input>
          </el-form-item>
          <el-form-item label="启用SSL">
            <el-switch v-model="emailSettings.ssl"></el-switch>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="saveEmailSettings">保存设置</el-button>
            <el-button @click="testEmail">发送测试邮件</el-button>
          </el-form-item>
        </el-form>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
export default {
  name: 'SystemSettings',
  data() {
    return {
      activeTab: 'basic',
      basicSettings: {
        platformName: '在线教育平台',
        platformDesc: '专业的在线学习平台，提供丰富的课程资源',
        contactEmail: 'support@example.com',
        phone: '400-123-4567',
        logo: ''
      },
      courseSettings: {
        auditEnabled: true,
        defaultValidDays: 365,
        allowUserCreate: true,
        maxChapters: 50
      },
      examSettings: {
        defaultDuration: 120,
        passingScore: 60,
        maxRetries: 3,
        autoGrading: true
      },
      certSettings: {
        enabled: true,
        condition: 'pass',
        numberPrefix: 'CERT',
        allowShare: true
      },
      emailSettings: {
        smtpHost: 'smtp.example.com',
        smtpPort: 465,
        senderEmail: 'noreply@example.com',
        senderPassword: '',
        ssl: true
      }
    }
  },
  methods: {
    saveBasicSettings() {
      this.$message.success('基本设置已保存')
    },
    saveCourseSettings() {
      this.$message.success('课程设置已保存')
    },
    saveExamSettings() {
      this.$message.success('考试设置已保存')
    },
    saveCertSettings() {
      this.$message.success('证书设置已保存')
    },
    saveEmailSettings() {
      this.$message.success('邮件设置已保存')
    },
    testEmail() {
      this.$message.info('测试邮件发送中...')
    }
  }
}
</script>

<style scoped>
.system-settings {
  padding: 20px;
}

.page-header h1 {
  margin: 0 0 8px 0;
  font-size: 24px;
}

.page-header .subtitle {
  margin: 0 0 20px 0;
  color: #909399;
  font-size: 14px;
}

.setting-tip {
  margin: 5px 0 0 0;
  font-size: 12px;
  color: #909399;
}

.logo-uploader {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  overflow: hidden;
}

.logo-uploader:hover {
  border-color: #409EFF;
}

.logo-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 178px;
  height: 178px;
  line-height: 178px;
  text-align: center;
  display: block;
}

.logo {
  width: 178px;
  height: 178px;
  display: block;
  object-fit: contain;
}
</style>
