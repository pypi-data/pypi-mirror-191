/******************************************************************************
Copyright (c) Microsoft Corporation.

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
PERFORMANCE OF THIS SOFTWARE.
***************************************************************************** */

function __decorate(decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
}

/**
 * Events dispatched by the commandbus event middleware
 */
// eslint-disable-next-line no-shadow
var CommandEventName;
(function (CommandEventName) {
    /**
     * Dispatched when the command has been received by the commandbus.
     * Calling `preventDefault()` on the event will stop the command from being handled
     *
     * @detail { command }
     */
    CommandEventName["Received"] = "command.received";
    /**
     * Dispatched when the command has been handled by the commandbus
     *
     * @detail { command | result }
     */
    CommandEventName["Handled"] = "command.handled";
    /**
     * Dispatched if an error occurs while handling the command
     *
     * @detail { command | error }
     */
    CommandEventName["Failed"] = "command.failed";
})(CommandEventName || (CommandEventName = {}));
/**
 * Register a class as a command
 *
 * @param {CommandOptions} options a CommandOptions object containing the id of the command
 *
 * @returns {Function} callback which accepts a `CommandClass` and sets the command id
 */
function Command(options) {
    return (commandClass) => {
        setCommandId(commandClass, options.id);
    };
}
function setCommandId(commandClass, id) {
    // eslint-disable-next-line @typescript-eslint/dot-notation
    commandClass['commandId'] = id;
}

/**
 * Open a dialog for bulk creating limeobjects
 *
 *
 * ### Flow example
 * Let's have a look at the general flow by going through the concrete example of adding several persons to a marketing activity:
 * - Go to the table view of persons.
 * - Filter everyone who should be included in the marketing activity.
 * - Select 'Bulk create objects' form the action menu.
 * - Select marketing activity as type of content.
 * - Fill out the rest of the form and click 'create'.
 * - A toast message appears and gives you 5 seconds to undo the action before it creates the corresponding task.
 * - Another toast message will inform you after the task is completed.
 * - If the task ended successful you can go to the participant table view and check the result.
 *
 * ### Configuration
 * In order to activate the feature go to a table configuration in lime-admin to the limetype you want to bulk create from
 * and add the following configuration:
 *
 * ```json
 * "actions": [
 * {
 *      "id": "limeobject.bulk-create-dialog",
 *      "params": {
 *        "relations": [<LIST OF CREATABLE, RELATED FIELDS (AS STRINGS)>]
 *      }
 *    }
 * ],
 * ```
 *
 * @id `limeobject.bulk-create-dialog`
 */
let BulkCreateDialogCommand = class BulkCreateDialogCommand {
    constructor() {
        /**
         * A list of relation names that are possible to create from the limetype
         */
        this.relations = [];
    }
};
BulkCreateDialogCommand = __decorate([
    Command({
        id: 'limeobject.bulk-create-dialog',
    })
], BulkCreateDialogCommand);

/**
 * Open a dialog for creating a new limeobject or editing a specific limeobject
 *
 * The create dialog is implemented as a command so a plugin can easily replace the original dialog with a custom one.
 * Check out the "Hello, Event!" tutorial for a detailed description on how to implement your own create dialog.
 *
 * This dialog also useful to edit a limeobject that already exists
 *
 * @id `limeobject.create-dialog`
 */
let CreateLimeobjectDialogCommand = class CreateLimeobjectDialogCommand {
    constructor() {
        /**
         * Specifies if routing to limeobject should be done after confirmation
         */
        this.route = false;
    }
};
CreateLimeobjectDialogCommand = __decorate([
    Command({
        id: 'limeobject.create-dialog',
    })
], CreateLimeobjectDialogCommand);

/**
 * Deletes the object from the database
 *
 * @id `limeobject.delete-object`
 */
let DeleteObjectCommand = class DeleteObjectCommand {
};
DeleteObjectCommand = __decorate([
    Command({
        id: 'limeobject.delete-object',
    })
], DeleteObjectCommand);

/**
 * Open a dialog to view and edit object access information
 *
 * @id `limeobject.object-access`
 */
let OpenObjectAccessDialogCommand = class OpenObjectAccessDialogCommand {
};
OpenObjectAccessDialogCommand = __decorate([
    Command({
        id: 'limeobject.object-access',
    })
], OpenObjectAccessDialogCommand);

