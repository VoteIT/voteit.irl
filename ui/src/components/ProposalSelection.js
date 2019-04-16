import { mapState, mapGetters, mapMutations } from 'vuex';

import Proposal from './Proposal.vue';

export default {
    data() {
        return {
            proposalActions: {
                left: this.selectProposal,
                right: this.downShift
            }
        }
    },
    components: {
        Proposal
    },
    methods: {
        ...mapMutations('projector', ['selectProposal', 'downShift'])
    },
    computed: {
        ...mapState('projector', ['proposalWorkflowStates']),
        ...mapGetters('projector', ['filteredProposals'])
    }
}
