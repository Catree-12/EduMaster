import http from './http'

/**
 * 知识点和标签管理 API
 */

// ==================== 标签管理 ====================

/**
 * 获取标签列表
 * @param {Object} params - 查询参数 { search, page, page_size }
 */
export const getTags = (params) => {
  return http.get('/knowledge/tags/', { params })
}

/**
 * 创建标签
 * @param {Object} data - { name, color, description }
 */
export const createTag = (data) => {
  return http.post('/knowledge/tags/', data)
}

/**
 * 获取标签详情
 * @param {Number} tagId - 标签ID
 */
export const getTagDetail = (tagId) => {
  return http.get(`/knowledge/tags/${tagId}/`)
}

/**
 * 更新标签
 * @param {Number} tagId - 标签ID
 * @param {Object} data - { name, color, description }
 */
export const updateTag = (tagId, data) => {
  return http.put(`/knowledge/tags/${tagId}/`, data)
}

/**
 * 删除标签
 * @param {Number} tagId - 标签ID
 */
export const deleteTag = (tagId) => {
  return http.delete(`/knowledge/tags/${tagId}/`)
}

/**
 * 给对象添加标签
 * @param {Object} data - { tag_id, content_type, object_id }
 */
export const attachTags = (data) => {
  return http.post('/knowledge/tags/attach/', data)
}

/**
 * 移除对象的标签
 * @param {Object} data - { tag_id, content_type, object_id }
 */
export const detachTags = (data) => {
  return http.delete('/knowledge/tags/detach/', { data })
}

/**
 * 获取对象的所有标签
 * @param {Object} params - { content_type, object_id }
 */
export const getObjectTags = (params) => {
  return http.get('/knowledge/tags/object/', { params })
}

// ==================== 知识点管理 ====================

/**
 * 获取知识点树状结构
 * @param {Object} params - { search, parent_id }
 */
export const getKnowledgePoints = (params) => {
  return http.get('/knowledge/points/', { params })
}

/**
 * 创建知识点
 * @param {Object} data - { name, parent_id, description, order }
 */
export const createKnowledgePoint = (data) => {
  return http.post('/knowledge/points/', data)
}

/**
 * 获取知识点详情
 * @param {Number} pointId - 知识点ID
 */
export const getKnowledgePointDetail = (pointId) => {
  return http.get(`/knowledge/points/${pointId}/`)
}

/**
 * 更新知识点
 * @param {Number} pointId - 知识点ID
 * @param {Object} data - { name, parent_id, description, order }
 */
export const updateKnowledgePoint = (pointId, data) => {
  return http.put(`/knowledge/points/${pointId}/`, data)
}

/**
 * 删除知识点
 * @param {Number} pointId - 知识点ID
 */
export const deleteKnowledgePoint = (pointId) => {
  return http.delete(`/knowledge/points/${pointId}/`)
}

/**
 * 给对象关联知识点
 * @param {Object} data - { content_type, object_id, point_id }
 */
export const attachKnowledgePoints = (data) => {
  return http.post('/knowledge/points/attach/', data)
}

/**
 * 移除对象的知识点关联
 * @param {Object} data - { content_type, object_id, point_id }
 */
export const detachKnowledgePoints = (data) => {
  return http.delete('/knowledge/points/detach/', { data })
}

/**
 * 获取对象关联的所有知识点
 * @param {Object} params - { content_type, object_id }
 */
export const getObjectKnowledgePoints = (params) => {
  return http.get('/knowledge/points/object/', { params })
}
