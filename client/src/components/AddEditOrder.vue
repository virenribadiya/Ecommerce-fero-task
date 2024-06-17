<template>
    <v-dialog v-model="localDialogVisible" max-width="600px">
        <v-card>
            <v-card-title>
                <span class="text-h5">{{ id ? 'Edit Order' : 'Add Order' }}</span>
            </v-card-title>
            <v-divider></v-divider>

            <div class="v-container">
                <form>
                    <v-text-field v-if="props.id !== null" v-model="orderNumber" label="Order Number"
                        readonly></v-text-field>

                    <v-select v-model="orderForm.customer" :items="customersList" item-title="name" item-value="id"
                        label="Customer" :error-messages="v$.customer.$errors.map(e => e.$message)"
                        @input="v$.customer.$reset" @focus="v$.customer.$reset">
                    </v-select>

                    <v-text-field v-model="orderForm.order_date" type="date" label="Order Date" :min="today"
                        :error-messages="v$.order_date.$errors.map(e => e.$message)" @input="v$.order_date.$reset"
                        @focus="v$.order_date.$reset"></v-text-field>

                    <v-textarea v-model="orderForm.address" label="Address" row-height="25" rows="3"
                        :error-messages="v$.address.$errors.map(e => e.$message)" @input="v$.address.$reset"
                        @focus="v$.address.$reset" auto-grow></v-textarea>

                    <div class="d-flex flex-row align-center ">
                        <span class="mx-2">Order Items</span>
                        <v-btn icon="mdi-plus" size="small" variant="plain" @click="addOrderItem"></v-btn>
                        <div v-if="v$.$errors" v-for="error in v$.order_items.$errors.map(e => e.$message)" :key="error"
                            class="error-message text-red">
                            {{ error }}
                        </div>
                    </div>
                    <div class="ma-2"> Total weight: <span class="text-orange">{{ totalOrderWeight }} Kg</span></div>

                    <div v-for="(item, index) in orderForm.order_items" :key="index"
                        class="d-flex flex-row align-self-center">

                        <v-select v-model="item.product" :items="productsList" item-title="name" item-value="id"
                            label="Product" width="4"></v-select>

                        <v-text-field v-model="item.quantity" class="mx-3" type="number" width="4" label="Quantity"
                            min="1"></v-text-field>

                        <v-btn @click="removeOrderItem(index)" class="pt-3" variant="plain" color="red"
                            icon="mdi-delete"></v-btn>

                    </div>

                    <v-divider></v-divider><br>
                    <v-card-actions>
                        <v-btn color="primary" variant="outlined" @click="submitOrderForm">Submit</v-btn>
                        <v-btn color="red" variant="outlined" @click="closeDialog">Close</v-btn>
                    </v-card-actions>
                </form>
            </div>
        </v-card>
    </v-dialog>
</template>

<script setup>
import { onMounted, reactive, ref, watch } from 'vue';
import useVuelidate from '@vuelidate/core';
import { helpers, required } from '@vuelidate/validators';

const props = defineProps({
    id: {
        type: [Number, null],
        default: null
    },
    dialogVisible: {
        type: Boolean,
        default: false
    }
});

const totalOrderWeight = ref(0);

const orderForm = reactive({
    customer: null,
    order_date: null,
    address: "",
    order_items: []
})

const rules = {
    customer: {
        required: helpers.withMessage("", required)
    },
    order_date: {
        required: helpers.withMessage("", required),
        notInPast: helpers.withMessage("Past date is not allowed.", (value) => { return value >= today ? true : false }),
    },
    address: {
        required: helpers.withMessage("", required),
    },
    order_items: {
        required: helpers.withMessage("Order Items are required.", required),
        cumulativeWeight: helpers.withMessage("Cumulative weight must be less then 150 kg.", (value) => {
            let totalWeight = 0;
            for (let item of value) {
                const productWeight = productWeightFromId(item.product);
                if (item.quantity && item.quantity > 0 && item.product && productWeight) {
                    totalWeight += Number(item.quantity) * productWeight;
                }
            }
            totalOrderWeight.value = totalWeight;
            return totalWeight <= 150;
        })
    }
}



const v$ = useVuelidate(rules, orderForm);

const localDialogVisible = ref(props.dialogVisible);
const today = new Date().toISOString().split('T')[0];
const orderNumber = ref(null);
const customersList = ref([]);
const productsList = ref([]);

const emit = defineEmits(['close']);


const closeDialog = () => {
    localDialogVisible.value = false;
    emit('close');
};

// handel the case when user clicks outside the modal
watch(localDialogVisible, (newVal) => {
    if (!newVal) {
        emit('close');
    }
});

const addOrderItem = () => {
    orderForm.order_items.push({ product: '1', quantity: 1 });
};

const removeOrderItem = (index) => {
    orderForm.order_items.splice(index, 1);
};

const productWeightFromId = (id) => {
    const product = productsList.value.find((product) => product.id === id)
    return product ? product.weight : "1";
}

const submitOrderForm = async () => {
    const isValidate = await v$.value.$validate();
    const apiUrl = props.id ? `http://127.0.0.1:8000/api/orders/${props.id}/` : 'http://127.0.0.1:8000/api/orders/';
    const method = props.id ? 'PUT' : 'POST';

    if (isValidate) {
        try {
            const response = await fetch(apiUrl, {
                method: method,
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(orderForm)
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const result = await response.json();
            console.log('Success:', result);

            // Close the dialog on success
            closeDialog();
        } catch (error) {
            console.error('Error submitting form:', error);
        }
    }
}

const fetchOrderDetail = async (id) => {
    try {
        let apiurl = `http://127.0.0.1:8000/api/orders/${id}/`
        const response = await fetch(apiurl);
        const data = await response.json();
        orderForm.customer = data.customer;
        orderForm.order_date = data.order_date;
        orderForm.address = data.address;
        orderForm.order_items = data.order_items;
        orderNumber.value = data.order_number;
    } catch (error) {
        console.error('Error fetching items:', error);
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

onMounted(async () => {
    await fetchCustomerList();
    await fetchProductList();
    if (props.id !== null) {
        await fetchOrderDetail(props.id);
    }
})

</script>