<template>
  <div class="Register">
    <div class="name">
      <div class="name-ch">问卷星球</div>
      <div class="name-en">Welcome to Ques-planet</div>
    </div>
    <div class="tips">tip:密码由6-16位数字和字母组成</div>
    <div class="regist-part">
      <div class="title">注册</div>
      <div class="username">
        <i class="el-icon-s-custom"></i>

        <input type="text" v-model="user_name" placeholder="请输入用户名" />
      </div>

      <!-- <div style="display: flex; flex-direction: column"> -->
      <div class="password">
        <i class="el-icon-lock"></i>
        <input type="password" v-model="password_1" placeholder="请输入密码" />
      </div>
      <!-- </div> -->

      <div class="password-confirm">
        <i class="el-icon-lock"></i>
        <input type="password" v-model="password_2" placeholder="请确认密码" />
      </div>
      <div class="rename">
        <i class="el-icon-edit"></i>
        <input type="text" v-model="re_name" placeholder="请输入昵称" />
      </div>
      <div class="re-button">
        <el-button @click="register" class="regist-button">注册</el-button>
      </div>
      <div class="to-login">
        <router-link to="/tologin">
          <el-link type="primary" style="color: white"
            >已经注册完成？立即登录！</el-link
          >
        </router-link>
      </div>
    </div>
  </div>
</template>

<style src="../css/Register.css"  scoped></style>

<script>
import { request } from "../network/request.js";

export default {
  name: "register",
  data() {
    return {
      user_name: "",
      password_1: "",
      password_2: "",
      re_name: "",
    };
  },
  methods: {
    register() {
      console.log(this.user_name);
      console.log(this.password_1);
      console.log(this.password_2);
      console.log(this.re_name);
      if (!this.user_name || !this.password_1 || !this.password_2) {
        this.$message({
          message: "用户名或密码不能为空",
          type: "warning",
        });
        return;
      }
      if (!this.re_name) {
        this.$message({
          message: "昵称不能为空",
          type: "warning",
        });
        return;
      }
      request({
        url: "/register",
        data: {
          username: this.user_name,
          password1: this.password_1,
          password2: this.password_2,
          rename: this.re_name,
        },
        method: "post",
      }).then((res) => {
        console.log(res);
        if (res.data.res == 1) {
          this.$message.error("密码不符合要求");
          return;
        } else if (res.data.res == 2) {
          this.$message.error("两次密码输入不一致");
          return;
        } else if (res.data.res == 3) {
          this.$message.error("用户名已被注册");
          return;
        } else if (res.data.res == 4) {
          this.$message({
            message: "恭喜你，注册成功！",
            type: "success",
          });
          this.$router.push("/tologin");
          //this.$store.commit("login");
          //this.$store.commit("setUsername", this.username);
        } else {
          this.$message.error("请重新输入");
          return;
        }
      });
    },
  },
};
</script>



