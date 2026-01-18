<template>
  <div class="teacher-course-detail">
    <!-- 顶部Logo区域 -->
    <header class="page-logo">
      <h1>EduMaster</h1>
    </header>

    <!-- 左侧固定导航栏 -->
    <aside class="sidebar-fixed">
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
            <div class="personal-filter">
              <label class="checkbox-label">
                <input 
                  type="checkbox" 
                  v-model="showMyThreadsOnly"
                  class="filter-checkbox"
                >
                <span>我发布的话题</span>
              </label>
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
                  <div v-if="canManageThread(thread)" class="thread-manage">
                    <a class="manage-link edit" @click.stop="editThread(thread.id)">编辑</a>
                    <a class="manage-link delete" @click.stop="deleteThread(thread.id)">删除</a>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div v-else class="no-data">
            <p>暂无话题</p>
            <p class="hint">点击"发布话题"按钮创建第一个讨论</p>
          </div>
        </section>

        <!-- 成绩管理模块 -->
        <section v-if="activeModule === 'grades'" class="module-section">
          <div class="module-header">
            <h2>成绩管理</h2>
            <div class="action-buttons">
              <button @click="downloadGradeReport" class="action-btn secondary-btn">
                📊 导出成绩单
              </button>
              <button @click="showGradeStats = !showGradeStats" class="action-btn secondary-btn">
                📈 统计分析
              </button>
            </div>
          </div>

          <!-- 成绩统计卡片 -->
          <div v-if="showGradeStats" class="stats-cards">
            <div class="stat-card">
              <span class="stat-label">平均分</span>
              <span class="stat-value">{{ averageGrade.toFixed(1) }}</span>
            </div>
            <div class="stat-card">
              <span class="stat-label">最高分</span>
              <span class="stat-value">{{ maxGrade }}</span>
            </div>
            <div class="stat-card">
              <span class="stat-label">最低分</span>
              <span class="stat-value">{{ minGrade }}</span>
            </div>
            <div class="stat-card">
              <span class="stat-label">及格率</span>
              <span class="stat-value">{{ passRate }}%</span>
            </div>
          </div>

          <!-- 筛选区 -->
          <div class="filter-section">
            <div class="filter-group">
              <label>班期筛选：</label>
              <select v-model="gradeFilter.termId" class="filter-select" @change="gradeFilter.class = ''">
                <option value="">全部班期</option>
                <option v-for="term in terms" :key="term.id" :value="term.id">{{ term.name }}</option>
              </select>
            </div>

            <div class="filter-group">
              <label>班级筛选：</label>
              <select v-model="gradeFilter.class" class="filter-select">
                <option value="">全部班级</option>
                <option 
                  v-for="cls in (gradeFilter.termId ? getClassesByTerm(gradeFilter.termId) : classes)" 
                  :key="cls.id" 
                  :value="cls.name"
                >
                  {{ cls.name }}
                </option>
              </select>
            </div>

            <div class="filter-group">
              <label>成绩筛选：</label>
              <div class="status-filter-btns">
                <button
                  v-for="type in ['全部', '优秀', '良好', '及格', '不及格']"
                  :key="type"
                  :class="['filter-btn', { active: gradeFilter.type === type }]"
                  @click="gradeFilter.type = type"
                >
                  {{ type }}
                </button>
              </div>
            </div>
          </div>

          <!-- 成绩表格 -->
          <div class="table-section">
            <table class="grades-table">
              <thead>
                <tr>
                  <th>序号</th>
                  <th>学生姓名</th>
                  <th>班级</th>
                  <th>考试成绩</th>
                  <th>作业成绩</th>
                  <th>总成绩</th>
                  <th>等级</th>
                  <th>操作</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(record, idx) in filteredGradeRecords" :key="record.id">
                  <td>{{ idx + 1 }}</td>
                  <td>{{ record.studentName }}</td>
                  <td>{{ record.className }}</td>
                  <td>{{ record.examGrade }}</td>
                  <td>{{ record.homeworkGrade }}</td>
                  <td class="total-grade">{{ record.totalGrade }}</td>
                  <td>
                    <span :class="['grade-badge', record.level]">{{ record.level }}</span>
                  </td>
                  <td>
                    <button @click="editStudentGrade(record)" class="action-link">详情</button>
                    <button @click="deleteGradeRecord(record.id)" class="action-link danger-action">删除</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <div v-if="filteredGradeRecords.length === 0" class="no-data">
            <p>暂无成绩数据</p>
          </div>
        </section>

        <!-- 题库模块 -->
        <section v-if="activeModule === 'questionBank'" class="module-section">
          <div class="module-header">
            <h2>题库管理</h2>
            <div class="action-buttons">
              <button @click="showQuestionModal = true" class="action-btn primary-btn">
                ➕ 添加题目
              </button>
              <button @click="importQuestions" class="action-btn secondary-btn">
                📥 批量导入
              </button>
              <button @click="exportQuestions" class="action-btn secondary-btn">
                📤 批量导出
              </button>
            </div>
          </div>

          <!-- 筛选区 -->
          <div class="filter-section">
            <input 
              v-model="questionSearch"
              type="text"
              placeholder="搜索题目内容..."
              class="search-input"
            >
            <div class="filter-group">
              <label>题型：</label>
              <select v-model="questionFilter.type" class="filter-select">
                <option value="">全部题型</option>
                <option value="choice">选择题</option>
                <option value="fill">填空题</option>
                <option value="essay">简答题</option>
              </select>
            </div>

            <div class="filter-group">
              <label>难度：</label>
              <select v-model="questionFilter.difficulty" class="filter-select">
                <option value="">全部难度</option>
                <option value="easy">简单</option>
                <option value="medium">中等</option>
                <option value="hard">困难</option>
              </select>
            </div>
          </div>

          <!-- 题目列表 -->
          <div v-if="filteredQuestions.length > 0" class="list-section">
            <div v-for="(question, idx) in filteredQuestions" :key="question.id" class="item-card question-card">
              <div class="question-header">
                <span class="question-number">第 {{ idx + 1 }} 题</span>
                <span :class="['type-badge', question.type]">{{ getQuestionTypeLabel(question.type) }}</span>
                <span :class="['difficulty-badge', question.difficulty]">{{ getDifficultyLabel(question.difficulty) }}</span>
                <span class="points-badge">{{ question.points }} 分</span>
              </div>

              <h4 class="question-content">{{ question.content }}</h4>

              <div v-if="question.type === 'choice'" class="question-options">
                <div v-for="(option, optIdx) in question.options" :key="optIdx" class="option">
                  {{ String.fromCharCode(65 + optIdx) }}. {{ option }}
                </div>
              </div>

              <div class="question-footer">
                <span class="usage-count">使用次数: {{ question.usageCount }}</span>
                <div class="question-actions">
                  <button @click="editQuestion(question)" class="action-link">编辑</button>
                  <button @click="previewQuestion(question)" class="action-link">预览</button>
                  <button @click="deleteQuestion(question.id)" class="action-link danger-action">删除</button>
                </div>
              </div>
            </div>
          </div>

          <div v-else class="no-data">
            <p>暂无题目数据</p>
          </div>
        </section>

        <!-- 班期管理模块 -->
        <section v-if="activeModule === 'terms'" class="module-section">
          <div class="module-header">
            <h2>班期管理</h2>
            <div class="action-buttons">
              <button @click="showTermModal = true" class="action-btn primary-btn">
                ➕ 新建班期
              </button>
            </div>
          </div>

          <div v-if="terms.length > 0" class="list-section">
            <div v-for="term in terms" :key="term.id" class="item-card term-card">
              <div class="item-header">
                <h3 class="item-title">{{ term.name }}</h3>
                <span :class="['status-badge', term.status]">{{ getTermStatusText(term.status) }}</span>
              </div>
              
              <div class="item-info">
                <div class="info-row">
                  <strong>开课时间：</strong>{{ term.startDate }} ~ {{ term.endDate }}
                </div>
                <div class="info-row">
                  <strong>班级数量：</strong>{{ term.classCount }} 个班级
                </div>
                <div class="info-row">
                  <strong>学生人数：</strong>{{ term.studentCount }} 人
                </div>
                <div class="info-row">
                  <strong>描述：</strong>{{ term.description }}
                </div>
              </div>

              <div class="item-actions">
                <button @click="editTerm(term)" class="action-link">
                  ✏️ 编辑
                </button>
                <button @click="viewTermClasses(term)" class="action-link primary-action">
                  👥 查看班级
                </button>
                <button @click="deleteTerm(term.id)" class="action-link danger-action">
                  🗑️ 删除
                </button>
              </div>
            </div>
          </div>

          <div v-else class="no-data">
            <p>暂无班期数据</p>
            <p class="hint">创建班期后，可以在班期内创建班级并管理学生</p>
          </div>
        </section>

        <!-- 班级管理模块 -->
        <section v-if="activeModule === 'classes'" class="module-section">
          <div class="module-header">
            <h2>班级管理</h2>
            <div class="action-buttons">
              <select v-model="selectedTermForClass" class="filter-select" style="margin-right: 1rem;">
                <option value="">选择班期</option>
                <option v-for="term in terms" :key="term.id" :value="term.id">
                  {{ term.name }}
                </option>
              </select>
              <button 
                @click="showClassModal = true" 
                class="action-btn primary-btn"
                :disabled="!selectedTermForClass"
              >
                ➕ 新建班级
              </button>
            </div>
          </div>

          <div v-if="!selectedTermForClass" class="no-data">
            <p>请先选择班期</p>
          </div>

          <div v-else-if="filteredClasses.length > 0" class="list-section">
            <div v-for="classItem in filteredClasses" :key="classItem.id" class="item-card class-card">
              <div class="item-header">
                <h3 class="item-title">{{ classItem.name }}</h3>
                <span :class="['status-badge', classItem.status]">{{ getClassStatusText(classItem.status) }}</span>
              </div>
              
              <div class="item-info">
                <div class="info-row">
                  <strong>所属班期：</strong>{{ getTermName(classItem.termId) }}
                </div>
                <div class="info-row">
                  <strong>班级容量：</strong>{{ classItem.studentCount }} / {{ classItem.capacity }} 人
                </div>
                <div class="info-row">
                  <strong>班主任：</strong>{{ classItem.teacher || '未指定' }}
                </div>
                <div class="info-row">
                  <strong>描述：</strong>{{ classItem.description }}
                </div>
              </div>

              <div class="item-actions">
                <button @click="editClass(classItem)" class="action-link">
                  ✏️ 编辑
                </button>
                <button @click="manageStudents(classItem)" class="action-link primary-action">
                  👥 管理学生
                </button>
                <button @click="viewClassStats(classItem)" class="action-link">
                  📊 查看统计
                </button>
                <button @click="deleteClass(classItem.id)" class="action-link danger-action">
                  🗑️ 删除
                </button>
              </div>
            </div>
          </div>

          <div v-else class="no-data">
            <p>该班期暂无班级</p>
            <p class="hint">点击"新建班级"按钮创建班级</p>
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
    <div v-if="showQuestionModal" class="modal-overlay" @click="showQuestionModal = false">
      <div class="modal-content modal-lg" @click.stop>
        <div class="modal-header">
          <h3>{{ editingQuestion ? '编辑题目' : '添加题目' }}</h3>
          <button @click="showQuestionModal = false" class="close-btn">✕</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label>题型 *</label>
            <select v-model="newQuestion.type" class="form-input">
              <option value="">请选择题型</option>
              <option value="choice">选择题</option>
              <option value="fill">填空题</option>
              <option value="essay">简答题</option>
            </select>
          </div>

          <div class="form-group">
            <label>题目内容 *</label>
            <textarea v-model="newQuestion.content" placeholder="输入题目内容" rows="4" class="form-textarea"></textarea>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>难度 *</label>
              <select v-model="newQuestion.difficulty" class="form-input">
                <option value="">请选择难度</option>
                <option value="easy">简单</option>
                <option value="medium">中等</option>
                <option value="hard">困难</option>
              </select>
            </div>
            <div class="form-group">
              <label>分值 *</label>
              <input v-model.number="newQuestion.points" type="number" min="1" placeholder="输入分值" class="form-input">
            </div>
          </div>

          <div v-if="newQuestion.type === 'choice'" class="form-group">
            <label>选项</label>
            <div v-for="(option, idx) in newQuestion.options" :key="idx" class="option-input">
              <span>{{ String.fromCharCode(65 + idx) }}.</span>
              <input v-model="newQuestion.options[idx]" type="text" placeholder="输入选项内容" class="form-input">
              <input v-model.number="newQuestion.answer" type="radio" :value="idx" name="answer">
              <label>答案</label>
            </div>
          </div>

          <div v-if="newQuestion.type !== 'choice'" class="form-group">
            <label>标准答案</label>
            <textarea v-model="newQuestion.answer" placeholder="输入标准答案" rows="3" class="form-textarea"></textarea>
          </div>

          <div class="modal-actions">
            <button @click="showQuestionModal = false" class="btn-cancel">取消</button>
            <button @click="submitQuestion" class="btn-submit">保存题目</button>
          </div>
        </div>
      </div>
    </div>

    <!-- 新建/编辑班期模态框 -->
    <div v-if="showTermModal" class="modal-overlay" @click="showTermModal = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ editingTerm ? '编辑班期' : '新建班期' }}</h3>
          <button @click="showTermModal = false" class="close-btn">✕</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label>班期名称 *</label>
            <input v-model="newTerm.name" type="text" placeholder="例如：2024春季班" class="form-input">
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>开始日期 *</label>
              <input v-model="newTerm.startDate" type="date" class="form-input">
            </div>
            <div class="form-group">
              <label>结束日期 *</label>
              <input v-model="newTerm.endDate" type="date" class="form-input">
            </div>
          </div>

          <div class="form-group">
            <label>班期描述</label>
            <textarea v-model="newTerm.description" placeholder="输入班期描述" rows="3" class="form-textarea"></textarea>
          </div>

          <div class="modal-actions">
            <button @click="showTermModal = false" class="btn-cancel">取消</button>
            <button @click="submitTermForm" class="btn-submit">保存</button>
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
              <label>班主任</label>
              <input v-model="newClass.teacher" type="text" placeholder="输入班主任姓名" class="form-input">
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
  </div>
