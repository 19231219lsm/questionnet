<template>
    <sapn>
    <img :src = "qusnaire" class="planet" style="width:90px;height:90px;position:absolute;left:50px;top:50px" >
    </sapn>
  <div class="manage">   
    <div class="line"></div>
    <el-menu
    :default-active="activeIndex2"
    class="el-menu-demo"
    mode="horizontal"
    @select="handleSelect"
    text-color="black"
    active-text-color="#1E90FF">
      <el-menu-item index="0"></el-menu-item>
      <!-- <el-submenu index="2">
      <template #title>团队问卷</template>
      <el-menu-item index="2-1">选项1</el-menu-item>
      <el-menu-item index="2-2">选项2</el-menu-item>
      <el-menu-item index="2-3">选项3</el-menu-item>
      <el-submenu index="2-4">
      <template #title>选项4</template>
      <el-menu-item index="2-4-1">选项1</el-menu-item>
      <el-menu-item index="2-4-2">选项2</el-menu-item>
      <el-menu-item index="2-4-3">选项3</el-menu-item>
      </el-submenu>
      </el-submenu> -->
       <!-- <el-menu-item index="3" disabled>更多功能</el-menu-item> -->
        <!-- <el-menu-item index="4"><a href="https://www.ele.me" target="_blank">链接测试</a></el-menu-item> -->
      </el-menu>
      <router-link to="/tologin"><el-button class="returnlo">&lt;&ensp;退出登录</el-button></router-link>
      <router-link to="/"><el-button class="returnmain">&lt;&ensp;返回首页</el-button></router-link>
    <el-row  style="position:absolute;left:30px">
      <el-col style="margin-top:25px"><h4>回收列表</h4> </el-col >     
    <el-col span="10" style="position:absolute;left:680px;width:300px;margin-top:18px"><el-button  style="font-size:14pxl;color:#1E90FF;margin-left:80px;border-width:1px;border-color:black;" @click="deleteall">清空回收站</el-button></el-col>
    </el-row>
    <div class = "list" >
    <div v-if="quscount==0">
      <h2 align="center" style="margin-top:60px">您还没有删除过的问卷</h2>
    </div>
    <template :key="index" v-for="(item, index) in quslist">
    <div class = "qus" style="height:100px">
    <el-row :gutter="12" class="topinfo">
      <el-col span="120" ><div class = "name" style="width:250px;text-align:left"> {{item.name}}</div></el-col>
      <el-col :offset="5" span="12" ><div class = "info" style="font-size:10px;"> ID:{{item.id}}</div></el-col>
      <el-col span="12" ><div class = "info" style="font-size:10px"> 回收量：{{item.recovernum}}</div></el-col>
      <el-col span="12" ><div class = "info" style="font-size:10px">创建时间：{{item.createtime}}</div></el-col>
    </el-row>
    <el-divider class="divide" content-position="center"></el-divider>
    <el-row :gutter="12" class="bottominfo">
     <!-- <el-col span="10" style="font-size:14px;">删除&ensp;<el-button type="danger" icon="el-icon-delete" circle @click="clickdelete(this.quslist[index].id)"></el-button></el-col>-->
      <el-col span="10" :offset="15"  style="font-size:14px;margin-top:-17px">恢复&ensp;<el-button type="success" icon="el-icon-refresh-right " circle @click="clickrecover(this.quslist[index].id)"></el-button></el-col> 
      <!-- <el-col span="10" :offset="15" style="font-size:14px;margin-top:7px">发布&ensp;<el-switch v-model="publishbutton[index]" active-color="#13ce66" inactive-color="#909399" @click="changepub(this.quslist[index].id)"></el-switch></el-col> -->
      <el-col span="10" style="font-size:14px;margin-top:-17px">永久删除&ensp;<el-button type="danger" icon="el-icon-delete" circle @click="clickdelete(this.quslist[index].id)"></el-button></el-col>
    </el-row>
    </div>
    </template>
    </div>
  </div>
  <el-row class="switch">
  <el-col :span="36"  style="width:170px" >
    <el-menu
      default-active="2"
      class="el-menu-vertical-demo"
      @open="handleOpen"
      @close="handleClose">
      <router-link to="/tomanage" style="text-decoration: none;">
      <el-menu-item index="1">
        <i class="el-icon-user"></i>
        <template #title>个人问卷</template>
      </el-menu-item>
      </router-link>
      <router-link to="/torecycle" style="text-decoration: none;">
       <el-menu-item index="2">
        <i class="el-icon-delete"></i>
        <template #title >回收站</template>
      </el-menu-item> 
      </router-link>
    </el-menu>
    </el-col>
  </el-row>
  <div class="qusname">
    <h1>问卷星球</h1>
  </div>
  <div class="new">
     <el-dropdown>
  <el-button type="primary" style="width:170px;height:70px">
    创建问卷 +<i class="el-icon-arrow-down el-icon--right"></i>
  </el-button>
  <template #dropdown>
    <el-dropdown-menu>
      <router-link :to="{ path: '/toedit', query: { id:2333333}}" style="text-decoration: none"
            ><el-dropdown-item>普通问卷</el-dropdown-item></router-link
          >
          <router-link :to="{ path: '/tovote', query: { id:2333333}}" style="text-decoration: none"
            ><el-dropdown-item>投票问卷</el-dropdown-item></router-link
          >
          <router-link :to="{ path: '/toexam', query: { id:2333333}}" style="text-decoration: none"
            ><el-dropdown-item>考试问卷</el-dropdown-item></router-link
          >
          <router-link :to="{ path: '/toapply', query: { id:2333333}}" style="text-decoration: none"
            ><el-dropdown-item>报名问卷</el-dropdown-item></router-link
          >
          <router-link :to="{ path: '/toepidemic', query: { id:2333333}}" style="text-decoration: none"
            ><el-dropdown-item>疫情打卡</el-dropdown-item></router-link
          >
      <!-- <el-dropdown-item>投票问卷</el-dropdown-item>
      <el-dropdown-item>考试问卷</el-dropdown-item> -->
    </el-dropdown-menu>
  </template>
