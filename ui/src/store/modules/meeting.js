const AGENDA_STATES = [
    'ongoing',
    'upcoming',
    'closed',
    'private'
]

const getRelativeAgendaItem = (state, position) => {
    const ai = state.agenda.find(ai => ai.uid === state.currentAgendaItemUid);
    const index = state.agenda.indexOf(ai) + position;
    if (-1 < index && index < state.agenda.length)
        return state.agenda[index];
}

export default {
    namespaced: true,

    state: {
        title: '',
        href: '',
        agenda: [],
        currentAgendaItemUid: undefined,
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
        currentAgendaItem(state) {
            return state.agenda.find(ai => ai.uid === state.currentAgendaItemUid);
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
        setAgenda(state, agenda) {
            state.agenda = agenda;
        },
        setAgendaItem(state, uid) {
            state.currentAgendaItemUid = uid;
        }
    },
}