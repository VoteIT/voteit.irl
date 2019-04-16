<template>
    <nav class="navbar navbar-static-top navbar-voteit" role="navigation">
        <div class="container-fluid" data-check-greedy>
            <a class="navbar-brand hidden-xs" href="/">
                <img height="31" width="85" class="voteitlogo"
                     src="${request.static_url('voteit.core:static/images/logo.png')}" />
            </a>
            <a class="navbar-brand greedy"
               id="navbar-heading"
               :href="currentAgendaItem ? currentAgendaItem.href : href">
                <span class="hidden-sm hidden-xs">{{ title }}: </span>
                <span v-if="currentAgendaItem">{{ currentAgendaItem.title }}</span>
                <span v-else>({{ $t('Click menu to select Agenda Item') }})</span>
            </a>
            <ul class="nav navbar-nav navbar-right">
            <li :class="{disabled: !previousAgendaItem}">
                <a href="#"
                   :title="$t('Previous')"
                   @click.prevent="loadAgendaItem(previousAgendaItem)">
                    <span class="glyphicon glyphicon-chevron-left"> </span>
                </a>
            </li>
            <li :class="{disabled: !nextAgendaItem}">
                <a href="#"
                   :title="$t('Next')"
                   @click.prevent="loadAgendaItem(nextAgendaItem)">
                    <span class="glyphicon glyphicon-chevron-right"> </span>
                </a>
            </li>
                <li class="dropdown">
                    <a href="#" class="dropdown-toggle"
                       title="Quickly create a poll"
                       i18n:attributes="title quick_poll_btn_title;"
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
                               @click.prevent>
                                {{ item.title }}
                            </a>
                        </li>

                        <li role="presentation" class="dropdown-header">
                            <span>{{ $t('Closed polls') }}</span>
                        </li>

                        <li>
                            <a role="menuitem"
                               data-open-modal
                               data-modal-dialog-class="modal-lg"
                               :href="hrefLastPollResult">
                                {{ $t('Show last poll result') }}
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
                        <span class="glyphicon glyphicon-filter"></span> <span class="caret"></span>
                    </a>
                    <ul class="dropdown-menu" id="proposal-filters" aria-labelledby="proposal-filtering">
                        <li class="text-nowrap" v-for="state in proposalWorkflowStates" :key="state.name" @click.stop :class="{ active: state.checked }">
                            <input type="checkbox" :id="state.name" :checked="state.checked" @change.prevent="toggleProposalWorkflow(state.name)" />
                            <label :for="state.name">{{ state.title }}</label>
                            <span class="badge">{{ proposals.filter(p=>p.workflowState === state.name).length }}</span>
                        </li>
                    </ul>
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
                            {{ $t('state:ongoing') }}
                        </li>
                        <li role="presentation" v-for="ai in agendaStates.ongoing" :key="ai.uid">
                            <a role="menuitem"
                               @click="loadAgendaItem(ai)"
                               :href="'#' + ai.uid">
                                {{ ai.title }}
                            </a>
                        </li>
                        <li role="presentation" class="divider"> </li>
                        <li role="presentation" class="dropdown-header">
                            <span class="glyphicon glyphicon-upcoming text-upcoming"> </span>
                            {{ $t('state:ongoing') }}
                        </li>
                        <li role="presentation" v-for="ai in agendaStates.upcoming" :key="ai.uid">
                            <a role="menuitem"
                                @click="loadAgendaItem(ai)"
                                :href="'#' + ai.uid">
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
</style>