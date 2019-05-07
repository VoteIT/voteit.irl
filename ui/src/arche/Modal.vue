<template>
    <div class="modal fade" id="modal-area" tabindex="-1" role="dialog" aria-labelledby="modal-title" :aria-hidden="true">
        <div class="modal-dialog" :class="modelDialogClass">
            <component v-if="component" :is="component" />
            <div v-else class="modal-content" v-html="content"></div>
        </div>
    </div>
</template>
<script src="./Modal.js"></script>
