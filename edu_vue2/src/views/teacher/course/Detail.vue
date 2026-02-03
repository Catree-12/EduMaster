<template>
  <div class="teacher-course-detail">
    <!-- 左侧固定导航栏 -->
    <aside class="sidebar-fixed">
      <!-- 课程名称 -->
      <div class="sidebar-logo">
        <h1>{{ courseInfo.name }}</h1>
      </div>
      
      <!-- 导航菜单 -->
      <nav class="nav-menu">
        <div
          v-for="item in navItems"
          :key="item.id"
          :class="['nav-item', { active: activeModule === item.id }]"
          @click="selectModule(item.id)"
          tabindex="0"
          role="button"
        >
          <span class="nav-icon">{{ item.icon }}</span>
          <span class="nav-label">{{ item.label }}</span>
        </div>
      </nav>
    </aside>

    <!-- 右侧内容区 -->
    <div class="main-wrapper">
      <main class="content-area">
        <!-- 章节模块 -->
        <section v-if="activeModule === 'sections'" class="module-section">
          <div class="sections-overview">
            <div class="overview-header">
              <h2>课程章节</h2>
              <div class="header-actions">
                <el-input
                  v-model="chapterSearch"
                  placeholder="搜索章节或课程..."
                  prefix-icon="el-icon-search"
                  clearable
                  style="width: 300px; margin-right: 1rem;"
                />
                <el-button type="primary" icon="el-icon-edit" @click="goToChapterEditor">
                  编辑章节
                </el-button>
              </div>
            </div>

            <div class="sections-list">
              <div
                v-for="section in filteredSections"
                :key="section.id"
                class="section-card"
              >
                <div class="section-card-header" @click="toggleSection(section.id)">
                  <div class="section-info">
                    <span :class="['expand-icon', { expanded: expandedSections.includes(section.id) }]">▶</span>
                    <h3>{{ section.title }}</h3>
                  </div>
                  <div class="section-meta">
                    <span class="lesson-count">{{ section.lessons.length }} 课时</span>
                  </div>
                </div>

                <div
                  v-show="expandedSections.includes(section.id)"
                  class="section-lessons"
                >
                  <div
                    v-for="(lesson, index) in section.lessons"
                    :key="lesson.id"
                    class="lesson-card"
                  >
                    <div class="lesson-index">{{ index + 1 }}</div>
                    <div class="lesson-icon">
                      {{ lesson.type === 'video' ? '🎥' : '📄' }}
                    </div>
                    <div class="lesson-content" @click="selectLesson(lesson, section)">
                      <div class="lesson-name">{{ lesson.name }}</div>
                      <div class="lesson-meta">
                        <span>{{ lesson.duration }}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div v-if="filteredSections.length === 0 && sections.length > 0" class="no-data">
              <i class="el-icon-folder-opened" style="font-size: 48px; color: #dcdfe6;"></i>
              <p>未找到相关章节</p>
            </div>
            
            <div v-if="sections.length === 0" class="no-data">
              <i class="el-icon-folder-add" style="font-size: 48px; color: #dcdfe6;"></i>
              <p>暂无章节数据，点击"编辑章节"开始创建</p>
            </div>
          </div>
        </section>

        <!-- 作业模块 -->
        <section v-if="activeModule === 'homework'" class="module-section">
          <div class="module-header">
            <h2>作业管理</h2>
            <div class="action-buttons">
              <button @click="goToCreateHomework" class="action-btn primary-btn">
                ➕ 新建作业
              </button>
              <button @click="goToHomeworkLibrary" class="action-btn secondary-btn">
                📚 作业库
              </button>
            </div>
          </div>

          <!-- 筛选区 -->
          <div class="filter-section">
            <div class="filter-group">
              <label>班期筛选：</label>
              <select v-model="homeworkFilter.termId" class="filter-select" @change="homeworkFilter.class = ''">
                <option value="">全部班期</option>
                <option v-for="term in terms" :key="term.id" :value="term.id">{{ term.name }}</option>
              </select>
            </div>

            <div class="filter-group">
              <label>班级筛选：</label>
              <select v-model="homeworkFilter.class" class="filter-select">
                <option value="">全部班级</option>
                <option 
                  v-for="cls in (homeworkFilter.termId ? getClassesByTerm(homeworkFilter.termId) : classes)" 
                  :key="cls.id" 
                  :value="cls.name"
                >
                  {{ cls.name }}
                </option>
              </select>
            </div>

            <div class="filter-group">
              <label>状态筛选：</label>
              <div class="status-filter-btns">
                <button
                  v-for="status in statusOptions"
                  :key="status"
                  :class="['filter-btn', { active: homeworkFilter.status === status }]"
                  @click="homeworkFilter.status = status"
                >
                  {{ status }}
                </button>
              </div>
            </div>
          </div>

          <!-- 列表区 -->
          <div v-if="filteredHomeworks.length > 0" class="list-section">
            <div v-for="hw in filteredHomeworks" :key="hw.id" class="homework-item-card">
              <!-- 顶部区域 -->
              <div class="card-top-section">
                <!-- 左侧：标题和状态 -->
                <div class="card-header">
                  <h3 class="task-title clickable-title" @click="viewHomeworkDetail(hw)">{{ hw.name }}</h3>
                  <span :class="['status-capsule', hw.status]">{{ hw.status }}</span>
                </div>
                
                <!-- 右侧：统计数字（横向排列） -->
                <div class="stats-inline">
                  <div class="stat-item stat-pending">
                    <div class="stat-number">{{ hw.pendingCount }}</div>
                    <div class="stat-label">待批</div>
                  </div>
                  <div class="stat-item stat-submitted">
                    <div class="stat-number">{{ hw.submittedCount }}</div>
                    <div class="stat-label">已交</div>
                  </div>
                  <div class="stat-item stat-unsubmitted">
                    <div class="stat-number">{{ hw.unsubmittedCount }}</div>
                    <div class="stat-label">未交</div>
                  </div>
                </div>
              </div>

              <!-- 中部区域：信息行 -->
              <div class="card-middle-section">
                <div class="info-item">
                  <span class="info-label">班期：</span>
                  <span class="info-value">{{ hw.termName || '未设置' }}</span>
                </div>
                <div class="info-item">
                  <span class="info-label">班级：</span>
                  <span class="info-value">{{ hw.className }}</span>
                </div>
                <div class="info-item">
                  <span class="info-label">作答时间：</span>
                  <span class="info-value">{{ hw.startTime }} ~ {{ hw.endTime }}</span>
                </div>
              </div>

              <!-- 底部区域：操作按钮 -->
              <div class="card-bottom-section">
                <el-button 
                  type="primary" 
                  size="large" 
                  class="primary-action-btn"
                  @click.stop="gradeHomework(hw)"
                >
                  批阅 ({{ hw.pendingCount }})
                </el-button>
                <div class="auxiliary-links">
                  <a class="link-edit" @click.stop="editHomework(hw)">修改设置</a>
                  <a class="link-delete" @click.stop="deleteHomework(hw.id)">删除</a>
                </div>
              </div>
            </div>
          </div>

          <div v-else class="no-data">
            <p>暂无作业数据</p>
          </div>
        </section>

        <!-- 考试模块 -->
        <section v-if="activeModule === 'exam'" class="module-section">
          <div class="module-header">
            <h2>考试管理</h2>
            <div class="action-buttons">
              <button @click="goToCreateExam" class="action-btn primary-btn">
                ➕ 新建考试
              </button>
              <button @click="goToExamLibrary" class="action-btn secondary-btn">
                📚 试卷库
              </button>
              <button @click="goToExamManage" class="action-btn secondary-btn">
                👁️ 监考
              </button>
            </div>
          </div>

          <!-- 筛选区 -->
          <div class="filter-section">
            <div class="filter-group">
              <label>班期筛选：</label>
              <select v-model="examFilter.termId" class="filter-select" @change="examFilter.class = ''">
                <option value="">全部班期</option>
                <option v-for="term in terms" :key="term.id" :value="term.id">{{ term.name }}</option>
              </select>
            </div>

            <div class="filter-group">
              <label>班级筛选：</label>
              <select v-model="examFilter.class" class="filter-select">
                <option value="">全部班级</option>
                <option 
                  v-for="cls in (examFilter.termId ? getClassesByTerm(examFilter.termId) : classes)" 
                  :key="cls.id" 
                  :value="cls.name"
                >
                  {{ cls.name }}
                </option>
              </select>
            </div>

            <div class="filter-group">
              <label>状态筛选：</label>
              <div class="status-filter-btns">
                <button
                  v-for="status in statusOptions"
                  :key="status"
                  :class="['filter-btn', { active: examFilter.status === status }]"
                  @click="examFilter.status = status"
                >
                  {{ status }}
                </button>
              </div>
            </div>
          </div>

          <!-- 列表区 -->
          <div v-if="filteredExams.length > 0" class="list-section">
            <div v-for="exam in filteredExams" :key="exam.id" class="exam-item-card">
              <!-- 顶部区域：标题 + 状态 + 统计 -->
              <div class="card-top-section">
                <div class="card-header">
                  <h3 class="task-title clickable-title" @click="viewExamDetail(exam)">{{ exam.name }}</h3>
                  <span :class="['status-capsule', exam.status]">{{ exam.status }}</span>
                </div>
                
                <!-- 右侧：统计数字（横向排列） -->
                <div class="stats-inline">
                  <div class="stat-item stat-pending">
                    <div class="stat-number">{{ exam.pendingCount }}</div>
                    <div class="stat-label">待批</div>
                  </div>
                  <div class="stat-item stat-submitted">
                    <div class="stat-number">{{ exam.completedCount }}</div>
                    <div class="stat-label">已交</div>
                  </div>
                  <div class="stat-item stat-unsubmitted">
                    <div class="stat-number">{{ exam.incompleteCount }}</div>
                    <div class="stat-label">未交</div>
                  </div>
                </div>
              </div>

              <!-- 中部区域：信息行 -->
              <div class="card-middle-section">
                <div class="info-item">
                  <span class="info-label">班期：</span>
                  <span class="info-value">{{ exam.termName || '未设置' }}</span>
                </div>
                <div class="info-item">
                  <span class="info-label">班级：</span>
                  <span class="info-value">{{ exam.className || '未设置' }}</span>
                </div>
                <div class="info-item">
                  <span class="info-label">考试时间：</span>
                  <span class="info-value">{{ exam.startTime }} ~ {{ exam.endTime }}</span>
                </div>
              </div>

              <!-- 底部区域：操作按钮 -->
              <div class="card-bottom-section">
                <el-button 
                  type="primary" 
                  size="large" 
                  class="primary-action-btn"
                  @click.stop="gradeExam(exam)"
                >
                  批阅 ({{ exam.pendingCount }})
                </el-button>
                <div class="auxiliary-links">
                  <a class="link-edit" @click.stop="editExam(exam)">修改设置</a>
                  <a class="link-delete" @click.stop="deleteExam(exam.id)">删除</a>
                </div>
              </div>
            </div>
          </div>

          <div v-else class="no-data">
            <p>暂无考试数据</p>
          </div>
        </section>

        <!-- 讨论区模块 -->
        <section v-if="activeModule === 'discussion'" class="module-section community-module">
          <div class="community-layout">
            <!-- 左侧：话题列表区域 -->
            <div class="community-main">
              <!-- 1. 顶部操作区 -->
              <div class="community-top-bar">
            <input 
              v-model="communitySearch"
              type="text"
              placeholder="搜索话题标题或内容..."
              class="community-search-input"
            >
            <button @click="createNewThread" class="community-publish-btn">
              ➕ 发布话题
            </button>
          </div>

          <!-- 2. 筛选与排序条 -->
          <div class="community-filter-bar">
            <div class="sort-tabs">
              <button
                v-for="sort in ['最新', '热门']"
                :key="sort"
                :class="['sort-tab', { active: communitySortBy === sort }]"
                @click="communitySortBy = sort"
              >
                {{ sort }}
              </button>
            </div>
          </div>

          <!-- 3. 话题列表容器 -->
          <div v-if="filteredCommunityThreads.length > 0" class="community-thread-list">
            <div v-for="thread in filteredCommunityThreads" :key="thread.id" class="thread-card">
              <!-- 标题层 -->
              <div class="thread-title-row">
                <h3 class="thread-title" @click="viewThreadDetail(thread.id)">{{ thread.title }}</h3>
                <div class="thread-badges">
                  <span v-if="thread.authorRole === 'teacher'" class="badge-role teacher">老师</span>
                  <span v-if="thread.essence" class="badge-tag essence">精选</span>
                </div>
              </div>

              <!-- 摘要层 -->
              <div class="thread-preview">
                <p class="thread-excerpt">{{ getThreadExcerpt(thread.content) }}</p>
              </div>

              <!-- 元数据层 -->
              <div class="thread-meta-row">
                <div class="thread-info">
                  <span class="author-name">{{ thread.author }}</span>
                  <span class="separator">·</span>
                  <span class="publish-time">{{ thread.createTime }}</span>
                </div>
                <div class="thread-stats">
                  <span class="stat-item">
                    <i class="icon-view">👁</i>
                    {{ thread.viewCount }}
                  </span>
                  <span class="stat-item clickable" @click.stop="viewThreadDetail(thread.id)">
                    <i class="icon-reply">💬</i>
                    {{ thread.replyCount }}
                  </span>
                  <button :class="['like-btn-list', { liked: thread.isLiked }]" @click.stop="toggleThreadLikeInList(thread)">
                    {{ thread.isLiked ? '❤️' : '🤍' }}
                    {{ thread.likeCount }}
                  </button>
                  <!-- 管理操作 -->
                  <div v-if="canEditThread(thread) || canDeleteThread(thread)" class="thread-manage">
                    <a v-if="canEditThread(thread)" class="manage-link edit" @click.stop="editThread(thread.id)">编辑</a>
                    <a v-if="canDeleteThread(thread)" class="manage-link delete" @click.stop="deleteThread(thread.id)">删除</a>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div v-else class="no-data">
            <p>暂无话题</p>
            <p class="hint">点击"发布话题"按钮创建第一个讨论</p>
          </div>
            </div>

            <!-- 右侧：分类目录 -->
            <aside class="community-sidebar">
              <div class="sidebar-section">
                <h3 class="sidebar-title">我的（讨论）</h3>
                <div class="category-list">
                  <div 
                    v-for="category in myCategories" 
                    :key="category.id"
                    :class="['category-item', { active: communityCategory === category.id }]"
                    @click="selectCommunityCategory(category.id)"
                  >
                    <span class="category-icon">{{ category.icon }}</span>
                    <span class="category-label">{{ category.label }}</span>
                  </div>
                </div>
              </div>
            </aside>
          </div>
        </section>

        <!-- 分析模块 -->
        <section v-if="activeModule === 'grades'" class="module-section analytics-module">
          <div class="analytics-container">
            <!-- 顶部页签 -->
            <el-tabs v-model="analyticsActiveTab" class="analytics-tabs">
              <!-- 页签一：成绩分析 -->
              <el-tab-pane label="成绩分析" name="scores">
                <div class="analytics-content">
                  <!-- 顶部筛选 -->
                  <div class="analytics-filters">
                    <el-select v-model="scoreAnalysis.selectedTerm" placeholder="选择班期" @change="onTermChange" style="width: 180px;">
                      <el-option label="全部班期" value=""></el-option>
                      <el-option 
                        v-for="term in terms" 
                        :key="term.id" 
                        :label="term.name" 
                        :value="term.id"
                      ></el-option>
                    </el-select>
                    
                    <el-select v-model="scoreAnalysis.selectedClass" placeholder="选择班级" :disabled="!scoreAnalysis.selectedTerm" style="width: 180px;">
                      <el-option label="全部班级" value=""></el-option>
                      <el-option 
                        v-for="cls in getClassesByTerm(scoreAnalysis.selectedTerm)" 
                        :key="cls.id" 
                        :label="cls.name" 
                        :value="cls.id"
                      ></el-option>
                    </el-select>
                    
                    <el-select v-model="scoreAnalysis.selectedExam" placeholder="选择测验" style="width: 200px;">
                      <el-option label="全部测验" value=""></el-option>
                      <el-option label="期中考试" value="midterm"></el-option>
                      <el-option label="期末考试" value="final"></el-option>
                      <el-option label="单元测验1" value="unit1"></el-option>
                      <el-option label="单元测验2" value="unit2"></el-option>
                    </el-select>
                  </div>

                  <!-- 概览卡片 -->
                  <div class="summary-cards">
                    <div class="summary-card">
                      <div class="card-icon" style="background: #dbeafe;">
                        <i class="el-icon-data-line" style="color: #3b82f6;"></i>
                      </div>
                      <div class="card-info">
                        <div class="card-label">平均分</div>
                        <div class="card-value">{{ scoreAnalysis.avgScore }}</div>
                      </div>
                    </div>
                    
                    <div class="summary-card">
                      <div class="card-icon" style="background: #d1fae5;">
                        <i class="el-icon-circle-check" style="color: #10b981;"></i>
                      </div>
                      <div class="card-info">
                        <div class="card-label">及格率</div>
                        <div class="card-value">{{ scoreAnalysis.passRate }}%</div>
                      </div>
                    </div>
                    
                    <div class="summary-card">
                      <div class="card-icon" style="background: #fef3c7;">
                        <i class="el-icon-top" style="color: #f59e0b;"></i>
                      </div>
                      <div class="card-info">
                        <div class="card-label">最高分</div>
                        <div class="card-value">{{ scoreAnalysis.maxScore }}</div>
                      </div>
                    </div>
                    
                    <div class="summary-card">
                      <div class="card-icon" style="background: #fce7f3;">
                        <i class="el-icon-warning" style="color: #ec4899;"></i>
                      </div>
                      <div class="card-info">
                        <div class="card-label">偏离度</div>
                        <div class="card-value">{{ scoreAnalysis.deviation }}</div>
                      </div>
                    </div>
                  </div>

                  <!-- 可视化图表 -->
                  <div class="chart-card">
                    <h3 class="chart-title">分数段分布</h3>
                    <div class="score-distribution">
                      <div v-for="range in scoreAnalysis.scoreRanges" :key="range.label" class="score-bar-item">
                        <div class="range-label">{{ range.label }}</div>
                        <div class="bar-container">
                          <div class="bar-fill" :style="{ width: range.percentage + '%', background: range.color }"></div>
                        </div>
                        <div class="range-count">{{ range.count }}人 ({{ range.percentage }}%)</div>
                      </div>
                    </div>
                  </div>

                  <!-- 明细表格 -->
                  <div class="detail-table-card">
                    <h3 class="table-title">学生成绩明细</h3>
                    <table class="analytics-table">
                      <thead>
                        <tr>
                          <th>排名</th>
                          <th>姓名</th>
                          <th>学号</th>
                          <th>客观题</th>
                          <th>主观题(AI评分)</th>
                          <th>总分</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr v-for="(student, index) in scoreAnalysis.students" :key="student.id">
                          <td>
                            <span :class="['rank-badge', getRankClass(index)]">
                              {{ index + 1 }}
                            </span>
                          </td>
                          <td>{{ student.name }}</td>
                          <td>{{ student.studentNo }}</td>
                          <td>{{ student.objectiveScore }}</td>
                          <td>{{ student.subjectiveScore }}</td>
                          <td class="total-score">{{ student.totalScore }}</td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>
              </el-tab-pane>

              <!-- 页签二：学习进度 -->
              <el-tab-pane label="学习进度" name="progress">
                <div class="analytics-content">
                  <!-- 视频观看看板 -->
                  <div class="progress-card">
                    <h3 class="card-title">视频观看进度</h3>
                    <div class="progress-list">
                      <div v-for="student in learningProgress.videoProgress" :key="student.id" class="progress-item">
                        <div class="student-info">
                          <span :class="['student-name', { 'low-progress': student.progress < 20 }]">
                            {{ student.name }}
                          </span>
                          <span class="progress-percent">{{ student.progress }}%</span>
                        </div>
                        <div class="progress-bar">
                          <div 
                            class="progress-fill" 
                            :style="{ 
                              width: student.progress + '%',
                              background: student.progress < 20 ? '#ef4444' : student.progress < 60 ? '#f59e0b' : '#10b981'
                            }"
                          ></div>
                        </div>
                      </div>
                    </div>
                  </div>

                  <!-- 任务参与率 -->
                  <div class="participation-card">
                    <h3 class="card-title">任务参与率</h3>
                    <div class="participation-chart">
                      <div v-for="task in learningProgress.taskParticipation" :key="task.name" class="task-bar">
                        <div class="task-name">{{ task.name }}</div>
                        <div class="bar-group">
                          <div class="bar-segment submitted" :style="{ width: task.submittedRate + '%' }">
                            <span v-if="task.submittedRate > 10">{{ task.submitted }}人</span>
                          </div>
                          <div class="bar-segment unsubmitted" :style="{ width: task.unsubmittedRate + '%' }">
                            <span v-if="task.unsubmittedRate > 10">{{ task.unsubmitted }}人</span>
                          </div>
                        </div>
                        <div class="task-stats">{{ task.submittedRate }}%</div>
                      </div>
                    </div>
                  </div>

                  <!-- 资源热力图 -->
                  <div class="heatmap-card">
                    <h3 class="card-title">课件热度排行</h3>
                    <div class="heatmap-list">
                      <div v-for="resource in learningProgress.resourceHeatmap" :key="resource.id" class="heatmap-item">
                        <div class="resource-name">{{ resource.name }}</div>
                        <div class="heat-bar">
                          <div class="heat-fill" :style="{ width: resource.heatPercent + '%' }"></div>
                        </div>
                        <div class="resource-stats">
                          <span><i class="el-icon-view"></i> {{ resource.views }}</span>
                          <span><i class="el-icon-download"></i> {{ resource.downloads }}</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </el-tab-pane>

              <!-- 页签三：智慧诊断 -->
              <el-tab-pane label="智慧诊断" name="diagnosis">
                <div class="analytics-content">
                  <!-- 知识点掌握雷达图 -->
                  <div class="radar-card">
                    <h3 class="card-title">知识点掌握情况</h3>
                    <div class="radar-placeholder">
                      <i class="el-icon-data-analysis" style="font-size: 3rem; color: #d1d5db;"></i>
                      <p>雷达图将在这里显示各知识点掌握率</p>
                      <p class="hint">需要集成 ECharts 或其他图表库</p>
                    </div>
                  </div>

                  <!-- 掌握度预警 -->
                  <div class="alert-card">
                    <h3 class="card-title">掌握度预警</h3>
                    <div class="alert-list">
                      <div v-for="alert in smartDiagnosis.alerts" :key="alert.id" :class="['alert-item', alert.level]">
                        <div class="alert-icon">
                          <i :class="alert.icon"></i>
                        </div>
                        <div class="alert-content">
                          <div class="alert-label">{{ alert.label }}</div>
                          <div class="alert-desc">{{ alert.description }}</div>
                          <div class="affected-students">
                            <span v-for="student in alert.students" :key="student" class="student-tag">
                              {{ student }}
                            </span>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>

                  <!-- 推送策略配置 -->
                  <div class="strategy-card">
                    <div class="strategy-header">
                      <h3 class="card-title">推送策略配置</h3>
                      <button @click="showStrategyModal = true" class="config-btn">
                        <i class="el-icon-setting"></i> 配置
                      </button>
                    </div>
                    <div class="strategy-status">
                      <div class="status-item">
                        <span class="status-label">自动推送：</span>
                        <el-switch v-model="smartDiagnosis.autoSend"></el-switch>
                      </div>
                      <div class="status-item">
                        <span class="status-label">判定阈值：</span>
                        <span class="status-value">{{ smartDiagnosis.threshold }}分</span>
                      </div>
                    </div>
                  </div>
                </div>
              </el-tab-pane>
            </el-tabs>
          </div>
        </section>

        <!-- 题库模块 -->
        <section v-if="activeModule === 'questionBank'" class="module-section question-bank-module">
          <!-- 顶部操作与筛选栏 -->
          <div class="question-bank-header">
            <div class="left-actions">
              <button @click="showQuestionModal = true" class="action-btn primary-btn">
                ➕ 创建题目
              </button>
              <button @click="importQuestions" class="action-btn secondary-btn">
                📥 批量导入
              </button>
              <label class="detail-toggle">
                <input type="checkbox" v-model="showQuestionDetail" class="toggle-checkbox">
                <span>显示题目详情</span>
              </label>
            </div>

            <div class="right-filters">
              <select v-model="questionFilter.type" class="compact-select">
                <option value="">全部题型</option>
                <option value="single">单选题</option>
                <option value="multiple">多选题</option>
                <option value="fill">填空题</option>
                <option value="judge">判断题</option>
                <option value="essay">简答题</option>
              </select>

              <select v-model="questionFilter.difficultyValue" class="compact-select">
                <option value="">全部难度</option>
                <option value="0.1">极易 (0.1)</option>
                <option value="0.2">很易 (0.2)</option>
                <option value="0.3">易 (0.3)</option>
                <option value="0.4">较易 (0.4)</option>
                <option value="0.5">中 (0.5)</option>
                <option value="0.6">较难 (0.6)</option>
                <option value="0.7">难 (0.7)</option>
                <option value="0.8">很难 (0.8)</option>
                <option value="0.9">极难 (0.9)</option>
                <option value="1.0">最难 (1.0)</option>
              </select>

              <el-select 
                v-model="questionFilter.knowledgePoints" 
                multiple 
                collapse-tags
                placeholder="全部知识点" 
                class="compact-select-multi"
                style="width: 180px;"
              >
                <el-option label="JavaScript基础" value="JavaScript基础"></el-option>
                <el-option label="原型链" value="原型链"></el-option>
                <el-option label="异步编程" value="异步编程"></el-option>
                <el-option label="闭包" value="闭包"></el-option>
              </el-select>

              <el-select 
                v-model="questionFilter.tags" 
                multiple 
                collapse-tags
                placeholder="全部标签" 
                class="compact-select-multi"
                style="width: 180px;"
              >
                <el-option label="重点" value="重点"></el-option>
                <el-option label="易错" value="易错"></el-option>
                <el-option label="常考" value="常考"></el-option>
                <el-option label="综合" value="综合"></el-option>
              </el-select>

              <select v-model="questionFilter.sortBy" class="compact-select" style="width: 150px;">
                <option value="">默认排序</option>
                <option value="time-desc">最新创建</option>
                <option value="time-asc">最早创建</option>
              </select>
            </div>
          </div>

          <!-- 主体布局：左目录 + 右列表 -->
          <div class="question-bank-body">
            <!-- 左侧目录树 -->
            <div class="folder-sidebar">
              <div class="sidebar-search">
                <input 
                  v-model="folderSearch"
                  type="text"
                  placeholder="搜索文件夹..."
                  class="folder-search-input"
                >
              </div>

              <div class="folder-tree">
                <!-- 根目录（未分类题目） -->
                <div 
                  :class="['folder-item', { active: selectedFolderId === null }]"
                  @click="selectFolder(null)"
                >
                  <span class="folder-icon">📂</span>
                  <span class="folder-name">根目录</span>
                  <span class="folder-count">({{ rootQuestionCount }})</span>
                </div>
                
                <!-- 文件夹列表 -->
                <draggable 
                  v-model="questionFolders" 
                  @end="onFolderDragEnd"
                  handle=".drag-handle"
                  animation="200"
                  class="folder-draggable-area"
                >
                  <div 
                    v-for="folder in filteredFolders" 
                    :key="folder.id"
                    :class="['folder-item', { active: selectedFolderId === folder.id, pinned: folder.pinned }]"
                    @click="selectFolder(folder.id)"
                  >
                    <span class="drag-handle" title="拖拽调整顺序">☰</span>
                    <span class="folder-icon">{{ folder.pinned ? '📌' : '📁' }}</span>
                    <span class="folder-name">{{ folder.name }}</span>
                    <span class="folder-count">({{ folder.questionCount }})</span>
                    <div class="folder-menu" @click.stop>
                      <button class="menu-trigger" @click="toggleFolderMenu(folder.id)">⋮</button>
                      <div v-if="activeFolderMenu === folder.id" class="menu-dropdown">
                        <button @click="pinFolder(folder)" class="menu-item">
                          {{ folder.pinned ? '取消置顶' : '置顶' }}
                        </button>
                        <button @click="renameFolder(folder)" class="menu-item">重命名</button>
                        <button @click="deleteFolder(folder.id)" class="menu-item danger">删除</button>
                        <button @click="copyFolder(folder)" class="menu-item">复制</button>
                      </div>
                    </div>
                  </div>
                </draggable>
              </div>

              <button @click="showFolderModal = true" class="new-folder-btn">
                ➕ 新建文件夹
              </button>
            </div>

            <!-- 右侧题目卡片列表 -->
            <div class="question-list-area">
              <div v-if="filteredQuestions.length > 0" class="question-cards">
                <div 
                  v-for="question in filteredQuestions" 
                  :key="question.id" 
                  class="question-preview-card"
                >
                    <!-- 卡片顶部：元数据行 -->
                    <div class="card-meta-row">
                      <span :class="['type-tag', question.type]">
                        {{ getQuestionTypeLabel(question.type) }}
                      </span>
                      <span class="difficulty-value">
                        难度: {{ question.difficultyValue }} ({{ getDifficultyText(question.difficultyValue) }})
                      </span>
                      <span v-if="question.knowledgePoint" class="knowledge-tag">
                        {{ question.knowledgePoint }}
                      </span>
                      <span v-for="tag in question.tags" :key="tag" class="tag-badge">
                        {{ tag }}
                      </span>
                    </div>

                    <!-- 卡片中部：题干预览（可点击标题） -->
                    <div class="card-content-preview">
                      <h4 class="question-title-clickable" @click="viewQuestionDetail(question)">
                        {{ showQuestionDetail ? question.content : getQuestionPreview(question.content) }}
                      </h4>
                      
                      <!-- 显示详情时展示选项和答案 -->
                      <div v-if="showQuestionDetail" class="detail-section">
                        <!-- 单选题/多选题选项 -->
                        <div v-if="question.type === 'single' || question.type === 'multiple'" class="options-preview">
                          <div v-for="(opt, idx) in question.options" :key="idx" class="option-item">
                            <span :class="{ 'correct-answer': isCorrectOption(question, idx) }">
                              {{ String.fromCharCode(65 + idx) }}. {{ opt }}
                              <span v-if="isCorrectOption(question, idx)" class="answer-mark">✓</span>
                            </span>
                          </div>
                        </div>
                        
                        <!-- 判断题答案 -->
                        <div v-if="question.type === 'judge'" class="judge-answer">
                          <strong>答案：</strong>{{ question.answer ? '正确 ✓' : '错误 ✗' }}
                        </div>
                        
                        <!-- 填空题答案 -->
                        <div v-if="question.type === 'fill'" class="fill-answer">
                          <strong>参考答案：</strong>{{ question.answer }}
                        </div>
                        
                        <!-- 简答题答案 -->
                        <div v-if="question.type === 'essay'" class="essay-answer">
                          <strong>参考答案：</strong>
                          <p>{{ question.answer }}</p>
                        </div>
                      </div>
                    </div>

                    <!-- 卡片底部：统计与操作 -->
                    <div class="card-footer-row">
                      <div class="card-stats">
                        <span class="stat-item">创建人: {{ question.creator || '未知' }}</span>
                        <span class="stat-separator">·</span>
                        <span class="stat-item">使用: {{ question.usageCount }}次</span>
                        <span class="stat-separator">·</span>
                        <span class="stat-item">{{ question.createTime }}</span>
                      </div>
                      <div class="card-actions">
                        <div class="more-menu" @click.stop>
                          <button class="more-btn" @click="toggleQuestionMenu(question.id)">更多</button>
                          <div v-if="activeQuestionMenu === question.id" class="menu-dropdown">
                            <button @click="editQuestion(question)" class="menu-item">编辑</button>
                            <button @click="showMoveQuestionDialog(question)" class="menu-item">移动到</button>
                            <button @click="copyQuestion(question)" class="menu-item">复制</button>
                            <button @click="deleteQuestion(question.id)" class="menu-item danger">删除</button>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
              </div>

              <div v-else class="no-data">
                <i class="el-icon-document" style="font-size: 48px; color: #dcdfe6;"></i>
                <p>暂无题目数据</p>
                <p class="hint">点击"创建题目"按钮开始添加题目</p>
              </div>
            </div>
          </div>
        </section>

        <!-- 管理模块 -->
        <section v-if="activeModule === 'management'" class="module-section">
          <div class="management-container">
            <!-- 标签页导航 -->
            <el-tabs v-model="managementTab" class="management-tabs">
              <!-- 教务组织标签 -->
              <el-tab-pane label="教务组织" name="academic">
                <div class="tab-content academic-content">
                  <!-- 一级页面：班期概览 -->
                  <div v-if="!currentViewingTerm" class="term-overview">
                    <!-- 顶部操作栏 -->
                    <div class="operation-bar">
                      <button @click="showTermModal = true" class="action-btn primary-btn">
                        ➕ 新建班期
                      </button>
                    </div>

                    <!-- 班期卡片列表 -->
                    <div v-if="terms.length > 0" class="term-cards-container">
                      <div v-for="term in terms" :key="term.id" class="term-wide-card">
                        <div class="card-content" @click="enterTermManagement(term)">
                          <div class="card-left">
                            <h3 class="card-title">{{ term.name }}</h3>
                            <div class="card-meta">
                              <span class="meta-item">
                                <i class="el-icon-date"></i>
                                {{ term.startDate }} ~ {{ term.endDate }}
                              </span>
                              <span :class="['status-tag', term.status]">
                                {{ getTermStatusText(term.status) }}
                              </span>
                            </div>
                            <div v-if="term.description" class="card-description">
                              <i class="el-icon-document"></i>
                              {{ term.description }}
                            </div>
                          </div>
                          <div class="card-center">
                            <div class="stat-item">
                              <span class="stat-value">{{ getTermClasses(term.id).length }}</span>
                              <span class="stat-label">个班级</span>
                            </div>
                            <div class="stat-item">
                              <span class="stat-value">{{ getTermStudentCount(term.id) }}</span>
                              <span class="stat-label">名学生</span>
                            </div>
                          </div>
                          <div class="card-right">
                            <button @click.stop="editTerm(term)" class="action-btn edit-btn">
                              <i class="el-icon-edit"></i> 编辑班期
                            </button>
                            <button @click.stop="enterTermManagement(term)" class="enter-btn">
                              进入管理 <i class="el-icon-arrow-right"></i>
                            </button>
                          </div>
                        </div>
                      </div>
                    </div>

                    <!-- 空状态 -->
                    <div v-else class="empty-state">
                      <i class="el-icon-folder-opened empty-icon"></i>
                      <p>暂无班期数据</p>
                      <p class="hint">创建班期后，可以在班期内创建班级并管理学生</p>
                    </div>
                  </div>

                  <!-- 二级页面：班级管理 -->
                  <div v-else class="class-management">
                    <!-- 面包屑导航 -->
                    <div class="breadcrumb-bar-compact">
                      <span class="breadcrumb-item clickable" @click="backToTermOverview">
                        <i class="el-icon-arrow-left"></i> 返回班期列表
                      </span>
                      <span class="breadcrumb-divider">/</span>
                      <span class="breadcrumb-item current">{{ currentViewingTerm.name }}</span>
                    </div>

                    <!-- 左右布局容器 -->
                    <div class="class-sidebar-layout">
                      <!-- 左侧班级目录 -->
                      <div class="class-sidebar">
                        <div class="sidebar-header">
                          <h4>班级列表</h4>
                          <button @click="showAddClassDialog(currentViewingTerm)" class="add-class-btn" title="新建班级">
                            <i class="el-icon-plus"></i>
                          </button>
                        </div>
                        <div class="sidebar-content">
                          <draggable 
                            :value="getTermClasses(currentViewingTerm.id)"
                            @input="updateClassOrder($event, currentViewingTerm.id)"
                            handle=".drag-handle"
                            animation="200"
                            class="class-draggable-area"
                          >
                            <div 
                              v-for="classItem in getTermClasses(currentViewingTerm.id)" 
                              :key="classItem.id"
                              :class="['class-item', { 'active': currentManagingClass && currentManagingClass.id === classItem.id }]"
                              @click="openMemberDrawer(classItem)"
                            >
                              <div class="class-item-header">
                                <span class="drag-handle" title="拖拽调整顺序">☰</span>
                                <span class="class-item-name">{{ classItem.name }}</span>
                              <el-dropdown trigger="click" @command="handleClassCommand($event, classItem)" @click.native.stop>
                                <span class="class-item-more">
                                  <i class="el-icon-more"></i>
                                </span>
                                <el-dropdown-menu slot="dropdown">
                                  <el-dropdown-item command="edit">编辑班级</el-dropdown-item>
                                  <el-dropdown-item command="delete" style="color: #F56C6C;">删除班级</el-dropdown-item>
                                </el-dropdown-menu>
                              </el-dropdown>
                            </div>
                            <div class="class-item-info">
                              <span class="info-text">
                                <i class="el-icon-user"></i> {{ getClassStudentCount(classItem.id) }} / {{ classItem.capacity }}
                              </span>
                            </div>
                            <div v-if="classItem.inviteCode" class="class-item-code">
                              <span class="code-label">邀请码：</span>
                              <span class="code-value" @click.stop="copyInviteCode(classItem.inviteCode)">{{ classItem.inviteCode.substring(0, 3) + '***' }}</span>
                              <i class="el-icon-document-copy copy-icon" @click.stop="copyInviteCode(classItem.inviteCode)" title="点击复制完整邀请码"></i>
                            </div>
                          </div>
                          </draggable>
                          <!-- 空状态 -->
                          <div v-if="getTermClasses(currentViewingTerm.id).length === 0" class="sidebar-empty">
                            <i class="el-icon-folder-opened"></i>
                            <p>暂无班级</p>
                          </div>
                        </div>
                      </div>

                      <!-- 右侧内容区 -->
                      <div class="class-content-area">
                        <!-- 未选择班级提示 -->
                        <div v-if="!currentManagingClass" class="content-placeholder">
                          <i class="el-icon-s-grid"></i>
                          <p>请从左侧选择一个班级查看学生信息</p>
                        </div>

                        <!-- 已选择班级，显示学生信息 -->
                        <div v-else class="member-content">
                          <!-- 操作栏 -->
                          <div class="operation-bar">
                            <el-input
                              v-model="studentSearch"
                              placeholder="搜索学生姓名或学号"
                              prefix-icon="el-icon-search"
                              clearable
                              style="width: 300px;"
                            />
                            <button @click="showAddStudentDialog" class="action-btn primary-btn">
                              <i class="el-icon-plus"></i> 添加学生
                            </button>
                          </div>

                          <!-- 学生列表 -->
                          <div v-if="filteredStudents.length > 0" class="member-table-container">
                            <table class="member-table">
                              <thead>
                                <tr>
                                  <th>姓名</th>
                                  <th>学号</th>
                                  <th>加入时间</th>
                                  <th>状态</th>
                                  <th style="text-align: center;">操作</th>
                                </tr>
                              </thead>
                              <tbody>
                                <tr v-for="student in filteredStudents" :key="student.id">
                                  <td>{{ student.name }}</td>
                                  <td>{{ student.studentNo }}</td>
                                  <td>{{ student.joinTime }}</td>
                                  <td>
                                    <span class="status-badge success">正常</span>
                                  </td>
                                  <td style="text-align: center;">
                                    <button @click="removeStudent(student)" class="action-btn danger-btn small">
                                      <i class="el-icon-delete"></i> 移除
                                    </button>
                                  </td>
                                </tr>
                              </tbody>
                            </table>
                          </div>

                          <!-- 空状态 -->
                          <div v-else class="empty-state">
                            <i class="el-icon-user-solid empty-icon"></i>
                            <p>暂无学生</p>
                            <p class="hint">点击"添加学生"按钮添加第一个学生</p>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </el-tab-pane>

              <!-- 课程管理标签 -->
              <el-tab-pane label="课程管理" name="courseManagement">
                <div class="tab-content course-management-content">
                  <!-- 右上角发布按钮 -->
                  <div class="page-top-actions">
                    <el-button 
                      type="success" 
                      size="medium"
                      icon="el-icon-upload2"
                      @click="publishCourse"
                    >
                      发布课程
                    </el-button>
                  </div>

                  <!-- 卡片一：基本信息 -->
                  <div class="cm-card">
                    <div class="cm-card-header">
                      <h3 class="cm-card-title">基本信息</h3>
                      <el-button 
                        v-if="!editingBasicInfo"
                        type="primary" 
                        size="small"
                        icon="el-icon-edit"
                        plain
                        @click="editingBasicInfo = true"
                      >
                        编辑
                      </el-button>
                    </div>
                    <div class="cm-form">
                      <div class="cm-form-item">
                        <label class="cm-label">课程名称</label>
                        <el-input
                          v-model="courseManagementData.courseName"
                          placeholder="请输入课程名称"
                          maxlength="100"
                          show-word-limit
                          :disabled="!editingBasicInfo"
                        />
                      </div>

                      <div class="cm-form-item">
                        <label class="cm-label">课程封面</label>
                        <div class="cm-upload-area">
                          <el-upload
                            v-if="editingBasicInfo"
                            class="cover-uploader"
                            action="/api/upload/image"
                            :show-file-list="false"
                            :on-success="handleCoverSuccess"
                            :before-upload="beforeCoverUpload"
                          >
                            <img v-if="courseManagementData.coverImage" :src="courseManagementData.coverImage" class="cover-preview">
                            <div v-else class="cover-upload-placeholder">
                              <i class="el-icon-plus"></i>
                              <div class="upload-text">点击上传封面</div>
                              <div class="upload-hint">建议尺寸：800x600px</div>
                            </div>
                          </el-upload>
                          <img v-else-if="courseManagementData.coverImage" :src="courseManagementData.coverImage" class="cover-preview-readonly">
                          <div v-else class="cover-placeholder-readonly">暂无封面</div>
                        </div>
                      </div>

                      <div class="cm-form-item">
                        <label class="cm-label">课程描述</label>
                        <el-input
                          v-model="courseManagementData.description"
                          type="textarea"
                          :rows="4"
                          placeholder="请输入课程描述"
                          maxlength="500"
                          show-word-limit
                          :disabled="!editingBasicInfo"
                        />
                      </div>

                      <div v-if="editingBasicInfo" class="cm-form-actions">
                        <el-button @click="cancelEditBasicInfo">取消</el-button>
                        <el-button type="primary" @click="saveBasicInfo">保存</el-button>
                      </div>
                    </div>
                  </div>

                  <!-- 卡片二：效期与模式 -->
                  <div class="cm-card">
                    <div class="cm-card-header">
                      <h3 class="cm-card-title">效期与模式</h3>
                      <el-button 
                        v-if="!editingValidityMode"
                        type="primary" 
                        size="small"
                        icon="el-icon-edit"
                        plain
                        @click="editingValidityMode = true"
                      >
                        编辑
                      </el-button>
                    </div>
                    <div class="cm-form">
                      <div class="cm-form-item">
                        <label class="cm-label">收费模式</label>
                        <el-radio-group 
                          v-model="courseManagementData.isFree" 
                          @change="onCourseTypeChange"
                          :disabled="!editingValidityMode"
                        >
                          <el-radio :label="true">免费</el-radio>
                          <el-radio :label="false">收费</el-radio>
                        </el-radio-group>
                      </div>

                      <div v-if="!courseManagementData.isFree" class="cm-form-item">
                        <label class="cm-label">课程价格</label>
                        <div class="cm-price-input">
                          <el-input-number
                            v-model="courseManagementData.price"
                            :min="0"
                            :max="99999"
                            :precision="2"
                            controls-position="right"
                            style="width: 200px;"
                            :disabled="!editingValidityMode"
                          />
                          <span class="cm-unit">元</span>
                        </div>
                      </div>

                      <div class="cm-divider"></div>

                      <div class="cm-form-item">
                        <label class="cm-label">有效期</label>
                        <el-radio-group 
                          v-model="courseManagementData.isPermanent" 
                          style="margin-bottom: 10px;"
                          :disabled="!editingValidityMode"
                        >
                          <el-radio :label="true">永久有效</el-radio>
                          <el-radio :label="false">限时有效</el-radio>
                        </el-radio-group>
                        <div v-if="!courseManagementData.isPermanent" class="cm-date-range">
                          <el-date-picker
                            v-model="courseManagementData.validStartDate"
                            type="date"
                            placeholder="开始日期"
                            value-format="yyyy-MM-dd"
                            style="width: 180px;"
                            :disabled="!editingValidityMode"
                          />
                          <span class="date-separator">至</span>
                          <el-date-picker
                            v-model="courseManagementData.validEndDate"
                            type="date"
                            placeholder="截至日期"
                            value-format="yyyy-MM-dd"
                            style="width: 180px;"
                            :disabled="!editingValidityMode"
                          />
                        </div>
                      </div>

                      <div class="cm-form-item">
                        <label class="cm-label">报名人数上限</label>
                        <el-radio-group 
                          v-model="courseManagementData.hasLimit" 
                          style="margin-bottom: 10px;"
                          :disabled="!editingValidityMode"
                        >
                          <el-radio :label="false">不限</el-radio>
                          <el-radio :label="true">有限</el-radio>
                        </el-radio-group>
                        <div v-if="courseManagementData.hasLimit">
                          <el-input-number
                            v-model="courseManagementData.maxStudents"
                            :min="1"
                            controls-position="right"
                            style="width: 200px;"
                            :disabled="!editingValidityMode"
                          />
                          <span class="cm-unit">人</span>
                        </div>
                      </div>

                      <div v-if="editingValidityMode" class="cm-form-actions">
                        <el-button @click="cancelEditValidityMode">取消</el-button>
                        <el-button type="primary" @click="saveValiditySettings">保存</el-button>
                      </div>
                    </div>
                  </div>
                </div>
              </el-tab-pane>

              <!-- 财务订单标签 -->
              <el-tab-pane label="财务订单" name="finance">
                <div class="tab-content">
                  <!-- 订单筛选 -->
                  <div class="filter-bar">
                    <div class="filter-group">
                      <label>搜索：</label>
                      <el-input
                        v-model="orderSearchKeyword"
                        placeholder="搜索订单编号/学生昵称"
                        prefix-icon="el-icon-search"
                        clearable
                        style="width: 240px;"
                      />
                    </div>
                    
                    <div class="filter-group">
                      <label>筛选班期：</label>
                      <select v-model="orderFilterTermId" class="filter-select">
                        <option value="">全部班期</option>
                        <option v-for="term in terms" :key="term.id" :value="term.id">
                          {{ term.name }}
                        </option>
                      </select>
                    </div>
                    
                    <div class="filter-group">
                      <label>支付状态：</label>
                      <select v-model="orderFilterStatus" class="filter-select">
                        <option value="">全部状态</option>
                        <option value="paid">已支付</option>
                        <option value="pending">待支付</option>
                        <option value="refunded">已退款</option>
                      </select>
                    </div>
                    
                    <div class="filter-group">
                      <label>支付时间：</label>
                      <select v-model="orderFilterTimeRange" class="filter-select">
                        <option value="">默认排序</option>
                        <option value="newest">最新在前</option>
                        <option value="oldest">最早在前</option>
                      </select>
                    </div>
                  </div>

                  <!-- 订单详情表格 -->
                  <div class="orders-section">
                    <h3 class="section-title">订单详情</h3>
                    <table class="data-table">
                      <thead>
                        <tr>
                          <th>订单编号</th>
                          <th>学生昵称</th>
                          <th>所属班期</th>
                          <th>支付金额</th>
                          <th>支付时间</th>
                          <th>支付方式</th>
                          <th>状态</th>
                          <th>操作</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr v-for="order in filteredOrders" :key="order.id">
                          <td>{{ order.orderNo }}</td>
                          <td>{{ order.studentName }}</td>
                          <td>{{ getTermName(order.termId) }}</td>
                          <td class="amount-text">¥ {{ order.amount.toFixed(2) }}</td>
                          <td>{{ order.payTime }}</td>
                          <td>{{ order.payMethod }}</td>
                          <td>
                            <span :class="['status-badge', order.status]">
                              {{ getOrderStatusText(order.status) }}
                            </span>
                          </td>
                          <td>
                            <button @click="viewOrderDetail(order)" class="action-link">查看详情</button>
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>
              </el-tab-pane>
            </el-tabs>
          </div>
        </section>
      </main>
    </div>

    <!-- 新建作业模态框 -->
    <div v-if="showHomeworkModal" class="modal-overlay" @click="showHomeworkModal = false">
      <div class="modal-content modal-lg" @click.stop>
        <div class="modal-header">
          <h3>{{ editingHomework ? '编辑作业' : '新建作业' }}</h3>
          <button @click="showHomeworkModal = false" class="close-btn">✕</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label>作业名称 *</label>
            <input v-model="newHomework.name" type="text" placeholder="输入作业名称" class="form-input">
          </div>

          <div class="form-group">
            <label>选择班级 *</label>
            <select v-model="newHomework.className" class="form-input">
              <option value="">请选择班级</option>
              <option value="高一（1）班">高一（1）班</option>
              <option value="高一（2）班">高一（2）班</option>
            </select>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>开始时间 *</label>
              <input v-model="newHomework.startTime" type="datetime-local" class="form-input">
            </div>
            <div class="form-group">
              <label>截止时间 *</label>
              <input v-model="newHomework.endTime" type="datetime-local" class="form-input">
            </div>
          </div>

          <div class="form-group">
            <label>作业描述</label>
            <textarea v-model="newHomework.description" placeholder="输入作业描述" rows="4" class="form-textarea"></textarea>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>满分 *</label>
              <input v-model.number="newHomework.totalPoints" type="number" min="1" placeholder="输入满分分值" class="form-input">
            </div>
            <div class="form-group">
              <label>是否发布</label>
              <select v-model="newHomework.isPublished" class="form-input">
                <option :value="false">草稿</option>
                <option :value="true">已发布</option>
              </select>
            </div>
          </div>

          <div class="modal-actions">
            <button @click="showHomeworkModal = false" class="btn-cancel">取消</button>
            <button @click="submitHomeworkForm" class="btn-submit">{{ editingHomework ? '更新' : '创建' }}作业</button>
          </div>
        </div>
      </div>
    </div>

    <!-- 新建考试模态框 -->
    <div v-if="showExamModal" class="modal-overlay" @click="showExamModal = false">
      <div class="modal-content modal-lg" @click.stop>
        <div class="modal-header">
          <h3>{{ editingExam ? '编辑考试' : '新建考试' }}</h3>
          <button @click="showExamModal = false" class="close-btn">✕</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label>考试名称 *</label>
            <input v-model="newExam.name" type="text" placeholder="输入考试名称" class="form-input">
          </div>

          <div class="form-group">
            <label>选择班级 *</label>
            <select v-model="newExam.className" class="form-input">
              <option value="">请选择班级</option>
              <option value="高一（1）班">高一（1）班</option>
              <option value="高一（2）班">高一（2）班</option>
            </select>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>考试开始时间 *</label>
              <input v-model="newExam.startTime" type="datetime-local" class="form-input">
            </div>
            <div class="form-group">
              <label>考试结束时间 *</label>
              <input v-model="newExam.endTime" type="datetime-local" class="form-input">
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>考试时长（分钟）*</label>
              <input v-model.number="newExam.duration" type="number" min="1" placeholder="输入时长" class="form-input">
            </div>
            <div class="form-group">
              <label>题目总数 *</label>
              <input v-model.number="newExam.questionCount" type="number" min="1" placeholder="输入题目数" class="form-input">
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>总分 *</label>
              <input v-model.number="newExam.totalPoints" type="number" min="1" placeholder="输入总分" class="form-input">
            </div>
            <div class="form-group">
              <label>及格分数 *</label>
              <input v-model.number="newExam.passingScore" type="number" min="1" placeholder="输入及格分" class="form-input">
            </div>
          </div>

          <div class="form-group">
            <label>考试描述</label>
            <textarea v-model="newExam.description" placeholder="输入考试描述和要求" rows="4" class="form-textarea"></textarea>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>是否随机出题</label>
              <select v-model="newExam.isRandom" class="form-input">
                <option :value="false">否</option>
                <option :value="true">是</option>
              </select>
            </div>
            <div class="form-group">
              <label>是否发布</label>
              <select v-model="newExam.isPublished" class="form-input">
                <option :value="false">草稿</option>
                <option :value="true">已发布</option>
              </select>
            </div>
          </div>

          <div class="modal-actions">
            <button @click="showExamModal = false" class="btn-cancel">取消</button>
            <button @click="submitExamForm" class="btn-submit">{{ editingExam ? '更新' : '创建' }}考试</button>
          </div>
        </div>
      </div>
    </div>

    <!-- 发表回复模态框 -->
    <div v-if="showReplyModal" class="modal-overlay" @click="showReplyModal = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>发表话题</h3>
          <button @click="showReplyModal = false" class="close-btn">✕</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label>话题标题</label>
            <input v-model="newThread.title" type="text" placeholder="输入话题标题" class="form-input">
          </div>
          <div class="form-group">
            <label>话题内容</label>
            <textarea v-model="newThread.content" placeholder="输入话题内容" rows="6" class="form-textarea"></textarea>
          </div>
          <div class="modal-actions">
            <button @click="showReplyModal = false" class="btn-cancel">取消</button>
            <button @click="submitThread" class="btn-submit">发表</button>
          </div>
        </div>
      </div>
    </div>

    <!-- 添加题目模态框 -->
    <!-- 创建/编辑题目模态框 - 完全重构版 -->
    <div v-if="showQuestionModal" class="modal-overlay" @click="closeQuestionModal">
      <div class="question-create-modal" @click.stop>
        <div class="modal-header">
          <h3>{{ editingQuestion ? '编辑题目' : '创建题目' }}</h3>
          <button @click="closeQuestionModal" class="close-btn">✕</button>
        </div>
        
        <div class="modal-body-split">
          <!-- 左侧：内容输入区 (70%) -->
          <div class="content-input-section">
            <!-- 1. 顶部：题型切换 -->
            <div class="type-selector-bar">
              <div class="type-tabs">
                <button 
                  v-for="type in questionTypes" 
                  :key="type.value"
                  :class="['type-tab', { active: newQuestion.type === type.value }]"
                  @click="changeQuestionType(type.value)"
                >
                  {{ type.label }}
                </button>
              </div>
            </div>

            <!-- 2. 题干编辑 -->
            <div class="form-section">
              <label class="section-label">题干内容 *</label>
              <textarea 
                v-model="newQuestion.content" 
                placeholder="请输入题目描述..." 
                rows="6" 
                class="large-textarea"
              ></textarea>
            </div>

            <!-- 3. 动态选项区 -->
            <!-- 单选题/多选题 -->
            <div v-if="newQuestion.type === 'single' || newQuestion.type === 'multiple'" class="form-section">
              <label class="section-label">选项设置</label>
              <div class="options-list">
                <div 
                  v-for="(option, idx) in newQuestion.options" 
                  :key="idx" 
                  class="option-row"
                >
                  <span class="option-label">{{ String.fromCharCode(65 + idx) }}.</span>
                  <input 
                    v-model="newQuestion.options[idx]" 
                    type="text" 
                    placeholder="输入选项内容" 
                    class="option-input"
                  >
                  <label class="checkbox-wrapper">
                    <input 
                      v-if="newQuestion.type === 'single'"
                      v-model="newQuestion.answer" 
                      type="radio" 
                      :value="idx"
                      class="answer-radio"
                    >
                    <input 
                      v-else
                      v-model="newQuestion.multipleAnswers" 
                      type="checkbox" 
                      :value="idx"
                      class="answer-checkbox"
                    >
                    <span class="checkbox-label">正确答案</span>
                  </label>
                  <button 
                    v-if="newQuestion.options.length > 2" 
                    @click="removeOption(idx)" 
                    class="remove-option-btn"
                  >
                    ✕
                  </button>
                </div>
              </div>
              <button @click="addOption" class="add-option-btn">+ 添加选项</button>
            </div>

            <!-- 判断题 -->
            <div v-if="newQuestion.type === 'judge'" class="form-section">
              <label class="section-label">正确答案</label>
              <div class="judge-options">
                <label class="radio-option">
                  <input v-model="newQuestion.judgeAnswer" type="radio" value="true">
                  <span>正确 (✓)</span>
                </label>
                <label class="radio-option">
                  <input v-model="newQuestion.judgeAnswer" type="radio" value="false">
                  <span>错误 (✗)</span>
                </label>
              </div>
            </div>

            <!-- 填空题 -->
            <div v-if="newQuestion.type === 'fill'" class="form-section">
              <label class="section-label">参考答案（多个答案用 | 分隔）</label>
              <input 
                v-model="newQuestion.fillAnswer" 
                type="text" 
                placeholder="例如：console.log|console.info" 
                class="form-input"
              >
            </div>

            <!-- 简答题 -->
            <div v-if="newQuestion.type === 'essay'" class="form-section">
              <label class="section-label">参考答案</label>
              <textarea 
                v-model="newQuestion.essayAnswer" 
                placeholder="输入简答题的参考答案..." 
                rows="5" 
                class="form-textarea"
              ></textarea>
            </div>

            <!-- 4. 解析说明 -->
            <div class="form-section">
              <label class="section-label">答案解析</label>
              <textarea 
                v-model="newQuestion.explanation" 
                placeholder="请输入题目解析" 
                rows="4" 
                class="form-textarea"
              ></textarea>
            </div>
          </div>

          <!-- 右侧：算法属性配置区 (30%) -->
          <div class="config-section">
            
            <!-- 难度系数 -->
            <div class="config-item">
              <label class="config-label">难度系数 *</label>
              <div class="slider-container">
                <input 
                  v-model.number="newQuestion.difficultyValue" 
                  type="range" 
                  min="0.1" 
                  max="1.0" 
                  step="0.1" 
                  class="difficulty-slider"
                >
                <div class="slider-value">
                  {{ newQuestion.difficultyValue }} - {{ getDifficultyText(newQuestion.difficultyValue) }}
                </div>
              </div>
              <div class="hint-text">用于智能组卷的难度权重</div>
            </div>

            <!-- 知识点挂载 -->
            <div class="config-item">
              <label class="config-label">知识点</label>
              <el-select 
                v-model="newQuestion.knowledgePoints" 
                multiple 
                filterable
                collapse-tags
                placeholder="选择知识点"
                class="full-width-select"
              >
                <el-option 
                  v-for="item in knowledgePointOptions" 
                  :key="item" 
                  :label="item" 
                  :value="item"
                ></el-option>
              </el-select>
              <button @click="showCreateKnowledgeDialog" class="create-new-btn">
                ➕ 创建新知识点
              </button>
              <div class="hint-text">关联知识点，用于错题推送相关资源</div>
            </div>

            <!-- 标签管理 -->
            <div class="config-item">
              <label class="config-label">标签</label>
              <el-select 
                v-model="newQuestion.tags" 
                multiple 
                filterable
                collapse-tags
                placeholder="选择标签"
                class="full-width-select"
              >
                <el-option 
                  v-for="item in tagOptions" 
                  :key="item" 
                  :label="item" 
                  :value="item"
                ></el-option>
              </el-select>
              <button @click="showCreateTagDialog" class="create-new-btn">
                ➕ 创建新标签
              </button>
              <div class="hint-text">辅助筛选和分类</div>
            </div>
          </div>
        </div>

        <!-- 底部：操作按钮 -->
        <div class="modal-footer">
          <button @click="closeQuestionModal" class="btn-cancel">取消</button>
          <button @click="saveAndContinue" class="btn-secondary">保存并继续创建</button>
          <button @click="saveQuestion" class="btn-primary">保存</button>
        </div>
      </div>
    </div>

    <!-- 班期详情模态框 -->
    <div v-if="showTermDetailModal" class="modal-overlay" @click="showTermDetailModal = false">
      <div class="modal-content modal-lg" @click.stop>
        <div class="modal-header">
          <h3>{{ viewingTerm?.name }} - 详细信息</h3>
          <button @click="showTermDetailModal = false" class="close-btn">✕</button>
        </div>
        <div class="modal-body" v-if="viewingTerm">
          <div class="detail-section">
            <h4 class="detail-title">班期基本信息</h4>
            <div class="detail-row">
              <div class="detail-item">
                <label>班期名称：</label>
                <span>{{ viewingTerm.name }}</span>
              </div>
              <div class="detail-item">
                <label>状态：</label>
                <span :class="['status-badge', viewingTerm.status]">
                  {{ getTermStatusText(viewingTerm.status) }}
                </span>
              </div>
            </div>
            <div class="detail-row">
              <div class="detail-item">
                <label>开始日期：</label>
                <span>{{ viewingTerm.startDate }}</span>
              </div>
              <div class="detail-item">
                <label>结束日期：</label>
                <span>{{ viewingTerm.endDate }}</span>
              </div>
            </div>
            <div class="detail-row">
              <div class="detail-item full-width">
                <label>描述：</label>
                <span>{{ viewingTerm.description || '暂无描述' }}</span>
              </div>
            </div>
          </div>

          <div class="detail-section">
            <h4 class="detail-title">统计信息</h4>
            <div class="stats-grid">
              <div class="stat-card">
                <div class="stat-label">班级数量</div>
                <div class="stat-value">{{ getTermClasses(viewingTerm.id).length }} 个</div>
              </div>
              <div class="stat-card">
                <div class="stat-label">学生总数</div>
                <div class="stat-value">{{ getTermStudentCount(viewingTerm.id) }} 人</div>
              </div>
              <div class="stat-card">
                <div class="stat-label">订单数量</div>
                <div class="stat-value">{{ getTermOrderCount(viewingTerm.id) }} 笔</div>
              </div>
              <div class="stat-card">
                <div class="stat-label">订单收入</div>
                <div class="stat-value">¥ {{ getTermOrderIncome(viewingTerm.id).toFixed(2) }}</div>
              </div>
            </div>
          </div>

          <div class="detail-section">
            <h4 class="detail-title">班级列表</h4>
            <table class="detail-table">
              <thead>
                <tr>
                  <th>班级名称</th>
                  <th>邀请码</th>
                  <th>容量</th>
                  <th>学生数</th>
                  <th>班主任</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="classItem in getTermClasses(viewingTerm.id)" :key="classItem.id">
                  <td>{{ classItem.name }}</td>
                  <td>{{ classItem.inviteCode || '未设置' }}</td>
                  <td>{{ classItem.capacity }}</td>
                  <td>{{ classItem.studentCount }}</td>
                  <td>{{ classItem.teacher || '未指定' }}</td>
                </tr>
              </tbody>
            </table>
          </div>

          <div class="modal-actions">
            <button @click="editTerm(viewingTerm)" class="btn-submit">编辑班期</button>
            <button @click="showTermDetailModal = false" class="btn-cancel">关闭</button>
          </div>
        </div>
      </div>
    </div>

    <!-- 新建/编辑班期模态框 -->
    <div v-if="showTermModal" class="modal-overlay" @click="showTermModal = false">
      <div class="modal-content term-modal" @click.stop>
        <div class="modal-header">
          <div class="header-title">
            <i :class="editingTerm ? 'el-icon-edit' : 'el-icon-plus'"></i>
            <h3>{{ editingTerm ? '编辑班期' : '新建班期' }}</h3>
          </div>
          <button @click="showTermModal = false" class="close-btn">
            <i class="el-icon-close"></i>
          </button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label class="form-label">
              <i class="el-icon-document"></i>
              班期名称 <span class="required">*</span>
            </label>
            <input v-model="newTerm.name" type="text" placeholder="例如：2024春季班" class="form-input">
          </div>

          <div class="form-row">
            <div class="form-group">
              <label class="form-label">
                <i class="el-icon-date"></i>
                开始日期 <span class="required">*</span>
              </label>
              <el-date-picker
                v-model="newTerm.startDate"
                type="date"
                placeholder="选择开始日期"
                format="yyyy-MM-dd"
                value-format="yyyy-MM-dd"
                style="width: 100%;"
              />
            </div>
            <div class="form-group">
              <label class="form-label">
                <i class="el-icon-date"></i>
                结束日期 <span class="required">*</span>
              </label>
              <el-date-picker
                v-model="newTerm.endDate"
                type="date"
                placeholder="选择结束日期"
                format="yyyy-MM-dd"
                value-format="yyyy-MM-dd"
                style="width: 100%;"
              />
            </div>
          </div>

          <div class="form-group">
            <label class="form-label">
              <i class="el-icon-edit-outline"></i>
              班期描述
            </label>
            <textarea v-model="newTerm.description" placeholder="输入班期描述（可选）" rows="3" class="form-textarea"></textarea>
          </div>

          <div class="modal-actions">
            <button @click="showTermModal = false" class="btn-cancel">
              <i class="el-icon-close"></i> 取消
            </button>
            <button @click="submitTermForm" class="btn-submit">
              <i class="el-icon-check"></i> {{ editingTerm ? '保存修改' : '创建班期' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 添加学生模态框 -->
    <div v-if="showAddStudentModal" class="modal-overlay" @click="showAddStudentModal = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>添加学生到 {{ currentManagingClass?.name }}</h3>
          <button @click="showAddStudentModal = false" class="close-btn">✕</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label>学生姓名 *</label>
            <input v-model="newStudent.name" type="text" placeholder="请输入学生姓名" class="form-input">
          </div>

          <div class="form-group">
            <label>联系电话 *</label>
            <input v-model="newStudent.phone" type="tel" placeholder="请输入联系电话" class="form-input">
          </div>

          <div class="modal-actions">
            <button @click="showAddStudentModal = false" class="btn-cancel">取消</button>
            <button @click="submitAddStudent" class="btn-submit">添加</button>
          </div>
        </div>
      </div>
    </div>

    <!-- 新建/编辑班级模态框 -->
    <div v-if="showClassModal" class="modal-overlay" @click="showClassModal = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ editingClass ? '编辑班级' : '新建班级' }}</h3>
          <button @click="showClassModal = false" class="close-btn">✕</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label>班级名称 *</label>
            <input v-model="newClass.name" type="text" placeholder="例如：一班" class="form-input">
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>班级容量 *</label>
              <input v-model.number="newClass.capacity" type="number" min="1" placeholder="50" class="form-input">
            </div>
            <div class="form-group">
              <label>创建人</label>
              <input v-model="newClass.teacher" type="text" placeholder="输入创建人姓名" class="form-input">
            </div>
          </div>

          <div class="form-group">
            <label>班级邀请码</label>
            <div class="input-with-button">
              <input v-model="newClass.inviteCode" type="text" placeholder="自动生成或手动输入" class="form-input">
              <button @click="generateInviteCode" class="btn-generate">生成</button>
            </div>
          </div>

          <div class="form-group">
            <label>班级描述</label>
            <textarea v-model="newClass.description" placeholder="输入班级描述" rows="3" class="form-textarea"></textarea>
          </div>

          <div class="modal-actions">
            <button @click="showClassModal = false" class="btn-cancel">取消</button>
            <button @click="submitClassForm" class="btn-submit">保存</button>
          </div>
        </div>
      </div>
    </div>
    <!-- 新建/编辑文件夹模态框 -->
    <div v-if="showFolderModal" class="modal-overlay" @click="showFolderModal = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ editingFolder ? '编辑文件夹' : '新建文件夹' }}</h3>
          <button @click="closeFolderModal" class="close-btn">✕</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label>文件夹名称 *</label>
            <input 
              v-model="newFolder.name" 
              type="text" 
              placeholder="输入文件夹名称" 
              class="form-input"
              @keyup.enter="submitFolder"
            >
          </div>
          <div class="modal-actions">
            <button @click="closeFolderModal" class="btn-cancel">取消</button>
            <button @click="submitFolder" class="btn-submit">保存</button>
          </div>
        </div>
      </div>
    </div>

    <!-- 移动题目模态框 -->
    <div v-if="showMoveQuestionModal" class="modal-overlay" @click="showMoveQuestionModal = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>移动题目到...</h3>
          <button @click="showMoveQuestionModal = false" class="close-btn">✕</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label>目标文件夹</label>
            <select v-model="moveToFolderId" class="form-input">
              <option :value="null">根目录（未分类）</option>
              <option 
                v-for="folder in questionFolders" 
                :key="folder.id" 
                :value="folder.id"
                :disabled="movingQuestion && movingQuestion.folderId === folder.id"
              >
                {{ folder.name }} ({{ folder.questionCount }})
              </option>
            </select>
          </div>
          <div class="modal-actions">
            <button @click="showMoveQuestionModal = false" class="btn-cancel">取消</button>
            <button @click="confirmMoveQuestion" class="btn-submit">确认移动</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import draggable from 'vuedraggable'

export default {
  name: 'TeacherCourseDetail',
  components: {
    draggable
  },
  data() {
    return {
      activeModule: 'sections',
      managementTab: 'academic', // 管理模块的子标签页
      courseInfo: {
        id: 101,
        name: '高级JavaScript开发',
        description: '深入学习JavaScript的高级特性和最佳实践'
      },
      navItems: [
        { id: 'sections', label: '章节', icon: '📑' },
        { id: 'homework', label: '作业', icon: '📝' },
        { id: 'exam', label: '考试', icon: '📄' },
        { id: 'discussion', label: '课程社区', icon: '💬' },
        { id: 'grades', label: '分析', icon: '📊' },
        { id: 'management', label: '管理', icon: '⚙️' },
        { id: 'questionBank', label: '题库', icon: '📚' }
      ],
      statusOptions: ['全部', '未开始', '进行中', '已结束'],

      // 作业数据和筛选
      homeworkFilter: {
        termId: '',
        class: '',
        status: '全部'
      },
      // 作业列表 - 只显示已发布的作业
      homeworks: [
        {
          id: 1,
          name: '函数进阶练习',
          className: '高一（1）班',
          startTime: '2024-01-15 09:00',
          endTime: '2024-01-22 23:59',
          status: '进行中',
          pendingCount: 3,
          submittedCount: 25,
          unsubmittedCount: 2,
          published: true
        },
        {
          id: 2,
          name: '原型链理解题',
          className: '高一（1）班',
          startTime: '2024-01-08 09:00',
          endTime: '2024-01-15 23:59',
          status: '已结束',
          pendingCount: 0,
          submittedCount: 28,
          unsubmittedCount: 0,
          published: true
        },
        {
          id: 3,
          name: '异步编程作业',
          className: '高一（2）班',
          startTime: '2024-01-20 09:00',
          endTime: '2024-01-27 23:59',
          status: '未开始',
          pendingCount: 0,
          submittedCount: 0,
          unsubmittedCount: 30,
          published: true
        }
      ],

      // 新建作业表单数据
      showHomeworkModal: false,
      editingHomework: null,
      newHomework: {
        name: '',
        className: '',
        startTime: '',
        endTime: '',
        description: '',
        totalPoints: 100,
        isPublished: false
      },

      // 考试数据和筛选
      examFilter: {
        termId: '',
        class: '',
        status: '全部'
      },
      // 考试列表 - 只显示已发布的试卷
      exams: [
        {
          id: 1,
          name: '第一单元测试',
          className: '高一（1）班',
          startTime: '2024-01-18 14:00',
          endTime: '2024-01-18 15:30',
          status: '进行中',
          pendingCount: 5,
          completedCount: 20,
          incompleteCount: 5,
          published: true
        },
        {
          id: 2,
          name: '中期模拟考',
          className: '高一（1）班',
          startTime: '2024-01-10 09:00',
          endTime: '2024-01-10 11:30',
          status: '已结束',
          pendingCount: 0,
          completedCount: 28,
          incompleteCount: 0,
          published: true
        },
        {
          id: 3,
          name: '期末考试',
          className: '高一（2）班',
          startTime: '2024-02-01 09:00',
          endTime: '2024-02-01 11:30',
          status: '未开始',
          pendingCount: 0,
          completedCount: 0,
          incompleteCount: 30,
          published: true
        }
      ],

      // 新建考试表单数据
      showExamModal: false,
      editingExam: null,
      newExam: {
        name: '',
        className: '',
        startTime: '',
        endTime: '',
        duration: 120,
        questionCount: 50,
        totalPoints: 100,
        passingScore: 60,
        description: '',
        isRandom: false,
        isPublished: false
      },

      sections: [
        {
          id: 1,
          title: 'Vue基础入门',
          description: '学习Vue.js的基础概念和核心特性',
          lessons: [
            { id: 101, name: '认识Vue.js', type: 'video', duration: '15分钟' },
            { id: 102, name: '环境搭建指南', type: 'video', duration: '12分钟' },
            { id: 103, name: '第一个Vue应用', type: 'video', duration: '20分钟' }
          ]
        },
        {
          id: 2,
          title: '数据绑定和指令',
          description: '深入理解数据绑定机制和各类指令',
          lessons: [
            { id: 201, name: '数据绑定原理', type: 'video', duration: '18分钟' },
            { id: 202, name: '常用指令详解', type: 'document', duration: '阅读' },
            { id: 203, name: '事件处理', type: 'video', duration: '20分钟' }
          ]
        }
      ],
      showSectionModal: false,
      chapterSearch: '',
      expandedSections: [1, 2], // 默认展开所有章节

      // 讨论区数据
      communitySearch: '',
      communityFilter: '全部',
      communitySortBy: '最新', // 最新、热门
      showMyThreadsOnly: false, // 仅显示我发布的
      currentUserId: 1, // 模拟当前登录用户ID
      currentUserRole: 'teacher', // 当前用户角色：teacher或student
      communityCategory: 'all', // 当前选中的分类
      
      // 社区分类目录
      myCategories: [
        { id: 'all', label: '全部', icon: '📋' },
        { id: 'my-published', label: '我发布的', icon: '✏️' }
      ],
      
      showReplyModal: false,
      newThread: {
        title: '',
        content: ''
      },
      communityThreads: [
        {
          id: 1,
          authorId: 1,
          author: '张三',
          authorRole: 'teacher',
          avatar: 'https://via.placeholder.com/40?text=Teacher1',
          title: '关于原型链的理解',
          content: '请问原型链和原型对象有什么区别？能否用代码示例说明？这是一个关于JavaScript基础的问题,希望老师能详细解答一下,最好能配合代码示例。',
          createTime: '2024-01-20 14:30',
          replyCount: 5,
          viewCount: 120,
          likeCount: 25,
          isLiked: false,
          solved: true,
          essence: true
        },
        {
          id: 2,
          authorId: 2,
          author: '李四',
          authorRole: 'student',
          avatar: 'https://via.placeholder.com/40?text=Student1',
          title: '异步编程最佳实践',
          content: '什么时候应该用 Promise,什么时候用 async/await？在实际开发中经常遇到这两种写法,想了解它们的使用场景和优劣对比。',
          createTime: '2024-01-19 10:15',
          replyCount: 8,
          viewCount: 200,
          likeCount: 42,
          isLiked: false,
          solved: true,
          essence: false
        },
        {
          id: 3,
          authorId: 3,
          author: '王五',
          authorRole: 'student',
          avatar: 'https://via.placeholder.com/40?text=Student2',
          title: '闭包的常见应用场景',
          content: '闭包在实际项目中有哪些应用？能否结合实际案例讲解一下？',
          createTime: '2024-01-18 15:45',
          replyCount: 3,
          viewCount: 85,
          likeCount: 12,
          isLiked: false,
          solved: false,
          essence: false
        }
      ],

      // 分析模块数据
      analyticsActiveTab: 'scores',
      showStrategyModal: false,
      
      // 成绩分析数据
      scoreAnalysis: {
        selectedTerm: '',
        selectedClass: '',
        selectedExam: '',
        avgScore: 85.6,
        passRate: 92.5,
        maxScore: 98,
        deviation: 12.3,
        scoreRanges: [
          { label: '90分以上', count: 15, percentage: 30, color: '#10b981' },
          { label: '80-90分', count: 20, percentage: 40, color: '#3b82f6' },
          { label: '70-80分', count: 10, percentage: 20, color: '#f59e0b' },
          { label: '60-70分', count: 4, percentage: 8, color: '#ef4444' },
          { label: '60分以下', count: 1, percentage: 2, color: '#dc2626' }
        ],
        students: [
          { id: 1, name: '张三', studentNo: '2024001', objectiveScore: 45, subjectiveScore: 53, totalScore: 98 },
          { id: 2, name: '李四', studentNo: '2024002', objectiveScore: 42, subjectiveScore: 48, totalScore: 90 },
          { id: 3, name: '王五', studentNo: '2024003', objectiveScore: 40, subjectiveScore: 46, totalScore: 86 },
          { id: 4, name: '赵六', studentNo: '2024004', objectiveScore: 38, subjectiveScore: 44, totalScore: 82 },
          { id: 5, name: '孙七', studentNo: '2024005', objectiveScore: 36, subjectiveScore: 42, totalScore: 78 }
        ]
      },
      
      // 学习进度数据
      learningProgress: {
        videoProgress: [
          { id: 1, name: '张三', progress: 95 },
          { id: 2, name: '李四', progress: 82 },
          { id: 3, name: '王五', progress: 68 },
          { id: 4, name: '赵六', progress: 45 },
          { id: 5, name: '孙七', progress: 15 }
        ],
        taskParticipation: [
          { name: '作业1', submitted: 45, unsubmitted: 5, submittedRate: 90, unsubmittedRate: 10 },
          { name: '作业2', submitted: 38, unsubmitted: 12, submittedRate: 76, unsubmittedRate: 24 },
          { name: '测验1', submitted: 42, unsubmitted: 8, submittedRate: 84, unsubmittedRate: 16 }
        ],
        resourceHeatmap: [
          { id: 1, name: 'JavaScript基础.pdf', views: 256, downloads: 89, heatPercent: 100 },
          { id: 2, name: '原型链讲解.ppt', views: 198, downloads: 65, heatPercent: 77 },
          { id: 3, name: '异步编程视频', views: 145, downloads: 42, heatPercent: 57 },
          { id: 4, name: '闭包练习题', views: 98, downloads: 28, heatPercent: 38 }
        ]
      },
      
      // 智慧诊断数据
      smartDiagnosis: {
        autoSend: true,
        threshold: 60,
        alerts: [
          {
            id: 1,
            level: 'critical',
            icon: 'el-icon-warning',
            label: '急需巩固',
            description: '逻辑判断知识点准确率低于60%',
            students: ['张三', '李四', '王五']
          },
          {
            id: 2,
            level: 'warning',
            icon: 'el-icon-time',
            label: '熟练度不足',
            description: '数组操作答题耗时过长',
            students: ['赵六', '孙七']
          },
          {
            id: 3,
            level: 'info',
            icon: 'el-icon-refresh',
            label: '遗忘风险',
            description: '函数闭包知识点长期未练习',
            students: ['周八']
          }
        ]
      },
      
      // 保留旧数据用于兼容
      showGradeStats: true,
      gradeFilter: {
        termId: '',
        class: '',
        type: '全部'
      },
      gradeRecords: [
        {
          id: 1,
          studentName: '学生A',
          className: '高一（1）班',
          examGrade: 92,
          homeworkGrade: 88,
          totalGrade: 90,
          level: '优秀'
        },
        {
          id: 2,
          studentName: '学生B',
          className: '高一（1）班',
          examGrade: 78,
          homeworkGrade: 82,
          totalGrade: 80,
          level: '良好'
        },
        {
          id: 3,
          studentName: '学生C',
          className: '高一（2）班',
          examGrade: 85,
          homeworkGrade: 90,
          totalGrade: 88,
          level: '优秀'
        },
        {
          id: 4,
          studentName: '学生D',
          className: '高一（2）班',
          examGrade: 65,
          homeworkGrade: 70,
          totalGrade: 68,
          level: '及格'
        },
        {
          id: 5,
          studentName: '学生E',
          className: '高一（1）班',
          examGrade: 45,
          homeworkGrade: 50,
          totalGrade: 48,
          level: '不及格'
        }
      ],

      // 题库数据
      questionSearch: '',
      folderSearch: '',
      showQuestionModal: false,
      showFolderModal: false,
      showMoveQuestionModal: false,
      showQuestionDetail: false, // 是否显示完整题目
      editingQuestion: null,
      editingFolder: null,
      movingQuestion: null,
      moveToFolderId: null,
      selectedFolderId: null, // 当前选中的文件夹ID，null表示根目录
      activeFolderMenu: null, // 当前打开的文件夹菜单
      activeQuestionMenu: null, // 当前打开的题目菜单
      // 创建知识点/标签对话框
      showKnowledgeDialog: false,
      showTagDialog: false,
      newKnowledgeName: '',
      newTagName: '',
      // 知识点和标签选项列表
      knowledgePointOptions: [
        'JavaScript基础',
        '闭包',
        '原型链',
        '异步编程',
        'Promise',
        'Event Loop',
        'ES6特性'
      ],
      tagOptions: ['重点', '易错', '常考', '综合'],
      questionFilter: {
        type: '',
        difficultyValue: '',
        knowledgePoints: [], // 改为数组支持多选
        tags: [], // 新增标签筛选
        sortBy: '' // 排序方式
      },
      // 题型选项
      questionTypes: [
        { label: '单选题', value: 'single' },
        { label: '多选题', value: 'multiple' },
        { label: '判断题', value: 'judge' },
        { label: '填空题', value: 'fill' },
        { label: '简答题', value: 'essay' }
      ],
      // 文件夹列表（移除全部题目）
      questionFolders: [
        { id: 2, name: 'JavaScript基础', questionCount: 5, pinned: false },
        { id: 3, name: '原型链与继承', questionCount: 3, pinned: false },
        { id: 4, name: '异步编程', questionCount: 4, pinned: false }
      ],
      newFolder: {
        name: ''
      },
      newQuestion: {
        type: 'single',
        content: '',
        difficultyValue: 0.5,
        knowledgePoints: [],
        tags: [],
        options: ['', '', '', ''],
        answer: 0, // 单选题答案索引
        multipleAnswers: [], // 多选题答案索引数组
        judgeAnswer: 'true', // 判断题答案
        fillAnswer: '', // 填空题答案
        essayAnswer: '', // 简答题答案
        explanation: '' // 答案解析
      },
      questions: [
        {
          id: 1,
          folderId: 2,
          type: 'single',
          content: '下列哪个是 JavaScript 的原始数据类型？',
          options: ['Object', 'Array', 'String', 'Function'],
          answer: 2,
          difficultyValue: 0.2,
          knowledgePoint: 'JavaScript基础',
          tags: ['重点', '常考'],
          points: 2,
          usageCount: 15,
          createTime: '2024-01-10',
          creator: '张老师'
        },
        {
          id: 2,
          folderId: 2,
          type: 'fill',
          content: '在 JavaScript 中，___ 是最常用的输出方式。',
          answer: 'console.log',
          difficultyValue: 0.1,
          knowledgePoint: 'JavaScript基础',
          tags: ['重点'],
          points: 2,
          usageCount: 20,
          createTime: '2024-01-11',
          creator: '张老师'
        },
        {
          id: 3,
          folderId: 3,
          type: 'single',
          content: '以下关于闭包的说法正确的是？',
          options: ['闭包是一个函数', '闭包会造成内存泄漏', '闭包可以访问外层函数的变量', '闭包只能在全局作用域中创建'],
          answer: 2,
          difficultyValue: 0.5,
          knowledgePoint: '闭包',
          tags: ['易错', '常考'],
          points: 3,
          usageCount: 8,
          createTime: '2024-01-12',
          creator: '李老师'
        },
        {
          id: 4,
          folderId: 4,
          type: 'essay',
          content: '请简述 Promise 的三个状态及其转换关系',
          answer: 'pending、fulfilled、rejected。pending 可转换为 fulfilled 或 rejected，状态确定后不再改变。',
          difficultyValue: 0.7,
          knowledgePoint: '异步编程',
          tags: ['重点', '综合'],
          points: 5,
          usageCount: 5,
          createTime: '2024-01-13',
          creator: '王老师'
        },
        {
          id: 5,
          folderId: 3,
          type: 'multiple',
          content: '以下哪些是原型链的特点？（多选）',
          options: ['每个对象都有__proto__属性', '原型链用于实现继承', '原型链的顶端是null', '原型链可以被修改'],
          answer: [0, 1, 2, 3],
          difficultyValue: 0.8,
          knowledgePoint: '原型链',
          tags: ['综合', '易错'],
          points: 4,
          usageCount: 3,
          createTime: '2024-01-14',
          creator: '李老师'
        },
        {
          id: 6,
          folderId: 2,
          type: 'judge',
          content: 'JavaScript 是一种强类型语言。',
          answer: false,
          difficultyValue: 0.1,
          knowledgePoint: 'JavaScript基础',
          tags: ['易错'],
          points: 1,
          usageCount: 25,
          createTime: '2024-01-09',
          creator: '张老师'
        },
        {
          id: 7,
          folderId: null,
          type: 'single',
          content: '什么是事件循环（Event Loop）？',
          options: ['一种循环结构', 'JavaScript的执行机制', '一个函数', '一个变量'],
          answer: 1,
          difficultyValue: 0.6,
          knowledgePoint: '异步编程',
          tags: ['重点', '常考'],
          points: 3,
          usageCount: 2,
          createTime: '2024-01-15',
          creator: '王老师'
        }
      ],

      // 班期管理数据
      showTermModal: false,
      editingTerm: null,
      terms: [
        {
          id: 1,
          name: '2024春季班',
          startDate: '2024-03-01',
          endDate: '2024-06-30',
          status: 'active',
          classCount: 3,
          studentCount: 150,
          description: '2024年春季学期'
        },
        {
          id: 2,
          name: '2024秋季班',
          startDate: '2024-09-01',
          endDate: '2024-12-31',
          status: 'upcoming',
          classCount: 0,
          studentCount: 0,
          description: '2024年秋季学期'
        }
      ],
      newTerm: {
        name: '',
        startDate: '',
        endDate: '',
        description: ''
      },

      // 班级管理数据
      showClassModal: false,
      editingClass: null,
      selectedTermForClass: '',
      classes: [
        {
          id: 1,
          termId: 1,
          name: '高一（1）班',
          inviteCode: 'ABC123',
          capacity: 50,
          studentCount: 48,
          teacher: '张老师',
          status: 'active',
          description: '重点班'
        },
        {
          id: 2,
          termId: 1,
          name: '高一（2）班',
          inviteCode: 'XYZ789',
          capacity: 50,
          studentCount: 50,
          teacher: '李老师',
          status: 'active',
          description: '普通班'
        },
        {
          id: 3,
          termId: 1,
          name: '高一（3）班',
          inviteCode: 'MNP567',
          capacity: 50,
          studentCount: 52,
          teacher: '王老师',
          status: 'active',
          description: '实验班'
        }
      ],
      newClass: {
        name: '',
        capacity: 50,
        teacher: '',
        description: '',
        inviteCode: ''
      },
      currentTermId: null,

      // 班期详情
      showTermDetailModal: false,
      viewingTerm: null,

      // 三级导航状态
      currentViewingTerm: null, // null = 显示班期概览(Level 1), object = 显示该班期的班级(Level 2)
      currentManagingClass: null, // null = 显示班级管理(Level 2), object = 显示该班级的成员管理(Level 3)
      studentSearch: '', // 学生搜索关键词
      
      // 添加学生模态框
      showAddStudentModal: false,
      newStudent: {
        name: '',
        studentNo: '',
        phone: '',
        email: ''
      },
      
      // 学生数据 (模拟数据)
      students: [
        // 班级1的学生
        { id: 1, classId: 1, name: '张三', studentNo: '2024001', joinTime: '2024-03-05 10:30' },
        { id: 2, classId: 1, name: '李四', studentNo: '2024002', joinTime: '2024-03-06 09:15' },
        { id: 3, classId: 1, name: '王五', studentNo: '2024003', joinTime: '2024-03-07 14:20' },
        { id: 4, classId: 1, name: '赵六', studentNo: '2024004', joinTime: '2024-03-08 11:45' },
        { id: 5, classId: 1, name: '钱七', studentNo: '2024005', joinTime: '2024-03-09 08:50' },
        // 班级2的学生
        { id: 6, classId: 2, name: '孙八', studentNo: '2024006', joinTime: '2024-03-10 13:30' },
        { id: 7, classId: 2, name: '周九', studentNo: '2024007', joinTime: '2024-03-11 10:15' },
        { id: 8, classId: 2, name: '吴十', studentNo: '2024008', joinTime: '2024-03-12 15:40' },
        { id: 9, classId: 2, name: '郑一', studentNo: '2024009', joinTime: '2024-03-13 09:20' },
        // 班级3的学生
        { id: 10, classId: 3, name: '冯二', studentNo: '2024010', joinTime: '2024-03-14 11:10' },
        { id: 11, classId: 3, name: '陈三', studentNo: '2024011', joinTime: '2024-03-15 14:55' },
        { id: 12, classId: 3, name: '褚四', studentNo: '2024012', joinTime: '2024-03-16 08:30' },
        { id: 13, classId: 3, name: '卫五', studentNo: '2024013', joinTime: '2024-03-17 16:20' },
        { id: 14, classId: 3, name: '蒋六', studentNo: '2024014', joinTime: '2024-03-18 10:45' },
        { id: 15, classId: 3, name: '沈七', studentNo: '2024015', joinTime: '2024-03-19 13:30' }
      ],

      // 拖拽相关状态
      draggedClass: null,
      dragOverClass: null,

      // 课程设置数据
      courseSettings: {
        originalPrice: 299.00,
        discountPrice: 199.00,
        onSale: true,
        maxEnrollment: 0,
        accessType: 'public',
        validDays: 365
      },

      // 财务订单数据
      orderFilterTermId: '', // 订单筛选的班期ID
      orderFilterStatus: '', // 订单状态筛选
      orderFilterTimeRange: '', // 支付时间筛选
      orderSearchKeyword: '', // 订单搜索关键词
      orders: [
        {
          id: 1,
          orderNo: 'ORD20260121001',
          studentName: '张三',
          termId: 1, // 所属班期
          amount: 199.00,
          payTime: '2026-01-21 10:30:25',
          payMethod: '微信支付',
          status: 'paid'
        },
        {
          id: 2,
          orderNo: 'ORD20260121002',
          studentName: '李四',
          termId: 1,
          amount: 199.00,
          payTime: '2026-01-21 11:15:40',
          payMethod: '支付宝',
          status: 'paid'
        },
        {
          id: 3,
          orderNo: 'ORD20260120003',
          studentName: '王五',
          termId: 2,
          amount: 199.00,
          payTime: '2026-01-20 15:20:10',
          payMethod: '微信支付',
          status: 'refunded'
        },
        {
          id: 4,
          orderNo: 'ORD20260119004',
          studentName: '赵六',
          termId: 1,
          amount: 199.00,
          payTime: '2026-01-19 09:20:30',
          payMethod: '微信支付',
          status: 'paid'
        }
      ],

      // 课程管理数据
      courseManagementData: {
        courseName: '',
        coverImage: '',
        description: '',
        isPublished: false,
        isFree: true,
        price: 0,
        isPermanent: true,
        validStartDate: '',
        validEndDate: '',
        hasLimit: false,
        maxStudents: 0,
        sectionCount: 0,
        lessonCount: 0
      },

      // 编辑模式标志
      editingBasicInfo: false,
      editingValidityMode: false
    }
  },
  computed: {
    filteredSections() {
      if (!this.chapterSearch) {
        return this.sections
      }
      const keyword = this.chapterSearch.toLowerCase()
      return this.sections.filter(section => {
        const titleMatch = section.title.toLowerCase().includes(keyword)
        const lessonMatch = section.lessons.some(lesson => 
          lesson.name.toLowerCase().includes(keyword)
        )
        return titleMatch || lessonMatch
      })
    },
    filteredHomeworks() {
      return this.homeworks.filter(hw => {
        // 只显示已发布的作业
        if (!hw.published) {
          return false
        }
        
        // 班期筛选：如果选了班期，先找到该班期下的所有班级名称
        let termMatch = true
        if (this.homeworkFilter.termId) {
          const termClasses = this.classes
            .filter(c => c.termId === this.homeworkFilter.termId)
            .map(c => c.name)
          termMatch = termClasses.includes(hw.className)
        }

        const classMatch = !this.homeworkFilter.class || hw.className === this.homeworkFilter.class
        let statusMatch = true
        if (this.homeworkFilter.status !== '全部') {
          statusMatch = hw.status === this.homeworkFilter.status
        }
        return termMatch && classMatch && statusMatch
      })
    },
    filteredExams() {
      return this.exams.filter(exam => {
        // 只显示已发布的试卷
        if (!exam.published) {
          return false
        }
        
        // 班期筛选
        let termMatch = true
        if (this.examFilter.termId) {
          const termClasses = this.classes
            .filter(c => c.termId === this.examFilter.termId)
            .map(c => c.name)
          termMatch = termClasses.includes(exam.className)
        }

        const classMatch = !this.examFilter.class || exam.className === this.examFilter.class
        let statusMatch = true
        if (this.examFilter.status !== '全部') {
          statusMatch = exam.status === this.examFilter.status
        }
        return termMatch && classMatch && statusMatch
      })
    },
    filteredCommunityThreads() {
      let threads = this.communityThreads.filter(thread => {
        // 搜索匹配
        const searchMatch = !this.communitySearch || 
                           thread.title.includes(this.communitySearch) || 
                           thread.content.includes(this.communitySearch)
        
        // 分类过滤
        let categoryMatch = true
        if (this.communityCategory === 'my-published') {
          categoryMatch = thread.authorId === this.currentUserId
        }
        
        // 个人筛选（保留兼容性）
        const personalMatch = !this.showMyThreadsOnly || 
                             thread.authorId === this.currentUserId
        
        return searchMatch && categoryMatch && personalMatch
      })

      // 排序
      if (this.communitySortBy === '最新') {
        threads = threads.sort((a, b) => new Date(b.createTime) - new Date(a.createTime))
      } else if (this.communitySortBy === '热门') {
        threads = threads.sort((a, b) => {
          // 热度 = 点赞数 * 10
          const hotA = a.likeCount * 10
          const hotB = b.likeCount * 10
          return hotB - hotA
        })
      }

      return threads
    },
    filteredClasses() {
      if (!this.selectedTermForClass) return []
      return this.classes.filter(cls => cls.termId === parseInt(this.selectedTermForClass))
    },
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
    },
    // 筛选后的订单
    filteredOrders() {
      let result = this.orders.filter(order => {
        // 搜索关键词匹配（订单编号或学生昵称）
        if (this.orderSearchKeyword) {
          const keyword = this.orderSearchKeyword.toLowerCase()
          const matchOrderNo = order.orderNo.toLowerCase().includes(keyword)
          const matchStudentName = order.studentName.toLowerCase().includes(keyword)
          if (!matchOrderNo && !matchStudentName) {
            return false
          }
        }
        
        // 班期筛选
        if (this.orderFilterTermId && order.termId !== parseInt(this.orderFilterTermId)) {
          return false
        }
        
        // 状态筛选
        if (this.orderFilterStatus && order.status !== this.orderFilterStatus) {
          return false
        }
        
        return true
      })
      
      // 支付时间排序
      if (this.orderFilterTimeRange === 'newest') {
        result = result.sort((a, b) => new Date(b.payTime) - new Date(a.payTime))
      } else if (this.orderFilterTimeRange === 'oldest') {
        result = result.sort((a, b) => new Date(a.payTime) - new Date(b.payTime))
      }
      
      return result
    },
    filteredGradeRecords() {
      return this.gradeRecords.filter(record => {
        // 班期筛选
        let termMatch = true
        if (this.gradeFilter.termId) {
          const termClasses = this.classes
            .filter(c => c.termId === this.gradeFilter.termId)
            .map(c => c.name)
          termMatch = termClasses.includes(record.className)
        }

        const classMatch = !this.gradeFilter.class || record.className === this.gradeFilter.class
        let typeMatch = true
        if (this.gradeFilter.type !== '全部') {
          typeMatch = record.level === this.gradeFilter.type
        }
        return termMatch && classMatch && typeMatch
      })
    },
    filteredQuestions() {
      let questions = this.questions

      // 文件夹筛选：null表示根目录（只显示folderId为null的未分类题目），否则按folderId筛选
      if (this.selectedFolderId === null) {
        questions = questions.filter(q => q.folderId === null)
      } else {
        questions = questions.filter(q => q.folderId === this.selectedFolderId)
      }

      // 题型筛选
      if (this.questionFilter.type) {
        questions = questions.filter(q => q.type === this.questionFilter.type)
      }

      // 难度筛选
      if (this.questionFilter.difficultyValue) {
        questions = questions.filter(q => q.difficultyValue === parseFloat(this.questionFilter.difficultyValue))
      }

      // 知识点筛选（多选，只要包含任一选中的知识点即可）
      if (this.questionFilter.knowledgePoints && this.questionFilter.knowledgePoints.length > 0) {
        questions = questions.filter(q => 
          this.questionFilter.knowledgePoints.includes(q.knowledgePoint)
        )
      }

      // 标签筛选（多选，只要包含任一选中的标签即可）
      if (this.questionFilter.tags && this.questionFilter.tags.length > 0) {
        questions = questions.filter(q => 
          q.tags && q.tags.some(tag => this.questionFilter.tags.includes(tag))
        )
      }

      // 排序
      if (this.questionFilter.sortBy === 'time-desc') {
        // 最新创建排序
        questions = questions.sort((a, b) => {
          const dateA = new Date(a.createTime)
          const dateB = new Date(b.createTime)
          return dateB - dateA
        })
      } else if (this.questionFilter.sortBy === 'time-asc') {
        // 最早创建排序
        questions = questions.sort((a, b) => {
          const dateA = new Date(a.createTime)
          const dateB = new Date(b.createTime)
          return dateA - dateB
        })
      }

      return questions
    },
    rootQuestionCount() {
      // 统计folderId为null的题目数量（未分类题目）
      return this.questions.filter(q => q.folderId === null).length
    },
    filteredFolders() {
      if (!this.folderSearch) {
        return this.questionFolders
      }
      return this.questionFolders.filter(f => 
        f.name.toLowerCase().includes(this.folderSearch.toLowerCase())
      )
    },
    averageGrade() {
      if (this.gradeRecords.length === 0) return 0
      const sum = this.gradeRecords.reduce((acc, r) => acc + r.totalGrade, 0)
      return sum / this.gradeRecords.length
    },
    maxGrade() {
      return this.gradeRecords.length > 0 ? Math.max(...this.gradeRecords.map(r => r.totalGrade)) : 0
    },
    minGrade() {
      return this.gradeRecords.length > 0 ? Math.min(...this.gradeRecords.map(r => r.totalGrade)) : 0
    },
    passRate() {
      if (this.gradeRecords.length === 0) return 0
      const passCount = this.gradeRecords.filter(r => r.totalGrade >= 60).length
      return Math.round((passCount / this.gradeRecords.length) * 100)
    },
    // 筛选后的学生列表 (用于成员管理抽屉)
    filteredStudents() {
      if (!this.currentManagingClass) return []
      
      return this.students.filter(s => {
        // 班级匹配
        const matchClass = s.classId === this.currentManagingClass.id
        
        // 搜索匹配 (姓名或学号)
        const matchSearch = !this.studentSearch || 
          s.name.includes(this.studentSearch) || 
          s.studentNo.includes(this.studentSearch)
        
        return matchClass && matchSearch
      })
    }
  },
  created() {
    // 根据路由参数初始化activeModule和managementTab
    const tab = this.$route.query.tab
    if (tab) {
      // 如果是管理子标签页(courseManagement, finance, academic)
      if (tab === 'courseManagement' || tab === 'finance' || tab === 'academic') {
        this.activeModule = 'management'
        this.managementTab = tab === 'academic' ? 'academic' : tab === 'finance' ? 'finance' : 'courseManagement'
      } else {
        // 验证tab是否有效
        const validTabs = this.navItems.map(item => item.id)
        if (validTabs.includes(tab)) {
          this.activeModule = tab
        }
      }
    }

    // 初始化课程管理数据
    this.courseManagementData.courseName = this.courseInfo.name
    this.courseManagementData.description = this.courseInfo.description || ''
    this.courseManagementData.coverImage = this.courseInfo.cover || ''    // 初始化课程内容统计
    this.courseManagementData.sectionCount = this.sections.length
    this.courseManagementData.lessonCount = this.sections.reduce((total, section) => total + section.lessons.length, 0)
  },
  methods: {
    // 选择模块
    selectModule(moduleId) {
      console.log('点击了模块:', moduleId)
      this.activeModule = moduleId
      console.log('当前模块:', this.activeModule)
      
      // 更新URL参数
      this.$router.replace({
        name: 'TeacherCourseDetail',
        params: { courseId: this.$route.params.courseId },
        query: { tab: moduleId }
      }).catch(err => {
        // 忽略重复导航错误
        if (err.name !== 'NavigationDuplicated') {
          console.error(err)
        }
      })
    },
    // 章节方法
    toggleSection(sectionId) {
      const index = this.expandedSections.indexOf(sectionId)
      if (index > -1) {
        this.expandedSections.splice(index, 1)
      } else {
        this.expandedSections.push(sectionId)
      }
    },
    selectLesson(lesson, section) {
      // 跳转到课程播放页面
      this.$router.push({
        path: `/teacher/courses/${this.courseInfo.id}/lessons/${lesson.id}`,
        query: {
          sectionId: section.id
        }
      })
    },
    editLesson(lesson) {
      this.$message.info(`编辑课程: ${lesson.name}`)
    },
    deleteLesson(sectionId, lessonId) {
      if (confirm('确定删除该课程吗？')) {
        const section = this.sections.find(s => s.id === sectionId)
        if (section) {
          section.lessons = section.lessons.filter(l => l.id !== lessonId)
          this.$message.success('课程已删除')
        }
      }
    },
    addLesson(section) {
      this.$message.info(`向章节 "${section.title}" 添加新课程`)
    },
    editSection(section) {
      this.$message.info(`编辑章节: ${section.title}`)
    },
    deleteSection(id) {
      if (confirm('确定删除该章节吗？')) {
        this.sections = this.sections.filter(s => s.id !== id)
        this.$message.success('章节已删除')
      }
    },

    // 作业方法
    editHomework(hw) {
      // 跳转到修改设置页面
      this.$router.push(`/teacher/homework/${hw.id}`)
    },
    gradeHomework(hw) {
      this.$router.push(`/teacher/homework/${hw.id}/grading`)
    },
    deleteHomework(id) {
      if (confirm('确定删除该作业吗？')) {
        this.homeworks = this.homeworks.filter(hw => hw.id !== id)
        this.$message.success('作业已删除')
      }
    },
    getClassesByTerm(termId) {
      if (!termId) return []
      return this.classes.filter(c => c.termId === termId)
    },
    goToHomeworkLibrary() {
      this.$router.push('/teacher/homework')
    },
    goToChapterEditor() {
      this.$router.push(`/teacher/courses/${this.$route.params.courseId}/chapters`)
    },
    goToCreateHomework() {
      this.$router.push('/teacher/homework/create')
    },
    viewHomeworkDetail(hw) {
      // 根据是否发布过判断跳转逻辑
      const published = hw.published || false
      this.$router.push({
        path: `/teacher/homework/${hw.id}`,
        query: { published: published }
      })
    },
    submitHomeworkForm() {
      if (!this.newHomework.name || !this.newHomework.className || !this.newHomework.startTime || !this.newHomework.endTime) {
        this.$message.error('请填写必填项')
        return
      }

      if (this.editingHomework) {
        const idx = this.homeworks.findIndex(h => h.id === this.editingHomework.id)
        if (idx > -1) {
          this.homeworks[idx] = {
            ...this.homeworks[idx],
            name: this.newHomework.name,
            className: this.newHomework.className,
            startTime: this.newHomework.startTime,
            endTime: this.newHomework.endTime,
            description: this.newHomework.description,
            totalPoints: this.newHomework.totalPoints,
            status: this.newHomework.isPublished ? '进行中' : '未开始'
          }
          this.$message.success('作业已更新')
        }
      } else {
        this.homeworks.push({
          id: Math.max(...this.homeworks.map(h => h.id), 0) + 1,
          name: this.newHomework.name,
          className: this.newHomework.className,
          startTime: this.newHomework.startTime,
          endTime: this.newHomework.endTime,
          description: this.newHomework.description,
          totalPoints: this.newHomework.totalPoints,
          status: this.newHomework.isPublished ? '进行中' : '未开始',
          pendingCount: 0,
          submittedCount: 0,
          unsubmittedCount: 30
        })
        this.$message.success('作业已创建')
      }

      this.resetHomeworkForm()
      this.showHomeworkModal = false
    },
    resetHomeworkForm() {
      this.newHomework = {
        name: '',
        className: '',
        startTime: '',
        endTime: '',
        description: '',
        totalPoints: 100,
        isPublished: false
      }
      this.editingHomework = null
    },

    // 考试方法
    editExam(exam) {
      // 跳转到修改设置页面
      this.$router.push(`/teacher/exams/${exam.id}`)
    },
    gradeExam(exam) {
      this.$router.push(`/teacher/exams/${exam.id}/grading`)
    },
    viewExamDetail(exam) {
      // 根据发放次数判断是否发布过
      const published = exam.publishCount > 0 || exam.published || false
      this.$router.push({
        path: `/teacher/exams/${exam.id}`,
        query: { published: published }
      })
    },
    deleteExam(id) {
      if (confirm('确定删除该考试吗？')) {
        this.exams = this.exams.filter(exam => exam.id !== id)
        this.$message.success('考试已删除')
      }
    },
    goToExamLibrary() {
      this.$router.push('/teacher/exams')
    },
    goToExamManage() {
      this.$router.push('/exam-center')
    },
    goToCreateExam() {
      this.$router.push('/teacher/exams/create')
    },
    submitExamForm() {
      if (!this.newExam.name || !this.newExam.className || !this.newExam.startTime || !this.newExam.endTime || !this.newExam.duration) {
        this.$message.error('请填写必填项')
        return
      }

      if (this.editingExam) {
        const idx = this.exams.findIndex(e => e.id === this.editingExam.id)
        if (idx > -1) {
          this.exams[idx] = {
            ...this.exams[idx],
            name: this.newExam.name,
            className: this.newExam.className,
            startTime: this.newExam.startTime,
            endTime: this.newExam.endTime,
            duration: this.newExam.duration,
            questionCount: this.newExam.questionCount,
            totalPoints: this.newExam.totalPoints,
            passingScore: this.newExam.passingScore,
            description: this.newExam.description,
            isRandom: this.newExam.isRandom,
            status: this.newExam.isPublished ? '进行中' : '未开始'
          }
          this.$message.success('考试已更新')
        }
      } else {
        this.exams.push({
          id: Math.max(...this.exams.map(e => e.id), 0) + 1,
          name: this.newExam.name,
          className: this.newExam.className,
          startTime: this.newExam.startTime,
          endTime: this.newExam.endTime,
          duration: this.newExam.duration,
          questionCount: this.newExam.questionCount,
          totalPoints: this.newExam.totalPoints,
          passingScore: this.newExam.passingScore,
          description: this.newExam.description,
          isRandom: this.newExam.isRandom,
          status: this.newExam.isPublished ? '进行中' : '未开始',
          pendingCount: 0,
          completedCount: 0,
          incompleteCount: 30
        })
        this.$message.success('考试已创建')
      }

      this.resetExamForm()
      this.showExamModal = false
    },
    resetExamForm() {
      this.newExam = {
        name: '',
        className: '',
        startTime: '',
        endTime: '',
        duration: 120,
        questionCount: 50,
        totalPoints: 100,
        passingScore: 60,
        description: '',
        isRandom: false,
        isPublished: false
      }
      this.editingExam = null
    },

    // 讨论区方法
    markThreadEssence(threadId) {
      const thread = this.communityThreads.find(t => t.id === threadId)
      if (thread) {
        thread.essence = !thread.essence
        this.$message.success(thread.essence ? '已标记为精华' : '已取消精华标记')
      }
    },
    viewThreadDetail(threadId) {
      // 跳转到话题详情页
      this.$router.push({
        path: `/teacher/courses/${this.courseInfo.id}/community/posts/${threadId}`
      })
    },
    createNewThread() {
      // 跳转到创建话题页面
      this.$router.push({
        path: `/teacher/courses/${this.courseInfo.id}/community/posts/create`
      })
    },
    editThread(threadId) {
      // 跳转到编辑页面
      this.$router.push({
        path: `/teacher/courses/${this.courseInfo.id}/community/posts/${threadId}/edit`
      })
    },
    deleteThread(threadId) {
      if (confirm('确定删除该讨论话题吗？')) {
        this.communityThreads = this.communityThreads.filter(t => t.id !== threadId)
        this.$message.success('讨论话题已删除')
      }
    },
    toggleThreadLikeInList(thread) {
      thread.isLiked = !thread.isLiked
      if (thread.isLiked) {
        thread.likeCount++
        // TODO: 调用点赞API
        // this.$api.likeThread(thread.id)
      } else {
        thread.likeCount--
        // TODO: 调用取消点赞API
        // this.$api.unlikeThread(thread.id)
      }
    },
    canManageThread(thread) {
      // 已弃用，保留兼容性
      return thread.authorId === this.currentUserId || this.currentUserRole === 'teacher'
    },
    
    canEditThread(thread) {
      // 只能编辑自己的帖子
      return thread.authorId === this.currentUserId
    },
    
    canDeleteThread(thread) {
      // 老师可以删除任何人的帖子，作者可以删除自己的
      return this.currentUserRole === 'teacher' || thread.authorId === this.currentUserId
    },
    selectCommunityCategory(categoryId) {
      this.communityCategory = categoryId
    },
    getThreadExcerpt(content) {
      // 提取前两行作为摘要
      const lines = content.split('。').filter(line => line.trim())
      const excerpt = lines.slice(0, 2).join('。')
      return excerpt.length > 100 ? excerpt.substring(0, 100) + '...' : excerpt + (lines.length > 0 ? '。' : '')
    },
    submitThread() {
      if (!this.newThread.title || !this.newThread.content) {
        this.$message.error('请填写话题标题和内容')
        return
      }
      this.communityThreads.unshift({
        id: Math.max(...this.communityThreads.map(t => t.id)) + 1,
        authorId: this.currentUserId,
        author: '讲师',
        authorRole: this.currentUserRole,
        avatar: 'https://via.placeholder.com/40?text=Teacher',
        title: this.newThread.title,
        content: this.newThread.content,
        createTime: new Date().toLocaleString('zh-CN'),
        replyCount: 0,
        viewCount: 0,
        solved: false,
        essence: false
      })
      this.newThread = { title: '', content: '' }
      this.showReplyModal = false
      this.$message.success('话题发表成功')
    },

    // 分析模块方法
    onTermChange() {
      this.scoreAnalysis.selectedClass = ''
    },
    getRankClass(index) {
      if (index === 0) return 'rank-1'
      if (index === 1) return 'rank-2'
      if (index === 2) return 'rank-3'
      return ''
    },
    
    // 课程管理方法
    handleCoverSuccess(res) {
      if (res.code === 0) {
        this.courseManagementData.coverImage = res.data.url
        this.$message.success('封面上传成功')
      } else {
        this.$message.error(res.message || '上传失败')
      }
    },
    beforeCoverUpload(file) {
      const isImage = file.type.startsWith('image/')
      const isLt2M = file.size / 1024 / 1024 < 2

      if (!isImage) {
        this.$message.error('只能上传图片文件!')
      }
      if (!isLt2M) {
        this.$message.error('图片大小不能超过 2MB!')
      }
      return isImage && isLt2M
    },
    saveBasicInfo() {
      if (!this.courseManagementData.courseName) {
        this.$message.warning('请输入课程名称')
        return
      }
      this.$confirm('确认保存基本信息？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        // TODO: 调用API保存
        this.courseInfo.name = this.courseManagementData.courseName
        this.courseInfo.description = this.courseManagementData.description
        this.courseInfo.cover = this.courseManagementData.coverImage
        this.editingBasicInfo = false
        this.$message.success('基本信息保存成功')
      }).catch(() => {})
    },
    cancelEditBasicInfo() {
      // 恢复原始数据
      this.courseManagementData.courseName = this.courseInfo.name
      this.courseManagementData.description = this.courseInfo.description || ''
      this.courseManagementData.coverImage = this.courseInfo.cover || ''
      this.editingBasicInfo = false
    },
    onCourseTypeChange(isFree) {
      if (isFree) {
        this.courseManagementData.price = 0
      }
    },
    saveValiditySettings() {
      if (!this.courseManagementData.isFree && this.courseManagementData.price <= 0) {
        this.$message.warning('收费课程价格必须大于0')
        return
      }
      // 限时有效时需要选择日期
      if (!this.courseManagementData.isPermanent) {
        if (!this.courseManagementData.validStartDate || !this.courseManagementData.validEndDate) {
          this.$message.warning('请选择有效期开始和结束时间')
          return
        }
      }
      this.$confirm('确认保存效期与模式设置？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        // TODO: 调用API保存
        this.editingValidityMode = false
        this.$message.success('效期与模式保存成功')
      }).catch(() => {})
    },
    cancelEditValidityMode() {
      // TODO: 恢复原始数据
      this.editingValidityMode = false
    },
    publishCourse() {
      // 检查必填信息
      if (!this.courseManagementData.courseName) {
        this.$message.warning('请先完善课程基本信息')
        return
      }
      if (!this.courseManagementData.isFree && this.courseManagementData.price <= 0) {
        this.$message.warning('收费课程必须设置价格')
        return
      }
      
      this.$confirm('确认发布课程？发布后学员即可看到此课程', '提示', {
        confirmButtonText: '确定发布',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        // TODO: 调用API发布
      }).catch(() => {})
    },
    
    // 保留旧成绩管理方法用于兼容
    editStudentGrade(record) {
      this.$message.info(`编辑学生 ${record.studentName} 的成绩`)
    },
    deleteGradeRecord(recordId) {
      if (confirm('确定删除该成绩记录吗？')) {
        this.gradeRecords = this.gradeRecords.filter(r => r.id !== recordId)
        this.$message.success('成绩记录已删除')
      }
    },
    downloadGradeReport() {
      this.$message.success('成绩单已下载')
    },

    // 题库方法
    selectFolder(folderId) {
      this.selectedFolderId = folderId
    },
    
    // 切换文件夹菜单
    toggleFolderMenu(folderId) {
      this.activeFolderMenu = this.activeFolderMenu === folderId ? null : folderId
      this.activeQuestionMenu = null
      // 点击其他地方关闭菜单
      if (this.activeFolderMenu) {
        setTimeout(() => {
          document.addEventListener('click', this.closeFolderMenu, { once: true })
        }, 100)
      }
    },
    
    closeFolderMenu() {
      this.activeFolderMenu = null
    },
    
    // 切换题目菜单
    toggleQuestionMenu(questionId) {
      this.activeQuestionMenu = this.activeQuestionMenu === questionId ? null : questionId
      this.activeFolderMenu = null
      // 点击其他地方关闭菜单
      if (this.activeQuestionMenu) {
        setTimeout(() => {
          document.addEventListener('click', this.closeQuestionMenu, { once: true })
        }, 100)
      }
    },
    
    closeQuestionMenu() {
      this.activeQuestionMenu = null
    },
    
    // 置顶/取消置顶文件夹
    pinFolder(folder) {
      folder.pinned = !folder.pinned
      // 排序：置顶的在前
      this.questionFolders.sort((a, b) => {
        if (a.pinned && !b.pinned) return -1
        if (!a.pinned && b.pinned) return 1
        return 0
      })
      this.activeFolderMenu = null
      this.$message.success(folder.pinned ? '已置顶' : '已取消置顶')
    },
    
    // 重命名文件夹
    renameFolder(folder) {
      this.$prompt('请输入新的文件夹名称', '重命名文件夹', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        inputValue: folder.name,
        inputPattern: /\S+/,
        inputErrorMessage: '文件夹名称不能为空'
      }).then(({ value }) => {
        folder.name = value.trim()
        this.$message.success('文件夹已重命名')
      }).catch(() => {})
      this.activeFolderMenu = null
    },
    
    // 提交文件夹表单
    submitFolder() {
      if (!this.newFolder.name.trim()) {
        this.$message.error('请输入文件夹名称')
        return
      }
      
      if (this.editingFolder) {
        // 编辑模式
        this.editingFolder.name = this.newFolder.name.trim()
        this.$message.success('文件夹已更新')
      } else {
        // 新建模式
        const newFolder = {
          id: Math.max(0, ...this.questionFolders.map(f => f.id)) + 1,
          name: this.newFolder.name.trim(),
          questionCount: 0,
          pinned: false
        }
        this.questionFolders.push(newFolder)
        this.$message.success('文件夹已创建')
      }
      
      this.closeFolderModal()
    },
    
    // 关闭文件夹模态框
    closeFolderModal() {
      this.showFolderModal = false
      this.editingFolder = null
      this.newFolder = {
        name: ''
      }
    },
    
    // 删除文件夹
    deleteFolder(folderId) {
      this.$confirm('删除文件夹将一并删除其中所有题目，确认删除？', '警告', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        // 删除文件夹和其中的题目
        this.questions = this.questions.filter(q => q.folderId !== folderId)
        this.questionFolders = this.questionFolders.filter(f => f.id !== folderId)
        if (this.selectedFolderId === folderId) {
          this.selectedFolderId = null
        }
        this.$message.success('删除成功')
      }).catch(() => {})
      this.activeFolderMenu = null
    },
    
    // 复制文件夹
    copyFolder(folder) {
      const newFolder = {
        id: Date.now(),
        name: folder.name + ' - 副本',
        questionCount: folder.questionCount,
        pinned: false
      }
      this.questionFolders.push(newFolder)
      
      // 复制文件夹中的题目
      const folderQuestions = this.questions.filter(q => q.folderId === folder.id)
      folderQuestions.forEach(q => {
        const newQuestion = { 
          ...q, 
          id: Date.now() + Math.random(), 
          folderId: newFolder.id,
          createTime: new Date().toISOString().split('T')[0]
        }
        this.questions.push(newQuestion)
      })
      
      this.$message.success('复制成功')
      this.activeFolderMenu = null
    },
    
    // 文件夹拖拽结束
    onFolderDragEnd() {
      this.$message.success('文件夹顺序已更新')
    },
    
    // 更新班级顺序
    updateClassOrder(newOrder) {
      // 更新对应班期的班级顺序
      newOrder.forEach((item, index) => {
        const cls = this.classes.find(c => c.id === item.id)
        if (cls) {
          this.$set(cls, 'order', index)
        }
      })
      this.$message.success('班级顺序已更新')
    },
    
    // 题目拖拽结束
    onQuestionDragEnd() {
      this.$message.success('题目顺序已更新')
    },
    
    // 显示移动题目对话框
    showMoveQuestionDialog(question) {
      this.movingQuestion = question
      this.moveToFolderId = question.folderId
      this.showMoveQuestionModal = true
      this.activeQuestionMenu = null
    },
    
    // 确认移动题目
    confirmMoveQuestion() {
      if (this.movingQuestion) {
        this.movingQuestion.folderId = this.moveToFolderId
        
        const targetFolder = this.moveToFolderId === null 
          ? { name: '根目录' } 
          : this.questionFolders.find(f => f.id === this.moveToFolderId)
        
        this.updateFolderCounts()
        this.$message.success(`已移动至 ${targetFolder.name}`)
        this.showMoveQuestionModal = false
        this.movingQuestion = null
        this.moveToFolderId = null
      }
    },
    
    // 复制题目
    copyQuestion(question) {
      const newQuestion = { 
        ...question, 
        id: Date.now(),
        content: question.content + ' (副本)',
        usageCount: 0,
        createTime: new Date().toISOString().split('T')[0]
      }
      this.questions.push(newQuestion)
      this.updateFolderCounts()
      this.$message.success('题目已复制')
      this.activeQuestionMenu = null
    },
    
    // 查看题目详情（点击标题）
    viewQuestionDetail(question) {
      // 显示题目详情对话框或跳转到详情页
      this.editingQuestion = { ...question }
      this.newQuestion = { ...question }
      this.showQuestionModal = true
    },
    
    getQuestionPreview(content) {
      return content.length > 80 ? content.substring(0, 80) + '...' : content
    },
    getQuestionTypeLabel(type) {
      const labels = {
        single: '单选题',
        multiple: '多选题',
        fill: '填空题',
        judge: '判断题',
        essay: '简答题',
        choice: '选择题' // 兼容旧数据
      }
      return labels[type] || type
    },
    getDifficultyText(value) {
      const difficultyMap = {
        0.1: '极易',
        0.2: '很易',
        0.3: '易',
        0.4: '较易',
        0.5: '中',
        0.6: '较难',
        0.7: '难',
        0.8: '很难',
        0.9: '极难',
        1.0: '最难'
      }
      return difficultyMap[value] || '未知'
    },
    // 判断选项是否为正确答案
    isCorrectOption(question, index) {
      if (question.type === 'single') {
        return question.answer === index
      }
      if (question.type === 'multiple') {
        return Array.isArray(question.answer) && question.answer.includes(index)
      }
      return false
    },
    getDifficultyLabel(difficulty) {
      const labels = {
        easy: '简单',
        medium: '中等',
        hard: '困难'
      }
      return labels[difficulty] || difficulty
    },
    editQuestion(question) {
      this.editingQuestion = question
      this.newQuestion = { ...question }
      this.showQuestionModal = true
    },
    previewQuestion(question) {
      this.$message.info(`预览题目: ${question.content}`)
    },
    deleteQuestion(questionId) {
      if (confirm('确定删除该题目吗？')) {
        this.questions = this.questions.filter(q => q.id !== questionId)
        // 更新文件夹计数
        this.updateFolderCounts()
        this.$message.success('题目已删除')
      }
    },
    updateFolderCounts() {
      // 更新每个文件夹的题目计数
      this.questionFolders.forEach(folder => {
        if (folder.id === 1) {
          folder.questionCount = this.questions.length
        } else {
          folder.questionCount = this.questions.filter(q => q.folderId === folder.id).length
        }
      })
    },
    // 题型切换
    changeQuestionType(type) {
      this.newQuestion.type = type
      // 根据题型初始化默认值
      if (type === 'single' || type === 'multiple') {
        if (this.newQuestion.options.length === 0) {
          this.newQuestion.options = ['', '', '', '']
        }
      }
      if (type === 'single') {
        this.newQuestion.answer = 0
      }
      if (type === 'multiple') {
        this.newQuestion.multipleAnswers = []
      }
      if (type === 'judge') {
        this.newQuestion.judgeAnswer = 'true'
      }
    },
    // 添加选项
    addOption() {
      if (this.newQuestion.options.length < 10) {
        this.newQuestion.options.push('')
      } else {
        this.$message.warning('最多支持10个选项')
      }
    },
    // 删除选项
    removeOption(index) {
      if (this.newQuestion.options.length <= 2) {
        this.$message.warning('至少保留2个选项')
        return
      }
      this.newQuestion.options.splice(index, 1)
      // 调整答案索引
      if (this.newQuestion.type === 'single' && this.newQuestion.answer >= index) {
        this.newQuestion.answer = Math.max(0, this.newQuestion.answer - 1)
      }
      if (this.newQuestion.type === 'multiple') {
        this.newQuestion.multipleAnswers = this.newQuestion.multipleAnswers
          .filter(a => a !== index)
          .map(a => a > index ? a - 1 : a)
      }
    },
    // 关闭模态框
    closeQuestionModal() {
      this.showQuestionModal = false
      this.resetQuestionForm()
    },
    // 保存题目
    saveQuestion() {
      if (!this.validateQuestion()) {
        return
      }
      
      const questionData = this.formatQuestionData()
      
      if (this.editingQuestion) {
        const idx = this.questions.findIndex(q => q.id === this.editingQuestion.id)
        if (idx > -1) {
          this.questions.splice(idx, 1, { ...questionData, id: this.editingQuestion.id })
          this.$message.success('题目已更新')
        }
      } else {
        this.questions.push({
          ...questionData,
          id: Math.max(0, ...this.questions.map(q => q.id)) + 1,
          usageCount: 0,
          createTime: new Date().toISOString().split('T')[0],
          creator: '当前用户' // 实际应从登录信息获取
        })
        this.$message.success('题目已创建')
      }

      this.updateFolderCounts()
      this.closeQuestionModal()
    },
    // 保存并继续创建
    saveAndContinue() {
      if (!this.validateQuestion()) {
        return
      }
      
      const questionData = this.formatQuestionData()
      
      this.questions.push({
        ...questionData,
        id: Math.max(0, ...this.questions.map(q => q.id)) + 1,
        usageCount: 0,
        createTime: new Date().toISOString().split('T')[0],
        creator: '当前用户'
      })

      this.$message.success('题目已保存，继续创建下一题')
      this.updateFolderCounts()
      
      // 只重置内容，保留题型
      const keepType = this.newQuestion.type
      this.resetQuestionForm()
      this.newQuestion.type = keepType
      this.changeQuestionType(keepType)
    },
    // 验证题目
    validateQuestion() {
      if (!this.newQuestion.type) {
        this.$message.error('请选择题型')
        return false
      }
      if (!this.newQuestion.content.trim()) {
        this.$message.error('请输入题干内容')
        return false
      }
      
      // 验证答案
      if (this.newQuestion.type === 'single' || this.newQuestion.type === 'multiple') {
        const hasEmptyOption = this.newQuestion.options.some(opt => !opt.trim())
        if (hasEmptyOption) {
          this.$message.error('请填写所有选项内容')
          return false
        }
      }
      if (this.newQuestion.type === 'multiple' && this.newQuestion.multipleAnswers.length === 0) {
        this.$message.error('请至少选择一个正确答案')
        return false
      }
      if (this.newQuestion.type === 'fill' && !this.newQuestion.fillAnswer.trim()) {
        this.$message.error('请输入填空题答案')
        return false
      }
      
      return true
    },
    // 格式化题目数据
    formatQuestionData() {
      const base = {
        type: this.newQuestion.type,
        folderId: this.selectedFolderId, // 自动设置为当前选中的文件夹
        content: this.newQuestion.content.trim(),
        difficultyValue: this.newQuestion.difficultyValue,
        knowledgePoint: this.newQuestion.knowledgePoints[0] || '', // 主要知识点
        knowledgePoints: this.newQuestion.knowledgePoints, // 所有知识点
        tags: this.newQuestion.tags,
        explanation: this.newQuestion.explanation
      }

      // 根据题型添加特定字段
      if (this.newQuestion.type === 'single') {
        base.options = [...this.newQuestion.options]
        base.answer = this.newQuestion.answer
      } else if (this.newQuestion.type === 'multiple') {
        base.options = [...this.newQuestion.options]
        base.answer = [...this.newQuestion.multipleAnswers]
      } else if (this.newQuestion.type === 'judge') {
        base.answer = this.newQuestion.judgeAnswer === 'true'
      } else if (this.newQuestion.type === 'fill') {
        base.answer = this.newQuestion.fillAnswer
      } else if (this.newQuestion.type === 'essay') {
        base.answer = this.newQuestion.essayAnswer
      }

      return base
    },
    submitQuestion() {
      // 保留旧方法名，调用新方法
      this.saveQuestion()
    },
    resetQuestionForm() {
      this.newQuestion = {
        type: 'single',
        content: '',
        difficultyValue: 0.5,
        knowledgePoints: [],
        tags: [],
        options: ['', '', '', ''],
        answer: 0,
        multipleAnswers: [],
        judgeAnswer: 'true',
        fillAnswer: '',
        essayAnswer: '',
        explanation: ''
      }
      this.editingQuestion = null
    },
    importQuestions() {
      this.$message.info('导入题目功能开发中...')
    },
    exportQuestions() {
      this.$message.success('题目已导出')
    },
    // 显示创建知识点对话框
    showCreateKnowledgeDialog() {
      this.$prompt('请输入新知识点名称', '创建知识点', {
        confirmButtonText: '创建',
        cancelButtonText: '取消',
        inputPattern: /\S+/,
        inputErrorMessage: '知识点名称不能为空'
      }).then(({ value }) => {
        if (!this.knowledgePointOptions.includes(value)) {
          this.knowledgePointOptions.push(value)
          this.newQuestion.knowledgePoints.push(value)
          this.$message.success(`知识点"${value}"已创建`)
        } else {
          this.$message.warning('该知识点已存在')
        }
      }).catch(() => {
        // 取消操作
      })
    },
    // 显示创建标签对话框
    showCreateTagDialog() {
      this.$prompt('请输入新标签名称', '创建标签', {
        confirmButtonText: '创建',
        cancelButtonText: '取消',
        inputPattern: /\S+/,
        inputErrorMessage: '标签名称不能为空'
      }).then(({ value }) => {
        if (!this.tagOptions.includes(value)) {
          this.tagOptions.push(value)
          this.newQuestion.tags.push(value)
          this.$message.success(`标签"${value}"已创建`)
        } else {
          this.$message.warning('该标签已存在')
        }
      }).catch(() => {
        // 取消操作
      })
    },

    // 班期管理方法
    getTermStatusText(status) {
      const map = {
        'active': '进行中',
        'upcoming': '未开始',
        'ended': '已结束'
      }
      return map[status] || status
    },
    editTerm(term) {
      this.editingTerm = term
      this.newTerm = {
        name: term.name,
        startDate: term.startDate,
        endDate: term.endDate,
        description: term.description
      }
      this.showTermModal = true
    },
    viewTermClasses(term) {
      this.selectedTermForClass = term.id.toString()
      this.activeModule = 'classes'
    },

    // ========== 三级导航方法 ==========
    // Level 1 → Level 2: 进入班期的班级管理
    enterTermManagement(term) {
      this.currentViewingTerm = term
      this.currentManagingClass = null
    },
    // Level 2 → Level 1: 返回班期概览
    backToTermOverview() {
      this.currentViewingTerm = null
      this.currentManagingClass = null
      this.studentSearch = ''
    },
    // Level 2 → Level 3: 进入成员管理页面
    openMemberDrawer(classItem) {
      this.currentManagingClass = classItem
      this.studentSearch = ''
    },
    // Level 3 → Level 2: 返回班级管理
    backToClassManagement() {
      this.currentManagingClass = null
      this.studentSearch = ''
    },
    // 复制邀请码到剪贴板
    copyInviteCode(code) {
      if (!code) {
        this.$message.warning('该班级还未设置邀请码')
        return
      }
      
      // 使用 Clipboard API 复制
      navigator.clipboard.writeText(code).then(() => {
        this.$message.success('邀请码已复制到剪贴板')
      }).catch(() => {
        // 降级方案: 使用传统方法
        const textarea = document.createElement('textarea')
        textarea.value = code
        textarea.style.position = 'fixed'
        textarea.style.opacity = '0'
        document.body.appendChild(textarea)
        textarea.select()
        try {
          document.execCommand('copy')
          this.$message.success('邀请码已复制到剪贴板')
        } catch (err) {
          this.$message.error('复制失败，请手动复制')
        }
        document.body.removeChild(textarea)
      })
    },
    // 处理班级下拉菜单命令
    handleClassCommand(command, classItem) {
      if (command === 'edit') {
        this.editClass(classItem)
      } else if (command === 'delete') {
        this.deleteClass(classItem.id)
      }
    },
    // 拖拽开始
    handleDragStart(event, classItem) {
      this.draggedClass = classItem
      event.target.style.opacity = '0.5'
    },
    // 拖拽经过
    handleDragOver(event, classItem) {
      event.preventDefault()
      if (this.draggedClass && this.draggedClass.id !== classItem.id) {
        this.dragOverClass = classItem
      }
    },
    // 放下
    handleDrop(event, targetClass) {
      event.preventDefault()
      if (this.draggedClass && this.draggedClass.id !== targetClass.id) {
        const draggedIndex = this.classes.findIndex(c => c.id === this.draggedClass.id)
        const targetIndex = this.classes.findIndex(c => c.id === targetClass.id)
        
        if (draggedIndex !== -1 && targetIndex !== -1) {
          // 交换位置
          const temp = this.classes[draggedIndex]
          this.classes.splice(draggedIndex, 1)
          this.classes.splice(targetIndex, 0, temp)
          this.$message.success('班级顺序已调整')
        }
      }
      this.dragOverClass = null
    },
    // 拖拽结束
    handleDragEnd(event) {
      event.target.style.opacity = '1'
      this.draggedClass = null
      this.dragOverClass = null
    },
    // 获取班级实际学生数量
    getClassStudentCount(classId) {
      return this.students.filter(s => s.classId === classId).length
    },
    // 移除学生
    removeStudent(student) {
      this.$confirm(`确定要将 ${student.name} 移出班级吗？`, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        const index = this.students.findIndex(s => s.id === student.id)
        if (index > -1) {
          this.students.splice(index, 1)
          this.$message.success('学生已移除')
          
          // 更新班级的学生数量
          if (this.currentManagingClass) {
            const classItem = this.classes.find(c => c.id === this.currentManagingClass.id)
            if (classItem && classItem.studentCount > 0) {
              classItem.studentCount -= 1
            }
          }
        }
      }).catch(() => {})
    },
    // 添加学生（未来功能）
    showAddStudentDialog() {
      if (!this.currentManagingClass) {
        this.$message.error('请先选择班级')
        return
      }
      // 重置表单
      this.newStudent = {
        name: '',
        studentNo: '',
        phone: '',
        email: ''
      }
      this.showAddStudentModal = true
    },
    submitAddStudent() {
      // 验证必填项（只需要姓名和手机号）
      if (!this.newStudent.name || !this.newStudent.phone) {
        this.$message.error('请填写学生姓名和联系电话')
        return
      }
      
      // 生成学号（使用时间戳+随机数）
      const timestamp = Date.now().toString().slice(-6)
      const random = Math.floor(Math.random() * 1000).toString().padStart(3, '0')
      const studentNo = timestamp + random
      
      // 添加学生
      const newId = Math.max(...this.students.map(s => s.id), 0) + 1
      const student = {
        id: newId,
        classId: this.currentManagingClass.id,
        name: this.newStudent.name,
        studentNo: studentNo,
        phone: this.newStudent.phone,
        joinTime: new Date().toISOString().slice(0, 16).replace('T', ' ')
      }
      
      this.students.push(student)
      
      // 更新班级学生数量
      const classItem = this.classes.find(c => c.id === this.currentManagingClass.id)
      if (classItem) {
        classItem.studentCount += 1
      }
      
      this.$message.success('学生添加成功')
      this.showAddStudentModal = false
    },
    // ========== 三级导航方法结束 ==========

    deleteTerm(id) {
      this.$confirm('确定删除该班期吗？删除后班期内的班级也将被删除。', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.terms = this.terms.filter(term => term.id !== id)
        this.classes = this.classes.filter(cls => cls.termId !== id)
        this.$message.success('班期已删除')
      }).catch(() => {})
    },
    submitTermForm() {
      if (!this.newTerm.name || !this.newTerm.startDate || !this.newTerm.endDate) {
        this.$message.error('请填写必填项')
        return
      }

      if (this.editingTerm) {
        const idx = this.terms.findIndex(t => t.id === this.editingTerm.id)
        if (idx > -1) {
          this.terms[idx] = {
            ...this.terms[idx],
            ...this.newTerm
          }
          this.$message.success('班期已更新')
        }
      } else {
        const newTermId = Math.max(...this.terms.map(t => t.id), 0) + 1
        
        // 创建班期
        this.terms.push({
          ...this.newTerm,
          id: newTermId,
          status: 'upcoming',
          classCount: 1,
          studentCount: 0
        })
        
        // 自动创建默认班级
        const newClassId = Math.max(...this.classes.map(c => c.id), 0) + 1
        this.classes.push({
          id: newClassId,
          termId: newTermId,
          name: '默认班级',
          inviteCode: '',
          capacity: 50,
          studentCount: 0,
          creator: '当前教师',
          status: 'active'
        })
        
        this.$message.success('班期已创建，并自动创建默认班级')
      }

      this.showTermModal = false
      this.editingTerm = null
      this.newTerm = { name: '', startDate: '', endDate: '', description: '' }
    },

    // 班级管理方法
    getClassStatusText(status) {
      const map = {
        'active': '正常',
        'archived': '已归档'
      }
      return map[status] || status
    },
    getTermName(termId) {
      const term = this.terms.find(t => t.id === termId)
      return term ? term.name : '未知班期'
    },
    editClass(classItem) {
      this.editingClass = classItem
      // 自动使用当前班期
      if (this.currentViewingTerm) {
        this.selectedTermForClass = this.currentViewingTerm.id.toString()
      }
      this.newClass = {
        name: classItem.name,
        capacity: classItem.capacity,
        teacher: classItem.teacher,
        description: classItem.description
      }
      this.showClassModal = true
    },
    manageStudents(classItem) {
      this.$message.info(`管理班级学生: ${classItem.name}`)
      // TODO: 跳转到学生管理页面
    },
    viewClassStats(classItem) {
      this.$message.info(`查看班级统计: ${classItem.name}`)
      // TODO: 显示班级统计信息
    },
    deleteClass(id) {
      this.$confirm('确定删除该班级吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.classes = this.classes.filter(cls => cls.id !== id)
        this.$message.success('班级已删除')
      }).catch(() => {})
    },
    submitClassForm() {
      if (!this.newClass.name || !this.newClass.capacity) {
        this.$message.error('请填写必填项')
        return
      }

      if (this.editingClass) {
        const idx = this.classes.findIndex(c => c.id === this.editingClass.id)
        if (idx > -1) {
          this.classes[idx] = {
            ...this.classes[idx],
            ...this.newClass
          }
          this.$message.success('班级已更新')
        }
      } else {
        this.classes.push({
          ...this.newClass,
          id: Math.max(...this.classes.map(c => c.id), 0) + 1,
          termId: parseInt(this.selectedTermForClass),
          status: 'active',
          studentCount: 0
        })
        this.$message.success('班级已创建')
      }

      this.showClassModal = false
      this.editingClass = null
      this.newClass = { name: '', capacity: 50, teacher: '', description: '', inviteCode: '' }
    },

    // 管理模块方法
    viewTermDetail(term) {
      this.viewingTerm = term
      this.showTermDetailModal = true
    },
    getTermClasses(termId) {
      return this.classes
        .filter(c => c.termId === termId)
        .sort((a, b) => (a.order || 0) - (b.order || 0))
    },
    getTermStudentCount(termId) {
      return this.classes
        .filter(c => c.termId === termId)
        .reduce((sum, c) => sum + c.studentCount, 0)
    },
    getTermOrderCount(termId) {
      return this.orders.filter(order => order.termId === termId).length
    },
    getTermOrderIncome(termId) {
      return this.orders
        .filter(order => order.termId === termId && order.status === 'paid')
        .reduce((sum, order) => sum + order.amount, 0)
    },
    showAddClassDialog(term) {
      this.currentTermId = term.id
      this.selectedTermForClass = term.id.toString()
      // 设置默认值
      this.newClass = {
        name: '新建班级',
        capacity: 50,
        teacher: '', // TODO: 从用户信息中获取真实姓名
        description: '',
        inviteCode: ''
      }
      this.showClassModal = true
    },
    generateInviteCode() {
      const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
      let code = ''
      for (let i = 0; i < 6; i++) {
        code += chars.charAt(Math.floor(Math.random() * chars.length))
      }
      this.$set(this.newClass, 'inviteCode', code)
      this.$message.success('邀请码已生成：' + code)
    },
    saveCourseSettings() {
      this.$message.success('课程设置已保存')
      // TODO: 调用API保存设置
    },
    getOrderStatusText(status) {
      const map = {
        paid: '已支付',
        pending: '待支付',
        refunded: '已退款'
      }
      return map[status] || status
    },
    viewOrderDetail(order) {
      this.$message.info(`查看订单详情：${order.orderNo}`)
      // TODO: 打开订单详情弹窗
    }
  }
}
</script>

