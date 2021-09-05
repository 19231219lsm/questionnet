<template>
    <div id="Preview">
        <div id="nav">
            <div id="realNav">
                <img src="https://pic1.zhimg.com/v2-5dfc909d8627c054a6f66f978831a0de_1440w.jpg?source=172ae18b" alt="">
                <h1 >问卷星球</h1>
                <span @click="tomanage">个人问卷</span>
            </div>
            <div id="option">
                <el-button @click="download">导出为PDF</el-button>
                <el-button @click="edit">编辑问卷</el-button>
            </div>
        </div>  
        <div id="mainPart">
            <div id="surveyTitle">
                {{data.titleContent}}
            </div>
            <div id="surveyIntro">
                {{data.info}}
            </div>
            <div 
            class="surveyContent" 
            v-for="ques in data.survey"
            :key ="ques.index"
            >
                <Radio 
                v-if="ques.type==1"
                :needOrder="data.needOrder"
                :number="ques.number"
                :status="0"
                :theTitle="ques.title"
                :theDescription="ques.description"
                :theChoices="ques.choices"
                :theMust="ques.must"
                :readOnly="this.readOnly"
                @getResult="change"
                >
                </Radio>

                <Checkbox 
                v-if="ques.type==2"
                :needOrder="data.needOrder"
                :number="ques.number"
                :status="0"
                :theTitle="ques.title"
                :theDescription="ques.description"
                :theChoices="ques.choices"
                :theMust="ques.must"
                :readOnly="this.readOnly"
                @getResult="change"
                >
                </Checkbox>

                <Text 
                v-if="ques.type==3"
                :needOrder="data.needOrder"
                :number="ques.number"
                :status="0"
                :theTitle="ques.title"
                :theDescription="ques.description"
                :theMust="ques.must"
                :readOnly="this.readOnly"
                @getResult="change"
                >
                </Text>

                <Evaluation
                v-if="ques.type==4"
                :needOrder="data.needOrder"
                :number="ques.number"
                :status="0"
                :theTitle="ques.title"
                :theDescription="ques.description"
                :theMust="ques.must"
                :theChoices="ques.choices"
                :readOnly="this.readOnly"
                @getResult="change"
                >
                </Evaluation>

                <Judge
                v-if="ques.type==5"
                :needOrder="data.needOrder"
                :number="ques.number"
                :status="0"
                :theTitle="ques.title"
                :theDescription="ques.description"
                :theMust="ques.must"
                :readOnly="this.readOnly"
                @getResult="change"
                >
                </Judge>

                <Location
                v-if="ques.type==7"
                :needOrder="data.needOrder"
                :number="ques.number"
                :status="0"
                :theTitle="ques.title"
                :theDescription="ques.description"
                :theMust="ques.must"
                :readOnly="this.readOnly"
                @getResult="change"
                >
                </Location>

                <Limitation
                v-if="ques.type==6"
                :needOrder="data.needOrder"
                :number="ques.number"
                :status="0"
                :theTitle="ques.title"
                :theDescription="ques.description"
                :theMust="ques.must"
                :theChoices="ques.choices"
                :readOnly="this.readOnly"
                @getResult="change"
                >
                </Limitation>
            </div>
            <div id="btn">
                <el-button @click="upload">提交问卷</el-button>
            </div>
        </div>
    </div>
</template>

<style src="../css/Preview.css" scoped></style>

<script>
import Radio from "../components/Radio.vue"
import Checkbox from "../components/Checkbox.vue"
import Text from "../components/Text.vue"
import Evaluation from "../components/Evaluation.vue"
import Judge from "../components/Judge.vue"
import Location from "../components/Location.vue"
import Limitation from "../components/Limitation.vue"
import {request} from '../network/request';

