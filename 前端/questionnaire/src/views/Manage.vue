<template>
  <span>
    <img
      :src="qusnaire"
      class="planet"
      style="
        width: 90px;
        height: 90px;
        position: absolute;
        left: 50px;
        top: 50px;
      "
    />
  </span>
  <div class="manage">
    <div class="line"></div>
    <el-menu
      :default-active="activeIndex2"
      class="el-menu-demo"
      mode="horizontal"
      @select="handleSelect"
      text-color="black"
      active-text-color="#1E90FF"
    >
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
    <router-link to="/tologin"
      ><el-button class="returnlo">&lt;&ensp;退出登录</el-button></router-link
    >
    <router-link to="/"
      ><el-button class="returnmain">&lt;&ensp;返回首页</el-button></router-link
    >
    <el-row style="position: absolute; left: 30px">
      <el-col style="margin-top: 25px"><h4>问卷列表</h4> </el-col>
      <el-col
        span="12"
        style="position: absolute; left: 570px; width: 100px; margin-top: 25px"
      >
      <el-dropdown style = "margin-right:-120px">
          <span class="el-dropdown-link"
            >分类<i class="el-icon-arrow-down el-icon--right"></i
          ></span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item @click="clickclass(0)"
                >全部问卷</el-dropdown-item
              >
              <el-dropdown-item @click="clickclass(1)"
                >普通问卷</el-dropdown-item
              >
              <el-dropdown-item @click="clickclass(2)"
                >投票问卷</el-dropdown-item
              >
              <el-dropdown-item @click="clickclass(4)"
                >考试问卷</el-dropdown-item
              >
              <el-dropdown-item @click="clickclass(3)"
                >报名问卷</el-dropdown-item
              >
              <el-dropdown-item @click="clickclass(5)"
                >疫情打卡</el-dropdown-item
              >
            </el-dropdown-menu>
          </template>
        </el-dropdown>
        <el-dropdown >
          <span class="el-dropdown-link"
            >排序<i class="el-icon-arrow-down el-icon--right"></i
          ></span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item @click="clicktime1()"
                >创建时间正序</el-dropdown-item
              >
              <el-dropdown-item @click="clicktime2()"
                >创建时间倒序</el-dropdown-item
              >
              <el-dropdown-item @click="clicktime5()"
                >发布时间正序</el-dropdown-item
              >
              <el-dropdown-item @click="clicktime6()"
                >发布时间倒序</el-dropdown-item
              >
              <el-dropdown-item @click="clicktime3()"
                >回收量顺序</el-dropdown-item
              >
              <el-dropdown-item @click="clicktime4()"
                >回收量倒序</el-dropdown-item
              >
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </el-col>
      <el-col
        span="200px"
        style="position: absolute; left: 680px; width: 300px; margin-top: 18px"
        ><el-input
          placeholder="请输入内容进行搜索"
          prefix-icon="el-icon-search"
          v-model="search"
          @keydown.enter="onSearch()"
        ></el-input
      ></el-col>
      <el-col
        style="position: absolute; left: 980px; width: 300px; margin-top: 18px"
      >
        <el-button type="primary" @click="onSearch()">
          <span style="vertical-align: middle"> 搜索 </span>
        </el-button></el-col
      >
    </el-row>
    <div class="list">
      <div v-if="quscount==0">
      <h2 align="center" style="margin-top:60px">问卷列表为空</h2>
    </div>
      <template :key="index" v-for="(item, index) in finalquslist" >
        <div class="qus" style="width: 1100px; height: 120px">
          <el-row :gutter="12" class="topinfo">
            <el-col span="120"
              ><div class="name" style="width: 250px; text-align: left">
                {{ item.name }}
              </div></el-col
            >
            <el-col :offset="5" span="12"
              ><div class="info" style="font-size: 10px">
                ID:{{ item.id }}
              </div></el-col
            >
            <el-col span="12"
              ><div class="info" style="font-size: 10px">
                回收量：{{ item.recovernum }}
              </div></el-col
            >
            <el-col span="12"
              ><div class="info" style="font-size: 10px">
                创建时间：{{ item.createtime }}
              </div></el-col
            >
            <el-col span="12"
              ><div class="info" style="font-size: 10px">
                发布时间：{{ item.publish_at }}
              </div></el-col
            >
          </el-row>
          <el-divider class="divide" content-position="center"></el-divider>
          <el-row :gutter="12" class="bottominfo">
            <el-col span="10" :offset="1"
              >
              <el-button
                icon="el-icon-edit"
                style="font-size: 14pxl; color: #1e90ff"
                @click="clickedit(index,this.publishbutton[index])"
                >编辑问卷</el-button
              >
              </el-col
            >
            <el-col span="10"
              >
              <router-link :to="{ path: '/topreview', query: { id: item.id }}">
              <el-button
                icon="el-icon-position"
                style="font-size: 14px; color: #1e90ff"
                @click="clicksend(index)"
                >预览问卷</el-button
              >
              </router-link>
              </el-col
            >
            <!-- <el-col span="10"
              ><el-button
                icon="el-icon-data-analysis"
                style="font-size: 14px; color: #1e90ff"
                @click="clickana(index)"
                >分析问卷</el-button
              ></el-col
            > -->

            <router-link :to="{ path: '/toanalysis', query: { id: item.id } }">
              <el-col span="10"
                ><el-button
                  icon="el-icon-data-analysis"
                  style="font-size: 14px; color: #1e90ff"
                  @click="clickana(index)"
                  >分析问卷</el-button
                ></el-col
              ></router-link
            >
            <el-col
              span="10"
              :offset="3"
              style="font-size: 14px; margin-top: 7px"
              >发布&ensp;<el-switch
                v-model="publishbutton[index]"
                active-color="#13ce66"
                inactive-color="#909399"
                @click="changepub(this.quslist[index].id)"
              ></el-switch
            ></el-col>
            <!-- <el-col span="10" style="font-size:14px;">删除&ensp;<el-button type="danger" icon="el-icon-delete" circle @click="clickdelete(this.quslist[index].id)"></el-button></el-col>-->
            <el-col span="10" style="font-size: 14px">
              重新生成链接
              <el-button
                type="warning"
                icon="el-icon-paperclip"
                circle
                @click="newclip(this.quslist[index].id,this.publishbutton[index])"
              ></el-button
            ></el-col>
            <!-- <el-col span="10" :offset="15" style="font-size:14px;margin-top:7px">发布&ensp;<el-switch v-model="publishbutton[index]" active-color="#13ce66" inactive-color="#909399" @click="changepub(this.quslist[index].id)"></el-switch></el-col> -->
            <el-col span="10" style="font-size: 14px"
              >分享问卷&ensp;<el-button
                type="success"
                icon="el-icon-share"
                circle
                @click="
                  clickshare(this.quslist[index].id, this.publishbutton[index])
                "
              ></el-button
            ></el-col>
            <el-col span="10" style="font-size: 14px"
              >复制&ensp;<el-button
                type="primary"
                icon="el-icon-copy-document"
                circle
                @click="clickcopy(this.quslist[index].id)"
              ></el-button
            ></el-col>
            <el-col span="10" style="font-size: 14px"
              >删除&ensp;<el-button
                type="danger"
                icon="el-icon-delete"
                circle
                @click="clickdelete(this.quslist[index].id)"
              ></el-button
            ></el-col>
          </el-row>
        </div>
      </template>
    </div>
  </div>
  <el-row class="switch">
    <el-col :span="36" style="width: 170px">
      <el-menu
        default-active="1"
        class="el-menu-vertical-demo"
        @open="handleOpen"
        @close="handleClose"
      >
        <el-menu-item index="1">
          <i class="el-icon-user"></i>
          <template #title>个人问卷</template>
        </el-menu-item>
        <router-link to="/torecycle" style="text-decoration: none">
          <el-menu-item index="2">
            <i class="el-icon-delete"></i>
            <template #title>回收站</template>
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
      <el-button type="primary" style="width: 170px; height: 70px">
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
import { request } from "../network/request";
import { ElMessage } from "element-plus";
import { h } from "vue";
export default {
  data() {
    return {
      qusnaire:
        "https://pic1.zhimg.com/v2-5dfc909d8627c054a6f66f978831a0de_1440w.jpg?source=172ae18b",
      activeIndex: "1",
      activeIndex2: "1",
      count: 0,
      quscount: 0,
      publishbutton: [],
      search: "",
      keykey:0,
      quslist1: [
        {
          id: "1281245490",
          name: "名字",
          createtime: "2021-08-22 11:10",
          publish_at: "2021-08-22 11:40",
          recovernum: "0",
          publish_status: "false",
          class:1,
        },
        {
          id: "9912454990",
          name: "名字2",
          createtime: "2021-08-23 11:10",
          publish_at: "2021-08-24 11:40",
          recovernum: "2",
          publish_status: "false",
          class:2,
        },
        {
          id: "6681249990",
          name: "名字3dasdsadadadsadad",
          createtime: "2021-08-22 10:10",
          publish_at: "2021-08-22 10:40",
          recovernum: "4",
          publish_status: "false",
          class:3,
        },
      ],
      quslist: [],
      
    };
  },
  computed:{
    finalquslist: function() {
      if(this.keykey!== undefined){
        var a = this.keykey;
      return this.quslist.filter(function (item) {
        console.log(a )
        console.log(item.class)
        // console.log(item.class );console.log(this.keykey);
        return (a==item.class)||(0==a);
      })}
    }
  },
  created: function () {
    if (!this.$store.state.isLogin) {
      this.$router.push("/tologin");
    }
    this.keykey = 0
    console.log("chushihua");
    request({
      url: "/manage",
      method: "post",
      data: {
        type: 3,
        keyword: "",
      },
    }).then((res) => {
      console.log(res);
      let i = 0;
      this.quslist = res.data.res;
      console.log(res.data.res);
      this.quscount = this.quslist.length;
      for (i = 0; i < this.quscount; i++) {
        if (this.quslist[i].publish == 0) {
          this.publishbutton[i] = false;
        } else {
          this.publishbutton[i] = true;
        }
      }
    });
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
    clickedit(index,publish_sta) {
      if (publish_sta == true) {
        ElMessage.warning({
          message: "请将问卷发布状态设为关闭，之后再编辑问卷",
          type: "warning",
          center: true,
        });
        return;
      }
      console.log("编辑" + index);
      let tem = this.quslist[index].class;
      // <router-link :to="{ path: '/toedit', query: { id: item.id }}">
      if(tem == 1){
      this.$router.push({path: '/toedit', query: { id: this.quslist[index].id }})
      return ;}
      if(tem == 2){
      this.$router.push({path: '/tovote', query: { id: this.quslist[index].id }})
      return ;}
      if(tem == 3){
      this.$router.push({path: '/toapply', query: { id: this.quslist[index].id }})
      return ;}
      if(tem == 4){
      this.$router.push({path: '/toexam', query: { id: this.quslist[index].id }})
      return ;}
      if(tem == 5){
      this.$router.push({path: '/toepidemic', query: { id: this.quslist[index].id }})
      return ;}
      
    },
    clickshare(id, publish_sta) {
      console.log("share");
      console.log(publish_sta);
      if (publish_sta == false) {
        ElMessage.warning({
          message: "请先将问卷发布状态设为开启，之后再分享问卷",
          type: "warning",
          center: true,
        });
        return;
      }
      request({
        url: "/manage",
        method: "post",
        data: {
          type: 5,
          survey_id: id,
        },
      }).then((res) => {
        console.log(res);
        this.$msgbox({
          title: "问卷链接和二维码",
          message: h("div", { style: "text-align: center" }, [
            // h('div', null, '我是一段链接'),
            h("div", null, res.data.link),
            h(
              "div",
              {
                style:
                  "display: flex; justify-content: center; padding-top: 20px",
              }, // h('img', {src: "https://gitee.com/static/images/logo.svg?t=158106664"})
              h("img", { src: res.data.photo })
            ),
          ]),
          showCancelButton: false,
          confirmButtonText: "确定",
          showClose:false,
        })

      });
    },
    newclip(id, publish_sta) {
      console.log("clip");
      console.log(publish_sta);
      if (publish_sta == false) {
        ElMessage.warning({
          message: "请先将问卷发布状态设为开启，之后再重新生成链接",
          type: "warning",
          center: true,
        });
        return;
      }
      request({
        url: "/manage",
        method: "post",
        data: {
          type: 7,
          survey_id: id,
        },
      }).then((res) => {
        console.log(res);
        this.$msgbox({
          title: "问卷链接和二维码",
          message: h("div", { style: "text-align: center" }, [
            // h('div', null, '我是一段链接'),
            h("div", null, res.data.link),
            h(
              "div",
              {
                style:
                  "display: flex; justify-content: center; padding-top: 20px",
              }, // h('img', {src: "https://gitee.com/static/images/logo.svg?t=158106664"})
              h("img", { src: res.data.photo })
            ),
          ]),
          showCancelButton: false,
          confirmButtonText: "确定",
            showClose:false,
        }).then(
          ()=>{
            this.onSearch();
          }
        );;
      });
    },
    changepub(id) {
      console.log("change");
      request({
        url: "/manage",
        method: "post",
        data: {
          type: 1,
          survey_id: id,
        },
      });
      return;
    },
    clicksend(index) {
      console.log("发送" + index);
      return;
    },
    clickdelete(id) {
      console.log("delete");
      request({
        url: "/manage",
        method: "post",
        data: {
          type: 2,
          survey_id: id,
        },
      }).then((res) => {
        console.log(res);
        let i = 0;
        this.quslist = res.data.res;
        this.quscount = this.quslist.length;
        for (i = 0; i < this.quscount; i++) {
          if (this.quslist[i].publish == 0) {
            this.publishbutton[i] = false;
          } else {
            this.publishbutton[i] = true;
          }
        }
      });
      this.$message({
        type: "success",
        message: "删除成功!",
      });
      return;
    },
    clickclass(type){
      this.keykey=type;
      console.log(this.keykey)
    },
    clickcopy(id) {
      console.log("copy");
      request({
        url: "/manage",
        method: "post",
        data: {
          type: 6,
          survey_id: id,
        },
      }).then((res) => {
        console.log(res);
        let i = 0;
        this.quslist = res.data.res;
        this.quscount = this.quslist.length;
        for (i = 0; i < this.quscount; i++) {
          if (this.quslist[i].publish == 0) {
            this.publishbutton[i] = false;
          } else {
            this.publishbutton[i] = true;
          }
        }
      });
      this.$message({
        type: "success",
        message: "复制副本成功!",
      });
      return;
    },
    clicktime1() {
      console.log("时间正序");
      request({
        url: "/manage",
        method: "post",
        data: {
          type: 4,
          judge: 1,
        },
      }).then((res) => {
        console.log(res);
        let i = 0;
        this.quslist = res.data.res;
        this.quscount = this.quslist.length;
        for (i = 0; i < this.quscount; i++) {
          if (this.quslist[i].publish == 0) {
            this.publishbutton[i] = false;
          } else {
            this.publishbutton[i] = true;
          }
        }
      });
      return;
    },
    clicktime2() {
      console.log("时间倒序");
      request({
        url: "/manage",
        method: "post",
        data: {
          type: 4,
          judge: 2,
        },
      }).then((res) => {
        console.log(res);
        console.log(res.data.res);
        let i = 0;
        this.quslist = res.data.res;
        this.quscount = this.quslist.length;
        for (i = 0; i < this.quscount; i++) {
          if (this.quslist[i].publish == 0) {
            this.publishbutton[i] = false;
          } else {
            this.publishbutton[i] = true;
          }
        }
      });
      return;
    },
    clicktime3() {
      console.log("回收量正序");
      request({
        url: "/manage",
        method: "post",
        data: {
          type: 4,
          judge: 3,
        },
      }).then((res) => {
        console.log(res);
        let i = 0;
        this.quslist = res.data.res;
        this.quscount = this.quslist.length;
        for (i = 0; i < this.quscount; i++) {
          if (this.quslist[i].publish == 0) {
            this.publishbutton[i] = false;
          } else {
            this.publishbutton[i] = true;
          }
        }
      });
      return;
    },
    clicktime4() {
      console.log("回收量正倒序");
      request({
        url: "/manage",
        method: "post",
        data: {
          type: 4,
          judge: 4,
        },
      }).then((res) => {
        console.log(res);
        let i = 0;
        this.quslist = res.data.res;
        this.quscount = this.quslist.length;
        for (i = 0; i < this.quscount; i++) {
          if (this.quslist[i].publish == 0) {
            this.publishbutton[i] = false;
          } else {
            this.publishbutton[i] = true;
          }
        }
      });
      return;
    },
    clicktime5() {
      console.log("发布时间正序");
      request({
        url: "/manage",
        method: "post",
        data: {
          type: 4,
          judge: 5,
        },
      }).then((res) => {
        console.log(res);
        let i = 0;
        this.quslist = res.data.res;
        this.quscount = this.quslist.length;
        for (i = 0; i < this.quscount; i++) {
          if (this.quslist[i].publish == 0) {
            this.publishbutton[i] = false;
          } else {
            this.publishbutton[i] = true;
          }
        }
      });
      return;
    },
    clicktime6() {
      console.log("发布时间倒序");
      request({
        url: "/manage",
        method: "post",
        data: {
          type: 4,
          judge: 6,
        },
      }).then((res) => {
        console.log(res);
        let i = 0;
        this.quslist = res.data.res;
        this.quscount = this.quslist.length;
        for (i = 0; i < this.quscount; i++) {
          if (this.quslist[i].publish == 0) {
            this.publishbutton[i] = false;
          } else {
            this.publishbutton[i] = true;
          }
        }
      });
      return;
    },
    clickana(index) {
      console.log("分析" + index);
      return;
    },
    onSearch() {
      request({
        url: "/manage",
        method: "post",
        data: {
          type: 3,
          keyword: this.search,
        },
      }).then((res) => {
        console.log(res);
        // this.$alert(res, '问卷链接', {
        //     confirmButtonText: '确定',
        //     callback: action => {
        //         this.$router.push({path: '/'});
        //     }
        // });
        let i = 0;
        this.quslist = res.data.res;
        this.quscount = this.quslist.length;
        for (i = 0; i < this.quscount; i++) {
          if (this.quslist[i].publish == 0) {
            this.publishbutton[i] = false;
          } else {
            this.publishbutton[i] = true;
          }
        }
      });
      console.log(this.search);
      return;
    },
  },
};
</script>
<style >
.manage {
  position: absolute;
  left: 200px;
  top: 10px;
  width: 86%;
}
.returnlo {
  position: absolute;
  right: 350px;
  top: 10px;
  color: #1e90ff;
}
.returnmain {
  position: absolute;
  right: 220px;
  top: 10px;
  color: #1e90ff;
}
.qusname {
  position: absolute;
  left: 30px;
  top: 10px;
}
.new {
  position: absolute;
  left: 10px;
  top: 160px;
}
.switch {
  position: absolute;
  left: 10px;
  top: 240px;
  width: 170px;
}
.list {
  position: absolute;
  top: 140px;
  left: 50px;
  width: 1000px;
  height: 120px;
}
.qus {
  border: 1px solid rgb(221, 211, 211);
  width: 1100px;
  height: 120px;
  margin-bottom: 10px;
}
.topinfo {
  left: 30px;
  top: 10px;
}
.divide {
  width: 94%;
  margin-left: 3%;
}
</style>