<style scoped>
.teacher-course-detail {
  display: flex;
  min-height: 100vh;
  background-color: white;
  margin: 0;
  padding: 0;
}

/* 左侧固定导航栏 */
.sidebar-fixed {
  width: 220px;
  background: white;
  border-right: 1px solid #e5e7eb;
  position: fixed;
  left: 0;
  top: 64px;
  height: calc(100vh - 64px);
  overflow-y: auto;
  z-index: 99;
  display: flex;
  flex-direction: column;
}

/* Logo区域 */
.sidebar-logo {
  padding: 1.5rem;
  border-bottom: 1px solid #e5e7eb;
  text-align: center;
}

.sidebar-logo h1 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 700;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.nav-menu {
  display: flex;
  flex-direction: column;
  gap: 0;
  padding: 1.5rem 0.75rem;
  flex: 1;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.875rem 1rem;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
  color: #6b7280;
  font-weight: 500;
  user-select: none;
  -webkit-user-select: none;
  margin-bottom: 0.25rem;
}

.nav-item:hover {
  background-color: #f3f4f6;
  color: #374151;
}

.nav-item.active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
}

.nav-icon {
  font-size: 1.2rem;
}

.nav-label {
  font-size: 0.95rem;
}

/* 右侧主内容区 */
.main-wrapper {
  flex: 1;
  margin-left: 220px;
  padding: 0;
  overflow-x: hidden;
}

