<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { ref } from "vue";
const drawer = ref(true);
const rail = ref(false);
</script>

<template>
    <v-layout>
        <v-app-bar>
            <template #prepend>
                <v-toolbar-title>
                    <v-app-bar-nav-icon @click.stop="rail = !rail"></v-app-bar-nav-icon>
                    <RouterLink :to="{ name: 'CustomerList' }" class="text-decoration-none">
                        FERO Mini Task
                    </RouterLink>
                </v-toolbar-title>
            </template>
        </v-app-bar>

        <v-navigation-drawer v-model="drawer" :rail="rail" permanent @click="rail = false">
            <v-list density="default" active-class="active-item">
                <v-list-item prepend-icon="mdi-account-group-outline" title="Customers"
                    :to="{ name: 'CustomerList' }"></v-list-item>
                <v-list-item prepend-icon="mdi-cube-outline" title="Products"
                    :to="{ name: 'ProductList' }"></v-list-item>
                <v-list-item prepend-icon="mdi-truck-fast" title="Orders" :to="{ name: 'OrderList' }"></v-list-item>
            </v-list>
        </v-navigation-drawer>

        <v-main style="min-height: 300px;">
            <div class="pa-5">
                <RouterView />
            </div>
        </v-main>
    </v-layout>
</template>

<style scoped>
.active-item {
    background-color: blue;
    color: white;
}
</style>