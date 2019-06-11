import { mapGetters, mapState, mapActions, mapMutations } from 'vuex';
import { ModalLink, FlashMessages } from 'arche';
import { requests, modal } from 'arche/utils';
import PollModal from 'components/PollModal.vue';
import Proposal from './Proposal.vue';


export default {
    components: {
        ModalLink,
        FlashMessages,
        Proposal
    },
    methods: {
        ...mapMutations('projector', ['toggleProposalWorkflow', 'updateProposals', 'selectProposals', 'setOpenPollUid', 'updatePoll', 'filterByTag']),
        ...mapActions('projector', ['updateAgendaItems']),
        pollAvailable(poll) {
            // If a reject proposal is added, that's another proposal. +1
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
            requests.post(this.api.quickPoll, {
                'quick-poll-method': pollMethod.name,
                'uid': this.proposalSelection,
                'reject-prop': pollMethod.rejectProp
            })
            .done(data => {
                this.updateProposals(data.proposals);
                this.selectProposals(data.proposals);
                this.updatePoll(data.poll);
                this.openPoll(data.poll);
            });
        },
        loadAgendaItem(ai) {
            if (ai) {
                this.$store.dispatch('projector/loadAgendaItem', ai);
                history.pushState(ai, ai.title, '#' + ai.name);
            }
        },
        openPoll(poll) {
            this.setOpenPollUid(poll.uid);
            modal.open({
                component: PollModal,
                modelDialogClass: "modal-lg"
            })
        }
    },
    computed: {
        ...mapState('meeting', ['href', 'title', 'agenda', 'hrefLastPollResult']),
        ...mapGetters('meeting', ['agendaStates', 'previousAgendaItem', 'nextAgendaItem', 'currentAgendaItem']),
        ...mapState('projector', ['proposalWorkflowStates', 'pollGroups', 'proposalSelection', 'proposals',
                                  'api', 'logo']),
        ...mapGetters('projector', ['pollsOngoing', 'pollsClosed', 'selectedProposals', 'nextTagInOrder']),

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
}