export default {
    components: {
        Radio,Checkbox, Text, Evaluation, Judge, Location, Limitation
    },
    data(){
        return {
            data: {
                // titleContent: "我的第一份问卷",
                titleContent: '',
                // info: "希望你喜欢",
                info: '',
                needOrder: true,
                survey: [],
                class: '',
                stopTime: ''
            },
            readOnly: true,
        }
    },
    // mounted(){
    //     window.onbeforeunload = e => {
    //         return '';
    //     };
    // },
    methods: {
        edit(){
            if(this.data.class == 1){
                this.$router.push({
                    path: '/toedit', 
                    query: { id: this.$route.query.id}
                })
            }
            else if(this.data.class == 2){
                this.$router.push({
                    path: '/tovote', 
                    query: { id: this.$route.query.id}
                })
            }
            else if(this.data.class == 3){
                this.$router.push({
                    path: '/toapply', 
                    query: { id: this.$route.query.id}
                })
            }
            else if(this.data.class == 4){
                this.$router.push({
                    path: '/toexam', 
                    query: { id: this.$route.query.id}
                })
            }
            else if(this.data.class == 5){
                this.$$router.push({
                    path: '/toepidemic', 
                    query: { id: this.$route.query.id}
                })
            }
        },
        tomanage(){
            this.$router.push("/tomanage");
        },
        tohome(){
            this.$router.push("/");
            
        },
        change(i, num){
            console.log(this.data)
            console.log(this.data.survey)
            this.data.survey[num-1].answer = i;
        },
        download() {
          var bodyData = document.body.innerHTML;
          var printData = document.getElementById("platform").innerHTML; // 只打印 forPrint 这个div中的内容。
          window.document.body.innerHTML = printData; //把 html 里的数据 复制给 body 的 html 数据 ，相当于重置了整个页面的 内容
          window.print();
          window.document.body.innerHTML = bodyData;
          location.reload();
          return;
        },
        upload(){
            for(var i in this.data.survey){
                if(this.data.survey[i].answer.length == 0 && this.data.survey[i].must==1){
                    this.$message({
                        message: "请至少填写问卷所有必答题",
                        type: "warning"
                        });
                    return;
                }
            }
            this.$message({
                message: "预览状态下不可提交问卷",
                type: "warning"
                });
        },
        download(){
            var bodyData = document.body.innerHTML;
            var printData = document.getElementById("mainPart").innerHTML; // 只打印 forPrint 这个div中的内容。
            window.document.body.innerHTML = printData;   //把 html 里的数据 复制给 body 的 html 数据 ，相当于重置了整个页面的 内容
            window.print(); 
            window.document.body.innerHTML = bodyData;
            return;
        }
    },
    created(){
        if (!this.$store.state.isLogin) {
            this.$router.push("/tologin");
            return
        }
        var obj1 = {
            type: 1,
            number: 1,
            title: "第一个问题",
            description: "此时无声胜有声",
            must: true,
            choices: ["Apple", "Samsung", "Huawei"],
            answer: ''
        }
        var obj2 = {
            type: 2,
            number: 2,
            title: "第二个问题",
            description: "银瓶乍破水浆迸",
            must: false,
            choices: ["Xiaomi", "Vivo", "Oppo", "Meizu"],
            answer: ''
        }
        var obj3 = {
            type: 3,
            number: 3,
            title: "第三个问题",
            description: "春江潮水连海平",
            must: true,
            choices: ["Xiaomi", "Vivo", "Oppo", "Meizu"],
            answer: ''
        }
        var obj4 = {
            type: 4,
            number: 4,
            title: "第四个问题",
            description: "海上明月共潮生",
            must: false,
            choices: 10,
            answer: ''
        }
        var obj5 = {
            type: 5,
            number: 5,
            title: "第五个问题",
            description: "人面不知何处去",
            must: true,
            choices: ["Xiaomi", "Vivo", "Oppo", "Meizu"],
            answer: ''
        }
        // this.data.survey.push(obj1)
        // this.data.survey.push(obj2)
        // this.data.survey.push(obj3)
        // this.data.survey.push(obj4)
        // this.data.survey.push(obj5)

        request({
             url:"/survey",
             method: "get",
             params: {
                 id: this.$route.query.id,
                editStatus: 1,
             }
         }).then(res => {
            console.log(res);
            this.data = res.data;
         })
    }
}
</script>