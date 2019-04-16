import ProjectorNav from './components/ProjectorNav.vue';
import ProposalSelection from './components/ProposalSelection.vue';
import ProposalsMain from './components/ProposalsMain.vue';

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
        ProposalsMain
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