/* 右侧内容区 */
.content-area {
  background: white;
  min-height: 100vh;
  width: 100%;
  overflow-x: hidden;
}

.module-section {
  padding: 20px;
  animation: fadeIn 0.3s ease-in;
  min-height: 100vh;
  width: 100%;
  box-sizing: border-box;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.module-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0;
  gap: 1rem;
  padding: 1.5rem 2rem;
  background: #f9fafb;
  border-bottom: 1px solid #e5e7eb;
}

.module-header h2 {
  margin: 0;
  color: #2c3e50;
  font-size: 1.3rem;
  font-weight: 700;
}

.action-buttons {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.action-btn {
  padding: 0.65rem 1.25rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.875rem;
  font-weight: 600;
  transition: all 0.3s;
  white-space: nowrap;
}

.action-btn.primary-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.action-btn.primary-btn:hover {
  opacity: 0.9;
  transform: translateY(-2px);
}

.action-btn.secondary-btn {
  background-color: #ecf0f1;
  color: #2c3e50;
  border: 1px solid #bdc3c7;
}

.action-btn.secondary-btn:hover {
  background-color: #d5dbdb;
}

.action-btn.small {
  padding: 0.375rem 0.75rem;
  font-size: 0.8125rem;
}

/* 筛选区 */
.filter-section {
  display: flex;
  gap: 2rem;
  margin: 0;
  padding: 1rem 2rem;
  background-color: #f8f9fa;
  border-bottom: 1px solid #e5e7eb;
  flex-wrap: wrap;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.filter-group label {
  color: #2c3e50;
  font-weight: 600;
  font-size: 0.9rem;
}

.filter-select {
  padding: 0.5rem 0.75rem;
  border: 1px solid #bdc3c7;
  border-radius: 4px;
  background-color: white;
  color: #2c3e50;
  cursor: pointer;
  font-size: 0.875rem;
}

.status-filter-btns {
  display: flex;
  gap: 0.5rem;
}

.filter-btn {
  padding: 0.5rem 1rem;
  background-color: white;
  border: 1px solid #bdc3c7;
  border-radius: 4px;
  color: #7f8c8d;
  cursor: pointer;
  font-size: 0.875rem;
  font-weight: 500;
  transition: all 0.3s;
}

.filter-btn:hover {
  border-color: #667eea;
  color: #667eea;
}

.filter-btn.active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-color: transparent;
}

/* 列表区 */
.list-section {
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
  padding: 1.5rem 2rem;
}

/* 优化后的作业/考试卡片样式 */
.homework-item-card {
  display: flex;
  flex-direction: column;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  padding: 1.5rem;
  transition: all 0.3s;
  gap: 1rem;
}

.exam-item-card {
  display: flex;
  flex-direction: column;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  padding: 1.5rem;
  transition: all 0.3s;
  gap: 1rem;
}

.homework-item-card:hover,
.exam-item-card:hover {
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
  border-color: #d1d5db;
}

/* ========== 顶部区域 ========== */
.card-top-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 2rem;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 0.875rem;
  flex: 1;
}

