<template>
  <div class="home">
    <div class="title">
      <div class="logo"></div>
      <router-link to="/">
        <div class="name">问卷星球</div>
      </router-link>
      <router-link to="/tologin">
        <el-button type="primary" class="login-button"
          >登录</el-button
        ></router-link
      >
      <router-link to="/toregister"
        ><el-button type="success" class="register-button"
          >注册</el-button
        ></router-link
      >
    </div>
    <div class="title0">
      <div class="title1">问卷星球</div>
      <div class="title2">为您量身定制的轻量级问卷平台</div>
      <router-link to="/tologin"
        ><el-button type="warning" round class="free-use-button"
          >免费使用</el-button
        ></router-link
      >
    </div>
  </div>
</template>

<style src="../css/Home.css"  scoped></style>



