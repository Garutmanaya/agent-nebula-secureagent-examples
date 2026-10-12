import {Catalog} from "@a2ui/web_core/catalog";
import {BASIC_COMPONENTS} from "@a2ui/web_core/v1_0/basic_catalog";
import {RICH_CATALOG} from "@agent-nebula-npm/a2ui-rich";

export const BASIC_CATALOG_ID =
  "https://a2ui.org/specification/v1_0/catalogs/basic/catalog.json";

export const BASIC_CATALOG = new Catalog(
  BASIC_CATALOG_ID, "v1.0", BASIC_COMPONENTS, [],
);

// Register both catalogs once. A presentation chooses the components it uses.
// This keeps the browser unchanged for Basic-only and mixed-catalog examples.
export const SUPPORTED_CATALOGS = [BASIC_CATALOG, RICH_CATALOG];
