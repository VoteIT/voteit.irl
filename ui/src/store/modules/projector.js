import { requests, polling } from "arche/utils";

export default {
    namespaced: true,

    state: {
        proposalWorkflowStates: [],
        pollGroups: [],
        proposals: [],
        proposalSelection: [],  // uids
        proposalOrder: [],  // uids
        polls: [],
        agendaUrl: null,
        requestActive: false,
        api: {},
        logo: '',
        openPollUid: null,
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
        },
        pollsOngoing(state) {
            return state.polls.filter(p => p.workflowState === 'ongoing');
        },
        pollsClosed(state) {
            return state.polls.filter(p => p.workflowState === 'closed');
        },
        openPoll(state) {
            return state.polls.find(p => p.uid === state.openPollUid);
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
            state.polls = [];
        },
        loadAgendaItem(state, data) {
            // To reset projector (I.E. if current Agenda Item is gone)
            data = data || { proposals: [], pollsOngoing: [], pollsClosed: [] }
            state.proposals = data.proposals;
            state.polls = data.polls;

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
            state.proposalSelection.push(proposal.uid);
        },
        selectProposals(state, proposals) {
            state.proposalSelection = proposals.map(p => p.uid);
        },
        deselectProposal(state, proposal) {
            state.proposalSelection.splice(state.proposalSelection.indexOf(proposal.uid), 1);
        },
        updateProposals(state, proposals) {
            // For state changes to a subset of proposals, i.e. with quickPoll.
            // Can add proposals, but not remove.
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
        },
        setOpenPollUid(state, uid) {
            state.openPollUid = uid;
        },
        updatePoll(state, data) {
            const poll = state.polls.find(p => p.uid === data.uid);
            if (poll)
                Object.assign(poll, data);
            else
                state.polls.push(data);
        }
    },

    actions: {
        loadAgendaItem({ state, commit }, ai) {
            if (state.agendaUrl) {
                polling.clearService(state.agendaUrl);
            }
            ai = ai || {jsonUrl: null, uid: null};
            commit('meeting/setAgendaItem', ai.uid, {root: true});
            commit('setAgendaUrl', ai.jsonUrl);
            if (ai.jsonUrl) {
                polling.addService(
                    ai.jsonUrl,
                    state.api.pollIntervalTime * 1000, 
                    data => {
                        // This function is called on poll requests done().
                        // Update meeting agenda first.
                        commit('meeting/setAgenda', data.agenda, { root: true });
                        // Check if current ai in incoming agenda.
                        if (data.agenda.find(newAi => newAi.uid === ai.uid)) {
                            commit('loadAgendaItem', data);
                        }
                        else {
                            // If current AI is not in incoming list it will reset view and stop polling.
                            commit('loadAgendaItem');
                            polling.clearService(ai.jsonUrl);
                        }
                    }
                );
            }
        },
        loadAgendaItemByName({ rootState, dispatch }, name) {
            // Used for loading agenda item from url hash string
            const ai = rootState.meeting.agenda.find(ai => ai.name === name);
            dispatch('loadAgendaItem', ai);
        },
        setProposalWorkflowState({ state, commit }, { proposal, workflowState }) {
            // Change proposal workflow, i.e. set proposal to approved, denied, published.
            const current = state.proposalWorkflowStates.find(wf => wf.name === proposal.workflowState);
            if (workflowState.quickSelect && current !== workflowState) {
                // TODO: Lock proposal controls during request.
                requests.post(proposal.workflowApi, {
                    state: workflowState.name
                })
                .done(data => {
                    const workflowState = state.proposalWorkflowStates.find(wf => wf.name === data.state);
                    commit('setProposalWorkflowState', { proposal, workflowState });
                });
            }
        },
        setPollWorkflowState({ commit }, { poll, workflowState }) {
            // TODO Send to backend
            requests.post(poll.api, { state: workflowState })
            .done(data => {
                commit('updatePoll', data)
            });
        }
    }
}
