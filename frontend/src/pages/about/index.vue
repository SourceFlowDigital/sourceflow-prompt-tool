<template>
  <view class="about-page">
    <image class="logo" src="/static/logo.png" mode="aspectFit" />
    <view class="brand-name">源流AI提示词工具</view>
    <view class="version">v1.0.0</view>
    <view class="intro">面向普通用户的AI提示词生成工具，无需任何提示词写作基础。</view>
    <view class="meta">本项目基于 MIT License 开源</view>
    <view class="copyright">© 2026 宁夏源流数字服务有限公司</view>
  </view>
</template>

<style>
.about-page {
  min-height: 100vh;
  box-sizing: border-box;
  padding: 120rpx 56rpx 180rpx;
  background: #F4F8FB;
  text-align: center;
}

.logo {
  width: 220rpx;
  height: 220rpx;
  margin-bottom: 28rpx;
}

.brand-name {
  font-size: 40rpx;
  font-weight: 700;
  color: #003060;
}

.version {
  margin-top: 12rpx;
  font-size: 24rpx;
  color: #6B7280;
}

.intro {
  margin-top: 56rpx;
  padding: 32rpx;
  background: #FFFFFF;
  border: 1rpx solid #DCE5EF;
  border-radius: 18rpx;
  box-shadow: 0 4rpx 24rpx rgba(0, 48, 96, 0.06);
  font-size: 28rpx;
  line-height: 1.75;
  color: #1F2933;
}

.meta,
.copyright {
  font-size: 24rpx;
  color: #6B7280;
}

.meta {
  margin-top: 56rpx;
}

.copyright {
  margin-top: 20rpx;
}
</style>