.task-title {
  margin: 0;
  color: #111827;
  font-size: 1.25rem;
  font-weight: 700;
  line-height: 1.3;
}

.clickable-title {
  cursor: pointer;
  transition: color 0.2s;
}

.clickable-title:hover {
  color: #667eea;
}

/* 状态胶囊 */
.status-capsule {
  padding: 0.4rem 1rem;
  border-radius: 24px;
  font-size: 0.8rem;
  font-weight: 600;
  white-space: nowrap;
  flex-shrink: 0;
}

.status-capsule.未开始 {
  background-color: #e5e7eb;
  color: #6b7280;
}

.status-capsule.进行中 {
  background-color: #fef3c7;
  color: #d97706;
}

.status-capsule.已结束 {
  background-color: #d1fae5;
  color: #059669;
}

/* 统计数字横向排列 */
.stats-inline {
  display: flex;
  gap: 3rem;
  align-items: center;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.25rem;
}

.stat-number {
  font-size: 2rem;
  font-weight: 700;
  line-height: 1;
}

.stat-item.stat-pending .stat-number {
  color: #ef4444;
}

.stat-item.stat-submitted .stat-number {
  color: #10b981;
}

.stat-item.stat-unsubmitted .stat-number {
  color: #9ca3af;
}

.stat-label {
  color: #6b7280;
  font-size: 0.875rem;
  font-weight: 500;
}

