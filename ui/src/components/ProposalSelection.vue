<template>
    <ul id="projector-pool" class="list-group" >
        <proposal
            v-for="item in filteredProposals"
            :key="item.uid"
            :actions="proposalActions"
            :item="item" />
    </ul>
</template>
<script src="./ProposalSelection.js"></script>
