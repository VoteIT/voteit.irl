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
        ...mapActions('projector', ['updateAgendaItems']),
        pollAvailable(poll) {
            const len = poll.rejectProp ? this.proposalSelection.length + 1 : this.proposalSelection.length;
            if (poll.proposalsMin && len < poll.proposalsMin)
                return false
            if (poll.proposalsMax && len > poll.proposalsMax)
                return false
            return true
        },
        quickPoll(pollMethod) {
            if (!this.pollAvailable(pollMethod))
                return;
            $.post(this.api.quickPoll, {
                'quick-poll-method': pollMethod.name,
                'uid': this.proposalSelection,
                'reject-prop': pollMethod.rejectProp
            })
            .done(response => {
                this.$root.$emit('flash::display', {
                    content: response.msg,
                    timeout: null
                })
            })
            .fail((jqXHR) => {
                let msg;
                if (jqXHR.getResponseHeader('content-type') === "application/json" && typeof(jqXHR.responseText) == 'string') {
                    var parsed = $.parseJSON(jqXHR.responseText);
                    msg = '<h4>' + parsed.title + '</h4>';
                    if (parsed.body && parsed.body != parsed.title) {
                        msg += parsed.body;
                    } else if (parsed.message != parsed.title) {
                        msg += parsed.message;
                    }
                } else {
                    msg = '<h4>' + jqXHR.status + ' ' + jqXHR.statusText + '</h4>' + jqXHR.responseText
                }
                this.$root.$emit('flash::display', {
                    content: msg,  // TODO - display whatever error server sends
                    type: 'danger'
                })
            });
        },
        loadAgendaItem(ai) {
            this.$store.dispatch('projector/loadAgendaItem', ai);
            history.pushState(ai, ai.title, '#' + ai.name);
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