/**
 * Saves the object to the database
 *
 * @id `limeobject.save-object`
 */
let SaveLimeObjectCommand = class SaveLimeObjectCommand {
    constructor() {
        /**
         * Specifies if routing to limeobject should be done after confirmation
         */
        this.route = false;
    }
};
SaveLimeObjectCommand = __decorate([
    Command({
        id: 'limeobject.save-object',
    })
], SaveLimeObjectCommand);

var Operator$1;
(function (Operator) {
    Operator["AND"] = "AND";
    Operator["OR"] = "OR";
    Operator["EQUALS"] = "=";
    Operator["NOT"] = "!";
    Operator["GREATER"] = ">";
    Operator["LESS"] = "<";
    Operator["IN"] = "IN";
    Operator["BEGINS"] = "=?";
    Operator["LIKE"] = "?";
    Operator["LESS_OR_EQUAL"] = "<=";
    Operator["GREATER_OR_EQUAL"] = ">=";
})(Operator$1 || (Operator$1 = {}));

// eslint-disable-next-line no-shadow
var TaskState$1;
(function (TaskState) {
    /**
     * Task state is unknown
     */
    TaskState["Pending"] = "PENDING";
    /**
     * Task was started by a worker
     */
    TaskState["Started"] = "STARTED";
    /**
     * Task is waiting for retry
     */
    TaskState["Retry"] = "RETRY";
    /**
     * Task succeeded
     */
    TaskState["Success"] = "SUCCESS";
    /**
     * Task failed
     */
    TaskState["Failure"] = "FAILURE";
})(TaskState$1 || (TaskState$1 = {}));
/**
 * Events dispatched by the task service
 */
// eslint-disable-next-line no-shadow
var TaskEventType;
(function (TaskEventType) {
    /**
     * Dispatched when a task has been created.
     *
     * @detail { task }
     */
    TaskEventType["Created"] = "task.created";
    /**
     * Dispatched when the task has successfully been completed
     *
     * @detail { task }
     */
    TaskEventType["Success"] = "task.success";
    /**
     * Dispatched if an error occured while running the task
     *
     * @detail { task | error? }
     */
    TaskEventType["Failed"] = "task.failed";
})(TaskEventType || (TaskEventType = {}));

/**
 * Core platform service names
 *
 * @deprecated use {@link BaseName PlatformServiceName} from `@limetech/lime-web-components` instead
 */
var PlatformServiceName;
(function (PlatformServiceName) {
    PlatformServiceName["Translate"] = "translate";
    PlatformServiceName["Http"] = "http";
    PlatformServiceName["Route"] = "route";
    PlatformServiceName["Notification"] = "notifications";
    PlatformServiceName["Query"] = "query";
    PlatformServiceName["CommandBus"] = "commandBus";
    PlatformServiceName["Dialog"] = "dialog";
    PlatformServiceName["EventDispatcher"] = "eventDispatcher";
    /**
     * @note Work in progress, do not use!
     * @private
     */
    PlatformServiceName["Navigator"] = "navigator";
    /**
     * @note Work in progress, do not use!
     * @private
     */
    PlatformServiceName["RouteRegistry"] = "routeRegistry";
    /**
     * @note Work in progress, do not use!
     * @private
     */
    PlatformServiceName["KeybindingRegistry"] = "keybindingRegistry";
    PlatformServiceName["LimetypesState"] = "state.limetypes";
    PlatformServiceName["LimeobjectsState"] = "state.limeobjects";
    PlatformServiceName["ApplicationState"] = "state.application";
    PlatformServiceName["ConfigsState"] = "state.configs";
    PlatformServiceName["FiltersState"] = "state.filters";
    PlatformServiceName["DeviceState"] = "state.device";
    PlatformServiceName["TaskState"] = "state.tasks";
    PlatformServiceName["UserData"] = "state.user-data";
})(PlatformServiceName || (PlatformServiceName = {}));

/**
 * @deprecated use {@link BaseOperator Operator} from `@limetech/lime-web-components` instead
 */
