<template>
    <div id="Text">
        <div id="editStatus" v-if="status == 1">
            <div id="space">
                <div>题目：<input type="text" v-model="this.title"></div>
                <div>备注：<input type="text" v-model="this.description"></div>
                <div id="opt"><input id="must" type="checkbox" v-model="this.must"><span>必填</span></div>
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
                <span>{{theTitle}}</span><span style="color: red"  v-if="theMust">*</span>
            </div>
            <div>{{theDescription}}</div>
            <div>
                <input type="text" id="answer" v-model="this.answer" :readonly="true">
                <el-button @click="ask">获取地址</el-button>
            </div>
            
        </div>
    </div>
</template>

<script>
import { request } from '../network/request';
export default {
    props: {
        needOrder: '',
        number: '',
        status: '',
        theTitle: '',
        theDescription: '',
        theMust: '',
        readOnly: Boolean,
    },
    data(){
        return {
            title: this.theTitle,
            description: this.theDescription,
            must: this.theMust,
            answer: '',
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
        answer(newVal, oldVal){
            this.$emit('getResult', newVal, this.number)
        }
    },
    methods:{
        ask(){
            if(this.readOnly == true){
                this.$message({
                    message: "问卷编辑状态时按钮不可用",
                    type: "warning"
                });
                return;
            }
            this.$confirm('此操作将获取您的当前位置，是否确定', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                showClose: false,
                type: 'success'
                }).then(() => {
                    // this.answer="湖南省 衡阳市"
                    request({
                        url: '/getLocation',
                        method: 'get',
                    }).then(res => {
                        console.log(res),
                        this.answer = res.data.location
                    })
                })
        },
        cancel(){
            this.$emit('result', this.number, 0);
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
                type: 7,
                status: 0,
                number: this.number,
                title: this.title,
                description: this.description == undefined? '' : this.description,
                //description: this.description,
                must: this.must
            }
            this.$emit('result', obj, 1)
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

#answer {
    height: 24px;
    width: 400px;
    font-size: 16px;
    padding: 2px;
    outline: none;
    margin-right: 50px;
}

</style>

