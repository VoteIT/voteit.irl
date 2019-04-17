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
            component: null,
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
        this.$root.$on('modal::open', options => {
            options = $.extend({}, MODAL_DEFAULTS, options);
            this.content = options.content;
            this.backdrop = options.backdrop;
            this.modelDialogClass = options.modelDialogClass;
            if (options.href) {
                $.get(options.href)
                .done(response => {
                    this.content = response;
                    this.open(options.params);
                })
                .fail(err => {
                    this.$root.$emit('flash::display', {
                        content: err,
                        type: 'danger'
                    });  // Should prob be a util
                });
            } else {
                this.open(options.params);
            }
        });
        this.$root.$on('modal::close', () => {
            this.close();
        });
    }
}
