// Important! Always return request
let requestQueue = [];
let hasOnlineEventListener = false;

function doRequest(state, commit, fn, options) {
    let { persist, failHard } = options || {};
    if (navigator.onLine && !state.requestActive) {
        commit('setRequestActive', true);
        fn().always(()=> {
            commit('setRequestActive', false);
            if (requestQueue.length)
                doRequest(state, commit, requestQueue.shift(), { failHard: true });
        })
    }
    else {
        if (!navigator.onLine && !hasOnlineEventListener) {
            window.addEventListener('online', ()=> {
                if (requestQueue.length)
                    doRequest(state, commit, requestQueue.shift(), { failHard: true });
            });
            hasOnlineEventListener = true;
        }
        if (persist) {
            requestQueue.push(fn);
        }
        else if (failHard) {
            throw new Error('Request failed!');
        }
    }
}

export default {
    namespaced: true,

    state: {
        proposalWorkflowStates: [],
        pollGroups: [],
        proposals: [],
        proposalSelection: [],  // uids
        proposalOrder: [],  // uids
        pollsOngoing: [],
        pollsClosed: [],
        agendaUrl: null,
        requestActive: false,
        api: {},
        logo: ''
    },

    getters: {
        filteredProposals(state) {
            let onStates = {};
            state.proposalWorkflowStates.forEach(state => {
                if (state.checked)
                    onStates[state.name] = true;
            });
            return state.proposalOrder.map(uid => {
                return state.proposals.find(p => p.uid === uid);
            }).filter(prop => {
                return prop.workflowState in onStates && !state.proposalSelection.includes(prop.uid);
            });
        },
        selectedProposals(state) {
            return state.proposalSelection.map(uid => state.proposals.find(prop => prop.uid === uid));
        }
    },

    mutations: {
        load(state, data) {
            state.proposalWorkflowStates = data.proposalWorkflowStates;
            state.pollGroups = data.pollGroups;
            state.api = data.api;
            state.logo = data.logo;
        },
        setAgendaUrl(state, url) {
            state.agendaUrl = url;
            state.proposals = [];
            state.proposalSelection = [];
            state.proposalOrder = [];
            state.pollsOngoing = [];
            state.pollsClosed = [];
        },
        loadAgendaItem(state, data) {
            state.proposals = data.proposals;
            state.pollsOngoing = data.pollsOngoing;
            state.pollsClosed = data.pollsClosed;

            // Remove deleted proposals from order and selection
            const containsFilter = uid => state.proposals.find(p => p.uid === uid) !== undefined;
            state.proposalOrder = state.proposalOrder.filter(containsFilter);
            state.proposalSelection = state.proposalSelection.filter(containsFilter);

            // Push new proposals to proposalOrder
            data.proposals.forEach(proposal => {
                if (!state.proposalOrder.includes(proposal.uid))
                    state.proposalOrder.push(proposal.uid);
            });
        },
        toggleProposalWorkflow(state, name) {
            const wf = state.proposalWorkflowStates.find(state => state.name===name);
            wf.checked = !wf.checked;
        },
        setProposalWorkflowState(state, {proposal, workflowState}) {
            proposal.workflowState = workflowState.name;
        },
        downShift(state, proposal) { // Get it?
            state.proposalOrder.splice(state.proposalOrder.indexOf(proposal.uid), 1);
            state.proposalOrder.push(proposal.uid);
        },
        selectProposal(state, proposal) {
            state.proposalSelection.unshift(proposal.uid);
        },
        deselectProposal(state, proposal) {
            state.proposalSelection.splice(state.proposalSelection.indexOf(proposal.uid), 1);
        },
        setRequestActive(state, value) {
            state.requestActive = value;
        }
    },

    actions: {
        updateAgendaItems({ state, commit }, polling=false) {
            if (state.agendaUrl && !(polling && document.hidden)) {
                doRequest(state, commit, () => {
                    return $.get(state.agendaUrl)
                    .done(data => {
                        commit('loadAgendaItem', data);
                    });
                }, { persist: !polling });
            }
        },
        loadAgendaItem({ state, commit, dispatch }, ai) {
            if (ai && state.agendaUrl !== ai.jsonUrl) {
                commit('meeting/setAgendaItem', ai.name, {root: true});
                commit('setAgendaUrl', ai.jsonUrl);
                dispatch('updateAgendaItems');
            }
        },
        setProposalWorkflowState({ state, commit }, { proposal, workflowState }) {
            if (proposal.workflowState !== workflowState.name) {
                doRequest(state, commit, () => {
                    return $.post(proposal.workflowApi, { state: workflowState.name })
                    .done(() => {  // FIXME Needs to respond with new proposal data
                        commit('setProposalWorkflowState', { proposal, workflowState });
                    })
                });
            }
        }
    }
}