/* ========== 中部区域：信息行 ========== */
.card-middle-section {
  display: flex;
  gap: 2rem;
  padding: 0.5rem 0;
}

.info-item {
  display: flex;
  align-items: baseline;
  gap: 0.25rem;
  font-size: 0.9rem;
}

.info-label {
  color: #6b7280;
  font-weight: 500;
}

.info-value {
  color: #374151;
  font-weight: 400;
}

/* ========== 底部区域：操作按钮 ========== */
.card-bottom-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  padding-top: 0.5rem;
}

.primary-action-btn {
  height: 42px;
  padding: 0 2rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  letter-spacing: 0.5px;
  transition: all 0.3s;
}

.primary-action-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(102, 126, 234, 0.3);
}

.primary-action-btn:active {
  transform: translateY(0);
}

/* 底部：辅助操作链 */
.auxiliary-links {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.auxiliary-links a {
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 500;
  text-decoration: none;
  transition: all 0.2s;
}

.link-edit {
  color: #667eea;
}

.link-edit:hover {
  color: #764ba2;
  text-decoration: underline;
}

.link-delete {
  color: #ef4444;
}

.link-delete:hover {
  color: #dc2626;
  text-decoration: underline;
}

/* 考试卡片已统一使用作业卡片的三层布局样式 */

/* 旧样式保留(兼容其他模块) */
.item-card {
  background: #f8f9fa;
  border: 1px solid #ecf0f1;
  border-radius: 6px;
  padding: 1.5rem;
  transition: all 0.3s;
}

.item-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.item-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
  gap: 1rem;
}

