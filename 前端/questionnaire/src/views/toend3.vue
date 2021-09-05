<template>
  <div class="grey">
    <div class="toend3">
      <div class="title">{{ this.name }}</div>
      <div class="line"></div>
      <div class="statistic" v-for="ques in statistic" :key="ques.index">
        <RadioToEnd
          v-if="ques.type == 1"
          :quesnumber="ques.quesnumber"
          :isRequired="ques.isRequired"
          :title="ques.title"
          :quesContent="ques.quesContent"
          :correctAnswer="ques.correctAnswer"
          :yourAnswer="ques.yourAnswer"
          :choicesContent="ques.choicesContent"
          :point="ques.point"
        ></RadioToEnd>
        <CheckboxToEnd
          v-if="ques.type == 2"
          :quesnumber="ques.quesnumber"
          :isRequired="ques.isRequired"
          :title="ques.title"
          :quesContent="ques.quesContent"
          :correctAnswer="ques.correctAnswer"
          :yourAnswer="ques.yourAnswer"
          :choicesContent="ques.choicesContent"
          :point="ques.point"
        ></CheckboxToEnd>
        <JudgeToEnd
          v-if="ques.type == 5"
          :quesnumber="ques.quesnumber"
          :isRequired="ques.isRequired"
          :title="ques.title"
          :quesContent="ques.quesContent"
          :correctAnswer="ques.correctAnswer"
          :yourAnswer="ques.yourAnswer"
          :choicesContent="ques.choicesContent"
          :point="ques.point"
        ></JudgeToEnd>
        <TextToEnd
          v-if="ques.type == 3"
          :quesnumber="ques.quesnumber"
          :isRequired="ques.isRequired"
          :title="ques.title"
          :quesContent="ques.quesContent"
          :correctAnswer="ques.correctAnswer"
          :yourAnswer="ques.yourAnswer"
          :point="ques.point"
        ></TextToEnd>
        <EvaluationToEnd
          v-if="ques.type == 4"
          :quesnumber="ques.quesnumber"
          :isRequired="ques.isRequired"
          :title="ques.title"
          :quesContent="ques.quesContent"
          :correctAnswer="ques.correctAnswer"
          :yourAnswer="ques.yourAnswer"
          :point="ques.point"
        ></EvaluationToEnd>
      </div>
    </div>
  </div>
</template>

 <style src="../css/toend3.css" scope>
</style>

<script>
import RadioToEnd from "../components/RadioToEnd.vue";
import CheckboxToEnd from "../components/CheckboxToEnd.vue";
import JudgeToEnd from "../components/JudgeToEnd.vue";
import TextToEnd from "../components/TextToEnd.vue";
import EvaluationToEnd from "../components/EvaluationToEnd.vue";
import { request } from "../network/request";
export default {
  components: {
    RadioToEnd,
    CheckboxToEnd,
    JudgeToEnd,
    TextToEnd,
    EvaluationToEnd,
  },
  data() {
    return {
      id: this.$route.query.id,
      name: "",
      titleContent: "asdfg",
      totalNum: "",
      statistic: [],
      class: "5", //问卷类型
    };
  },
  created() {
    // var obj1 = {
    //   type: 1,
    //   quesnumber: 10,
    //   isRequired: true,
    //   quesContent:
    //     "css: 控制好宽度一般A4 我调试的是794px多了放不下，小了填不满。当时多页打印的时候，一定要控制好每一个页面内容显示的高度不要超过一个页面，当然根据自己项目来。由于我的项目是每一个页面固定一个页尾部，所以当显示的时候正常排版显示。但是一旦点击了打印预览需要修改这个区域的css让他固定在每一个页面的底部",
    //   choicesContent: ["aa", "bb", "cc", "dd"],
    //   title: "lalal",
    //   correctAnswer: "2",
    //   yourAnswer: "1",
    //   point: "5",
    // };
    // var obj4 = {
    //   type: 2,
    //   quesnumber: 2,
    //   isRequired: true,
    //   quesContent:
    //     "adsfadsfasdfcss: 控制好宽度一般A4 我调试的是794px多了放不下，小了填不满。当时多页打印的时候，一定要控制好每一个页面内容显示的高度不要超过一个页面，当然根据自己项目来。由于我的项目是每一个页面固定一个页尾部，所以当显示的时候正常排版显示。但是一旦点击了打印预览需要修改这个区域的css让他固定在每一个页面的底部",
    //   choicesContent: ["aaaa", "bbb", "ccc", "ddd"],
    //   correctAnswer: ["2", "3"],
    //   yourAnswer: ["1", "2"],
    //   title: "多选题adsf",
    //   point: "3",
    // };
    // var obj2 = {
    //   type: 5,
    //   quesnumber: 8,
    //   isRequired: false,
    //   title: "判断afd",

    //   point: "1",
    //   quesContent:
    //     "判断css: 控制好宽度一般A4 我调试的是794px多了放不下，小了填不满。当时多页打印的时候，一定要控制好每一个页面内容显示的高度不要超过一个页面，当然根据自己项目来。由于我的项目是每一个页面固定一个页尾部，所以当显示的时候正常排版显示。但是一旦点击了打印预览需要修改这个区域的css让他固定在每一个页面的底部",
    //   choicesContent: ["正确", "错误"],

    //   correctAnswer: "2",
    //   yourAnswer: "1",
    // };
    // var obj5 = {
    //   type: 3,
    //   quesnumber: 1,
    //   isRequired: false,
    //   title: "填空afd",

    //   point: "1",
    //   quesContent:
    //     "填空css: 控制好宽度一般A4 我调试的是794px多了放不下，小了填不满。当时多页打印的时候，一定要控制好每一个页面内容显示的高度不要超过一个页面，当然根据自己项目来。由于我的项目是每一个页面固定一个页尾部，所以当显示的时候正常排版显示。但是一旦点击了打印预览需要修改这个区域的css让他固定在每一个页面的底部",

    //   correctAnswer: "我是正确答案",
    //   yourAnswer: "我是你的答案",
    // };
    // var obj3 = {
    //   type: 4,
    //   quesnumber: 5,
    //   isRequired: true,
    //   scores: ["1", "2", "3", "4"],
    //   point: "1",
    //   quesContent:
    //     "评分css: 控制好宽度一般A4 我调试的是794px多了放不下，小了填不满。当时多页打印的时候，一定要控制好每一个页面内容显示的高度不要超过一个页面，当然根据自己项目来。由于我的项目是每一个页面固定一个页尾部，所以当显示的时候正常排版显示。但是一旦点击了打印预览需要修改这个区域的css让他固定在每一个页面的底部",

    //   correctAnswer: "我是5fen ",
    //   yourAnswer: "我是5fen ",
    //   title: "评分",
    // };

    // this.statistic.push(obj1);
    // this.statistic.push(obj4);
    // this.statistic.push(obj2);
    // this.statistic.push(obj5);
    // this.statistic.push(obj3);
    // this.statistic.push(obj4);
    // this.statistic.push(obj2);

    request({
      url: "/toend3",
      method: "get",
      params: {
        id: this.id,
      },
    }).then((res) => {
      console.log(res),
        (this.name = res.data.name),
        (this.statistic = res.data.statistic);
    });
  },
};
</script>


