<template>
    <div class="container container-float-below">
      <div class="float-below">
          <div v-for="msg in messages"
               :key="msg.id"
               role="alert"
               class="alert alert-dismissable"
               :class="'alert-' + msg.type">
              <button type="button" class="close" data-dismiss="alert" aria-hidden="true">×</button>
              <span class="msg-part" v-html="msg.content"> </span>
          </div>
      </div>
    </div>
</template>
<script src="./FlashMessages.js"></script>