</template>

<script>
export default {
  name: 'TeacherCourseDetail',
  data() {
    return {
      activeModule: 'sections',
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
        { id: 'grades', label: '成绩管理', icon: '📊' },
        { id: 'terms', label: '班期管理', icon: '📅' },
        { id: 'classes', label: '班级管理', icon: '👥' },
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

      // 成绩管理数据
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
      showQuestionModal: false,
      editingQuestion: null,
      questionFilter: {
        type: '',
        difficulty: ''
      },
      newQuestion: {
        type: '',
        content: '',
        difficulty: '',
        points: 5,
        options: ['', '', '', ''],
        answer: ''
      },
      questions: [
        {
          id: 1,
          type: 'choice',
          content: '下列哪个是 JavaScript 的原始数据类型？',
          options: ['Object', 'Array', 'String', 'Function'],
          answer: 2,
          difficulty: 'easy',
          points: 2,
          usageCount: 15
        },
        {
          id: 2,
          type: 'fill',
          content: '在 JavaScript 中，___ 是最常用的输出方式。',
          answer: 'console.log',
          difficulty: 'easy',
          points: 2,
          usageCount: 20
        },
        {
          id: 3,
          type: 'choice',
          content: '以下关于闭包的说法正确的是？',
          options: ['闭包是一个函数', '闭包会造成内存泄漏', '闭包可以访问外层函数的变量', '闭包只能在全局作用域中创建'],
          answer: 2,
          difficulty: 'medium',
          points: 3,
          usageCount: 8
        },
        {
          id: 4,
          type: 'essay',
          content: '请简述 Promise 的三个状态及其转换关系',
          answer: 'pending、fulfilled、rejected。pending 可转换为 fulfilled 或 rejected，状态确定后不再改变。',
          difficulty: 'hard',
          points: 5,
          usageCount: 5
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
        description: ''
      }
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
        
        // 个人筛选
        const personalMatch = !this.showMyThreadsOnly || 
                             thread.authorId === this.currentUserId
        
        return searchMatch && personalMatch
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
      return this.questions.filter(q => {
        const searchMatch = q.content.includes(this.questionSearch)
        const typeMatch = !this.questionFilter.type || q.type === this.questionFilter.type
        const difficultyMatch = !this.questionFilter.difficulty || q.difficulty === this.questionFilter.difficulty
        return searchMatch && typeMatch && difficultyMatch
      })
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
    }
  },
  methods: {
    // 选择模块
    selectModule(moduleId) {
      console.log('点击了模块:', moduleId)
      this.activeModule = moduleId
      console.log('当前模块:', this.activeModule)
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
        path: `/course/${this.courseInfo.id}/lesson/${lesson.id}`,
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
      this.$router.push(`/teacher/homework/${hw.id}/settings`)
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
      this.$router.push('/teacher/homework/library')
    },
    goToChapterEditor() {
      this.$router.push(`/teacher/course/${this.courseInfo.id}/chapters/edit`)
    },
    goToCreateHomework() {
      this.$router.push('/teacher/homework/create')
    },
    viewHomeworkDetail(hw) {
      // 根据是否发布过判断跳转逻辑
      const published = hw.published || false
      this.$router.push({
        path: `/teacher/homework/${hw.id}/detail`,
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
      this.$router.push(`/teacher/exam/${exam.id}/settings`)
    },
    gradeExam(exam) {
      this.$router.push(`/teacher/exam/${exam.id}/grading`)
    },
    viewExamDetail(exam) {
      // 根据发放次数判断是否发布过
      const published = exam.publishCount > 0 || exam.published || false
      this.$router.push({
        path: `/teacher/exam/${exam.id}/detail`,
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
      this.$router.push('/teacher/exam-library')
    },
    goToExamManage() {
      this.$router.push('/exam-center')
    },
    goToCreateExam() {
      this.$router.push('/teacher/exam-create')
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
        name: 'CommunityThreadDetail',
        params: { 
          courseId: this.courseInfo.id,
          id: threadId 
        }
      })
    },
    createNewThread() {
      // 跳转到创建话题页面
      this.$router.push({
        name: 'CommunityThreadCreate',
        params: {
          courseId: this.courseInfo.id
        }
      })
    },
    editThread(threadId) {
      // 跳转到编辑页面
      this.$router.push({
        name: 'CommunityThreadEdit',
        params: {
          courseId: this.courseInfo.id,
          id: threadId
        }
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
      // 作者本人或老师可以管理话题
      return thread.authorId === this.currentUserId || this.currentUserRole === 'teacher'
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

    // 成绩管理方法
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
    getQuestionTypeLabel(type) {
      const labels = {
        choice: '选择题',
        fill: '填空题',
        essay: '简答题'
      }
      return labels[type] || type
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
        this.$message.success('题目已删除')
      }
    },
    submitQuestion() {
      if (!this.newQuestion.type || !this.newQuestion.content || !this.newQuestion.difficulty) {
        this.$message.error('请填写完整的题目信息')
        return
      }

      if (this.editingQuestion) {
        const idx = this.questions.findIndex(q => q.id === this.editingQuestion.id)
        if (idx > -1) {
          this.questions[idx] = { ...this.newQuestion, id: this.editingQuestion.id }
          this.$message.success('题目已更新')
        }
      } else {
        this.questions.push({
          ...this.newQuestion,
          id: Math.max(...this.questions.map(q => q.id)) + 1,
          usageCount: 0
        })
        this.$message.success('题目已添加')
      }

      this.resetQuestionForm()
      this.showQuestionModal = false
    },
    resetQuestionForm() {
      this.newQuestion = {
        type: '',
        content: '',
        difficulty: '',
        points: 5,
        options: ['', '', '', ''],
        answer: ''
      }
      this.editingQuestion = null
    },
    importQuestions() {
      this.$message.info('导入题目功能开发中...')
    },
    exportQuestions() {
      this.$message.success('题目已导出')
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
        this.terms.push({
          ...this.newTerm,
          id: Math.max(...this.terms.map(t => t.id), 0) + 1,
          status: 'upcoming',
          classCount: 0,
          studentCount: 0
        })
        this.$message.success('班期已创建')
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

      if (!this.selectedTermForClass) {
        this.$message.error('请先选择班期')
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
      this.newClass = { name: '', capacity: 50, teacher: '', description: '' }
    }
  }
}
</script>

<style scoped>
.teacher-course-detail {
  display: flex;
  min-height: 100vh;
  background-color: #f8f9fa;
}

/* 左侧固定导航栏 */
/* Logo区域 */
.page-logo {
  position: fixed;
  left: 0;
  top: 70px;
  width: 220px;
  height: 56px;
  background: white;
  border-right: 1px solid #e5e7eb;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 101;
}

.page-logo h1 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 700;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.sidebar-fixed {
  width: 220px;
  background: white;
  border-right: 1px solid #e5e7eb;
  padding: 1.5rem 0;
  position: fixed;
  left: 0;
  top: 126px;
  height: calc(100vh - 126px);
  overflow-y: auto;
  z-index: 100;
}

.nav-menu {
  display: flex;
  flex-direction: column;
  gap: 0;
  padding: 0 0.75rem;
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
  margin-top: 70px;
  padding: 0;
}

/* 右侧内容区 */
.content-area {
  background: white;
  min-height: calc(100vh - 70px);
}

.module-section {
  padding: 2rem;
  animation: fadeIn 0.3s ease-in;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.module-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  gap: 1rem;
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

/* 筛选区 */
.filter-section {
  display: flex;
  gap: 2rem;
  margin-bottom: 2rem;
  padding: 1rem;
  background-color: #f8f9fa;
  border-radius: 6px;
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
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 8px;
  width: 90%;
  max-width: 500px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #ecf0f1;
}

.modal-header h3 {
  margin: 0;
  color: #2c3e50;
  font-size: 1.1rem;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #7f8c8d;
}

.close-btn:hover {
  color: #2c3e50;
}

.modal-body {
  padding: 1.5rem;
  color: #7f8c8d;
}

/* ========== 课程社区模块样式 ========== */
.community-module {
  padding: 0 !important;
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


/* 成绩管理样式 */
.stats-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
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
  margin-bottom: 1.5rem;
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

/* 题库样式 */
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

.form-group {
  margin-bottom: 1.5rem;
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
  padding: 0.75rem;
  border: 1px solid #bdc3c7;
  border-radius: 4px;
  font-size: 0.9rem;
  font-family: inherit;
}

.form-input:focus,
.form-textarea:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
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
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid #ecf0f1;
}

.btn-cancel,
.btn-submit {
  padding: 0.65rem 1.5rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s;
}

.btn-cancel {
  background: #ecf0f1;
  color: #2c3e50;
}

.btn-cancel:hover {
  background: #d5dbdb;
}

.btn-submit {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.btn-submit:hover {
  opacity: 0.9;
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
}

.overview-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
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
</style>

