

<template >
    <div style="font-size: 14px;color: #666;" @click="onMouseDown">剩余支付时间（超时自动关闭）</div>
</template>
 
<script>
export default {
    methods: {
        onMousedown(event, column) {
        const resizeProxy = this.$refs.resizeProxy;
        resizeProxy.style.left = this.dragState.startLeft + 'px';
        document.onselectstart = function() { return false; };//解决拖动会选中文字的问题
        document.ondragstart = function() { return false; };

        const handleMouseMove = (event) => {
          const deltaLeft = event.clientX - this.dragState.startMouseLeft;
          const proxyLeft = this.dragState.startLeft + deltaLeft;

          resizeProxy.style.left = Math.max(minLeft, proxyLeft) + 'px';
        };

        const handleMouseUp = () => {
          document.removeEventListener('mousemove', handleMouseMove);
          document.removeEventListener('mouseup', handleMouseUp);
          document.onselectstart = null;
          document.ondragstart = null;
        };

        document.addEventListener('mousemove', handleMouseMove);
        document.addEventListener('mouseup', handleMouseUp);
      },
    }
}
// import moment from 'moment';
// export default {
//     name: 'TimeRangPage',
//     data () {
//       return {
//         startTime: "Sat Aug 28 2021 12:32:23 GMT+0800 (中国标准时间) 0时0分0秒",
//         endTime: "Sat Aug 28 2021 14:32:23 GMT+0800 (中国标准时间) 0时0分0秒",
//         day: 0,
//         hr: 0,
//         min: 0,
//         sec: 0,
//         timeSetInterval: null,
//         showTimeDown: false,
//         showOver: false
//       };
//     },
//     mounted () {
//   this.countdown()
// },
//     methods: {
//      countdown () {
//       const end = Date.parse(new Date('2021-08-28 13:59:23'))
//       const now = Date.parse(new Date())
//       const msec = end - now

//       console.log(msec)
//       if(msec<0) return;

//       let day = parseInt(msec / 1000 / 60 / 60 / 24)
//       let hr = parseInt(msec / 1000 / 60 / 60 % 24)
//       let min = parseInt(msec / 1000 / 60 % 60)
//       let sec = parseInt(msec / 1000 % 60)
//       this.day = day
//       this.hr = hr > 9 ? hr : '0' + hr
//       this.min = min > 9 ? min : '0' + min
//       this.sec = sec > 9 ? sec : '0' + sec
//       const that = this
//       if(min>=0 && sec>=0){
//         //倒计时结束关闭订单
//         if(min==0 && sec==0){

//           return
//         }
//         setTimeout(function () {
//           that.countdown()
//         }, 1000)
//       }
//     }
//     }
//   };
// //拖拽调换顺序
// export default {
//     name: 'Toolbar',
//     data () {
//         return {
//             items: [
//             { key: 1, color: '#ffebcc'},
//             { key: 2, color: '#ffb86c'},
//             { key: 3, color: '#f01b2d'},
//             { key: 4, color: '#f01b2d'},
//             { key: 5, color: '#f01b2d'},
//             { key: 6, color: '#f01b2d'},
//             { key: 7, color: '#f01b2d'},
//             { key: 8, color: '#f01b2d'},
//             { key: 9, color: '#f01b2d'},
//             { key: 10, color: '#f01b2d'},
//             { key: 11, color: '#f01b2d'},
//             { key: 12, color: '#f01b2d'},
//             { key: 13, color: '#f01b2d'},

//             ],
   
//             dragging: null
//         }
//     },
//     methods:{
//         handleDragStart(e,item){
//             this.dragging = item;
//         },
//         handleDragEnd(e,item){
//             this.dragging = null
//         },
//         //首先把div变成可以放置的元素，即重写dragenter/dragover
//         handleDragOver(e) {
//             e.dataTransfer.dropEffect = 'move'// e.dataTransfer.dropEffect="move";//在dragenter中针对放置目标来设置!
//         },
//         handleDragEnter(e,item){
//             e.dataTransfer.effectAllowed = "move"//为需要移动的元素设置dragstart事件
//             if(item === this.dragging){
//             return
//             }
//             const newItems = [...this.items]
//             console.log(newItems)
//             const src = newItems.indexOf(this.dragging)
//             const dst = newItems.indexOf(item)
            
//             newItems.splice(dst, 0, ...newItems.splice(src, 1))
            
//             this.items = newItems
//         }
//     }
// }
</script>
  
<style scoped>
 /* .container{
  width: 80px;
  position: absolute;
  left: 0;
  display:flex;
  flex-direction: column;
  padding: 0;
 }
 .item {
  margin-top: 10px;
  transition:all linear .3s;
  height: 200px;
 } */
 </style>