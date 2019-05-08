<template>
    <a :role="role" @click.prevent="openModal" :href="href" v-html="content"/>
</template>
<script>
import { modal } from 'arche/utils';

export default {
    props: {
        href: String,
        modelDialogClass: String,
        content: String,
        role: String
    },
    methods: {
        openModal() {
            modal.open(this.href, { modelDialogClass: this.modelDialogClass });
        }
    }
}
</script>