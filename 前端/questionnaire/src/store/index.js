import { t } from "element-plus/lib/locale";
import { createStore } from "vuex";

export default createStore({
  state: {
    isLogin: false,
    username: '',
    // survey: [],
    // counter: 1,//题号
    // newPos: '',
    // oldPos: '',
    // needOrder: true,
    // titleContent: '',
    // info: "为了给您提供更好的服务，希望您能抽出几分钟时间，将您的感受和建议告诉我们，我们非常重视每位用户的宝贵意见，期待您的参与！现在我们就马上开始吧！"
  },
  mutations: {
    login(state) {
      state.isLogin = true;
    },
    logout(state) {
      state.isLogin = false;
    },
    setUsername(state, newName) {
      state.username = newName;
    }
    // s1(state, survey) {
    //   state.survey = survey
    // },
    // s2(state, counter) {
    //   state.counter = counter
    // },
    // s3(state, newPos) {
    //   state.newPos = newPos
    // },
    // s4(state, oldPos) {
    //   state.oldPos = oldPos
    // },
    // s5(state, needOrder) {
    //   state.needOrder = needOrder
    // },
    // s6(state, titleContent) {
    //   state.titleContent = titleContent
    // },
    // s7(state, info) {
    //   state.info = info
    // }
  },
  actions: {},
  modules: {},
});
