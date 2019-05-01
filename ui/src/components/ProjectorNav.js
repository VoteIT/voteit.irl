import { mapGetters, mapState, mapActions, mapMutations } from 'vuex';
import { ModalLink, FlashMessages } from '../core_components';
import { flashMessage, doRequest } from '../core_components/utils';

const UPDATE_INTERVAL = 5000;

export default {
    components: {
        ModalLink,
        FlashMessages
    },
    methods: {
        ...mapMutations('projector', ['toggleProposalWorkflow']),
        ...mapActions('projector', ['updateAgendaItems']),
        pollAvailable(poll) {
            // If a reject proposal is added, that's another proposal. Add one.
            const len = this.proposalSelection.length + (poll.rejectProp ? 1 : 0);
            if (poll.proposalsMin && len < poll.proposalsMin)
                return false
            if (poll.proposalsMax && len > poll.proposalsMax)
                return false
            return true
        },
        quickPoll(pollMethod) {
            if (!this.pollAvailable(pollMethod))
                return;
            doRequest(this.api.quickPoll, {
                method: 'POST',
                data: {
                    'quick-poll-method': pollMethod.name,
                    'uid': this.proposalSelection,
                    'reject-prop': pollMethod.rejectProp
                }
            })
            .done(response => {
                flashMessage(response.msg, { timeout: null });
            });
        },
        loadAgendaItem(ai) {
            if (ai) {
                this.$store.dispatch('projector/loadAgendaItem', ai);
                history.pushState(ai, ai.title, '#' + ai.name);
            }
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
