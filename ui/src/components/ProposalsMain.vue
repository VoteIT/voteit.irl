<template>
    <ul id="projector-main" class="list-group">
        <proposal
            v-for="item in selectedProposals"
            :key="item.uid"
            :actions="proposalActions"
            :item="item"
            :workflowStates="proposalWorkflowStates.filter(wf => wf.quickSelect || wf.name === item.workflowState)"/>
    </ul>
</template>
<script>
import { mapState, mapGetters, mapMutations, mapActions } from 'vuex';

import Proposal from './Proposal.vue';

const noop = ()=>{};

export default {
    data() {
        return {
            proposalActions: {
                right: this.deselectProposal,
                setWorkflowState: this.setProposalWorkflowState
            }
        }
    },
    components: {
        Proposal
    },
    methods: {
        ...mapMutations('projector', ['deselectProposal']),
        ...mapActions('projector', ['setProposalWorkflowState'])
    },
    computed: {
        ...mapGetters('projector', ['selectedProposals']),
        ...mapState('projector', ['proposalWorkflowStates'])
    }
}
</script>