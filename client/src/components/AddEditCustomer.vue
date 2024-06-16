<template>
    <v-dialog v-model="localDialogVisible" max-width="600px">
        <v-card>
            <v-card-title>
                <span class="text-h5">{{ id ? 'Edit Customer' : 'Add Customer' }}</span>
            </v-card-title>
            <v-divider></v-divider>

            <div class="v-container">
                <form>
                    <v-text-field v-model="customerForm.name" label="Name" required></v-text-field>

                    <v-text-field v-model="customerForm.contact_number" label="Contact Number" required></v-text-field>

                    <v-text-field v-model="customerForm.email" label="Email" required type="email"></v-text-field>

                    <v-divider></v-divider>
                    <v-card-actions>
                        <v-btn color="primary" variant="outlined" @click="submitCustomerForm">Submit</v-btn>
                        <v-btn color="red" variant="outlined" @click="closeDialog">Close</v-btn>
                    </v-card-actions>
                </form>
            </div>
        </v-card>
    </v-dialog>
</template>

<script setup>
import { onMounted, ref, watch } from 'vue';

const props = defineProps({
    id: {
        type: Number,
        required: true
    },
    dialogVisible: {
        type: Boolean,
        default: false
    }
});

const customerForm = ref({
    name: "",
    contact_number: "",
    email: ""
})

const localDialogVisible = ref(props.dialogVisible);

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

const submitCustomerForm = async () => {
    const apiUrl = props.id ? `http://127.0.0.1:8000/api/customers/${props.id}/` : 'http://127.0.0.1:8000/api/customers/';
    const method = props.id ? 'PUT' : 'POST';

    try {
        const response = await fetch(apiUrl, {
            method: method,
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(customerForm.value)
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
};

const fetchCustomerDetail = async (id) => {
    try {
        let apiurl = `http://127.0.0.1:8000/api/customers/${id}/`
        const response = await fetch(apiurl);
        const data = await response.json();
        customerForm.value.name = data.name;
        customerForm.value.contact_number = data.contact_number;
        customerForm.value.email = data.email;
    } catch (error) {
        console.error('Error fetching items:', error);
    }
}

onMounted(async () => {
    if (props.id !== null) {
        await fetchCustomerDetail(props.id);
    }
})

</script>