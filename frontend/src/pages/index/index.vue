<template>
  <view class="page">
    <view class="brand">
      <image class="brand-logo" src="/static/logo.png" mode="aspectFit" />
      <view class="brand-text">
        <view class="brand-title">源流AI提示词</view>
        <view class="brand-subtitle">4步生成，无需基础</view>
        <view class="brand-signature">源流数字 · SOURCEFLOW DIGITAL</view>
      </view>
    </view>

    <view class="step-card">
      <view class="step-title">① 选择分类</view>
      <view
        :class="['category-trigger', { placeholder: categoryIndex < 0 }]"
        @tap="toggleCategoryList"
      >
        <text>{{ selectedCategory ? selectedCategory.name : '请选择分类' }}</text>
        <text class="category-arrow">{{ categoryListOpen ? '▴' : '▾' }}</text>
      </view>
      <view v-if="categoryListOpen" class="category-list">
        <view
          v-for="(category, index) in categories"
          :key="category.id"
          :class="['category-option', { selected: categoryIndex === index }]"
          @tap="selectCategory(index)"
        >
          <view class="category-option-name">{{ category.name }}</view>
          <view class="category-option-description">{{ getCategoryDescription(category) }}</view>
        </view>
      </view>
    </view>

    <view v-if="selectedCategory" class="step-card">
      <view class="step-title">② 选择角色</view>
      <view class="category-trigger" @tap="toggleRoleList">
        <text class="role-trigger-name">{{ selectedRole ? selectedRole.name : '' }}</text>
        <text class="category-arrow">{{ roleListOpen ? '▴' : '▾' }}</text>
      </view>
      <view v-if="selectedRole && !roleListOpen" class="role-summary">
        {{ selectedRole.desc }}
      </view>
      <view v-if="roleListOpen" class="category-list">
        <view
          v-for="(role, index) in filteredRoles"
          :key="role.id"
          :class="['category-option', { selected: roleIndex === index }]"
          @tap="selectRole(index)"
        >
          <view class="category-option-name">{{ role.name }}</view>
          <view class="category-option-description">{{ role.desc }}</view>
        </view>
      </view>
    </view>

    <view v-if="selectedRole" class="step-card">
      <view class="step-header">
        <view class="step-title step-title-inline">③ 选择应用场景（可选）</view>
        <text class="skip-link" @tap="skipScene">跳过 →</text>
      </view>
      <view class="scene-grid">
        <view
          v-for="scene in standardScenes"
          :key="scene.scene_id"
          :class="['scene-chip', { selected: isSceneSelected(scene.scene_id) }]"
          @tap="selectScene(scene.scene_id)"
        >
          <text class="scene-chip-name">{{ scene.scene_name }}</text>
        </view>
      </view>
      <view class="custom-scene-area">
        <view
          :class="['scene-chip', 'scene-chip-custom', { selected: sceneMode === 'custom' }]"
          @tap="selectCustom"
        >
          <text class="scene-chip-name">+ 自定义</text>
        </view>
        <view v-if="sceneMode === 'custom'" class="custom-inline-input">
          <view class="inline-input-wrap inline-input-wrap-custom">
            <textarea
              v-model="customSceneText"
              class="inline-textarea inline-textarea-custom"
              auto-height
              maxlength="50"
              placeholder="请输入你的具体用途，例如：准备客户汇报、写朋友圈文案、整理竞品分析"
              placeholder-class="input-placeholder"
              @input="resetResult"
            />
            <view class="counter counter-below">{{ customSceneText.length }}/50字</view>
          </view>
        </view>
      </view>
    </view>

    <view v-if="selectedRole" class="step-card">
      <view class="step-title">④ 描述你的任务</view>
      <view class="inline-input-wrap">
        <textarea
          v-model="task"
          class="inline-textarea"
          auto-height
          maxlength="200"
          placeholder="请描述你希望AI帮你完成的任务，越具体效果越好"
          placeholder-class="input-placeholder"
          @input="resetResult"
        />
        <view class="counter">{{ task.length }}/200字</view>
      </view>
      <view class="advanced-options">
        <view class="advanced-label">高级选项</view>
        <view class="advanced-card">
          <view class="advanced-row">
            <view class="advanced-info">
              <view class="advanced-name">AI增强优化</view>
              <view class="advanced-desc">
                调用 DeepSeek 对基础提示词进一步优化，让提示词更具体、更完整、更专业。
              </view>
              <view class="advanced-hint">该功能需要付费或消耗次数，当前暂未开放。</view>
            </view>
            <switch :checked="false" disabled color="#003060" class="advanced-switch" />
          </view>
          <view class="advanced-status">付费功能，暂未开放</view>
        </view>
      </view>
      <button v-if="task.trim()" class="primary-btn" @tap="generatePrompt">生成提示词</button>
    </view>

    <view v-if="generatedPrompt" class="result-card">
      <view class="result-title">你的提示词已生成</view>
      <view class="result-content">{{ generatedPrompt }}</view>
      <button :class="['copy-btn', { copied }]" @tap="copyPrompt">
        {{ copied ? '已复制 ✓' : '一键复制' }}
      </button>
    </view>

  </view>
