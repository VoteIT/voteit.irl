import { mapActions } from 'vuex';

import { ProjectorNav, ProposalSelection, ProposalsMain } from './components';
import { Modal, FlashMessage } from './core_components';

export default {
    name: 'app',
    data() {
        return {
            ready: false,
            src: $('body').data('src')
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
        $.get(this.src)
        .done(data => {
            this.$store.commit('meeting/load', data.meeting);
            this.$store.commit('projector/load', data);
            this.$root.ts = data.ts;
            this.ready = true;

            const name = location.hash[0] === '#' ? location.hash.slice(1) : location.hash;
            if (name)
                this.loadAgendaItemByName(name);
        });
        window.onpopstate = event => {
            this.loadAgendaItemByName(event.state && event.state.name);
        };
    },
    methods: {
        ...mapActions('projector', ['loadAgendaItemByName'])
    }
}
