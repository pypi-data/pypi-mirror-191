'use strict';

Object.defineProperty(exports, '__esModule', { value: true });

const index = require('./index-397a20ca.js');
const EnumViews = require('./EnumViews-c38e917e.js');
const index$1 = require('./index-70de2618.js');
const workflowSteps = require('./workflow-steps-578fdbd9.js');

const lwcGetacceptRootCss = "limel-dialog{--dialog-heading-icon-background-color:#f49132}limel-dialog.preview-view{--dialog-width:40rem;--dialog-height:45rem}limel-dialog .ga-version{position:absolute;bottom:0;right:0}limel-dialog .ga-body{overflow:auto;min-height:min-content;margin-top:1rem}limel-dialog .ga-top-bar{position:sticky;top:0;height:5rem;background-color:#fff;z-index:4;display:flex;align-items:center;z-index:9}@media (min-width: 1074px){limel-dialog{--dialog-width:65rem;--dialog-height:40rem}}@media (max-width: 1075px){limel-dialog{--dialog-width:55rem;--dialog-height:40rem}}@media (min-width: 1800px){limel-dialog{--dialog-width:70rem;--dialog-height:60rem}}limel-button{--lime-primary-color:#f49132}.logo-container{height:2.2rem;width:10rem;margin-bottom:1rem;cursor:pointer;transition:width 0.5s;overflow:hidden}.logo-container.compact{width:2.8rem}.logo-container:hover{opacity:0.8}.logo-container .logo{height:2.2rem}.close{display:block;position:absolute;right:-1rem;top:0rem;cursor:pointer}.close:hover{color:#eee}.actionpad-container{width:100%}.getaccept-button{width:100%;display:flex;justify-content:start;align-items:center;padding:0.425rem 0.875rem 0.425rem 0.875rem;border:none;border-radius:2rem;cursor:pointer;transition:background 0.8s;background-position:center;font-size:0.8rem;font-weight:bold;color:#444;background:#eee}.getaccept-button:focus{outline:0}.getaccept-button:hover{background:#f5f5f5 radial-gradient(circle, transparent 1%, #f5f5f5 1%) center/15000%}.getaccept-button:active{background-color:white;background-size:100%;transition:background 0s}.getaccept-button img{height:2rem;flex:0}.getaccept-button .button-text{margin-left:0.5rem;flex:2;text-align:left}.getaccept-button .document-count{margin-left:auto;display:flex;align-items:center}.getaccept-button .document-count limel-icon{margin-right:0.3rem}workflow-progress-bar{position:absolute;top:1.5rem;left:4rem;right:4rem}";

