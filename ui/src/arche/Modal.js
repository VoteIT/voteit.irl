import { eventBus, requests } from 'arche/utils';

const MODAL_DEFAULTS = {
    backdrop: true,
    modelDialogClass: null
};

export default {
    data() {
        return {
            modelDialogClass: null,
            content: null,
            backdrop: true,
            component: null
        }
    },
    methods: {
        open(params) {
            $(this.$el).modal(params);
        },
        close() {
            $(this.$el).modal({ show: false });
        }
    },
    created() {
        eventBus.$on('modal::open', options => {
            this.component = null;

            options = $.extend({}, MODAL_DEFAULTS, options);
            this.content = options.content;
            this.backdrop = options.backdrop;
            this.modelDialogClass = options.modelDialogClass;
            if (options.href) {
                requests.get(options.href)
                .done(response => {
                    this.content = response;
                    this.open(options.params);
                });
            }
            else if (options.component) {
                this.component = options.component;
                this.open(options.params)
            }
            else {
                this.open(options.params);
            }
        });
        eventBus.$on('modal::close', () => {
            this.close();
        });
    },
    mounted() {
        // Handle bootstrap closing
        $(this.$el).modal({ show: false })
        .on('hidden.bs.modal', () => {
            this.component = null;
            this.content = null;
        });
    }
}
