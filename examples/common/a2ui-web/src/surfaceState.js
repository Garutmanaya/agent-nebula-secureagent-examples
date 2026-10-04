import {MessageProcessor, STRICT_VALIDATION} from "@a2ui/web_core/processing";
import {SUPPORTED_CATALOGS} from "./catalogs.js";

export function createSurfaceProcessor(messages, actionHandler) {
  const processor = new MessageProcessor(SUPPORTED_CATALOGS, actionHandler, {
    version: "v1.0",
    validationConfig: {...STRICT_VALIDATION, targetVersion: "v1.0"},
  });
  processor.processMessages(messages);
  return processor;
}