var Operator;
(function (Operator) {
    Operator["AND"] = "AND";
    Operator["OR"] = "OR";
    Operator["EQUALS"] = "=";
    Operator["NOT"] = "!";
    Operator["GREATER"] = ">";
    Operator["LESS"] = "<";
    Operator["IN"] = "IN";
    Operator["BEGINS"] = "=?";
    Operator["LIKE"] = "?";
    Operator["LESS_OR_EQUAL"] = "<=";
    Operator["GREATER_OR_EQUAL"] = ">=";
})(Operator || (Operator = {}));

/* eslint-disable jsdoc/require-returns */
/**
 * @deprecated use {@link CommandEventName} from `@limetech/lime-web-components`
 * instead
 */
var CommandEvent;
(function (CommandEvent) {
    /**
     * Dispatched when the command has been received by the commandbus.
     * Calling `preventDefault()` on the event will stop the command from being handled
     *
     * @detail { command }
     */
    CommandEvent["Received"] = "command.received";
    /**
     * Dispatched when the command has been handled by the commandbus
     *
     * @detail { command | result }
     */
    CommandEvent["Handled"] = "command.handled";
    /**
     * Dispatched if an error occurs while handling the command
     *
     * @detail { command | error }
     */
    CommandEvent["Failed"] = "command.failed";
})(CommandEvent || (CommandEvent = {}));

/**
 * @deprecated use {@link BaseState TaskState} from `@limetech/lime-web-components` instead
 */
var TaskState;
(function (TaskState) {
    /**
     * Task state is unknown
     */
    TaskState["Pending"] = "PENDING";
    /**
     * Task was started by a worker
     */
    TaskState["Started"] = "STARTED";
    /**
     * Task is waiting for retry
     */
    TaskState["Retry"] = "RETRY";
    /**
     * Task succeeded
     */
    TaskState["Success"] = "SUCCESS";
    /**
     * Task failed
     */
    TaskState["Failure"] = "FAILURE";
})(TaskState || (TaskState = {}));
/**
 * @deprecated use {@link TaskEventType} from `@limetech/lime-web-components` instead
 */
var TaskEvent;
(function (TaskEvent) {
    /**
     * Dispatched when a task has been created.
     *
     * @detail { task }
     */
    TaskEvent["Created"] = "task.created";
    /**
     * Dispatched when the task has successfully been completed
     *
     * @detail { task }
     */
    TaskEvent["Success"] = "task.success";
    /**
     * Dispatched if an error occured while running the task
     *
     * @detail { task | error? }
     */
    TaskEvent["Failed"] = "task.failed";
})(TaskEvent || (TaskEvent = {}));

