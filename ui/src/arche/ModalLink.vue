<template>
    <a :role="role" @click.prevent="openModal" :href="href" v-html="content"/>
</template>
<script>
import { eventBus } from 'arche/utils';

export default {
    props: {
        href: String,
        modelDialogClass: String,
        content: String,
        role: String
    },
    methods: {
        openModal() {
            eventBus.$emit('modal::open', {
                modelDialogClass: this.modelDialogClass,
                href: this.href
            });
        }
    }
}
</script>