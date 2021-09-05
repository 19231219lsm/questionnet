<template>
  <div>
    <div id="exportPdf">
      <div>adsfasf</div>
      <div>adsffdhfgh</div>

      <table>
        <tr>
          <th>用户名</th>
          <th>学号</th>
          <th>姓名</th>
        </tr>
        <tr>
          <td>asdf</td>
          <td>123</td>
          <td>sdfg</td>
        </tr>
        <tr>
          <td>asdf</td>
          <td>123</td>
          <td>sdfg</td>
        </tr>
      </table>

      <section class="chart-container">
        <el-row>
          <el-col :span="12">
            <div id="chartPie" style="width: 100%; height: 400px"></div>
          </el-col>
        </el-row>
      </section>
    </div>

    <el-button type="warning" round @click="toImg">打印pdf</el-button>
  </div>
</template>
<style scoped>
table tr th,
td {
  border: 2px solid;
}
</style>

<script>
import echarts from "echarts";
import html2canvas from "html2canvas"; // 转为图片
import printJS from "print-js"; // 打印
export default {
  data() {
    return {
      chartPie: null,
    };
  },
  methods: {
    // toImg() {
    //   // 转图片打印
    //   html2canvas(this.$refs.exportPdf, {
    //     backgroundColor: "#ffffff",
    //     useCORS: true,
    //     // width: window.screen.availWidth,
    //     // height: window.screen.availHeight,
    //     windowHeight: document.body.scrollHeight,
    //     y: window.pageYOffset,
    //   }).then((canvas) => {
    //     // let url = canvas.toDataURL('image/jpeg', 1.0)
    //     const url = canvas.toDataURL();
    //     this.img = url;
    //     //打印图片
    //     printJS({
    //       printable: url,
    //       type: "image",
    //       documentTitle: "打印图片",
    //     });
    //     // base64格式图片打印查看
    //     // console.log(url)
    //   });
    // },

    toImg() {
      printJS({
        printable: "exportPdf", //打印区域
        type: "html", //打印类型html，还可以是json，image等，详细写法见官网
        targetStyles: ["*"], //css样式，写成*代表打印样式完全继承你页面的样式
        maxWidth: "800px", //打印界面最大宽度，适当调整可以解决打印页面过宽，显示不完整的问题
      });
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

    drawPieChart() {
      this.chartPie = echarts.init(document.getElementById("chartPie"));
      this.chartPie.setOption({
        title: {
          text: "第一题",
          //   subtext: "纯属虚构",
          x: "center",
        },
        tooltip: {
          trigger: "item",
          formatter: "{a} <br/>{b} : {c} ({d}%)",
        },
        legend: {
          orient: "vertical",
          left: "left",
          //data: ["选择1", "选项2", "选项3", "选项4", "选择5"],
          //data: ["直接访问", "邮件营销", "联盟广告", "视频广告", "搜索引擎"],
        },
        series: [
          {
            name: "访问来源",
            type: "pie",
            radius: "55%",
            center: ["50%", "60%"],
            // data: [
            //   { value: 335, name: "直接访问" },
            //   { value: 310, name: "邮件营销" },
            //   { value: 234, name: "联盟广告" },
            //   { value: 135, name: "视频广告" },
            //   { value: 1548, name: "搜索引擎" },
            // ],
            data: [
              { value: 3, name: "选项1" },
              { value: 6, name: "选项2" },
              { value: 9, name: "选项3" },
              { value: 12, name: "选项4" },
              { value: 15, name: "选项5" },
            ],
            itemStyle: {
              emphasis: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: "rgba(0, 0, 0, 0.5)",
              },
            },
          },
        ],
      });
    },
    drawCharts() {
      this.drawPieChart();
    },
  },
  created() {
    // if (!this.$store.state.isLogin) {
    //   this.$router.push("/tologin");
    // }
  },
  mounted: function () {
    this.drawCharts();
  },
  // updated: function () {
  //     this.drawCharts()
  // }
};
</script>

<style scoped>
.chart-container {
  width: 100%;
  float: left;
}
.el-col {
  padding: 30px 20px;
}
</style>
