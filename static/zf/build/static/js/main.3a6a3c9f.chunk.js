(window.webpackJsonp=window.webpackJsonp||[]).push([[0],{143:function(t,e,n){t.exports=n(293)},148:function(t,e,n){},149:function(t,e,n){},293:function(t,e,n){"use strict";n.r(e);var a=n(1),i=n.n(a),o=n(7),r=n.n(o),c=(n(148),n(149),n(92)),l=n.n(c),s=n(125),d=n(126),u=n(127),p=n(140),m=n(128),g=n(141),f=n(295),h=n(70),w="http://zf-api.yangzhixiao.top",v=function(t){function e(){var t,n;Object(d.a)(this,e);for(var a=arguments.length,i=new Array(a),o=0;o<a;o++)i[o]=arguments[o];return(n=Object(p.a)(this,(t=Object(m.a)(e)).call.apply(t,[this].concat(i)))).state={data:[],loading:!1},n.handleDownloadClick=function(t){window.open(w+"/download/"+t,"_blank")},n.fetchData=Object(s.a)(l.a.mark(function t(){var e;return l.a.wrap(function(t){for(;;)switch(t.prev=t.next){case 0:return n.setState({loading:!0}),t.next=3,fetch(w+"/api/list");case 3:e=t.sent,n.setState({data:e,loading:!1});case 5:case"end":return t.stop()}},t)})),n}return Object(g.a)(e,t),Object(u.a)(e,[{key:"componentDidMount",value:function(){this.fetchData()}},{key:"render",value:function(){var t=this,e=this.state,n=e.data,i=e.loading;return a.createElement(f.a,{style:{padding:"15px"},rowKey:"id",loading:i,dataSource:n,pagination:{position:"bottom",pageSize:8},columns:[{title:"\u56fe\u7247",dataIndex:"imgs",render:function(t,e,n){return a.createElement("div",null,a.createElement("div",{style:{lineHeight:"20px",marginBottom:"5px",marginLeft:"10px"}},"".concat(e.updatetime," ").concat(e.title)),e.imgs&&e.imgs.split(",").map(function(t){return a.createElement("a",{key:t,href:w+"/static/images/"+t,target:"_blank",rel:"noopener noreferrer"},a.createElement("img",{style:{margin:"5px"},alt:t,src:w+"/static/images/"+t.replace(".jpg","_thumb.jpg")}))}))}},{title:"\u64cd\u4f5c",dataIndex:"id",width:150,render:function(e,n,i){return a.createElement(h.a,{type:"primary",onClick:function(){return t.handleDownloadClick(n.id)}},"\u4e0b\u8f7d\u56fe\u7247")}}]})}}]),e}(a.Component),y=(n(292),function(){return i.a.createElement(v,null)});Boolean("localhost"===window.location.hostname||"[::1]"===window.location.hostname||window.location.hostname.match(/^127(?:\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}$/));r.a.render(i.a.createElement(y,null),document.getElementById("root")),"serviceWorker"in navigator&&navigator.serviceWorker.ready.then(function(t){t.unregister()})}},[[143,1,2]]]);
//# sourceMappingURL=main.3a6a3c9f.chunk.js.map