</template>

<script>
import categories from '../../data/categories.js'
import roles from '../../data/roles.js'

const STANDARD_SCENES = [
  {
    scene_id: 'content_creation',
    scene_name: '内容创作',
    scene_desc: '写文章、脚本、报告、提案、文档、课程材料等内容',
    sort_order: 1,
  },
  {
    scene_id: 'growth_conversion',
    scene_name: '获客转化',
    scene_desc: '做流量、曝光、广告、销售开发、客户转化',
    sort_order: 2,
  },
  {
    scene_id: 'research_analysis',
    scene_name: '调研分析',
    scene_desc: '查资料、看数据、做市场、用户、财务、竞品或学术分析',
    sort_order: 3,
  },
  {
    scene_id: 'planning_strategy',
    scene_name: '规划决策',
    scene_desc: '定战略、做方案、排优先级、定预算、做路线图',
    sort_order: 4,
  },
  {
    scene_id: 'product_development',
    scene_name: '产品开发',
    scene_desc: '写代码、做系统、搭架构、开发产品或技术方案',
    sort_order: 5,
  },
  {
    scene_id: 'design_experience',
    scene_name: '设计体验',
    scene_desc: '做UI、UX、品牌、视觉、图像、无障碍体验',
    sort_order: 6,
  },
  {
    scene_id: 'quality_risk',
    scene_name: '质检风控',
    scene_desc: '做测试、审查、安全、风控、合规把关',
    sort_order: 7,
  },
  {
    scene_id: 'operations_delivery',
    scene_name: '运营交付',
    scene_desc: '管流程、管项目、管资源、推动执行落地',
    sort_order: 8,
  },
]

export default {
  data() {
    return {
      categories,
      roles,
      categoryIndex: -1,
      categoryListOpen: false,
      roleListOpen: false,
      roleIndex: -1,
      sceneMode: 'standard',
      selectedSceneId: 'content_creation',
      customSceneText: '',
      task: '',
      generatedPrompt: '',
      copied: false,
    }
  },
  computed: {
    standardScenes() {
      return [...STANDARD_SCENES].sort((a, b) => a.sort_order - b.sort_order)
    },
    selectedCategory() {
      return this.categoryIndex >= 0 ? this.categories[this.categoryIndex] : null
    },
    filteredRoles() {
      if (!this.selectedCategory) return []
      return this.roles.filter((role) => role.category_id === this.selectedCategory.id)
    },
    selectedRole() {
      return this.roleIndex >= 0 ? this.filteredRoles[this.roleIndex] : null
    },
  },
  methods: {
    toggleCategoryList() {
      this.categoryListOpen = !this.categoryListOpen
    },
    toggleRoleList() {
      this.roleListOpen = !this.roleListOpen
    },
    getCategoryDescription(category) {
      if (category.description) return category.description
      return category.subcategories.map((subcategory) => subcategory.name).join('、')
    },
    resetSceneSelection() {
      this.sceneMode = 'standard'
      this.selectedSceneId = 'content_creation'
    },
    selectCategory(index) {
      this.categoryIndex = index
      this.categoryListOpen = false
      this.roleListOpen = false
      this.customSceneText = ''
      this.resetSceneSelection()
      this.task = ''
      this.resetResult()
      const roles = this.roles.filter((role) => role.category_id === this.categories[index].id)
      this.roleIndex = roles.length > 0 ? 0 : -1
    },
    selectRole(index) {
      this.roleIndex = index
      this.roleListOpen = false
      this.customSceneText = ''
      this.resetSceneSelection()
      this.task = ''
      this.resetResult()
    },
    isSceneSelected(sceneId) {
      return this.sceneMode === 'standard' && this.selectedSceneId === sceneId
    },
    selectScene(sceneId) {
      this.sceneMode = 'standard'
      this.selectedSceneId = sceneId
      this.resetResult()
    },
    skipScene() {
      this.sceneMode = 'skipped'
      this.selectedSceneId = ''
      this.resetResult()
    },
    selectCustom() {
      this.sceneMode = 'custom'
      this.selectedSceneId = ''
      this.resetResult()
    },
    resetResult() {
      this.generatedPrompt = ''
      this.copied = false
    },
    generatePrompt() {
      if (this.sceneMode === 'custom' && !this.customSceneText.trim()) {
        uni.showToast({
          title: '请输入自定义应用场景',
          icon: 'none',
        })
        return
      }

      const parts = [`你是一名${this.selectedRole.name}`]

      if (this.sceneMode === 'standard' && this.selectedSceneId) {
        const scene = this.standardScenes.find((item) => item.scene_id === this.selectedSceneId)
        if (scene) {
          parts.push(`应用场景：${scene.scene_name}`)
          parts.push(`场景说明：${scene.scene_desc}`)
        }
      } else if (this.sceneMode === 'custom' && this.customSceneText.trim()) {
        parts.push(`应用场景：${this.customSceneText.trim()}`)
      }

      parts.push(`你的任务是：${this.task.trim()}`)
      parts.push('请以专业、清晰的方式完成这个任务。')

      this.generatedPrompt = parts.join('\n')
      this.copied = false
    },
    copyPrompt() {
      uni.setClipboardData({
        data: this.generatedPrompt,
        success: () => {
          this.copied = true
        },
      })
    },
  },
}
</script>

