<template>
  <div class="grey">
    <div class="analysis">
      <div class="title">{{ this.name }}</div>
      <!-- this.$route.query.id -->
      <div class="total">共计{{ this.totalNum }}条数据</div>
      <div class="line"></div>

      <!-- 投票问卷 -->
      <div
        class="statistic"
        v-for="ques in statistic"
        :key="ques.index"
        v-if="this.class == 2"
      >
        <Checkboxana
          v-if="ques.type == 2"
          :quesnumber="ques.quesnumber"
          :isRequired="ques.isRequired"
          :chooseNumber="ques.chooseNumber"
          :chooseRatio="ques.chooseRatio"
          :title="ques.title"
        ></Checkboxana>
        <Judgeana
          v-if="ques.type == 5"
          :quesnumber="ques.quesnumber"
          :isRequired="ques.isRequired"
          :chooseNumber="ques.chooseNumber"
          :chooseRatio="ques.chooseRatio"
          :title="ques.title"
        ></Judgeana>
        <Evaluationana
          v-if="ques.type == 4"
          :quesnumber="ques.quesnumber"
          :isRequired="ques.isRequired"
          :chooseNumber="ques.chooseNumber"
          :chooseRatio="ques.chooseRatio"
          :title="ques.title"
        ></Evaluationana>
        <Radioana
          v-if="ques.type == 1"
          :quesnumber="ques.quesnumber"
          :isRequired="ques.isRequired"
          :chooseNumber="ques.chooseNumber"
          :chooseRatio="ques.chooseRatio"
          :title="ques.title"
        ></Radioana>
      </div>

      <!-- 测试 -->
      <!-- <div class="statistics">
        <Checkboxana
          v-if="statistic[0].type == 2"
          :quesnumber="statistic[0].quesnumber"
          :isRequired="statistic[0].isRequired"
          :chooseNumber="statistic[0].chooseNumber"
          :chooseRatio="statistic[0].chooseRadio"
          :title="statistic[0].title"
        ></Checkboxana>
        <Judgeana
          v-if="statistic[1].type == 5"
          :quesnumber="statistic[1].quesnumber"
          :isRequired="statistic[1].isRequired"
          :chooseNumber="statistic[1].chooseNumber"
          :chooseRatio="statistic[1].chooseRadio"
          :title="statistic[1].title"
        ></Judgeana>
        <Evaluationana
          v-if="statistic[2].type == 4"
          :quesnumber="statistic[2].quesnumber"
          :isRequired="statistic[2].isRequired"
          :chooseNumber="statistic[2].chooseNumber"
          :chooseRatio="statistic[2].chooseRadio"
          :title="statistic[2].title"
          :scores="statistic[2].scores"
        ></Evaluationana>
        <Radioana
          v-if="statistic[3].type == 1"
          :quesnumber="statistic[3].quesnumber"
          :isRequired="statistic[3].isRequired"
          :chooseNumber="statistic[3].chooseNumber"
          :chooseRatio="statistic[3].chooseRadio"
          :title="statistic[3].title"
        ></Radioana>
      </div> -->

      <!-- 考试问卷 -->
      <!-- <div
        class="statistic"
        v-for="ques in statistic"
        :key="ques.index"
        v-if="this.class == 4"
      >
        <CheckboxExamana
          v-if="ques.type == 2"
          :quesnumber="ques.quesnumber"
          :isRequired="ques.isRequired"
          :chooseNumber="ques.chooseNumber"
          :chooseRatio="ques.chooseRatio"
          :title="ques.title"
          :correctAnswer="ques.correctAnswer"
          :correctNumber="ques.correctNumber"
          :correctRatio="ques.correctRatio"
          :point="ques.point"
        ></CheckboxExamana>
        <RadioExamana
          v-if="ques.type == 1"
          :quesnumber="ques.quesnumber"
          :isRequired="ques.isRequired"
          :chooseNumber="ques.chooseNumber"
          :chooseRatio="ques.chooseRatio"
          :title="ques.title"
          :correctAnswer="ques.correctAnswer"
          :point="ques.point"
        ></RadioExamana>
        <EvaluationExamana
          v-if="ques.type == 4"
          :quesnumber="ques.quesnumber"
          :isRequired="ques.isRequired"
          :chooseNumber="ques.chooseNumber"
          :chooseRatio="ques.chooseRatio"
          :title="ques.title"
          :correctAnswer="ques.correctAnswer"
          :point="ques.point"
        ></EvaluationExamana>
        <JudgeExamana
          v-if="ques.type == 5"
          :quesnumber="ques.quesnumber"
          :isRequired="ques.isRequired"
          :chooseNumber="ques.chooseNumber"
          :chooseRatio="ques.chooseRatio"
          :title="ques.title"
          :correctAnswer="ques.correctAnswer"
          :point="ques.point"
        ></JudgeExamana>
      </div> -->
    </div>
  </div>

  <!-- <div class="chooseButton">
    <el-button type="primary" plain>主要按钮</el-button>
    <el-button type="primary" plain>主要按钮</el-button>
  </div> -->
