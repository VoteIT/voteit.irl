(function(t){function e(e){for(var a,r,l=e[0],i=e[1],c=e[2],d=0,u=[];d<l.length;d++)r=l[d],n[r]&&u.push(n[r][0]),n[r]=0;for(a in i)Object.prototype.hasOwnProperty.call(i,a)&&(t[a]=i[a]);p&&p(e);while(u.length)u.shift()();return s.push.apply(s,c||[]),o()}function o(){for(var t,e=0;e<s.length;e++){for(var o=s[e],a=!0,l=1;l<o.length;l++){var i=o[l];0!==n[i]&&(a=!1)}a&&(s.splice(e--,1),t=r(r.s=o[0]))}return t}var a={},n={app:0},s=[];function r(e){if(a[e])return a[e].exports;var o=a[e]={i:e,l:!1,exports:{}};return t[e].call(o.exports,o,o.exports,r),o.l=!0,o.exports}r.m=t,r.c=a,r.d=function(t,e,o){r.o(t,e)||Object.defineProperty(t,e,{enumerable:!0,get:o})},r.r=function(t){"undefined"!==typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(t,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(t,"__esModule",{value:!0})},r.t=function(t,e){if(1&e&&(t=r(t)),8&e)return t;if(4&e&&"object"===typeof t&&t&&t.__esModule)return t;var o=Object.create(null);if(r.r(o),Object.defineProperty(o,"default",{enumerable:!0,value:t}),2&e&&"string"!=typeof t)for(var a in t)r.d(o,a,function(e){return t[e]}.bind(null,a));return o},r.n=function(t){var e=t&&t.__esModule?function(){return t["default"]}:function(){return t};return r.d(e,"a",e),e},r.o=function(t,e){return Object.prototype.hasOwnProperty.call(t,e)},r.p="/";var l=window["webpackJsonp"]=window["webpackJsonp"]||[],i=l.push.bind(l);l.push=e,l=l.slice();for(var c=0;c<l.length;c++)e(l[c]);var p=i;s.push([0,"chunk-vendors"]),o()})({0:function(t,e,o){t.exports=o("56d7")},"01d4":function(t,e,o){"use strict";var a=o("18be"),n=o.n(a);n.a},"0cfb":function(t,e,o){},"18be":function(t,e,o){},"56d7":function(t,e,o){"use strict";o.r(e);o("7f7f"),o("cadf"),o("551c"),o("f751"),o("097d");var a=o("2b0e"),n=function(){var t=this,e=t.$createElement,o=t._self._c||e;return o("div",{attrs:{id:"app"}},[t.ready?t._e():o("div",{staticClass:"loading"},[t._v("Loading...")]),t.ready?o("projector-nav"):t._e(),t.ready?o("div",{staticClass:"container-fluid"},[o("div",{staticClass:"row"},[o("div",{staticClass:"col-xs-10"},[o("proposals-main")],1),o("div",{staticClass:"col-xs-2 fixed-right"},[o("proposal-selection")],1)])]):t._e(),o("modal")],1)},s=[],r=o("cebc"),l=o("2f62"),i=function(){var t=this,e=t.$createElement,o=t._self._c||e;return o("nav",{staticClass:"navbar navbar-static-top navbar-voteit",attrs:{role:"navigation"}},[o("div",{staticClass:"container-fluid",attrs:{"data-check-greedy":""}},[o("a",{staticClass:"navbar-brand hidden-xs",attrs:{href:"/"}},[o("img",{staticClass:"voteitlogo",attrs:{height:"31",width:"85",src:t.logo}})]),o("a",{staticClass:"navbar-brand greedy",attrs:{id:"navbar-heading",href:t.currentAgendaItem?t.currentAgendaItem.href:t.href}},[t.currentAgendaItem?o("span",[t._v(t._s(t.currentAgendaItem.title))]):o("span",[o("span",{staticClass:"hidden-sm hidden-xs"},[t._v(t._s(t.title)+": ")]),t._v("\n                ("+t._s(t.$t("Click menu to select Agenda Item"))+")\n            ")])]),o("ul",{staticClass:"nav navbar-nav navbar-right"},[o("li",{class:{disabled:!t.previousAgendaItem}},[o("a",{attrs:{href:"#",title:t.$t("Previous")},on:{click:function(e){return e.preventDefault(),t.loadAgendaItem(t.previousAgendaItem)}}},[o("span",{staticClass:"glyphicon glyphicon-chevron-left"})])]),o("li",{class:{disabled:!t.nextAgendaItem}},[o("a",{attrs:{href:"#",title:t.$t("Next")},on:{click:function(e){return e.preventDefault(),t.loadAgendaItem(t.nextAgendaItem)}}},[o("span",{staticClass:"glyphicon glyphicon-chevron-right"})])]),o("li",{staticClass:"dropdown"},[t._m(0),o("ul",{staticClass:"dropdown-menu",attrs:{id:"quick-polls"}},[t._l(t.pollList,function(e){return o("li",{key:e.name||e.title,class:{"dropdown-header":!e.name&&e.title,divider:!e.title,disabled:!t.pollAvailable(e)},attrs:{role:"presentation"}},[e.name?e.title?o("a",{attrs:{role:"menuitem",href:"#"+e.name},on:{click:function(o){return o.preventDefault(),t.quickPoll(e)}}},[t._v("\n                            "+t._s(e.title)+" "),e.rejectProp?o("span",[t._v("("+t._s(t.$t("add reject"))+")")]):t._e()]):t._e():o("span",[t._v(t._s(e.title))])])}),t.pollsOngoing.length?o("li",{staticClass:"divider",attrs:{role:"presentation"}}):t._e(),t.pollsOngoing.length?o("li",{staticClass:"dropdown-header",attrs:{role:"presentation"}},[o("span",[t._v(t._s(t.$t("Ongoing polls")))])]):t._e(),t._l(t.pollsOngoing,function(e){return o("li",{key:e.uid},[o("a",{attrs:{role:"menuitem","data-open-modal":"","data-modal-dialog-class":"modal-lg",href:e.href}},[t._v("\n                            "+t._s(e.title)+"\n                            "),o("div",{staticClass:"progress"},[o("div",{staticClass:"progress-bar progress-bar-success",style:"width: "+100*e.votes/e.potentialVotes+"%",attrs:{role:"progress-bar"}},[t._v("\n                                    "+t._s(e.votes)+" / "+t._s(e.potentialVotes)+"\n                                ")])])])])}),t.pollsClosed.length?o("li",{staticClass:"divider",attrs:{role:"presentation"}}):t._e(),t.pollsClosed.length?o("li",{staticClass:"dropdown-header",attrs:{role:"presentation"}},[o("span",[t._v(t._s(t.$t("Closed polls")))])]):t._e(),t._l(t.pollsClosed,function(t){return o("li",{key:t.uid},[o("modal-link",{attrs:{role:"menuitem",href:t.href,"model-dialog-class":"modal-lg",content:t.title}})],1)})],2)]),o("li",{staticClass:"dropdown"},[t._m(1),o("ul",{staticClass:"dropdown-menu",attrs:{id:"proposal-filters","aria-labelledby":"proposal-filtering"}},t._l(t.proposalWorkflowStates,function(e){return o("li",{key:e.name,staticClass:"text-nowrap",class:{active:e.checked},on:{click:function(t){t.stopPropagation()}}},[o("input",{attrs:{type:"checkbox",id:e.name},domProps:{checked:e.checked},on:{change:function(o){return o.preventDefault(),t.toggleProposalWorkflow(e.name)}}}),o("label",{attrs:{for:e.name}},[t._v(t._s(e.title))]),o("span",{staticClass:"badge"},[t._v(t._s(t.proposals.filter(function(t){return t.workflowState===e.name}).length))])])}),0)]),o("li",{staticClass:"dropdown"},[t._m(2),o("ul",{staticClass:"dropdown-menu",attrs:{id:"projector-ai-menu"}},[o("li",{staticClass:"dropdown-header",attrs:{role:"presentation"}},[o("span",{staticClass:"glyphicon glyphicon-ongoing text-ongoing"}),t._v("\n                        "+t._s(t.$t("ongoing"))+"\n                    ")]),t._l(t.agendaStates.ongoing,function(e){return o("li",{key:e.uid,attrs:{role:"presentation"}},[o("a",{attrs:{role:"menuitem",href:"#"+e.name},on:{click:function(o){return o.preventDefault(),t.loadAgendaItem(e)}}},[t._v("\n                            "+t._s(e.title)+"\n                        ")])])}),o("li",{staticClass:"divider",attrs:{role:"presentation"}}),o("li",{staticClass:"dropdown-header",attrs:{role:"presentation"}},[o("span",{staticClass:"glyphicon glyphicon-upcoming text-upcoming"}),t._v("\n                        "+t._s(t.$t("upcoming"))+"\n                    ")]),t._l(t.agendaStates.upcoming,function(e){return o("li",{key:e.uid,attrs:{role:"presentation"}},[o("a",{attrs:{role:"menuitem",href:"#"+e.name},on:{click:function(o){return o.preventDefault(),t.loadAgendaItem(e)}}},[t._v("\n                            "+t._s(e.title)+"\n                        ")])])})],2)])])]),t._m(3),o("flash-messages")],1)},c=[function(){var t=this,e=t.$createElement,o=t._self._c||e;return o("a",{staticClass:"dropdown-toggle",attrs:{href:"#",title:"Quickly create a poll","i18n:attributes":"title quick_poll_btn_title;","data-toggle":"dropdown","aria-expanded":"false"}},[o("span",{staticClass:"glyphicon glyphicon-star"}),o("span",{staticClass:"caret"})])},function(){var t=this,e=t.$createElement,o=t._self._c||e;return o("a",{staticClass:"dropdown-toggle",attrs:{id:"proposal-filtering","data-toggle":"dropdown","aria-haspopup":"true","aria-expanded":"false"}},[o("span",{staticClass:"glyphicon glyphicon-filter"}),o("span",{staticClass:"caret"})])},function(){var t=this,e=t.$createElement,o=t._self._c||e;return o("a",{staticClass:"dropdown-toggle",attrs:{href:"#","data-toggle":"dropdown","aria-expanded":"false"}},[o("span",{staticClass:"glyphicon glyphicon-list"}),o("span",{staticClass:"caret"})])},function(){var t=this,e=t.$createElement,o=t._self._c||e;return o("div",{staticClass:"container container-float-below"},[o("div",{staticClass:"float-below",attrs:{"data-flash-slot":"voteit-main"}})])}],p=(o("ac6a"),function(){var t=this,e=t.$createElement,o=t._self._c||e;return o("div",{staticClass:"container container-float-below"},[o("div",{staticClass:"float-below"},t._l(t.messages,function(e){return o("div",{key:e.id,staticClass:"alert alert-dismissable",class:"alert-"+e.type,attrs:{role:"alert"}},[o("button",{staticClass:"close",attrs:{type:"button","data-dismiss":"alert","aria-hidden":"true"}},[t._v("×")]),o("span",{staticClass:"msg-part",domProps:{innerHTML:t._s(e.content)}})])}),0)])}),d=[],u=o("75fc"),f=o("7618"),g=!1,m=[],h=!1,v=function t(e,o){if(o=o||{},"object"===Object(f["a"])(e)?o=e:o.url=e,navigator.onLine&&!g)return g=!0,$.ajax(o).always(function(){g=!1,m.length&&t(m.shift())}).fail(function(t){!0===o.suppressError||o.polling||_(t)});navigator.onLine||h||(window.addEventListener("online",function(){m.length&&t(m.shift())}),h=!0),o.polling||m.push(o)},b=new a["a"],w=function(t,e){e=e||{},e.content=t,b.$emit("flash::display",e)},_=function(t){var e="";if("application/json"===t.getResponseHeader("content-type")&&"string"==typeof t.responseText){var o=$.parseJSON(t.responseText);o.title&&(e="<h4>"+o.title+"</h4>"),o.body&&o.body!=o.title?e+=o.body:o.message&&o.message!=o.title?e+=o.message:o.msg&&(e+=o.msg)}else e="<h4>"+t.status+" "+t.statusText+"</h4>"+t.responseText;w(e,{type:"danger"})},k={type:"success",timeout:3e3},y={data:function(){return{messages:[]}},created:function(){var t=this;b.$on("flash::display",function(e){e=$.extend({},k,e),e.id||(e.id=t.messages.length?Math.max.apply(Math,Object(u["a"])(t.messages.map(function(t){return"number"===typeof t.id?t.id:0})))+1:1),t.messages.push(e),e.timeout&&setTimeout(function(){t.messages.splice(t.messages.indexOf(e),1)},e.timeout)})}},C=y,S=o("2877"),j=Object(S["a"])(C,p,d,!1,null,null,null),O=j.exports,x=function(){var t=this,e=t.$createElement,o=t._self._c||e;return o("div",{staticClass:"modal fade",attrs:{id:"modal-area",tabindex:"-1",role:"dialog","aria-labelledby":"modal-title","aria-hidden":!0}},[o("div",{staticClass:"modal-dialog",class:t.modelDialogClass},[o("div",{staticClass:"modal-content",domProps:{innerHTML:t._s(t.content)}})])])},A=[],P={backdrop:!0,modelDialogClass:null},I={data:function(){return{modelDialogClass:null,content:null,backdrop:!0,component:null}},methods:{open:function(t){$(this.$el).modal(t)},close:function(){$(this.$el).modal({show:!1})}},created:function(){var t=this;this.$root.$on("modal::open",function(e){e=$.extend({},P,e),t.content=e.content,t.backdrop=e.backdrop,t.modelDialogClass=e.modelDialogClass,e.href?$.get(e.href).done(function(o){t.content=o,t.open(e.params)}).fail(function(e){t.$root.$emit("flash::display",{content:e,type:"danger"})}):t.open(e.params)}),this.$root.$on("modal::close",function(){t.close()})}},W=I,M=Object(S["a"])(W,x,A,!1,null,null,null),E=M.exports,T=function(){var t=this,e=t.$createElement,o=t._self._c||e;return o("a",{attrs:{role:t.role,href:t.href},domProps:{innerHTML:t._s(t.content)},on:{click:function(e){return e.preventDefault(),t.openModal(e)}}})},D=[],q={props:{href:String,modelDialogClass:String,content:String,role:String},methods:{openModal:function(){this.$root.$emit("modal::open",{modelDialogClass:this.modelDialogClass,href:this.href})}}},L=q,B=Object(S["a"])(L,T,D,!1,null,null,null),U=B.exports,N=5e3,G={components:{ModalLink:U,FlashMessages:O},methods:Object(r["a"])({},Object(l["d"])("projector",["toggleProposalWorkflow"]),Object(l["b"])("projector",["updateAgendaItems"]),{pollAvailable:function(t){var e=this.proposalSelection.length+(t.rejectProp?1:0);return!(t.proposalsMin&&e<t.proposalsMin)&&!(t.proposalsMax&&e>t.proposalsMax)},quickPoll:function(t){this.pollAvailable(t)&&v(this.api.quickPoll,{method:"POST",data:{"quick-poll-method":t.name,uid:this.proposalSelection,"reject-prop":t.rejectProp}}).done(function(t){w(t.msg,{timeout:null})})},loadAgendaItem:function(t){t&&(this.$store.dispatch("projector/loadAgendaItem",t),history.pushState(t,t.title,"#"+t.name))}}),computed:Object(r["a"])({},Object(l["e"])("meeting",["href","title","agenda","currentAgendaItem","hrefLastPollResult"]),Object(l["c"])("meeting",["agendaStates","previousAgendaItem","nextAgendaItem"]),Object(l["e"])("projector",["proposalWorkflowStates","pollGroups","proposalSelection","proposals","api","logo","pollsOngoing","pollsClosed"]),{pollList:function(){var t=[];return this.pollGroups.forEach(function(e,o){o>0&&t.push({id:"divider-"+o}),t.push(e),t=t.concat(e.methods)}),t}}),created:function(){var t=this;setInterval(function(){return t.updateAgendaItems(!0)},N)}},H=G,F=(o("01d4"),Object(S["a"])(H,i,c,!1,null,null,null)),J=F.exports,R=function(){var t=this,e=t.$createElement,o=t._self._c||e;return o("ul",{staticClass:"list-group",attrs:{id:"projector-pool"}},t._l(t.filteredProposals,function(e){return o("proposal",{key:e.uid,attrs:{actions:t.proposalActions,item:e}})}),1)},V=[],Q=function(){var t=this,e=t.$createElement,o=t._self._c||e;return o("li",{staticClass:"list-group-item proposal"},[t.actions.left?o("button",{staticClass:"btn btn-xs btn-default move-left",on:{click:function(e){return t.actions.left(t.item)}}},[o("span",{staticClass:"glyphicon glyphicon-chevron-left"})]):t._e(),o("div",{staticClass:"main-controls pull-right"},[o("div",{staticClass:"btn-group"},t._l(t.workflowStates,function(e){return o("button",{key:e.name,staticClass:"btn btn-default btn-sm",class:{active:e.name===t.item.workflowState&&t.actions.setWorkflowState},on:{click:function(o){return t.setWorkflowState(t.item,e)}}},[o("span",{class:["text-"+e.name,"glyphicon","glyphicon-"+e.name]})])}),0),o("button",{staticClass:"btn btn-sm btn-default move-right",on:{click:function(e){return t.actions.right(t.item)}}},[o("span",{staticClass:"glyphicon glyphicon-chevron-right"})])]),o("h3",{staticClass:"prop-meta-heading"},[o("strong",{staticClass:"proposal-aid"},[o("a",{attrs:{href:"#","data-tag-filter":t.item.aid}},[t._v("#"+t._s(t.item.aid))])]),t._v("\n        "+t._s(t.$t("by"))+"\n        "),o("span",{staticClass:"proposal-author"},[t._v(t._s(t.item.creator))])]),o("div",{staticClass:"proposal-text",domProps:{innerHTML:t._s(t.item.text)}})])},z=[],K={props:{actions:Object,item:Object,quickSelect:Boolean},methods:{setWorkflowState:function(t,e){this.actions.setWorkflowState&&this.actions.setWorkflowState({proposal:t,workflowState:e})}},computed:Object(r["a"])({},Object(l["e"])("projector",["proposalWorkflowStates"]),{workflowStates:function(){var t=this;return this.proposalWorkflowStates.filter(function(e){return t.quickSelect&&e.quickSelect||e.name===t.item.workflowState})}})},X=K,Y=Object(S["a"])(X,Q,z,!1,null,null,null),Z=Y.exports,tt={data:function(){return{proposalActions:{left:this.selectProposal,right:this.downShift}}},components:{Proposal:Z},methods:Object(r["a"])({},Object(l["d"])("projector",["selectProposal","downShift"])),computed:Object(r["a"])({},Object(l["e"])("projector",["proposalWorkflowStates"]),Object(l["c"])("projector",["filteredProposals"]))},et=tt,ot=Object(S["a"])(et,R,V,!1,null,null,null),at=ot.exports,nt=function(){var t=this,e=t.$createElement,o=t._self._c||e;return o("ul",{staticClass:"list-group",attrs:{id:"projector-main"}},t._l(t.selectedProposals,function(e){return o("proposal",{key:e.uid,attrs:{actions:t.proposalActions,item:e,"quick-select":""}})}),1)},st=[],rt={data:function(){return{proposalActions:{right:this.deselectProposal,setWorkflowState:this.setProposalWorkflowState}}},components:{Proposal:Z},methods:Object(r["a"])({},Object(l["d"])("projector",["deselectProposal"]),Object(l["b"])("projector",["setProposalWorkflowState"])),computed:Object(r["a"])({},Object(l["c"])("projector",["selectedProposals"]))},lt=rt,it=Object(S["a"])(lt,nt,st,!1,null,null,null),ct=it.exports,pt={name:"app",data:function(){return{ready:!1}},components:{ProjectorNav:J,ProposalSelection:at,ProposalsMain:ct,Modal:E,FlashMessages:O},created:function(){var t=this;v($("body").data("src")).done(function(e){t.$store.commit("meeting/load",e.meeting),t.$store.commit("projector/load",e),t.$root.ts=e.ts,t.ready=!0;var o="#"===location.hash[0]?location.hash.slice(1):location.hash;o&&t.loadAgendaItemByName(o)}),window.onpopstate=function(e){t.loadAgendaItemByName(e.state&&e.state.name)},$("body").on("click","[data-tag-filter]",function(e){e.preventDefault();var o=$(e.currentTarget).data("tagFilter").toLowerCase();t.filterByTag(o)})},methods:Object(r["a"])({},Object(l["b"])("projector",["loadAgendaItemByName"]),Object(l["d"])("projector",["filterByTag"]))},dt=pt,ut=(o("cf25"),Object(S["a"])(dt,n,s,!1,null,null,null)),ft=ut.exports,gt=(o("7514"),o("456d"),["ongoing","upcoming","closed","private"]),mt=function(t,e){var o=t.agenda.indexOf(t.currentAgendaItem)+e;if(-1<o&&o<t.agenda.length)return t.agenda[o]},ht={namespaced:!0,state:{title:"",href:"",agenda:[],currentAgendaItem:void 0,loaded:!1},getters:{agendaStates:function(t){var e={};return gt.forEach(function(o){e[o]=t.agenda.filter(function(t){return t.workflowState===o})}),e},previousAgendaItem:function(t){return mt(t,-1)},nextAgendaItem:function(t){return mt(t,1)}},mutations:{load:function(t,e){Object.keys(e).forEach(function(o){t[o]=e[o]}),t.loaded=!0},setAgendaItem:function(t,e){t.currentAgendaItem=t.agenda.find(function(t){return t.uid===e})}}},vt=(o("6762"),o("2fdb"),{namespaced:!0,state:{proposalWorkflowStates:[],pollGroups:[],proposals:[],proposalSelection:[],proposalOrder:[],pollsOngoing:[],pollsClosed:[],agendaUrl:null,requestActive:!1,api:{},logo:""},getters:{filteredProposals:function(t){var e={};return t.proposalWorkflowStates.forEach(function(t){t.checked&&(e[t.name]=!0)}),t.proposalOrder.map(function(e){return t.proposals.find(function(t){return t.uid===e})}).filter(function(o){return o.workflowState in e&&!t.proposalSelection.includes(o.uid)})},selectedProposals:function(t){return t.proposalSelection.map(function(e){return t.proposals.find(function(t){return t.uid===e})})}},mutations:{load:function(t,e){t.proposalWorkflowStates=e.proposalWorkflowStates,t.pollGroups=e.pollGroups,t.api=e.api,t.logo=e.logo},setAgendaUrl:function(t,e){t.agendaUrl=e,t.proposals=[],t.proposalSelection=[],t.proposalOrder=[],t.pollsOngoing=[],t.pollsClosed=[]},loadAgendaItem:function(t,e){t.proposals=e.proposals,t.pollsOngoing=e.pollsOngoing,t.pollsClosed=e.pollsClosed;var o=function(e){return void 0!==t.proposals.find(function(t){return t.uid===e})};t.proposalOrder=t.proposalOrder.filter(o),t.proposalSelection=t.proposalSelection.filter(o),e.proposals.forEach(function(e){t.proposalOrder.includes(e.uid)||t.proposalOrder.push(e.uid)})},toggleProposalWorkflow:function(t,e){var o=t.proposalWorkflowStates.find(function(t){return t.name===e});o.checked=!o.checked},setProposalWorkflowState:function(t,e){var o=e.proposal,a=e.workflowState;o.workflowState=a.name},downShift:function(t,e){t.proposalOrder.splice(t.proposalOrder.indexOf(e.uid),1),t.proposalOrder.push(e.uid)},selectProposal:function(t,e){t.proposalSelection.unshift(e.uid)},deselectProposal:function(t,e){t.proposalSelection.splice(t.proposalSelection.indexOf(e.uid),1)},setRequestActive:function(t,e){t.requestActive=e},filterByTag:function(t,e){var o={};t.proposalWorkflowStates.forEach(function(t){t.checked&&(o[t.name]=!0)}),t.proposalSelection=t.proposals.filter(function(t){return-1!==t.tags.indexOf(e)&&t.workflowState in o}).map(function(t){return t.uid})}},actions:{updateAgendaItems:function(t){var e=t.state,o=t.commit,a=arguments.length>1&&void 0!==arguments[1]&&arguments[1];!e.agendaUrl||a&&document.hidden||v(e.agendaUrl,{polling:a}).done(function(t){o("loadAgendaItem",t)})},loadAgendaItem:function(t,e){var o=t.commit,a=t.dispatch;e&&(o("meeting/setAgendaItem",e.uid,{root:!0}),o("setAgendaUrl",e.jsonUrl),a("updateAgendaItems"))},loadAgendaItemByName:function(t,e){var o=t.rootState,a=t.dispatch,n=o.meeting.agenda.find(function(t){return t.name===e})||{jsonUrl:null,uid:null};a("loadAgendaItem",n)},setProposalWorkflowState:function(t,e){var o=t.state,a=t.commit,n=e.proposal,s=e.workflowState,r=o.proposalWorkflowStates.find(function(t){return t.name===n.workflowState});s.quickSelect&&r!==s&&v(n.workflowApi,{method:"POST",data:{state:s.name}}).done(function(t){var e=o.proposalWorkflowStates.find(function(e){return e.name===t.state});a("setProposalWorkflowState",{proposal:n,workflowState:e})})}}});a["a"].use(l["a"]);var bt=!1,wt=new l["a"].Store({modules:{meeting:ht,projector:vt},strict:bt});a["a"].config.productionTip=!1;var _t={install:function(t){t.prototype.$t=function(t){return this.$root.ts[t]||t}}};a["a"].use(_t),$(function(){new a["a"]({store:wt,render:function(t){return t(ft)},data:{ts:{}}}).$mount("#app")})},cf25:function(t,e,o){"use strict";var a=o("0cfb"),n=o.n(a);n.a}});
//# sourceMappingURL=app.7c5fb6f5.js.map