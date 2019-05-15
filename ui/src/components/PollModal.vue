<template>
    <div v-if="result">
        <div class="modal-content" v-html="result"></div>
    </div>
    <div v-else class="modal-content" id="poll-modal">
        <div class="modal-header">
            <button type="button" class="close" data-dismiss="modal" :aria-label="$t('Close')">
                <span aria-hidden="true">&times;</span>
            </button>
            <h4 class="modal-title">{{ poll.title }} <small>({{ $t(poll.workflowState) }})</small></h4>
        </div>
        <div class="modal-body">
            <div class="progress">
                <div
                    class="progress-bar progress-bar-success progress-bar-striped active"
                    role="progress-bar"
                    aria-valuemin="0"
                    :aria-valuenow="poll.votes"
                    :aria-valuemax="poll.potentialVotes"
                    :style="'width: ' + 100 * poll.votes / poll.potentialVotes + '%'">
                    {{ poll.votes }} / {{ poll.potentialVotes }} <span class="sr-only">{{ $t('votes') }}</span>
                </div>
            </div>
            <div class="btn-group">
                <button type="button" class="btn btn-xs btn-default dropdown-toggle" data-toggle="dropdown" aria-expanded="false">
                    <span class="text-ongoing">
                        <span class="glyphicon glyphicon-ongoing"></span>
                        <span>{{ $t($t(poll.workflowState)) }}</span>
                        <span class="caret"></span>
                    </span>
                </button>
                <ul class="dropdown-menu" role="menu">
                    <li v-for="state in ['canceled', 'closed']" :key="state">
                        <a :href="'#' + state" @click.prevent="setPollWorkflowState({ poll, workflowState: state })">
                            <span :class="'glyphicon glyphicon-' + state + ' text-' + state"></span>
                            <span>{{ $t(state) }}</span>
                        </a>
                    </li>
                </ul>
            </div>
        </div>
    </div>
</template>
<script>
import { mapActions, mapGetters } from 'vuex';
import { requests, modal } from 'arche/utils';

export default {
    data() {
        return {
            result: null
        }
    },
    created() {
        if (this.poll.workflowState === 'closed')
            this.getResult(this.poll.href);
    },
    methods: {
        ...mapActions('projector', ['setPollWorkflowState']),
        getResult(href) {
            requests.get(href)
            .done(data => {
                this.result = data;
            });
        }
    },
    computed: {
        ...mapGetters('projector', ['openPoll']),
        poll() {
            return this.openPoll;
        },
        pollState() {
            return this.openPoll && this.openPoll.workflowState;
        }
    },
    watch: {
        pollState(state) {
            if (state === 'closed')
                this.getResult(this.openPoll.href);
            if (state === 'canceled')
                modal.close();
        }
    }
}
</script>
<style lang="sass">
#poll-modal
    .progress-bar
        min-width: fit-content
    .btn-group
        .glyphicon
            margin-right: 5px
        .caret
            margin-left: 5px
</style>
