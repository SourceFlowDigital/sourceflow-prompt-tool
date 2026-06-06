<template>
  <view class="about-page">
    <view class="brand">
      <image class="brand-logo" src="/static/logo.png" mode="aspectFit" />
      <view class="brand-text">
        <view class="brand-title">源流AI提示词</view>
        <view class="brand-subtitle">4步生成，无需基础</view>
        <view class="brand-signature">源流数字 · SOURCEFLOW DIGITAL</view>
      </view>
    </view>

    <view class="info-card product-card">
      <view class="product-heading">
        <view class="card-title product-title">源流AI提示词工具</view>
        <view class="version">v1.0.0</view>
      </view>
      <view class="card-content">
        面向国内普通用户的AI提示词生成工具，通过4步引导（选场景→选角色→定身份→输入任务），自动生成可直接使用的结构化提示词，无需任何提示词写作基础。
      </view>
    </view>

    <view class="info-card">
      <view class="card-title">如何使用</view>
      <view class="step-list">
        <view class="step-item">· 第一步：选择使用场景（12个分类）</view>
        <view class="step-item">· 第二步：选择合适的AI角色（108个角色）</view>
        <view class="step-item">· 第三步：确认或修改AI身份</view>
        <view class="step-item">· 第四步：描述你的任务，生成提示词</view>
      </view>
    </view>

    <view class="info-card">
      <view class="card-title">高级模式</view>
      <view class="card-content">
        高级模式由DeepSeek AI驱动，可生成更专业、更精准的结构化提示词。每次调用 ¥0.99，按次计费，无订阅。
      </view>
      <view class="security-tip">
        您的API调用通过我们的服务器安全代理，API Key不会暴露给前端或用户设备。
      </view>
    </view>

    <view class="info-card">
      <view class="card-title">开源声明</view>
      <view class="card-content">
        本项目基于 MIT License 开源发布。角色数据来源于 agency-agents 开源项目（msitarzewski/agency-agents），已按 MIT 协议使用并保留版权声明。
      </view>
      <navigator
        class="source-link"
        url="https://github.com/SourceFlowDigital/sourceflow-prompt-tool"
        target="_blank"
      >
        查看源码 →
      </navigator>
    </view>

    <view class="info-card">
      <view class="card-title">联系我们</view>
      <view class="contact-item">技术支持：源流数字</view>
      <view class="contact-item">联系邮箱：待补充</view>
      <view class="contact-item">联系电话：待补充</view>
    </view>

    <view class="copyright">© 2026 宁夏源流数字服务有限公司</view>
  </view>
</template>

<style>
.about-page {
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

.info-card {
  box-sizing: border-box;
  margin-bottom: 20rpx;
  padding: 26rpx 28rpx;
  background: #FFFFFF;
  border: 1rpx solid #DCE5EF;
  border-radius: 18rpx;
  box-shadow: 0 4rpx 24rpx rgba(0, 48, 96, 0.06);
}

.product-card {
  border-left: 6rpx solid #003060;
}

.product-heading {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20rpx;
}

.card-title {
  margin-bottom: 20rpx;
  font-size: 30rpx;
  font-weight: 600;
  color: #003060;
}

.product-title {
  margin-bottom: 0;
  font-weight: 700;
}

.version {
  margin-left: 20rpx;
  font-size: 24rpx;
  color: #6B7280;
}

.card-content,
.step-item,
.contact-item {
  font-size: 26rpx;
  line-height: 1.75;
  color: #1F2933;
}

.step-item + .step-item,
.contact-item + .contact-item {
  margin-top: 10rpx;
}

.security-tip {
  margin-top: 22rpx;
  padding: 18rpx 20rpx;
  background: #FFF8E1;
  border-left: 4rpx solid #F59E0B;
  border-radius: 8rpx;
  font-size: 24rpx;
  line-height: 1.7;
  color: #6B7280;
}

.source-link {
  margin-top: 22rpx;
  font-size: 26rpx;
  font-weight: 500;
  color: #2A86B8;
}

.copyright {
  margin-top: 32rpx;
  font-size: 22rpx;
  text-align: center;
  color: #9CA3AF;
}
</style>
