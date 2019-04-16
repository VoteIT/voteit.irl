<template>
    <li class="list-group-item proposal">
        <button class="btn btn-xs btn-default move-left" v-if="actions.left" @click="actions.left(item)">
            <span class="glyphicon glyphicon-chevron-left"> </span>
        </button>
        <div class="main-controls pull-right">
                <div class="btn-group">
                    <button
                            class="btn btn-default btn-sm"
                            v-for="state in workflowStates"
                            :key="state.name"
                            :class="{active: state.name === item.workflowState && actions.setWorkflowState}"
                            @click="setWorkflowState(item, state)">
                        <span :class="['text-' + state.name, 'glyphicon', 'glyphicon-' + state.name]"> </span>
                    </button>
                </div>
            <button class="btn btn-sm btn-default move-right" @click="actions.right(item)">
                <span class="glyphicon glyphicon-chevron-right"> </span>
            </button>
        </div>
        <h3 class="prop-meta-heading">
            <strong class="proposal-aid">#{{ item.aid }}</strong>
            {{ $t('by') }}
            <span class="proposal-author">{{ item.creator }}</span>
        </h3>
        <div class="proposal-text">{{ item.text }}</div>
    </li>
</template>
<script>
export default {
    props: {
        actions: Object,
        item: Object,
        workflowStates: Array
    },
    methods: {
        setWorkflowState(proposal, workflowState) {
            if (this.actions.setWorkflowState)
                this.actions.setWorkflowState({ proposal, workflowState })
        }
    }
}
</script>