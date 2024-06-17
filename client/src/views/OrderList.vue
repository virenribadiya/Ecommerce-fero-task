<template>
    <v-card flat>
        <v-card-title class="d-flex align-center pe-2">
            <v-icon icon="mdi-truck-fast"></v-icon> &nbsp;
            List of all the orders

            <v-spacer></v-spacer>
        </v-card-title>

        <v-card-text class="d-flex my-2 align-center">

            <v-text-field class="mx-2" v-model="searchByCustomerName" density="compact" prepend-inner-icon="mdi-magnify"
                label="Search by customer name" hide-details ></v-text-field>
            <v-btn variant="outlined" @click="filterSearchByCustomerName">Search</v-btn>


            &nbsp;&nbsp;&nbsp;&nbsp;

            <v-text-field class="mx-2" v-model="searchByProducts" density="compact" prepend-inner-icon="mdi-magnify"
                label="Search by products" hide-details></v-text-field>
            <v-btn variant="outlined" @click="filterSearchByProducts">Search</v-btn>

            <v-spacer></v-spacer>

            <v-btn class="text-none" variant="outlined" color="primary" @click=openDialog(null)>Add Order</v-btn>
        </v-card-text>

        <v-divider></v-divider>


        <v-data-table-virtual :loading="loading" :hover="true" :headers="headers" :items="orderList" fixed-header
            :height="450">
            <template v-slot:item="{ item }">
                <tr>
                    <td>{{ item.order_number }}</td>
                    <td>{{ customerNameFromId(item.customer) }}</td>
                    <td>{{ item.order_date }}</td>
                    <td>{{ item.address }}</td>
                    <td>{{ orderItemListGetter(item.order_items) }}</td>
                    <td>
                        <v-icon size="large" color="blue-lighten-1" icon="mdi-pencil"
                            @click=openDialog(item.id)></v-icon>
                    </td>
                </tr>
            </template>
        </v-data-table-virtual>

        <AddEditOrder v-if="dialogVisible" :id="currentOrderId" @close="closeDialog" :dialogVisible=dialogVisible />

    </v-card>
</template>

<script setup>
import AddEditOrder from '@/components/AddEditOrder.vue';
import { onMounted, ref } from 'vue';

const loading = ref(false);
const orderList = ref([]);
const dialogVisible = ref(false);
const currentOrderId = ref(null);
const searchByCustomerName = ref("");
const searchByProducts = ref("");
const headers = [
    { title: 'Order Number', key: 'order_number' },
    { title: 'Customer', key: 'customer' },
    { title: 'Order Date', key: 'order_date' },
    { title: 'Address', key: 'address' },
    { title: 'Order Items', key: 'order_items' },
    { title: 'Actions', sortable: false }
];
const customersList = ref([]);
const productsList = ref([]);

const openDialog = (id) => {
    currentOrderId.value = id;
    dialogVisible.value = true;
}

const closeDialog = async () => {
    dialogVisible.value = false;
    await fetchOrderList();
};

const filterSearchByCustomerName = async () => {
    try {
        let apiurl = `http://127.0.0.1:8000/api/orders/?customer=${searchByCustomerName.value}`
        const response = await fetch(apiurl);
        const data = await response.json();
        orderList.value = data;
    } catch (error) {
        console.error('Error fetching items:', error);
    }
}

const filterSearchByProducts = async () => {
    try {
        let apiurl = `http://127.0.0.1:8000/api/orders/?products=${searchByProducts.value}`
        const response = await fetch(apiurl);
        const data = await response.json();
        orderList.value = data;
    } catch (error) {
        console.error('Error fetching items:', error);
    }
}

const fetchOrderList = async () => {
    loading.value = true;
    try {
        let apiurl = `http://127.0.0.1:8000/api/orders/`
        const response = await fetch(apiurl);
        const data = await response.json();
        orderList.value = data;
    } catch (error) {
        console.error('Error fetching items:', error);
    } finally {
        loading.value = false;
    }
}

const fetchCustomerList = async () => {
    try {
        let apiurl = `http://127.0.0.1:8000/api/customers/`
        const response = await fetch(apiurl);
        const data = await response.json();
        customersList.value = data;
    } catch (error) {
        console.error('Error fetching items:', error);
    }
}

const fetchProductList = async () => {
    try {
        let apiurl = `http://127.0.0.1:8000/api/products/`
        const response = await fetch(apiurl);
        const data = await response.json();
        productsList.value = data;
    } catch (error) {
        console.error('Error fetching items:', error);
    }
}

const customerNameFromId = (id) => {
    const customer = customersList.value.find((customer) => customer.id === id);
    return customer ? customer.name : "Not Found";
}

const productNameFromId = (id) => {
    const product = productsList.value.find((product) => product.id === id)
    return product ? product.name : "Not Found";
}

const orderItemListGetter = (arrayOfObjects) => {
    var orderItemStr = "";
    for (var i = 0; i < arrayOfObjects.length; i++) {
        let nameOfProduct = productNameFromId(arrayOfObjects[i].product);
        let quantity = String(arrayOfObjects[i].quantity);
        orderItemStr += (nameOfProduct + " x " + quantity + " ,");
    }
    return orderItemStr;
}

onMounted(async () => {
    await fetchCustomerList();
    await fetchProductList();
    await fetchOrderList();
})
</script>


<style lang="scss" scoped></style>