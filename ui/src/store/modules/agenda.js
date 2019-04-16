const STATES = {
    empty: 1,
    loading: 2,
    loaded: 3
}

export default {
    namespaced: true,

    state: {
        jsonUrl: '',
        proposals: [],
        state: STATES.empty
    },

    mutations: {
        setJsonUrl(state, url) {
            state.jsonUrl = url;
        },
        clear(state) {
            state.proposals = [];
        },
        setState(state, s) {
            state.state = s;
        },
        setProposals(state, proposals) {
            state.proposals = proposals;
            state.state = STATES.loaded;
        }
    },

    actions: {
        load({ commit, dispatch }, url) {
            commit('setJsonUrl', url)
            commit('setState', STATES.loading);
            commit('clear');
            $.get(url)
            .done(data => {
                commit('setProposals', data.proposals);
            });
        }
    }
}
