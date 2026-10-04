import React, {useEffect, useMemo, useRef, useState} from "react";
import {ComponentContext, GenericBinder} from "@a2ui/web_core/rendering";
import {RICH_COMPONENT_RENDERERS} from "@agent-nebula/a2ui-rich";
import "@agent-nebula/a2ui-rich/styles.css";
import {createSurfaceProcessor, rendererDataModel} from "./surfaceState.js";


/**
 * Isolate strict A2UI validation/rendering failures from the host application.
 *
 * Invalid provider documents must remain visible as an A2UI failure while the
 * manager workflow, diagnostics and secure execution trace continue to work.
 */
class A2UIErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = {error: null};
  }

  static getDerivedStateFromError(error) {
    return {error};
  }

  componentDidCatch(error) {
    console.error("[A2UI] Provider surface rejected by strict v1.0 processing", error);
  }

  componentDidUpdate(previousProps) {
    if (previousProps.resetKey !== this.props.resetKey && this.state.error) {
      this.setState({error: null});
    }
  }

  render() {
    if (this.state.error) {
      return <div className="a2ui-error" role="alert"><strong>Agent-generated view unavailable</strong><span>{this.state.error.message}</span></div>;
    }
    return this.props.children;
  }
}

/*
 * React presentation adapter for registered A2UI v1.0 catalogs.
 *
 * @a2ui/web_core owns protocol validation, lifecycle/state, data binding,
 * two-way setters and standard action construction. This file deliberately
 * contains browser-native Basic Catalog presentation and delegates custom catalog components through a pluggable registry.
 */

/** Subscribe React to the official GenericBinder for one component model. */
function useBoundProperties(surface, component, basePath) {
  const binder = useMemo(() => {
    const api = component.catalog?.components.get(component.type)
      ?? surface.catalog.components.get(component.type);
    if (!api) return null;
    return new GenericBinder(new ComponentContext(surface, component.id, basePath), api.schema);
  }, [surface, component, basePath]);
  const [properties, setProperties] = useState(() => binder?.snapshot ?? component.properties);

  useEffect(() => {
    if (!binder) {
      setProperties(component.properties);
      return undefined;
    }
    setProperties(binder.snapshot);
    const subscription = binder.subscribe((next) => setProperties({...next}));
    return () => {
      subscription.unsubscribe();
      binder.dispose();
    };
  }, [binder, component]);

  return properties ?? {};
}

/** Convert a structural child reference into the renderer's common shape. */
function childRef(value, fallbackBasePath = "/") {
  if (typeof value === "string") return {id: value, basePath: fallbackBasePath};
  if (value && typeof value === "object" && typeof value.id === "string") {
    return {id: value.id, basePath: value.basePath ?? fallbackBasePath};
  }
  return null;
}

/** Render a list of static or template-expanded child references. */
function Children({surface, children, basePath = "/", presentation = null}) {
  const refs = Array.isArray(children) ? children : [];
  return refs.map((value, index) => {
    const ref = childRef(value, basePath);
    if (!ref) return null;
    const childPresentation = presentation ? {...presentation, index} : null;
    return <Component key={`${ref.id}:${ref.basePath}:${index}`} surface={surface} componentId={ref.id} basePath={ref.basePath} presentation={childPresentation}/>;
  });
}

/** Render one child reference. */
function Child({surface, child, basePath = "/"}) {
  const ref = childRef(child, basePath);
  return ref ? <Component surface={surface} componentId={ref.id} basePath={ref.basePath}/> : null;
}

/**
 * Infer richer presentation from an already validated Basic Catalog structure.
 *
 * A2UI v1.0 Basic Catalog intentionally has no Table component. Providers therefore
 * compose tables from Column -> Row -> Text primitives. This classifier operates only
 * on the validated web_core model and never changes or annotates the wire document.
 * Homogeneous rows with three or more text cells are presented as a data table; pairs
 * are presented as compact label/value fields. Other layouts retain generic rendering.
 */
function classifyColumn(surface, children, basePath) {
  if (!Array.isArray(children) || children.length < 2) return null;
  const rows = children.map((value) => {
    const ref = childRef(value, basePath);
    return ref ? surface.componentsModel.get(ref.id) : null;
  });
  if (rows.some((row) => row?.type !== "Row")) return null;

  const widths = rows.map((row) => Array.isArray(row.properties?.children) ? row.properties.children.length : 0);
  const columns = widths[0] ?? 0;
  if (columns < 2 || widths.some((width) => width !== columns)) return null;

  const textOnly = rows.every((row) => row.properties.children.every((value) => {
    const ref = childRef(value, basePath);
    return ref && surface.componentsModel.get(ref.id)?.type === "Text";
  }));
  if (!textOnly) return null;

  return {kind: columns >= 3 ? "table" : "fields", columns};
}

