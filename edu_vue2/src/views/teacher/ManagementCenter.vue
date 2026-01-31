<template>
  <div class="management-center">
    <!-- 顶部标题栏 -->
    <div class="header-bar">
      <el-button icon="el-icon-arrow-left" class="back-btn" @click="goBack">返回</el-button>
      <h2 class="title">管理中心</h2>
    </div>

    <!-- 主容器 -->
    <div class="main-container">
      <!-- 页签导航 -->
      <el-tabs v-model="activeTab" class="management-tabs">
        <!-- Tab 1: 教务组织 -->
        <el-tab-pane label="教务组织" name="academic">
          <div class="tab-content">
            <!-- 顶部操作栏 -->
            <div class="operation-bar">
              <el-button type="primary" icon="el-icon-plus" @click="showTermDialog = true">
                + 新增班期
              </el-button>
            </div>

            <!-- 班期列表 -->
            <div v-if="terms.length > 0" class="term-list">
              <div v-for="term in terms" :key="term.id" class="term-card">
                <!-- 班期头部 -->
                <div class="term-header">
                  <div class="term-info">
                    <h3 class="term-name">{{ term.name }}</h3>
                    <div class="term-meta">
                      <span class="term-date">{{ term.startDate }} ~ {{ term.endDate }}</span>
                      <el-tag 
                        :type="getTermStatusType(term.status)" 
                        size="small"
                      >
                        {{ getTermStatusText(term.status) }}
                      </el-tag>
                    </div>
                  </div>
                  <div class="term-actions">
                    <el-button type="text" @click="editTerm(term)">编辑班期</el-button>
                    <el-button type="primary" size="small" @click="showAddClassDialog(term)">
                      + 添加班级
                    </el-button>
                  </div>
                </div>

                <!-- 班级列表 -->
                <div v-if="getTermClasses(term.id).length > 0" class="class-list">
                  <el-table :data="getTermClasses(term.id)" style="width: 100%">
                    <el-table-column prop="name" label="班级名称" min-width="150" />
                    <el-table-column prop="inviteCode" label="班级邀请码" width="140" align="center" />
                    <el-table-column label="学生人数" width="120" align="center">
                      <template slot-scope="scope">
                        <span>{{ scope.row.studentCount }} / {{ scope.row.capacity }}</span>
                      </template>
                    </el-table-column>
                    <el-table-column label="操作" width="200" align="center">
                      <template slot-scope="scope">
                        <el-button type="text" @click="manageStudents(scope.row)">成员管理</el-button>
                        <el-button type="text" style="color: #F56C6C;" @click="deleteClass(scope.row)">删除</el-button>
                      </template>
                    </el-table-column>
                  </el-table>
                </div>
                <div v-else class="no-classes">
                  <span>暂无班级，点击"添加班级"创建</span>
                </div>
              </div>
            </div>

            <!-- 空状态 -->
            <div v-else class="empty-state">
              <i class="el-icon-document-copy empty-icon"></i>
              <p>暂无班期数据</p>
              <p class="hint">创建班期后，可以在班期内创建班级并管理学生</p>
            </div>
          </div>
        </el-tab-pane>

        <!-- Tab 2: 课程设置 -->
        <el-tab-pane label="课程设置" name="course">
          <div class="tab-content">
            <!-- 课程基本属性卡片 -->
            <el-card class="setting-card" shadow="hover">
              <div slot="header">
                <span class="card-title">课程基本属性</span>
              </div>

              <el-form :model="courseSettings" label-width="120px" class="setting-form">
                <!-- 价格设置 -->
                <el-form-item label="价格设置">
                  <div class="price-inputs">
                    <el-input-number 
                      v-model="courseSettings.originalPrice" 
                      :min="0" 
                      :precision="2"
                      placeholder="原价"
                      style="width: 180px; margin-right: 20px;"
                    >
                      <template slot="prepend">原价 ¥</template>
                    </el-input-number>
                    <el-input-number 
                      v-model="courseSettings.discountPrice" 
                      :min="0" 
                      :precision="2"
                      placeholder="折扣价"
                      style="width: 180px;"
                    >
                      <template slot="prepend">折扣价 ¥</template>
                    </el-input-number>
                  </div>
                </el-form-item>

                <!-- 销售状态 -->
                <el-form-item label="销售状态">
                  <el-switch 
                    v-model="courseSettings.onSale" 
                    active-text="上架销售" 
                    inactive-text="下架"
                  />
                  <span class="form-tip">开启后，课程将在课程中心展示并允许购买</span>
                </el-form-item>

                <!-- 报名限制 -->
                <el-form-item label="报名限制">
                  <el-input-number 
                    v-model="courseSettings.maxEnrollment" 
                    :min="0" 
                    placeholder="0表示不限制"
                    style="width: 200px;"
                  />
                  <span class="form-tip">设置该课程最大允许报名的人数，0表示不限制</span>
                </el-form-item>
              </el-form>
            </el-card>

            <!-- 访问权限设置卡片 -->
            <el-card class="setting-card" shadow="hover">
              <div slot="header">
                <span class="card-title">访问权限设置</span>
              </div>

              <el-form :model="courseSettings" label-width="120px" class="setting-form">
                <!-- 公开/私有 -->
                <el-form-item label="访问权限">
                  <el-radio-group v-model="courseSettings.accessType">
                    <el-radio label="public">公开课程</el-radio>
                    <el-radio label="private">私有课程</el-radio>
                  </el-radio-group>
                  <div class="form-tip">
                    公开：所有人可见；私有：仅限邀请加入
                  </div>
                </el-form-item>

                <!-- 有效期设置 -->
                <el-form-item label="有效期设置">
                  <el-input-number 
                    v-model="courseSettings.validDays" 
                    :min="0" 
                    placeholder="0表示永久有效"
                    style="width: 200px;"
                  />
                  <span class="form-tip">学生购买后可观看的天数，0表示永久有效</span>
                </el-form-item>
              </el-form>
            </el-card>

            <!-- 保存按钮 -->
            <div class="save-bar">
              <el-button type="primary" size="medium" @click="saveCourseSettings">
                保存设置
              </el-button>
            </div>
          </div>
        </el-tab-pane>

        <!-- Tab 3: 财务订单 -->
        <el-tab-pane label="财务订单" name="finance">
          <div class="tab-content">
            <!-- 财务概览 -->
            <div class="finance-overview">
              <el-card class="overview-card">
                <div class="overview-item">
                  <div class="overview-label">今日收入</div>
                  <div class="overview-value">¥ {{ todayIncome.toFixed(2) }}</div>
                </div>
              </el-card>
              <el-card class="overview-card">
                <div class="overview-item">
                  <div class="overview-label">累计销售额</div>
                  <div class="overview-value">¥ {{ totalSales.toFixed(2) }}</div>
                </div>
              </el-card>
              <el-card class="overview-card">
                <div class="overview-item">
                  <div class="overview-label">成交订单数</div>
                  <div class="overview-value">{{ completedOrders }}</div>
                </div>
              </el-card>
            </div>

            <!-- 订单详情表格 -->
            <el-card class="order-card" shadow="hover">
              <div slot="header">
                <span class="card-title">订单详情</span>
              </div>

              <el-table :data="orders" style="width: 100%">
                <el-table-column prop="orderNo" label="订单编号" width="180" />
                <el-table-column prop="studentName" label="学生昵称" width="120" />
                <el-table-column label="支付金额" width="120" align="center">
                  <template slot-scope="scope">
                    <span class="amount-text">¥ {{ scope.row.amount.toFixed(2) }}</span>
                  </template>
                </el-table-column>
                <el-table-column prop="payTime" label="支付时间" width="180" />
                <el-table-column prop="payMethod" label="支付方式" width="120" align="center" />
                <el-table-column label="状态" width="100" align="center">
                  <template slot-scope="scope">
                    <el-tag :type="getOrderStatusType(scope.row.status)" size="small">
                      {{ getOrderStatusText(scope.row.status) }}
                    </el-tag>
                  </template>
                </el-table-column>
                <el-table-column label="操作" align="center">
                  <template slot-scope="scope">
                    <el-button type="text" @click="viewOrderDetail(scope.row)">查看详情</el-button>
                  </template>
                </el-table-column>
              </el-table>
            </el-card>
          </div>
        </el-tab-pane>
      </el-tabs>
    </div>

    <!-- 新增班期对话框 -->
    <el-dialog 
      :title="editingTerm ? '编辑班期' : '新增班期'" 
      :visible.sync="showTermDialog"
      width="500px"
    >
      <el-form :model="termForm" label-width="100px">
        <el-form-item label="班期名称">
          <el-input v-model="termForm.name" placeholder="如：2026春季学期" />
        </el-form-item>
        <el-form-item label="开始日期">
          <el-date-picker 
            v-model="termForm.startDate" 
            type="date" 
            placeholder="选择日期"
            value-format="yyyy-MM-dd"
            style="width: 100%;"
          />
        </el-form-item>
        <el-form-item label="结束日期">
          <el-date-picker 
            v-model="termForm.endDate" 
            type="date" 
            placeholder="选择日期"
            value-format="yyyy-MM-dd"
            style="width: 100%;"
          />
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="showTermDialog = false">取 消</el-button>
        <el-button type="primary" @click="submitTerm">确 定</el-button>
      </span>
    </el-dialog>

    <!-- 添加班级对话框 -->
    <el-dialog 
      title="添加班级" 
      :visible.sync="showClassDialog"
      width="500px"
    >
      <el-form :model="classForm" label-width="100px">
        <el-form-item label="班级名称">
          <el-input v-model="classForm.name" placeholder="如：高一（1）班" />
        </el-form-item>
        <el-form-item label="班级容量">
          <el-input-number v-model="classForm.capacity" :min="1" style="width: 100%;" />
        </el-form-item>
        <el-form-item label="邀请码">
          <el-input v-model="classForm.inviteCode" placeholder="自动生成或手动输入">
            <el-button slot="append" @click="generateInviteCode">生成</el-button>
          </el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="showClassDialog = false">取 消</el-button>
        <el-button type="primary" @click="submitClass">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'ManagementCenter',
  data() {
    return {
      activeTab: 'academic',
      
      // 班期相关
      showTermDialog: false,
      editingTerm: null,
      termForm: {
        name: '',
        startDate: '',
        endDate: ''
      },
      terms: [
        {
          id: 1,
          name: '2026春季学期',
          startDate: '2026-03-01',
          endDate: '2026-06-30',
          status: 'active' // active, upcoming, ended
        },
        {
          id: 2,
          name: '2025秋季学期',
          startDate: '2025-09-01',
          endDate: '2025-12-31',
          status: 'ended'
        }
      ],

      // 班级相关
      showClassDialog: false,
      currentTermId: null,
      classForm: {
        name: '',
        capacity: 50,
        inviteCode: ''
      },
      classes: [
        {
          id: 1,
          termId: 1,
          name: '高一（1）班',
          inviteCode: 'ABC123',
          capacity: 50,
          studentCount: 48
        },
        {
          id: 2,
          termId: 1,
          name: '高一（2）班',
          inviteCode: 'DEF456',
          capacity: 50,
          studentCount: 45
        },
        {
          id: 3,
          termId: 2,
          name: '高二（1）班',
          inviteCode: 'GHI789',
          capacity: 45,
          studentCount: 43
        }
      ],

      // 课程设置
      courseSettings: {
        originalPrice: 299.00,
        discountPrice: 199.00,
        onSale: true,
        maxEnrollment: 0,
        accessType: 'public',
        validDays: 365
      },

      // 财务订单
      orders: [
        {
          id: 1,
          orderNo: 'ORD20260121001',
          studentName: '张三',
          amount: 199.00,
          payTime: '2026-01-21 10:30:25',
          payMethod: '微信支付',
          status: 'paid' // paid, pending, refunded
        },
        {
          id: 2,
          orderNo: 'ORD20260121002',
          studentName: '李四',
          amount: 199.00,
          payTime: '2026-01-21 11:15:40',
          payMethod: '支付宝',
          status: 'paid'
        },
        {
          id: 3,
          orderNo: 'ORD20260120003',
          studentName: '王五',
          amount: 199.00,
          payTime: '2026-01-20 15:20:10',
          payMethod: '微信支付',
          status: 'refunded'
        }
      ]
    }
  },
  computed: {
    // 今日收入
    todayIncome() {
      const today = new Date().toISOString().split('T')[0]
      return this.orders
        .filter(order => order.status === 'paid' && order.payTime.startsWith(today))
        .reduce((sum, order) => sum + order.amount, 0)
    },
    // 累计销售额
    totalSales() {
      return this.orders
        .filter(order => order.status === 'paid')
        .reduce((sum, order) => sum + order.amount, 0)
    },
    // 成交订单数
    completedOrders() {
      return this.orders.filter(order => order.status === 'paid').length
    }
  },
  methods: {
    goBack() {
      this.$router.back()
    },

    // 班期方法
    editTerm(term) {
      this.editingTerm = term
      this.termForm = { ...term }
      this.showTermDialog = true
    },
    submitTerm() {
      if (!this.termForm.name || !this.termForm.startDate || !this.termForm.endDate) {
        this.$message.warning('请填写完整信息')
        return
      }

      if (this.editingTerm) {
        // 编辑
        const index = this.terms.findIndex(t => t.id === this.editingTerm.id)
        if (index > -1) {
          this.terms.splice(index, 1, { ...this.editingTerm, ...this.termForm })
        }
        this.$message.success('班期更新成功')
      } else {
        // 新增
        const newTerm = {
          id: Date.now(),
          ...this.termForm,
          status: 'upcoming'
        }
        this.terms.unshift(newTerm)
        this.$message.success('班期创建成功')
      }

      this.showTermDialog = false
      this.editingTerm = null
      this.termForm = { name: '', startDate: '', endDate: '' }
    },

    // 班级方法
    showAddClassDialog(term) {
      this.currentTermId = term.id
      this.showClassDialog = true
    },
    getTermClasses(termId) {
      return this.classes.filter(c => c.termId === termId)
    },
    generateInviteCode() {
      const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
      let code = ''
      for (let i = 0; i < 6; i++) {
        code += chars.charAt(Math.floor(Math.random() * chars.length))
      }
      this.classForm.inviteCode = code
    },
    submitClass() {
      if (!this.classForm.name || !this.classForm.inviteCode) {
        this.$message.warning('请填写完整信息')
        return
      }

      const newClass = {
        id: Date.now(),
        termId: this.currentTermId,
        ...this.classForm,
        studentCount: 0
      }
      this.classes.push(newClass)
      this.$message.success('班级创建成功')

      this.showClassDialog = false
      this.classForm = { name: '', capacity: 50, inviteCode: '' }
    },
    manageStudents(classItem) {
      this.$message.info(`打开班级"${classItem.name}"的成员管理页面`)
      // TODO: 跳转到学生名单页面
    },
    deleteClass(classItem) {
      this.$confirm(`确定要删除班级"${classItem.name}"吗？`, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        const index = this.classes.findIndex(c => c.id === classItem.id)
        if (index > -1) {
          this.classes.splice(index, 1)
          this.$message.success('删除成功')
        }
      }).catch(() => {})
    },

    // 课程设置方法
    saveCourseSettings() {
      this.$message.success('课程设置已保存')
      // TODO: 调用API保存设置
    },

    // 订单方法
    viewOrderDetail(order) {
      this.$message.info(`查看订单详情：${order.orderNo}`)
      // TODO: 打开订单详情弹窗或页面
    },

    // 状态文本和类型
    getTermStatusText(status) {
      const map = {
        active: '进行中',
        upcoming: '未开始',
        ended: '已结束'
      }
      return map[status] || status
    },
    getTermStatusType(status) {
      const map = {
        active: 'success',
        upcoming: 'info',
        ended: 'info'
      }
      return map[status] || 'info'
    },
    getOrderStatusText(status) {
      const map = {
        paid: '已支付',
        pending: '待支付',
        refunded: '已退款'
      }
      return map[status] || status
    },
    getOrderStatusType(status) {
      const map = {
        paid: 'success',
        pending: 'warning',
        refunded: 'info'
      }
      return map[status] || 'info'
    }
  }
}
</script>

