<template>
  <div class="certificate-share-view">
    <!-- 证书未找到 -->
    <div v-if="notFound" class="not-found">
      <div class="empty-state">
        <h1>❌ 证书不存在或已过期</h1>
        <p>此分享链接可能已过期或已被撤销。</p>
        <el-button type="primary" @click="goHome">返回首页</el-button>
      </div>
    </div>

    <!-- 需要密码 -->
    <div v-else-if="needPassword && !authenticated" class="password-dialog">
      <div class="password-container">
        <h2>🔐 证书受密码保护</h2>
        <p>请输入密码以查看此证书</p>
        <el-input
          v-model="password"
          type="password"
          placeholder="请输入密码"
          @keyup.enter="verifyPassword"
        ></el-input>
        <el-button
          type="primary"
          @click="verifyPassword"
          :loading="verifyLoading"
          style="margin-top: 1rem; width: 100%"
        >
          验证
        </el-button>
      </div>
    </div>

    <!-- 证书内容 -->
    <div v-else-if="certificate && authenticated" class="certificate-container">
      <!-- 证书卡片 -->
      <div class="certificate-card">
        <div class="certificate-header">
          <h1>🎓 课程完成证书</h1>
          <p class="share-time">分享于 {{ formatDate(certificate.shareTime) }}</p>
        </div>

        <div class="certificate-content">
          <div class="cert-section">
            <h3>学生信息</h3>
            <div class="info-row">
              <span class="label">学生姓名：</span>
              <span class="value">{{ certificate.studentName }}</span>
            </div>
            <div class="info-row">
              <span class="label">学号：</span>
              <span class="value">{{ certificate.studentId }}</span>
            </div>
          </div>

          <div class="cert-section">
            <h3>课程信息</h3>
            <div class="info-row">
              <span class="label">课程名称：</span>
              <span class="value">{{ certificate.courseName }}</span>
            </div>
            <div class="info-row">
              <span class="label">讲师：</span>
              <span class="value">{{ certificate.instructorName }}</span>
            </div>
            <div class="info-row">
              <span class="label">课程班期：</span>
              <span class="value">{{ certificate.termName }}</span>
            </div>
          </div>

          <div class="cert-section">
            <h3>成绩信息</h3>
            <div class="info-row">
              <span class="label">最终成绩：</span>
              <span class="value grade" :class="getGradeClass(certificate.score)">
                {{ certificate.score }} 分
              </span>
            </div>
            <div class="info-row">
              <span class="label">学分：</span>
              <span class="value">{{ certificate.credits }} 学分</span>
            </div>
          </div>

          <div class="cert-section">
            <h3>颁发信息</h3>
            <div class="info-row">
              <span class="label">证书编号：</span>
              <span class="value certificate-number">{{ certificate.certificateNumber }}</span>
            </div>
            <div class="info-row">
              <span class="label">颁发日期：</span>
              <span class="value">{{ formatDate(certificate.issueDate) }}</span>
            </div>
            <div class="info-row" v-if="certificate.expiryDate">
              <span class="label">有效期至：</span>
              <span class="value">{{ formatDate(certificate.expiryDate) }}</span>
            </div>
          </div>
        </div>

        <!-- 证书印章 -->
        <div class="certificate-seal">
          <div class="seal-circle">
            <span class="seal-text">官方</span>
            <span class="seal-text">印章</span>
          </div>
        </div>
      </div>

      <!-- 操作按钮 -->
      <div class="actions">
        <el-button type="primary" @click="downloadCertificate" :loading="downloadLoading">
          📥 下载证书
        </el-button>
        <el-button @click="printCertificate">
          🖨️ 打印
        </el-button>
        <el-button @click="backToShare">
          🔙 返回
        </el-button>
      </div>

      <!-- 分享统计 -->
      <div class="share-stats" v-if="certificate.shareStats">
        <h3>分享统计</h3>
        <div class="stats-row">
          <span>👁️ 浏览次数：{{ certificate.shareStats.viewCount }}</span>
          <span>📤 分享次数：{{ certificate.shareStats.shareCount }}</span>
        </div>
      </div>
    </div>

    <!-- 加载中 -->
    <div v-else class="loading">
      <el-spin description="加载中..."></el-spin>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CertificateShareView',
  data() {
    return {
      certificate: null,
      notFound: false,
      needPassword: false,
      authenticated: false,
      password: '',
      verifyLoading: false,
      downloadLoading: false,
      shareCode: ''
    }
  },
  created() {
    this.shareCode = this.$route.params.shareCode
    this.loadCertificate()
  },
  methods: {
    async loadCertificate() {
      try {
        // 模拟 API 调用：获取分享的证书信息
        // 实际使用时，需要调用真实 API
        const response = await this.getCertificateByShareCode(this.shareCode)

        if (response && response.data) {
          this.certificate = response.data
          if (this.certificate.isPasswordProtected) {
            this.needPassword = true
            this.authenticated = false
          } else {
            this.authenticated = true
          }
        } else {
          this.notFound = true
        }
      } catch (error) {
        console.error('加载证书失败', error)
        this.notFound = true
      }
    },

    async verifyPassword() {
      if (!this.password) {
        this.$message.warning('请输入密码')
        return
      }

      this.verifyLoading = true
      try {
        // 模拟 API 调用：验证密码
        const response = await this.verifyCertificatePassword(
          this.shareCode,
          this.password
        )

        if (response && response.success) {
          this.authenticated = true
          this.$message.success('密码正确')
        } else {
          this.$message.error('密码错误，请重试')
        }
      } catch (error) {
        console.error('密码验证失败', error)
        this.$message.error('验证失败，请稍后重试')
      } finally {
        this.verifyLoading = false
      }
    },

    async downloadCertificate() {
      this.downloadLoading = true
      try {
        // 模拟下载 PDF
        // 实际使用时需要调用后端 PDF 生成 API
        const link = document.createElement('a')
        link.href = `/api/certificate/${this.certificate.id}/download-pdf`
        link.download = `${this.certificate.courseName}_证书.pdf`
        link.click()

        // 记录下载事件
        await this.recordCertificateAction('download')
        this.$message.success('下载成功')
      } catch (error) {
        console.error('下载失败', error)
        this.$message.error('下载失败，请稍后重试')
      } finally {
        this.downloadLoading = false
      }
    },

    printCertificate() {
      window.print()
      // 记录打印事件
      this.recordCertificateAction('print')
    },

    backToShare() {
      this.$router.back()
    },

    goHome() {
      this.$router.push('/')
    },

    formatDate(date) {
      if (!date) return '-'
      const d = new Date(date)
      const year = d.getFullYear()
      const month = String(d.getMonth() + 1).padStart(2, '0')
      const day = String(d.getDate()).padStart(2, '0')
      return `${year}-${month}-${day}`
    },

    getGradeClass(score) {
      if (score >= 90) return 'excellent'
      if (score >= 80) return 'good'
      if (score >= 70) return 'pass'
      return 'fail'
    },

    // API 模拟方法（实际开发时替换为真实 API 调用）
    async getCertificateByShareCode() {
      // TODO: 调用真实 API
      return Promise.resolve({
        data: {
          id: '12345',
          studentName: '张三',
          studentId: 'STU001',
          courseName: 'Vue.js 全栈开发',
          instructorName: '李四',
          termName: '2024年秋季班',
          score: 92,
          credits: 3,
          certificateNumber: 'CERT-2024-12345',
          issueDate: '2024-12-15',
          expiryDate: '2026-12-15',
          isPasswordProtected: false,
          shareTime: '2024-12-16',
          shareStats: {
            viewCount: 15,
            shareCount: 3
          }
        }
      })
    },

    async verifyCertificatePassword(shareCode, password) {
      // TODO: 调用真实 API
      return Promise.resolve({
        success: password === 'demo123'
      })
    },

    async recordCertificateAction() {
      // TODO: 调用真实 API 记录用户操作
      try {
        // API 调用
      } catch (error) {
        console.error('记录操作失败', error)
      }
    }
  }
}
</script>

