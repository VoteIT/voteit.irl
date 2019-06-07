import { eventBus } from './utils'

const MESSAGE_DEFAULTS = {
    type: 'success',
    timeout: 3000
}

export default {
    data() {
        return {
            messages: [],
        }
    },
    created() {
        eventBus.$on('flash::display', msg => {
            msg = $.extend({}, MESSAGE_DEFAULTS, msg);
            if (!msg.id)
                msg.id = this.messages.length ?
                    Math.max(...this.messages.map(msg => typeof msg.id === 'number' ? msg.id : 0)) + 1 :
                    1;
            this.messages.push(msg);
            if (msg.timeout) {
                setTimeout(()=> {
                    this.messages.splice(this.messages.indexOf(msg), 1)
                }, msg.timeout);
            }
        })
    }
}