/* eslint-disable camelcase */
const fetchMe = async (platform, session) => {
  const options = {
    headers: getHeaders(session),
  };
  const { data } = await platform
    .get(PlatformServiceName.Http)
    .get('getaccept/me', options);
  return data;
};
const switchEntity = async (entity_id, platform, session) => {
  const options = {
    headers: getHeaders(session),
  };
  const payload = {
    entity_id: entity_id,
  };
  const { data } = await platform
    .get(PlatformServiceName.Http)
    .post('getaccept/switch-entity', payload, options);
  return data;
};
const fetchLimeDocuments = async (platform, limetype, record_id, selectedLimeDocument) => {
  const options = {
    params: {
      limetype: limetype,
      record_id: record_id.toString(),
    },
  };
  const documents = await platform
    .get(PlatformServiceName.Http)
    .get('getaccept/documents', options);
  return documents.map(document => ({
    text: document.comment ? document.comment : '(Empty description)',
    value: document.id,
    icon: 'document',
    iconColor: 'var(--lime-green)',
    selected: selectedLimeDocument && selectedLimeDocument.value === document.id,
  }));
};
const fetchSentDocuments = async (platform, externalId, session) => {
  const options = {
    headers: {
      'ga-auth-token': session.access_token,
    },
    params: {
      external_id: externalId,
    },
  };
  const { documents } = await platform
    .get(PlatformServiceName.Http)
    .get('getaccept/sent-documents', options);
  return documents;
};
const fetchTemplates = async (platform, session, selectedTemplate) => {
  const options = {
    headers: {
      'ga-auth-token': session.access_token,
    },
  };
  const { templates = [] } = await platform
    .get(PlatformServiceName.Http)
    .get('getaccept/templates', options);
  return templates.map((template) => ({
    text: template.name,
    value: template.id,
    icon: 'document',
    iconColor: 'var(--lime-orange)',
    selected: selectedTemplate && selectedTemplate.value === template.id,
  }));
};
const fetchTemplateFields = async (platform, session, limetype, record_id, selectedTemplate) => {
  const options = {
    headers: {
      'ga-auth-token': session.access_token,
    },
    params: {
      template_id: selectedTemplate.value,
      limetype: limetype,
      record_id: record_id.toString(),
    },
  };
  const { data: { fields = [] }, } = await platform
    .get(PlatformServiceName.Http)
    .get('getaccept/template-fields', options);
  return fields;
};
const fetchTemplateRoles = async (platform, session, limetype, record_id, selectedTemplate) => {
  const options = {
    headers: {
      'ga-auth-token': session.access_token,
    },
    params: {
      template_id: selectedTemplate.value,
      limetype: limetype,
      record_id: record_id.toString(),
    },
  };
  const { data } = await platform
    .get(PlatformServiceName.Http)
    .get('getaccept/template-roles', options);
  return (data === null || data === void 0 ? void 0 : data.roles) || [];
};
const fetchObjectProps = async (platform, session, limetype, record_id) => {
  const options = {
    headers: {
      'ga-auth-token': session.access_token,
    },
    params: {
      limetype: limetype,
      record_id: record_id.toString(),
    },
  };
  // eslint-disable-next-line no-return-await
  return await platform
    .get(PlatformServiceName.Http)
    .get('getaccept/object-props', options);
};
const getHeaders = (session) => {
  return {
    'ga-auth-token': session.access_token,
  };
};
const fetchEntity = async (platform, session) => {
  const options = {
    headers: getHeaders(session),
  };
  const { data } = await platform
    .get(PlatformServiceName.Http)
    .get('getaccept/entity', options);
  return data;
};
const fetchDocumentDetails = async (platform, session, document_id) => {
  const options = {
    headers: getHeaders(session),
    params: {
      document_id: document_id,
    },
  };
  const { data } = await platform
    .get(PlatformServiceName.Http)
    .get('getaccept/document-details', options);
  return data;
};
const fetchVideos = async (platform, session) => {
  const options = {
    headers: getHeaders(session),
  };
  const { data } = await platform
    .get(PlatformServiceName.Http)
    .get('getaccept/videos', options);
  return data;
};
const createDocument = async (platform, session, document) => {
  const options = {
    headers: getHeaders(session),
  };
  return platform
    .get(PlatformServiceName.Http)
    .post('getaccept/create-document', document, options);
};
const sealDocument = async (platform, session, documentId) => {
  const options = {
    headers: getHeaders(session),
  };
  const payload = {
    document_id: documentId,
  };
  return platform
    .get(PlatformServiceName.Http)
    .post('getaccept/seal-document', payload, options);
};
const uploadDocument = async (platform, session, documentId) => {
  const options = {
    headers: getHeaders(session),
  };
  const payload = {
    document_id: documentId,
  };
  return platform
    .get(PlatformServiceName.Http)
    .post('getaccept/upload-document', payload, options);
};
const removeDocument = async (platform, session, documentId) => {
  const options = {
    headers: getHeaders(session),
  };
  const payload = {
    document_id: documentId,
  };
  return platform
    .get(PlatformServiceName.Http)
    .post('getaccept/delete-document', payload, options);
};
const signup = async (platform, data) => {
  const payload = data;
  return platform
    .get(PlatformServiceName.Http)
    .post('getaccept/signup', payload);
};
const refreshToken = async (platform, session) => {
  const { access_token, expires_in } = session;
  return platform
    .get(PlatformServiceName.Http)
    .post('getaccept/refresh-token', {
    access_token: access_token,
    expires_in: expires_in,
  });
};

export { PlatformServiceName as P, fetchEntity as a, fetchSentDocuments as b, fetchDocumentDetails as c, removeDocument as d, fetchTemplates as e, fetchMe as f, fetchLimeDocuments as g, fetchTemplateFields as h, fetchObjectProps as i, fetchTemplateRoles as j, createDocument as k, sealDocument as l, fetchVideos as m, signup as n, refreshToken as r, switchEntity as s, uploadDocument as u };
