import { createRouter, createWebHistory } from "vue-router";

const routes = [
  {
    path: "/",
    name: "Home",
    component: () => import("../views/Home.vue"),
  },
  {
    path: "/about",
    name: "About",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/About.vue"),
  },
  {
    path: "/tomanage",
    name: "Manage",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import("../views/Manage.vue"),
  },
  {
    path: "/tologin",
    name: "Login",
    component: () => import("../views/Login.vue"),
  },
  {
    path: "/torecycle",
    name: "Recycle",
    component: () => import("../views/Recycle.vue"),
  },
  {
    path: "/toend",
    name: "End",
    component: () => import("../views/End.vue"),
  },
  {
    path: "/toend3",
    name: "End3",
    component: () => import("../views/toend3.vue"),
  },
  {
    path: "/toregister",
    name: "Register",
    component: () => import("../views/Register.vue"),
  },
  {
    path: "/torecycle",
    name: "Recycle",
    component: () => import("../views/Recycle.vue"),
  },
  {
    path: "/toedit",
    name: "Edit",
    component: () => import("../views/Edit.vue")
  },
  {
    path: "/tosurvey",
    name: "Survey",
    component: () => import("../views/Survey.vue")
  },
  {
    path: "/toerror",
    name: "Error",
    component: () => import("../views/Error.vue")
  },
  {
    path: "/toanalysis",
    name: "Analysis",
    component: () => import("../views/Analysis.vue")
  },
  {
    path: "/topreview",
    name: "Preview",
    component: () => import("../views/Preview.vue")
  },
  {
    path: "/toanauser",
    name: "AnalysisForUser",
    component: () => import("../views/AnalysisForUser.vue")
  },
  {
    path: "/toepidemic",
    name: "Epidemic",
    component: () => import("../views/Epidemic.vue")
  },
  {
    path: "/tovote",
    name: "Vote",
    component: () => import("../views/Vote.vue")
  },
  {
    path: "/toapply",
    name: "Apply",
    component: () => import("../views/Apply.vue")
  },
  {
    path: "/toexam",
    name: "Exam",
    component: () => import("../views/Exam.vue")
  },
  {
    path: "/totest",
    name: "Test",
    component: () => import("../views/Test.vue")
  },
  {
    path: "/toend2",
    name: "End2",
    component: () => import("../views/toend2.vue")
  },
];

const router = createRouter({
  mode: 'history',
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