<style scoped lang="scss">
.management-center {
  min-height: 100vh;
  background-color: #F5F5F5;
  padding: 20px;

  .header-bar {
    display: flex;
    align-items: center;
    margin-bottom: 20px;
    position: relative;

    .back-btn {
      position: absolute;
      left: 0;
    }

    .title {
      flex: 1;
      text-align: center;
      font-size: 20px;
      font-weight: 600;
      color: #303133;
      margin: 0;
    }
  }

  .main-container {
    max-width: 1200px;
    min-width: 1100px;
    margin: 0 auto;
    background: #FFFFFF;
    border-radius: 8px;
    padding: 20px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);

    .management-tabs {
      ::v-deep .el-tabs__header {
        margin: 0 0 20px;
      }

      ::v-deep .el-tabs__nav-wrap {
        padding: 0 20px;
      }

      ::v-deep .el-tabs__item {
        font-size: 15px;
        font-weight: 500;
        height: 50px;
        line-height: 50px;
      }
    }

    .tab-content {
      padding: 0 20px 20px;
    }
  }

  // 教务组织样式
  .operation-bar {
    margin-bottom: 20px;
  }

  .term-list {
    display: flex;
    flex-direction: column;
    gap: 20px;

    .term-card {
      border: 1px solid #E4E7ED;
      border-radius: 8px;
      padding: 20px;
      background: #FAFAFA;

      .term-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 16px;
        padding-bottom: 16px;
        border-bottom: 1px solid #E4E7ED;

        .term-info {
          .term-name {
            font-size: 18px;
            font-weight: 600;
            color: #303133;
            margin: 0 0 8px 0;
          }

          .term-meta {
            display: flex;
            align-items: center;
            gap: 12px;

            .term-date {
              color: #606266;
              font-size: 14px;
            }
          }
        }

        .term-actions {
          display: flex;
          gap: 10px;
        }
      }

      .class-list {
        background: #FFFFFF;
        border-radius: 6px;
        padding: 12px;
      }

      .no-classes {
        text-align: center;
        padding: 30px;
        color: #909399;
        font-size: 14px;
        background: #FFFFFF;
        border-radius: 6px;
      }
    }
  }

  .empty-state {
    text-align: center;
    padding: 80px 20px;

    .empty-icon {
      font-size: 64px;
      color: #DCDFE6;
      margin-bottom: 16px;
    }

    p {
      color: #909399;
      font-size: 14px;
      margin: 8px 0;

      &.hint {
        font-size: 13px;
        color: #C0C4CC;
      }
    }
  }

  // 课程设置样式
  .setting-card {
    margin-bottom: 20px;

    .card-title {
      font-size: 16px;
      font-weight: 600;
      color: #303133;
    }

    .setting-form {
      .price-inputs {
        display: flex;
        align-items: center;
      }

      .form-tip {
        margin-left: 16px;
        color: #909399;
        font-size: 13px;
      }
    }
  }

  .save-bar {
    text-align: center;
    padding-top: 20px;
  }

  // 财务订单样式
  .finance-overview {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
    margin-bottom: 20px;

    .overview-card {
      .overview-item {
        text-align: center;
        padding: 20px;

        .overview-label {
          font-size: 14px;
          color: #909399;
          margin-bottom: 12px;
        }

        .overview-value {
          font-size: 28px;
          font-weight: 600;
          color: #303133;
        }
      }
    }
  }

  .order-card {
    .card-title {
      font-size: 16px;
      font-weight: 600;
      color: #303133;
    }

    .amount-text {
      color: #F56C6C;
      font-weight: 600;
    }
  }
}

::v-deep .el-table {
  .el-table__header th {
    background-color: #FAFAFA;
    color: #606266;
    font-weight: 600;
  }
}
</style>
