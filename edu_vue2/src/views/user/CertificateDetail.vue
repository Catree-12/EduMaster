<template>
  <el-dialog title="证书详情" :visible.sync="dialogVisible" width="80%" @close="handleClose">
    <div v-if="certificate" class="certificate-detail">
      <!-- 证书预览 -->
      <div class="certificate-preview">
        <div class="cert-card">
          <div class="cert-header">
            <img src="/logo.png" alt="logo" class="logo" />
            <h2>{{ certificate.certificateContent.title }}</h2>
          </div>

          <p class="statement">{{ certificate.certificateContent.statement }}</p>

          <div class="cert-info">
            <div class="info-row">
              <span class="label">学生名称：</span>
              <span class="value">{{ certificate.userName }}</span>
            </div>
            <div class="info-row">
              <span class="label">课程名称：</span>
              <span class="value">{{ certificate.courseName }}</span>
            </div>
            <div class="info-row">
              <span class="label">班期：</span>
              <span class="value">{{ certificate.termName }}</span>
            </div>
            <div class="info-row">
              <span class="label">考试成绩：</span>
              <span class="value">{{ certificate.score }} / {{ certificate.passingScore }}</span>
            </div>
            <div class="info-row">
              <span class="label">颁发日期：</span>
              <span class="value">{{ certificate.issueDate }}</span>
            </div>
            <div class="info-row">
              <span class="label">证书编号：</span>
              <span class="value cert-no">{{ certificate.certificateNo }}</span>
            </div>
          </div>

          <img src="/seal.png" alt="印章" class="seal" />
        </div>
      </div>

      <!-- 操作按钮 -->
      <div class="actions">
        <el-button type="primary" icon="el-icon-download" @click="download">
          下载 PDF
        </el-button>
        <el-button icon="el-icon-printer" @click="print">
          打印
        </el-button>
        <el-button icon="el-icon-share" @click="handleShare">
          分享
        </el-button>
      </div>
    </div>
  </el-dialog>
</template>

<script>
export default {
  name: 'CertificateDetail',
  props: {
    visible: Boolean,
    certificate: Object
  },
  data() {
    return {
      dialogVisible: false
    }
  },
  watch: {
    visible(newVal) {
      this.dialogVisible = newVal
    }
  },
  methods: {
    download() {
      window.location.href = `/api/certificate/${this.certificate.id}/download`
      this.$message.success('下载开始...')
    },

    print() {
      window.print()
    },

    handleShare() {
      this.$emit('update:visible', false)
      this.$parent.$emit('share-certificate', this.certificate)
    },

    handleClose() {
      this.$emit('update:visible', false)
    }
  }
}
</script>

<style scoped lang="scss">
.certificate-detail {
  .certificate-preview {
    margin: 20px 0;
    text-align: center;
  }

  .cert-card {
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    border: 3px solid #1890ff;
    border-radius: 4px;
    padding: 40px;
    position: relative;
    min-height: 500px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);

    .cert-header {
      margin-bottom: 30px;

      .logo {
        width: 60px;
        height: 60px;
        margin-bottom: 15px;
      }

      h2 {
        font-size: 32px;
        color: #1890ff;
        margin: 0;
        font-weight: bold;
      }
    }

    .statement {
      font-size: 14px;
      color: #333;
      line-height: 1.8;
      margin: 20px 0;
      max-width: 500px;
    }

    .cert-info {
      margin: 30px 0;
      text-align: left;

      .info-row {
        display: flex;
        justify-content: center;
        margin: 8px 0;

        .label {
          font-weight: bold;
          color: #333;
          margin-right: 20px;
          min-width: 100px;
        }

        .value {
          color: #666;

          &.cert-no {
            font-family: monospace;
            color: #1890ff;
          }
        }
      }
    }

    .seal {
      width: 100px;
      position: absolute;
      bottom: 20px;
      right: 30px;
      opacity: 0.7;
    }
  }

  .actions {
    display: flex;
    justify-content: center;
    gap: 20px;
    margin-top: 30px;
    padding-top: 20px;
    border-top: 1px solid #f0f0f0;
  }
}
</style>
