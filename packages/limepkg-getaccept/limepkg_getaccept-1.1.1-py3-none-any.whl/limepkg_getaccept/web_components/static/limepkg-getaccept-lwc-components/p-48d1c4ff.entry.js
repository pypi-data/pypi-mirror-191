import{r,h as t}from"./p-c89d00a0.js";const e=class{constructor(t){r(this,t),this.thumbUrl=void 0}render(){return this.thumbUrl?t("img",{class:"thumbnail",src:this.getThumbUrl(this.thumbUrl)}):t("div",{class:"thumbnail thumbnail-placeholder"},t("limel-icon",{name:"user"}))}getThumbUrl(r=""){const t=r.split("/").slice(-1)[0];return`getaccept/thumb_proxy/${r.split("/")[3]}/${t}`}};e.style=".thumbnail{display:flex;justify-content:center;align-items:center;width:6rem;height:6rem;border-radius:50%;box-shadow:0 3px 6px rgba(0, 0, 0, 0.05), 0 3px 6px rgba(0, 0, 0, 0.05);margin-bottom:1rem}.thumbnail-placeholder{background-color:#f5f5f5}.thumbnail-placeholder limel-icon{height:3rem;width:3rem}";export{e as profile_picture}