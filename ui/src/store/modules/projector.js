import { requests } from "src/core_components/utils";

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
        selectProposals(state, proposals) {
            state.proposalSelection = proposals.map(p => p.uid);
        },
        deselectProposal(state, proposal) {
            state.proposalSelection.splice(state.proposalSelection.indexOf(proposal.uid), 1);
        },
        updateProposals(state, proposals) {
            proposals.forEach(incoming => {
                const prop = state.proposals.find(p => p.uid === incoming.uid);
                if (prop !== undefined) {
                    Object.assign(prop, incoming);
                } else {
                    state.proposals.push(incoming);
                }
            });
        },
        setRequestActive(state, value) {
            state.requestActive = value;
        },
        filterByTag(state, tagName) {
            let onStates = {};
            state.proposalWorkflowStates.forEach(state => {
                if (state.checked)
                    onStates[state.name] = true;
            });
            state.proposalSelection = state.proposals
                .filter(p => p.tags.indexOf(tagName) !== -1 && p.workflowState in onStates)
                .map(p => p.uid);
        }
    },

    actions: {
        updateAgendaItems({ state, commit }, polling=false) {
            // If agenda item active.
            // If polling: only if document is visible.
            if (state.agendaUrl && !(polling && document.hidden)) {
                requests.get(state.agendaUrl, { polling })
                .done(data => {
                    commit('loadAgendaItem', data);
                });
            }
        },
        loadAgendaItem({ commit, dispatch }, ai) {
            if (ai) {
                commit('meeting/setAgendaItem', ai.uid, {root: true});
                commit('setAgendaUrl', ai.jsonUrl);
                dispatch('updateAgendaItems');
            }
        },
        loadAgendaItemByName({ rootState, dispatch }, name) {
            const ai = rootState.meeting.agenda.find(ai => ai.name === name) || {jsonUrl: null, uid: null};
            dispatch('loadAgendaItem', ai);
        },
        setProposalWorkflowState({ state, commit }, { proposal, workflowState }) {
            const current = state.proposalWorkflowStates.find(wf => wf.name === proposal.workflowState);
            if (workflowState.quickSelect && current !== workflowState) {
                requests.post(proposal.workflowApi, {
                    state: workflowState.name
                })
                .done(data => {
                    const workflowState = state.proposalWorkflowStates.find(wf => wf.name === data.state);
                    commit('setProposalWorkflowState', { proposal, workflowState });
                });
            }
        }
    }
}