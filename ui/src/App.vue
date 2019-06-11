<template>
    <div id="app">
        <div class="loading" v-if="!ready">Loading...</div>
        <projector-nav v-if="ready"/>
        <div class="container-fluid" v-if="ready">
            <div class="row">
                <div class="col-xs-10">
                    <proposals-main/>
                </div>
                <div class="col-xs-2 fixed-right">
                    <proposal-selection/>
                </div>
            </div>
        </div>
        <modal/>
    </div>
</template>

<script src="./App.js"></script>

<style lang="sass">

body
    padding: 0

.proposal
    .btn-group
        margin-right: .4rem

.fixed-right
    overflow-y: auto
    position: fixed
    float: none
    top: 70px
    right: 0
    bottom: 0
    margin-bottom: 0
    padding: 0

#quick-polls
    .progress
        margin: 4px 0
    .progress-bar
        min-width: 4em
        min-width: fit-content

#projector-pool
    li
        border-top-right-radius: 0
        border-bottom-right-radius: 0
        border-right: 0
    h3
        font-size: 100%
    .proposal-text
        margin-bottom: 5px
        padding-bottom: 5px
        max-height: 150px
        overflow: hidden
        position: relative
        &::before
            content: ''
            width: 100%
            height: 20%
            position: absolute
            left: 0
            top: 80%
            background: linear-gradient(rgba(#fff,0), rgba(#fff,1))

#projector-main
    .proposal-text
        font-size: 150%
</style>
