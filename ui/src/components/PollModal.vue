<template>
    <div v-if="result">
        <div class="modal-content" v-html="result"></div>
    </div>
    <div v-else class="modal-content" id="poll-modal">
        <div class="modal-header">
            <button type="button" class="close" data-dismiss="modal" :aria-label="$t('Close')">
                <span aria-hidden="true">&times;</span>
            </button>
            <h4 class="modal-title">{{ poll.title }} <small>({{ $t('Ongoing') }})</small></h4>
        </div>
        <div class="modal-body" v-if="poll.workflowState === 'ongoing'">
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
            <div>
                <button class="btn btn-primary" @click="closePoll(poll.uid)">{{ $t('Stäng omröstning') }}</button>
            </div>
        </div>
    </div>
</template>
<script>
import { mapActions, mapGetters } from 'vuex';
import { requests } from 'arche/utils';

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
        ...mapActions('projector', ['closePoll']),
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
        }
    }
}
</script>
<style lang="sass">
#poll-modal
    .progress-bar
        min-width: fit-content
</style>
