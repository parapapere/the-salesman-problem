import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  // {
  //   path: '/editnote/:id',
  //   name: 'EditNote',
  //   component: EditNoteView,
  //   meta: { requiresAuth: true },
  //   props: true,
  // },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

// router.beforeEach((to, _, next) => {
//   if (to.matched.some(record => record.meta.requiresAuth)) {
//     if (store.getters.isAuthenticated) {
//       next();
//       return;
//     }
//     next('/login');
//   } else {
//     next();
//   }
// });

export default router;
