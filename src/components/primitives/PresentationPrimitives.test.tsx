import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { MetricTile } from "./MetricTile";
import { PageHeader } from "./PageHeader";
import { Panel } from "./Panel";

describe("presentation primitives", () => {
  it("renders metric units and optional state badge", () => {
    const { rerender } = render(
      <MetricTile label="Queue age" value="12" unit="min" note="Synthetic fixture" badge="Ready" />,
    );
    expect(screen.getByText("min")).toBeVisible();
    expect(screen.getByText("Ready")).toBeVisible();

    rerender(<MetricTile label="Queue age" value="12" note="Synthetic fixture" />);
    expect(screen.queryByText("min")).not.toBeInTheDocument();
    expect(screen.queryByText("Ready")).not.toBeInTheDocument();
  });

  it("renders header metadata and actions only when supplied", () => {
    const { rerender } = render(
      <PageHeader
        title="Title"
        summary="Summary"
        meta={<span>Metadata</span>}
        actions={<button>Act</button>}
      />,
    );
    expect(screen.getByText("Metadata")).toBeVisible();
    expect(screen.getByRole("button", { name: "Act" })).toBeVisible();

    rerender(<PageHeader title="Title" summary="Summary" />);
    expect(screen.queryByText("Metadata")).not.toBeInTheDocument();
    expect(screen.queryByRole("button", { name: "Act" })).not.toBeInTheDocument();
  });

  it("supports descriptive, actionable, and flush panel variants", () => {
    const { rerender } = render(
      <Panel title="Evidence" description="Grounded" actions={<button>Review</button>} flush>
        Body
      </Panel>,
    );
    expect(screen.getByText("Grounded")).toBeVisible();
    expect(screen.getByRole("button", { name: "Review" })).toBeVisible();

    rerender(<Panel title="Evidence">Body</Panel>);
    expect(screen.queryByText("Grounded")).not.toBeInTheDocument();
    expect(screen.queryByRole("button", { name: "Review" })).not.toBeInTheDocument();
  });
});
