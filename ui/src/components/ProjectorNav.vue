<template>

    <nav id="fixed-top-nav" class="navbar-fixed-top" role="navigation">

        <div class="container-fluid">
            <a class="voteit-logo-nav" :href="currentAgendaItem ? currentAgendaItem.href : href"></a>
            <a class="text-overflow voteit-nav-header"
               :href="currentAgendaItem ? currentAgendaItem.href : href">
                <span v-if="currentAgendaItem">{{ currentAgendaItem.title }}</span>
                <span v-else>
                    <span class="hidden-sm hidden-xs">{{ title }}: </span>
                    ({{ $t('Click menu to select Agenda Item') }})
                </span>
            </a>

            <ul class="nav voteit-nav navbar-right" id="navbar-controls">

                <li v-if="nextTagInOrder">
                    <a href="#" @click.prevent="filterByTag(nextTagInOrder)"
                    :title="'#'+nextTagInOrder">
                    <span class="glyphicon glyphicon-tags"> </span>
                    </a>
                </li>

                <li class="dropdown">
                    <a href="#" class="dropdown-toggle"
                       :title="$t('Quickly create a poll')"
                       data-toggle="dropdown"
                       aria-expanded="false">
                        <span class="glyphicon glyphicon-star"> </span>
                        <span class="caret"> </span>
                    </a>
                    <ul class="dropdown-menu" id="quick-polls">
                        <li
                            role="presentation"
                            v-for="item in pollList"
                            :key="item.name || item.title"
                            :class="{'dropdown-header': !item.name && item.title, divider: !item.title, disabled: !pollAvailable(item)}">
                            <span v-if="!item.name">{{ item.title }}</span>
                            <a v-else-if="item.title"
                               role="menuitem"
                               :href="'#' + item.name"
                               @click.prevent="quickPoll(item)">
                                {{ item.title }} <span v-if="item.rejectProp">({{ $t('add reject') }})</span>
                            </a>
                        </li>

                        <li v-if="pollsOngoing.length" role="presentation" class="divider"> </li>
                        <li v-if="pollsOngoing.length" role="presentation" class="dropdown-header">
                            <span>{{ $t('Ongoing polls') }}</span>
                        </li>

                        <li v-for="poll in pollsOngoing" :key="poll.uid">
                            <a role="menuitem"
                               @click.prevent="openPoll(poll)"
                               :href="poll.href">
                                {{ poll.title }}
                                <div class="progress">
                                    <div class="progress-bar progress-bar-success" role="progress-bar" :style="'width: ' + 100 * poll.votes / poll.potentialVotes + '%'">
                                        {{ poll.votes }} / {{ poll.potentialVotes }}
                                    </div>
                                </div>
                            </a>
                        </li>

                        <li v-if="pollsClosed.length" role="presentation" class="divider"> </li>
                        <li v-if="pollsClosed.length" role="presentation" class="dropdown-header">
                            <span>{{ $t('Closed polls') }}</span>
                        </li>

                        <li v-for="poll in pollsClosed" :key="poll.uid">
                            <a role="menuitem"
                               @click.prevent="openPoll(poll)"
                               :href="poll.href">
                                {{ poll.title }}
                            </a>
                        </li>
                    </ul>
                </li>

                <li class="dropdown">
                    <a id="proposal-filtering"
                       class="dropdown-toggle"
                       data-toggle="dropdown"
                       aria-haspopup="true"
                       aria-expanded="false">
                        <span class="glyphicon glyphicon-filter"> </span><span class="caret"> </span>
                    </a>
                    <ul class="dropdown-menu" id="proposal-filters" aria-labelledby="proposal-filtering">

                        <li class="text-nowrap" v-for="state in proposalWorkflowStates" :key="state.name" @click.stop :class="{ active: state.checked }">
                            <a>
                                <input type="checkbox" :id="state.name" :checked="state.checked" @change.prevent="toggleProposalWorkflow(state.name)" />
                                <label :for="state.name">{{ state.title }}</label>
                                <span class="badge">{{ proposals.filter(p=>p.workflowState === state.name).length }}</span>
                            </a>
                        </li>
                    </ul>
                </li>

                <li :class="{disabled: !previousAgendaItem}">
                    <a href="#"
                    :title="previousAgendaItem ? previousAgendaItem.title : $t('Previous')"
                    @click.prevent="loadAgendaItem(previousAgendaItem)">
                        <span class="glyphicon glyphicon-chevron-left"> </span>
                    </a>
                </li>
                <li :class="{disabled: !nextAgendaItem}">
                    <a href="#"
                    :title="nextAgendaItem ? nextAgendaItem.title : $t('Next')"
                    @click.prevent="loadAgendaItem(nextAgendaItem)">
                        <span class="glyphicon glyphicon-chevron-right"> </span>
                    </a>
                </li>

                <li class="dropdown">
                    <a href="#" class="dropdown-toggle"
                       data-toggle="dropdown"
                       aria-expanded="false">
                        <span class="glyphicon glyphicon-list"> </span>
                        <span class="caret"> </span>
                    </a>
                    <ul class="dropdown-menu" id="projector-ai-menu">
                        <li role="presentation" class="dropdown-header">
                            <span class="glyphicon glyphicon-ongoing text-ongoing"> </span>
                            {{ $t('ongoing') }}
                        </li>
                        <li role="presentation" v-for="ai in agendaStates.ongoing" :key="ai.uid">
                            <a role="menuitem"
                               @click.prevent="loadAgendaItem(ai)"
                               :href="'#' + ai.name">
                                {{ ai.title }}
                            </a>
                        </li>
                        <li role="presentation" class="divider"> </li>
                        <li role="presentation" class="dropdown-header">
                            <span class="glyphicon glyphicon-upcoming text-upcoming"> </span>
                            {{ $t('upcoming') }}
                        </li>
                        <li role="presentation" v-for="ai in agendaStates.upcoming" :key="ai.uid">
                            <a role="menuitem"
                                @click.prevent="loadAgendaItem(ai)"
                                :href="'#' + ai.name">
                                {{ ai.title }}
                            </a>
                        </li>
                    </ul>
                </li>
            </ul>
        </div><!-- /.container-->
        <div class="container container-float-below">
            <div class="float-below" data-flash-slot="voteit-main"></div>
        </div>
        <flash-messages/>
    </nav>
</template>
<script src="./ProjectorNav.js"></script>
<style lang="sass">
#proposal-filters
    li
        padding-right: 5px
    input
        margin-left: 6px
    label
        padding: 3px 5px
        font-weight: normal

.navbar
    a[role="checkbox"]
        opacity: .2
        &[aria-checked]
            opacity: 1
</style>
