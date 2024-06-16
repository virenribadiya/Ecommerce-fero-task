<template>
    <v-card flat>
        <v-card-title class="d-flex align-center pe-2">
            <v-icon icon="mdi-cube"></v-icon> &nbsp;
            List of all the products

            <v-spacer></v-spacer>

            <v-btn class="text-none" color="primary" variant="outlined" @click="openDialog()">Add Product</v-btn>
        </v-card-title>
        <br>
        <v-divider></v-divider>

        <v-data-table-virtual :loading="loading" :hover="true" :headers="headers" :items="productList" fixed-header
            :height="450">
            <template v-slot:item="{ item }">
                <tr>
                    <td>{{ item.name }}</td>
                    <td>{{ item.weight }} kg</td>
                </tr>
            </template>
        </v-data-table-virtual>

        <AddProduct v-if="dialogVisible" @close="closeDialog" :dialogVisible="dialogVisible"></AddProduct>

    </v-card> 
</template>

<script setup>
import AddProduct from '@/components/AddProduct.vue';
import { onMounted, ref } from 'vue';

const loading = ref(false);
const dialogVisible = ref(false);
const productList = ref([]);
const headers = [
    { title: 'Name', key: 'name' },
    { title: 'Weight', key: 'weight' },
];

const openDialog = () => {
    console.log("Open");
    dialogVisible.value = true;
}

const closeDialog = async() => { 
    dialogVisible.value = false;
    await fetchProductList();
};

const fetchProductList = async () => {
    loading.value = true;
    try {
        let apiurl = `http://127.0.0.1:8000/api/products/`
        const response = await fetch(apiurl);
        const data = await response.json();
        productList.value = data;
    } catch (error) {
        console.error('Error fetching items:', error);
    } finally {
        loading.value = false;
    }
}

onMounted(async () => {
    await fetchProductList();
})
</script>

<style lang="scss" scoped></style>