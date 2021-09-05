<template>
  <div class="login">
    <div class="name">
      <div class="name-ch">问卷星球</div>
      <div class="name-en">Welcome to Ques-planet</div>
    </div>

    <div class="login-part">
      <div class="login-in">登录</div>
      <div class="username">
        <i class="el-icon-s-custom"></i>

        <input type="text" v-model="username" placeholder="请输入用户名" />
      </div>
      <div class="password">
        <i class="el-icon-lock"></i>

        <input type="password" v-model="password" placeholder="请输入密码" />
      </div>
      <div class="log-button">
        <el-button @click="login" class="login-button">登录</el-button>
      </div>
      <div class="to-regist">
        <router-link to="/toregister">
          <el-link type="primary" style="color: white"
            >还没有账号？立即注册！</el-link
          >
        </router-link>
      </div>
    </div>
  </div>
</template>

<style src="../css/Login.css"  scoped></style>

<script>
import { request } from "../network/request.js";

export default {
  name: "login",
  data() {
    return {
      username: "",
      password: "",
    };
  },
  methods: {
    login() {
      console.log(this.username);
      console.log(this.password);
      if (!this.username || !this.password) {
        this.$message({
          message: "用户名或密码不能为空",
          type: "warning",
        });
        return;
      }
      request({
        url: "/login",
        data: {
          username: this.username,
          password: this.password,
        },
        method: "post",
      }).then((res) => {
        console.log(res);
        if (res.data.res == 1) {
          this.$message.error("用户名或密码错误");
          return;
        } else {
          this.$message({
            message: "恭喜你，登录成功！",
            type: "success",
          });
          this.$store.commit("login");
          this.$store.commit("setUsername", this.username);

          this.$router.push("/tomanage");
        }
      });
    },
  },
};
</script>