<style>
.page {
  min-height: 100vh;
  box-sizing: border-box;
  padding: 32rpx 32rpx 120rpx;
  background: #F4F8FB;
}

.brand {
  display: flex;
  flex-direction: row;
  align-items: center;
  margin: -32rpx -32rpx 32rpx;
  padding: 40rpx 32rpx 32rpx;
  background: transparent;
  border-bottom: 1rpx solid #DCE5EF;
}

.brand-logo {
  width: 120rpx;
  height: 120rpx;
  flex-shrink: 0;
}

.brand-text {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  margin-left: 24rpx;
}

.brand-title {
  font-size: 40rpx;
  font-weight: 700;
  line-height: 1.32;
  color: #003060;
  background: linear-gradient(135deg, #E8C060, #003060);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.brand-subtitle {
  margin-top: 8rpx;
  font-size: 24rpx;
  color: #6B7280;
}

.brand-signature {
  margin-top: 8rpx;
  font-size: 20rpx;
  color: #9CA3AF;
}

.step-card,
.result-card {
  box-sizing: border-box;
  margin-bottom: 20rpx;
  padding: 26rpx 28rpx;
  background: #FFFFFF;
  border: 1rpx solid #DCE5EF;
  border-radius: 18rpx;
  box-shadow: 0 4rpx 24rpx rgba(0, 48, 96, 0.06);
}

.step-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20rpx;
}

.step-title,
.result-title {
  margin-bottom: 20rpx;
  font-size: 30rpx;
  font-weight: 600;
  color: #003060;
}

.step-title-inline {
  margin-bottom: 0;
}

.skip-link {
  font-size: 24rpx;
  color: #9CA3AF;
}

.category-trigger {
  box-sizing: border-box;
  width: 100%;
  height: 80rpx;
  padding: 0 20rpx;
  background: #FFFFFF;
  border: 1rpx solid #DCE5EF;
  border-radius: 16rpx;
  font-size: 28rpx;
  color: #1F2933;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.category-arrow {
  margin-left: 20rpx;
  font-size: 24rpx;
  color: #9CA3AF;
}

.category-list {
  margin-top: 12rpx;
  overflow: hidden;
  background: #FFFFFF;
  border: 1rpx solid #D6A84F;
  border-radius: 16rpx;
}

.category-option {
  position: relative;
  box-sizing: border-box;
  padding: 20rpx 24rpx;
  border-bottom: 1rpx solid #E5E7EB;
}

.category-option:last-child {
  border-bottom: 0;
}

.category-option.selected {
  padding-left: 30rpx;
  background: #F4F8FB;
}

.category-option.selected::before {
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  width: 6rpx;
  content: '';
  background: #003060;
}

.category-option-name {
  font-size: 26rpx;
  font-weight: 500;
  line-height: 1.4;
  color: #003060;
}

.category-option-description {
  margin-top: 6rpx;
  font-size: 22rpx;
  line-height: 1.45;
  color: #9CA3AF;
}