/** Browser-native rendering for one official Basic Catalog component. */
function Component({surface, componentId, basePath = "/", presentation = null}) {
  const component = surface.componentsModel.get(componentId);
  if (!component) return null;
  const props = useBoundProperties(surface, component, basePath);
  const weightStyle = props.weight == null ? undefined : {flexGrow: props.weight};

  switch (component.type) {
    case "Text":
      return <div className={`text text-${props.variant ?? "body"}`} style={weightStyle}>{props.text ?? "—"}</div>;
    case "Image":
      return <img className={`a2ui-image image-${props.variant ?? "mediumFeature"}`} src={props.url} alt={props.description ?? ""} style={{...weightStyle, objectFit: props.fit ?? "fill"}}/>;
    case "Icon":
      return <span className="a2ui-icon" style={weightStyle} aria-label={props.name}>{props.name}</span>;
    case "Video":
      return <video className="a2ui-media" controls src={props.url} poster={props.posterUrl} style={weightStyle}/>;
    case "AudioPlayer":
      return <audio className="a2ui-media" controls src={props.url} aria-label={props.description} style={weightStyle}/>;
    case "Row": {
      const rowClass = presentation?.kind === "table"
        ? `a2ui-table-row${presentation.index === 0 ? " a2ui-table-header" : ""}`
        : presentation?.kind === "fields" ? "a2ui-field-row" : "row";
      const rowStyle = presentation?.columns
        ? {...weightStyle, gridTemplateColumns: `repeat(${presentation.columns}, minmax(0, 1fr))`}
        : weightStyle;
      return <div className={`${rowClass} justify-${props.justify ?? "start"} align-${props.align ?? "stretch"}`} style={rowStyle}><Children surface={surface} children={props.children} basePath={basePath}/></div>;
    }
    case "Column": {
      const layout = classifyColumn(surface, props.children, basePath);
      if (layout?.kind === "table") {
        return <div className="a2ui-table-scroll" style={weightStyle}><div className="a2ui-table" role="table"><Children surface={surface} children={props.children} basePath={basePath} presentation={layout}/></div></div>;
      }
      if (layout?.kind === "fields") {
        return <div className="a2ui-fields" style={weightStyle}><Children surface={surface} children={props.children} basePath={basePath} presentation={layout}/></div>;
      }
      return <div className={`column justify-${props.justify ?? "start"} align-${props.align ?? "stretch"}`} style={weightStyle}><Children surface={surface} children={props.children} basePath={basePath}/></div>;
    }
    case "List":
      return <div className={`a2ui-list list-${props.direction ?? "vertical"} align-${props.align ?? "stretch"}`} style={weightStyle}><Children surface={surface} children={props.children} basePath={basePath}/></div>;
    case "Card":
      return <section className="card" style={weightStyle}><Child surface={surface} child={props.child} basePath={basePath}/></section>;
    case "Tabs":
      return <Tabs surface={surface} tabs={props.tabs} basePath={basePath} style={weightStyle}/>;
    case "Modal":
      return <Modal surface={surface} trigger={props.trigger} content={props.content} basePath={basePath} style={weightStyle}/>;
    case "Divider":
      return <hr className={`divider-${props.axis ?? "horizontal"}`} style={weightStyle}/>;
    case "Button":
      return <button className={`a2ui-button button-${props.variant ?? "default"}`} type="button" disabled={props.isValid === false} onClick={props.action} style={weightStyle}><Child surface={surface} child={props.child} basePath={basePath}/></button>;
    case "TextField":
      return <TextField props={props} style={weightStyle}/>;
    case "CheckBox":
      return <label className="a2ui-control a2ui-checkbox" style={weightStyle}><input type="checkbox" checked={Boolean(props.value)} onChange={(event) => props.setValue?.(event.target.checked)}/><span>{props.label}</span><ValidationErrors props={props}/></label>;
    case "ChoicePicker":
      return <ChoicePicker props={props} style={weightStyle}/>;
    case "Slider":
      return <label className="a2ui-control" style={weightStyle}><span>{props.label}</span><input type="range" min={props.min ?? 0} max={props.max} step={props.steps ? (props.max - (props.min ?? 0)) / props.steps : undefined} value={props.value ?? props.min ?? 0} onChange={(event) => props.setValue?.(Number(event.target.value))}/><output>{props.value}</output><ValidationErrors props={props}/></label>;
    case "DateTimeInput":
      return <DateTimeInput props={props} style={weightStyle}/>;
    default: {
      const RichComponent = RICH_COMPONENT_RENDERERS[component.type];
      return RichComponent
        ? <RichComponent surface={surface} component={component} basePath={basePath}/>
        : null;
    }
  }
}

/** Render validation errors produced by web_core check evaluation. */
function ValidationErrors({props}) {
  if (props.isValid !== false || !props.validationErrors?.length) return null;
  return <small className="a2ui-validation" role="alert">{props.validationErrors.join(" · ")}</small>;
}

