<template>
    <ul id="projector-main" class="list-group">
        <proposal
            v-for="item in selectedProposals"
            :key="item.uid"
            :actions="proposalActions"
            :item="item"
            quick-select />
    </ul>
</template>
<script>
import { mapGetters, mapMutations, mapActions } from 'vuex';

import Proposal from './Proposal.vue';

export default {
    data() {
        return {
            proposalActions: {
                right: this.deselectProposal,
                setWorkflowState: this.setProposalWorkflowState,
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
        ...mapGetters('projector', ['selectedProposals'])
    }
}
</script>