.role-trigger-name {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.role-summary {
  margin-top: 10rpx;
  font-size: 22rpx;
  line-height: 1.45;
  color: #9CA3AF;
}

.scene-grid {
  display: flex;
  flex-wrap: wrap;
  margin: -8rpx;
}

.scene-chip {
  box-sizing: border-box;
  display: flex;
  align-items: center;
  justify-content: center;
  width: calc(50% - 16rpx);
  min-height: 72rpx;
  margin: 8rpx;
  padding: 16rpx 20rpx;
  background: #F2F6FA;
  border: 1rpx solid #DCE5EF;
  border-radius: 12rpx;
}

.scene-chip.selected {
  background: #F4F8FB;
  border-color: #D6A84F;
  box-shadow: inset 0 0 0 1rpx #D6A84F;
}

.scene-chip-name {
  font-size: 26rpx;
  line-height: 1.4;
  color: #003060;
  text-align: center;
}

.custom-scene-area {
  margin-top: 8rpx;
}

.scene-chip-custom {
  width: calc(100% - 16rpx);
  margin: 8rpx;
  border-style: dashed;
}

.scene-chip-custom.selected {
  border-style: solid;
}

.custom-inline-input {
  width: 100%;
  margin-top: 4rpx;
  padding: 0 8rpx;
  box-sizing: border-box;
}

.placeholder,
.input-placeholder {
  color: #9CA3AF;
}

.inline-input-wrap {
  position: relative;
  box-sizing: border-box;
  padding: 16rpx 20rpx 44rpx;
  background: #F2F6FA;
  border: 1rpx solid #DCE5EF;
  border-radius: 12rpx;
}

.inline-input-wrap-custom {
  padding: 16rpx 20rpx 12rpx;
}

.inline-textarea {
  display: block;
  width: 100%;
  min-height: 44rpx;
  font-size: 28rpx;
  line-height: 1.5;
  color: #1F2933;
  word-break: break-all;
}

.inline-textarea-custom {
  min-height: 80rpx;
}

.counter-below {
  position: static;
  margin-top: 10rpx;
  text-align: right;
}

.advanced-options {
  margin-top: 24rpx;
}

.advanced-label {
  margin-bottom: 12rpx;
  font-size: 24rpx;
  font-weight: 500;
  color: #6B7280;
}

.advanced-card {
  box-sizing: border-box;
  padding: 20rpx 22rpx;
  background: #F8FAFC;
  border: 1rpx solid #DCE5EF;
  border-radius: 12rpx;
}

.advanced-row {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16rpx;
}

.advanced-info {
  flex: 1;
  min-width: 0;
}

.advanced-name {
  font-size: 28rpx;
  font-weight: 600;
  color: #003060;
}

.advanced-desc {
  margin-top: 8rpx;
  font-size: 24rpx;
  line-height: 1.55;
  color: #4B5563;
}

.advanced-hint {
  margin-top: 8rpx;
  font-size: 22rpx;
  line-height: 1.45;
  color: #9CA3AF;
}

.advanced-switch {
  flex-shrink: 0;
  transform: scale(0.85);
}

.advanced-status {
  margin-top: 14rpx;
  padding-top: 14rpx;
  border-top: 1rpx solid #E5E7EB;
  font-size: 22rpx;
  color: #9CA3AF;
}

.counter {
  position: absolute;
  right: 20rpx;
  bottom: 16rpx;
  font-size: 22rpx;
  color: #9CA3AF;
}

.primary-btn,
.copy-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  box-sizing: border-box;
  width: 100%;
  margin-top: 24rpx;
  border-radius: 18rpx;
  font-size: 30rpx;
  font-weight: 500;
  line-height: 1;
}

.primary-btn {
  height: 88rpx;
  color: #FFFFFF;
  background: #003060;
  box-shadow: 0 4rpx 16rpx rgba(0, 48, 96, 0.25);
}

.primary-btn::after,
.copy-btn::after {
  border: 0;
}

.result-card {
  border-left: 6rpx solid #003060;
}

.result-content {
  padding: 20rpx;
  background: #F2F6FA;
  border-radius: 12rpx;
  font-size: 26rpx;
  line-height: 1.75;
  color: #1F2933;
  white-space: pre-line;
}

.copy-btn {
  height: 80rpx;
  color: #003060;
  background: #FFFFFF;
  border: 1rpx solid #003060;
  box-shadow: none;
}

.copy-btn.copied {
  color: #16A085;
  border-color: #16A085;
}
</style>
