import { EventEmitter } from '../../stencil-public-runtime';
import { IDocument } from '../../types/Document';
import { IListItem } from '../../types/ListItem';
import { LimeWebComponentPlatform } from '@limetech/lime-web-components-interfaces';
import { ISession } from '../../types/Session';
export declare class LayoutSendDocument {
  document: IDocument;
  template: IListItem;
  limeDocument: IListItem;
  platform: LimeWebComponentPlatform;
  session: ISession;
  setNewDocumentName: EventEmitter<string>;
  setDocumentValue: EventEmitter<number>;
  setIsSmsSending: EventEmitter<boolean>;
  setSmartReminder: EventEmitter<boolean>;
  private documentName;
  private value;
  private smartReminder;
  private sendLinkBySms;
  private documentVideo;
  changeView: EventEmitter;
  removeVideo: EventEmitter;
  componentWillLoad(): void;
  componentDidUpdate(): void;
  constructor();
  render(): any[];
  private fileName;
  private handleChangeDocumentName;
  private handleChangeValue;
  private handleChangeSmartReminder;
  private handleChangeSendLinkBySms;
  private handleAddVideo;
  private handleRemoveVideo;
}
