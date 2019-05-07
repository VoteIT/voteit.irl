import { mapActions, mapMutations } from 'vuex';

import { ProjectorNav, ProposalSelection, ProposalsMain } from 'components';
import { Modal, FlashMessages } from 'arche';
import { requests } from 'arche/utils';

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
        FlashMessages
    },
    created() {
        requests.get($('body').data('src'))
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
        $('body').on('click', '[data-tag-filter]', event => {
            event.preventDefault();
            const tagName = $(event.currentTarget).data('tagFilter').toLowerCase();
            this.filterByTag(tagName);
        });
    },
    methods: {
        ...mapActions('projector', ['loadAgendaItemByName']),
        ...mapMutations('projector', ['filterByTag'])
    }
}
