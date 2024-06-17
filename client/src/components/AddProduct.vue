<template>
    <v-dialog v-model="localDialogVisible" max-width="600px">
        <v-card>
            <v-card-title>
                <span class="text-h5">Add Product</span>
            </v-card-title>
            <v-divider></v-divider>

            <div class="v-container">
                <form>
                    <v-text-field v-model="productForm.name" label="Name"
                        :error-messages="v$.name.$errors.map(e => e.$message)" @input="v$.name.$reset"
                        @focus="v$.name.$reset"></v-text-field>

                    <v-text-field v-model="productForm.weight" label="Weight (in kg)" type="number" min="1"
                        :error-messages="v$.weight.$errors.map(e => e.$message)" @input="v$.weight.$reset"
                        @focus="v$.weight.$reset"></v-text-field>

                    <v-divider></v-divider>
                    <v-card-actions>
                        <v-btn color="primary" variant="outlined" @click="submitProductForm">Submit</v-btn>
                        <v-btn color="red" variant="outlined" @click="closeDialog">Close</v-btn>
                    </v-card-actions>
                </form>
            </div>
        </v-card>
    </v-dialog>
</template>

<script setup>
import { reactive, ref, watch } from 'vue';
import useVuelidate from '@vuelidate/core';
import { helpers, required } from '@vuelidate/validators';


const props = defineProps({
    dialogVisible: {
        type: Boolean,
        default: false
    }
});

const productForm = reactive({
    name: "",
    weight: ""
})

const rules = {
    name: {
        required: helpers.withMessage("", required)
    },
    weight: {
        required: helpers.withMessage("", required),
        customLimit: helpers.withMessage("Not more than 25kg", (value) => { return !value || isNaN(value) ? false : parseFloat(value) > 0 && parseFloat(value) <= 25; })
    },
}

const v$ = useVuelidate(rules, productForm);

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

const submitProductForm = async () => {
    const isValidate = await v$.value.$validate();
    const apiUrl = `http://127.0.0.1:8000/api/products/`;
    const method = 'POST';

    if (isValidate) {
        try {
            const response = await fetch(apiUrl, {
                method: method,
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(productForm)
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const result = await response.json();

            closeDialog();

        } catch (error) {
            console.error('Error submitting form:', error);
        }
    }
}

</script>
