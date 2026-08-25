import { render } from "@testing-library/react";
import { axe } from "jest-axe";
import { describe, expect, it } from "vitest";
import { CategoryBars } from "@/components/overview/CategoryBars";
import { ExceptionTable } from "@/components/overview/ExceptionTable";
import { QueueLaneList } from "@/components/overview/QueueLaneList";
import { Panel } from "@/components/primitives/Panel";
import { categoryBreakdown, queueLanes, recentExceptions } from "@/data/overview";

describe("accessibility smoke coverage", () => {
  it("reports no automated violations in the overview content", async () => {
    const { container } = render(
      <main aria-label="Synthetic trade operations overview">
        <Panel title="Recent exceptions" description="Deterministic synthetic fixture.">
          <ExceptionTable rows={recentExceptions} />
        </Panel>
        <Panel title="Exception categories">
          <CategoryBars items={categoryBreakdown} />
        </Panel>
        <Panel title="Queue lanes">
          <QueueLaneList lanes={queueLanes} />
        </Panel>
      </main>,
    );

    const results = await axe(container);
    expect(results.violations).toEqual([]);
  });
});
