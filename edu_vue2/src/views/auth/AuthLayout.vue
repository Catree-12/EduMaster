<template>
  <div class="auth-layout">
    <div class="auth-wrapper">
      <div class="auth-left">
        <div class="auth-brand">
          <h1>🎓 EduHub</h1>
          <p>在线教育学习平台</p>
          <div class="features">
            <div class="feature-item">
              <span class="feature-icon">📚</span>
              <span>海量优质课程</span>
            </div>
            <div class="feature-item">
              <span class="feature-icon">👨‍🏫</span>
              <span>名师一对一教学</span>
            </div>
            <div class="feature-item">
              <span class="feature-icon">🏆</span>
              <span>获得权威认证</span>
            </div>
            <div class="feature-item">
              <span class="feature-icon">💼</span>
              <span>职业发展加速</span>
            </div>
          </div>
        </div>
      </div>
      <div class="auth-right">
        <div class="auth-card">
          <router-view></router-view>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AuthLayout'
}
</script>

<style scoped>
.auth-layout {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.auth-wrapper {
  display: grid;
  grid-template-columns: 1fr 1fr;
  width: 90%;
  max-width: 1000px;
  gap: 50px;
  align-items: center;
}

.auth-left {
  color: white;
}

.auth-brand h1 {
  font-size: 48px;
  margin: 0 0 10px;
  font-weight: 700;
}

.auth-brand p {
  font-size: 18px;
  margin: 0 0 40px;
  opacity: 0.9;
}

.features {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 15px;
  font-size: 16px;
}

.feature-icon {
  font-size: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 50px;
  height: 50px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
}

.auth-right {
  display: flex;
  justify-content: center;
}

.auth-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
  padding: 50px 40px;
  width: 100%;
  max-width: 400px;
}

@media (max-width: 768px) {
  .auth-wrapper {
    grid-template-columns: 1fr;
    width: 95%;
    gap: 30px;
  }

  .auth-left {
    display: none;
  }

  .auth-card {
    padding: 40px 30px;
    max-width: 100%;
  }
}
</style>
