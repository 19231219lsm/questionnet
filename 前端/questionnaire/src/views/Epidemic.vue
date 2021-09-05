<template>
    <div id="nav">
        <div id="realNav">
            <img src="https://pic1.zhimg.com/v2-5dfc909d8627c054a6f66f978831a0de_1440w.jpg?source=172ae18b" alt="">
            <h1 >问卷星球</h1>
            
            <span @click="tomanage">个人问卷</span>
            <span style="color: rgb(71,157,230)">疫情打卡问卷</span>
        </div>
        <div id="btn">
            <el-button id="safe" @click="saveSurvey">保存</el-button>
            <el-button id="release" @click="releaseSurvey">发布</el-button>
        </div>
    </div>  
    <div id="Edit">
        <div id="left">
            <div class="title">
                题目控件
            </div>
            <div class="questionList">
                <div class="questionType" @click="addRadio">
                    <i class="el-icon-success"></i>
                    单选题
                </div>
                <div class="questionType" @click="addCheckbox">
                    <i class="el-icon-s-fold"></i>
                    多选题
                </div>
                <div class="questionType" @click="addText">
                    <i class="el-icon-s-order"></i>
                    填空题
                </div>
                <div class="questionType" @click="addEvaluation">
                    <i class="el-icon-star-on"></i>
                    评分题
                </div>
                <div class="questionType" @click="addLocation">
                    <i class="el-icon-position"></i>
                    定位题
                </div>
                <div class="option" style="margin-bottom: 20px">
                    <input type="checkbox" v-model="needOrder">
                    自动插入题号
                </div>
                <div class="option">
                    <el-date-picker
                    v-model="stopTime"
                    type="datetime"
                    placeholder="问卷收集截止时间"
                    >
                    </el-date-picker>
                </div>
            </div>
        </div>
        <div id="right">
            <div id="platform">
                <div id="surveyTitle">
                    <input id="titleContent" type="text" placeholder="问卷标题" v-model="titleContent">
                </div>
                <div id="surveyIntro">
                    <textarea
                    id="introContent"
                    v-model="this.info"
                    ></textarea>
                </div>
                <transition-group tag="div" class="container">
                    <div 
                    class="surveyContent" 
                    v-for="ques in survey"
                    :key ="ques.index"
                    draggable="!ques.status"
                    @dragstart="handleDragStart($event, ques)"
                    @dragover.prevent="handleDragOver($event, ques)"
                    @dragenter="handleDragEnter($event, ques)"
                    @dragend="handleDragEnd($event, ques)"
                    >
                    <Radio 
                    v-if="ques.type==1"
                    :needOrder="this.needOrder"
                    :number="ques.number"
                    :status="ques.status"
                    :theTitle="ques.title"
                    :theDescription="ques.description"
                    :theChoices="ques.choices"
                    :theMust="ques.must"
                    :readOnly="this.readOnly"
                    @result="change"
                    >
                    </Radio>

                    <Checkbox 
                    v-if="ques.type==2"
                    :needOrder="this.needOrder"
                    :number="ques.number"
                    :status="ques.status"
                    :theTitle="ques.title"
                    :theDescription="ques.description"
                    :theChoices="ques.choices"
                    :theMust="ques.must"
                    :readOnly="this.readOnly"
                    @result="change"
                    >
                    </Checkbox>

                    <Text 
                    v-if="ques.type==3"
                    :needOrder="this.needOrder"
                    :number="ques.number"
                    :status="ques.status"
                    :theTitle="ques.title"
                    :theDescription="ques.description"
                    :theMust="ques.must"
                    :readOnly="this.readOnly"
                    @result="change"
                    >
                    </Text>

                    <Evaluation
                    v-if="ques.type==4"
                    :needOrder="this.needOrder"
                    :number="ques.number"
                    :status="ques.status"
                    :theTitle="ques.title"
                    :theDescription="ques.description"
                    :theMust="ques.must"
                    :theChoices="ques.choices"
                    :readOnly="this.readOnly"
                    @result="change"
                    >
                    </Evaluation>

                    <Location
                    v-if="ques.type==7"
                    :needOrder="this.needOrder"
                    :number="ques.number"
                    :status="ques.status"
                    :theTitle="ques.title"
                    :theDescription="ques.description"
                    :theMust="ques.must"
                    :readOnly="this.readOnly"
                    @result="change"
                    >
                    </Location>

                    <div class="tool" v-if="ques.status==0">
                        <el-button @click="modify(ques.number)">编辑</el-button>
                        <el-button @click="backspace(ques.number)">删除</el-button>
                        <el-button @click="copy(ques.number)">复制</el-button>
                    </div>

                    </div>
                </transition-group>
            </div>
        </div>
    </div>
