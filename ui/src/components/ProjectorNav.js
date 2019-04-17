import { mapGetters, mapState, mapActions, mapMutations } from 'vuex';
import { ModalLink, FlashMessages } from '../core_components';

const UPDATE_INTERVAL = 5000;

export default {
    components: {
        ModalLink,
        FlashMessages
    },
    methods: {
        ...mapMutations('projector', ['toggleProposalWorkflow']),
        ...mapActions('projector', ['loadAgendaItem', 'updateAgendaItems']),
        pollAvailable(poll) {
            if (poll.proposalsMin && this.proposalSelection.length < poll.proposalsMin)
                return false
            if (poll.proposalsMax && this.proposalSelection.length > poll.proposalsMax)
                return false
            return true
        },
        openLatestPollResult() {

        },
        quickPoll(pollMethod) {
            if (!this.pollAvailable(pollMethod))
                return;
            $.post(this.api.quickPoll, {
                method: pollMethod.name,
                proposals: this.proposalSelection
            })
            .done(response => {
                this.$root.$emit('flash::display', {
                    content: response.msg,
                    timeout: null
                })
            })
            .fail((err) => {
                console.log(err)
                this.$root.$emit('flash::display', {
                    content: err.statusText,  // TODO - display whatever error server sends
                    type: 'danger'
                })
            });
        }
    },
    computed: {
        ...mapState('meeting', ['href', 'title', 'agenda', 'currentAgendaItem', 'hrefLastPollResult']),
        ...mapGetters('meeting', ['agendaStates', 'previousAgendaItem', 'nextAgendaItem']),
        ...mapState('projector', ['proposalWorkflowStates', 'pollGroups', 'proposalSelection', 'proposals',
                                  'api', 'logo', 'pollsOngoing', 'pollsClosed']),
        pollList() {
            let list = [];
            this.pollGroups.forEach((group,i) => {
                if (i > 0)
                    list.push({id: 'divider-' + i});
                list.push(group);
                list = list.concat(group.methods);
            });
            return list;
        }
    },
    created() {
        setInterval(() => this.updateAgendaItems(true), UPDATE_INTERVAL);
    }
}
