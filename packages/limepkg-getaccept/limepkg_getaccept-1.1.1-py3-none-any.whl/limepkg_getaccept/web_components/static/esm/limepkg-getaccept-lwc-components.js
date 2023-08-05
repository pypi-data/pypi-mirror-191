import { p as promiseResolve, b as bootstrapLazy } from './index-5c035b3e.js';

/*
 Stencil Client Patch Browser v2.20.0 | MIT Licensed | https://stenciljs.com
 */
const patchBrowser = () => {
    const importMeta = import.meta.url;
    const opts = {};
    if (importMeta !== '') {
        opts.resourcesUrl = new URL('.', importMeta).href;
    }
    return promiseResolve(opts);
};

patchBrowser().then(options => {
  return bootstrapLazy([["lwc-getaccept-root",[[1,"lwc-getaccept-root",{"platform":[16],"context":[16],"externalId":[32],"isOpen":[32],"session":[32],"user":[32],"entities":[32],"documentId":[32],"activeView":[32],"documentData":[32],"isSealed":[32],"template":[32],"limeDocument":[32],"templateFields":[32],"templateRoles":[32],"errorMessage":[32],"documents":[32],"isLoadingDocuments":[32],"isSending":[32]},[[0,"changeView","changeViewHandler"],[0,"loadRelatedDocuments","loadRealtedDocumentsHandler"],[0,"setTemplate","setTemplate"],[0,"setLimeDocument","setLimeDocument"],[0,"setCustomFields","setCustomFields"],[0,"setTemplateRoles","setTemplateRoles"],[0,"updateDocumentRecipient","updateDocumentRecipientHandler"],[0,"setDocumentType","documentTypeHandler"],[0,"setSession","setSessionHandler"],[0,"setNewDocumentName","setDocumentName"],[0,"setDocumentValue","setDocumentValue"],[0,"setSmartReminder","setDocumentSmartReminder"],[0,"setIsSmsSending","setDocumentIsSmsSending"],[0,"setEmailSubject","setDocumentEmailSubject"],[0,"setEmailMessage","setDocumentEmailMessage"],[0,"validateDocument","validateDocumentHandler"],[0,"openDocument","openDocumentDetails"],[0,"recipientRoleUpdated","updateRecipientRole"],[0,"setVideo","setDocumentVideo"],[0,"removeVideo","removeDocumentVideo"],[0,"isSendingDocument","setIsSending"],[0,"documentCompleted","documentCompleted"],[0,"errorHandler","onError"]]]]],["lwc-getaccept-loader",[[1,"lwc-getaccept-loader",{"platform":[16],"context":[16]}]]],["menu-button",[[1,"menu-button",{"menuItem":[16]}]]],["send-document-button-group",[[1,"send-document-button-group",{"disabled":[32],"loading":[32]}]]],["create-email",[[1,"create-email",{"document":[16],"emailSubject":[32],"emailMessage":[32]}]]],["document-page-info",[[1,"document-page-info",{"page":[16],"documentId":[1,"document-id"],"session":[16],"totalTime":[2,"total-time"],"value":[32],"valuePercent":[32]}]]],["profile-picture",[[1,"profile-picture",{"thumbUrl":[1,"thumb-url"]}]]],["video-thumb",[[1,"video-thumb",{"video":[16]}]]],["ga-login_2",[[1,"ga-login",{"platform":[16],"loading":[32],"errorOnLogin":[32],"email":[32],"password":[32]}],[1,"ga-signup",{"platform":[16],"isLoading":[32],"disableSignup":[32],"signupFirstName":[32],"signupLastName":[32],"companyName":[32],"mobile":[32],"countryCode":[32],"signupEmail":[32],"signupPassword":[32]}]]],["recipient-item",[[1,"recipient-item",{"recipient":[16],"showAdd":[4,"show-add"]}]]],["empty-state",[[1,"empty-state",{"text":[1],"icon":[1]}]]],["recipient-item-added_2",[[1,"selected-recipient-list",{"recipients":[16],"document":[16]}],[1,"recipient-item-added",{"recipient":[16],"isSigning":[4,"is-signing"]}]]],["document-list_3",[[1,"document-list",{"documents":[16],"intervalId":[32]}],[1,"send-new-document-button",{"isSigning":[4,"is-signing"]}],[1,"document-list-item",{"document":[16]}]]],["ga-loader",[[1,"ga-loader"]]],["custom-fields_4",[[1,"custom-fields",{"template":[16],"customFields":[16],"isLoading":[4,"is-loading"]}],[1,"lime-document-list",{"documents":[16],"selectedLimeDocument":[16],"isLoading":[4,"is-loading"]}],[1,"template-list",{"templates":[16],"selectedTemplate":[16],"isLoading":[4,"is-loading"]}],[1,"template-preview",{"template":[16],"isLoading":[4,"is-loading"],"session":[16]}]]],["document-error_5",[[1,"document-error-feedback",{"document":[16],"errorList":[16]}],[1,"document-validate-info",{"document":[16]}],[1,"ga-loader-with-text",{"showText":[4,"show-text"],"text":[1]}],[1,"share-document-link",{"recipient":[16]}],[1,"document-error",{"error":[16]}]]],["error-message_14",[[1,"layout-validate-document",{"document":[16],"template":[16],"templateRoles":[16],"limeDocument":[16],"fields":[16],"platform":[16],"session":[16],"isSealed":[4,"is-sealed"],"isSending":[4,"is-sending"],"isLoading":[32],"recipients":[32],"errorList":[32],"sentDocument":[32]}],[1,"layout-select-file",{"platform":[16],"context":[16],"session":[16],"selectedTemplate":[16],"selectedLimeDocument":[16],"customFields":[16],"templateRoles":[16],"isLoadingTemplates":[32],"templates":[32],"isLoadingFields":[32],"isLoadingLimeDocuments":[32],"limeDocuments":[32],"openSection":[32],"tableData":[32],"columns":[32],"tabs":[32],"gaMergeFieldColumns":[32],"gaMergeFields":[32]},[[0,"updateFieldValue","updateFieldValue"]]],[1,"layout-overview",{"sentDocuments":[16],"platform":[16],"externalId":[1,"external-id"],"session":[16],"documents":[16],"isLoadingDocuments":[32]}],[1,"layout-select-recipient",{"platform":[16],"document":[16],"context":[16],"searchTerm":[32],"selectedRecipientList":[32],"includeCoworkers":[32],"recipientList":[32]},[[0,"removeRecipient","removeRecipientHandler"],[0,"changeRecipientRole","changeRecipientRoleHandler"]]],[1,"layout-document-details",{"documentId":[1,"document-id"],"platform":[16],"session":[16],"documentData":[32],"isLoading":[32]}],[1,"layout-login",{"platform":[16],"isSignup":[32]}],[1,"layout-settings",{"entities":[16],"user":[8],"session":[16],"platform":[16],"entityOptions":[32],"selectedEntity":[32],"isLoading":[32],"error":[32]}],[1,"layout-video-library",{"platform":[16],"session":[16],"videos":[32],"isLoadingVideos":[32]}],[1,"layout-send-document",{"document":[16],"template":[16],"limeDocument":[16],"platform":[16],"session":[16],"documentName":[32],"value":[32],"smartReminder":[32],"sendLinkBySms":[32],"documentVideo":[32]}],[1,"error-message",{"timeout":[2],"error":[1],"message":[32]}],[1,"layout-help"],[1,"layout-menu",{"activeView":[1,"active-view"],"isSending":[4,"is-sending"],"menuItems":[32],"isOpen":[32]}],[1,"layout-template-roles",{"context":[16],"document":[16],"template":[16],"limeDocument":[16],"platform":[16],"session":[16],"templateRoles":[16],"value":[32],"options":[32],"recipients":[32]}],[1,"workflow-progress-bar",{"activeView":[1,"active-view"],"isVisible":[4,"is-visible"]}]]]], options);
});
