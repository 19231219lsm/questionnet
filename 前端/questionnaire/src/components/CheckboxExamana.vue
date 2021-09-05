<template>
  <div class="Checkbox-ana">
    <div class="firstline">
      <div class="must" v-if="this.isRequired == true">*</div>
      <div class="number">第{{ this.quesnumber }}题：</div>
      <div class="title">{{ this.title }}</div>
      <div class="quetype">[多选题]</div>
      <div class="quepoint">[{{ this.point }}分]</div>
    </div>
    <table class="choices">
      <tr class="choicestitle">
        <th>选项</th>
        <th>数量</th>
        <th>占比</th>
      </tr>
      <tr v-for="item in length" :key="item.index">
        <td>{{ item }}</td>

        <td>{{ chooseNumber[item - 1] }}</td>
        <td>{{ chooseRatio[item - 1] }}</td>
        <!-- <td>{{ chooseNumber[item - 1] }}</td>
        <td>{{ chooseRatio[item - 1] }}</td> -->
      </tr>
      <!-- <tr>
        <td>合计</td>
        <td></td>
        <td></td>
      </tr> -->
    </table>

    <div class="Pie">
      <el-row>
        <el-col :span="12">
          <div
            :id="this.quesnumber + ''"
            style="width: 100%; height: 400px"
          ></div>
        </el-col>
      </el-row>
    </div>
    <div class="Correct">
      <div class="correctans" style="display: flex">
        [正确答案]:
        <div class="correctAnswers" v-for="item in this.correctAnswer">
          &nbsp;选项{{ item }}
        </div>
      </div>
      <div class="correctnum">[正确人数]: {{ this.correctNumber }}人</div>
      <div class="correctratio">[正确率]: {{ this.correctRatio }}</div>
    </div>

    <div class="line"></div>
  </div>
  <div style="page-break-after: always"></div>
</template>

<style scoped src="../css/CheckboxExamana.css">
</style>

<script>
import echarts from "echarts";
import { request } from "../network/request";

export default {
  props: {
    quesnumber: "",
    isRequired: "",
    chooseNumber: [],
    chooseRatio: [],
    title: "",
    correctAnswer: [],
    correctNumber: "",
    correctRatio: "",
    point: "",
  },
  data() {
    return {
      chartPie: null,
      type: 2,
      length: this.chooseNumber.length,
      array0: [],
      array1: [],
    };
  },
  methods: {
    drawPieChart() {
      this.chartPie = echarts.init(document.getElementById(this.quesnumber));
      this.chartPie.setOption({
        title: {
          text: "第" + this.quesnumber + "题",
          subtext: "共计" + this.length + "个选项",
          x: "center",
        },
        tooltip: {
          trigger: "item",
          formatter: "{a} <br/>{b} : {c} ({d}%)",
        },
        legend: {
          orient: "vertical",
          left: "left",
          //data: this.array,
          //data: ["选择1", "选项2", "选项3", "选项4", "选择5"],
        },
        series: [
          {
            name: "访问来源",
            type: "pie",
            radius: "55%",
            center: ["50%", "60%"],
            data: this.array1,
            // data: [
            //   { value: 3, name: "选项1" },
            //   { value: 6, name: "选项2" },
            //   { value: 9, name: "选项3" },
            //   { value: 12, name: "选项4" },
            //   { value: 15, name: "选项5" },
            // ],
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
    for (var i = 1; i <= this.length; i++) {
      this.array0.push("选项" + i);
      this.array1.push({ value: this.chooseNumber[i - 1], name: "选项" + i });
    }
  },
  mounted: function () {
    this.drawCharts();
  },
};
</script>
