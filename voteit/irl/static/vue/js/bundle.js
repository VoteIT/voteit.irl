(function(t){function e(e){for(var n,r,l=e[0],i=e[1],c=e[2],u=0,d=[];u<l.length;u++)r=l[u],a[r]&&d.push(a[r][0]),a[r]=0;for(n in i)Object.prototype.hasOwnProperty.call(i,n)&&(t[n]=i[n]);p&&p(e);while(d.length)d.shift()();return s.push.apply(s,c||[]),o()}function o(){for(var t,e=0;e<s.length;e++){for(var o=s[e],n=!0,l=1;l<o.length;l++){var i=o[l];0!==a[i]&&(n=!1)}n&&(s.splice(e--,1),t=r(r.s=o[0]))}return t}var n={},a={app:0},s=[];function r(e){if(n[e])return n[e].exports;var o=n[e]={i:e,l:!1,exports:{}};return t[e].call(o.exports,o,o.exports,r),o.l=!0,o.exports}r.m=t,r.c=n,r.d=function(t,e,o){r.o(t,e)||Object.defineProperty(t,e,{enumerable:!0,get:o})},r.r=function(t){"undefined"!==typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(t,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(t,"__esModule",{value:!0})},r.t=function(t,e){if(1&e&&(t=r(t)),8&e)return t;if(4&e&&"object"===typeof t&&t&&t.__esModule)return t;var o=Object.create(null);if(r.r(o),Object.defineProperty(o,"default",{enumerable:!0,value:t}),2&e&&"string"!=typeof t)for(var n in t)r.d(o,n,function(e){return t[e]}.bind(null,n));return o},r.n=function(t){var e=t&&t.__esModule?function(){return t["default"]}:function(){return t};return r.d(e,"a",e),e},r.o=function(t,e){return Object.prototype.hasOwnProperty.call(t,e)},r.p="/";var l=window["webpackJsonp"]=window["webpackJsonp"]||[],i=l.push.bind(l);l.push=e,l=l.slice();for(var c=0;c<l.length;c++)e(l[c]);var p=i;s.push([0,"chunk-vendors"]),o()})({0:function(t,e,o){t.exports=o("56d7")},"01d4":function(t,e,o){"use strict";var n=o("18be"),a=o.n(n);a.a},"0cfb":function(t,e,o){},"18be":function(t,e,o){},4127:function(t,e,o){"use strict";var n=o("e073"),a=o.n(n);a.a},"56d7":function(t,e,o){"use strict";o.r(e);o("7f7f"),o("cadf"),o("551c"),o("f751"),o("097d");var n=o("2b0e"),a=function(){var t=this,e=t.$createElement,o=t._self._c||e;return o("div",{attrs:{id:"app"}},[t.ready?t._e():o("div",{staticClass:"loading"},[t._v("Loading...")]),t.ready?o("projector-nav"):t._e(),t.ready?o("div",{staticClass:"container-fluid"},[o("div",{staticClass:"row"},[o("div",{staticClass:"col-xs-10"},[o("proposals-main")],1),o("div",{staticClass:"col-xs-2 fixed-right"},[o("proposal-selection")],1)])]):t._e(),o("modal")],1)},s=[],r=o("cebc"),l=o("2f62"),i=function(){var t=this,e=t.$createElement,o=t._self._c||e;return o("nav",{staticClass:"navbar-fixed-top",attrs:{id:"fixed-top-nav",role:"navigation"}},[o("div",{staticClass:"container-fluid"},[o("a",{staticClass:"voteit-logo-nav",attrs:{href:t.currentAgendaItem?t.currentAgendaItem.href:t.href}}),o("a",{staticClass:"text-overflow voteit-nav-header",attrs:{href:t.currentAgendaItem?t.currentAgendaItem.href:t.href}},[t.currentAgendaItem?o("span",[t._v(t._s(t.currentAgendaItem.title))]):o("span",[o("span",{staticClass:"hidden-sm hidden-xs"},[t._v(t._s(t.title)+": ")]),t._v("\n                ("+t._s(t.$t("Click menu to select Agenda Item"))+")\n            ")])]),o("ul",{staticClass:"nav voteit-nav navbar-right",attrs:{id:"navbar-controls"}},[t.nextTagInOrder?o("li",[o("a",{attrs:{href:"#",title:"#"+t.nextTagInOrder},on:{click:function(e){return e.preventDefault(),t.filterByTag(t.nextTagInOrder)}}},[o("span",{staticClass:"glyphicon glyphicon-tags"})])]):t._e(),o("li",{staticClass:"dropdown"},[o("a",{staticClass:"dropdown-toggle",attrs:{href:"#",title:t.$t("Quickly create a poll"),"data-toggle":"dropdown","aria-expanded":"false"}},[o("span",{staticClass:"glyphicon glyphicon-star"}),o("span",{staticClass:"caret"})]),o("ul",{staticClass:"dropdown-menu",attrs:{id:"quick-polls"}},[t._l(t.pollList,function(e){return o("li",{key:e.name||e.title,class:{"dropdown-header":!e.name&&e.title,divider:!e.title,disabled:!t.pollAvailable(e)},attrs:{role:"presentation"}},[e.name?e.title?o("a",{attrs:{role:"menuitem",href:"#"+e.name},on:{click:function(o){return o.preventDefault(),t.quickPoll(e)}}},[t._v("\n                            "+t._s(e.title)+" "),e.rejectProp?o("span",[t._v("("+t._s(t.$t("add reject"))+")")]):t._e()]):t._e():o("span",[t._v(t._s(e.title))])])}),t.pollsOngoing.length?o("li",{staticClass:"divider",attrs:{role:"presentation"}}):t._e(),t.pollsOngoing.length?o("li",{staticClass:"dropdown-header",attrs:{role:"presentation"}},[o("span",[t._v(t._s(t.$t("Ongoing polls")))])]):t._e(),t._l(t.pollsOngoing,function(e){return o("li",{key:e.uid},[o("a",{attrs:{role:"menuitem",href:e.href},on:{click:function(o){return o.preventDefault(),t.openPoll(e)}}},[t._v("\n                            "+t._s(e.title)+"\n                            "),o("div",{staticClass:"progress"},[o("div",{staticClass:"progress-bar progress-bar-success",style:"width: "+100*e.votes/e.potentialVotes+"%",attrs:{role:"progress-bar"}},[t._v("\n                                    "+t._s(e.votes)+" / "+t._s(e.potentialVotes)+"\n                                ")])])])])}),t.pollsClosed.length?o("li",{staticClass:"divider",attrs:{role:"presentation"}}):t._e(),t.pollsClosed.length?o("li",{staticClass:"dropdown-header",attrs:{role:"presentation"}},[o("span",[t._v(t._s(t.$t("Closed polls")))])]):t._e(),t._l(t.pollsClosed,function(e){return o("li",{key:e.uid},[o("a",{attrs:{role:"menuitem",href:e.href},on:{click:function(o){return o.preventDefault(),t.openPoll(e)}}},[t._v("\n                            "+t._s(e.title)+"\n                        ")])])})],2)]),o("li",{staticClass:"dropdown"},[t._m(0),o("ul",{staticClass:"dropdown-menu",attrs:{id:"proposal-filters","aria-labelledby":"proposal-filtering"}},t._l(t.proposalWorkflowStates,function(e){return o("li",{key:e.name,staticClass:"text-nowrap",class:{active:e.checked},on:{click:function(t){t.stopPropagation()}}},[o("a",[o("input",{attrs:{type:"checkbox",id:e.name},domProps:{checked:e.checked},on:{change:function(o){return o.preventDefault(),t.toggleProposalWorkflow(e.name)}}}),o("label",{attrs:{for:e.name}},[t._v(t._s(e.title))]),o("span",{staticClass:"badge"},[t._v(t._s(t.proposals.filter(function(t){return t.workflowState===e.name}).length))])])])}),0)]),o("li",{class:{disabled:!t.previousAgendaItem}},[o("a",{attrs:{href:"#",title:t.previousAgendaItem?t.previousAgendaItem.title:t.$t("Previous")},on:{click:function(e){return e.preventDefault(),t.loadAgendaItem(t.previousAgendaItem)}}},[o("span",{staticClass:"glyphicon glyphicon-chevron-left"})])]),o("li",{class:{disabled:!t.nextAgendaItem}},[o("a",{attrs:{href:"#",title:t.nextAgendaItem?t.nextAgendaItem.title:t.$t("Next")},on:{click:function(e){return e.preventDefault(),t.loadAgendaItem(t.nextAgendaItem)}}},[o("span",{staticClass:"glyphicon glyphicon-chevron-right"})])]),o("li",{staticClass:"dropdown"},[t._m(1),o("ul",{staticClass:"dropdown-menu",attrs:{id:"projector-ai-menu"}},[o("li",{staticClass:"dropdown-header",attrs:{role:"presentation"}},[o("span",{staticClass:"glyphicon glyphicon-ongoing text-ongoing"}),t._v("\n                        "+t._s(t.$t("ongoing"))+"\n                    ")]),t._l(t.agendaStates.ongoing,function(e){return o("li",{key:e.uid,attrs:{role:"presentation"}},[o("a",{attrs:{role:"menuitem",href:"#"+e.name},on:{click:function(o){return o.preventDefault(),t.loadAgendaItem(e)}}},[t._v("\n                            "+t._s(e.title)+"\n                        ")])])}),o("li",{staticClass:"divider",attrs:{role:"presentation"}}),o("li",{staticClass:"dropdown-header",attrs:{role:"presentation"}},[o("span",{staticClass:"glyphicon glyphicon-upcoming text-upcoming"}),t._v("\n                        "+t._s(t.$t("upcoming"))+"\n                    ")]),t._l(t.agendaStates.upcoming,function(e){return o("li",{key:e.uid,attrs:{role:"presentation"}},[o("a",{attrs:{role:"menuitem",href:"#"+e.name},on:{click:function(o){return o.preventDefault(),t.loadAgendaItem(e)}}},[t._v("\n                            "+t._s(e.title)+"\n                        ")])])})],2)])])]),t._m(2),o("flash-messages")],1)},c=[function(){var t=this,e=t.$createElement,o=t._self._c||e;return o("a",{staticClass:"dropdown-toggle",attrs:{id:"proposal-filtering","data-toggle":"dropdown","aria-haspopup":"true","aria-expanded":"false"}},[o("span",{staticClass:"glyphicon glyphicon-filter"}),o("span",{staticClass:"caret"})])},function(){var t=this,e=t.$createElement,o=t._self._c||e;return o("a",{staticClass:"dropdown-toggle",attrs:{href:"#","data-toggle":"dropdown","aria-expanded":"false"}},[o("span",{staticClass:"glyphicon glyphicon-list"}),o("span",{staticClass:"caret"})])},function(){var t=this,e=t.$createElement,o=t._self._c||e;return o("div",{staticClass:"container container-float-below"},[o("div",{staticClass:"float-below",attrs:{"data-flash-slot":"voteit-main"}})])}],p=(o("ac6a"),function(){var t=this,e=t.$createElement,o=t._self._c||e;return o("div",{staticClass:"container container-float-below"},[o("div",{staticClass:"float-below"},t._l(t.messages,function(e){return o("div",{key:e.id,staticClass:"alert alert-dismissable",class:"alert-"+e.type,attrs:{role:"alert"}},[o("button",{staticClass:"close",attrs:{type:"button","data-dismiss":"alert","aria-hidden":"true"}},[t._v("×")]),o("span",{staticClass:"msg-part",domProps:{innerHTML:t._s(e.content)}})])}),0)])}),u=[],d=o("75fc"),f=o("7618"),g=o("d225"),m=o("b0b4"),h=function(){function t(){Object(g["a"])(this,t),this.requestActive=!1,this.requestQueue=[]}return Object(m["a"])(t,[{key:"next",value:function(){this.requestQueue.length&&!this.requestActive&&this.request(this.requestQueue.shift())}},{key:"request",value:function(t,e){var o=this;return e=e||{},"object"===Object(f["a"])(t)?e=t:e.url=t,this.requestActive?(e.deferred=$.Deferred(),e.polling||this.requestQueue.push(e),e.deferred):(this.requestActive=!0,$.ajax(e).done(function(t,o,n){e.deferred&&e.deferred.resolve(t,o,n)}).fail(function(t,o,n){!0===e.suppressError||e.polling||S(t),e.deferred&&e.deferred.reject(t,o,n)}).always(function(){o.requestActive=!1,o.next()}))}},{key:"get",value:function(t,e){return e=e||{},this.request(t,e)}},{key:"post",value:function(t,e,o){return o=o||{},o.method="POST",o.data=e,this.request(t,o)}}]),t}(),v=function(){function t(e){var o=this;Object(g["a"])(this,t),this.requests=e,this.services=[],this.intervalDefault=5e3,window.addEventListener("online",this._startAll.bind(this)),window.addEventListener("offline",this._stopAll.bind(this)),void 0!==document.hidden&&document.addEventListener("visibilitychange",function(){document.hidden?o._stopAll():o._startAll()})}return Object(m["a"])(t,[{key:"_startService",value:function(t){var e=this,o=function(){var o=e.requests.get(t.url,{polling:!0});t.callback&&o.done(t.callback)};o(),void 0===t.intervalId&&(t.intervalId=setInterval(o,t.intervalTime))}},{key:"_stopService",value:function(t){t.intervalId&&(clearInterval(t.intervalId),delete t.intervalId)}},{key:"_startAll",value:function(){var t=this;this.services.forEach(function(e){t._startService(e)})}},{key:"_stopAll",value:function(){var t=this;this.services.forEach(function(e){t._stopService(e)})}},{key:"addService",value:function(t,e,o){e=e||this.intervalDefault;var n={url:t,intervalTime:e,callback:o};this.services.push(n),this._startService(n)}},{key:"clearService",value:function(t){var e=this;this.services.filter(function(e){return e.url===t}).forEach(function(t){e._stopService(t)}),this.services=this.services.filter(function(e){return e.url!==t})}}]),t}(),b=new h,w=new v(b),_=new n["a"],k=function(t,e){e=e||{},e.content=t,_.$emit("flash::display",e)},y={open:function(t,e){"object"===Object(f["a"])(t)?e=t:(e=e||{},e.href=t),_.$emit("modal::open",e)},close:function(){_.$emit("modal::close")}},S=function(t){var e="";if("application/json"===t.getResponseHeader("content-type")&&"string"==typeof t.responseText){var o=$.parseJSON(t.responseText);o.title&&(e="<h4>"+o.title+"</h4>"),o.body&&o.body!=o.title?e+=o.body:o.message&&o.message!=o.title?e+=o.message:o.msg&&(e+=o.msg)}else e="<h4>"+t.status+" "+t.statusText+"</h4>"+t.responseText;k(e,{type:"danger"})},C={type:"success",timeout:3e3},j={data:function(){return{messages:[]}},created:function(){var t=this;_.$on("flash::display",function(e){e=$.extend({},C,e),e.id||(e.id=t.messages.length?Math.max.apply(Math,Object(d["a"])(t.messages.map(function(t){return"number"===typeof t.id?t.id:0})))+1:1),t.messages.push(e),e.timeout&&setTimeout(function(){t.messages.splice(t.messages.indexOf(e),1)},e.timeout)})}},O=j,P=o("2877"),A=Object(P["a"])(O,p,u,!1,null,null,null),x=A.exports,I=function(){var t=this,e=t.$createElement,o=t._self._c||e;return o("div",{staticClass:"modal fade",attrs:{id:"modal-area",tabindex:"-1",role:"dialog","aria-labelledby":"modal-title","aria-hidden":!0}},[o("div",{staticClass:"modal-dialog",class:t.modelDialogClass},[t.component?o(t.component,{tag:"component"}):o("div",{staticClass:"modal-content",domProps:{innerHTML:t._s(t.content)}})],1)])},W=[],q={backdrop:!0,modelDialogClass:null},T={data:function(){return{modelDialogClass:null,content:null,backdrop:!0,component:null}},methods:{open:function(t){$(this.$el).modal(t)},close:function(){$(this.$el).modal("hide")}},created:function(){var t=this;_.$on("modal::open",function(e){t.component=null,e=$.extend({},q,e),t.content=e.content,t.backdrop=e.backdrop,t.modelDialogClass=e.modelDialogClass,e.href?b.get(e.href).done(function(o){t.content=o,t.open(e.params)}):e.component?(t.component=e.component,t.open(e.params)):t.open(e.params)}),_.$on("modal::close",function(){t.close()})},mounted:function(){var t=this;$(this.$el).modal({show:!1}).on("hidden.bs.modal",function(){t.component=null,t.content=null})}},E=T,D=Object(P["a"])(E,I,W,!1,null,null,null),M=D.exports,U=function(){var t=this,e=t.$createElement,o=t._self._c||e;return o("a",{attrs:{role:t.role,href:t.href},domProps:{innerHTML:t._s(t.content)},on:{click:function(e){return e.preventDefault(),t.openModal(e)}}})},L=[],B={props:{href:String,modelDialogClass:String,content:String,role:String},methods:{openModal:function(){y.open(this.href,{modelDialogClass:this.modelDialogClass})}}},N=B,H=Object(P["a"])(N,U,L,!1,null,null,null),R=H.exports,G=function(){var t=this,e=t.$createElement,o=t._self._c||e;return t.result?o("div",[o("div",{staticClass:"modal-content",domProps:{innerHTML:t._s(t.result)}})]):o("div",{staticClass:"modal-content",attrs:{id:"poll-modal"}},[o("div",{staticClass:"modal-header"},[o("button",{staticClass:"close",attrs:{type:"button","data-dismiss":"modal","aria-label":t.$t("Close")}},[o("span",{attrs:{"aria-hidden":"true"}},[t._v("×")])]),o("h4",{staticClass:"modal-title"},[t._v(t._s(t.poll.title)+" "),o("small",[t._v("("+t._s(t.$t(t.poll.workflowState))+")")])])]),o("div",{staticClass:"modal-body"},[o("div",{staticClass:"progress"},[o("div",{staticClass:"progress-bar progress-bar-success progress-bar-striped active",style:"width: "+100*t.poll.votes/t.poll.potentialVotes+"%",attrs:{role:"progress-bar","aria-valuemin":"0","aria-valuenow":t.poll.votes,"aria-valuemax":t.poll.potentialVotes}},[t._v("\n                "+t._s(t.poll.votes)+" / "+t._s(t.poll.potentialVotes)+" "),o("span",{staticClass:"sr-only"},[t._v(t._s(t.$t("votes")))])])]),o("div",{staticClass:"btn-group"},[o("button",{staticClass:"btn btn-xs btn-default dropdown-toggle",attrs:{type:"button","data-toggle":"dropdown","aria-expanded":"false"}},[o("span",{class:"text-"+t.poll.workflowState},[o("span",{class:"glyphicon glyphicon-"+t.poll.workflowState}),o("span",[t._v(t._s(t.$t(t.$t(t.poll.workflowState))))]),o("span",{staticClass:"caret"})])]),o("ul",{staticClass:"dropdown-menu",attrs:{role:"menu"}},t._l(["canceled","closed"],function(e){return o("li",{key:e},[o("a",{attrs:{href:"#"+e},on:{click:function(o){return o.preventDefault(),t.setPollWorkflowState({poll:t.poll,workflowState:e})}}},[o("span",{class:"glyphicon glyphicon-"+e+" text-"+e}),o("span",[t._v(t._s(t.$t(e)))])])])}),0)])])])},Q=[],V={data:function(){return{result:null}},created:function(){"closed"===this.poll.workflowState&&this.getResult(this.poll.href)},methods:Object(r["a"])({},Object(l["b"])("projector",["setPollWorkflowState"]),{getResult:function(t){var e=this;b.get(t).done(function(t){e.result=t})}}),computed:Object(r["a"])({},Object(l["c"])("projector",["openPoll"]),{poll:function(){return this.openPoll},pollState:function(){return this.openPoll&&this.openPoll.workflowState}}),watch:{pollState:function(t){"closed"===t&&this.getResult(this.openPoll.href),"canceled"===t&&y.close()}}},F=V,J=(o("4127"),Object(P["a"])(F,G,Q,!1,null,null,null)),z=J.exports,K=function(){var t=this,e=t.$createElement,o=t._self._c||e;return o("li",{staticClass:"list-group-item proposal"},[t.actions.left?o("button",{staticClass:"btn btn-xs btn-default move-left",on:{click:function(e){return t.actions.left(t.item)}}},[o("span",{staticClass:"glyphicon glyphicon-chevron-left"})]):t._e(),o("div",{staticClass:"main-controls pull-right"},[o("div",{staticClass:"btn-group"},t._l(t.workflowStates,function(e){return o("button",{key:e.name,staticClass:"btn btn-default btn-sm",class:{active:e.name===t.item.workflowState&&t.actions.setWorkflowState},on:{click:function(o){return t.setWorkflowState(t.item,e)}}},[o("span",{class:["text-"+e.name,"glyphicon","glyphicon-"+e.name]})])}),0),o("button",{staticClass:"btn btn-sm btn-default move-right",on:{click:function(e){return t.actions.right(t.item)}}},[o("span",{staticClass:"glyphicon glyphicon-chevron-right"})])]),o("h3",{staticClass:"prop-meta-heading"},[o("strong",{staticClass:"proposal-aid"},[o("a",{attrs:{href:"#","data-tag-filter":t.item.aid}},[t._v("#"+t._s(t.item.aid))])]),t._v("\n        "+t._s(t.$t("by"))+"\n        "),o("span",{staticClass:"proposal-author"},[t._v(t._s(t.item.creator))])]),o("div",{staticClass:"proposal-text",domProps:{innerHTML:t._s(t.item.text)}})])},X=[],Y={props:{actions:Object,item:Object,quickSelect:Boolean},methods:{setWorkflowState:function(t,e){this.actions.setWorkflowState&&this.actions.setWorkflowState({proposal:t,workflowState:e})}},computed:Object(r["a"])({},Object(l["e"])("projector",["proposalWorkflowStates"]),{workflowStates:function(){var t=this;return this.proposalWorkflowStates.filter(function(e){return t.quickSelect&&e.quickSelect||e.name===t.item.workflowState})}})},Z=Y,tt=Object(P["a"])(Z,K,X,!1,null,null,null),et=tt.exports,ot={components:{ModalLink:R,FlashMessages:x,Proposal:et},methods:Object(r["a"])({},Object(l["d"])("projector",["toggleProposalWorkflow","updateProposals","selectProposals","setOpenPollUid","updatePoll","filterByTag"]),Object(l["b"])("projector",["updateAgendaItems"]),{pollAvailable:function(t){var e=this.proposalSelection.length+(t.rejectProp?1:0);return!(t.proposalsMin&&e<t.proposalsMin)&&!(t.proposalsMax&&e>t.proposalsMax)},quickPoll:function(t){var e=this;this.pollAvailable(t)&&b.post(this.api.quickPoll,{"quick-poll-method":t.name,uid:this.proposalSelection,"reject-prop":t.rejectProp}).done(function(t){e.updateProposals(t.proposals),e.selectProposals(t.proposals),e.updatePoll(t.poll),e.openPoll(t.poll)})},loadAgendaItem:function(t){t&&(this.$store.dispatch("projector/loadAgendaItem",t),history.pushState(t,t.title,"#"+t.name))},openPoll:function(t){this.setOpenPollUid(t.uid),y.open({component:z,modelDialogClass:"modal-lg"})}}),computed:Object(r["a"])({},Object(l["e"])("meeting",["href","title","agenda","hrefLastPollResult"]),Object(l["c"])("meeting",["agendaStates","previousAgendaItem","nextAgendaItem","currentAgendaItem"]),Object(l["e"])("projector",["proposalWorkflowStates","pollGroups","proposalSelection","proposals","api","logo"]),Object(l["c"])("projector",["pollsOngoing","pollsClosed","selectedProposals","nextTagInOrder"]),{pollList:function(){var t=[];return this.pollGroups.forEach(function(e,o){o>0&&t.push({id:"divider-"+o}),t.push(e),t=t.concat(e.methods)}),t}})},nt=ot,at=(o("01d4"),Object(P["a"])(nt,i,c,!1,null,null,null)),st=at.exports,rt=function(){var t=this,e=t.$createElement,o=t._self._c||e;return o("ul",{staticClass:"list-group",attrs:{id:"projector-pool"}},t._l(t.filteredProposals,function(e){return o("proposal",{key:e.uid,attrs:{actions:t.proposalActions,item:e}})}),1)},lt=[],it={data:function(){return{proposalActions:{left:this.selectProposal,right:this.downShift}}},components:{Proposal:et},methods:Object(r["a"])({},Object(l["d"])("projector",["selectProposal","downShift"])),computed:Object(r["a"])({},Object(l["e"])("projector",["proposalWorkflowStates"]),Object(l["c"])("projector",["filteredProposals"]))},ct=it,pt=Object(P["a"])(ct,rt,lt,!1,null,null,null),ut=pt.exports,dt=function(){var t=this,e=t.$createElement,o=t._self._c||e;return t.selectedProposals.length?o("ul",{staticClass:"list-group",attrs:{id:"projector-main"}},t._l(t.selectedProposals,function(e){return o("proposal",{key:e.uid,attrs:{actions:t.proposalActions,item:e,"quick-select":""}})}),1):t._e()},ft=[],gt={data:function(){return{proposalActions:{right:this.deselectProposal,setWorkflowState:this.setProposalWorkflowState}}},components:{Proposal:et},methods:Object(r["a"])({},Object(l["d"])("projector",["deselectProposal"]),Object(l["b"])("projector",["setProposalWorkflowState"])),computed:Object(r["a"])({},Object(l["c"])("projector",["selectedProposals"]))},mt=gt,ht=Object(P["a"])(mt,dt,ft,!1,null,null,null),vt=ht.exports,bt={name:"app",data:function(){return{ready:!1}},components:{ProjectorNav:st,ProposalSelection:ut,ProposalsMain:vt,Modal:M,FlashMessages:x},created:function(){var t=this;b.get($("body").data("src")).done(function(e){t.$store.commit("meeting/load",e.meeting),t.$store.commit("projector/load",e),t.$root.ts=e.ts,t.ready=!0;var o="#"===location.hash[0]?location.hash.slice(1):location.hash;o&&t.loadAgendaItemByName(o)}),window.onpopstate=function(e){t.loadAgendaItemByName(e.state&&e.state.name)},$("body").on("click","[data-tag-filter]",function(e){e.preventDefault();var o=$(e.currentTarget).data("tagFilter").toLowerCase();t.filterByTag(o)})},methods:Object(r["a"])({},Object(l["b"])("projector",["loadAgendaItemByName"]),Object(l["d"])("projector",["filterByTag"]))},wt=bt,_t=(o("cf25"),Object(P["a"])(wt,a,s,!1,null,null,null)),kt=_t.exports,yt=(o("456d"),o("7514"),["ongoing","upcoming","closed","private"]),St=function(t,e){var o=t.agenda.find(function(e){return e.uid===t.currentAgendaItemUid}),n=t.agenda.indexOf(o)+e;if(-1<n&&n<t.agenda.length)return t.agenda[n]},Ct={namespaced:!0,state:{title:"",href:"",agenda:[],currentAgendaItemUid:void 0,loaded:!1},getters:{agendaStates:function(t){var e={};return yt.forEach(function(o){e[o]=t.agenda.filter(function(t){return t.workflowState===o})}),e},previousAgendaItem:function(t){return St(t,-1)},currentAgendaItem:function(t){return t.agenda.find(function(e){return e.uid===t.currentAgendaItemUid})},nextAgendaItem:function(t){return St(t,1)}},mutations:{load:function(t,e){Object.keys(e).forEach(function(o){t[o]=e[o]}),t.loaded=!0},setAgenda:function(t,e){t.agenda=e},setAgendaItem:function(t,e){t.currentAgendaItemUid=e}}},jt=(o("6762"),o("2fdb"),{namespaced:!0,state:{proposalWorkflowStates:[],pollGroups:[],proposals:[],proposalSelection:[],proposalOrder:[],tagOrder:[],polls:[],agendaUrl:null,requestActive:!1,api:{},logo:"",openPollUid:null},getters:{filteredProposals:function(t){var e={};return t.proposalWorkflowStates.forEach(function(t){t.checked&&(e[t.name]=!0)}),t.proposalOrder.map(function(e){return t.proposals.find(function(t){return t.uid===e})}).filter(function(o){return o.workflowState in e&&!t.proposalSelection.includes(o.uid)})},selectedProposals:function(t){return t.proposalSelection.map(function(e){return t.proposals.find(function(t){return t.uid===e})})},pollsOngoing:function(t){return t.polls.filter(function(t){return"ongoing"===t.workflowState})},pollsClosed:function(t){return t.polls.filter(function(t){return"closed"===t.workflowState})},openPoll:function(t){return t.polls.find(function(e){return e.uid===t.openPollUid})},nextTagInOrder:function(t){for(var e=function(){var e=t.tagOrder[o];if(t.proposals.find(function(t){return"published"===t.workflowState&&t.tags.includes(e)}))return{v:e}},o=0;o<t.tagOrder.length;o++){var n=e();if("object"===Object(f["a"])(n))return n.v}}},mutations:{load:function(t,e){t.proposalWorkflowStates=e.proposalWorkflowStates,t.pollGroups=e.pollGroups,t.api=e.api,t.logo=e.logo},setAgendaUrl:function(t,e){t.agendaUrl=e,t.proposals=[],t.proposalSelection=[],t.proposalOrder=[],t.polls=[]},loadAgendaItem:function(t,e){e=e||{proposals:[],pollsOngoing:[],pollsClosed:[]},t.proposals=e.proposals,t.polls=e.polls,t.tagOrder=e.tagOrder||[];var o=function(e){return void 0!==t.proposals.find(function(t){return t.uid===e})};t.proposalOrder=t.proposalOrder.filter(o),t.proposalSelection=t.proposalSelection.filter(o),e.proposals.forEach(function(e){t.proposalOrder.includes(e.uid)||t.proposalOrder.push(e.uid)})},toggleProposalWorkflow:function(t,e){var o=t.proposalWorkflowStates.find(function(t){return t.name===e});o.checked=!o.checked},setProposalWorkflowState:function(t,e){var o=e.proposal,n=e.workflowState;o.workflowState=n.name},downShift:function(t,e){t.proposalOrder.splice(t.proposalOrder.indexOf(e.uid),1),t.proposalOrder.push(e.uid)},selectProposal:function(t,e){t.proposalSelection.push(e.uid)},selectProposals:function(t,e){t.proposalSelection=e.map(function(t){return t.uid})},deselectProposal:function(t,e){t.proposalSelection.splice(t.proposalSelection.indexOf(e.uid),1)},updateProposals:function(t,e){e.forEach(function(e){var o=t.proposals.find(function(t){return t.uid===e.uid});void 0!==o?Object.assign(o,e):t.proposals.push(e)})},setRequestActive:function(t,e){t.requestActive=e},filterByTag:function(t,e){var o={};t.proposalWorkflowStates.forEach(function(t){t.checked&&(o[t.name]=!0)}),t.proposalSelection=t.proposals.filter(function(t){return-1!==t.tags.indexOf(e)&&t.workflowState in o}).map(function(t){return t.uid})},setOpenPollUid:function(t,e){t.openPollUid=e},updatePoll:function(t,e){var o=t.polls.find(function(t){return t.uid===e.uid});o?Object.assign(o,e):t.polls.push(e)}},actions:{loadAgendaItem:function(t,e){var o=t.state,n=t.commit;o.agendaUrl&&w.clearService(o.agendaUrl),e=e||{jsonUrl:null,uid:null},n("meeting/setAgendaItem",e.uid,{root:!0}),n("setAgendaUrl",e.jsonUrl),e.jsonUrl&&w.addService(e.jsonUrl,1e3*o.api.pollIntervalTime,function(t){n("meeting/setAgenda",t.agenda,{root:!0}),t.agenda.find(function(t){return t.uid===e.uid})?n("loadAgendaItem",t):(n("loadAgendaItem"),w.clearService(e.jsonUrl))})},loadAgendaItemByName:function(t,e){var o=t.rootState,n=t.dispatch,a=o.meeting.agenda.find(function(t){return t.name===e});n("loadAgendaItem",a)},setProposalWorkflowState:function(t,e){var o=t.state,n=t.commit,a=e.proposal,s=e.workflowState,r=o.proposalWorkflowStates.find(function(t){return t.name===a.workflowState});s.quickSelect&&r!==s&&b.post(a.workflowApi,{state:s.name}).done(function(t){var e=o.proposalWorkflowStates.find(function(e){return e.name===t.state});n("setProposalWorkflowState",{proposal:a,workflowState:e})})},setPollWorkflowState:function(t,e){var o=t.commit,n=e.poll,a=e.workflowState;b.post(n.api,{state:a}).done(function(t){o("updatePoll",t)})}}});n["a"].use(l["a"]);var Ot=!1,Pt=new l["a"].Store({modules:{meeting:Ct,projector:jt},strict:Ot});n["a"].config.productionTip=!1;var At={install:function(t){t.prototype.$t=function(t){return this.$root.ts[t]||t}}};n["a"].use(At),$(function(){new n["a"]({store:Pt,render:function(t){return t(kt)},data:{ts:{}}}).$mount("#app")})},cf25:function(t,e,o){"use strict";var n=o("0cfb"),a=o.n(n);a.a},e073:function(t,e,o){}});
//# sourceMappingURL=bundle.js.map