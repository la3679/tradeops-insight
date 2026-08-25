import { render, screen, within } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { categoryBreakdown, queueLanes, recentExceptions } from "@/data/overview";
import { CategoryBars } from "./CategoryBars";
import { ExceptionTable } from "./ExceptionTable";
import { QueueLaneList } from "./QueueLaneList";

describe("overview presentation components", () => {
  it("renders the synthetic exception fixture as a semantic table", () => {
    render(<ExceptionTable rows={recentExceptions} />);

    const table = screen.getByRole("table", {
      name: "Most recent synthetic trade exceptions from a fixed sample fixture",
    });
    const bodyRows = within(table).getAllByRole("row").slice(1);
    const [firstException] = recentExceptions;

    if (!firstException) {
      throw new Error("The deterministic exception fixture must contain at least one row.");
    }

    expect(within(table).getByRole("columnheader", { name: "Reference" })).toBeVisible();
    expect(within(table).getByRole("columnheader", { name: "Review state" })).toBeVisible();
    expect(bodyRows).toHaveLength(recentExceptions.length);
    expect(within(table).getByRole("rowheader", { name: firstException.id })).toBeVisible();
  });

  it("gives every category bar a text alternative", () => {
    render(<CategoryBars items={categoryBreakdown} />);

    for (const item of categoryBreakdown) {
      expect(
        screen.getByRole("img", {
          name: `${item.category}: ${item.count} items, ${item.share} percent of the sample`,
        }),
      ).toBeVisible();
    }
  });

  it("renders every deterministic queue lane", () => {
    render(<QueueLaneList lanes={queueLanes} />);

    for (const lane of queueLanes) {
      const laneName = screen.getByText(lane.name);
      const laneRow = laneName.closest("li");
      expect(laneName).toBeVisible();
      expect(laneRow).not.toBeNull();
      expect(within(laneRow as HTMLElement).getByText(`${lane.open} open items`)).toBeVisible();
    }
  });
});
