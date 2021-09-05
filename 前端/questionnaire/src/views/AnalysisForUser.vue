<template>
  <div class="grey">
    <div class="anaUser">
      <div style="display: flex; justify-content: space-between">
        <router-link :to="{ path: '/toanalysis', query: { id: this.id } }">
          <el-button type="warning" round class="toAnauserButton"
            >进入题目分析详情</el-button
          >
        </router-link>

        <el-button type="primary" plain class="printpdfButton" @click="toprint">
          导出数据</el-button
        >

        <router-link :to="{ path: '/tomanage', query: { id: this.id } }">
          <el-button type="success" class="tomanageButton1">
            返回主页</el-button
          ></router-link
        >
      </div>

      <div class="title">{{ this.name }}</div>
      <!-- <div class="title">{{ this.name }}</div> -->
      <!-- this.$route.query.id -->
      <div class="total">共计{{ this.totalNum }}条数据</div>
      <div class="line"></div>

      <table class="choices" id="platform">
        <tr class="choicestitle">
          <th>用户名</th>
          <th>填写时间</th>
          <th v-for="item in length">第{{ item }}题</th>
        </tr>
        <tr v-for="ques in statistic" :key="ques.index">
          <th>{{ ques.username }}</th>

          <th>{{ ques.date }}</th>

          <th v-for="item in length">
            {{ ques.choices[item - 1].answer }}
          </th>
        </tr>
        <!-- <tr v-for="i in length">
          <th>asdfasfd</th>
          <th>2020.12.23:15:52:00</th>
          <th v-for="item in length">asdfsadf123213</th>
        </tr> -->
      </table>
    </div>
  </div>
</template>

<style scoped src="../css/AnalysisForUser.css">
</style>

<script>
import { request } from "../network/request";
export default {
  data() {
    return {
      id: this.$route.query.id,
      name: "",
      totalNum: "",
      statistic: [],
      //length: 100,
      length: "",
    };
  },
  methods: {
    toprint() {
      request({
        url: "/printf",
        method: "get",
        params: {
          id: this.id,
        },
      }).then((res) => {
        console.log(res), saveFile(res, fileName + ".csv");
      });
    },
    saveFile(data, fileName) {
      let blob = new Blob([data], {
        type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
      }); // res就是接口返回的文件流了

      let url = window.URL || window.webkitURL;

      let fileURL = url.createObjectURL(blob);

      let a = document.createElement("a");

      a.href = fileURL;

      a.download = fileName;

      a.target = "_self";

      a.click();

      url.revokeObjectURL(fileURL);
    },

    printpdf() {
      var bodyData = document.body.innerHTML;
      var printData = document.getElementById("platform").innerHTML; // 只打印 forPrint 这个div中的内容。
      window.document.body.innerHTML = printData; //把 html 里的数据 复制给 body 的 html 数据 ，相当于重置了整个页面的 内容
      window.print();
      window.document.body.innerHTML = bodyData;
      location.reload();
      return;
    },
  },
  created() {
    if (!this.$store.state.isLogin) {
      this.$router.push("/tologin");
    }
    request({
      url: "/analysisForUser",
      method: "get",
      params: {
        id: this.id,
      },
    }).then((res) => {
      console.log(res),
        (this.statistic = res.data.statistic),
        (this.totalNum = res.data.totalNum),
        (this.name = res.data.name),
        (this.length = this.statistic[0].choices.length);
    });
  },
};
</script>