.item-title {
  margin: 0;
  color: #2c3e50;
  font-size: 1rem;
  font-weight: 700;
  flex: 1;
}

.status-badge {
  padding: 0.35rem 0.75rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 600;
  white-space: nowrap;
  flex-shrink: 0;
}

.status-badge.未开始 {
  background-color: #ecf0f1;
  color: #7f8c8d;
}

.status-badge.进行中 {
  background-color: #fff3cd;
  color: #856404;
}

.status-badge.已结束 {
  background-color: #d5f4e6;
  color: #27ae60;
}

.item-info {
  display: flex;
  flex-wrap: wrap;
  gap: 2rem;
  margin-bottom: 1rem;
}

.info-item {
  color: #7f8c8d;
  font-size: 0.875rem;
}

.info-item strong {
  color: #2c3e50;
  font-weight: 600;
}

.item-stats {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #e8eaed;
}

.stat-box {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat-label {
  color: #7f8c8d;
  font-size: 0.8rem;
  margin-bottom: 0.25rem;
}

.stat-value {
  font-size: 1.25rem;
  font-weight: 700;
  color: #2c3e50;
}

.stat-value.pending {
  color: #e74c3c;
}

.stat-value.submitted {
  color: #27ae60;
}

.stat-value.unsubmitted {
  color: #95a5a6;
}

.item-actions {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.action-link {
  padding: 0.5rem 1rem;
  background: none;
  border: none;
  color: #667eea;
  cursor: pointer;
  font-weight: 600;
  font-size: 0.85rem;
  transition: color 0.3s;
  text-decoration: none;
}

.action-link:hover {
  color: #764ba2;
  text-decoration: underline;
}

.action-link.primary-action {
  color: #27ae60;
  background-color: rgba(39, 174, 96, 0.1);
  border-radius: 4px;
  padding: 0.5rem 1rem;
}

.action-link.danger-action {
  color: #e74c3c;
}

.action-link.danger-action:hover {
  color: #c0392b;
}

.no-data {
  text-align: center;
  padding: 3rem 2rem;
  color: #95a5a6;
  background-color: #f8f9fa;
  border-radius: 6px;
  border: 1px dashed #bdc3c7;
}

/* 章节卡片 */
.section-card {
  border-left: 4px solid #667eea;
}

.section-number {
  display: inline-block;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 0.35rem 0.75rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 600;
  margin-right: 0.75rem;
}

.lesson-count {
  padding: 0.35rem 0.75rem;
  background: #ecf0f1;
  border-radius: 4px;
  font-size: 0.75rem;
  color: #7f8c8d;
  font-weight: 600;
}

.section-desc {
  color: #7f8c8d;
  line-height: 1.5;
  margin: 0.75rem 0;
  font-size: 0.9rem;
}

.action-lessons {
  margin: 1.5rem 0;
  border: 1px solid #ecf0f1;
  border-radius: 4px;
  overflow: hidden;
}

.lesson-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  border-bottom: 1px solid #ecf0f1;
}

.lesson-item:last-child {
  border-bottom: none;
}

.lesson-item:hover {
  background-color: #f8f9fa;
}

.lesson-number {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  background: #ecf0f1;
  border-radius: 50%;
  font-size: 0.8rem;
  font-weight: 600;
  color: #7f8c8d;
  flex-shrink: 0;
}

.lesson-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex: 1;
}

.lesson-type {
  font-size: 1rem;
}

.lesson-name {
  color: #2c3e50;
  font-weight: 500;
}

.lesson-duration {
  color: #95a5a6;
  font-size: 0.85rem;
  white-space: nowrap;
}

.lesson-item .action-link {
  padding: 0.4rem 0.6rem;
  font-size: 0.9rem;
  border-radius: 4px;
  transition: all 0.3s;
}

.lesson-item .action-link:hover {
  background-color: rgba(102, 126, 234, 0.1);
}

.lesson-item .action-link.danger {
  color: #e74c3c;
}

.lesson-item .action-link.danger:hover {
  background-color: rgba(231, 76, 60, 0.1);
}

/* 模态框 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(2px);
}

.modal-content {
  background: white;
  border-radius: 12px;
  width: 90%;
  max-width: 600px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  animation: modalSlideIn 0.3s ease-out;
}

@keyframes modalSlideIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.modal-content.term-modal {
  max-width: 650px;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 2rem;
  border-bottom: 1px solid #e5e7eb;
  background: linear-gradient(135deg, #f9fafb 0%, #ffffff 100%);
  border-radius: 12px 12px 0 0;
}

.header-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.header-title i {
  font-size: 1.5rem;
  color: #667eea;
}

.modal-header h3 {
  margin: 0;
  color: #1f2937;
  font-size: 1.25rem;
  font-weight: 600;
}

.close-btn {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  font-size: 1.25rem;
  cursor: pointer;
  color: #6b7280;
  transition: all 0.2s;
}

.close-btn:hover {
  background: #fee;
  border-color: #fca5a5;
  color: #dc2626;
}

.modal-body {
  padding: 2rem;
}

/* ========== 课程社区模块样式 ========== */
.community-module {
  padding: 0 !important;
}

/* 布局容器 */
.community-layout {
  display: flex;
  gap: 1.5rem;
  padding: 0;
}

.community-main {
  flex: 1;
  min-width: 0;
}

.community-sidebar {
  width: 280px;
  flex-shrink: 0;
}

/* 1. 顶部操作区 */
.community-top-bar {
  display: flex;
  gap: 1rem;
  padding: 1.5rem 2rem;
  background: white;
  border-bottom: 1px solid #e5e7eb;
  align-items: center;
}

.community-search-input {
  flex: 1;
  height: 42px;
  padding: 0 1rem;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 0.95rem;
  transition: all 0.3s;
}

.community-search-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.community-publish-btn {
  height: 42px;
  padding: 0 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  white-space: nowrap;
}

.community-publish-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(102, 126, 234, 0.3);
}

/* 2. 筛选与排序条 */
.community-filter-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background: #f9fafb;
  border-bottom: 1px solid #e5e7eb;
}

.sort-tabs {
  display: flex;
  gap: 0.5rem;
}

.sort-tab {
  padding: 0.5rem 1.25rem;
  background: white;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  color: #6b7280;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.sort-tab:hover {
  background: #f3f4f6;
  border-color: #9ca3af;
}

.sort-tab.active {
  background: #667eea;
  color: white;
  border-color: #667eea;
}

.personal-filter {
  display: flex;
  align-items: center;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  user-select: none;
}

.filter-checkbox {
  width: 18px;
  height: 18px;
  cursor: pointer;
}

.checkbox-label span {
  color: #374151;
  font-size: 0.9rem;
  font-weight: 500;
}

/* 3. 话题列表容器 */
.community-thread-list {
  padding: 1.5rem 2rem;
  background: #f9fafb;
}

.thread-card {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  padding: 1.5rem;
  margin-bottom: 1rem;
  transition: all 0.3s;
  cursor: pointer;
}

.thread-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  border-color: #d1d5db;
  transform: translateY(-2px);
}

/* 标题层 */
.thread-title-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 0.75rem;
  gap: 1rem;
}

.thread-title {
  flex: 1;
  margin: 0;
  color: #111827;
  font-size: 1.125rem;
  font-weight: 700;
  line-height: 1.4;
  cursor: pointer;
  transition: color 0.2s;
}

.thread-title:hover {
  color: #667eea;
}

.thread-badges {
  display: flex;
  gap: 0.5rem;
  flex-shrink: 0;
}

.badge-role {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
  white-space: nowrap;
}

.badge-role.teacher {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.badge-tag {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
  white-space: nowrap;
}

.badge-tag.essence {
  background: #fef3c7;
  color: #f59e0b;
}

/* 摘要层 */
.thread-preview {
  margin-bottom: 1rem;
}

.thread-excerpt {
  margin: 0;
  color: #6b7280;
  font-size: 0.9rem;
  line-height: 1.6;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* 元数据层 */
.thread-meta-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 0.75rem;
  border-top: 1px solid #e5e7eb;
  font-size: 0.875rem;
}

.thread-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #6b7280;
}

.author-name {
  color: #374151;
  font-weight: 500;
}

.separator {
  color: #d1d5db;
}

.publish-time {
  color: #9ca3af;
}

.thread-stats {
  display: flex;
  align-items: center;
  gap: 1.25rem;
  color: #9ca3af;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.stat-item.clickable {
  cursor: pointer;
  transition: color 0.2s;
}

.stat-item.clickable:hover {
  color: #667eea;
}

.icon-view,
.icon-reply {
  font-style: normal;
}

/* 列表页点赞按钮 */
.like-btn-list {
  background: transparent;
  border: 1px solid #e5e7eb;
  padding: 0.25rem 0.625rem;
  border-radius: 4px;
  font-size: 0.8125rem;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.2s;
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
}

.like-btn-list:hover {
  border-color: #ff6b6b;
  color: #ff6b6b;
  background: #fff5f5;
}

.like-btn-list.liked {
  border-color: #ff6b6b;
  color: #ff6b6b;
  background: #fff5f5;
}

/* 管理操作 */
.thread-manage {
  display: flex;
  gap: 0.75rem;
  margin-left: 1rem;
  padding-left: 1rem;
  border-left: 1px solid #e5e7eb;
}

.manage-link {
  color: #667eea;
  font-weight: 500;
  cursor: pointer;
  text-decoration: none;
  transition: color 0.2s;
}

.manage-link:hover {
  color: #764ba2;
  text-decoration: underline;
}

.manage-link.delete {
  color: #ef4444;
}

.manage-link.delete:hover {
  color: #dc2626;
}

/* 右侧分类导航 */
.community-sidebar {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  padding: 1.5rem;
  align-self: flex-start;
  position: sticky;
  top: 1.5rem;
}

.sidebar-section {
  margin-bottom: 0;
}

.sidebar-title {
  margin: 0 0 1rem 0;
  color: #111827;
  font-size: 1rem;
  font-weight: 700;
  padding-bottom: 0.75rem;
  border-bottom: 2px solid #e5e7eb;
}

.category-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.category-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
  background: white;
  border: 1px solid transparent;
}

.category-item:hover {
  background: #f9fafb;
  border-color: #e5e7eb;
}

.category-item.active {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
  border-color: #667eea;
}

.category-icon {
  font-size: 1.25rem;
  flex-shrink: 0;
}

.category-label {
  color: #374151;
  font-size: 0.9375rem;
  font-weight: 500;
  flex: 1;
}

.category-item.active .category-label {
  color: #667eea;
  font-weight: 600;
}

