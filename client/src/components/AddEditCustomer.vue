<template>
    <v-dialog v-model="localDialogVisible" max-width="600px">
        <v-card>
            <v-card-title>
                <span class="text-h5">{{ id ? 'Edit Customer' : 'Add Customer' }}</span>
            </v-card-title>
            <v-divider></v-divider>

            <div class="v-container">
                <form>
                    <v-text-field v-model="customerForm.name" label="Name"
                        :error-messages="v$.name.$errors.map(e => e.$message)" @input="v$.name.$reset"
                        @focus="v$.name.$reset"></v-text-field>

                    <v-text-field v-model="customerForm.contact_number" label="Contact Number"
                        :error-messages="v$.contact_number.$errors.map(e => e.$message)"
                        @input="v$.contact_number.$reset" @focus="v$.contact_number.$reset"></v-text-field>

                    <v-text-field v-model="customerForm.email" label="Email" type="email"
                        :error-messages="v$.email.$errors.map(e => e.$message)" @input="v$.email.$reset"
                        @focus="v$.email.$reset"></v-text-field>

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
import { onMounted, reactive, ref, watch } from 'vue';
import useVuelidate from '@vuelidate/core';
import { email, helpers, maxLength, minLength, required } from '@vuelidate/validators';

const props = defineProps({
    id: {
        type: [Number, null],
        required: true
    },
    dialogVisible: {
        type: Boolean,
        default: false
    }
});

const customerForm = reactive({
    name: "",
    contact_number: "",
    email: ""
})


const rules = {
    name: {
        required: helpers.withMessage("", required)
    },
    contact_number: { 
        required: helpers.withMessage("", required), 
        minLength: helpers.withMessage("Invalid Contact Number", minLength(10)), 
        maxLength: helpers.withMessage("Invalid Contact Number", maxLength(10)),
        customNumeric: helpers.withMessage("Contact Number must contain only numeric characters", (value)=>{return value && /^[0-9]*$/.test(value) ? true : false;}), 
    },
    email: { 
        required: helpers.withMessage("", required), 
        email: helpers.withMessage("Enter valid email.", email) 
    },
}

const v$ = useVuelidate(rules, customerForm);

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
    const isValidate = await v$.value.$validate();
    const apiUrl = props.id ? `http://127.0.0.1:8000/api/customers/${props.id}/` : 'http://127.0.0.1:8000/api/customers/';
    const method = props.id ? 'PUT' : 'POST';
    if (isValidate) {
        try {
            const response = await fetch(apiUrl, {
                method: method,
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(customerForm)
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const result = await response.json();
            console.log('Success:', result);
            closeDialog();

        } catch (error) {
            console.error('Error submitting form:', error);
        }
    }
};
const fetchCustomerDetail = async (id) => {
    try {
        let apiurl = `http://127.0.0.1:8000/api/customers/${id}/`
        const response = await fetch(apiurl);
        const data = await response.json();
        customerForm.name = data.name;
        customerForm.contact_number = data.contact_number;
        customerForm.email = data.email;
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