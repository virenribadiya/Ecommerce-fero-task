import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'CustomerList',
      component: () => import('../views/CustomerList.vue')
    },
    {
      path: '/products',
      name: 'ProductList',
      component: () => import('../views/ProductList.vue')
    },
    {
      path: '/orders',
      name: 'OrderList',
      component: () => import('../views/OrderList.vue')
    }
  ]
})

export default router
