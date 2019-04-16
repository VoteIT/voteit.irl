<template>
    <ul id="projector-pool" class="list-group" >
        <proposal
            v-for="item in filteredProposals"
            :key="item.uid"
            :actions="proposalActions"
            :item="item"
            :workflowStates="[proposalWorkflowStates.find(wf => wf.name === item.workflowState)]"/>
    </ul>
</template>
<script src="./ProposalSelection.js"></script>