<style scoped>
.certificate-share-view {
  padding: 2rem;
  max-width: 900px;
  margin: 0 auto;
}

.not-found,
.password-dialog,
.loading {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
}

.empty-state {
  text-align: center;
  color: #606266;
}

.empty-state h1 {
  margin: 1rem 0;
  color: #f56c6c;
}

.empty-state p {
  margin: 1rem 0;
  font-size: 16px;
}

.password-container {
  background: white;
  border-radius: 8px;
  padding: 3rem 2rem;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

.password-container h2 {
  margin: 0 0 1rem 0;
  color: #303133;
  text-align: center;
}

.password-container p {
  color: #606266;
  text-align: center;
  margin-bottom: 1rem;
}

.certificate-container {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.certificate-card {
  background: linear-gradient(135deg, #fafbfc 0%, #f5f7fa 100%);
  border: 2px solid #dcdfe6;
  border-radius: 12px;
  padding: 3rem;
  position: relative;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  print-color-adjust: exact;
  -webkit-print-color-adjust: exact;
}

.certificate-header {
  text-align: center;
  margin-bottom: 2rem;
  border-bottom: 3px solid #409eff;
  padding-bottom: 1rem;
}

.certificate-header h1 {
  margin: 0;
  color: #303133;
  font-size: 28px;
  font-weight: 700;
}

.share-time {
  color: #909399;
  font-size: 12px;
  margin-top: 0.5rem;
}

.certificate-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  margin: 2rem 0;
}

.cert-section {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  border-left: 4px solid #409eff;
}

.cert-section h3 {
  margin: 0 0 1rem 0;
  color: #303133;
  font-size: 14px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.info-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 0;
  border-bottom: 1px solid #f0f0f0;
}

.info-row:last-child {
  border-bottom: none;
}

.label {
  color: #606266;
  font-weight: 500;
  min-width: 100px;
}

.value {
  color: #303133;
  font-weight: 600;
  text-align: right;
}

.grade {
  font-size: 18px;
  padding: 0.25rem 0.75rem;
  border-radius: 4px;
}

.grade.excellent {
  background: #f0f9ff;
  color: #67c23a;
}

.grade.good {
  background: #fef3c7;
  color: #e6a23c;
}

.grade.pass {
  background: #dbeafe;
  color: #409eff;
}

.grade.fail {
  background: #fee2e2;
  color: #f56c6c;
}

.certificate-number {
  font-family: 'Courier New', monospace;
  font-size: 12px;
  letter-spacing: 2px;
}

.certificate-seal {
  position: absolute;
  bottom: 2rem;
  right: 2rem;
  width: 120px;
  height: 120px;
  opacity: 0.3;
}

.seal-circle {
  width: 100%;
  height: 100%;
  border: 3px solid #e6a23c;
  border-radius: 50%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  transform: rotate(-45deg);
  font-weight: 700;
  color: #e6a23c;
  font-size: 14px;
  text-align: center;
}

.seal-text {
  display: block;
  line-height: 1;
}

.actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

.actions .el-button {
  min-width: 120px;
}

.share-stats {
  background: #f5f7fa;
  border-radius: 8px;
  padding: 1.5rem;
  text-align: center;
}

.share-stats h3 {
  margin: 0 0 1rem 0;
  color: #303133;
}

.stats-row {
  display: flex;
  gap: 2rem;
  justify-content: center;
  color: #606266;
}

/* 打印样式 */
@media print {
  .certificate-share-view {
    padding: 0;
  }

  .actions,
  .share-stats {
    display: none;
  }

  .certificate-card {
    box-shadow: none;
    border: 1px solid #dcdfe6;
    padding: 2rem;
  }

  .certificate-seal {
    opacity: 1;
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .certificate-content {
    grid-template-columns: 1fr;
  }

  .certificate-card {
    padding: 1.5rem;
  }

  .certificate-header h1 {
    font-size: 22px;
  }

  .certificate-seal {
    width: 80px;
    height: 80px;
    bottom: 1rem;
    right: 1rem;
  }

  .seal-circle {
    font-size: 12px;
  }

  .stats-row {
    flex-direction: column;
    gap: 1rem;
  }
}
</style>
