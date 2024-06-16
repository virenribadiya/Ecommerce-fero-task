<template>
    <v-card flat>
        <v-card-title class="d-flex align-center pe-2">
            <v-icon icon="mdi-account-group"></v-icon> &nbsp;
            List of all the customers

            <v-spacer></v-spacer>

            <v-btn class="text-none" color="primary" variant="outlined" @click=openDialog(null)>Add Customer</v-btn>
        </v-card-title>

        <br>
        <v-divider></v-divider>

        <v-data-table-virtual :loading="loading" :hover="true" :headers="headers" :items="customerList" fixed-header
            :height="450">
            <template v-slot:item="{ item }">
                <tr>
                    <td>
                        <v-avatar color="green">
                            <span class="text-h5">{{ item.name[0] }}</span>
                        </v-avatar> &nbsp;
                        {{ item.name }}
                    </td>
                    <td>{{ item.contact_number }}</td>
                    <td>{{ item.email }}</td>
                    <td>
                        <v-icon color="blue-lighten-1" size="large" icon="mdi-pencil"
                            @click="openDialog(item.id)"></v-icon>&nbsp;
                    </td>
                </tr>
            </template>
        </v-data-table-virtual>

        <AddEditCustomer v-if="dialogVisible" :id="currentCustomerId" @close="closeDialog"
            :dialogVisible="dialogVisible" />

    </v-card>
</template>

<script setup>
import AddEditCustomer from '@/components/AddEditCustomer.vue';
import { onMounted, ref } from 'vue';

const loading = ref(false);
const dialogVisible = ref(false);
const currentCustomerId = ref(null);
const customerList = ref([]);
const headers = [
    { title: 'Name', key: 'name' },
    { title: 'Contact Number', key: 'contact_number' },
    { title: 'Email', key: 'email' },
    { title: 'Actions', sortable: false },
];

const openDialog = (id) => {
    currentCustomerId.value = id;
    dialogVisible.value = true;
}

const closeDialog = async () => {
    dialogVisible.value = false;
    await fetchCustomerList();
};


const fetchCustomerList = async () => {
    loading.value = true;
    try {
        let apiurl = `http://127.0.0.1:8000/api/customers/`
        const response = await fetch(apiurl);
        const data = await response.json();
        customerList.value = data;
    } catch (error) {
        console.error('Error fetching items:', error);
    } finally {
        loading.value = false;
    }
}

onMounted(async () => {
    await fetchCustomerList();
})

</script>

<style lang="scss" scoped></style>