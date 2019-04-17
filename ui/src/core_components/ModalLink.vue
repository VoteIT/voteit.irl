<template>
    <a :role="role" @click.prevent="openModal" :href="href" v-html="content">
    </a>
</template>
<script>
export default {
    props: {
        href: String,
        modelDialogClass: String,
        content: String,
        role: String
    },
    methods: {
        openModal() {
            this.$root.$emit('modal::open', {
                modelDialogClass: this.modelDialogClass,
                href: this.href
            });
        }
    }
}
</script>