</template>

<style scoped src="../css/Analysis.css">
</style>

<script>
import Checkboxana from "../components/Checkboxana.vue";
import { request } from "../network/request";
import Judgeana from "../components/Judgeana.vue";
import Evaluationana from "../components/Evaluationana.vue";
import Radioana from "../components/Radioana.vue";
import CheckboxExamana from "../components/CheckboxExamana.vue";
import RadioExamana from "../components/RadioExamana.vue";
import JudgeExamana from "../components/JudgeExamana.vue";
import EvaluationExamana from "../components/EvaluationExamana.vue";
export default {
  components: {
    Checkboxana,
    CheckboxExamana,
    JudgeExamana,
    Judgeana,
    Evaluationana,
    EvaluationExamana,
    Radioana,
    RadioExamana,
  },
  data() {
    return {
      id: this.$route.query.id,
      name: "",
      //   titleContent: "asdfg",
      totalNum: "",
      statistic: [],
      class: "", //问卷类型
    };
  },
  created() {
    // var obj1 = {
    //   type: 2,
    //   quesnumber: 10,
    //   isRequired: true,
    //   chooseNumber: ["3", "6", "9", "12"],
    //   chooseRatio: ["10%", "20%", "30%", "40%"],
    //   title: "lalal",
    //   correctAnswer: ["1", "2"],
    //   correctNumber: "7",
    //   correctRatio: "10%",
    //   point: "5",
    // };
    // var obj2 = {
    //   type: 5,
    //   quesnumber: 8,
    //   isRequired: false,
    //   chooseNumber: ["6", "6"],
    //   chooseRatio: ["50%", "50%"],
    //   title: "判断",
    //   correctAnswer: "1",
    //   point: "1",
    // };
    // var obj3 = {
    //   type: 4,
    //   quesnumber: 5,
    //   isRequired: true,
    //   scores: ["1", "2", "3", "4"],
    //   chooseNumber: ["6", "6", "18", "30"],
    //   chooseRatio: ["10%", "10%", "30%", "50"],
    //   correctAnswer: "1",
    //   title: "评分",
    //   point: "10",
    // };
    // var obj4 = {
    //   type: 1,
    //   quesnumber: 2,
    //   isRequired: true,
    //   chooseNumber: ["1", "2", "3", "4"],
    //   chooseRatio: ["10%", "20%", "30%", "40%"],
    //   correctAnswer: "4",
    //   title: "单选",
    //   point: "3",
    // };
    // this.statistic.push(obj1);

    // this.statistic.push(obj3);
    // this.statistic.push(obj4);
    // this.statistic.push(obj2);

    request({
      url: "/analysis",
      method: "get",
      params: {
        id: this.id,
      },
    }).then((res) => {
      console.log(res),
        (this.name = res.data.name),
        (this.statistic = res.data.statistic),
        (this.class = res.data.class),
        (this.totalNum = res.data.totalNum);
    });
  },
};
</script>