/* 旧样式保留(兼容) */
.community-card {
  border-left: 4px solid #667eea;
}

.thread-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
  gap: 1rem;
}

.thread-user {
  display: flex;
  gap: 0.75rem;
  flex: 1;
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
  flex-shrink: 0;
}

.user-info {
  flex: 1;
}

.user-name {
  margin: 0;
  color: #2c3e50;
  font-weight: 600;
  font-size: 0.9rem;
}

.thread-time {
  color: #95a5a6;
  font-size: 0.8rem;
}

.badge {
  padding: 0.25rem 0.6rem;
  border-radius: 3px;
  font-size: 0.75rem;
  font-weight: 600;
  white-space: nowrap;
}

.badge.solved {
  background: #d5f4e6;
  color: #27ae60;
}

.badge.essence {
  background: #fef5e7;
  color: #f39c12;
}

.thread-content {
  color: #7f8c8d;
  line-height: 1.6;
  margin: 0 0 1rem 0;
  font-size: 0.9rem;
}

.thread-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #ecf0f1;
}

.reply-count,
.view-count {
  color: #95a5a6;
  font-size: 0.85rem;
}

.thread-actions {
  display: flex;
  gap: 0.75rem;
}


/* 分析模块样式 */
.analytics-module {
  padding: 0 !important;
}

.analytics-container {
  width: 100%;
}

.analytics-tabs {
  background: white;
}

.analytics-tabs >>> .el-tabs__header {
  padding: 0 2rem;
  margin: 0;
  background: #f9fafb;
  border-bottom: 2px solid #e5e7eb;
}

.analytics-tabs >>> .el-tabs__nav-wrap {
  padding: 1rem 0 0 0;
}

.analytics-tabs >>> .el-tabs__item {
  font-size: 1rem;
  font-weight: 600;
  height: 50px;
  line-height: 50px;
}

.analytics-tabs >>> .el-tabs__item.is-active {
  color: #667eea;
}

.analytics-tabs >>> .el-tabs__active-bar {
  background: #667eea;
  height: 3px;
}

.analytics-content {
  padding: 2rem;
}

/* 筛选区 */
.analytics-filters {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: #f9fafb;
  border-radius: 12px;
}

/* 概览卡片 */
.summary-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.summary-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  transition: all 0.3s;
}

.summary-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 16px rgba(0,0,0,0.1);
}

.card-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.75rem;
}

.card-info {
  flex: 1;
}

.card-label {
  font-size: 0.875rem;
  color: #6b7280;
  margin-bottom: 0.5rem;
}

.card-value {
  font-size: 1.875rem;
  font-weight: 700;
  color: #1f2937;
}

/* 图表卡片 */
.chart-card,
.detail-table-card,
.progress-card,
.participation-card,
.heatmap-card,
.radar-card,
.alert-card,
.strategy-card {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  margin-bottom: 2rem;
}

.chart-title,
.table-title,
.card-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 1.5rem;
  padding-bottom: 0.75rem;
  border-bottom: 2px solid #e5e7eb;
}

/* 分数段分布 */
.score-distribution {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.score-bar-item {
  display: grid;
  grid-template-columns: 100px 1fr 150px;
  align-items: center;
  gap: 1rem;
}

.range-label {
  font-weight: 600;
  color: #374151;
}

.bar-container {
  background: #f3f4f6;
  height: 32px;
  border-radius: 8px;
  overflow: hidden;
}

.bar-fill {
  height: 100%;
  border-radius: 8px;
  transition: width 0.6s ease;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  padding-right: 0.5rem;
  color: white;
  font-size: 0.875rem;
  font-weight: 600;
}

.range-count {
  text-align: right;
  color: #6b7280;
  font-size: 0.9375rem;
}

/* 明细表格 */
.analytics-table {
  width: 100%;
  border-collapse: collapse;
}

.analytics-table th {
  background: #f9fafb;
  padding: 1rem;
  text-align: left;
  font-weight: 600;
  color: #374151;
  border-bottom: 2px solid #e5e7eb;
}

.analytics-table td {
  padding: 0.875rem 1rem;
  border-bottom: 1px solid #e5e7eb;
  color: #6b7280;
}

.analytics-table tbody tr:hover {
  background: #f9fafb;
}

.rank-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  font-weight: 700;
  background: #e5e7eb;
  color: #6b7280;
}

.rank-badge.rank-1 {
  background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
  color: white;
}

.rank-badge.rank-2 {
  background: linear-gradient(135deg, #d1d5db 0%, #9ca3af 100%);
  color: white;
}

.rank-badge.rank-3 {
  background: linear-gradient(135deg, #f87171 0%, #dc2626 100%);
  color: white;
}

.total-score {
  font-weight: 700;
  color: #667eea;
  font-size: 1.125rem;
}

/* 学习进度样式 */
.progress-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.progress-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.student-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.student-name {
  font-weight: 600;
  color: #374151;
}

.student-name.low-progress {
  color: #ef4444;
}

.progress-percent {
  font-size: 0.875rem;
  color: #6b7280;
  font-weight: 600;
}

.progress-bar {
  background: #f3f4f6;
  height: 24px;
  border-radius: 12px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  border-radius: 12px;
  transition: width 0.6s ease;
}

/* 任务参与率 */
.participation-chart {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.task-bar {
  display: grid;
  grid-template-columns: 150px 1fr 80px;
  align-items: center;
  gap: 1rem;
}

.task-name {
  font-weight: 600;
  color: #374151;
}

.bar-group {
  display: flex;
  height: 40px;
  border-radius: 8px;
  overflow: hidden;
  background: #f3f4f6;
}

.bar-segment {
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 0.875rem;
  font-weight: 600;
  transition: width 0.6s ease;
}

.bar-segment.submitted {
  background: #10b981;
}

.bar-segment.unsubmitted {
  background: #ef4444;
}

.task-stats {
  text-align: right;
  font-weight: 700;
  color: #10b981;
}

/* 资源热力图 */
.heatmap-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.heatmap-item {
  display: grid;
  grid-template-columns: 200px 1fr 200px;
  align-items: center;
  gap: 1rem;
}

.resource-name {
  font-weight: 600;
  color: #374151;
}

.heat-bar {
  background: #f3f4f6;
  height: 28px;
  border-radius: 8px;
  overflow: hidden;
}

.heat-fill {
  height: 100%;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
  border-radius: 8px;
  transition: width 0.6s ease;
}

.resource-stats {
  display: flex;
  gap: 1.5rem;
  justify-content: flex-end;
  color: #6b7280;
  font-size: 0.875rem;
}

.resource-stats span {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

/* 智慧诊断样式 */
.radar-placeholder {
  text-align: center;
  padding: 4rem 2rem;
  color: #9ca3af;
}

.radar-placeholder .hint {
  font-size: 0.875rem;
  margin-top: 0.5rem;
}

.alert-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.alert-item {
  display: flex;
  gap: 1rem;
  padding: 1.5rem;
  border-radius: 12px;
  border: 2px solid;
  transition: all 0.3s;
}

.alert-item.critical {
  background: #fef2f2;
  border-color: #fee2e2;
}

.alert-item.warning {
  background: #fffbeb;
  border-color: #fef3c7;
}

.alert-item.info {
  background: #eff6ff;
  border-color: #dbeafe;
}

.alert-icon {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  flex-shrink: 0;
}

.alert-item.critical .alert-icon {
  background: #fee2e2;
  color: #dc2626;
}

.alert-item.warning .alert-icon {
  background: #fef3c7;
  color: #f59e0b;
}

.alert-item.info .alert-icon {
  background: #dbeafe;
  color: #3b82f6;
}

.alert-content {
  flex: 1;
}

.alert-label {
  font-size: 1.125rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 0.5rem;
}

.alert-desc {
  color: #6b7280;
  margin-bottom: 0.75rem;
}

.affected-students {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.student-tag {
  padding: 0.25rem 0.75rem;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 16px;
  font-size: 0.875rem;
  color: #374151;
}

/* 推送策略配置 */
.strategy-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 0.75rem;
  border-bottom: 2px solid #e5e7eb;
}

.config-btn {
  padding: 0.5rem 1rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 600;
  transition: all 0.3s;
}

.config-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.strategy-status {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.status-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: #f9fafb;
  border-radius: 8px;
}

.status-label {
  font-weight: 600;
  color: #374151;
}

.status-value {
  font-weight: 700;
  color: #667eea;
  font-size: 1.125rem;
}

/* 保留旧样式用于兼容 */
.stats-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin: 0;
  padding: 1.5rem 2rem;
}

.stat-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 1.5rem;
  border-radius: 8px;
  text-align: center;
}

.stat-label {
  display: block;
  font-size: 0.9rem;
  opacity: 0.9;
  margin-bottom: 0.5rem;
}

.stat-value {
  display: block;
  font-size: 2rem;
  font-weight: 700;
}

.table-section {
  overflow-x: auto;
  margin: 0;
  padding: 0 2rem 1.5rem 2rem;
}

.grades-table {
  width: 100%;
  border-collapse: collapse;
  background: white;
  font-size: 0.9rem;
}

.grades-table thead {
  background: #f8f9fa;
  border-bottom: 2px solid #ecf0f1;
}

.grades-table th {
  padding: 1rem;
  text-align: left;
  color: #2c3e50;
  font-weight: 600;
}

.grades-table td {
  padding: 0.75rem 1rem;
  border-bottom: 1px solid #ecf0f1;
  color: #7f8c8d;
}

.grades-table tbody tr:hover {
  background: #f8f9fa;
}

.total-grade {
  color: #667eea;
  font-weight: 600;
}

.grade-badge {
  padding: 0.35rem 0.75rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 600;
  white-space: nowrap;
}

.grade-badge.优秀 {
  background: #d5f4e6;
  color: #27ae60;
}

.grade-badge.良好 {
  background: #d5e8f7;
  color: #3498db;
}

.grade-badge.及格 {
  background: #fef5e7;
  color: #f39c12;
}

.grade-badge.不及格 {
  background: #ffe5e5;
  color: #e74c3c;
}

/* ========== 题库模块样式 ========== */
.question-bank-module {
  height: 100vh;
  display: flex;
  flex-direction: column;
  padding: 0;
}

/* 顶部操作栏 */
.question-bank-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 2rem;
  background: white;
  border-bottom: 1px solid #e5e7eb;
}

.left-actions {
  display: flex;
  gap: 1rem;
  align-items: center;
}

/* 显示详情开关 */
.detail-toggle {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  user-select: none;
  font-size: 0.875rem;
  color: #6b7280;
  padding: 0.5rem 0.75rem;
  background: #f9fafb;
  border-radius: 6px;
  transition: all 0.2s;
}

.detail-toggle:hover {
  background: #f3f4f6;
}

.toggle-checkbox {
  width: 16px;
  height: 16px;
  cursor: pointer;
}

.right-filters {
  display: flex;
  gap: 0.75rem;
}

.compact-select {
  padding: 0.5rem 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 0.875rem;
  color: #374151;
  background: white;
  cursor: pointer;
  transition: all 0.2s;
  min-width: 140px;
}

.compact-select:hover {
  border-color: #667eea;
}

.compact-select:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

/* Element UI 多选下拉框样式调整 */
.compact-select-multi {
  font-size: 0.875rem;
}

.compact-select-multi .el-input__inner {
  padding: 0.5rem 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 0.875rem;
  color: #374151;
  transition: all 0.2s;
  min-height: 36px;
}

.compact-select-multi .el-input__inner:hover {
  border-color: #667eea;
}

.compact-select-multi .el-input__inner:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

/* 主体布局 */
.question-bank-body {
  display: flex;
  flex: 1;
  overflow: hidden;
}

/* 左侧文件夹树 */
.folder-sidebar {
  width: 20%;
  min-width: 200px;
  background: white;
  border-right: 1px solid #e5e7eb;
  display: flex;
  flex-direction: column;
}

.sidebar-search {
  padding: 1rem;
  border-bottom: 1px solid #e5e7eb;
}

.folder-search-input {
  width: 100%;
  padding: 0.5rem 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 0.875rem;
  transition: all 0.2s;
}

.folder-search-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.folder-tree {
  flex: 1;
  overflow-y: auto;
  padding: 0.5rem 0;
}

.folder-item {
  display: flex;
  align-items: center;
  padding: 0.75rem 1rem;
  cursor: pointer;
  transition: all 0.2s;
  gap: 0.5rem;
  position: relative;
}

.drag-handle {
  font-size: 1rem;
  color: #9ca3af;
  cursor: move;
  padding: 0.25rem;
  margin-right: 0.25rem;
  transition: color 0.2s;
}

.drag-handle:hover {
  color: #667eea;
}

.folder-draggable-area {
  min-height: 50px;
}

.folder-item:hover {
  background: #f3f4f6;
}

.folder-item.active {
  background: linear-gradient(135deg, #667eea20 0%, #764ba220 100%);
  border-left: 3px solid #667eea;
}

.folder-item.pinned {
  background: #fffbeb;
  border-left: 3px solid #f59e0b;
}

.folder-item.pinned.active {
  background: linear-gradient(135deg, #fef3c720 0%, #fde68a20 100%);
  border-left: 3px solid #f59e0b;
}

.folder-icon {
  font-size: 1.125rem;
}

.folder-name {
  flex: 1;
  font-size: 0.875rem;
  color: #374151;
  font-weight: 500;
}

.folder-count {
  font-size: 0.75rem;
  color: #9ca3af;
}

/* 文件夹菜单 */
.folder-menu {
  position: relative;
  margin-left: auto;
}

.menu-trigger {
  padding: 0.25rem 0.5rem;
  background: transparent;
  border: none;
  color: #9ca3af;
  font-size: 1.25rem;
  cursor: pointer;
  border-radius: 4px;
  transition: all 0.2s;
  line-height: 1;
}

.menu-trigger:hover {
  background: #e5e7eb;
  color: #374151;
}

.menu-dropdown {
  position: absolute;
  right: 0;
  top: 100%;
  margin-top: 0.25rem;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  z-index: 1000;
  min-width: 120px;
  overflow: hidden;
}

.menu-item {
  display: block;
  width: 100%;
  padding: 0.625rem 1rem;
  background: white;
  border: none;
  text-align: left;
  font-size: 0.875rem;
  color: #374151;
  cursor: pointer;
  transition: all 0.2s;
}

.menu-item:hover {
  background: #f3f4f6;
}

.menu-item.danger {
  color: #ef4444;
}

.menu-item.danger:hover {
  background: #fef2f2;
}

.new-folder-btn {
  margin: 1rem;
  padding: 0.75rem;
  background: white;
  border: 2px dashed #d1d5db;
  border-radius: 6px;
  color: #667eea;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.new-folder-btn:hover {
  border-color: #667eea;
  background: #f5f7ff;
}

/* 右侧题目列表 */
.question-list-area {
  flex: 1;
  overflow-y: auto;
  background: #f9fafb;
  padding: 1.5rem;
}

.question-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(450px, 1fr));
  gap: 1.25rem;
}

.question-preview-card {
  background: white;
  border-radius: 8px;
  padding: 1.25rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: all 0.3s;
  border-left: 4px solid #667eea;
  cursor: move;
}

.question-preview-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  transform: translateY(-2px);
}

/* 卡片顶部元数据 */
.card-meta-row {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 0.875rem;
  flex-wrap: wrap;
}

.type-tag {
  padding: 0.25rem 0.625rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 600;
  color: white;
}

.type-tag.single {
  background: #667eea;
}

.type-tag.multiple {
  background: #764ba2;
}

.type-tag.fill {
  background: #3498db;
}

.type-tag.judge {
  background: #27ae60;
}

.type-tag.essay {
  background: #e74c3c;
}

.difficulty-value {
  padding: 0.25rem 0.625rem;
  background: #f3f4f6;
  color: #6b7280;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 500;
}

.knowledge-tag {
  padding: 0.25rem 0.625rem;
  background: #ecfdf5;
  color: #059669;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 500;
}

.tag-badge {
  padding: 0.25rem 0.625rem;
  background: #fef3c7;
  color: #f59e0b;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 500;
}

/* 卡片内容预览 */
.card-content-preview {
  margin-bottom: 1rem;
}

/* 可点击的题目标题 */
.question-title-clickable {
  font-size: 0.9375rem;
  color: #1f2937;
  line-height: 1.6;
  margin: 0 0 0.75rem 0;
  font-weight: 500;
  cursor: pointer;
  transition: color 0.2s;
}

.question-title-clickable:hover {
  color: #667eea;
}

.options-preview {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.option-item {
  padding: 0.5rem 0.75rem;
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 4px;
  font-size: 0.8125rem;
  color: #6b7280;
}

.question-text {
  font-size: 0.9375rem;
  color: #1f2937;
  line-height: 1.6;
  margin: 0 0 0.75rem 0;
  font-weight: 500;
}

.options-preview {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.option-tag {
  padding: 0.375rem 0.625rem;
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 4px;
  font-size: 0.8125rem;
  color: #6b7280;
}

.more-options {
  padding: 0.375rem 0.625rem;
  color: #9ca3af;
  font-size: 0.8125rem;
}

/* 卡片底部 */
.card-footer-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 0.875rem;
  border-top: 1px solid #f3f4f6;
}

.card-stats {
  display: flex;
  gap: 0.5rem;
  align-items: center;
  font-size: 0.8125rem;
  color: #9ca3af;
}

.stat-separator {
  color: #d1d5db;
}

.card-actions {
  display: flex;
  gap: 0.5rem;
  position: relative;
}

/* 更多菜单 */
.more-menu {
  position: relative;
}

.more-btn {
  padding: 0.375rem 0.875rem;
  background: transparent;
  border: 1px solid #e5e7eb;
  border-radius: 4px;
  font-size: 0.8125rem;
  color: #667eea;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.more-btn:hover {
  background: #f5f7ff;
  border-color: #667eea;
}

.card-action-btn {
  padding: 0.375rem 0.875rem;
  background: transparent;
  border: 1px solid #e5e7eb;
  border-radius: 4px;
  font-size: 0.8125rem;
  color: #667eea;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.card-action-btn:hover {
  background: #f5f7ff;
  border-color: #667eea;
}

.card-action-btn.delete {
  color: #ef4444;
}

.card-action-btn.delete:hover {
  background: #fef2f2;
  border-color: #ef4444;
}

/* 旧版题库样式（保留以兼容） */
.question-card {
  border-left: 4px solid #27ae60;
}

.question-header {
  display: flex;
  gap: 0.75rem;
  align-items: center;
  margin-bottom: 1rem;
  flex-wrap: wrap;
}

.question-number {
  color: #2c3e50;
  font-weight: 600;
}

.type-badge {
  padding: 0.25rem 0.6rem;
  border-radius: 3px;
  font-size: 0.75rem;
  font-weight: 600;
  color: white;
}

.type-badge.choice {
  background: #667eea;
}

.type-badge.fill {
  background: #3498db;
}

.type-badge.essay {
  background: #e74c3c;
}

.difficulty-badge {
  padding: 0.25rem 0.6rem;
  border-radius: 3px;
  font-size: 0.75rem;
  font-weight: 600;
}

.difficulty-badge.easy {
  background: #d5f4e6;
  color: #27ae60;
}

.difficulty-badge.medium {
  background: #fef5e7;
  color: #f39c12;
}

.difficulty-badge.hard {
  background: #ffe5e5;
  color: #e74c3c;
}

.points-badge {
  padding: 0.25rem 0.6rem;
  background: #ecf0f1;
  color: #7f8c8d;
  border-radius: 3px;
  font-size: 0.75rem;
  font-weight: 600;
}

.question-content {
  margin: 0 0 0.75rem 0;
  color: #2c3e50;
  font-size: 0.95rem;
  font-weight: 500;
}

.question-options {
  margin: 1rem 0;
  padding: 0.75rem;
  background: #f8f9fa;
  border-radius: 4px;
}

.option {
  padding: 0.4rem 0;
  color: #7f8c8d;
  font-size: 0.85rem;
  line-height: 1.6;
}

.question-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 1rem;
  border-top: 1px solid #ecf0f1;
  flex-wrap: wrap;
  gap: 1rem;
}

.usage-count {
  color: #95a5a6;
  font-size: 0.85rem;
}

.question-actions {
  display: flex;
  gap: 0.75rem;
}

/* 搜索输入框样式 */
.search-input {
  flex: 1;
  min-width: 250px;
  padding: 0.75rem 1rem;
  border: 1px solid #bdc3c7;
  border-radius: 4px;
  font-size: 0.9rem;
}

.search-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

/* 模态框增强样式 */
.modal-lg {
  max-width: 700px;
}

/* 创建题目模态框样式 */
.question-create-modal {
  background: white;
  border-radius: 12px;
  width: 95%;
  max-width: 1400px;
  max-height: 90vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.question-create-modal .modal-header {
  padding: 1.5rem 2rem;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-body-split {
  display: flex;
  gap: 2rem;
  padding: 2rem;
  overflow-y: auto;
  flex: 1;
}

/* 左侧内容输入区 (70%) */
.content-input-section {
  flex: 0 0 68%;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.type-selector-bar {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 1rem;
  background: #f9fafb;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
}

.type-tabs {
  display: flex;
  gap: 0.5rem;
}

.type-tab {
  padding: 0.5rem 1rem;
  border: 1px solid #d1d5db;
  background: white;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s;
}

.type-tab:hover {
  border-color: #667eea;
  color: #667eea;
}

.type-tab.active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-color: transparent;
}

.form-section {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.section-label {
  font-weight: 600;
  color: #374151;
  font-size: 14px;
}

.large-textarea {
  width: 100%;
  padding: 1rem;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 15px;
  resize: vertical;
  font-family: inherit;
}

.large-textarea:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

/* 选项列表 */
.options-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.option-row {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem;
  background: #f9fafb;
  border-radius: 6px;
  border: 1px solid #e5e7eb;
}

.option-label {
  font-weight: 600;
  color: #6b7280;
  min-width: 30px;
}

.option-input {
  flex: 1;
  padding: 0.5rem;
  border: 1px solid #d1d5db;
  border-radius: 4px;
  background: white;
}

.checkbox-wrapper {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  padding: 0.25rem 0.75rem;
  border-radius: 4px;
  background: white;
  border: 1px solid #d1d5db;
  white-space: nowrap;
}

.checkbox-wrapper:hover {
  background: #f3f4f6;
}

.checkbox-label {
  font-size: 13px;
  color: #6b7280;
}

.answer-radio,
.answer-checkbox {
  margin: 0;
  cursor: pointer;
}

.remove-option-btn {
  padding: 0.25rem 0.5rem;
  border: none;
  background: #fee2e2;
  color: #dc2626;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  line-height: 1;
}

.remove-option-btn:hover {
  background: #fecaca;
}

.add-option-btn {
  align-self: flex-start;
  padding: 0.5rem 1rem;
  border: 1px dashed #9ca3af;
  background: white;
  border-radius: 6px;
  cursor: pointer;
  color: #6b7280;
  font-size: 14px;
}

.add-option-btn:hover {
  border-color: #667eea;
  color: #667eea;
  background: #f9fafb;
}

/* 判断题选项 */
.judge-options {
  display: flex;
  gap: 1rem;
}

.radio-option {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  cursor: pointer;
  background: white;
  transition: all 0.2s;
}

.radio-option:hover {
  border-color: #667eea;
  background: #f9fafb;
}

.radio-option input[type="radio"] {
  margin: 0;
  cursor: pointer;
}

.radio-option input[type="radio"]:checked + span {
  color: #667eea;
  font-weight: 600;
}

/* 右侧配置区 (30%) */
.config-section {
  flex: 0 0 28%;
  background: #f9fafb;
  padding: 1.5rem;
  border-radius: 12px;
  border: 1px solid #e5e7eb;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.config-title {
  font-size: 16px;
  font-weight: 600;
  color: #1f2937;
  margin: 0;
  padding-bottom: 1rem;
  border-bottom: 2px solid #e5e7eb;
}

.config-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.config-label {
  font-weight: 600;
  color: #374151;
  font-size: 13px;
}

.slider-container {
  padding: 0.5rem 0;
}

.difficulty-slider {
  width: 100%;
  height: 6px;
  border-radius: 3px;
  background: linear-gradient(to right, #10b981, #f59e0b, #ef4444);
  outline: none;
  -webkit-appearance: none;
}

.difficulty-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: white;
  border: 3px solid #667eea;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.difficulty-slider::-moz-range-thumb {
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: white;
  border: 3px solid #667eea;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.slider-value {
  margin-top: 0.5rem;
  padding: 0.5rem;
  background: white;
  border-radius: 6px;
  text-align: center;
  font-weight: 600;
  color: #667eea;
  font-size: 14px;
}

.hint-text {
  font-size: 12px;
  color: #9ca3af;
  font-style: italic;
}

.full-width-select {
  width: 100%;
}

/* 创建新项按钮 */
.create-new-btn {
  margin-top: 0.5rem;
  width: 100%;
  padding: 0.5rem;
  border: 1px dashed #9ca3af;
  background: white;
  border-radius: 6px;
  cursor: pointer;
  color: #667eea;
  font-size: 13px;
  font-weight: 500;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.25rem;
}

.create-new-btn:hover {
  border-color: #667eea;
  background: #f3f4f6;
  transform: translateY(-1px);
}

/* 模态框底部 */
.modal-footer {
  padding: 1rem 2rem;
  border-top: 1px solid #e5e7eb;
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  background: #f9fafb;
}

.btn-cancel {
  padding: 0.75rem 1.5rem;
  border: 1px solid #d1d5db;
  background: white;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  color: #6b7280;
  transition: all 0.2s;
}

.btn-cancel:hover {
  background: #f3f4f6;
  border-color: #9ca3af;
}

.btn-secondary {
  padding: 0.75rem 1.5rem;
  border: 1px solid #667eea;
  background: white;
  color: #667eea;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.2s;
}

.btn-secondary:hover {
  background: #f3f4f6;
}

.btn-primary {
  padding: 0.75rem 1.5rem;
  border: none;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.2s;
}

.btn-primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

/* 题目详情展示样式 */
.detail-section {
  margin-top: 1rem;
  padding: 1rem;
  background: #f9fafb;
  border-radius: 6px;
  border: 1px solid #e5e7eb;
}

.options-preview .option-item {
  padding: 0.5rem 0;
  color: #374151;
}

.options-preview .correct-answer {
  color: #059669;
  font-weight: 600;
}

.answer-mark {
  margin-left: 0.5rem;
  color: #10b981;
  font-weight: bold;
}

.judge-answer,
.fill-answer {
  padding: 0.75rem;
  background: white;
  border-radius: 4px;
  color: #374151;
}

.essay-answer {
  padding: 0.75rem;
  background: white;
  border-radius: 4px;
}

.essay-answer strong {
  display: block;
  margin-bottom: 0.5rem;
  color: #1f2937;
}

.essay-answer p {
  margin: 0;
  color: #374151;
  line-height: 1.6;
}


.form-group {
  margin-bottom: 1.5rem;
}

.form-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #374151;
  font-weight: 600;
  margin-bottom: 0.625rem;
  font-size: 0.9375rem;
}

.form-label i {
  color: #667eea;
  font-size: 1rem;
}

.form-label .required {
  color: #ef4444;
  margin-left: 0.125rem;
}

.form-group label {
  display: block;
  color: #2c3e50;
  font-weight: 600;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
}

.form-input,
.form-textarea {
  width: 100%;
  padding: 0.875rem 1rem;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 0.9375rem;
  font-family: inherit;
  transition: all 0.2s;
  background: #fafafa;
}

.form-input:hover,
.form-textarea:hover {
  border-color: #9ca3af;
  background: white;
}

.form-input:focus,
.form-textarea:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
  background: white;
}

.form-textarea {
  resize: vertical;
  min-height: 90px;
  line-height: 1.6;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.option-input {
  display: flex;
  gap: 0.5rem;
  align-items: center;
  margin-bottom: 0.5rem;
}

.option-input .form-input {
  flex: 1;
}

.option-input label {
  font-size: 0.75rem;
}

.modal-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 2rem;
  padding-top: 1.5rem;
  border-top: 1px solid #e5e7eb;
}

.btn-cancel,
.btn-submit {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.75rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  font-size: 0.9375rem;
  transition: all 0.2s;
}

.btn-cancel {
  background: #f3f4f6;
  color: #6b7280;
  border: 1px solid #e5e7eb;
}

.btn-cancel:hover {
  background: #e5e7eb;
  color: #374151;
}

.btn-submit {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
}

.btn-submit:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.filter-tabs {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

@media (max-width: 768px) {
  .form-row {
    grid-template-columns: 1fr;
  }

  .thread-header {
    flex-direction: column;
  }

  .grades-table {
    font-size: 0.8rem;
  }

  .grades-table th,
  .grades-table td {
    padding: 0.5rem;
  }
}

/* 章节概览样式 */
.sections-overview {
  width: 100%;
  padding: 0;
}

.overview-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0;
  padding: 1.5rem 2rem;
  background: #f9fafb;
  border-bottom: 1px solid #e5e7eb;
}

.overview-header h2 {
  margin: 0;
  font-size: 1.5rem;
  color: #2c3e50;
}

.header-actions {
  display: flex;
  align-items: center;
}

.sections-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding: 1.5rem 2rem;
}

