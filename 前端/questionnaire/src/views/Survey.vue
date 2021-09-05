<template>
    <div id="Survey">
        <div class="time" v-if="data.class==4">
            <div style="color:red; text-align: center">剩余时间</div>
            <div><i class="el-icon-time"></i> {{day}}天{{hour}}时{{minute}}分{{second}}秒</div> 
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

<style src="../css/Survey.css" scoped></style>

<script>
import Radio from "../components/Radio.vue"
import Checkbox from "../components/Checkbox.vue"
import Text from "../components/Text.vue"
import Evaluation from "../components/Evaluation.vue"
import Judge from "../components/Judge.vue"
import Location from "../components/Location.vue"
import Limitation from "../components/Limitation.vue"
import {request} from '../network/request';
import moment from 'moment'

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
                stopTime: String,
                // stopTime: "Sat Aug 28 2021 14:32:23 GMT+0800 (中国标准时间) 0时0分0秒"
            },
            readOnly: false,
            day: 0,
            hour: 0,
            minute: 0,
            second: 0,
        }
    },
    // mounted(){
    //     window.onbeforeunload = e => {
    //         return '';
    //     };
    // },
    methods: {
        change(i, num){
            console.log(this.data)
            console.log(this.data.survey)
            this.data.survey[num-1].answer = i;
        },
        countDown(){
            const end = Date.parse(new Date(this.data.stopTime))+28800000
            const now = Date.parse(new Date())
            const msec = end - now;
            if(msec < 0){
                this.$router.push('/toerror')
                return;
            }
            let day = parseInt(msec / 1000 / 60 / 60 / 24)
            let hr = parseInt(msec / 1000 / 60 / 60 % 24)
            let min = parseInt(msec / 1000 / 60 % 60)
            let sec = parseInt(msec / 1000 % 60)
            this.day = day
            this.hourr = hr > 9 ? hr : '0' + hr
            this.minute = min > 9 ? min : '0' + min
            this.second = sec > 9 ? sec : '0' + sec

            const that = this
            if(min>=0 && sec>=0){
                //倒计时结束关闭订单
                if(min==0 && sec==0){
                    console.log("hahaha")
                    request({
                        url: '/survey',
                        method: 'post',
                        data: {
                            id: this.$route.query.id,
                            data: this.data
                        }
                    }).then(res => {
                        console.log(res) 
                        if(res.data.res == 1){
                            
                            if(this.data.class == 2){//投票问卷，结束页面为投票结果
                                this.$message({
                                message: "投票成功",
                                type: "success"
                                });
                                this.$router.push({
                                    path: '/toend2',
                                    query: { id: this.$route.query.id}
                                    });
                            }
                            else if(this.data.class == 4){//考试问卷，结束页面为考试答案
                                this.$message({
                                message: "考试结束",
                                type: "success"
                                });
                                this.$router.push({
                                    path: '/toend3',
                                    query: { id: this.$route.query.id}
                                })
                            }
                            else{
                                this.$message({
                                message: "已提交问卷",
                                type: "success"
                                });
                                this.$router.push({path: '/toend'});
                            }
                        }
                        else{
                            this.$message({
                            message: "提交问卷失败",
                            type: "warning"
                            });
                        }
                    })
                return
                }
                setTimeout(function () {
                that.countDown()
                }, 1000)
            }
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
            console.log(this.data)
            request({
                url: '/survey',
                method: 'post',
                data: {
                    id: this.$route.query.id,
                    data: this.data
                }
            }).then(res => {
                console.log(res) 
                if(res.data.res == 1){
                    
                    if(this.data.class == 2){//投票问卷，结束页面为投票结果
                        this.$message({
                        message: "投票成功",
                        type: "success"
                        });
                        this.$router.push({
                            path: '/toend2',
                            query: { id: this.$route.query.id}
                            });
                    }
                    else if(this.data.class == 4){//考试问卷，结束页面为考试答案
                        this.$message({
                        message: "考试结束",
                        type: "success"
                        });
                        this.$router.push({
                            path: '/toend3',
                            query: { id: this.$route.query.id}
                        })
                    }
                    else{
                        this.$message({
                        message: "已提交问卷",
                        type: "success"
                        });
                        this.$router.push({path: '/toend'});
                    }
                }
                else{
                    this.$message({
                    message: "提交问卷失败",
                    type: "warning"
                    });
                }
            })
                
        }
    },
    created(){
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
            type: 1,
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
            choices: 5,
            answer: ''
        }
        var obj5 = {
            type: 2,
            number: 4,
            title: "第五个问题",
            description: "人面不知何处去",
            must: true,
            choices: ["Xiaomi", "Vivo", "Oppo", "Meizu"],
            answer: ''
        }
        // this.data.survey.push(obj1)
        // this.data.survey.push(obj2)
        // this.data.survey.push(obj3)
        // this.data.survey.push(obj5)
        // this.data.survey.push(obj3)
        // this.data.survey.push(obj4)
        // this.data.survey.push(obj5)

        request({
             url:"/survey",
             method: "get",
             params: {
                 id: this.$route.query.id,
                editStatus: 0,
             }
         }).then(res => {
             console.log(res);
            if(res.data.status != 1){
               //this.$router.push({path: '/toerror'});
           }
            this.data = res.data;
            this.countDown();
         })
    }
}
</script>