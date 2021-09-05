<template>
  <div id="nav">
    <router-view />
  </div>
</template>

<script>
export default {
  created(){
    if(sessionStorage.getItem("store")) {
      this.$store.replaceState(
        Object.assign(
          {},
          this.$store.state,
          JSON.parse(sessionStorage.getItem("store"))
        )
      );
    }
    window.addEventListener("beforeunload", () => {
      sessionStorage.setItem("store", JSON.stringify(this.$store.state))
    })
  }
}
</script>

<style>
* {
  margin: 0px;
  padding: 0px;
}
</style>
