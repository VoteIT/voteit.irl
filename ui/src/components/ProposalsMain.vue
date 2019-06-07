<template>
    <ul id="projector-main" class="list-group" v-if="selectedProposals.length">
        <proposal
            v-for="item in selectedProposals"
            :key="item.uid"
            :actions="proposalActions"
            :item="item"
            quick-select />
    </ul>
    <div v-else-if="nextTagInOrder" id="projector-action-centered">
        <button class="btn btn-lg" @click="filterByTag(nextTagInOrder)">
            {{ $t('Next') }}: <strong>#{{ nextTagInOrder }}</strong>
        </button>
    </div>
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
        ...mapMutations('projector', ['deselectProposal', 'filterByTag']),
        ...mapActions('projector', ['setProposalWorkflowState'])
    },
    computed: {
        ...mapGetters('projector', ['selectedProposals', 'nextTagInOrder'])
    }
}
</script>
<style lang="sass">
#projector-action-centered
    padding-top: 60px
    text-align: center
</style>
