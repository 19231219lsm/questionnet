<template>
    <div id="Evaluation">
        <div id="editStatus" v-if="status == 1">
            <div id="space">
                <div>题目：<input type="text" v-model="this.title"></div>
                <div>备注：<input type="text" v-model="this.description"></div>
                <div id="opt">
                    <input id="must" type="checkbox" v-model="this.must" style="margin-bottom: 5px">
                    <span>必填</span>
                    <span style="display: flex; align-items: flex-end; margin-left: 40px; line-height: 28px">
                        <!-- 评分星级上限<input id="starNum" type="text" v-model="this.starNum">颗星 -->
                        <span style="width:100px">评分星级上限</span>
                        <el-select v-model="this.starNum" style="margin-bottom: 0px; width:60px" size="mini">
                            <el-option
                            v-for="item in 10"
                            :key="item.index"
                            :value="item">
                            </el-option>
                        </el-select>
                        <span style="width:50px">颗星</span> 
                    </span>
                </div>
                <div id="examAnswer" v-if="this.examStatus" style="margin-top: 20px">
                    答案:
                    <el-select clearable="true" v-model="this.correctAnswer" style="width: 150px; margin: 0 8px; margin-right:0px">
                        <el-option
                        v-for="item in 10"
                        :key="item.index"
                        :value="item">
                        </el-option>
                    </el-select>
                    颗星
                    <span style="margin-left: 10px">分值:</span> 
                    <el-input-number v-model="this.point" :min="0" :max="100" style="width: 200px;margin: 0 8px"></el-input-number>
                </div>
                <div id="process">
                    <el-button id="confirm" @click="confirm">确定</el-button>
                    <el-button id="cancel" @click="cancel">删除</el-button>
                </div>
            </div>
        </div>
        <div id="showStatus" v-else>
            <!-- 此部分的对象应该是 -->
            <div>
                <span id="sequence" v-if="this.needOrder==1">{{this.number}}.</span>
                <span>{{theTitle}}</span><span style="color: red" v-if="theMust">*</span>
                <span v-if="this.examStatus&&this.point">&nbsp;&nbsp;&nbsp;({{this.point}}分)</span>
            </div>
            <div>{{theDescription}}</div>
            <div v-if="this.readOnly">
                <i class="el-icon-star-off" v-for="i in this.starNum" :key="i.index"></i>
            </div>
            <div v-else>
                <span  v-for="i in this.starNum" :key="i.index">
                    <i class="el-icon-star-off" v-if="this.score<=(i-1)" @click="this.score=i"></i>
                    <i class="el-icon-star-on"  v-if="this.score>=i" @click="this.score=i"></i>
                </span>
                <!-- <i class="el-icon-star-off" @click="this.score=1" v-if="this.score==0"></i>
                <i class="el-icon-star-on" @click="this.score=1" v-if="this.score>=1"></i>
                <i class="el-icon-star-off" @click="this.score=2" v-if="this.score<=1"></i>
                <i class="el-icon-star-on" @click="this.score=2" v-if="this.score>=2"></i>
                <i class="el-icon-star-off" @click="this.score=3" v-if="this.score<=2"></i>
                <i class="el-icon-star-on" @click="this.score=3" v-if="this.score>=3"></i>
                <i class="el-icon-star-off" @click="this.score=4" v-if="this.score<=3"></i>
                <i class="el-icon-star-on" @click="this.score=4" v-if="this.score>=4"></i>
                <i class="el-icon-star-off" @click="this.score=5" v-if="this.score<=4"></i>
                <i class="el-icon-star-on" @click="this.score=5" v-if="this.score==5"></i> -->
            </div>

        </div>
    </div>
</template>

<script>
export default {
    props: {
        needOrder: '',
        number: '',
        status: '',
        theTitle: '',
        theDescription: String,
        theMust: '',
        theChoices: Number,
        readOnly: Boolean,
        examStatus: '',
        thePoint: '',
        theCorrectAnswer: ''
    },
    data(){
        return {
            title: this.theTitle,
            description: this.theDescription,
            must: this.theMust,
            score: 0,
            starNum: this.theChoices,
            point: this.thePoint,
            correctAnswer: this.theCorrectAnswer,
        }
    },
    watch:{
        theTitle(newVal, oldVal){
            this.title=newVal;
        },
        theDescription(newVal, oldVal){
            this.description = newVal;
        },
        theMust(newVal, oldVal){
            this.must = newVal
        },
        score(newVal, oldVal){
            this.$emit('getResult', newVal, this.number)
        }
    },
    methods:{
        cancel(){
            this.$emit('result', this.number, 0);
            if(this.examStatus){
                this.$emit('examResult', this.number, 0)
            }
        },
        confirm(){
            if(this.title.length == 0
            ){
                this.$message({
                message: "请填写完整问题信息",
                type: "warning"
                });
                return;
            }
            var obj = {
                type: 4,
                status: 0,
                number: this.number,
                title: this.title,
                description: this.description == undefined? '' : this.description,
                //description: this.description,
                must: this.must,
                choices: this.starNum
            }
            console.log(obj)
            this.$emit('result', obj, 1)
            if(this.examStatus){
                if(this.correctAnswer > this.starNum){
                    this.$message({
                    message: "请提供有效的正确答案",
                    type: "warning"
                    });
                    return;
                }
                var obj2 = {
                    type: 4,
                    status: 0,
                    number: this.number,
                    title: this.title,
                    description: this.description == undefined? '' : this.description,
                    //description: this.description,
                    must: this.must,
                    choices: this.starNum, 
                    point: this.point,
                    correctAnswer: this.correctAnswer
                }
                this.$emit('examResult', obj2, 1)
            }
        }
    }
}
</script>

<style scoped>

#editStatus {
    background-color: rgb(250,250,250);
    border: 1px solid rgb(229,229,229);
    width: 100%;
}

#space {
    margin: 20px 150px;
    width: 60%;
    padding-left: 55px;
}

#space div{
    margin-bottom: 20px;
    width: 100%;
}

#space input {
    height: 24px;
    width: 550px;
    font-size: 16px;
    padding: 2px;
    outline: none;
}

#opt {
    display: flex;
    align-items: flex-end;
    width: 100%;
    line-height: 28px
}

#editStatus #must {
    width: 18px;
    height: 18px;
    margin-right: 10px;
    padding: 0px;
    font-style: 20px;
}

#process {
    margin-top: 40px;
    display: flex;
    flex-direction: row-reverse;
}

#process .el-button{
    margin-right: 20px;
}

#confirm {
    background-color: rgb(71,157,230);
    color: #fff;
}

#showStatus {
    display: flex;
    flex-direction: column;
    justify-content: space-around;
    margin: 20px 150px;
    width: 60%;
    padding-left: 55px;
}

#showStatus div{
    margin-bottom: 15px;
}

#sequence {
    margin-right: 5px;
}

.el-icon-star-off, .el-icon-star-on{
    font-size: 20px;
    margin-right: 10px;
}

#opt #starNum {
    width: 40px;
    text-align: center;
}

</style>