</el-dropdown>
  </div>
</template>
<script>
  import {request} from '../network/request';
  import { ElMessage } from 'element-plus'
  export default {
    data() {
      return {
        qusnaire:'https://pic1.zhimg.com/v2-5dfc909d8627c054a6f66f978831a0de_1440w.jpg?source=172ae18b',
        activeIndex: '1',
        activeIndex2: '1',
        count:0,
        quscount:0,
        publishbutton:[],
        search:"",
       quslist1:[{
          id:"1281245490",
          name:"名字",
          createtime:"2021-08-22 11:10",
          publish_at:"2021-08-22 11:40",
          recovernum:"0",
          publish_status:"false"
        },{
          id:"9912454990",
          name:"名字2",
          createtime:"2021-08-23 11:10",
          publish_at:"2021-08-24 11:40",
          recovernum:"2",
          publish_status:"false"
        },{
          id:"6681249990",
          name:"名字3dasdsadadadsadad",
          createtime:"2021-08-22 10:10",
          publish_at:"2021-08-22 10:40",
          recovernum:"4",
          publish_status:"false"
        }],
        quslist:[],
      };
    },
    created:function(){
      if (!this.$store.state.isLogin) {
      this.$router.push("/tologin");
    }
      console.log("chushihua");
       request({
                url: '/recycle',
                method: "post",
                data: {
                    type:1,
                }
            }).then(res => {
                console.log(res);
                let i=0;
                this.quslist = res.data.res;
                console.log(res.data.res);
                this.quscount = this.quslist.length;
            })
    },
    methods: {
      handleSelect(key, keyPath) {
        console.log(key, keyPath);
      },
       handleOpen(key, keyPath) {
        console.log(key, keyPath);
      },
      handleClose(key, keyPath) {
        console.log(key, keyPath);
      },
      clickedit(index){
        console.log("编辑"+index)
        return;
      },
      deleteall(e){
          console.log("deleteALL")
          let target = e.target
          if(target.nodeName == "SPAN"||target.nodeName == "I"){
            target = e.target.parentNode;
        }
        target.blur();
         request({
                url: '/recycle',
                method: "post",
                data: {
                    type:4,
                }
            });
        this.quslist =[];
        this.quscount = 0;
      },
      changepub(id){
          console.log("change");
          request({
                url: '/manage',
                method: "post",
                data: {
                    type:1,
                    survey_id:id,
                }
            });
        return;
      },
      clickdelete(id){
        console.log("foreverdelete");
        this.$confirm('此操作将永久删除该问卷, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
            request({
                url: '/recycle',
                method: "post",
                data: {
                    type:3,
                    survey_id:id,
                }
            }).then(res => {
                console.log(res);
                let i=0;
                this.quslist = res.data.res;
                this.quscount = this.quslist.length;
            });
          this.$message({
            type: 'success',
            message: '删除成功!'
          });
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消删除'
          });
        });
      
        return;
      },
      clickrecover(id){
        console.log("recovery")
        request({
                url: '/recycle',
                method: "post",
                data: {
                    type:2,
                    survey_id:id,
                }
            }).then(res => {
                console.log(res);
                let i=0;
                this.quslist = res.data.res;
                this.quscount = this.quslist.length;
            });
        ElMessage.success({
            message: '该问卷已成功恢复',
            type: 'success',
            center:true
          });
        return;
      },
    }
  }
</script>
<style >
.manage{
  position:absolute;
  left:200px;
  top:10px;
  width:86%
}
.returnlo{
  position:absolute;
  right:350px;
  top:10px;
  color:#1E90FF
}
.returnmain{
  position:absolute;
  right:220px;
  top:10px;
  color:#1E90FF
}
.qusname{
  position:absolute;
  left:30px;
  top:10px
}
.new{
  position:absolute;
  left:10px;
  top:160px;
}
.switch{
  position:absolute;
  left:10px;
  top:240px;
  width:170px
}
.list{
  position:absolute;
  top:140px;
  left:50px;
  width:1000px;
  height:120px;
}
.qus{
  border:1px solid rgb(221, 211, 211);
  width:1000px;
  height:100px;
  margin-bottom: 10px;
}
.topinfo{
  left:30px;
  top:10px;
}
.divide{
  width: 94%;
  margin-left: 3%;

}
</style>