.section-card {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  overflow: hidden;
  transition: all 0.3s;
}

.section-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.section-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.25rem 1.5rem;
  background: #f7f8fa;
  cursor: pointer;
  transition: all 0.2s;
}

.section-card-header:hover {
  background: #ebeef5;
}

.section-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex: 1;
}

.expand-icon {
  color: #909399;
  transition: transform 0.3s;
  font-size: 0.8rem;
}

.expand-icon.expanded {
  transform: rotate(90deg);
}

.section-info h3 {
  margin: 0;
  font-size: 1.1rem;
  color: #2c3e50;
  font-weight: 600;
}

.section-meta {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.lesson-count {
  color: #909399;
  font-size: 0.9rem;
}

.section-lessons {
  padding: 0.5rem;
  background: white;
}

.lesson-card {
  display: flex;
  align-items: center;
  padding: 1rem 1.5rem;
  border-radius: 6px;
  transition: all 0.2s;
  gap: 1rem;
}

.lesson-card:hover {
  background: #f5f7fa;
}

.lesson-index {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background: #e8eaed;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.9rem;
  font-weight: 600;
  color: #606266;
}

.lesson-icon {
  font-size: 1.3rem;
}

.lesson-content {
  flex: 1;
  cursor: pointer;
}

.lesson-name {
  font-size: 1rem;
  color: #2c3e50;
  margin-bottom: 0.25rem;
  font-weight: 500;
}

.lesson-meta {
  color: #909399;
  font-size: 0.85rem;
}

.lesson-actions {
  display: flex;
  gap: 0.5rem;
  opacity: 0;
  transition: opacity 0.2s;
}

.lesson-card:hover .lesson-actions {
  opacity: 1;
}

.add-lesson-btn {
  padding: 0.75rem 1.5rem;
  text-align: center;
  border-top: 1px dashed #dcdfe6;
  margin-top: 0.5rem;
}

/* 管理模块样式 */
.management-container {
  padding: 1rem 0.5rem 1rem 20px;
}

.management-tabs {
  background: white;
}

.management-tabs ::v-deep .el-tabs__header {
  margin: 0 0 1.5rem;
  border-bottom: 2px solid #e5e7eb;
}

.management-tabs ::v-deep .el-tabs__item {
  font-size: 15px;
  font-weight: 500;
  padding: 0 20px;
  height: 50px;
  line-height: 50px;
}

.management-tabs ::v-deep .el-tabs__active-bar {
  height: 3px;
  background: #5B4FE0;
}

.tab-content {
  padding: 0;
}

/* 教务组织样式 */
.term-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.term-card {
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 1.5rem;
}

.term-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #e5e7eb;
}

.term-info {
  flex: 1;
}

.term-name {
  font-size: 18px;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 0.5rem 0;
}

.term-meta {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.term-date {
  color: #6b7280;
  font-size: 14px;
}

.term-actions {
  display: flex;
  gap: 0.75rem;
  align-items: center;
}

.action-btn.small {
  padding: 0.5rem 1rem;
  font-size: 14px;
}

.class-table {
  background: white;
  border-radius: 6px;
  overflow: hidden;
}

.class-table table {
  width: 100%;
  border-collapse: collapse;
}

.class-table thead {
  background: #f3f4f6;
}

.class-table th {
  padding: 0.75rem 1rem;
  text-align: left;
  font-weight: 600;
  color: #374151;
  font-size: 14px;
  border-bottom: 1px solid #e5e7eb;
}

.class-table td {
  padding: 0.875rem 1rem;
  border-bottom: 1px solid #f3f4f6;
  color: #4b5563;
  font-size: 14px;
}

.class-table tbody tr:hover {
  background: #f9fafb;
}

.class-table td .action-link {
  margin-right: 0.75rem;
}

.no-classes {
  text-align: center;
  padding: 2rem;
  background: white;
  border-radius: 6px;
  color: #9ca3af;
  font-size: 14px;
}

/* 课程管理样式 */
.settings-section {
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
}

.section-title {
  font-size: 16px;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 1.5rem 0;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid #e5e7eb;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group:last-child {
  margin-bottom: 0;
}

.form-group label {
  display: block;
  font-weight: 500;
  color: #374151;
  margin-bottom: 0.5rem;
  font-size: 14px;
}

.form-input {
  width: 100%;
  padding: 0.625rem 0.875rem;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 14px;
  transition: all 0.2s;
}

.form-input[type="date"] {
  padding: 0.625rem 0.75rem;
  cursor: pointer;
  min-height: 42px;
}

.form-input[type="date"]::-webkit-calendar-picker-indicator {
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  transition: background 0.2s;
}

.form-input[type="date"]::-webkit-calendar-picker-indicator:hover {
  background: #f3f4f6;
}

.form-input:focus {
  outline: none;
  border-color: #5B4FE0;
  box-shadow: 0 0 0 3px rgba(91, 79, 224, 0.1);
}

.price-inputs {
  display: flex;
  gap: 1rem;
}

.input-wrapper {
  flex: 1;
  position: relative;
  display: flex;
  align-items: center;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  overflow: hidden;
}

.input-prefix {
  background: #f3f4f6;
  padding: 0.625rem 0.875rem;
  color: #6b7280;
  font-size: 14px;
  white-space: nowrap;
  border-right: 1px solid #d1d5db;
}

.input-wrapper input {
  flex: 1;
  border: none;
  padding: 0.625rem 0.875rem;
  font-size: 14px;
}

.input-wrapper input:focus {
  outline: none;
}

.switch-group {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.form-tip {
  color: #9ca3af;
  font-size: 13px;
  margin-top: 0.5rem;
  display: block;
}

.radio-group {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 0.5rem;
}

.radio-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
}

.radio-item input[type="radio"] {
  width: 16px;
  height: 16px;
  cursor: pointer;
}

.save-bar {
  text-align: center;
  padding-top: 1rem;
}

/* 财务订单样式 */
.finance-overview {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.overview-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 8px;
  padding: 1.5rem;
  color: white;
}

.overview-label {
  font-size: 14px;
  opacity: 0.9;
  margin-bottom: 0.5rem;
}

.overview-value {
  font-size: 28px;
  font-weight: 700;
}

.orders-section {
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 1.5rem;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  background: white;
  border-radius: 6px;
  overflow: hidden;
}

.data-table thead {
  background: #f3f4f6;
}

.data-table th {
  padding: 0.75rem 1rem;
  text-align: left;
  font-weight: 600;
  color: #374151;
  font-size: 14px;
  border-bottom: 1px solid #e5e7eb;
}

.data-table td {
  padding: 0.875rem 1rem;
  border-bottom: 1px solid #f3f4f6;
  color: #4b5563;
  font-size: 14px;
}

.data-table tbody tr:hover {
  background: #f9fafb;
}

.amount-text {
  color: #dc2626;
  font-weight: 600;
}

.status-badge.paid {
  background: #d1fae5;
  color: #065f46;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
}

.status-badge.pending {
  background: #fef3c7;
  color: #92400e;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
}

.status-badge.refunded {
  background: #e5e7eb;
  color: #4b5563;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
}

.status-badge.active {
  background: #d1fae5;
  color: #065f46;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
}

.status-badge.upcoming {
  background: #dbeafe;
  color: #1e40af;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
}

.status-badge.ended {
  background: #e5e7eb;
  color: #4b5563;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
}

/* 输入框带按钮样式 */
.input-with-button {
  display: flex;
  gap: 0.5rem;
}

.input-with-button .form-input {
  flex: 1;
}

.btn-generate {
  padding: 0.625rem 1.25rem;
  background: #5B4FE0;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
}

.btn-generate:hover {
  background: #4A3FD0;
}

/* 班期标题可点击样式 */
.term-name.clickable {
  cursor: pointer;
  transition: color 0.2s;
}

.term-name.clickable:hover {
  color: #5B4FE0;
}

/* 课程管理样式 */
.course-management-content {
  background: #f5f7fa;
  padding: 20px;
  padding-top: 80px;
  width: 100%;
  box-sizing: border-box;
  position: relative;
}

/* 右上角发布按钮 */
.page-top-actions {
  position: absolute;
  top: 20px;
  right: 20px;
  z-index: 10;
}

.cm-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 20px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  max-width: 100%;
}

.cm-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 12px;
  border-bottom: 2px solid #e5e7eb;
}

.cm-card-title {
  font-size: 18px;
  font-weight: 600;
  color: #1f2937;
  margin: 0;
}

.cm-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.cm-form-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.cm-label {
  font-size: 14px;
  font-weight: 600;
  color: #374151;
}

.cm-label-large {
  font-size: 16px;
  font-weight: 600;
  color: #1f2937;
}

.cm-price-input {
  display: flex;
  align-items: center;
  gap: 8px;
}

.cm-unit {
  color: #6b7280;
  font-size: 14px;
}

.cm-hint {
  font-size: 12px;
  color: #9ca3af;
  margin-top: 4px;
}

/* 发布开关特殊样式 */
.cm-publish-switch {
  flex-direction: row !important;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
  border-radius: 8px;
  border: 2px solid #667eea30;
}

.switch-left {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.switch-hint {
  font-size: 13px;
  color: #6b7280;
}

/* 分割线 */
.cm-divider {
  height: 1px;
  background: #e5e7eb;
  margin: 10px 0;
}

/* 封面上传 */
.cm-upload-area {
  width: fit-content;
}

.cover-uploader >>> .el-upload {
  border: 2px dashed #d1d5db;
  border-radius: 8px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: all 0.3s;
}

.cover-uploader >>> .el-upload:hover {
  border-color: #667eea;
}

.cover-preview {
  width: 300px;
  height: 200px;
  object-fit: cover;
  display: block;
}

.cover-upload-placeholder {
  width: 300px;
  height: 200px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: #f9fafb;
}

.cover-upload-placeholder i {
  font-size: 48px;
  color: #9ca3af;
  margin-bottom: 10px;
}

.upload-text {
  font-size: 14px;
  color: #6b7280;
  margin-bottom: 4px;
}

.upload-hint {
  font-size: 12px;
  color: #9ca3af;
}

/* 只读模式封面 */
.cover-preview-readonly {
  width: 300px;
  height: 200px;
  object-fit: cover;
  display: block;
  border-radius: 8px;
}

.cover-placeholder-readonly {
  width: 300px;
  height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f3f4f6;
  color: #9ca3af;
  font-size: 14px;
  border-radius: 8px;
  border: 2px dashed #d1d5db;
}

/* 日期范围 */
.cm-date-range {
  display: flex;
  align-items: center;
  gap: 10px;
}

.date-separator {
  color: #6b7280;
  font-size: 14px;
}

/* 操作按钮 */
.cm-form-actions {
  display: flex;
  justify-content: flex-start;
  padding-top: 10px;
}

/* 价格设置行样式 */
.price-settings-row {
  display: flex;
  gap: 1rem;
  align-items: flex-end;
}

.price-settings-row .form-group {
  flex: 1;
  margin-bottom: 0;
}

/* 筛选栏样式 */
.filter-bar {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 1.5rem;
  padding: 1rem;
  background: #f9fafb;
  border-radius: 6px;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.filter-bar label {
  font-weight: 500;
  color: #374151;
  font-size: 14px;
  white-space: nowrap;
}

.filter-select {
  padding: 0.5rem 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 14px;
  background: white;
  cursor: pointer;
  min-width: 150px;
}

.filter-select:focus {
  outline: none;
  border-color: #5B4FE0;
}

/* 班期详情模态框样式 */
.detail-section {
  margin-bottom: 2rem;
}

.detail-section:last-child {
  margin-bottom: 0;
}

.detail-title {
  font-size: 16px;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 1rem 0;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #e5e7eb;
}

.detail-row {
  display: flex;
  gap: 2rem;
  margin-bottom: 0.75rem;
}

.detail-item {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.detail-item.full-width {
  flex: 1 1 100%;
}

.detail-item label {
  font-weight: 500;
  color: #6b7280;
  font-size: 14px;
  white-space: nowrap;
}

.detail-item span {
  color: #1f2937;
  font-size: 14px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
}

.stat-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 8px;
  padding: 1.25rem;
  color: white;
  text-align: center;
}

.stat-label {
  font-size: 13px;
  opacity: 0.9;
  margin-bottom: 0.5rem;
}

.stat-value {
  font-size: 24px;
  font-weight: 700;
}

.detail-table {
  width: 100%;
  border-collapse: collapse;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  overflow: hidden;
}

.detail-table thead {
  background: #f3f4f6;
}

.detail-table th {
  padding: 0.75rem 1rem;
  text-align: left;
  font-weight: 600;
  color: #374151;
  font-size: 14px;
  border-bottom: 1px solid #e5e7eb;
}

.detail-table td {
  padding: 0.75rem 1rem;
  border-bottom: 1px solid #f3f4f6;
  color: #4b5563;
  font-size: 14px;
}

.detail-table tbody tr:last-child td {
  border-bottom: none;
}

/* ========== 三级导航样式 ========== */
/* 容器 */
.academic-content {
  width: 100%;
  padding-right: 20px;
}

/* Level 1: 班期概览 */
.term-overview {
  padding: 1rem 0;
}

.term-cards-container {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.term-wide-card {
  width: 100%;
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  transition: all 0.3s;
  overflow: hidden;
}

.term-wide-card:hover {
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  transform: translateY(-2px);
}

.card-content {
  display: flex;
  align-items: center;
  padding: 2rem;
  gap: 2rem;
  cursor: pointer;
}

.card-left {
  flex: 0 0 200px;
}

.card-description {
  margin-top: 0.75rem;
  padding: 0.5rem 0.75rem;
  background: #f9fafb;
  border-left: 3px solid #667eea;
  border-radius: 4px;
  font-size: 0.875rem;
  color: #6b7280;
  line-height: 1.5;
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
}

.card-description i {
  color: #667eea;
  margin-top: 2px;
  flex-shrink: 0;
}

.term-wide-card h3 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 0.5rem;
}

.card-meta {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-top: 0.5rem;
  flex-wrap: wrap;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  color: #6b7280;
  font-size: 0.875rem;
}

.meta-item i {
  font-size: 0.875rem;
}

.status-tag {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
  white-space: nowrap;
  display: inline-flex;
  align-items: center;
}

.status-tag.upcoming {
  background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
  color: #1e40af;
  border: 1px solid #93c5fd;
}

.status-tag.active {
  background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
  color: #065f46;
  border: 1px solid #6ee7b7;
}

.status-tag.ended {
  background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%);
  color: #6b7280;
  border: 1px solid #d1d5db;
}

.term-wide-card .term-time {
  color: #6b7280;
  font-size: 0.875rem;
}

.card-center {
  flex: 1;
  display: flex;
  gap: 2rem;
  padding-left: 2rem;
  border-left: 1px solid #e5e7eb;
}

.stat-item {
  text-align: center;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 600;
  color: #3b82f6;
  margin-bottom: 0.25rem;
}

.stat-label {
  color: #6b7280;
  font-size: 0.875rem;
}

.card-right {
  flex: 0 0 auto;
  display: flex;
  gap: 0.75rem;
  justify-content: flex-end;
  align-items: center;
}

.enter-btn {
  padding: 0.5rem 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.875rem;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.2s;
  white-space: nowrap;
}

.enter-btn:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 8px rgba(102, 126, 234, 0.3);
}

.action-btn.edit-btn {
  padding: 0.5rem 1rem;
  background: white;
  color: #667eea;
  border: 1px solid #667eea;
  white-space: nowrap;
}

.action-btn.edit-btn:hover {
  background: #f5f3ff;
  border-color: #764ba2;
  color: #764ba2;
}

/* Level 2: 班级管理 */
.class-management {
  padding: 0;
}

/* 紧凑型面包屑导航 */
.breadcrumb-bar-compact {
  margin-bottom: 0;
  padding: 0.5rem 0;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

/* 左右布局容器 */
.class-sidebar-layout {
  display: flex;
  gap: 0;
  height: calc(100vh - 200px);
  min-height: 600px;
}

/* 左侧班级目录 */
.class-sidebar {
  width: 280px;
  border-right: 1px solid #e5e7eb;
  background: #f9fafb;
  display: flex;
  flex-direction: column;
}

.sidebar-header {
  padding: 1rem 1.25rem;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: white;
}

.sidebar-header h4 {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
  color: #1f2937;
}

.add-class-btn {
  width: 32px;
  height: 32px;
  border-radius: 6px;
  border: none;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.add-class-btn:hover {
  transform: scale(1.1);
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
}

.sidebar-content {
  flex: 1;
  overflow-y: auto;
  padding: 0.5rem;
}

.sidebar-content::-webkit-scrollbar {
  width: 6px;
}

.sidebar-content::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.sidebar-content::-webkit-scrollbar-thumb {
  background: #d1d5db;
  border-radius: 3px;
}

.sidebar-content::-webkit-scrollbar-thumb:hover {
  background: #9ca3af;
}

.class-item {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  padding: 0.875rem;
  margin-bottom: 0.5rem;
  cursor: move;
  transition: all 0.2s;
}

.class-item:hover {
  border-color: #667eea;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.class-item.active {
  background: linear-gradient(135deg, #f5f3ff 0%, #ede9fe 100%);
  border-color: #667eea;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.15);
}

.class-item-header {
  display: flex;
  align-items: center;
  margin-bottom: 0.5rem;
  gap: 0.5rem;
}

.class-draggable-area {
  min-height: 50px;
}

.class-item-name {
  font-weight: 600;
  color: #1f2937;
  font-size: 0.9375rem;
}

.class-item-more {
  color: #6b7280;
  cursor: pointer;
  padding: 0.25rem;
  border-radius: 4px;
  transition: all 0.2s;
  margin-left: auto;
}

.class-item-more:hover {
  background: #f3f4f6;
  color: #374151;
}

.class-item-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.8125rem;
  color: #6b7280;
}

.info-text {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.class-item-code {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.5rem 0;
  margin-top: 0.5rem;
  border-top: 1px solid #f3f4f6;
  font-size: 0.8125rem;
}

.code-label {
  color: #9ca3af;
}

.code-value {
  font-family: 'Courier New', monospace;
  font-weight: 600;
  color: #667eea;
  background: #eef2ff;
  padding: 0.125rem 0.5rem;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
}

.code-value:hover {
  background: #667eea;
  color: white;
}

.copy-icon {
  color: #9ca3af;
  cursor: pointer;
  font-size: 1rem;
  transition: color 0.2s;
}

.copy-icon:hover {
  color: #667eea;
}

.invite-code-mini {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.25rem 0.5rem;
  background: #f3f4f6;
  border-radius: 4px;
  font-size: 0.75rem;
  transition: all 0.2s;
}

.invite-code-mini:hover {
  background: #667eea;
  color: white;
}

.invite-code-mini.disabled {
  cursor: not-allowed;
  opacity: 0.5;
}

.invite-code-mini.disabled:hover {
  background: #f3f4f6;
  color: #6b7280;
}

.sidebar-empty {
  text-align: center;
  padding: 3rem 1rem;
  color: #9ca3af;
}

.sidebar-empty i {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
  opacity: 0.5;
}

.sidebar-empty p {
  font-size: 0.875rem;
  margin: 0;
}

/* 右侧内容区 */
.class-content-area {
  flex: 1;
  background: white;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
}

.content-placeholder {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #9ca3af;
}

.content-placeholder i {
  font-size: 4rem;
  margin-bottom: 1rem;
  opacity: 0.3;
}

.content-placeholder p {
  font-size: 0.9375rem;
  margin: 0;
}

.member-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 0.75rem 1.5rem 1.5rem 1.5rem;
}

.member-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.member-title {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
}

.close-detail-btn {
  width: 32px;
  height: 32px;
  border: 1px solid #e5e7eb;
  background: white;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #6b7280;
  transition: all 0.2s;
}

.close-detail-btn:hover {
  border-color: #667eea;
  color: #667eea;
  background: #f5f3ff;
}

.breadcrumb-bar {
  margin-bottom: 1.5rem;
  padding: 1rem 0;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.breadcrumb-item {
  color: #6b7280;
  font-size: 0.875rem;
}

.breadcrumb-item.clickable {
  color: #3b82f6;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.25rem;
  transition: color 0.2s;
}

.breadcrumb-item.clickable:hover {
  color: #2563eb;
  text-decoration: underline;
}

.breadcrumb-item.current {
  color: #374151;
  font-weight: 500;
}

.breadcrumb-divider {
  color: #9ca3af;
}

.class-cards-flow {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(500px, 1fr));
  gap: 1.5rem;
}

.class-card {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 1.5rem;
  transition: all 0.2s;
}

.class-card:hover {
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}

.class-card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.class-name-section {
  flex: 1;
}

.class-name {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 0.75rem;
}

.class-actions {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.class-card-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1f2937;
}

.class-card-body {
  margin-bottom: 1rem;
}

.invite-code-section {
  margin-bottom: 1rem;
}

.invite-code-label {
  color: #6b7280;
  font-size: 0.875rem;
  margin-bottom: 0.5rem;
}

.invite-code-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
  font-weight: 500;
  font-size: 1rem;
  letter-spacing: 0.05em;
}

.invite-code-badge:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 8px rgba(102, 126, 234, 0.3);
}

.invite-code-badge i {
  font-size: 1rem;
}

.class-card-body {
  margin-bottom: 1rem;
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 0;
  color: #6b7280;
  font-size: 0.875rem;
}

.info-label {
  font-weight: 500;
}

.info-value {
  color: #374151;
  font-weight: 600;
}

.enrollment-info {
  color: #6b7280;
  font-size: 0.875rem;
  margin-bottom: 0.5rem;
}

.enrollment-count {
  font-weight: 600;
  color: #3b82f6;
}

.class-card-footer {
  display: flex;
  gap: 0.75rem;
  padding-top: 1rem;
  border-top: 1px solid #f3f4f6;
}

/* Level 3: 成员管理页面 */
.member-management {
  padding: 1rem 0;
}

.member-stats-cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  transition: all 0.2s;
}

.stat-card:hover {
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  transform: translateY(-2px);
}

.stat-icon {
  width: 3rem;
  height: 3rem;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
}

.stat-info {
  flex: 1;
}

.stat-info .stat-label {
  color: #6b7280;
  font-size: 0.875rem;
  margin-bottom: 0.25rem;
}

.stat-info .stat-value {
  font-size: 1.75rem;
  font-weight: 600;
  color: #1f2937;
}

.member-table-container {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  overflow: hidden;
}

.member-table {
  width: 100%;
  border-collapse: collapse;
}

.member-table thead {
  background: #f9fafb;
}

.member-table th {
  padding: 1rem;
  text-align: left;
  font-weight: 600;
  color: #374151;
  font-size: 0.875rem;
  border-bottom: 2px solid #e5e7eb;
}

.member-table td {
  padding: 1rem;
  border-bottom: 1px solid #f3f4f6;
  color: #4b5563;
  font-size: 0.875rem;
}

.member-table tbody tr:hover {
  background: #f9fafb;
}

.member-table tbody tr:last-child td {
  border-bottom: none;
}

.status-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 500;
}

.status-badge.success {
  background: #d1fae5;
  color: #065f46;
}

.action-btn.danger-btn {
  color: #ef4444;
  background: #fef2f2;
  border: 1px solid #fecaca;
}

.action-btn.danger-btn:hover {
  background: #fee2e2;
  border-color: #fca5a5;
}

.action-btn.small {
  padding: 0.375rem 0.75rem;
  font-size: 0.8125rem;
}
/* ========== 三级导航样式结束 ========== */
</style>
```

