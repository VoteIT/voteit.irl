import { mapGetters, mapState, mapActions, mapMutations } from 'vuex'

const UPDATE_INTERVAL = 5000;

export default {
    methods: {
        ...mapMutations('projector', ['toggleProposalWorkflow']),
        ...mapActions('projector', ['loadAgendaItem', 'updateAgendaItems']),
        pollAvailable(poll) {
            if (poll.proposalsMin && this.proposalSelection.length < poll.proposalsMin)
                return false
            if (poll.proposalsMax && this.proposalSelection.length > poll.proposalsMax)
                return false
            return true
        }
    },
    computed: {
        ...mapState('meeting', ['href', 'title', 'agenda', 'currentAgendaItem', 'hrefLastPollResult']),
        ...mapGetters('meeting', ['agendaStates', 'previousAgendaItem', 'nextAgendaItem']),
        ...mapState('projector', ['proposalWorkflowStates', 'pollGroups', 'proposalSelection', 'proposals']),
        pollList() {
            let list = [];
            this.pollGroups.forEach((group,i) => {
                list.push(group);
                list = list.concat(group.methods);
                list.push({id: 'divider-' + i});
            });
            return list;
        }
    },
    created() {
        setInterval(() => this.updateAgendaItems(true), UPDATE_INTERVAL);
    }
}
