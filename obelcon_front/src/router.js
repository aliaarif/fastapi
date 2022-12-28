import { createRouter, createWebHistory } from "vue-router";
// import App from './App.vue';
// import MasterPage from './pages/MasterPage.vue';

import LandingPage from './pages/LandingPage.vue';

// import CategoryPage from './pages/CategoryPage.vue';
import LoginPage from './pages/LoginPage.vue';
import RegisterPage from './pages/RegisterPage.vue';

const router = createRouter({
    history: createWebHistory(),
    routes: [
        { path: '/', name: 'LandingPage', component: LandingPage },
        { path: '/login', name: 'LoginPage', component: LoginPage },
        { path: '/signup', name: 'RegisterPage', component: RegisterPage },

        // {
        //     path: '',
        //     name: 'master',
        //     component: MasterPage,
        //     children: [
        //         { path: '/', name: 'LandingPage', component: LandingPage },
        //         {
        //             path: '/:location/:query',
        //             name: 'LandingPage',
        //             component: LandingPage
        //         },

        //         { path: '/login', name: 'LoginPage', component: LoginPage },
        //         { path: '/signup', name: 'RegisterPage', component: RegisterPage },

        //     ]
        // }

    ]
})

export default router