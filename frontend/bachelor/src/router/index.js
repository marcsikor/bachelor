import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import { getAuth, onAuthStateChanged } from "firebase/auth";
import { auth } from "../firebase/firebaseCredentials";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/', // add summary, styling
      name: 'home',
      component: HomeView
    },
    {
      path: '/login', // styling
      name: 'login',
      component: () => import('../views/Login.vue')
    },
    {
      path: '/new', // styling
      name: 'new',
      component: () => import('../views/NewReport.vue'),
      meta: {
        requiresAuth: true
      },
    },
    {
      path: '/list', // delete, send for approval, styling
      name: 'list',
      component: () => import('../views/List.vue'),
      meta: {
        requiresAuth: true
      },
    },
    {
      path: '/edit/:id', // add firebase, styling
      name: 'edit',
      component: () => import('../views/EditReport.vue'),
      props: true,
      meta: {
        requiresAuth: true
      },
    },
    {
      path: '/new-user', // add proper forms, firebase, styling
      name: 'new-user',
      component: () => import('../views/NewUser.vue'),
      // props: true
      meta: {
        requiresAuth: true
      },
    },
    {
      path: '/new-password', // add proper forms, firebase, styling
      name: 'new-password',
      component: () => import('../views/NewPassword.vue'),
      // props: true
    },
    {
      path: '/list-users', // add view, buttons for editing for superadmin, firebase, guards, styling
      name: 'list-users',
      component: () => import('../views/ListUsers.vue'),
      meta: {
        requiresFullAccess: true
      },
      // props: true
    },
    {
      path: '/open-reports', // add view, firebase, styling
      name: 'open-reports',
      component: () => import('../views/OpenReports.vue'),
      meta: {
        requiresMidAccess: true
      },
      // props: true
    },
    {
      path: '/edit-user/:id', // add firebase, styling
      name: 'edit-user',
      component: () => import('../views/EditUser.vue'),
      props: true,
      meta: {
        requiresAuth: true
      },
    },
    {
      path: '/history', // add view, firebase, styling
      name: 'history',
      component: () => import('../views/History.vue'),
      props: true,
      meta: {
        requiresAuth: true
      },
    }
  ]
})

const getCurrentUser = () => {
   return new Promise((resolve,reject) => {
    const removeListener = onAuthStateChanged(
      auth,
      (user) => {
        removeListener();
        resolve(user);
      },
      reject
    );
   });
};

router.beforeEach(async (to,from,next) => {
  if(to.matched.some((record) => record.meta.requiresAuth)){
    if (await getCurrentUser()){
      next();
    } else {
      alert("Dostęp do tej strony wymaga zalogowania");
      next("/login");
    };
  } else if(to.matched.some((record) => record.meta.requiresMidAccess)) {
    if (await getCurrentUser()){
      const currentUser = await getCurrentUser()
      const customClaim = await currentUser.getIdTokenResult()
      if(customClaim.claims.function === 'Członek zarządu' || customClaim.claims.function === 'Skarbnik'){
          next();
        }
      else {
          alert("Dostęp do tej strony wymaga wyższych uprawnień");
          next('/');
      };  
    } else {
      alert("Dostęp do tej strony wymaga zalogowania");
      next("/login");
    };
  } else if(to.matched.some((record) => record.meta.requiresFullAccess)) {
    if (await getCurrentUser()){
      const currentUser = await getCurrentUser()
      const customClaim = await currentUser.getIdTokenResult()
      if(customClaim.claims.function === 'Skarbnik'){
          next();
        }
      else {
          alert("Dostęp do tej strony wymaga wyższych uprawnień");
          next('/');
      };  
    } else {
      alert("Dostęp do tej strony wymaga zalogowania");
      next("/login");
    };
  } else {
    next();
  }
})

export default router
