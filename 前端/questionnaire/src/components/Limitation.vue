<template>
    <div id="Radio">
        <div id="editStatus" v-if="status == 1">
            <div id="space">
                <div>题目：<input type="text" v-model="this.title"></div>
                <div>备注：<input type="text" v-model="this.description"></div>
                <div id="opt"><input id="must" type="checkbox" v-model="this.must"><span>必填</span></div>
                <div
                id="choices"
                v-for="item in i"
                :key="item.index"
                >
                    <input type="text" v-model="this.choices[item-1].content" placeholder="选项">
                    <input type="text" v-model="this.choices[item-1].limit" placeholder="限额">
                    <i class="el-icon-circle-close" @click="deleteOption(item-1)"></i>
                </div>
                <el-button id="newOption" @click="addOption">新建选项</el-button>
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
            </div>
            <div>{{theDescription}}</div>
            <ul>
                <li v-for="item in theChoices" :key="item.index">
                    <input type="radio" :class="this.number+''" :name="this.number+''" @click="write" :disabled="check(item.limit)">&nbsp;&nbsp;&nbsp;{{item.content}}
                    <span style="margin-left: 20px; font-size:12px; line-height: 20px">剩余{{item.limit}}</span>
                </li>
            </ul>
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
        theDescription: '',
        theChoices: [],
        theMust: '',
        readOnly: Boolean,
    },
    data(){
        return {
            title: this.theTitle,
            description: this.theDescription,
            must: this.theMust,
            choices: this.theChoices,//2-10个选项，要检查选项是否相同
            i:2,
            answer: ''
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
        theChoices(newVal, oldVal){
            this.choices = newVal
            this.i = this.choices.length
        }
    },
    methods:{
        check(item){
            if(item == 0){
                return true;
            }
            else return this.readOnly;
        },
        write(){
            var radios = document.getElementsByClassName(this.number);
            console.log(radios)
            for(var i = 0; i < radios.length; i ++){
                if(radios[i].checked==true){
                    i++;
                    this.$emit('getResult', i, this.number)
                    return;
                }
            }
        },
        addOption(){
            if(this.i == 10){
                this.$message({
                message: "最多添加10个选项",
                type: "warning"
                });
                return;
            }
            this.i ++;
            this.choices.push({
                content:'',
                limit: ''
            })
        },
        deleteOption(item){
            if(this.i == 2){
                this.$message({
                message: "至少要有两个选项",
                type: "warning"
                });
                return;
            }
            this.choices.splice(item, 1)
            this.i--;
        },
        cancel(){
            this.$emit('result', this.number, 0);
        },
        confirm(){
            console.log(this.choices.length)
            if(this.title.length == 0 ||
            this.choices.length == 0 ||
            this.choices.length == 1 ||
            this.choices.length < this. i
            ){
                this.$message({
                message: "请填写完整问题信息",
                type: "warning"
                });
                return;
            }
            for(var item in this.choices){
                if(this.choices[item].content.length==0 || this.choices[item].limit.length==0){
                    this.$message({
                    message: "请填写完整问题信息",
                    type: "warning"
                    });
                    return;
                }
                const boo = new RegExp('^[1-9][0-9]*$').test(this.choices[item].limit);
                    if(!boo){
                        this.$message.warning('请输入正整数限额');
                        return;
                    }
            }
            const hash = {}
            for (let i = 0; i < this.choices.length; i++) {
                if (hash[this.choices[i].content]) {
                    // 选项重复了
                    this.$message({
                    message: "请不要提供相同的选项",
                    type: "warning"
                    });
                    return;
                    }
                hash[this.choices[i].content] = true
                }
            var obj = {
                type: 6,
                status: 0,
                number: this.number,
                title: this.title,
                description: this.description == undefined? '' : this.description,
                //description: this.description,
                must: this.must,
                choices: this.choices
            }
            this.$emit('result', obj, 1)
        }
    }
}
</script>

<style scoped>

#editStatus {
    background-color: rgb(250,250,250);
    border-top: 1px solid rgb(229,229,229);
    border-bottom: 1px solid rgb(229,229,229);
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

#choices input {
    width: 200px;
    margin-left: 48px;
}

#newOption {
    width: 410px;
    margin-left: 48px;
    height: 20px;
}

#choices i {
    margin-left: 20px;
    height: 18px;
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

li {
    list-style-type: none;
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

ul li{
    margin-bottom: 10px;
}

#sequence {
    margin-right: 5px;
}

</style>

