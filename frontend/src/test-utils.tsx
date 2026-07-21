import React from "react";
import { render as rtlRender, RenderOptions } from "@testing-library/react";

const render = (
  ui: React.ReactElement,
  options?: Omit<RenderOptions, "wrapper">,
) => rtlRender(ui, { ...options });

export * from "@testing-library/react";
export { render };
