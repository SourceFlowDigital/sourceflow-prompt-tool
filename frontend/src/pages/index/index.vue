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
      <view class="step-title">① 选择使用场景</view>
      <view
        :class="['category-trigger', { placeholder: categoryIndex < 0 }]"
        @tap="toggleCategoryList"
      >
        <text>{{ selectedCategory ? selectedCategory.name : '请选择场景' }}</text>
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
      <picker :range="roleOptions" :value="roleIndex" @change="onRoleChange">
        <view :class="['picker-field', { placeholder: roleIndex < 0 }]">
          <text class="picker-text">{{ selectedRole ? formatRole(selectedRole) : '请选择角色' }}</text>
          <text class="arrow">›</text>
        </view>
      </picker>
    </view>

    <view v-if="selectedRole" class="step-card">
      <view class="step-title">③ 定义AI的身份</view>
      <input
        v-model="aiIdentity"
        class="text-input"
        maxlength="50"
        placeholder="请输入AI身份"
        placeholder-class="input-placeholder"
        @input="resetResult"
      />
      <view class="field-hint">可直接使用默认身份，或自行修改</view>
    </view>

    <view v-if="aiIdentity.trim()" class="step-card">
      <view class="step-title">④ 描述你的任务</view>
      <view class="textarea-wrap">
        <textarea
          v-model="task"
          class="task-textarea"
          maxlength="200"
          placeholder="请描述你希望AI帮你完成的任务，越具体效果越好"
          placeholder-class="input-placeholder"
          @input="resetResult"
        />
        <view class="counter">{{ task.length }}/200字</view>
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

export default {
  data() {
    return {
      categories,
      roles,
      categoryIndex: -1,
      categoryListOpen: false,
      roleIndex: -1,
      aiIdentity: '',
      task: '',
      generatedPrompt: '',
      copied: false,
    }
  },
  computed: {
    selectedCategory() {
      return this.categoryIndex >= 0 ? this.categories[this.categoryIndex] : null
    },
    filteredRoles() {
      if (!this.selectedCategory) return []
      return this.roles.filter((role) => role.category_id === this.selectedCategory.id)
    },
    roleOptions() {
      return this.filteredRoles.map((role) => this.formatRole(role))
    },
    selectedRole() {
      return this.roleIndex >= 0 ? this.filteredRoles[this.roleIndex] : null
    },
  },
  methods: {
    formatRole(role) {
      const desc = role.desc.length > 20 ? `${role.desc.slice(0, 20)}...` : role.desc
      return `${role.name}——${desc}`
    },
    toggleCategoryList() {
      this.categoryListOpen = !this.categoryListOpen
    },
    getCategoryDescription(category) {
      if (category.description) return category.description
      return category.subcategories.map((subcategory) => subcategory.name).join('、')
    },
    selectCategory(index) {
      this.categoryIndex = index
      this.categoryListOpen = false
      this.roleIndex = -1
      this.aiIdentity = ''
      this.task = ''
      this.resetResult()
    },
    onRoleChange(event) {
      this.roleIndex = Number(event.detail.value)
      this.aiIdentity = this.selectedRole.name
      this.task = ''
      this.resetResult()
    },
    resetResult() {
      this.generatedPrompt = ''
      this.copied = false
    },
    generatePrompt() {
      this.generatedPrompt = `你是一位${this.aiIdentity.trim()}。\n你的任务是：${this.task.trim()}。\n请以专业、清晰的方式完成这个任务。`
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
  padding: 32rpx 32rpx 180rpx;
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

.step-title,
.result-title {
  margin-bottom: 20rpx;
  font-size: 30rpx;
  font-weight: 600;
  color: #003060;
}

.picker-field,
.category-trigger,
.text-input {
  box-sizing: border-box;
  width: 100%;
  height: 80rpx;
  padding: 0 20rpx;
  background: #F2F6FA;
  border: 1rpx solid #DCE5EF;
  border-radius: 12rpx;
  font-size: 28rpx;
  color: #1F2933;
}

.picker-field {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.category-trigger {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #FFFFFF;
  border: 1rpx solid #DCE5EF;
  border-radius: 16rpx;
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

.picker-text {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.placeholder,
.input-placeholder {
  color: #9CA3AF;
}

.arrow {
  margin-left: 20rpx;
  font-size: 34rpx;
  color: #9CA3AF;
}

.field-hint {
  margin-top: 10rpx;
  font-size: 22rpx;
  color: #9CA3AF;
}

.textarea-wrap {
  position: relative;
  box-sizing: border-box;
  padding: 20rpx 20rpx 52rpx;
  background: #F2F6FA;
  border: 1rpx solid #DCE5EF;
  border-radius: 12rpx;
}

.task-textarea {
  width: 100%;
  min-height: 160rpx;
  font-size: 28rpx;
  line-height: 1.6;
  color: #1F2933;
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