</template>

<style src="../css/Epidemic.css" scoped></style>

<script>
import Radio from "../components/Radio.vue"
import Checkbox from "../components/Checkbox.vue"
import Text from "../components/Text.vue"
import Evaluation from "../components/Evaluation.vue"
import Judge from "../components/Judge.vue"
import Location from "../components/Location.vue"
import {request} from '../network/request';
import { h } from 'vue';

export default {
    components: {
        Radio,Checkbox, Text, Evaluation, Judge, Location
    },
    data(){
        return {
            dragging: null,
            survey: [],
            counter: 1,//题号
            newPos: '',
            oldPos: '',
            readOnly: true, 
            needOrder: true,
            titleContent: '',
            stopTime: '',
            info: "为了给您提供更好的服务，希望您能抽出几分钟时间，将您的感受和建议告诉我们，我们非常重视每位用户的宝贵意见，期待您的参与！现在我们就马上开始吧！"
        }
    },
    created(){
        if (!this.$store.state.isLogin) {
            this.$router.push("/tologin");
            return
        }
        if(this.$route.query.id == 2333333){
            
            var obj1 = {
                type: 3,
                number: 1,
                status: 0,
                title: "学号",
                description: " ",
                must: true,
                choices: [],
            }
            var obj2 = {
                type: 3,
                number: 2,
                status: 0,
                title: "姓名",
                description: " ",
                must: true,
                choices: [],
            }
            var obj3 = {
                type: 1,
                number: 3,
                status: 0,
                title: "今日体温",
                description: " ",
                must: true,
                choices: ["36度以下", "36度-37.2度之间", "37.3度及以上"],
            }
            var obj4 = {
                type: 1,
                number: 4,
                status: 0,
                title: "是否在十四天内去过高风险地区",
                description: " ",
                must: true,
                choices: ["是", "否"],
            }
            var obj5 = {
                type: 1,
                number: 5,
                status: 0,
                title: "有无新冠肺炎症状",
                description: "发热、干咳、乏力等",
                must: true,
                choices: ["有", "无"],
            }
            var obj6 = {
                type: 7,
                number: 6,
                status: 0,
                title: "所在地址",
                description: " ",
                must: true,
                choices: [],
            }
            this.survey.push(obj1),
            this.survey.push(obj2),
            this.survey.push(obj3),
            this.survey.push(obj4),
            this.survey.push(obj5),
            this.survey.push(obj6),
            console.log(this.survey)
            this.counter = 7
            return;
        }
        request({
            url:"/survey",
            method: "get",
            params: {
                id: this.$route.query.id,
                editStatus: 1,
            }
        }).then(res => {
            console.log(res);
            this.survey= res.data.survey,
            this.needOrder = res.data.needOrder,
            this.titleContent = res.data.titleContent,
            this.info = res.data.info,
            this.stopTime = res.data.stopTime
        })
    },
    methods: {
        tomanage(){
            this.$confirm('跳转页面将不会保存您此次的编辑内容，是否继续？', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
                }).then(() => {
                    this.$router.push("/tomanage");
                });
            
        },
        tohome(){
            this.$confirm('回到主页将不会保存您此次的编辑内容，是否继续？', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
                }).then(() => {
                    this.$router.push("/");
                });
            
        },
        addRadio(){
            if(this.survey.length > 0){
                for(var o in this.survey){
                    if(this.survey[o].status == "1"){
                        this.$message('请先完成或取消当前问题的编辑');
                        return;
                    }
                }
            }
            var obj = {
                title: '',
                description: '',
                type: 1,
                status: 1,
                must: true,
                number: this.counter,
                choices:['','']
            }
            this.survey.push(obj);
            this.counter++;
        },
        addCheckbox(){
            if(this.survey.length > 0){
                for(var o in this.survey){
                    if(this.survey[o].status == "1"){
                        this.$message('请先完成或取消当前问题的编辑');
                        return;
                    }
                }
            }
            var obj = {
                title: '',
                description: '',
                type: 2,
                status: 1,
                must:true,
                number: this.counter,
                choices:['','']
            }
            this.survey.push(obj);
            this.counter++;
            console.log(this.survey)
        },
        addText(){
            if(this.survey.length > 0){
                for(var o in this.survey){
                    if(this.survey[o].status == "1"){
                        this.$message('请先完成或取消当前问题的编辑');
                        return;
                    }
                }
            }
            var obj = {
                title: '',
                description: '',
                type: 3,
                status: 1,
                must:true,
                number: this.counter
            }
            this.survey.push(obj);
            this.counter++;
            console.log(this.survey)
        },
        addEvaluation(){
            if(this.survey.length > 0){
                for(var o in this.survey){
                    if(this.survey[o].status == "1"){
                        this.$message('请先完成或取消当前问题的编辑');
                        return;
                    }
                }
            }
            var obj = {
                title: '',
                description: '',
                type: 4,
                status: 1,
                must:true,
                number: this.counter,
                choices: 5
            }
            this.survey.push(obj);
            this.counter++;
            console.log(this.survey)
        },
        addLocation(){
            if(this.survey.length > 0){
                for(var o in this.survey){
                    if(this.survey[o].status == "1"){
                        this.$message('请先完成或取消当前问题的编辑');
                        return;
                    }
                }
            }
            var obj = {
                title: '',
                description: '',
                type: 7,
                status: 1,
                must:true,
                number: this.counter,
            }
            this.survey.push(obj);
            this.counter++;
            console.log(this.survey)
        },
        change(obj, i){
            console.log(this.survey)
            if(i == 0){
                this.survey.splice(obj-1, 1)
                const len = this.survey.length
                for(var o = 0; o < len; o ++){
                    this.survey[o].number = o+1
                }
                this.counter--;
                this.$message({
                    message: "成功删除",
                    type: "success"
                    });
            }
            else{
                this.survey[obj.number-1]=obj;
                this.$message({
                    message: "成功添加",
                    type: "success"
                    });
            }
            console.log(this.survey)
        },
        modify(i){
            for(var o in this.survey){
                if(this.survey[o].status == "1"){
                    this.$message('请先完成或取消当前问题的编辑');
                    return;
                }
            }
            this.survey[i-1].status=1;
        },
        backspace(i){
            for(var o in this.survey){
                if(this.survey[o].status == "1"){
                    this.$message('请先完成或取消当前问题的编辑');
                    return;
                }
            }
            this.survey.splice(i-1, 1);
            this.counter--;
            var len = this.survey.length;
            for(var j=i-1; j < len; j ++){
                this.survey[j].number --;
            }
        },
        copy(i){
            for(var o in this.survey){
                if(this.survey[o].status == "1"){
                    this.$message('请先完成或取消当前问题的编辑');
                    return;
                }
            }
            var obj = {
                type: this.survey[i-1].type,
                status: this.survey[i-1].status,
                number: this.counter,
                title: this.survey[i-1].title,
                description: this.survey[i-1].description,
                must: this.survey[i-1].must,
                choices: this.survey[i-1].choices
            }
            this.survey.push(obj)
            this.counter++;
            var height = document.body.clientHeight;
            window.scroll({ top: height , left: 0, behavior: 'smooth' });

        },
        
        handleDragStart(e,item){
            for(var o in this.survey){
                    if(this.survey[o].status == "1"){
                        this.$message('请先完成或取消当前问题的编辑');
                        return;
                    }
                }
            this.dragging = item;
        },
        handleDragEnd(e,item){
            this.dragging = null
        },
        //首先把div变成可以放置的元素，即重写dragenter/dragover
        handleDragOver(e) {
            if(this.dragging == null){
                return;
            }
            e.dataTransfer.dropEffect = 'move'// e.dataTransfer.dropEffect="move";//在dragenter中针对放置目标来设置!
        },
        handleDragEnter(e,item){
            if(this.dragging == null){
                return;
            }
            e.dataTransfer.effectAllowed = "move"//为需要移动的元素设置dragstart事件
            if(item === this.dragging){
            return
            }
            const newItems = [...this.survey]
            console.log(newItems)
            const oldPos = newItems.indexOf(this.dragging)
            const newPos = newItems.indexOf(item)
            
            newItems.splice(newPos, 0, ...newItems.splice(oldPos, 1))
            
            this.survey = newItems

            const len = this.survey.length
            for(var o = 0; o < len; o ++){
                this.survey[o].number = o+1
            }
        },
        saveSurvey(){


            if(this.survey.length == 0){
                this.$message({
                    message: "请为问卷设置至少一个问题",
                    type: "warning"
                    });
                return;
            }
            for(var o in this.survey){
                if(this.survey[o].status == "1"){
                    this.$message('请先完成或取消当前问题的编辑');
                    return;
                }
            }
            if(this.titleContent.length == 0){
                this.$message({
                    message: "请填写问卷标题",
                    type: "warning"
                    });
                return;
            }
            if(this.stopTime.length == 0){
                this.$message({
                    message: "请填写问卷收集截止时间",
                    type: "warning"
                    });
                return;
            }
            var date = new Date()
            if(this.stopTime < date){
                this.$message({
                    message: "请设置有效的问卷截止时间",
                    type: "warning"
                    });
                return;
            }
            request({
                url: '/edit',
                method: "post",
                data: {
                    type: 1,
                    class: 5,
                    survey: this.survey,
                    needOrder: this.needOrder,
                    titleContent: this.titleContent,
                    info: this.info,
                    stopTime: this.stopTime,
                    id: this.$route.query.id,
                }
            }).then(res => {
                console.log(res);
                if(res.data.res == 1){
                    this.$message({
                    message: "保存问卷成功",
                    type: "success"
                    });
                    this.$router.push({path: '/tomanage'});
                }
                
            })
        },
        releaseSurvey(){
            if(this.survey.length == 0){
                this.$message({
                    message: "请为问卷设置至少一个问题",
                    type: "warning"
                    });
                return;
            }
            for(var o in this.survey){
                if(this.survey[o].status == "1"){
                    this.$message('请先完成或取消当前问题的编辑');
                    return;
                }
            }
            if(this.titleContent.length == 0){
                this.$message({
                    message: "请填写问卷标题",
                    type: "warning",
                    });
                return;
            }
            if(this.stopTime.length == 0){
                this.$message({
                    message: "请填写问卷收集截止时间",
                    type: "warning"
                    });
                return;
            }
            var date = new Date()
            if(this.stopTime < date){
                this.$message({
                    message: "请设置有效的问卷截止时间",
                    type: "warning"
                    });
                return;
            }
            request({
                url: '/edit',
                method: "post",
                data: {
                    type: 2,
                    class: 5,
                    survey: this.survey,
                    needOrder: this.needOrder,
                    titleContent: this.titleContent,
                    info: this.info,
                    stopTime: this.stopTime,
                    id: this.$route.query.id,
                }
            }).then(res => {
                console.log(res);
                this.$msgbox({
                    title: '问卷链接和二维码',
                    message: h('div', {style: 'text-align: center'}, [
                        // h('div', null, '我是一段链接'),
                        h('div', null, res.data.link),
                        h('div', {style: 'display: flex; justify-content: center; padding-top: 20px'}, 
                            // h('img', {src: "https://gitee.com/static/images/logo.svg?t=158106664"})
                            h('img', {src: res.data.photo})
                        )
                    ]),
                    showCancelButton: false,
                    confirmButtonText: '确定',
                    showClose:false
                }).then(action => {
                    this.$router.push({path: '/tomanage'});
                })
            })
        },
    }
}
</script>
