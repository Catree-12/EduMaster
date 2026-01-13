<template>
  <el-dialog title="分享证书" :visible.sync="dialogVisible" width="600px">
    <div v-if="certificate" class="certificate-share">
      <!-- 分享链接 -->
      <div class="share-section">
        <h4>分享链接</h4>
        <div class="link-input">
          <el-input v-model="shareLink" type="text" readonly />
          <el-button type="primary" @click="copyLink">复制</el-button>
        </div>
      </div>

      <!-- 二维码 -->
      <div class="share-section" v-if="qrCode">
        <h4>分享二维码</h4>
        <div class="qrcode-container">
          <img :src="qrCode" alt="分享二维码" class="qrcode" />
          <el-button @click="downloadQRCode" type="text">下载二维码</el-button>
        </div>
      </div>

      <!-- 分享到社交媒体 -->
      <div class="share-section">
        <h4>分享到社交媒体</h4>
        <div class="social-share">
          <el-tooltip content="复制链接">
            <el-button icon="el-icon-document-copy" circle @click="copyLink" />
          </el-tooltip>
          <el-tooltip content="微信好友">
            <el-button icon="el-icon-user" circle />
          </el-tooltip>
          <el-tooltip content="微信朋友圈">
            <el-button icon="el-icon-share" circle />
          </el-tooltip>
          <el-tooltip content="QQ">
            <el-button icon="el-icon-chat-dot-round" circle />
          </el-tooltip>
          <el-tooltip content="QQ空间">
            <el-button icon="el-icon-picture" circle />
          </el-tooltip>
        </div>
      </div>

      <!-- 分享设置 -->
      <div class="share-section">
        <h4>分享设置</h4>
        <el-checkbox v-model="enablePassword">
          使用密码保护
        </el-checkbox>
        <el-input
          v-if="enablePassword"
          v-model="password"
          type="password"
          placeholder="输入分享密码"
          style="margin-top: 10px"
        />

        <el-checkbox v-model="enableExpiry" style="margin-top: 15px">
          设置过期时间
        </el-checkbox>
        <el-date-picker
          v-if="enableExpiry"
          v-model="expiryDate"
          type="date"
          placeholder="选择过期日期"
          style="margin-top: 10px; width: 100%"
        />
      </div>

      <!-- 分享统计 -->
      <div class="share-stats">
        <el-row :gutter="20">
          <el-col :xs="12">
            <div class="stat">
              <p class="label">已被查看</p>
              <p class="value">{{ certificate.viewCount || 0 }} 次</p>
            </div>
          </el-col>
          <el-col :xs="12">
            <div class="stat">
              <p class="label">已被分享</p>
              <p class="value">{{ certificate.shareCount || 0 }} 次</p>
            </div>
          </el-col>
        </el-row>
      </div>

      <!-- 说明 -->
      <div class="share-tips">
        <p>💡 提示：</p>
        <ul>
          <li>分享链接可让任何人查看你的证书</li>
          <li>可设置密码或过期时间保护分享</li>
          <li>分享统计显示有多少人查看了你的证书</li>
        </ul>
      </div>
    </div>

    <span slot="footer" class="dialog-footer">
      <el-button @click="dialogVisible = false">取消</el-button>
      <el-button type="primary" @click="saveSettings">保存设置</el-button>
    </span>
  </el-dialog>
</template>

<script>
export default {
  name: 'CertificateShare',
  props: {
    visible: Boolean,
    certificate: Object
  },
  data() {
    return {
      dialogVisible: false,
      shareLink: '',
      qrCode: '',
      enablePassword: false,
      password: '',
      enableExpiry: false,
      expiryDate: null
    }
  },
  watch: {
    visible(newVal) {
      this.dialogVisible = newVal
      if (newVal && this.certificate) {
        this.generateShareLink()
      }
    }
  },
  methods: {
    // 生成分享链接
    generateShareLink() {
      this.$api.post(`/certificate/${this.certificate.id}/generate-share-link`, {
        password: this.enablePassword ? this.password : undefined,
        expiryDays: this.enableExpiry ? this.calculateDays() : undefined
      })
        .then(res => {
          this.shareLink = res.data.shareLink
          this.qrCode = res.data.qrCode
        })
        .catch(() => {
          this.$message.error('生成分享链接失败')
        })
    },

    // 复制链接
    copyLink() {
      navigator.clipboard.writeText(this.shareLink)
        .then(() => {
          this.$message.success('链接已复制到剪贴板')
        })
        .catch(() => {
          // 备用方案
          const textarea = document.createElement('textarea')
          textarea.value = this.shareLink
          document.body.appendChild(textarea)
          textarea.select()
          document.execCommand('copy')
          document.body.removeChild(textarea)
          this.$message.success('链接已复制到剪贴板')
        })
    },

    // 下载二维码
    downloadQRCode() {
      const link = document.createElement('a')
      link.href = this.qrCode
      link.download = `证书分享码_${this.certificate.courseName}.png`
      link.click()
    },

    // 计算天数
    calculateDays() {
      if (!this.expiryDate) return undefined
      return Math.ceil((new Date(this.expiryDate) - new Date()) / (1000 * 60 * 60 * 24))
    },

    // 保存设置
    saveSettings() {
      this.generateShareLink()
      this.$message.success('分享设置已保存')
      this.$emit('update:visible', false)
    }
  }
}
</script>

<style scoped lang="scss">
.certificate-share {
  padding: 20px;
}

.share-section {
  margin-bottom: 30px;
}

.share-section h4 {
  font-size: 14px;
  color: #333;
  font-weight: bold;
  margin-bottom: 12px;
}

.link-input {
  display: flex;
  gap: 10px;

  ::v-deep .el-input {
    flex: 1;
  }
}

.qrcode-container {
  text-align: center;
}

.qrcode {
  width: 200px;
  height: 200px;
  border: 1px solid #ddd;
  padding: 10px;
  border-radius: 4px;
  background: white;
  display: block;
  margin: 0 auto 15px;
}

.social-share {
  display: flex;
  gap: 15px;
  flex-wrap: wrap;

  ::v-deep .el-button {
    &--circle {
      width: 40px;
      height: 40px;
      border-radius: 50%;
    }
  }
}

.share-stats {
  background: #f5f7fa;
  border-radius: 4px;
  padding: 20px;
  margin-bottom: 20px;
}

.stat {
  text-align: center;
}

.label {
  font-size: 12px;
  color: #999;
  margin: 0;
}

.value {
  font-size: 24px;
  font-weight: bold;
  color: #1890ff;
  margin: 5px 0 0 0;
}

.share-tips {
  background: #e6f7ff;
  border-left: 4px solid #1890ff;
  padding: 12px 15px;
  border-radius: 2px;
}

.share-tips p {
  margin: 0 0 8px 0;
  font-size: 13px;
  color: #0050b3;
  font-weight: bold;
}

.share-tips p:first-child {
  margin-bottom: 10px;
}

.share-tips ul {
  margin: 0;
  padding-left: 20px;
}

.share-tips li {
  font-size: 12px;
  color: #0050b3;
  margin: 5px 0;
}
</style>
