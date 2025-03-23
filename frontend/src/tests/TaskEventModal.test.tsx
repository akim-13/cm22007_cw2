import React from "react";
import { render, screen } from "@testing-library/react";
import TaskEventModal from "../components/TaskEventModal";
import "@testing-library/jest-dom";

describe("TaskEventModal", () => {
  test("renders modal title", () => {
    render(
      <TaskEventModal
        events={[]}
        setEvents={jest.fn()}
        isModalOpen={true}
        setIsModalOpen={jest.fn()}
        newFCEvent={{ current: {} }}
        initialExtendedProps={{}}
        isTaskMode={true}
        setIsTaskMode={jest.fn()}
      />
    );

    expect(screen.getByText(/Manage Task/i)).toBeInTheDocument();
  });
});