const Root = class {
  constructor(hostRef) {
    index.registerInstance(this, hostRef);
    this.errorHandler = index.createEvent(this, "errorHandler", 7);
    this.platform = undefined;
    this.context = undefined;
    this.externalId = undefined;
    this.isOpen = false;
    this.session = undefined;
    this.user = undefined;
    this.entities = [];
    this.documentId = undefined;
    this.activeView = EnumViews.EnumViews.login;
    this.documentData = undefined;
    this.isSealed = undefined;
    this.template = undefined;
    this.limeDocument = undefined;
    this.templateFields = undefined;
    this.templateRoles = undefined;
    this.errorMessage = '';
    this.documents = [];
    this.isLoadingDocuments = undefined;
    this.isSending = false;
    this.openDialog = this.openDialog.bind(this);
    this.handleLogoClick = this.handleLogoClick.bind(this);
    this.renderLayout = this.renderLayout.bind(this);
    this.loadInitialData = this.loadInitialData.bind(this);
    this.loadSentDocuments = this.loadSentDocuments.bind(this);
    this.showWorkflow = this.showWorkflow.bind(this);
  }
  componentWillLoad() {
    this.externalId = `${this.context.limetype}_${this.context.id}`;
    this.activeView = this.checkIfSessionExists
      ? EnumViews.EnumViews.home
      : EnumViews.EnumViews.login;
    if (this.session) {
      this.loadInitialData();
    }
    this.setDefaultDocumentData();
  }
  async loadInitialData() {
    this.loadSentDocuments();
    try {
      const { user, entities } = await index$1.fetchMe(this.platform, this.session);
      this.user = user;
      this.entities = entities;
    }
    catch (e) {
      this.errorHandler.emit('Could not load user session. Try relogging');
    }
    this.loadEntityDetails();
  }
  async loadEntityDetails() {
    try {
      const { entity } = await index$1.fetchEntity(this.platform, this.session);
      this.session.entity_id = entity.id;
      this.documentData.email_send_message =
        entity.email_send_message !== ''
          ? entity.email_send_message
          : entity.default_email_send_message;
      this.documentData.email_send_subject =
        entity.email_send_subject !== ''
          ? entity.email_send_subject
          : entity.default_email_send_subject;
    }
    catch (e) {
      this.errorHandler.emit('Could not load user session. Try relogging');
    }
  }
  render() {
    return [
      index.h("limel-flex-container", { class: "actionpad-container" }, index.h("button", { class: "getaccept-button", onClick: this.openDialog }, index.h("img", { src: "https://static-vue-rc.getaccept.com/img/integrations/logo_only.png" }), index.h("span", { class: "button-text" }, "Send document"), this.renderDocumentCount(!!this.session))),
      index.h("limel-dialog", { open: this.isOpen, closingActions: { escapeKey: true, scrimClick: false }, onClose: () => {
          this.isOpen = false;
        } }, index.h("div", { class: "ga-top-bar" }, this.renderLogo(this.showWorkflow()), index.h("limel-icon", { class: "close", name: "cancel", size: "small", onClick: () => {
          this.isOpen = false;
        } }), (() => {
        if (this.activeView !== EnumViews.EnumViews.login) {
          return [
            index.h("layout-menu", { activeView: this.activeView, isSending: this.isSending }),
            index.h("workflow-progress-bar", { isVisible: this.showWorkflow(), activeView: this.activeView }),
          ];
        }
      })()), index.h("div", { class: "ga-body" }, this.renderLayout()), index.h("limel-button-group", { slot: "button" }, index.h("limel-button", { label: "Cancel", onClick: () => {
          this.isOpen = false;
        } })), index.h("error-message", { error: this.errorMessage }), index.h("div", { class: "ga-version" }, index.h("span", null, "Version: 1.1.1"))),
    ];
  }
  renderDocumentCount(hasSession) {
    if (hasSession) {
      return (index.h("span", { class: "document-count" }, index.h("limel-icon", { name: "file", size: "small" }), index.h("span", null, this.documents.length)));
    }
    return [];
  }
  renderLogo(compact) {
    const classes = `logo-container ${compact ? 'compact' : ''}`;
    return (index.h("div", { class: classes }, index.h("img", { onClick: this.handleLogoClick, src: "https://static-vue-rc.getaccept.com/img/integrations/logo-inverted.png", class: "logo" })));
  }
  showWorkflow() {
    if (this.isSending || this.isSealed) {
      return false;
    }
    return workflowSteps.workflowSteps.some(view => view.currentView === this.activeView);
  }
  renderLayout() {
    switch (this.activeView) {
      case EnumViews.EnumViews.home:
        return (index.h("layout-overview", { platform: this.platform, session: this.session, externalId: this.externalId, documents: this.documents }));
      case EnumViews.EnumViews.login:
        return index.h("layout-login", { platform: this.platform });
      case EnumViews.EnumViews.selectFile:
        return (index.h("layout-select-file", { platform: this.platform, session: this.session, context: this.context, selectedLimeDocument: this.limeDocument, selectedTemplate: this.template, customFields: this.templateFields, templateRoles: this.templateRoles }));
      case EnumViews.EnumViews.templateRoles:
        return (index.h("layout-template-roles", { platform: this.platform, session: this.session, context: this.context, document: this.documentData, limeDocument: this.limeDocument, template: this.template, templateRoles: this.templateRoles }));
      case EnumViews.EnumViews.recipient:
        return (index.h("layout-select-recipient", { platform: this.platform, document: this.documentData, context: this.context }));
      case EnumViews.EnumViews.settings:
        return (index.h("layout-settings", { user: this.user, entities: this.entities, session: this.session, platform: this.platform }));
      case EnumViews.EnumViews.help:
        return index.h("layout-help", null);
      case EnumViews.EnumViews.sendDocument:
        return (index.h("layout-send-document", { document: this.documentData, limeDocument: this.limeDocument, template: this.template, session: this.session, platform: this.platform }));
      case EnumViews.EnumViews.videoLibrary:
        return (index.h("layout-video-library", { platform: this.platform, session: this.session }));
      case EnumViews.EnumViews.documentDetail:
        return (index.h("layout-document-details", { platform: this.platform, session: this.session, documentId: this.documentId }));
      case EnumViews.EnumViews.documentValidation:
        return (index.h("layout-validate-document", { platform: this.platform, session: this.session, document: this.documentData, limeDocument: this.limeDocument, template: this.template, fields: this.templateFields, isSealed: this.isSealed, isSending: this.isSending, templateRoles: this.templateRoles }));
      default:
        return index.h("layout-overview", null);
    }
  }
  logout() {
    localStorage.removeItem('getaccept_session');
    this.documents = [];
    this.activeView = EnumViews.EnumViews.login;
  }
  openDialog() {
    this.isOpen = true;
    if (this.checkIsPreviewView) {
      this.element.shadowRoot.lastElementChild.classList.add('preview-view');
    }
  }
  handleLogoClick() {
    this.activeView = this.checkIfSessionExists
      ? EnumViews.EnumViews.home
      : EnumViews.EnumViews.login;
  }
  async loadSentDocuments() {
    this.isLoadingDocuments = true;
    try {
      this.documents = await index$1.fetchSentDocuments(this.platform, this.externalId, this.session);
    }
    catch (e) {
      this.errorHandler.emit('Something went wrong while documents from GetAccept...');
    }
    this.isLoadingDocuments = false;
  }
  changeViewHandler(view) {
    if (view.detail === EnumViews.EnumViews.logout) {
      this.logout();
    }
    else if (this.isSealed) {
      this.activeView = EnumViews.EnumViews.home;
      this.setDefaultDocumentData();
    }
    else {
      this.activeView = view.detail;
    }
  }
  loadRealtedDocumentsHandler() {
    this.loadSentDocuments();
  }
  setTemplate(event) {
    this.template = event.detail;
    this.documentData.name = event.detail.text;
    this.limeDocument = null;
    this.templateFields = [];
  }
  setLimeDocument(event) {
    this.limeDocument = event.detail;
    this.template = null;
    this.templateFields = [];
  }
  setCustomFields(event) {
    this.templateFields = event.detail;
  }
  setTemplateRoles(event) {
    this.templateRoles = event.detail;
    this.documentData = Object.assign(Object.assign({}, this.documentData), { recipients: this.documentData.recipients.map(recipient => (Object.assign(Object.assign({}, recipient), { role_id: '' }))) });
  }
  updateDocumentRecipientHandler(recipients) {
    this.documentData.recipients = recipients.detail;
  }
  documentTypeHandler(isSigning) {
    this.documentData.is_signing = isSigning.detail;
  }
  setSessionHandler(sessionData) {
    this.setSessionData(sessionData.detail);
    this.activeView = EnumViews.EnumViews.home;
    this.loadInitialData();
  }
  setDocumentName(documentName) {
    this.documentData = Object.assign(Object.assign({}, this.documentData), { name: documentName.detail });
  }
  setDocumentValue(value) {
    this.documentData = Object.assign(Object.assign({}, this.documentData), { value: value.detail });
  }
  setDocumentSmartReminder(smartReminder) {
    this.documentData.is_reminder_sending = smartReminder.detail;
  }
  setDocumentIsSmsSending(isSmsSending) {
    this.documentData.is_sms_sending = isSmsSending.detail;
  }
  setDocumentEmailSubject(emailSendSubject) {
    this.documentData.email_send_subject = emailSendSubject.detail;
  }
  setDocumentEmailMessage(emailSendMessage) {
    this.documentData.email_send_message = emailSendMessage.detail;
  }
  validateDocumentHandler() {
    this.activeView = EnumViews.EnumViews.documentValidation;
  }
  openDocumentDetails(document) {
    this.activeView = EnumViews.EnumViews.documentDetail;
    this.documentId = document.detail.id;
  }
  updateRecipientRole(event) {
    const newRecipients = [...this.documentData.recipients];
    const recipientIndex = newRecipients.findIndex(recipient => recipient.email === event.detail.recipient.email &&
      recipient.lime_id === event.detail.recipient.lime_id);
    newRecipients[recipientIndex].role_id = event.detail.role.role_id;
    this.documentData = Object.assign(Object.assign({}, this.documentData), { recipients: [...newRecipients] });
  }
  setDocumentVideo(videoId) {
    this.documentData.video_id = videoId.detail;
    this.documentData.is_video = true;
  }
  removeDocumentVideo() {
    this.documentData.video_id = '';
    this.documentData.is_video = false;
  }
  setIsSending(isSending) {
    this.isSending = isSending.detail;
  }
  documentCompleted(isSealed) {
    this.setDefaultDocumentData();
    this.loadEntityDetails();
    this.isSealed = isSealed.detail;
    if (!this.isSealed) {
      this.activeView = EnumViews.EnumViews.home;
    }
    this.loadSentDocuments();
  }
  onError(event) {
    this.errorMessage = event.detail;
    // eslint-disable-next-line @typescript-eslint/no-magic-numbers
    setTimeout(() => (this.errorMessage = ''), 100); // Needed for same consecutive error message
  }
  get checkIfSessionExists() {
    const storedSession = window.localStorage.getItem('getaccept_session');
    if (storedSession) {
      const sessionObj = JSON.parse(storedSession);
      // used to check if token should be refreshed or not.
      this.validateToken(sessionObj);
      this.session = sessionObj;
    }
    return !!storedSession;
  }
  get checkIsPreviewView() {
    var _a;
    return (_a = document
      .querySelector('limec-related-view')
      .shadowRoot.firstElementChild) === null || _a === void 0 ? void 0 : _a.classList.contains('related-view');
  }
  async validateToken(session) {
    const { data, success } = await index$1.refreshToken(this.platform, session);
    if (success) {
      const storedSession = window.localStorage.getItem('getaccept_session');
      if (storedSession) {
        const sessionObj = JSON.parse(storedSession);
        sessionObj.expires_in = data.expires_in;
        sessionObj.access_token = data.access_token;
        this.setSessionData(sessionObj);
      }
    }
    else {
      this.errorMessage = 'Could not refresh token.';
      setTimeout(() => (this.errorMessage = ''));
    }
    return true;
  }
  setSessionData(session) {
    window.localStorage.setItem('getaccept_session', JSON.stringify(session));
    this.session = session;
  }
  setDefaultDocumentData() {
    this.documentData = {
      is_signing: false,
      name: '',
      recipients: [],
      template_id: '',
      custom_fields: [],
      is_reminder_sending: false,
      is_sms_sending: false,
      email_send_subject: '',
      email_send_message: '',
      video_id: '',
      is_video: false,
      external_id: this.externalId,
      value: 0,
    };
    this.templateFields = [];
    this.isSealed = false;
    this.template = null;
    this.limeDocument = null;
  }
  get element() { return index.getElement(this); }
};
Root.style = lwcGetacceptRootCss;

exports.lwc_getaccept_root = Root;
