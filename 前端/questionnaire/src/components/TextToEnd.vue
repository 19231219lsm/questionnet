<template>
  <div class="TextToEnd">
    <div class="firstline">
      <div class="must" v-if="this.isRequired == true">*</div>
      <div class="number">第{{ this.quesnumber }}题：</div>
      <div class="title1">{{ this.title }}</div>
      <div class="quetype">[填空题]</div>
      <div class="quespoint">({{ this.point }}分)</div>
    </div>
    <div class="quesContent">
      {{ this.quesContent }}
    </div>
    <div class="correctAns">
      [正确答案]
      <div class="correctAnswer">
        {{ this.correctAnswer }}
      </div>
    </div>
    <div class="yourAns">
      [你的答案]
      <div class="yourAnswer">
        {{ this.yourAnswer }}
      </div>
      <div class="isCorrect" v-if="this.yourAnswer == this.correctAnswer">
        [ 正确 ]
      </div>
      <div class="notCorrect" v-if="this.yourAnswer != this.correctAnswer">
        [ 错误 ]
      </div>
    </div>
    <div class="line"></div>
  </div>
</template>


<style scoped src="../css/TextToEnd.css">
</style>
<script>
export default {
  props: {
    quesnumber: "",
    isRequired: "",
    scores: [],
    title: "",
    quesContent: "",
    correctAnswer: "",
    yourAnswer: "",
    point: "",
  },
  data() {
    return {
      //   length: this.choicesContent.length,
      array1: [],
    };
  },
  methods: {},
  //   created() {
  //     for (var i = 1; i <= this.length; i++) {
  //       this.array0.push("选项" + i);
  //       this.array1.push({ value: this.chooseNumber[i - 1], name: "选项" + i });
  //     }
  //   },
};
</script>