/** Render the standard Basic Catalog TextField with two-way DataModel binding. */
function TextField({props, style}) {
  const type = props.variant === "number" ? "number" : props.variant === "obscured" ? "password" : "text";
  const input = props.variant === "longText"
    ? <textarea value={props.value ?? ""} placeholder={props.placeholder ?? ""} onChange={(event) => props.setValue?.(event.target.value)}/>
    : <input type={type} value={props.value ?? ""} placeholder={props.placeholder ?? ""} onChange={(event) => props.setValue?.(event.target.value)}/>;
  return <label className="a2ui-control" style={style}><span>{props.label}</span>{input}<ValidationErrors props={props}/></label>;
}

/** Render mutually-exclusive or multiple-selection Basic Catalog choices. */
function ChoicePicker({props, style}) {
  const selected = new Set(props.value ?? []);
  const multiple = props.variant === "multipleSelection";
  const update = (value, checked) => {
    const next = new Set(selected);
    if (multiple) checked ? next.add(value) : next.delete(value);
    else {
      next.clear();
      if (checked) next.add(value);
    }
    props.setValue?.([...next]);
  };
  return <fieldset className="a2ui-control a2ui-choice" style={style}><legend>{props.label}</legend>{(props.options ?? []).map((option) => <label key={option.value}><input type={multiple ? "checkbox" : "radio"} checked={selected.has(option.value)} onChange={(event) => update(option.value, event.target.checked)}/><span>{option.label}</span></label>)}<ValidationErrors props={props}/></fieldset>;
}

/** Render the Basic Catalog DateTimeInput using the enabled date/time dimensions. */
function DateTimeInput({props, style}) {
  const type = props.enableDate && props.enableTime ? "datetime-local" : props.enableTime ? "time" : "date";
  return <label className="a2ui-control" style={style}><span>{props.label}</span><input type={type} value={props.value ?? ""} min={props.min} max={props.max} onChange={(event) => props.setValue?.(event.target.value)}/><ValidationErrors props={props}/></label>;
}

/** Minimal local state required to present the standard Tabs component. */
function Tabs({surface, tabs = [], basePath, style}) {
  const [active, setActive] = useState(0);
  const selected = tabs[Math.min(active, Math.max(tabs.length - 1, 0))];
  return <section className="a2ui-tabs" style={style}><div className="a2ui-tab-list" role="tablist">{tabs.map((tab, index) => <button key={`${tab.title}:${index}`} type="button" role="tab" aria-selected={index === active} onClick={() => setActive(index)}>{tab.title}</button>)}</div>{selected && <div role="tabpanel"><Child surface={surface} child={selected.child} basePath={basePath}/></div>}</section>;
}

/** Minimal local visibility state required to present the standard Modal component. */
function Modal({surface, trigger, content, basePath, style}) {
  const [open, setOpen] = useState(false);
  return <div className="a2ui-modal" style={style}><span onClick={() => setOpen(true)}><Child surface={surface} child={trigger} basePath={basePath}/></span>{open && <div className="a2ui-modal-backdrop" role="presentation" onClick={() => setOpen(false)}><section className="a2ui-modal-content" role="dialog" aria-modal="true" onClick={(event) => event.stopPropagation()}><button className="a2ui-modal-close" type="button" onClick={() => setOpen(false)}>Close</button><Child surface={surface} child={content} basePath={basePath}/></section></div>}</div>;
}

/** Render one official SurfaceModel from its reserved root component. */
function Surface({surface}) {
  if (!surface.componentsModel.get("root")) return null;
  return <article className="a2ui-surface" data-surface-id={surface.id}><Component surface={surface} componentId="root"/></article>;
}

/** Render provider-owned A2UI v1.0 messages using the official web_core engine. */
function A2UIRendererContent({ui, onAction}) {
  const processorRef = useRef(null);
  const actionRef = useRef(onAction);
  const [revision, setRevision] = useState(0);
  actionRef.current = onAction;

  if (!processorRef.current) {
    let processor;
    processor = createSurfaceProcessor([], async (action) => {
      await actionRef.current?.(action, rendererDataModel(processor));
    });
    processorRef.current = processor;
  }

  const processor = processorRef.current;
  const messages = useMemo(() => Array.isArray(ui) ? ui : [], [ui]);

  useEffect(() => {
    if (!messages.length) return;
    // Keep one processor for the interaction. Incremental provider messages
    // must update surfaces created by earlier A2UI responses.
    processor.processMessages(messages);
    setRevision((value) => value + 1);
  }, [processor, messages]);

  useEffect(() => () => processor.dispose(), [processor]);

  const surfaces = [...processor.getSurfaces().values()];
  if (!surfaces.length) return null;
  return <div className="a2ui-surfaces" data-revision={revision}>{surfaces.map((surface) => <Surface key={surface.id} surface={surface}/>)}</div>;
}

/** Render provider-owned A2UI without allowing one invalid stream to blank the host UI. */
export function A2UIRenderer({ui, onAction}) {
  const resetKey = useMemo(() => Array.isArray(ui) ? ui.length : 0, [ui]);
  return <A2UIErrorBoundary resetKey={resetKey}><A2UIRendererContent ui={ui} onAction={onAction}/></A2UIErrorBoundary>;
}
