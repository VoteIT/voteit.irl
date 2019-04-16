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
    </div>
</template>

<script src="./App.js"></script>

<style lang="sass">
@import ../../../voteit.core/voteit/core/scss/main

body
    padding: 0

.proposal
    .btn-group
        margin-right: .4rem

.fixed-right
    padding-right: 0
    padding-left: 0

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
</style>
