import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { EmptyState, LoadingState, PermissionDeniedState, SkeletonRows } from "./StateBlocks";

describe("state presentation primitives", () => {
  it("announces loading without exposing decorative icons", () => {
    const { container } = render(<LoadingState label="Loading exception queue" />);

    expect(screen.getByRole("status")).toHaveTextContent("Loading exception queue…");
    expect(container.querySelector("svg")).toHaveAttribute("aria-hidden", "true");
  });

  it("renders an empty-state action", () => {
    render(
      <EmptyState
        title="No exceptions"
        description="The deterministic sample returned no rows."
        action={<button type="button">Reset filters</button>}
      />,
    );

    expect(screen.getByText("No exceptions")).toBeVisible();
    expect(screen.getByRole("button", { name: "Reset filters" })).toBeEnabled();
  });

  it("keeps authorization ownership outside the presentation component", () => {
    render(<PermissionDeniedState resource="audit records" />);

    expect(screen.getByText("Access not available")).toBeVisible();
    expect(screen.getByText(/Entitlements are managed outside this console/)).toBeVisible();
  });

  it("hides skeleton rows from assistive technology", () => {
    const { container } = render(<SkeletonRows rows={3} />);

    expect(container.firstElementChild).toHaveAttribute("aria-hidden", "true");
    expect(container.firstElementChild?.children).toHaveLength(3);
  });
});
