const AGENDA_STATES = [
    'ongoing',
    'upcoming',
    'closed',
    'private'
]

const getRelativeAgendaItem = (state, position) => {
    const index = state.agenda.indexOf(state.currentAgendaItem) + position;
    if (-1 < index && index < state.agenda.length)
        return state.agenda[index];
}

export default {
    namespaced: true,

    state: {
        title: '',
        href: '',
        agenda: [],
        currentAgendaItem: undefined,
        loaded: false
    },

    getters: {
        agendaStates(state) {
            let states = {};
            AGENDA_STATES.forEach(wf => {
                states[wf] = state.agenda.filter(ai => ai.workflowState === wf);
            });
            return states;
        },
        previousAgendaItem(state) {
            return getRelativeAgendaItem(state, -1);
        },
        nextAgendaItem(state) {
            return getRelativeAgendaItem(state, 1);
        },
    },

    mutations: {
        load(state, data) {
            Object.keys(data).forEach(key => {
                state[key] = data[key];
            });
            state.loaded = true;
        },
        setAgendaItem(state, name) {
            state.currentAgendaItem = state.agenda.find(item => item.name===name);
        }
    },
}