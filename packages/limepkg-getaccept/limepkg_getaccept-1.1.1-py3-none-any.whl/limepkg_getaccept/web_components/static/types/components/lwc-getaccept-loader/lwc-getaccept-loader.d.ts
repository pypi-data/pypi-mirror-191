import { LimePluginLoader, LimeWebComponentContext, LimeWebComponentPlatform } from '@limetech/lime-web-components-interfaces';
export declare class Loader implements LimePluginLoader {
  platform: LimeWebComponentPlatform;
  context: LimeWebComponentContext;
  componentWillLoad(): void;
  disconnectedCallback(): void;
  componentWillUpdate(): void;
}
