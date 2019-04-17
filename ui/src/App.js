import { ProjectorNav, ProposalSelection, ProposalsMain } from './components';
import { Modal, FlashMessage } from './core_components';

export default {
    name: 'app',
    data() {
        return {
            ready: false
        };
    },
    components: {
        ProjectorNav,
        ProposalSelection,
        ProposalsMain,
        Modal,
        FlashMessage
    },
    created() {
        $.get($('body').data('src'))
        .done(data => {
            this.$store.commit('meeting/load', data.meeting);
            this.$store.commit('projector/load', data);
            this.$root.ts = data.ts;
            this.ready = true;
        });
    },
}
